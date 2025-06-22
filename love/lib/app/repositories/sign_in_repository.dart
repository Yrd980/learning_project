import 'dart:async';

import 'package:i_iwara/utils/logger_utils.dart';
import 'base_repository.dart';

class SignInRepository extends BaseRepository {
  SignInRepository.privateConstructor();
  static final SignInRepository instance =
      SignInRepository.privateConstructor();

  Future<Map<String, dynamic>?> checkIfSignedInToday(String userId) async {
    try {
      final now = DateTime.now();
      final dateStr = now.toIso8601String().split('T').first;
      final db = databaseService.database;
      final result = db.select(
        'SELECT status, reason FROM sign_in_records WHERE user_id = ? AND date = ?',
        [userId, dateStr],
      );
      if (result.isNotEmpty) {
        return {
          'status': result.first['status'] as int,
          'reason': result.first['reason'] as String?,
        };
      }
      return null;
    } catch (e) {
      LogUtils.e('check sign status error', error: e);
      rethrow;
    }
  }

  Future<void> signIn(
    String userId, {
    required bool isSuccess,
    String? reason,
  }) async {
    try {
      final now = DateTime.now();
      final dateStr = now.toIso8601String().split('T').first;
      final db = databaseService.database;

      final existing = db.select(
        'SELECT * FROM sign_in_records WHERE user_id = ? AND date = ?',
        [userId, dateStr],
      );
      if (existing.isEmpty) {
        db.execute(
          'INSERT INTO sign_in_records (user_id,date,status,reason) VALUES(?,?,?,?)',
          [userId, dateStr, isSuccess ? 1 : 0, reason],
        );
      } else {
        db.execute(
          'UPDATE sign_in_records SET status = ? , reason = ? WHERE user_id is ? and date = ?',
          [isSuccess ? 1 : 0, reason, userId, dateStr],
        );
      }
    } catch (e) {
      LogUtils.e('sign fail', error: e);
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> getSignInRecords(String userId) async {
    try {
      final db = databaseService.database;
      final result = db.select(
        'SELECT date, status , reason FROM sign_in_records WHERE user_id = ? ORDER  BY date DESC',
        [userId],
      );
      return result
          .map(
            (row) => {
              'date': DateTime.parse(row['date'] as String),
              'status': row['status'] as int,
              'reason': row['reason'] as String?,
            },
          )
          .toList();
    } catch (e) {
      LogUtils.e('fail to get user records', error: e);
      rethrow;
    }
  }

  Future<int> getTotalSignIns(String userId) async {
    try {
      final db = databaseService.database;
      final result = db.select(
        'SELECT COUNT(*) as total FROM sign_in_records WHERE user_id = ? and status = 1',
        [userId],
      );
      LogUtils.d('get user total sign count：$result', 'SignInRepository');
      if (result.isNotEmpty) {
        return result.first['total'] as int;
      }
      return 0;
    } catch (e) {
      LogUtils.e('fail to get user total sign count', error: e);
      rethrow;
    }
  }

  Future<int> getConsecutiveSignIns(String userId) async {
    try {
      final db = databaseService.database;
      final result = db.select(
        'SELECT date,status FROM sign_in_records WHERE user_id = ? ORDER BY date DESC',
        [userId],
      );

      int streak = 0;
      DateTime currentDay = DateTime.now();
      currentDay = DateTime(currentDay.year, currentDay.month, currentDay.day);

      for (var row in result) {
        final date = DateTime.parse(row['date'] as String);
        final flooredDate = DateTime(date.year, date.month, date.day);
        final status = row['status'] as int;

        if (status != 1) {
          break;
        }

        final difference = currentDay.difference(flooredDate).inDays;

        if (difference == 0) {
          streak += 1;
          currentDay = currentDay.subtract(const Duration(days: 1));
        } else {
          break;
        }
      }
      return streak;
    } catch (e) {
      LogUtils.e('get consecutive sign day error', error: e);
      rethrow;
    }
  }
}
