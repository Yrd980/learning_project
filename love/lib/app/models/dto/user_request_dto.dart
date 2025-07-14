import 'package:i_iwara/app/models/user.model.dart';

class UserRequestDTO {
  final String id;
  final DateTime createdAt;
  final User target;
  final User user;

  UserRequestDTO({
    required this.id,
    required this.createdAt,
    required this.target,
    required this.user,
  });

  factory UserRequestDTO.fromJson(Map<String, dynamic> json) {
    return UserRequestDTO(
      id: json['id'],
      createdAt: DateTime.parse(json['createdAt']),
      target: User.fromJson(json['target']),
      user: User.fromJson(json['user']),
    );
  }
}
