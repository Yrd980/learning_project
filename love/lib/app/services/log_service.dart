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
        logLevel = LogLevel.info;
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

  Future<void> _checkAndCleanupBySize() async {
    try {
      final currentSize = await getLogDatabaseSize();
      final maxSize = CommonConstants.maxLogDatabaseSize;

      if (currentSize < maxSize * 0.9) {
        return;
      }

      final timeRangeResult = _db.prepare('''
        SELECT
          MIN(timestamp) as min_time,
          MAX(timestamp) as max_time
        FROM app_logs
      ''').select();

      if (timeRangeResult.isEmpty) {
        return;
      }

      final minTime = timeRangeResult.first['min_time'] as int? ?? 0;
      final maxTime = timeRangeResult.first['max_time'] as int? ?? 0;

      if (minTime == 0 || maxTime == 0 || minTime >= maxTime) {
        await _deleteOldestRecords(currentSize, maxSize);
        return;
      }

      final timeSpan = maxTime - minTime;

      final targetRententionRio = 0.8;

      final newCutoffTimestamp =
          minTime + (timeSpan * (1 - targetRententionRio)).toInt();

      final countResult = _db
          .prepare('''
        SELECT COUNT(*) as count FROM app_logs
        WHERE timestamp < ?
      ''')
          .select([newCutoffTimestamp]);

      final count = countResult.isEmpty
          ? 0
          : (countResult.first['count'] as int? ?? 0);

      if (count > 0) {
        _db
            .prepare('''
          DELETE FROM app_logs
          WHERE timestamp < ?
        ''')
            .execute([newCutoffTimestamp]);

        final sizeBeforeMB = (currentSize / (1024 * 1024)).toStringAsFixed(2);

        await addLog(
          level: LogLevel.info,
          tag: "log system",
          message:
              "databse size at $sizeBeforeMB MB contain ${maxSize / (1024 * 1024)} MB have clean $count old log record",
        );

        _db.execute('VACUUM');
      }
    } catch (e) {
      if (kDebugMode) {
        print("clean log fail base size: $e");
      }
    }
  }

  Future<void> _checkDatabaseSizeBeforeAdd() async {
    try {
      if (_db
                  .prepare('SELECT MAX(id) as max_id FROM app_logs')
                  .select()
                  .first['max_id'] %
              100 !=
          0) {
        return;
      }

      await _checkAndCleanupBySize();
    } catch (e) {
      if (kDebugMode) {
        print("check database size fail: $e");
      }
    }
  }

  Future<void> _deleteOldestRecords(int currentSize, int maxSize) async {
    try {
      final targetDeleteRatio = 0.2;

      final countResult = _db
          .prepare('SELECT COUNT(*) as count FROM app_logs')
          .select();
      final totalCount = countResult.isEmpty
          ? 0
          : (countResult.first['count'] as int? ?? 0);

      if (totalCount == 0) {
        return;
      }

      final recordsToDelete = (totalCount * targetDeleteRatio).ceil();

      final idsToDeleteResult = _db
          .prepare('''
        SELECT id FROM app_logs
        ORDER BY timestamp ASC 
        LIMIT ?
      ''')
          .select([recordsToDelete]);

      if (idsToDeleteResult.isEmpty) {
        return;
      }

      final idsToDelete = idsToDeleteResult
          .map((row) => row['id'] as int)
          .toList();

      final batchSize = 1000;

      for (var i = 0; i < idsToDelete.length; i += batchSize) {
        final end = (i + batchSize < idsToDelete.length)
            ? i + batchSize
            : idsToDelete.length;
        final batch = idsToDelete.sublist(i, end);
        final placeholders = List.filled(batch.length, '?').join(',');

        _db
            .prepare('''
          DELETE FROM app_logs
          WHERE id in ($placeholders)
        ''')
            .execute(batch);
      }

      final sizeBeforeMB = (currentSize / (1024 * 1024)).toStringAsFixed(2);

      await addLog(
        level: LogLevel.info,
        tag: "log system",
        message:
            "database size obtain $sizeBeforeMB MB，near ${maxSize / (1024 * 1024)} MB，clean $recordsToDelete line early log record",
      );

      _db.execute('VACUUM');
    } catch (e) {
      if (kDebugMode) {
        print("delete old log fail: $e");
      }
    }
  }

  Future<int> getLogDatabaseSize() async {
    try {
      await _flushBuffer();

      final sizeResult = _db.prepare('''
        SELECT
          COUNT(*) as row_count,
          AVG(LENGTH(message) + LENGTH(IFNULL(details,'')) + LENGTH(IFNULL(tag,''))) as avg_size 
        FROM app_logs
      ''').select();

      if (sizeResult.isEmpty) {
        return 0;
      }

      final rowCount = sizeResult.first['row_count'] as int? ?? 0;
      final avgSize = sizeResult.first['avg_size'] as double? ?? 0;

      return (rowCount * avgSize).toInt();
    } catch (e) {
      if (kDebugMode) {
        print("get log database size fail: $e");
      }
      return 0;
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

  void addLogSync({
    required LogLevel level,
    String? tag,
    required String message,
    String? details,
  }) {
    try {
      final now = DateTime.now();
      final timestamp = now.millisecondsSinceEpoch ~/ 1000;

      _insertLogStmt.execute([
        timestamp,
        LogEntry.levelToString(level),
        tag,
        message,
        details,
        _sessionId,
      ]);
    } catch (e) {
      if (kDebugMode) {
        print("sync add log error: $e");
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

  Future<void> flushBufferToDatabase() async {
    return _flushBuffer();
  }

  Future<bool> forceCheckAndCleanupBySize() async {
    try {
      final currentSize = await getLogDatabaseSize();

      final maxSize = CommonConstants.maxLogDatabaseSize;

      if (currentSize > maxSize) {
        final targetDeleteRatio = Math.max(0.3, 1 - (maxSize / currentSize));

        final countResult = _db
            .prepare('SELECT COUNT(*) as count FROM app_logs')
            .select();
        final totalCount = countResult.isEmpty
            ? 0
            : (countResult.first['count'] as int? ?? 0);

        if (totalCount == 0) return false;

        final recordsToDelete = (totalCount * targetDeleteRatio).ceil();

        final idsToDeleteResult = _db
            .prepare('''
          SELECT id FROM app_logs 
          ORDER BY timestamp ASC 
          LIMIT ?
        ''')
            .select([recordsToDelete]);

        if (idsToDeleteResult.isEmpty) return false;

        final idsToDelete = idsToDeleteResult
            .map((row) => row['id'] as int)
            .toList();

        final batchSize = 1000;
        for (var i = 0; i < idsToDelete.length; i += batchSize) {
          final end = (i + batchSize < idsToDelete.length)
              ? i + batchSize
              : idsToDelete.length;
          final batch = idsToDelete.sublist(i, end);

          final placeholders = List.filled(batch.length, '?').join(',');

          _db
              .prepare('''
            DELETE FROM app_logs 
            WHERE id IN ($placeholders)
          ''')
              .execute(batch);
        }

        final sizeBeforeMB = (currentSize / (1024 * 1024)).toStringAsFixed(2);

        await addLog(
          level: LogLevel.info,
          tag: "log system",
          message:
              "databse size at $sizeBeforeMB MB contain ${maxSize / (1024 * 1024)} MB have clean $recordsToDelete old log record",
        );

        _db.execute('VACUUM');

        return true;
      } else {
        await _checkAndCleanupBySize();
        return false;
      }
    } catch (e) {
      if (kDebugMode) {
        print("force clean log fail: $e");
      }
      return false;
    }
  }

  Future<List<LogEntry>> queryLogs({
    DateTime? startDate,
    DateTime? endDate,
    List<LogLevel>? levels,
    String? tag,
    String? searchText,
    String? sessionId,
    int limit = 1000,
    int offset = 0,
  }) async {
    try {
      final List<dynamic> params = [];
      final List<String> conditions = [];

      if (startDate != null) {
        conditions.add('timestamp >= ?');
        params.add(startDate.millisecondsSinceEpoch ~/ 1000);
      }

      if (endDate != null) {
        final endOfDay = DateTime(
          endDate.year,
          endDate.month,
          endDate.day,
          23,
          59,
          59,
        );
        conditions.add('timestamp <= ?');
        params.add(endOfDay.millisecondsSinceEpoch ~/ 1000);
      }

      if (levels != null && levels.isNotEmpty) {
        final levelStrings = levels
            .map((l) => LogEntry.levelToString(l))
            .toList();
        final placeholders = List.generate(
          levelStrings.length,
          (index) => '?',
        ).join(',');
        conditions.add('level IN ($placeholders)');
        params.addAll(levelStrings);
      }

      if (tag != null && tag.isNotEmpty) {
        conditions.add('tag = ?');
        params.add(tag);
      }

      if (searchText != null && searchText.isNotEmpty) {
        conditions.add('(message LIKE ? OR details LIKE ?)');
        params.add('%$searchText%');
        params.add('%$searchText%');
      }

      if (sessionId != null && sessionId.isNotEmpty) {
        conditions.add('session_id = ?');
        params.add(sessionId);
      }

      String sql =
          '''
        SELECT * FROM app_logs
        ${conditions.isNotEmpty ? 'WHERE ${conditions.join(' AND ')}' : ''}
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
      ''';
      params.addAll([limit, offset]);

      final results = _db.prepare(sql).select(params);

      return results.map((row) => LogEntry.fromJson(row)).toList();
    } catch (e) {
      if (kDebugMode) {
        print("query log fail: $e");
      }
      return [];
    }
  }

  Future<List<DateTime>> getLogDates() async {
    try {
      final sql = '''
        SELECT DISTINCT 
          date(timestamp, 'unixepoch', 'localtime') as log_date
        FROM app_logs
        ORDER BY log_date DESC
      ''';

      final results = _db.prepare(sql).select();

      if (results.isEmpty) {
        await addLog(
          level: LogLevel.info,
          tag: "system",
          message: "get log date list",
        );

        await _flushBuffer();

        final retryResults = _db.prepare(sql).select();
        if (retryResults.isEmpty) {
          return [];
        }

        return retryResults.map((row) {
          final dateStr = row['log_date'] as String;
          return DateTime.parse(dateStr);
        }).toList();
      }

      return results.map((row) {
        final dateStr = row['log_date'] as String;
        return DateTime.parse(dateStr);
      }).toList();
    } catch (e) {
      if (kDebugMode) {
        print("获取日志日期列表失败: $e");
      }
      return [];
    }
  }

  String get currentSessionId => _sessionId;

  Future<File> exportLogsToFile({
    required String targetPath,
    DateTime? startDate,
    DateTime? endDate,
    List<LogLevel>? levels,
    String? tag,
    String? searchText,
    String? sessionId,
    bool mergeAllDates = false,
  }) async {
    try {
      await _flushBuffer();

      final logs = await queryLogs(
        startDate: startDate,
        endDate: endDate,
        levels: levels,
        tag: tag,
        searchText: searchText,
        sessionId: sessionId,
        limit: 50000,
      );

      if (logs.isEmpty) {
        throw Exception("not find");
      }

      final targetFile = File(targetPath);
      final targetDir = Directory(path.dirname(targetPath));
      if (!await targetDir.exists()) {
        await targetDir.create(recursive: true);
      }

      final buffer = StringBuffer();
      buffer.writeln("===== export time: ${DateTime.now()} =====");

      if (!mergeAllDates && (startDate != null || endDate != null)) {
        buffer.write("===== date range: ");
        if (startDate != null) {
          buffer.write("${startDate.toString().split(' ')[0]} ");
        }
        buffer.write("to ");
        if (endDate != null) {
          buffer.write("${endDate.toString().split(' ')[0]}");
        } else {
          buffer.write("today");
        }
        buffer.writeln(" =====");
      }

      buffer.writeln("===== total logs: ${logs.length} =====");
      buffer.writeln();

      final chunkSize = 1000;
      for (var i = 0; i < logs.length; i += chunkSize) {
        final end = (i + chunkSize < logs.length) ? i + chunkSize : logs.length;
        final chunk = logs.sublist(i, end);

        for (final log in chunk) {
          buffer.writeln(log.toFormattedString());
        }

        if (i == 0) {
          await targetFile.writeAsString(buffer.toString());
          buffer.clear();
        } else {
          await targetFile.writeAsString(
            buffer.toString(),
            mode: FileMode.append,
          );
          buffer.clear();
        }
      }

      return targetFile;
    } catch (e) {
      if (kDebugMode) {
        print("export log error: $e");
      }
      rethrow;
    }
  }

  Future<void> clearLogs({
    DateTime? beforeDate,
    List<LogLevel>? levels,
    String? tag,
  }) async {
    try {
      await _flushBuffer();

      final List<dynamic> params = [];
      final List<String> conditions = [];

      if (beforeDate != null) {
        conditions.add('timestamp < ?');
        params.add(beforeDate.millisecondsSinceEpoch ~/ 1000);
      }

      if (levels != null && levels.isNotEmpty) {
        final levelStrings = levels
            .map((l) => LogEntry.levelToString(l))
            .toList();
        final placeholders = List.generate(
          levelStrings.length,
          (index) => '?',
        ).join(',');
        conditions.add('level IN ($placeholders)');
        params.addAll(levelStrings);
      }

      if (tag != null && tag.isNotEmpty) {
        conditions.add('tag = ?');
        params.add(tag);
      }

      String sql =
          '''
        DELETE FROM app_logs
        ${conditions.isNotEmpty ? 'WHERE ${conditions.join(' AND ')}' : ''}
      ''';

      String countSql =
          '''
        SELECT COUNT(*) as count FROM app_logs
        ${conditions.isNotEmpty ? 'WHERE ${conditions.join(' AND ')}' : ''}
      ''';

      final countResult = _db.prepare(countSql).select(params);
      final count = countResult.isEmpty
          ? 0
          : (countResult.first['count'] as int? ?? 0);

      _db.prepare(sql).execute(params);

      _buffer.clear();

      await addLog(
        level: LogLevel.info,
        tag: "system",
        message: "log cleaned，clean $count line record",
      );

      await _flushBuffer();
    } catch (e) {
      if (kDebugMode) {
        print("clean log fail: $e");
      }
    }
  }

  Future<Map<String, int>> getLogStats() async {
    try {
      await _flushBuffer();

      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);
      final lastWeek = today.subtract(const Duration(days: 7));

      final todayTimestamp = today.millisecondsSinceEpoch ~/ 1000;
      final lastWeekTimestamp = lastWeek.millisecondsSinceEpoch ~/ 1000;

      final stats = _db
          .prepare('''
        SELECT
          (SELECT COUNT(*) FROM app_logs WHERE timestamp >= ?) as today_count,
          (SELECT COUNT(*) FROM app_logs WHERE timestamp >= ?) as week_count,
          (SELECT COUNT(*) FROM app_logs) as total_count
      ''')
          .select([todayTimestamp, lastWeekTimestamp]);

      if (stats.isEmpty) {
        return {'today': 0, 'week': 0, 'total': 0};
      }

      return {
        'today': stats.first['today_count'] as int? ?? 0,
        'week': stats.first['week_count'] as int? ?? 0,
        'total': stats.first['total_count'] as int? ?? 0,
      };
    } catch (e) {
      if (kDebugMode) {
        print('get log count fail: $e');
      }
      return {'today': 0, 'week': 0, 'total': 0};
    }
  }

  Future<void> close() async {
    _flushTimer?.cancel();
    _flushTimer = null;

    await _flushBuffer();

    _insertLogStmt.dispose();
  }

  Future<int> getLogCount() async {
    try {
      await _flushBuffer();

      final result = _db
          .prepare('SELECT COUNT(*) as count FROM app_logs')
          .select();
      return result.isEmpty ? 0 : (result.first['count'] as int? ?? 0);
    } catch (e) {
      if (kDebugMode) {
        print("get log count fail: $e");
      }
      return 0;
    }
  }

  Future<String> getDatabaseDirectory() async {
    try {
      final documentsDirectory = await getApplicationDocumentsDirectory();
      final appDir = path.join(
        documentsDirectory.path,
        CommonConstants.applicationName ?? 'i_iwara',
      );
      return appDir;
    } catch (e) {
      if (kDebugMode) {
        print("get database path fail: $e");
      }
      throw Exception("get database path fail: $e");
    }
  }

  CommonDatabase get database => _db;

  Future<void> vacuum() async {
    try {
      await _flushBuffer();

      _db.execute('VACUUM');

      await addLog(
        level: LogLevel.info,
        tag: "system",
        message: "execute VACUUM",
      );
    } catch (e) {
      if (kDebugMode) {
        print("execute VACUUM fail: $e");
      }
    }
  }
}
