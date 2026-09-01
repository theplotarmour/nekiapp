class User {
  final String id;
  final String name;
  final String email;
  final int impactScore;
  final bool isVerified;
  final String avatarUrl;

  User({
    required this.id,
    required this.name,
    required this.email,
    this.impactScore = 0,
    this.isVerified = false,
    this.avatarUrl = '',
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      impactScore: json['impactScore'] as int? ?? 0,
      isVerified: json['isVerified'] as bool? ?? false,
      avatarUrl: json['avatarUrl'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'impactScore': impactScore,
      'isVerified': isVerified,
      'avatarUrl': avatarUrl,
    };
  }
}
