import 'package:flutter/material.dart';
import 'package:i_iwara/app/models/sort.model.dart';
import 'package:i_iwara/i18n/strings.g.dart';

class LogMasking {
  static const String placeholder = '***';

  static final List<RegExp> patterns = [
    RegExp(r'"password"\s*:\s*".*?"', caseSensitive: false),
    RegExp(r"'password'\s*:\s*'.*?'", caseSensitive: false),
    RegExp(r'<password>.*?</password>', caseSensitive: false),

    RegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),

    RegExp(
      r'"(token|key|secret)"\s*:\s*"[A-Za-z0-9\-_/+]+"',
      caseSensitive: false,
    ),
    RegExp(
      r"'(token|key|secret)'\s*:\s*'[A-Za-z0-9\-_/+]+'",
      caseSensitive: false,
    ),

    RegExp(
      r'Authorization:\s*Bearer\s+[A-Za-z0-9\-_/+]+',
      caseSensitive: false,
    ),
    RegExp(r'Authorization:\s*Basic\s+[A-Za-z0-9\-_/+]+', caseSensitive: false),

    RegExp(r'\b1[3-9]\d{9}\b'),

    RegExp(r'\b\d{17}[\dX]\b', caseSensitive: false),

    RegExp(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),

    RegExp(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'),

    RegExp(
      r'Access Token:?\s*[A-Za-z0-9\-_/+]+\.[A-Za-z0-9\-_/+]+\.[A-Za-z0-9\-_/+]+',
      caseSensitive: false,
    ),

    RegExp(
      r'Auth [Tt]oken:?\s*[A-Za-z0-9\-_/+]+\.[A-Za-z0-9\-_/+]+\.[A-Za-z0-9\-_/+]+',
    ),
  ];
}

class CommonConstants {
  CommonConstants._internal();

  static const String VERSION = '0.3.13';

  static String? applicationName = 'i_iwara';

  static String applicationNickname = 'love';

  static String packageName = 'm.c.g.a.i_iwara';

  static String launcherIconPath = 'assets/icon/launcher_icon_v2.png';

  static String defaultLanguagePlaceholder = '[TL]';

  static const String iwaraBaseUrl = 'https://www.iwara.tv';

  static const String iwaraDomain = 'iwara.tv';

  static const String iwaraApiBaseUrl = 'https://api.iwara.tv';

  static const String iwaraImageBaseUrl = 'https://i.iwara.tv';

  static bool isSetBrightness = false;

  static bool isSetVolume = false;

  static const String defaultAvatarUrl =
      '$iwaraBaseUrl/images/default-avatar.jpg';

  static const String defaultProfileHeaderUrl =
      '$iwaraBaseUrl/images/default-background.jpg';

  static int maxLogDatabaseSize = 1024 * 1024 * 1024;

  static const int logRetentionDays = 30;

  static bool enableLogPersistence = true;

  static List<Sort> mediaSorts = [
    Sort(
      id: SortId.trending,
      label: t.common.trending,
      icon: const Icon(Icons.trending_up),
    ),
    Sort(
      id: SortId.date,
      label: t.common.latest,
      icon: const Icon(Icons.new_releases),
    ),
    Sort(
      id: SortId.popularity,
      label: t.common.popular,
      icon: const Icon(Icons.star),
    ),
    Sort(
      id: SortId.likes,
      label: t.common.likesCount,
      icon: const Icon(Icons.thumb_up),
    ),
    Sort(
      id: SortId.views,
      label: t.common.viewsCount,
      icon: const Icon(Icons.remove_red_eye),
    ),
  ];

  static const List<Sort> translationSorts = [
    Sort(id: SortId.zhCN, label: '简体中文', extData: 'zh-CN'),
    Sort(id: SortId.zhTW, label: '繁體中文', extData: 'zh-TW'),

    Sort(id: SortId.enUS, label: 'English', extData: 'en-US'),

    Sort(id: SortId.ja, label: '日本語', extData: 'ja'),
    Sort(id: SortId.ko, label: '한국어', extData: 'ko'),
    Sort(id: SortId.vi, label: 'Tiếng Việt', extData: 'vi'),

    Sort(id: SortId.th, label: 'ภาษาไทย', extData: 'th'),
    Sort(id: SortId.id, label: 'Bahasa Indonesia', extData: 'id'),
    Sort(id: SortId.ms, label: 'Bahasa Melayu', extData: 'ms'),

    Sort(id: SortId.fr, label: 'Français', extData: 'fr'),
    Sort(id: SortId.de, label: 'Deutsch', extData: 'de'),
    Sort(id: SortId.es, label: 'Español', extData: 'es'),
    Sort(id: SortId.it, label: 'Italiano', extData: 'it'),
    Sort(id: SortId.pt, label: 'Português', extData: 'pt'),
    Sort(id: SortId.ru, label: 'Русский', extData: 'ru'),
  ];

  static String defaultThumbnailUrl =
      '$iwaraBaseUrl/images/default-thumbnail.jpg';

