import 'dart:io';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:sqlite3/common.dart' show CommonDatabase;
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:i_iwara/common/constants.dart';

import 'migration_manager.dart';
import 'sqlite3/sqlite3.dart' show openSqliteDb;

class DatabaseException implements Exception {
  final String message;

  DatabaseException(this.message);

  @override
  String toString() => 'database error: $message';
}

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();

  factory DatabaseService() => _instance;

  DatabaseService._internal();
  late CommonDatabase _db;
  CommonDatabase? _logDb;
  final MigrationManager _migrationManager = MigrationManager();

  Future<void> init() async {
    try {
      _db = await openSqliteDb();
    } catch (e) {
      LogUtils.e('database init error', tag: 'DatabaseService', error: e);
      throw DatabaseException('database init fail: $e');
    }
  }

  CommonDatabase get database => _db;

  Future<CommonDatabase> initLogDatabase() async {
    if (_logDb != null) {
      return _logDb!;
    }

    try {
      final appDocDir = await getApplicationDocumentsDirectory();
      final dbDir = path.join(
        appDocDir.path,
        CommonConstants.applicationName ?? 'i_iwara',
      );

      await Directory(dbDir).create(recursive: true);

      final logDbPath = path.join(dbDir, 'iwara_logs.db');

      _logDb = await openSqliteDb(customPath: logDbPath);

      _initLogTable(_logDb!);

      LogUtils.i('log database init success', 'DatabaseService');

      return _logDb!;
    } catch (e) {
      LogUtils.e('log database init fail', tag: 'DatabaseService', error: e);
      throw DatabaseException('log database init fail: $e');
    }
  }

  void _initLogTable(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXIST app_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER  NOT NULL,
        level TEXT NOT NULL,
        tag TEXT,
        message TEXT NOT NULL,
        details TEXT,
        session_id TEXT,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
      );
    ''');

    db.execute(
      'CREATE INDEX IF NOT EXIST idx_logs_timestamp ON app_logs(timestamp);',
    );
    db.execute('CREATE INDEX IF NOT EXIST idx_logs_level ON app_logs(level);');
    db.execute('CREATE INDEX IF NOT EXIST idx_logs_tag ON app_logs(tag);');
    db.execute(
      'CREATE INDEX IF NOT EXIST idx_logs_session_id ON app_logs(session_id);',
    );
  }

  Future<CommonDatabase> getLogDatabase() async {
    if (_logDb == null) {
      return await initLogDatabase();
    }
    return _logDb!;
  }

  void close() {
    _db.dispose();
    if (_logDb != null) {
      _logDb!.dispose();
      LogUtils.d('log database shutdown', 'DatabaseService');
    }
    LogUtils.d('database shutdown', 'DatabaseService');
  }
}
