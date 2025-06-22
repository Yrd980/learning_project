import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'migration.dart';

class MigrationV6Config extends Migration {
  @override
  int get version => 6;

  @override
  String get description => "create/update app_config table";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXISTS app_config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      );
    ''');
    db.execute('PRAGMA user_version = 6;');
    LogUtils.i('migration v6：create/update app_config');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('DROP TABLE IF EXISTS app_config;');
    db.execute('PRAGMA user_version = 5;');
    LogUtils.i('rollback v5：delete app_config');
  }
}
