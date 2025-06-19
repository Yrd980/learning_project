class VideoSource {
  final String id;
  final String? name;
  final String? view;
  final String? download;
  final String? type;
  final DateTime? createdAt;
  final DateTime? updatedAt;
  final VideoSrc? src;

  VideoSource({
    required this.id,
    this.name,
    this.view,
    this.download,
    this.type,
    this.createdAt,
    this.updatedAt,
    this.src,
  });

  factory VideoSource.fromJson(Map<String, dynamic> json) {
    return VideoSource(
      id: json['id'],
      name: json['name'],
      view: json['src'] != null ? 'https:${json['src']['view']}' : null,
      download: json['src'] != null ? 'https:${json['src']['download']}' : null,
      type: json['type'],
      createdAt: json['createdAt'] != null
          ? DateTime.parse(json['createdAt'])
          : null,
      updatedAt: json['updatedAt'] != null
          ? DateTime.parse(json['updatedAt'])
          : null,
      src: json['src'] != null ? VideoSrc.fromJson(json['src']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'type': type,
      'createdAt': createdAt?.toIso8601String(),
      'updatedAt': updatedAt?.toIso8601String(),
      'src': src?.toJson(),
    };
  }
}

class VideoSrc {
  final String? view;
  final String? download;

  VideoSrc({
    this.view, // 视频播放源
    this.download,
  });

  factory VideoSrc.fromJson(Map<String, dynamic> json) {
    return VideoSrc(
      view: json['view'], // 视频播放源
      download: json['download'],
    );
  }

  Map<String, dynamic> toJson() {
    return {'view': view, 'download': download};
  }
}
