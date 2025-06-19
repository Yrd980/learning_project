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

  static String maskSensitiveData(String? input){
    if (input == null || input.isEmpty) {
      return '';
    }
    String maskedInput = input;
    try {
      for(final pattern in LogMasking.patterns) {

      }
    }
  }
}
