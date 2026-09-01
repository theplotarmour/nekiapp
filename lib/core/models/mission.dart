class Mission {
  final String id;
  final String title;
  final String description;
  final String category;
  final String location;
  final double distance;
  final int requiredVolunteers;
  final int currentVolunteers;
  final bool isUrgent;
  final String status;
  final String imageUrl;

  Mission({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.location,
    required this.distance,
    required this.requiredVolunteers,
    required this.currentVolunteers,
    this.isUrgent = false,
    this.status = 'active',
    this.imageUrl = '',
  });

  factory Mission.fromJson(Map<String, dynamic> json) {
    return Mission(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String,
      category: json['category'] as String,
      location: json['location'] as String,
      distance: (json['distance'] as num).toDouble(),
      requiredVolunteers: json['requiredVolunteers'] as int,
      currentVolunteers: json['currentVolunteers'] as int,
      isUrgent: json['isUrgent'] as bool? ?? false,
      status: json['status'] as String? ?? 'active',
      imageUrl: json['imageUrl'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'category': category,
      'location': location,
      'distance': distance,
      'requiredVolunteers': requiredVolunteers,
      'currentVolunteers': currentVolunteers,
      'isUrgent': isUrgent,
      'status': status,
    };
  }
}
