enum MessageRole { user, assistant }

class ChatMessage {
  final String content;
  final MessageRole role;
  final DateTime timestamp;

  ChatMessage({
    required this.content,
    required this.role,
    required this.timestamp,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      content: json['content'],
      role: json['role'] == 'user' ? MessageRole.user : MessageRole.assistant,
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}
