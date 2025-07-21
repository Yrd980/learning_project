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
  ];

  int getCurrentVersion(CommonDatabase db) {
    final stmt = db.prepare('PRAGMA user_version;');
    final ResultSet result = stmt.select([]);
    stmt.dispose();
    return result.first['user_version'] as int;
  }

  void runMigrations(CommonDatabase db) {
    final currentVersion = getCurrentVersion(db);
    final pendingMigrations =
        migrations.where((m) => m.version > currentVersion).toList()
          ..sort((a, b) => a.version.compareTo(b.version));

    if (pendingMigrations.isEmpty) {
      LogUtils.i(
        'current database version is v$currentVersion, dont need migration',
      );
      return;
    }

    db.execute('BEGIN TRANSACTION;');
    try {
      for (var migration in pendingMigrations) {
        LogUtils.i(
          'application migrating v${migration.version} : ${migration.description}',
        );
        migration.up(db);
      }
      db.execute('COMMIT;');
      LogUtils.i('all migrations success');
    } catch (e) {
      db.execute('ROLLBACK;');
      throw DatabaseException("migration fail: $e");
    }
  }
}
