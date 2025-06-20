import 'dart:async';
import 'dart:collection';
import 'dart:io';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:i_iwara/db/database_service.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'package:sqlite3/common.dart';
import 'package:i_iwara/common/constants.dart';
import 'dart:math' as Math;

enum LogLevel { debug, info, warn, error }

class LogEntry {
  final int? id;
  final DateTime timestamp;
  final LogLevel level;
  final String? tag;
  final String message;
  final String? details;
  final String? sessionId;
  final DateTime? createdAt;

  LogEntry({
    this.id,
    required this.timestamp,
    required this.level,
    this.tag,
    required this.message,
    this.details,
    this.sessionId,
    this.createdAt,
  });

  factory LogEntry.fromJson(Map<String, dynamic> json) {
    LogLevel logLevel;
    final levelStr = (json['level'] as String).toLowerCase();
    switch (levelStr) {
      case 'debug':
        logLevel = LogLevel.debug;
        break;
      case 'info':
        logLevel = LogLevel.info;
        break;
      case 'warn':
        logLevel = LogLevel.warn;
        break;
      case 'error':
        logLevel = LogLevel.error;
        break;
      default:
        logLevel = LogLevel.info; // 默认为info级别
    }

    return LogEntry(
      id: json['id'] as int?,
      timestamp: DateTime.fromMillisecondsSinceEpoch(
        (json['timestamp'] as int) * 1000,
      ),
      level: logLevel,
      tag: json['tag'] as String?,
      message: json['message'] as String,
      details: json['details'] as String?,
      sessionId: json['session_id'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.fromMillisecondsSinceEpoch(
              (json['created_at'] as int) * 1000,
            )
          : null,
    );
  }

  String toFormattedString() {
    final timeStr = timestamp.toString().substring(0, 19);
    final levelStr = level.name.toUpperCase();
    final tagStr = tag != null ? "[$tag]" : "";
    final detailsStr = details != null ? "\n$details" : "";

    return "[$timeStr][$levelStr]$tagStr $message$detailsStr";
  }

  static String levelToString(LogLevel level) => level.name;
}

class LogService extends GetxService {
  late final CommonDatabase _db;

  final String _sessionId = const Uuid().v4();

  final Queue<LogEntry> _buffer = Queue();

  static const int _maxBufferSize = 100;

  Timer? _flushTimer;

  final _bufferLock = RxBool(false);

  DateTime? _lastCleanupTime;

  static const int _cleanupIntervalHours = 24;

  static LogService get to => Get.find();

  late final dynamic _insertLogStmt;

  Future<LogService> init() async {
    try {
      _db = await DatabaseService().initLogDatabase();

      _insertLogStmt = _db.prepare('''
        INSERT INTO app_logs
        (timestamp, level, tag, message, details, session_id)
        VALUES(?,?,?,?,?,?)
      ''');

      _startFlushTimer();

      unawaited(_cleanupOldLogs());
      unawaited(_checkAndCleanupBySize());

      await addLog(
        level: LogLevel.info,
        tag: "system",
        message: "log system init success - use independant database",
      );

      await _flushBuffer();
      return this;
    } catch (e) {
      if (kDebugMode) {
        print("log system init error: $e");
      }
      rethrow;
    }
  }

  void _startFlushTimer() {
    _flushTimer?.cancel();
    _flushTimer = Timer.periodic(
      const Duration(seconds: 10),
      (_) => _flushBuffer(),
    );
  }

  Future<void> _cleanupOldLogs() async {
    final now = DateTime.now();
    if (_lastCleanupTime != null &&
        now.difference(_lastCleanupTime!).inHours < _cleanupIntervalHours) {
      return;
    }

    try {
      final retentionDays = CommonConstants.logRetentionDays;

      final cutoffDate = now.subtract(Duration(days: retentionDays));

      final cutoffTimestamp = cutoffDate.millisecondsSinceEpoch ~/ 1000;

      final countResult = _db
          .prepare('''
        SELECT COUNT(*) as count FROM app_logs
        WHERE timestamp < ?
      ''')
          .select([cutoffTimestamp]);

      final count = countResult.isEmpty
          ? 0
          : (countResult.first['count'] as int? ?? 0);

      if (count > 0) {
        _db
            .prepare('''
          DELETE FROM app_logs
          WHERE timestamp < ?
        ''')
            .execute([cutoffTimestamp]);

        await addLog(
          level: LogLevel.info,
          tag: "log system",
          message:
              "auto clean $count lines more than $retentionDays days log record",
        );
      }

      _lastCleanupTime = now;
    } catch (e) {
      if (kDebugMode) {
        print("clean outdated log error: $e");
      }
    }
  }

  Future<void> addLog({
    required LogLevel level,
    String? tag,
    required String message,
    String? details,
  }) async {
    try {
      if (!CommonConstants.enableLogPersistence && level != LogLevel.error) {
        return;
      }

      final now = DateTime.now();

      final entry = LogEntry(
        timestamp: now,
        level: level,
        tag: tag,
        message: message,
        details: details,
        sessionId: _sessionId,
      );

      _buffer.add(entry);

      if (_buffer.length >= _maxBufferSize) {
        unawaited(_flushBuffer());
      }

      if (level == LogLevel.info) {
        unawaited(_checkDatabaseSizeBeforeAdd());
      }
    } catch (e) {
      if (kDebugMode) {
        print("add log error: $e");
        print("try to add log info: $message");
      }
    }
  }

  Future<void> _flushBuffer() async {
    if (_buffer.isEmpty || _bufferLock.value) {
      return;
    }

    _bufferLock.value = true;
    try {
      _db.execute('BEGIN TRANSACTION');

      try {
        final batch = List.from(_buffer);
        _buffer.clear();

        for (final entry in batch) {
          _insertLogStmt.execute([
            entry.timestamp.millisecondsSinceEpoch ~/ 1000,
            LogEntry.levelToString(entry.level),
            entry.tag,
            entry.message,
            entry.details,
            entry.sessionId,
          ]);
        }
        _db.execute('COMMIT');
      } catch (e) {
        _db.execute('ROLLBACK');
        if (kDebugMode) {
          print("write log to database error : $e");
        }

        if (_buffer.isEmpty) {
          final failedBatch = _db
              .prepare('SELECT MAX(id) as max_id FROM app_logs')
              .select();
          final lastId = failedBatch.isEmpty
              ? 0
              : (failedBatch.first['max_id'] as int? ?? 0);

          final now = DateTime.now();
          final oneMinuteAgo = now.subtract(const Duration(minutes: 1));

          final recentLogsCount = _db
              .prepare('''
            SELECT COUNT(*) as count FROM app_logs
            WHERE timestap >= ?
          ''')
              .select([oneMinuteAgo.millisecondsSinceEpoch ~/ 1000]);

          final count = recentLogsCount.isEmpty
              ? 0
              : (recentLogsCount.first['count'] as int? ?? 0);

          if (count < 100) {
            final errorEntry = LogEntry(
              timestamp: now,
              level: LogLevel.error,
              tag: "log system",
              message: "fail to write log to database ",
              details: "error info : $e",
              sessionId: _sessionId,
            );
            _buffer.add(errorEntry);
          }
        }
      }
    } finally {
      _bufferLock.value = false;
    }
  }
}
