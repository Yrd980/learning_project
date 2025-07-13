import 'dart:async';
import 'dart:collection';

import 'package:dio/dio.dart' as d_dio;
import 'package:dio/io.dart';
import 'package:get/get.dart';

import '../../common/constants.dart';
import '../../utils/logger_utils.dart';
import 'auth_service.dart';
import 'message_service.dart';

class _TokenQueue {
  final Queue<Future Function()> _queue = Queue();
  bool _processing = false;
  static const int maxQueueSize = 100;

  Future<T> add<T>(Future<T> Function()task) async {
    LogUtils.d('TokenQueue: add task to queue, current queue length: ${_queue.length}');
    if(_queue.length >= maxQueueSize) {
      throw Exception('Token refresh queue is full');
    }

    final completer = Completer<T>();

    Future<void> executeTask() async {
      try {
        LogUtils.d('TokenQueue: start execute task');
        if (_queue.length >= maxQueueSize) {

      throw Exception('Token refresh queue is full');
        }
      }
      catch(e) {
        LogUtils.e('TokenQueue: task execute failure');
      }
    }
  }
}
