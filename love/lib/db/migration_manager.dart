// lib/migrations/migration_manager.dart

import 'package:i_iwara/db/migrations/migration_v3.dart';
import 'package:i_iwara/db/migrations/migration_v4.dart';
import 'package:i_iwara/db/migrations/migration_v5.dart';
import 'package:i_iwara/db/migrations/migration_v8_disable_theater.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:sqlite3/common.dart';

import 'database_service.dart';
import 'migrations/migration.dart';
import 'migrations/migration_v1.dart';
import 'migrations/migration_v2.dart';
import 'migrations/migration_v6_config.dart';
import 'migrations/migration_v7_config_storage.dart';

class MigrationManager {
  final List<Migration> migrations = [
    MigrationV1Initial(),
    MigrationV2History(),
    MigrationV3DownloadTask(),
    MigrationV4Favorites(),
    MigrationV5PlaybackHistory(),
    MigrationV6Config(),
    MigrationV7ConfigStorage(),
    MigrationV8DisableTheater(),
  ]
}
