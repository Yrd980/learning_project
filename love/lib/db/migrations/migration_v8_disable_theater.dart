import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'migration.dart';

class MigrationV8DisableTheater extends Migration {
  @override
  int get version => 8;

  @override
  String get description => "close theater_mode";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      UPDATE app_config
      SET value = 'false'
      WHERE key = 'theater_mode';
    ''');
    db.execute('PRAGMA user_version = 8');
    LogUtils.i('migration v8: force close theater_mode');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('''
      UPDATE app_config
      SET value = 'true'
      WHERE key = 'theater_mode';
    ''');
    db.execute('PRAGMA user_version = 7');
    LogUtils.i('rollback v7: recover theater_mode');
  }
}
