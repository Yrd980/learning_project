import 'dart:async';
import 'dart:convert';
import 'dart:nativewrappers/_internal/vm/lib/math_patch.dart';

import 'package:dio/dio.dart' as dio;
import 'package:dio/io.dart';
import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:i_iwara/app/services/user_service.dart';
import 'package:i_iwara/app/ui/widgets/MDToastWidget.dart';
import 'package:i_iwara/i18n/strings.g.dart';
import 'package:win32/win32.dart';

import '../../common/constants.dart';
import '../../utils/logger_utils.dart';
import '../models/api_result.model.dart';
import '../models/captcha.model.dart';
import 'storage_service.dart';
import 'message_service.dart';

enum TokenValidationResult { valid, expired, invalid, wrongType, malformed }

class AuthService extends GetxService {
  final StorageService _storage = StorageService();
  final MessageService _messageService = Get.find<MessageService>();
  final dio.Dio _dio = dio.Dio(
    dio.BaseOptions(
      baseUrl: CommonConstants.iwaraApiBaseUrl,
      headers: {'Content-Type': 'application/json'},
    ),
  );

  static const String _tag = 'auth_service';

  String? _authToken;
  String? get authToken => _authToken;
  String? _accessToken;
  String? get accessToken => _accessToken;

  bool get hasToken => _authToken != null && _accessToken != null;

  Completer<void>? _refreshTokenCompleter;

  Timer? _tokenRefreshTimer;
  DateTime? _tokenExpireTime;

  bool get isTokenExpired {
    if (_tokenExpireTime == null) return true;
    return DateTime.now().isAfter(_tokenExpireTime!);
  }

