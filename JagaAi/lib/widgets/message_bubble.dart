import 'package:flutter/material.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import 'package:intl/intl.dart';
import '../models/chat_message.dart';

class MessageBubble extends StatelessWidget {
  final ChatMessage message;

  const MessageBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    bool isUser = message.role == MessageRole.user;
    
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 12.0),
      child: Column(
        crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (!isUser) ...[
                const CircleAvatar(
                  backgroundColor: Color(0xFF10A37F),
                  child: Icon(Icons.rocket_launch, color: Colors.white, size: 20),
                ),
                const SizedBox(width: 8),
              ],
              Flexible(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  decoration: BoxDecoration(
                    color: isUser 
                        ? const Color(0xFF007AFF) 
                        : Colors.white.withAlpha(230),
                    borderRadius: BorderRadius.only(
                      topLeft: const Radius.circular(20),
                      topRight: const Radius.circular(20),
                      bottomLeft: Radius.circular(isUser ? 20 : 0),
                      bottomRight: Radius.circular(isUser ? 0 : 20),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withAlpha(25),
                        blurRadius: 5,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: isUser 
                    ? Text(
                        message.content,
                        style: const TextStyle(color: Colors.white, fontSize: 16),
                      )
                    : MarkdownBody(
                        data: message.content,
                        styleSheet: MarkdownStyleSheet(
                          p: const TextStyle(color: Colors.black87, fontSize: 16),
                          h1: const TextStyle(color: Colors.black, fontSize: 24, fontWeight: FontWeight.bold),
                          h2: const TextStyle(color: Colors.black, fontSize: 20, fontWeight: FontWeight.bold),
                          listBullet: const TextStyle(color: Colors.black87),
                        ),
                      ),
                ),
              ),
              if (isUser) ...[
                const SizedBox(width: 8),
                const CircleAvatar(
                  backgroundColor: Colors.blueAccent,
                  child: Icon(Icons.person, color: Colors.white, size: 20),
                ),
              ],
            ],
          ),
          Padding(
            padding: const EdgeInsets.only(top: 4.0, left: 48, right: 48),
            child: Text(
              DateFormat('hh:mm a').format(message.timestamp),
              style: TextStyle(color: Colors.white70, fontSize: 10),
            ),
          ),
        ],
      ),
    );
  }
}
