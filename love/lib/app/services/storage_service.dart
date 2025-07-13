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
        } catch (e) {
          _useSecureStorage = false;
          LogUtils.w(
            'secure storage can not use , use normal storage as roll ',
            _tag,
          );
        }
      }

      initialized = true;
    } catch (e) {
      LogUtils.e('storage services init fail', tag: _tag, error: e);
      rethrow;
    }
  }

  GetStorage get box {
    if (_box == null) {
      throw StateError('storage services not init');
    }
    return _box!;
  }

  @Deprecated('Use [CommonDatabase] instead')
  Future<void> writeData(String key, dynamic value) async {
    await box.write(key, value);
  }

  @Deprecated('Use [CommonDatabase] instead')
  T? readData<T>(String key) {
    return box.read<T>(key);
  }

  @Deprecated('Use [CommonDatabase] instead')
  Future<void> deleteData(String key) async {
    await box.remove(key);
  }

  @Deprecated('Use [CommonDatabase] instead')
  Future<void> clearAll() async {
    await box.erase();
    if (_useSecureStorage) {
      try {
        await _secureStorage.deleteAll();
      } catch (e) {
        LogUtils.e('clear secure storage fail', tag: _tag, error: e);
      }
    }
  }

  Future<void> writeSecureData(String key, String value) async {
    if (_useSecureStorage) {
      try {
        await _secureStorage.write(key: key, value: value);
        return;
      } catch (e) {
        LogUtils.w('write secure storage fail roll to normal storage', _tag);
        _useSecureStorage = false;
      }
    }
    await box.write(_securePrefix + key, value);
  }

  Future<String?> readSecureData(String key) async {
    if (_useSecureStorage) {
      try {
        return await _secureStorage.read(key: key);
      } on PlatformException catch (e) {
        if (e.message?.contains('BAD_DECRYPT') ?? false) {
          LogUtils.w('secure storage decode fail clear all data', _tag);
          await _secureStorage.deleteAll();
        }
        LogUtils.w('read fail，roll to normal', _tag);
        _useSecureStorage = false;
      } catch (e) {
        LogUtils.w('read fail，roll to normal', _tag);
        _useSecureStorage = false;
      }
    }
    return box.read<String>(_securePrefix + key);
  }

  Future<void> deleteSecureData(String key) async {
    if (_useSecureStorage) {
      try {
        await _secureStorage.delete(key: key);
        return;
      } catch (e) {
        LogUtils.w('delete fail, roll to normal', _tag);
        _useSecureStorage = false;
      }
    }
    await box.remove(_securePrefix + key);
  }

  Future<void> writeSecureObject(String key, Map<String, dynamic> value) async {
    final string = json.encode(value);
    await writeSecureData(key, string);
  }

  Future<Map<String, dynamic>?> readSecureObject(String key) async {
    try {
      final string = await readSecureData(key);
      if (string == null) return null;
      return json.decode(string) as Map<String, dynamic>;
    } catch (e) {
      LogUtils.e('read fail', tag: _tag, error: e);
      return null;
    }
  }

  Future<void> writeCredentials(String username, String password) async {
    await writeSecureData('username', username);
    await writeSecureData('password', password);
  }

  Future<Map<String, String>?> readCredentials() async {
    final username = await readSecureData('username');
    final password = await readSecureData('password');
    if (username != null && password != null) {
      return {'username': username, 'password': password};
    }
    return null;
  }

  Future<void> clearCredentials() async {
    await deleteSecureData('username');
    await deleteSecureData('password');
  }
}