  int? _getTokenExpiration(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return null;

      final payload = jsonDecode(
        utf8.decode(base64Url.decode(base64Url.normalize(parts[1]))),
      );
      return payload['exp'] as int?;
    } catch (e) {
      LogUtils.e('Token parse failure', tag: _tag, error: e);
      return null;
    }
  }

  String? _getTokenType(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return null;

      final payload = jsonDecode(
        utf8.decode(base64Url.decode(base64Url.normalize(parts[1]))),
      );
      return payload['type'] as String?;
    } catch (e) {
      LogUtils.e('Token parse failure', tag: _tag, error: e);
      return null;
    }
  }

  DateTime? _authTokenExpireTime;
  DateTime? _accessTokenExpireTime;

  static const int _refreshThreshold = 5 * 60;

  bool get isAuthTokenExpired {
    if (_authToken == null || _authTokenExpireTime == null) return true;
    return DateTime.now().isAfter(_authTokenExpireTime!);
  }

  bool get isAccessTokenExpired {
    if (_accessToken == null || _accessTokenExpireTime == null) return true;
    return DateTime.now()
        .add(const Duration(seconds: _refreshThreshold))
        .isAfter(_accessTokenExpireTime!);
  }

  void _updateTokenExpireTime(String token, bool isAuthToken) {
    try {
      final type = _getTokenType(token);

      if (type == null) {
        LogUtils.e('Token type parse error', tag: _tag);
        return;
      }

      if (isAuthToken && type != 'refresh_token') {
        LogUtils.e('Auth token type error: $type', tag: _tag);
        return;
      }
      if (!isAuthToken && type != 'access_token') {
        LogUtils.e('Access token type error: $type', tag: _tag);
        return;
      }

      final expiration = _getTokenExpiration(token);

      if (expiration != null) {
        if (isAuthToken) {
          _authTokenExpireTime = DateTime.fromMillisecondsSinceEpoch(
            expiration * 1000,
          );
          LogUtils.d('$_tag Auth token expiration time: $_authTokenExpireTime');
        } else {
          _accessTokenExpireTime = DateTime.fromMillisecondsSinceEpoch(
            expiration * 1000,
          );
          LogUtils.d(
            '$_tag Access token expiration time: $_accessTokenExpireTime',
          );
        }
      }
    } catch (e) {
      LogUtils.e('Token expiration time parse error', tag: _tag, error: e);
    }
  }

  final RxBool _isAuthenticated = false.obs;
  bool get isAuthenticated => hasToken && isTokenValid;

  bool get isTokenValid {
    final valid = !isAuthTokenExpired && !isAccessTokenExpired;
    assert(() {
      // LogUtils.d('$_tag Token valid check: authToken=${!isAuthTokenExpired}, accessToken=${!isAccessTokenExpired}');
      return true;
    }());
    return valid;
  }

  TokenValidationResult validateToken(String token, bool isAuthToken) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return TokenValidationResult.malformed;

      final payload = jsonDecode(
        utf8.decode(base64Url.decode(base64Url.normalize(parts[1]))),
      );

      final type = payload['type'] as String?;
      if (type == null) return TokenValidationResult.invalid;

      if (isAuthToken && type != 'refresh_token')
        return TokenValidationResult.wrongType;
      if (!isAuthToken && type != 'access_token')
        return TokenValidationResult.wrongType;

      final exp = payload['exp'] as int?;
      if (exp == null) return TokenValidationResult.invalid;

      final expireTime = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
      if (DateTime.now().isAfter(expireTime))
        return TokenValidationResult.expired;

      return TokenValidationResult.valid;
    } catch (e) {
      LogUtils.e('Token valid error', tag: _tag, error: e);
      return TokenValidationResult.malformed;
    }
  }

  Future<AuthService> init() async {
    try {
      _authToken = await _storage.readSecureData(KeyConstants.autoToken);
      _accessToken = await _storage.readSecureData(KeyConstants.accessToken);

      if (_authToken != null && _accessToken != null) {
        final authTokenResult = validateToken(_authToken!, true);
        final accessTokenResult = validateToken(_accessToken!, false);

        LogUtils.d(
          '$_tag Token valid result:\n'
          'Auth token: $authTokenResult\n'
          'Access token: $accessTokenResult',
        );

        if (authTokenResult == TokenValidationResult.malformed ||
            authTokenResult == TokenValidationResult.invalid ||
            authTokenResult == TokenValidationResult.wrongType ||
            authTokenResult == TokenValidationResult.expired) {
          LogUtils.i('Auth token uneffect state: $authTokenResult', _tag);
          await _handleTokenExpiredSilently();
          return this;
        }

        if (accessTokenResult == TokenValidationResult.malformed ||
            accessTokenResult == TokenValidationResult.invalid ||
            accessTokenResult == TokenValidationResult.wrongType ||
            accessTokenResult == TokenValidationResult.expired) {
          if (authTokenResult == TokenValidationResult.valid) {
            LogUtils.i('Access token uneffect try to refresh', _tag);
            _updateTokenExpireTime(_authToken!, true);

            _refreshTokenInBackground();
            _isAuthenticated.value = true;
          } else {
            await _handleTokenExpiredSilently();
          }
          return this;
        }

        _updateTokenExpireTime(_authToken!, true);
        _updateTokenExpireTime(_accessToken!, false);

        if (isAccessTokenExpired && !isAuthTokenExpired) {
          LogUtils.i('Access token expiration try to refresh', _tag);

          _refreshTokenInBackground();
          _isAuthenticated.value = true;
        } else if (!isAccessTokenExpired) {
          _startTokenRefreshTimer();
          _isAuthenticated.value = true;
        }
      }
    } catch (e) {
      LogUtils.e("AuthService init fail", tag: _tag, error: e);
      await _handleTokenExpiredSilently();
    }
    return this;
  }

  void _refreshTokenInBackground() {
    Future.microtask(() async {
      if (hasToken) {
        try {
          final success = await refreshAccessToken();
          if (success) {
            _startTokenRefreshTimer();
          } else {
            LogUtils.w("background refresh token fail", _tag);
            await _handleTokenExpiredSilently();
          }
        } catch (e) {
          LogUtils.e("background refresh token error", tag: _tag, error: e);
          await _handleTokenExpiredSilently();
        }
      }
    });
  }

  static const int maxRefreshRetries = 3;
  static const Duration refreshRetryDelay = Duration(seconds: 1);

  Future<bool> refreshAccessToken() async {
    LogUtils.d('AuthService: start refresh Access Token');
    final oldAccessToken = accessToken;

    try {
      final response = await _dio.post(
        '/user/token',
        options: dio.Options(
          headers: {'Authorization': 'Bearer $_authToken'},
          sendTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 10),
        ),
      );

      if (response.statusCode == 200 && response.data['accessToken'] != null) {
        final newAccessToken = response.data['accessToken'];
        final tokenResult = validateToken(newAccessToken, false);

        if (tokenResult == TokenValidationResult.valid) {
          _accessToken = newAccessToken;
          _updateTokenExpireTime(newAccessToken, false);
          await _storage.writeSecureData(
            KeyConstants.accessToken,
            newAccessToken,
          );

          LogUtils.i('AuthService: Access Token refresh success');
          LogUtils.d('AuthService: Access Token update');
          return true;
        }
      }
    } catch (e) {
      LogUtils.e('refresh token fail', error: e);
      return false;
    }
  }

  void _startTokenRefreshTimer() {}

  Future<void> handleTokenExpired() async {
    if (!_isAuthenticated.value) {
      return;
    }

    _isAuthenticated.value = false;
    _accessToken = null;
    _authToken = null;
    _accessTokenExpireTime = null;

    await _storage.deleteSecureData(KeyConstants.autoToken);
    await _storage.deleteSecureData(KeyConstants.accessToken);

    try {
      Get.find<UserService>().handleLogout();
    } catch (e) {
      LogUtils.e('notify user logout error', error: e);
    }

    _messageService.showMessage(t.errors.pleaseLoginAgain, MDToastType.warning);

    LogUtils.d('user logout');
  }

  void resetProxy() {
    _dio.httpClientAdapter = IOHttpClientAdapter();
  }

  Future<void> _handleTokenExpiredSilently() async {
    if (!_isAuthenticated.value) {
      return;
    }

    _isAuthenticated.value = false;
    _accessToken = null;
    _authToken = null;
    _accessTokenExpireTime = null;

    _tokenRefreshTimer?.cancel();
    _tokenRefreshTimer = null;

    await _storage.deleteSecureData(KeyConstants.autoToken);
    await _storage.deleteSecureData(KeyConstants.accessToken);

    try {
      Get.find<UserService>().handleLogout();
    } catch (e) {
      LogUtils.e('notify user logout fail', tag: _tag, error: e);
    }

    LogUtils.d('user silently logout', _tag);
  }

  Future<void> logout() async {
    try {
      _authToken = null;
      _accessToken = null;
      _tokenExpireTime = null;
      _tokenRefreshTimer?.cancel();
      _isAuthenticated.value = false;
      await _storage.deleteSecureData(KeyConstants.autoToken);
      await _storage.deleteSecureData(KeyConstants.accessToken);
    } catch (e) {
      LogUtils.e('logout process fail', tag: _tag, error: e);
      _authToken = null;
      _accessToken = null;
      _tokenExpireTime = null;
      _isAuthenticated.value = false;
    }
  }

  Future<ApiResult> register(
    String email,
    String captchaId,
    String captchaAnswer,
  ) async {
    try {
      final headers = {'X-Captcha': '$captchaId:$captchaAnswer'};
      final data = {'email': email, 'locale': Get.locale?.countryCode ?? 'en'};
      final response = await _dio.post(
        '/user/register',
        data: data,
        options: dio.Options(headers: headers),
      );

      if (response.statusCode == 200 &&
          response.data['message'] == 'register.emailInstructionsSent') {
        LogUtils.d('register success send email', _tag);
        return ApiResult.success();
      } else {
        return ApiResult.fail(
          response.data['message'] ?? t.errors.registerFailed,
        );
      }
    } on dio.DioException catch (e) {
      LogUtils.e('register fail: ${e.message}', tag: _tag);
      if (e.response != null && e.response?.data != null) {
        var errorMessage =
            e.response!.data['errors']?[0]['message'] ??
            e.response!.data['message'] ??
            t.errors.unknownError;
        switch (errorMessage) {
          case 'errors.invalidEmail':
            return ApiResult.fail(t.errors.invalidEmail);
          case 'errors.emailAlreadyExists':
            return ApiResult.fail(t.errors.emailAlreadyExists);
          case 'errors.invalidCaptcha':
            return ApiResult.fail(t.errors.invalidCaptcha);
          case 'errors.tooManyRequests':
            return ApiResult.fail(t.errors.tooManyRequests);
          default:
            return ApiResult.fail(errorMessage);
        }
      } else {
        return ApiResult.fail(t.errors.networkError);
      }
    } catch (e) {
      LogUtils.e('register occur problem: $e', tag: _tag);
      return ApiResult.fail(t.errors.unknownError);
    }
  }
}

class AuthServiceException implements Exception {
  final String message;

  AuthServiceException(this.message);
}

class InvalidCredentialsException extends AuthServiceException {
  InvalidCredentialsException(super.message);
}

class NetworkException extends AuthServiceException {
  NetworkException(super.message);
}

class UnauthorizedException extends AuthServiceException {
  UnauthorizedException(super.message);
}
