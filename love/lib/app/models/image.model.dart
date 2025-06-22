import 'package:i_iwara/app/models/media_file.model.dart';
import 'package:i_iwara/app/models/tag.model.dart';
import 'package:i_iwara/app/models/user.model.dart';
import 'package:i_iwara/common/constants.dart';

import 'custom_thumbnail.model.dart';

class ImageModel {
  final String id;
  final String status;
  final String body;
  final String slug;
  final String title;
  final CustomThumbnail? thumbnail;
  final String rating;
  final bool liked;
  final int numImages;
  final int numLikes;
  final int numViews;
  final int numComments;

  final User? user;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  final List<MediaFile> files;
  final List<Tag> tags;

  ImageModel({
    required this.id,
    this.status = 'active',
    this.body = '',
    this.slug = '',
    this.title = '',
    this.thumbnail,
    this.rating = 'ecchi',
    this.liked = false,
    this.numImages = 0,
    this.numLikes = 0,
    this.numViews = 0,
    this.numComments = 0,
    this.user,
    this.createdAt,
    this.updatedAt,
    this.files = const [],
    this.tags = const [],
  });

  factory ImageModel.fromJson(Map<String, dynamic> json) {
    return ImageModel(
      id: json['id'] ?? '',
      status: json['status'] ?? 'active',
      body: json['body'] ?? '',
      slug: json['slug'] ?? '',
      title: json['title'] ?? '',
      thumbnail: json['thumbnail'] != null
          ? CustomThumbnail.fromJson(json['thumbnail'])
          : null,
      rating: json['rating'] ?? 'ecchi',
      liked: json['liked'] ?? false,
      numImages: json['numImages'] ?? 0,
      numLikes: json['numLikes'] ?? 0,
      numViews: json['numViews'] ?? 0,
      numComments: json['numComments'] ?? 0,
      user: json['user'] != null ? User.fromJson(json['user']) : null,
      createdAt: json['createdAt'] != null
          ? DateTime.parse(json['createdAt'])
          : null,
      updatedAt: json['updatedAt'] != null
          ? DateTime.parse(json['updatedAt'])
          : null,
      files: json['files'] != null
          ? (json['files'] as List)
                .map((file) => MediaFile.fromJson(file))
                .toList()
          : [],
      tags: json['tags'] != null
          ? (json['tags'] as List).map((tag) => Tag.fromJson(tag)).toList()
          : [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'status': status,
      'body': body,
      'slug': slug,
      'title': title,
      'thumbnail': thumbnail?.toJson(),
      'rating': rating,
      'liked': liked,
      'numImages': numImages,
      'numLikes': numLikes,
      'numViews': numViews,
      'numComments': numComments,
      'user': user?.toJson(),
      'createdAt': createdAt?.toIso8601String(),
      'updatedAt': updatedAt?.toIso8601String(),
      'files': files.map((file) => file.toJson()).toList(),
      'tags': tags.map((tag) => tag.toJson()).toList(),
    };
  }

  ImageModel copyWith({
    String? id,
    String? status,
    String? body,
    String? slug,
    String? title,
    CustomThumbnail? thumbnail,
    String? rating,
    bool? liked,
    int? numImages,
    int? numLikes,
    int? numViews,
    int? numComments,
    User? user,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<MediaFile>? files,
    List<Tag>? tags,
  }) {
    return ImageModel(
      id: id ?? this.id,
      status: status ?? this.status,
      body: body ?? this.body,
      slug: slug ?? this.slug,
      title: title ?? this.title,
      thumbnail: thumbnail ?? this.thumbnail,
      rating: rating ?? this.rating,
      liked: liked ?? this.liked,
      numImages: numImages ?? this.numImages,
      numLikes: numLikes ?? this.numLikes,
      numViews: numViews ?? this.numViews,
      numComments: numComments ?? this.numComments,
      user: user ?? this.user,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      files: files ?? this.files,
      tags: tags ?? this.tags,
    );
  }

  String get thumbnailUrl {
    if (thumbnail != null) {
      String url =
          'https://i.iwara.tv/image/thumbnail/${thumbnail!.id}/${thumbnail!.name}';
      return url.replaceAll('.${thumbnail!.name.split('.').last}', '.jpg');
    } else {
      return CommonConstants.defaultThumbnailUrl;
    }
  }
}
