class UserNotificationCount {
  final int messages;
  final int notifications;
  final int friendRequests;

  UserNotificationCount({
    required this.messages,
    required this.notifications,
    required this.friendRequests,
  });

  factory UserNotificationCount.fromJson(Map<String, dynamic> json) {
    return UserNotificationCount(
      messages: json['messages'],
      notifications: json['notifications'],
      friendRequests: json['friendRequests'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'messages': messages,
      'notifications': notifications,
      'friendRequests': friendRequests,
    };
  }
}
