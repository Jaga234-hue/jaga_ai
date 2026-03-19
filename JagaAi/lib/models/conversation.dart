class Conversation {
  final String id;
  final String title;
  final String userName;
  final DateTime createdAt;

  Conversation({
    required this.id,
    required this.title,
    required this.userName,
    required this.createdAt,
  });

  factory Conversation.fromJson(Map<String, dynamic> json) {
    return Conversation(
      id: json['id'],
      title: json['title'],
      userName: json['user_name'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
