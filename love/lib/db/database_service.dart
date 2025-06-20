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
  static final DatabaseService _instance = DatabaseService()._internal();

  factory DatabaseService() => _instance;

  DatabaseService._internal();
  late CommonDatabase _db;
  CommonDatabase? _logDb;
  final MigrationManager _migrationManager = MigrationManager();
}
