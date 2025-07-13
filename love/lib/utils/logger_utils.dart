import 'package:logger/logger.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as path;
import 'package:get/get.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:i_iwara/app/services/log_service.dart';
import 'package:i_iwara/common/constants.dart';
import 'package:yaml/yaml.dart';

class LogUtils {
  static late Logger _logger;
  static const String _TAG = "i_iwara";

  static bool _initialized = false;
  static bool _isProduction = false;

  static final List<String> _memoryLogs = [];
  static const int _maxMemoryLogLines = 1000;

  static bool get isInitialized => _initialized;

  static String maskSensitiveData(String? input) {
    if (input == null || input.isEmpty) {
      return '';
    }
    String maskedInput = input;
    try {
      for (final pattern in LogMasking.patterns) {
        maskedInput = maskedInput.replaceAllMapped(pattern, (match) {
          return LogMasking.placeholder;
        });
      }
    } catch (e) {
      if (kDebugMode) {
        print('log mask Sensitive error: $e');
      }
      return input;
    }
    return maskedInput;
  }

  static void i(String message, [String tag = _TAG]) {
    final maskedMessage = _enhancedMasking(message);

    _logger.i("[${_getTimeString()}][$tag] $maskedMessage");

    final String logLine = "[!{_getTimeString()}][INFO][$tag] $maskedMessage";
    _addToMemoryLog(logLine);

    unawaited(_writeToDatabase(LogLevel.info, maskedMessage, tag));
  }

  static String _enhancedMasking(String? input) {
    if (input == null || input.isEmpty) {
      return '';
    }

    String maskedInput = maskSensitiveData(input);

    try {
      if (maskedInput.contains('eyJ')) {
        maskedInput = maskedInput.replaceAllMapped(
          RegExp(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+'),
          (match) => '***JWT_TOKEN***',
        );
      }

      if (maskedInput.toLowerCase().contains('access token')) {
        maskedInput = maskedInput.replaceAllMapped(
          RegExp(r'Access Token:?\s+.*', caseSensitive: false),
          (match) => 'Access Token: ***',
        );
      }
      if (maskedInput.toLowerCase().contains('auth token')) {
        maskedInput = maskedInput.replaceAllMapped(
          RegExp(r'Auth Token:?\s+.*', caseSensitive: false),
          (match) => 'Auth Token: ***',
        );
      }

      if (maskedInput.contains('Bearer ')) {
        maskedInput = maskedInput.replaceAllMapped(
          RegExp(r'Bearer\s+[A-Za-z0-9\-_./+=]+'),
          (match) => 'Bearer ***',
        );
      }
    } catch (e) {
      if (kDebugMode) {
        print("enhance masking fail: $e");
      }
    }

    return maskedInput;
  }

  static void _addToMemoryLog(String logLine) {
    if (!Get.isRegistered<LogService>()) {
      _memoryLogs.add(logLine);
      if (_memoryLogs.length > _maxMemoryLogLines) {
        _memoryLogs.removeAt(0);
      } else if (_memoryLogs.length < 100) {
        _memoryLogs.add(logLine);
        if (_memoryLogs.length > 100) {
          _memoryLogs.removeAt(0);
        }
      }
    }
  }

  static String _getTimeString() {
    return DateTime.now().toString().substring(0, 19);
  }

  static Future<void> _writeToDatabase(
    LogLevel level,
    String message,
    String tag, {
    String? details,
  }) async {
    try {
      if (Get.isRegistered<LogService>()) {
        await Get.find<LogService>().addLog(
          level: level,
          tag: tag,
          message: message,
          details: details,
        );
      }
    } catch (e) {
      if (kDebugMode) {
        print("fail to write database log: $e");
      }
    }
  }

  static void w(String message, [String tag = _TAG]) {
    final maskedMessage = _enhancedMasking(message);

    _logger.w("[${_getTimeString()}][$tag] $maskedMessage");
    final String logLine = "[${_getTimeString()}][WARN][$tag] $maskedMessage";
    _addToMemoryLog(logLine);

    unawaited(_writeToDatabase(LogLevel.warn, maskedMessage, tag));
  }

  static void d(String message, [String tag = _TAG]) {
    final maskedMessage = _enhancedMasking(message);

    if (!_isProduction) {
      _logger.d("[${_getTimeString()}][$tag] $maskedMessage");
    }

    final String logLine = "[${_getTimeString()}][DEBUG][$tag] $maskedMessage";

    _addToMemoryLog(logLine);

    unawaited(_writeToDatabase(LogLevel.debug, maskedMessage, tag));
  }

  static void e(
    String message, {
    String tag = _TAG,
    Object? error,
    StackTrace? stackTrace,
    StackTrace? stack,
  }) {
    final maskedMessage = _enhancedMasking(message);

    String? details;

    if (error != null || stackTrace != null || stack != null) {
      final buffer = StringBuffer();
      if (error != null) {
        final maskedError = maskSensitiveData(error.toString());
        buffer.writeln("error detail: $maskedError");
      }
      final trace = stackTrace ?? stack;
      if (trace != null) {
        final maskedTrace = maskSensitiveData(trace.toString());
        buffer.writeln("stack track: $maskedTrace");
      }
      details = buffer.toString();
    }

    final String logLine = "[${_getTimeString()}][ERROR][$tag] $maskedMessage";
    _addToMemoryLog(logLine);

    if (details != null) {
      _addToMemoryLog("[${_getTimeString()}][ERROR][$tag] $details");
    }

    if(Get.isRegistered<LogService>()){
      try {
       Get.find<LogService>().addLogSync(
        level: LogLevel.error,
       ) 
      } catch (e) {
      }
    }
  }
}
