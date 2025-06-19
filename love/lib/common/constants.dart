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

  static const String iwaraImgBaseUrl = 'https://i.iwara.tv';

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
