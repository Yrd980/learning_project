import 'dart:async';
import 'package:get/get.dart';
import 'package:i_iwara/app/models/dto/profile_user_dto.dart';
import 'package:i_iwara/app/models/dto/user_request_dto.dart';
import 'package:i_iwara/app/models/page_data.model.dart';
import 'package:i_iwara/app/models/user_notification_count.model.dart';
import 'package:i_iwara/i18n/strings.g.dart';

import '../../common/constants.dart';
import '../../utils/logger_utils.dart';
import '../models/api_result.model.dart';
import '../models/user.model.dart';
import '../routes/app_routes.dart';
import 'api_service.dart';
import 'auth_service.dart';

class UserService extends GetxService {
  final AuthService _authService = Get.find<AuthService>();
  final ApiService _apiService = Get.find<ApiService>();

  final String _tag = '[UserService]';

  Rxn<User> currentUser = Rxn<User>();
  RxInt notificationCount = RxInt(0);
  RxInt friendRequestsCount = RxInt(0);

  RxInt messagesCount = RxInt(0);
  Timer? _notificationTimer;

  bool get isLogin => currentUser.value != null;
  RxBool isLogining = RxBool(false);

  String get userAvatar =>
      currentUser.value?.avatar?.avatarUrl ?? CommonConstants.defaultAvatarUrl;

  void startNotificationTimer() {
    if (_notificationTimer == null) {
      _notificationTimer = Timer.periodic(const Duration(minutes: 15), (
        timer,
      ) async {
        if (_authService.hasToken) {
          await refreshNotificationCount();
        }
      });

      if (_authService.hasToken) {
        refreshNotificationCount();
      }
    }
  }

  void stopNotificationTimer() {
    _notificationTimer?.cancel();
    _notificationTimer = null;
  }

  void clearAllNotificationCounts() {
    stopNotificationTimer();
    notificationCount.value = 0;
    friendRequestsCount.value = 0;
    messagesCount.value = 0;
  }

  Future<void> refreshNotificationCount() async {
    try {
      final result = await fetchUserNotificationCount();
      if (result.data != null) {
        notificationCount.value = result.data?.notifications ?? 0;
        friendRequestsCount.value = result.data?.friendRequests ?? 0;
        messagesCount.value = result.data?.messages ?? 0;
      }
    } catch (e) {
      LogUtils.e('fetch notification count fail', tag: _tag, error: e);
    }
  }

  @override
  void onClose() {
    stopNotificationTimer();
    super.onClose();
  }

  Future<void> logout() async {
    try {
      await _authService.logout();
      currentUser.value = null;
    } catch (e) {
      LogUtils.e('user logout fail', error: e);
      throw AuthServiceException(t.errors.failedToOperate);
    }
  }

