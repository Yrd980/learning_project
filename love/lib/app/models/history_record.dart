import 'dart:convert';

import 'package:i_iwara/app/models/forum.model.dart';
import 'package:i_iwara/app/models/image.model.dart';
import 'package:i_iwara/app/models/video.model.dart';
import 'package:i_iwara/app/models/post.model.dart';

class HistoryRecord {
  final int id;
  final String itemId;
  final String itemType;
  final String title;
  final String? thumbnailUrl;
  final String? author;
  final String? authorId;
  final String data;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  HistoryRecord({
    required this.id,
    required this.itemId,
    required this.itemType,
    required this.title,
    this.thumbnailUrl,
    this.author,
    this.authorId,
    required this.data,
    this.createdAt,
    this.updatedAt,
  });

  factory HistoryRecord.fromVideo(Video video) {
    return HistoryRecord(
      id: 0,
      itemId: video.id,
      itemType: 'video',
      title: video.title ?? 'no title',
      thumbnailUrl: video.thumbnailUrl,
      author: video.user?.name,
      authorId: video.user?.id,
      data: jsonEncode(video.toJson()),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  factory HistoryRecord.fromImageModel(ImageModel image) {
    return HistoryRecord(
      id: 0,
      itemId: image.id,
      itemType: 'image',
      title: image.title,
      thumbnailUrl: image.thumbnailUrl,
      author: image.user?.name,
      authorId: image.user?.id,
      data: jsonEncode(image.toJson()),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  factory HistoryRecord.fromPost(PostModel post) {
    return HistoryRecord(
      id: 0,
      itemId: post.id,
      itemType: 'post',
      title: post.title,
      thumbnailUrl: null, // 帖子可能没有缩略图
      author: post.user.name,
      authorId: post.user.id,
      data: jsonEncode(post.toJson()),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  factory HistoryRecord.fromThread(ForumThreadModel thread) {
    return HistoryRecord(
      id: 0,
      itemId: thread.id,
      itemType: 'thread',
      title: thread.title,
      thumbnailUrl: null,
      author: thread.user.name,
      authorId: thread.user.id,
      data: jsonEncode(thread.toJson()),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  dynamic getOriginalData() {
    final Map<String, dynamic> jsonData = jsonDecode(data);
    switch (itemType) {
      case 'video':
        return Video.fromJson(jsonData);
      case 'image':
        return ImageModel.fromJson(jsonData);
      case 'post':
        return PostModel.fromJson(jsonData);
      case 'thread':
        return ForumThreadModel.fromJson(jsonData);
      default:
        throw Exception('unknown type : $itemType');
    }
  }

  factory HistoryRecord.fromJson(Map<String, dynamic> json) {
    return HistoryRecord(
      id: json['id'],
      itemId: json['item_id'],
      itemType: json['item_type'],
      title: json['title'],
      thumbnailUrl: json['thumbnail_url'],
      author: json['author'],
      authorId: json['author_id'],
      data: json['data'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'item_id': itemId,
      'item_type': itemType,
      'title': title,
      'thumbnail_url': thumbnailUrl,
      'author': author,
      'author_id': authorId,
      'data': data,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}
