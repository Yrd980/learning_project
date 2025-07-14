import 'package:get/get.dart';

class RulesModel {
  final String id;
  final int weight;
  final Map<String, String> title;
  final Map<String, String> body;
  final String createdAt;
  final String updatedAt;

  RulesModel({
    required this.id,
    required this.weight,
    required this.title,
    required this.body,
    required this.createdAt,
    required this.updatedAt,
  });

  factory RulesModel.fromJson(Map<String, dynamic> json) {
    final Map<String, dynamic> titleMap = json['title'] as Map<String, dynamic>;
    final Map<String, String> title = titleMap.map(
      (key, value) => MapEntry(key, value.toString()),
    );

    final Map<String, dynamic> bodyMap = json['body'] as Map<String, dynamic>;
    final Map<String, String> body = bodyMap.map(
      (key, value) => MapEntry(key, value.toString()),
    );

    return RulesModel(
      id: json['id'],
      weight: json['weight'],
      title: title,
      body: body,
      createdAt: json['createdAt'],
      updatedAt: json['updatedAt'],
    );
  }

  String getLocalizedTitle() {
    final languageCode = Get.deviceLocale?.languageCode ?? 'en';
    if (title.containsKey(languageCode)) {
      return title[languageCode]!;
    }
    if (languageCode.startsWith('zh') && title.containsKey('zh')) {
      return title['zh']!;
    }
    return title['en'] ?? title.values.first;
  }

  String getLocalizedBody() {
    final languageCode = Get.deviceLocale?.languageCode ?? 'en';
    if (body.containsKey(languageCode)) {
      return body[languageCode]!;
    }
    if (languageCode.startsWith('zh') && body.containsKey('zh')) {
      return body['zh']!;
    }
    return body['en'] ?? body.values.first;
  }
}
