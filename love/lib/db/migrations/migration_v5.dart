import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'migration.dart';

class MigrationV5PlaybackHistory extends Migration {
  @override
  int get version => 5;

  @override
  String get description => "create video_playback_history table";

  @override
  void up(CommonDatabase db) {
    db.execute('''
      CREATE TABLE IF NOT EXISTS video_playback_history(
        id INTEGER PRIMARY KEY AUTOINCREAMENT,
        video_id TEXT NOT NULL,
        total_duration INTEGER NOT NULL,
        played_duration INTEGER NOT NULL,
        created_at INTEGER NOT NULL DEFAULT(strftime('%s','now')),
        updated_at INTEGER NOT NULL DEFAULT(strftime('%s','now')),
      );
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_video_playback_history_video_id
      ON video_playback_history(video_id);
    ''');

    db.execute('''
      CREATE INDEX IF NOT EXISTS idx_video_playback_history_created_at
      ON video_playback_history(created_at);
    ''');

    db.execute('PRAGMA user_version=5;');
    LogUtils.i('migration v5: create video_playback_history');
  }

  @override
  void down(CommonDatabase db) {
    db.execute('DROP TABLE IF EXISTS video_playback_history;');
    db.execute('PRAGMA user_version = 4;');
    LogUtils.i('rollback v4: delete video_playback_history');
  }
}
