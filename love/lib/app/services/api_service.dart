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

  Future<T> add<T>(Future<T> Function() task) async {
    LogUtils.d(
      'TokenQueue: add task to queue, current queue length: ${_queue.length}',
    );

    if (_queue.length >= maxQueueSize) {
      throw Exception('Token refresh queue is full');
    }

    final completer = Completer<T>();

    Future<void> executeTask() async {
      try {
        LogUtils.d('TokenQueue: start execute task');
        if (_queue.length >= maxQueueSize) {
          throw Exception('Token refresh queue is full');
        }
      } catch (e) {
        LogUtils.e('TokenQueue: task execute failure');
      }
    }

    _queue.add(executeTask);

    if (!_processing) {
      _processing = true;
      LogUtils.d('TokenQueue: start process, queue length: ${_queue.length}');
      while (_queue.isNotEmpty) {
        final nextTask = _queue.removeFirst();
        await nextTask();
      }

      _processing = false;
      LogUtils.d('TokenQueue: process finished');
    } else {
      LogUtils.d('TokenQueue processing new task add to queue');
    }

    return completer.future;
  }
}

class ApiService extends GetxService {
  static ApiService? _instance;
  late d_dio.Dio _dio;
  final AuthService _authService = Get.find<AuthService>();
  final String _tag = 'ApiService';

  static const int maxRetries = 3;
  static const Duration baseRetryDelay = Duration(seconds: 1);
  static const Duration requestTimeout = Duration(seconds: 45);

  final _TokenQueue _refreshQueue = _TokenQueue();

  bool _interceptorAdded = false;

  ApiService._();

  d_dio.Dio get dio => _dio;

  static Future<ApiService> getInstance() async {
    _instance ??= await ApiService._().init();
    return _instance!;
  }

  Future<ApiService> init() async {
    _dio = d_dio.Dio(
      d_dio.BaseOptions(
        baseUrl: CommonConstants.iwaraApiBaseUrl,
        connectTimeout: requestTimeout,
        receiveTimeout: requestTimeout,
        sendTimeout: requestTimeout,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
          'Accept': 'application/json, text/plain, */*',
          'Connection': 'keep-alive',
          'Referer': CommonConstants.iwaraApiBaseUrl,
        },
      ),
    );

    if (_interceptorAdded) {
      return this;
    }

    _dio.interceptors.add(
      d_dio.InterceptorsWrapper(
        onRequest: (options, handler) async {
          final accessToken = _authService.accessToken;
          LogUtils.d(
            'ApiService: interceptor handler request: ${options.path}, params" ${options.queryParameters}',
          );

          if (accessToken != null) {
            options.headers['Authorization'] = 'Bearer $accessToken';
          }

          return handler.next(options);
        },

        onError: (error, handler) async {
          if (error.response?.statusCode == 401 ||
              error.response?.statusCode == 403) {
            LogUtils.e('ApiService: auth error ${error.response?.statusCode}');

            if (error.requestOptions.path == '/user/token') {
              await handlerAuthError();
              return handler.next(error);
            }

            final result = await _refreshQueue.add(() async {
              return await _authService.refreshAccessToken();
            });

            if (result) {
              try {
                final response = await _retryRequest(error.requestOptions);
                return handler.resolve(response);
              } catch (e) {
                LogUtils.e('retry fail', error: e);
                await handlerAuthError();
              }
            } else {
              await handlerAuthError();
            }
          }
          return handler.next(error);
        },
      ),
    );

    _interceptorAdded = true;
    return this;
  }

  Future<d_dio.Response<T>> _retryRequest<T>(
    d_dio.RequestOptions options,
  ) async {
    LogUtils.d('ApiService: start retry: ${options.path}');

    final accessToken = _authService.accessToken;
    if (accessToken != null) {
      options.headers['Authorization'] = 'Bearer $accessToken';
    }

    LogUtils.d('ApiService: retry Headers: ${options.headers}');

    return _dio.fetch(
      options..copyWith(
        baseUrl: options.baseUrl,
        queryParameters: options.queryParameters,
        data: options.data,
      ),
    );
  }

  Future<void> handlerAuthError() async {
    await _authService.handleTokenExpired();
  }

  Future<d_dio.Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? headers,
    d_dio.CancelToken? cancelToken,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: d_dio.Options(headers: headers),
        cancelToken: cancelToken,
      );
    } on d_dio.DioException catch (e) {
      LogUtils.e(
        'Get request fail: ${e.message}, path: $path',
        tag: _tag,
        error: e,
      );
      rethrow;
    }
  }

  Future<d_dio.Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
      );
    } on d_dio.DioException catch (e) {
      LogUtils.e('POST request fail: ${e.message}', tag: _tag, error: e);
      rethrow;
    }
  }

  Future<d_dio.Response<T>> delete<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      return await _dio.delete<T>(path, queryParameters: queryParameters);
    } on d_dio.DioException catch (e) {
      LogUtils.e('DELETE request fail: ${e.message}', tag: _tag, error: e);
      rethrow;
    }
  }

  Future<d_dio.Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
      );
    } on d_dio.DioException catch (e) {
      LogUtils.e('PUT request fail: ${e.message}', tag: _tag, error: e);
      rethrow;
    }
  }

  void resetProxy() {
    _dio.httpClientAdapter = IOHttpClientAdapter();
  }

  bool _isSameToken(String? token1, String? token2) {
    if (token1 == null || token2 == null) return false;

    final t1 = token1.replaceFirst('Bearer ', '').trim();
    final t2 = token2.replaceFirst('Bearer ', '').trim();

    return t1 == t2;
  }
}
