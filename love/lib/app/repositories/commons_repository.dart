import 'package:i_iwara/utils/logger_utils.dart';
import 'base_repository.dart';

class CommonsRepository extends BaseRepository {
  CommonsRepository._privateConstructor();
  static final CommonsRepository instance =
      CommonsRepository._privateConstructor();

  Future<String?> getData(String key) async {
    try {
      final db = databaseService.database;
      final result = db.select('SELECT data FROM commons WHERE key = ?', [key]);
      if (result.isNotEmpty) {
        return result.first['data'] as String;
      }
      return null;
    } catch (e) {
      LogUtils.e('get config data fail', error: e);
      rethrow;
    }
  }

  Future<void> setData(String key, String data) async {
    try {
      final db = databaseService.database;
      db.execute(
        '''
        INSERT INTO commons(key, data)
        VALUES(?, ?)
        ON CONFLICT(key) DO UPDATE SET
        data = excluded.data
        ''',
        [key, data],
      );
    } catch (e) {
      LogUtils.e('save config data fail', error: e);
      rethrow;
    }
  }

  Future<void> deleteData(String key) async {
    try {
      final db = databaseService.database;
      db.execute('DELETE FROM commons WHERE key = ?', [key]);
    } catch (e) {
      LogUtils.e('delete config data fail', error: e);
      rethrow;
    }
  }

  Future<Map<String, String>> getAllData() async {
    try {
      final db = databaseService.database;
      final result = db.select('SELECT key, data FROM commons');
      return Map.fromEntries(
        result.map(
          (row) => MapEntry(row['key'] as String, row['data'] as String),
        ),
      );
    } catch (e) {
      LogUtils.e('get all data fail', error: e);
      rethrow;
    }
  }
}
