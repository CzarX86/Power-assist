import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'services/api_service.dart';

void main() {
  runApp(const PowerAssistApp());
}

class PowerAssistApp extends StatelessWidget {
  const PowerAssistApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Provider(
      create: (_) => ApiService(baseUrl: 'http://localhost:8000'),
      child: MaterialApp(
        title: 'Power Assist',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
          useMaterial3: true,
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
