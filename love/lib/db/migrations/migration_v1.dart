import 'package:i_iwara/utils/logger_utils.dart';
import 'package:sqlite3/common.dart';
import 'migration.dart';

class MigrationV1Initial extends Migration {
  @override
  int get version => 1;

  @override
  String get description =>
      "init migration : create sign_in_records and commons";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXISTS sign_in_records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        data TEXT NOT NULL,
        status INTEGER NOT NULL,
        reason TEXT,
        created_at TEXT NOT NULL DEFAULT(datetime('now')),
        updated_at TEXT NOT NULL DEFAULT(datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(id),
        UNIQUE(user_id, date)
      );
    ''');

    db.execute('''
      CREATE INDEX idx_sign_in_records_user_date
      ON sign_in_records(user_id,date);
    ''');

    db.execute('''
      CREATE  TRIGGER trigger_sign_in_records_updated_at
      AFTER UPDATE ON sign_in_records
      BEGIN
        UPDATE sign_in_records
        SET updated_at = datetime('now')
        WHERE id = NEW.id;
      END;
    ''');

    db.execute('''
      CREATE TABLE IF NOT EXISTS commons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        data TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT(datetime('now')),
        updated_at TEXT NOT NULL DEFAULT(datetime('now'))
      );
    ''');

    db.execute('''
      CREATE TRIGGER trigger_commons_updated_at
      AFTER UPDATE ON commons
      BEGIN
        UPDATE commons
        SET updated_at = datetime('now')
        WHERE id = NEW.id;
      END;
    ''');

    db.execute('PRAGMA user_version = 1 ;');
    LogUtils.i('apply migration_v1: create sign_in_records and commons');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('DROP TRIGGER IF EXISTS trigger_sign_in_records_updated_at;');
    db.execute('DROP INDEX IF EXISTS idx_sign_in_records_user_date;');
    db.execute('DROP TABLE IF EXISTS sign_in_records;');
    db.execute('DROP TRIGGER IF EXISTS trigger_commons_updated_at;');
    db.execute('DROP TABLE IF EXISTS commons');
    db.execute('PRAGMA user_version=0;');
    LogUtils.i('rollback migration_v1: delete sign_in_records and commons');
  }
}
