import 'package:i_iwara/app/models/video.model.dart';

enum DownloadTaskExtDataType { video, gallery }

class DownloadTaskExtData {
  final DownloadTaskExtDataType type;
  final Map<String, dynamic> data;

  DownloadTaskExtData({required this.type, required this.data});

  factory DownloadTaskExtData.fromJson(Map<String, dynamic> json) {
    return DownloadTaskExtData(
      type: DownloadTaskExtDataType.values.byName(json['type']),
      data: json['data'] as Map<String, dynamic>,
    );
  }

  Map<String, dynamic> toJson() {
    return {'type': type.name, 'data': data};
  }
}

class VideoDownloadExtData {
  final String? id;
  final String? title;
  final String? thumbnail;
  final String? authorName;
  final String? authorUsername;
  final String? authorAvatar;
  final int? duration;
  final String? quality;

  VideoDownloadExtData({
    this.id,
    this.title,
    this.thumbnail,
    this.authorName,
    this.authorUsername,
    this.authorAvatar,
    this.duration,
    this.quality,
  });

  factory VideoDownloadExtData.fromJson(Map<String, dynamic> json) {
    return VideoDownloadExtData(
      id: json['id'] as String?,
      title: json['title'] as String?,
      thumbnail: json['thumbnail'] as String?,
      authorName: json['author_name'] as String?,
      authorUsername: json['author_username'] as String?,
      authorAvatar: json['author_avatar'] as String?,
      duration: json['duration'] as int?,
      quality: json['quality'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'thumbnail': thumbnail,
      'author_name': authorName,
      'author_username': authorUsername,
      'author_avatar': authorAvatar,
      'duration': duration,
      'quality': quality,
    };
  }

  static String genExtDataIdByVideoInfo(Video videoInfo, String sourceName) {
    return '${DownloadTaskExtDataType.video.name}_${videoInfo.id}_$sourceName';
  }
}

class GalleryDownloadExtData {
  final String? id;
  final String? title;
  final List<String> previewUrls;
  final String? authorName;
  final String? authorUsername;
  final String? authorAvatar;
  final int totalImages;
  final Map<String, String> imageList;
  final Map<String, String> localPaths;

  GalleryDownloadExtData({
    this.id,
    this.title,
    this.previewUrls = const [],
    this.authorName,
    this.authorUsername,
    this.authorAvatar,
    this.totalImages = 0,
    this.imageList = const {}, // 默认值改为空Map
    this.localPaths = const {},
  });

  factory GalleryDownloadExtData.fromJson(Map<String, dynamic> json) {
    return GalleryDownloadExtData(
      id: json['id'] as String?,
      title: json['title'] as String?,
      previewUrls:
          (json['preview_urls'] as List<dynamic>?)?.cast<String>() ?? [],
      authorName: json['author_name'] as String?,
      authorUsername: json['author_username'] as String?,
      authorAvatar: json['author_avatar'] as String?,
      totalImages: json['total_images'] as int? ?? 0,
      imageList:
          (json['image_list'] as Map<String, dynamic>?)
              ?.cast<String, String>() ??
          {},
      localPaths:
          (json['local_paths'] as Map<String, dynamic>?)
              ?.cast<String, String>() ??
          {},
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'preview_urls': previewUrls,
      'author_name': authorName,
      'author_username': authorUsername,
      'author_avatar': authorAvatar,
      'total_images': totalImages,
      'image_list': imageList,
      'local_paths': localPaths,
    };
  }

  static String genExtDataIdByGalleryInfo(String id) {
    return '${DownloadTaskExtDataType.gallery.name}_$id';
  }
}
