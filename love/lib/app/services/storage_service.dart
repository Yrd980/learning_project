import 'package:flutter/services.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';
import 'package:flutter/foundation.dart';

import 'package:i_iwara/utils/logger_utils.dart';

class StorageService {
  static final StorageService _instance = StorageService._internal();
  static const String _tag = 'StorageService';

  factory StorageService() => _instance;
  StorageService._internal();

  GetStorage? _box;
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  bool _useSecureStorage = true;
  static const String _securePrefix = 'secure_';

  bool initialized = false;

  Future<void> init() async {
    if (initialized) {
      return;
    }

    try {
      await GetStorage.init();
      _box = GetStorage();

      if (kIsWeb) {
        _useSecureStorage = false;
        LogUtils.w(
          'running on web, unsupport secure storage, use plain storage as rollback plan',
          _tag,
        );
      } else {
        try {
          await _secureStorage.write(key: 'test_key', value: 'test_vale');
          await _secureStorage.read(key: 'test_key');
          await _secureStorage.delete(key: 'test_key');
          _useSecureStorage = true;
          LogUtils.d('secure storage available', _tag);
        } catch (e) {}
      }
    } catch (e) {}
  }
}
