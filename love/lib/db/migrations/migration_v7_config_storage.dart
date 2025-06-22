import 'package:i_iwara/app/services/config_service.dart';
import 'package:sqlite3/common.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:i_iwara/app/services/storage_service.dart';
import 'dart:convert';
import 'migration.dart';

class MigrationV7ConfigStorage extends Migration {
  @override
  int get version => 7;

  @override
  String get description =>
      "migration config_service from StorageService to database";

  @override
  Future<void> up(CommonDatabase db) async {
    try {
      final storage = StorageService();
    } catch () {
    }
  }

  @override
  void down(CommonDatabase db) {
    LogUtils.i('v7 can not rollback');
  }
}
