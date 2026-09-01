import 'package:flutter/material.dart';

class AppTheme {
  // Brand Colors (Apple/Premium minimal style)
  static const Color offWhite = Color(0xFFFAF9F7);
  static const Color richBlack = Color(0xFF111111);
  static const Color nekiGold = Color(0xFFD4AF6A);
  static const Color secondaryText = Color(0xFF6B6B6B);
  
  // Status Colors
  static const Color forestGreen = Color(0xFF1B4332);
  static const Color urgentRed = Color(0xFFE63946);

  static ThemeData get lightTheme {
    return ThemeData(
      scaffoldBackgroundColor: offWhite,
      primaryColor: richBlack,
      colorScheme: const ColorScheme.light(
        primary: richBlack,
        secondary: nekiGold,
        surface: Colors.white,
        background: offWhite,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: offWhite,
        elevation: 0,
        scrolledUnderElevation: 0,
        iconTheme: IconThemeData(color: richBlack),
        titleTextStyle: TextStyle(
          color: richBlack,
          fontSize: 20,
          fontWeight: FontWeight.w800,
        ),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(color: richBlack, fontWeight: FontWeight.w800),
        titleLarge: TextStyle(color: richBlack, fontWeight: FontWeight.w700),
        bodyLarge: TextStyle(color: richBlack),
        bodyMedium: TextStyle(color: Color(0xFF4B5563)), // Gray 600
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: offWhite,
        selectedItemColor: nekiGold,
        unselectedItemColor: Color(0xFF9CA3AF), // Gray 400
        type: BottomNavigationBarType.fixed,
        elevation: 8,
      ),
    );
  }
}
