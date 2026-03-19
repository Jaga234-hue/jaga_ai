import 'package:flutter/material.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import '../api/chat_service.dart';

class AboutUsScreen extends StatelessWidget {
  const AboutUsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final chatService = ChatService();

    return Scaffold(
      appBar: AppBar(
        title: const Text('About Jaga AI'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      extendBodyBehindAppBar: true,
      body: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF0F2027), Color(0xFF203A43), Color(0xFF2C5364)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
          ),
          FutureBuilder<String>(
            future: chatService.getAbout(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator(color: Colors.white));
              }

              if (snapshot.hasError) {
                return const Center(child: Text('Error loading information', style: TextStyle(color: Colors.white)));
              }

              return SafeArea(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Markdown(
                    data: snapshot.data ?? 'No information available.',
                    styleSheet: MarkdownStyleSheet(
                      p: const TextStyle(color: Colors.white, fontSize: 16),
                      h1: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                      h2: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                      listBullet: const TextStyle(color: Colors.white),
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
