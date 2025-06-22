import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'migration.dart';

class MigrationV4Favorites extends Migration {
  @override
  int get version => 4;

  @override
  String get description => "create favorite_folders table";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXISTS favorite_folders(
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT(strftime('%s','now')),
        updated_at TEXT NOT NULL DEFAULT(strftime('%s','now')),
      );
    ''');

    db.execute('''
      CREATE TABLE IF NOT EXISTS favorite_items(
        id TEXT PRIMARY KEY,
        folder_id TEXT NOT NULL,
        item_type TEXT NOT NULL,
        item_id TEXT NOT NULL,
        title TEXT NOT NULL,
        preview_url TEXT,
        author_name TEXT,
        author_username TEXT,
        author_avatar_url TEXT,
        ext_data TEXT,
        tags TEXT,
        created_at TEXT NOT NULL DEFAULT(strftime('%s','now')),
        updated_at TEXT NOT NULL DEFAULT(strftime('%s','now')),
        FOREIGN KEY(folder_id) REFERENCES favorite_folders(id) ON DELETE CASCADE
      );
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_favorite_items_folder_time
      ON favorite_items(folder_id,created_at DESC);
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_favorite_items_type_id
      ON favorite_items(item_type,item_id);
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_favorite_items_created_ad
      ON favorite_items(created_at DESC);
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_favorite_items_tags
      ON favorite_items(tags);
    ''');

    db.execute('''
      INSERT INTO favorite_folders (id,title, description)
      VALUES('default', 'Default Favorites', 'System default favorites folder');
    ''');

    db.execute('PRAGMA user_version=4;');
    LogUtils.i('migration v3: create favorite_folders and favorite_items');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('DROP TABLE IF EXISTS favorite_items;');
    db.execute('DROP TABLE IF EXISTS favorite_folders;');
    db.execute('PRAGMA user_version = 3;');
    LogUtils.i('rollback v4: delete favorite_folders and favorite_items');
  }
}
