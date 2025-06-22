import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'migration.dart';

class MigrationV2History extends Migration {
  @override
  int get version => 2;

  @override
  String get description => "create history_records table";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXISTS history_records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id TEXT NOT NULL,
        item_type TEXT NOT NULL,
        title TEXT NOT NULL,
        thumbnail_url TEXT,
        author TEXT,
        author_id TEXT,
        data TEXT NOT NULL,
        item_id TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT(datetime('now')),
        updated_at TEXT NOT NULL DEFAULT(datetime('now')),
        UNIQUE(item_id, item_type)
      );
    ''');

    db.execute('''
      CREATE INDEX idx_history_recodes_type_date
      ON history_records(item_type, created_at);
    ''');

    db.execute('''
      CREATE INDEX idx_history_recodes_title
      ON history_records(title);
    ''');

    db.execute('''
      CREATE TRIGGER trigger_history_records_updated_at
      AFTER UPDATE ON history_records
      BEGIN
        UPDATE history_records
        SET updated_at = datetime('now')
        WHERE id=NEW.id;
    ''');

    db.execute('PRAGMA user_version=2;');
    LogUtils.i('migration v2: create history_records');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('DEOP TRIGGER IF EXISTS trigger_history_records_updated_at;');
    db.execute('DEOP INDEX IF EXISTS idx_history_recodes_type_date;');
    db.execute('DEOP INDEX IF EXISTS idx_history_recodes_title;');
    db.execute('DEOP TABLE IF EXISTS history_records;');
    LogUtils.i('rollback v2: delete history_records');
  }
}
