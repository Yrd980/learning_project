import 'package:i_iwara/app/models/user.model.dart';

class ForumCategoryTreeModel {
  final String name;
  final List<ForumCategoryModel> children;

  ForumCategoryTreeModel({required this.name, required this.children});

  Map<String, dynamic> toJson() {
    return {'name': name, 'children': children.map((e) => e.toJson()).toList()};
  }
}

class ForumCategoryModel {
  final String id;
  final String group;
  final String label;
  final String description;
  final bool locked;
  final int numPosts;
  final int numThreads;
  final ForumThreadModel? lastThread;

  ForumCategoryModel({
    required this.id,
    required this.group,
    required this.label,
    required this.description,
    required this.locked,
    required this.numPosts,
    required this.numThreads,
    required this.lastThread,
  });

  factory ForumCategoryModel.fromJson(Map<String, dynamic> json) {
    return ForumCategoryModel(
      id: json['id'],
      group: json['group'],
      label: json['label'] ?? json['id'],
      description: json['description'] ?? '',
      locked: json['locked'],
      numPosts: json['numPosts'],
      numThreads: json['numThreads'],
      lastThread: json['lastThread'] != null
          ? ForumThreadModel.fromJson(json['lastThread'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'group': group,
      'label': label,
      'description': description,
      'locked': locked,
      'numPosts': numPosts,
      'numThreads': numThreads,
      'lastThread': lastThread?.toJson(),
    };
  }
}

class ForumThreadModel {
  final String id;
  final bool approved;
  final String? slug;
  final String section;
  final String title;
  final bool locked;
  final bool sticky;
  final ThreadCommentModel? lastPost;
  final int numViews;
  final int numPosts;
  final DateTime createdAt;
  final DateTime updatedAt;
  final User user;

  ForumThreadModel({
    required this.id,
    required this.approved,
    this.slug,
    required this.section,
    required this.title,
    required this.locked,
    required this.sticky,
    required this.lastPost,
    required this.numViews,
    required this.numPosts,
    required this.createdAt,
    required this.updatedAt,
    required this.user,
  });

  factory ForumThreadModel.fromJson(Map<String, dynamic> json) {
    return ForumThreadModel(
      id: json['id'],
      approved: json['approved'],
      slug: json['slug'],
      section: json['section'],
      title: json['title'],
      locked: json['locked'],
      sticky: json['sticky'],
      lastPost: json['lastPost'] != null
          ? ThreadCommentModel.fromJson(json['lastPost'])
          : null,
      numViews: json['numViews'],
      numPosts: json['numPosts'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
      user: User.fromJson(json['user']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'approved': approved,
      'slug': slug,
      'section': section,
      'title': title,
      'locked': locked,
      'sticky': sticky,
      'lastPost': lastPost?.toJson(),
      'numViews': numViews,
      'numPosts': numPosts,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
      'user': user.toJson(),
    };
  }
}

class ThreadCommentModel {
  final String id;
  final bool approved;
  final String body;
  final int replyNum;
  final User user;
  final dynamic thread;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String threadId;

  ThreadCommentModel({
    required this.id,
    required this.approved,
    required this.body,
    required this.replyNum,
    required this.user,
    this.thread,
    required this.createdAt,
    required this.updatedAt,
    required this.threadId,
  });

  factory ThreadCommentModel.fromJson(Map<String, dynamic> json) {
    return ThreadCommentModel(
      id: json['id'],
      approved: json['approved'],
      body: json['body'],
      replyNum: json['replyNum'],
      user: User.fromJson(json['user']),
      thread: json['thread'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
      threadId: json['threadId'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'approved': approved,
      'body': body,
      'replyNum': replyNum,
      'user': user.toJson(),
      'thread': thread,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
      'threadId': threadId,
    };
  }
}