  Future<ApiResult> followUser(String userId) async {
    if (userId.isEmpty) {
      return ApiResult.fail(t.errors.invalidParameter);
    }

    if (!_authService.hasToken) {
      Get.toNamed(Routes.LOGIN);
      return ApiResult.fail(t.errors.pleaseLoginFirst);
    }

    try {
      await _apiService.post(ApiConstants.userFollowOrUnfollow(userId));
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('follow fail', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult> unfollowUser(String userId) async {
    if (userId.isEmpty) {
      return ApiResult.fail(t.errors.invalidParameter);
    }

    if (!_authService.hasToken) {
      Get.toNamed(Routes.LOGIN);
      return ApiResult.fail(t.errors.pleaseLoginFirst);
    }

    try {
      await _apiService.delete(ApiConstants.userFollowOrUnfollow(userId));
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('unfollow fail', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult> removeFriend(String userId) async {
    if (userId.isEmpty) {
      return ApiResult.fail(t.errors.invalidParameter);
    }

    if (!_authService.hasToken) {
      Get.toNamed(Routes.LOGIN);
      return ApiResult.fail(t.errors.pleaseLoginFirst);
    }

    try {
      await _apiService.delete(ApiConstants.userAddOrRemoveFriend(userId));
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('remove friend fail', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult> addFriend(String userId) async {
    if (userId.isEmpty) {
      return ApiResult.fail(t.errors.invalidParameter);
    }

    if (!_authService.hasToken) {
      Get.toNamed(Routes.LOGIN);
      return ApiResult.fail(t.errors.pleaseLoginFirst);
    }

    try {
      await _apiService.post(ApiConstants.userAddOrRemoveFriend(userId));
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('send friend request fail', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult> acceptFriendRequest(String requestId) async {
    return addFriend(requestId);
  }

  Future<ApiResult> rejectFriendRequest(String requestId) async {
    return removeFriend(requestId);
  }

  Future<ApiResult> cancelFriendRequest(String requestId) async {
    return removeFriend(requestId);
  }

  Future<ApiResult<PageData<User>>> fetchFriends({
    int page = 0,
    int limit = 20,
    required String userId,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.userFriends(userId),
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<User> results = (response.data['results'] as List)
          .map((userJson) => User.fromJson(userJson))
          .map((user) => user.copyWith(friend: true))
          .toList();

      final PageData<User> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );

      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get friend list fail', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult<PageData<UserRequestDTO>>> fetchUserFriendsRequests({
    int page = 0,
    int limit = 20,
    required String userId,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.userFriendsRequests(userId),
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<UserRequestDTO> results = (response.data['results'] as List)
          .map((userJson) => UserRequestDTO.fromJson(userJson))
          .toList();

      final PageData<UserRequestDTO> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );

      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get friend request list fail', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }

  Future<ApiResult<PageData<User>>> fetchFollowingUsers({
    int page = 0,
    int limit = 20,
    required String userId,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.userFollowing(userId),
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<User> results = (response.data['results'] as List)
          .map((item) => User.fromJson(item['user']))
          .toList();

      final PageData<User> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );
      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get follower list fail', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }

  Future<ApiResult<PageData<User>>> fetchFollowers({
    int page = 0,
    int limit = 20,
    required String userId,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.userFollowers(userId),
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<User> results = (response.data['results'] as List)
          .map((item) => User.fromJson(item['follower']))
          .toList();

      final PageData<User> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );
      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get follower list fail', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }

  void handleLogout() {
    currentUser.value = null;

    clearAllNotificationCounts();
    stopNotificationTimer();

    notificationCount.value = 0;
    friendRequestsCount.value = 0;
    messagesCount.value = 0;

    LogUtils.d('user service state clear', _tag);
  }

  Future<ApiResult<ProfileUserDto>> fetchProfileUser() async {
    try {
      final response = await _apiService.get(ApiConstants.user);
      return ApiResult.success(data: ProfileUserDto.fromJson(response.data));
    } catch (e) {
      LogUtils.e('get currentUser information fail', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }

  UserService() {
    LogUtils.d('$_tag init user service');
    if (_authService.hasToken) {
      try {
        LogUtils.d('$_tag exist valid TOKEN try to get user information');
        fetchUserProfile();
      } catch (e) {
        LogUtils.e('$_tag init user service fail', error: e);
      }
    } else {
      LogUtils.d('$_tag unlogin');
    }
  }

  Future<void> fetchUserProfile() async {
    try {
      isLogining.value = true;
      LogUtils.d('$_tag fetch user information');
      final response = await _apiService.get<Map<String, dynamic>>('/user');
      LogUtils.d('$_tag get user information');
      currentUser.value = User.fromJson(response.data!['user']);
      LogUtils.d('$_tag user information parse complete: ${currentUser.value}');
      startNotificationTimer();
    } catch (e) {
      LogUtils.e('get user information fail', error: e);
      if (e is! UnauthorizedException) {
        throw AuthServiceException(t.errors.failedToOperate);
      }
      rethrow;
    } finally {
      isLogining.value = false;
    }
  }

  Future<ApiResult<UserNotificationCount>> fetchUserNotificationCount() async {
    try {
      final response = await _apiService.get(ApiConstants.userCounts);
      return ApiResult.success(
        data: UserNotificationCount.fromJson(response.data),
      );
    } catch (e) {
      LogUtils.e('获取消息 count 失败', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }

  Future<ApiResult<PageData<Map<String, dynamic>>>> fetchUserNotifications(
    String userId, {
    int page = 0,
    int limit = 20,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.userNotifications(userId),
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<Map<String, dynamic>> results =
          (response.data['results'] as List)
              .map((item) => item as Map<String, dynamic>)
              .toList();

      final PageData<Map<String, dynamic>> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );
      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get notification information fail', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }
}