  static bool enableVibration = true;
  static bool enableR18 = false;

  static bool enableHistory = true;

  static String defaultPlaylistThumbnailUrl =
      '$iwaraBaseUrl/images/default-thumbnail.jpg';

  static int themeMode = 0;
  static bool useDynamicColor = true;
  static bool usePresetColor = true;
  static int currentPresetIndex = 0;
  static String currentCustomHex = '';
  static List<String> customThemeColors = [];

  static ColorScheme? dynamicLightColorScheme;
  static ColorScheme? dynamicDarkColorScheme;

  static bool isPaginated = false;

  static String avatarOriginalUrl(String id, String name) =>
      '$iwaraImageBaseUrl/image/original/$id/$name';

  static String avatarUrl(String id, String name) =>
      '$iwaraImageBaseUrl/image/avatar/$id/$name.jpg';

  static userProfileHeaderUrl(String? headerId) {
    if (headerId == null) {
      return defaultProfileHeaderUrl;
    }
    return '$iwaraBaseUrl/image/profileHeader/$headerId/$headerId.jpg';
  }
}

class KeyConstants {
  static const String autoToken = 'auth_token';
  static const String accessToken = 'access_token';
}

class ApiConstants {
  static String rules = '/rules';

  static String user = '/user';

  static String userCounts = '/user/counts';

  static String userNotificationAllRead = '/notifications/all/read';

  static String autocompleteUsers = '/autocomplete/users';

  static String userWithId(String userId) => '/user/$userId';

  static String videos() => '/videos';

  static String images() => '/images';

  static String profilePrefix() => '/profile';

  static String galleryDetail() => '/image';

  static String videoDetail() => '/video';

  static String userProfile(String userName) => '/profile/$userName';

  static String userFollowers(String userId) => '/user/$userId/followers';

  static String userFollowing(String userId) => '/user/$userId/following';

  static String userRelationshipStatus(String userId) =>
      '/user/$userId/friends/status';

  static String userAddOrRemoveFriend(String userId) => '/user/$userId/friends';

  static String userFollowOrUnfollow(String userId) =>
      '/user/$userId/followers';

  static String comments(String type, String id) => '/$type/$id/comments';

  static String tags() => '/tags';

  static String imageDetail(String imageModelId) => '/image/$imageModelId';

  static String relatedVideos(String id) => '/video/$id/related';

  static String relatedImages(String mediaId) => '/image/$mediaId/related';

  static String videoLikes(String videoId) => '/video/$videoId/likes';

  static String imageLikes(String imageId) => '/image/$imageId/likes';

  static String lightVideo(String videoId) => '/light/video/$videoId';

  static String lightForum(String forumId) => '/light/forum/$forumId';

  static String lightImage(String imageId) => '/light/image/$imageId';

  static String lightProfile(String userId) => '/light/profile/$userId';

  static String lightPlaylist(String playlistId) =>
      '/light/playlist/$playlistId';

  static String search() => '/search';

  static String favoriteVideos() => '/favorites/videos';

  static String favoriteImages() => '/favorites/images';

  static String likeImage(String mediaId) => '/image/$mediaId/like';

  static String likeVideo(String mediaId) => '/video/$mediaId/like';

  static String userFriends(String userId) => '/user/$userId/friends';

  static String userFriendsRequests(String userId) =>
      '/user/$userId/friends/requests';

  static String comment(String id) => '/comment/$id';

  static String posts() => '/posts';

  static String post(String id) => '/post/$id';

  static String userPostCooldown() => '/user/post/cooldown';

  static String forumThreadCooldown() => '/user/forumThread/cooldown';

  static String forum() => '/forum';

  static String forumThread(String forumCategoryId) =>
      '/forum/$forumCategoryId';

  static String forumThreadReply(String threadId) => '/forum/$threadId/reply';

  static String forumThreadsWithCategoryId(String categoryId) =>
      '/forum/$categoryId';

  static String forumThreads() => '/forum/threads';

  static String forumPosts(String postId) => '/forum/post/$postId';

  static String forumThreadDetail(String categoryId, String threadId) =>
      '/forum/$categoryId/$threadId';

  static String userNotifications(String userId) =>
      '/user/$userId/notifications';

  static String userNotificationWithId(String notificationId) =>
      '/notifications/$notificationId/read';

  static String userConversations(String userId) =>
      '/user/$userId/conversations';

  static String conversationMessages(String conversationId) =>
      '/conversation/$conversationId/messages';

  static String messageWithId(String messageId) => '/message/$messageId';

  static String video(String videoId) => '/video/$videoId';

  static String lightRule(String ruleId) => '/light/rule/$ruleId';
}

enum SortId {
  trending,
  date,
  popularity,
  likes,
  views,
  // 中文
  zhCN,
  zhTW,
  zhHK,
  // 英语变体
  enUS,
  enGB,
  // 东亚语言
  ja,
  ko,
  vi,
  // 东南亚语言
  th,
  id,
  ms,
  // 欧洲语言
  fr,
  de,
  es,
  it,
  pt,
  ru,
}
