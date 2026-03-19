import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const JagaAiApp());
}

class JagaAiApp extends StatelessWidget {
  const JagaAiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jaga AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorSchemeSeed: Colors.teal,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
