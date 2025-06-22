import 'package:flutter/material.dart';
import 'package:i_iwara/common/constants.dart';
import 'package:i_iwara/db/database_service.dart';
import 'package:sqlite3/common.dart';
import 'package:i_iwara/app/models/history_record.dart';

class HistoryRepository {
  late final CommonDatabase _db;

  HistoryRepository() {
    _db = DatabaseService().database;
  }

  Future<void> addRecord(HistoryRecord record) async {
    if (!CommonConstants.enableHistory) {
      return;
    }

    _db
        .prepare('''
      INSERT OR REPLACE INTO history_records
      (item_id,item_type,title,thumbnail_url,author,author_id,data)
      VALUES(?,?,?,?,?,?,?);
    ''')
        .execute([
          record.itemId,
          record.itemType,
          record.title,
          record.thumbnailUrl,
          record.author,
          record.authorId,
          record.data,
        ]);
  }

  Future<void> addRecords(List<HistoryRecord> records) async {
    _db.execute('BEGIN TRANSACTION;');
    try {
      for (var record in records) {
        await addRecord(record);
      }
      _db.execute('COMMIT;');
    } catch (e) {
      _db.execute('ROLLBACK;');
      rethrow;
    }
  }

  Future<List<HistoryRecord>> searchByTitle(String keyword) async {
    final stmt = _db.prepare('''
      SELECT * FROM history_records
      WHERE title like ?
      ORDER BY created_at DESC;
    ''');

    final results = stmt.select(['%%keyword%']);
    return results.map((row) => HistoryRecord.fromJson(row)).toList();
  }

  Future<void> deleteRecord(int id) async {
    _db.prepare('DELETE FROM history_records WHERE id = ?').execute([id]);
  }

  Future<void> deleteRecords(List<int> ids) async {
    final placeholders = List.filled(ids.length, '? ').join(',');
    _db
        .prepare('DELETE FROM history_records WHERE id in ($placeholders)')
        .execute(ids);
  }

  Future<void> clearHistoryByType(String itemType) async {
    _db.prepare('DELETE FROM history_records WHERE item_type = ?').execute([
      itemType,
    ]);
  }

  Future<List<HistoryRecord>> getRecordsByType(
    String itemType, {
    int limit = 20,
    int offset = 0,
  }) async {
    String sql;
    List<Object?> params;

    if (itemType == 'all') {
      sql = '''
        SELECT * FROM history_records
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
      ''';
      params = [limit, offset];
    } else {
      sql = '''
        SELECT * FROM history_records
        WHERE item_type = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
      ''';
      params = [itemType, limit, offset];
    }

    final stmt = _db.prepare(sql);
    final results = stmt.select(params);
    return results.map((row) => HistoryRecord.fromJson(row)).toList();
  }

  Future<List<HistoryRecord>> searchByTitlePaged(
    String keyword, {
    String? itemType,
    int limit = 20,
    int offset = 0,
  }) async {
    final List<Object?> params = ['%keyword%'];
    String sql = '''
      SELECT * FROM history_records
      WHERE keyword like ?
    ''';

    if (itemType != null) {
      sql += ' AND item_type = ?';
      params.add(itemType);
    }

    sql += '''
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    ''';
    params.addAll([limit, offset]);
    final stmt = _db.prepare(sql);
    final results = stmt.select(params);
    return results.map((row) => HistoryRecord.fromJson(row)).toList();
  }

  Future<void> addRecordWithCheck(HistoryRecord record) async {
    if (!CommonConstants.enableHistory) {
      return;
    }

    try {
      final existing = _db
          .prepare(
            'SELECT updated_at FROM history_records WHERE item_id = ? AND item_type = ?',
          )
          .select([record.itemId, record.itemType]);

      if (existing.isEmpty) {
        await addRecord(record);
      } else {
        _db
            .prepare(
              'UPDATE history_records SET updated_at = ? WHERE item_id = ? AND item_type = ?',
            )
            .select([
              DateTime.now().toIso8601String(),
              record.itemId,
              record.itemType,
            ]);
      }
    } catch (e) {
      await addRecord(record);
    }
  }

  Future<List<HistoryRecord>> getRecordsByTypeAndTimeRange(
    String itemType, {
    DateTime? startDate,
    DateTime? endDate,
    int limit = 20,
    int offset = 0,
  }) async {
    final List<Object?> params = [];
    final List<String> conditions = [];

    if (itemType != 'all') {
      conditions.add('item_type = ?');
      params.add(itemType);
    }

    if (startDate != null) {
      conditions.add('created_at >= ?');
      params.add(startDate.toIso8601String());
    }

    if (endDate != null) {
      conditions.add('created_at <= ?');
      params.add(endDate.toIso8601String());
    }

    final String sql =
        '''
      SELECT * FROM history_records 
      ${conditions.isNotEmpty ? 'WHERE ${conditions.join(' AND ')}' : ''}
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    ''';

    params.addAll([limit, offset]);

    final stmt = _db.prepare(sql);
    final results = stmt.select(params);
    return results.map((row) => HistoryRecord.fromJson(row)).toList();
  }

  Future<List<HistoryRecord>> searchByTitleAndTimeRange(
    String keyword, {
    String? itemType,
    DateTime? startDate,
    DateTime? endDate,
    int limit = 20,
    int offset = 0,
  }) async {
    final List<Object?> params = ['%$keyword%'];
    String sql = '''
      SELECT * FROM history_records 
      WHERE title LIKE ? 
    ''';

    if (itemType != null) {
      sql += ' AND item_type = ?';
      params.add(itemType);
    }

    if (startDate != null) {
      sql += ' AND created_at >= ?';
      params.add(startDate.toIso8601String());
    }

    if (endDate != null) {
      sql += ' AND created_at <= ?';
      params.add(endDate.toIso8601String());
    }

    sql += '''
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    ''';
    params.addAll([limit, offset]);

    final stmt = _db.prepare(sql);
    final results = stmt.select(params);
    return results.map((row) => HistoryRecord.fromJson(row)).toList();
  }
}
