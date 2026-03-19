import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart';

class ChatService {
  static const String baseUrl = 'http://localhost:8000'; // Change to your IP if testing on physical device

  Future<Stream<String>> chatStream(String conversationId, String message, String userName) async {
    final url = Uri.parse('$baseUrl/chat');
    final client = http.Client();
    final request = http.Request('POST', url);
    request.headers['Content-Type'] = 'application/json';
    request.body = jsonEncode({
      'conversation_id': conversationId,
      'message': message,
      'user_name': userName,
    });

    final response = await client.send(request);
    
    if (response.statusCode != 200) {
      throw Exception('Failed to connect to chat service');
    }

    return response.stream
        .transform(utf8.decoder);
  }

  Future<List<Map<String, dynamic>>> getHistory(String userName) async {
    final response = await http.get(Uri.parse('$baseUrl/history?user_name=$userName'))
        .timeout(const Duration(seconds: 10));
    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(jsonDecode(response.body));
    }
    return [];
  }

  Future<List<ChatMessage>> getMessages(String conversationId) async {
    final response = await http.get(Uri.parse('$baseUrl/history/$conversationId'))
        .timeout(const Duration(seconds: 10));
    if (response.statusCode == 200) {
      List data = jsonDecode(response.body);
      return data.map((m) => ChatMessage.fromJson(m)).toList();
    }
    return [];
  }

  Future<String> createNewChat(String userName) async {
    final response = await http.post(Uri.parse('$baseUrl/conversations/new?user_name=$userName'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['conversation_id'];
    }
    throw Exception('Failed to create new chat');
  }

  Future<String> getAbout() async {
    final response = await http.get(Uri.parse('$baseUrl/about'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['about'];
    }
    return 'About information not available.';
  }
}
