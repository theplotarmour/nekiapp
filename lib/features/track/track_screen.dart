import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/theme/app_theme.dart';

class TrackScreen extends StatelessWidget {
  const TrackScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.offWhite,
      body: Stack(
        children: [
          // Simulated 3D Map
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                color: Colors.grey.shade200,
                image: const DecorationImage(
                  image: NetworkImage('https://maps.googleapis.com/maps/api/staticmap?center=28.5355,77.3910&zoom=15&size=600x800&maptype=roadmap&style=feature:all|element:labels.text.fill|color:0x222222&key=FAKE_KEY'), 
                  fit: BoxFit.cover,
                ),
              ),
              child: Center(
                // Animated pulse for volunteer location
                child: Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                    color: AppTheme.nekiGold.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Container(
                      width: 20,
                      height: 20,
                      decoration: BoxDecoration(
                        color: AppTheme.nekiGold,
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white, width: 3),
                        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.2), blurRadius: 4)],
                      ),
                    ),
                  ),
                ).animate(onPlay: (controller) => controller.repeat()).scale(begin: const Offset(0.8, 0.8), end: const Offset(1.5, 1.5)).fade(begin: 1.0, end: 0.0),
              ),
            ),
          ),
          
          // Header overlay
          Positioned(
            top: 60,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 20)],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Mission Tracking', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                      Text('Feed 200 Cows', style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(8)),
                    child: Text('LIVE', style: TextStyle(color: Colors.green.shade700, fontWeight: FontWeight.bold, fontSize: 12)),
                  ).animate(onPlay: (controller) => controller.repeat(reverse: true)).fade(begin: 1.0, end: 0.5),
                ],
              ),
            ).animate().slideY(begin: -0.2),
          ),

          // Uber style bottom sheet
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 30, offset: const Offset(0, -10))],
              ),
              child: SafeArea(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Container(
                        width: 40,
                        height: 5,
                        decoration: BoxDecoration(color: Colors.grey.shade300, borderRadius: BorderRadius.circular(10)),
                      ),
                    ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Volunteer En Route', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900)),
                        Text('3 min', style: TextStyle(color: AppTheme.forestGreen, fontSize: 22, fontWeight: FontWeight.w900)),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text('Arriving at NGO Center', style: TextStyle(color: Colors.grey.shade500, fontSize: 14)),
                    
                    const SizedBox(height: 24),
                    Container(height: 1, color: Colors.grey.shade200),
                    const SizedBox(height: 24),
                    
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 28,
                          backgroundColor: Colors.grey.shade200,
                          child: const Icon(Icons.person, color: Colors.grey, size: 30),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Rahul Sharma', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                              Row(
                                children: [
                                  Icon(Icons.star, color: AppTheme.nekiGold, size: 14),
                                  const SizedBox(width: 4),
                                  const Text('4.9', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                  const SizedBox(width: 8),
                                  Text('• 142 Missions', style: TextStyle(color: Colors.grey.shade500, fontSize: 13)),
                                ],
                              ),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(color: AppTheme.offWhite, shape: BoxShape.circle),
                          child: const Icon(Icons.phone, color: AppTheme.richBlack, size: 20),
                        ),
                        const SizedBox(width: 12),
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(color: AppTheme.offWhite, shape: BoxShape.circle),
                          child: const Icon(Icons.message, color: AppTheme.richBlack, size: 20),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ).animate().slideY(begin: 1.0, duration: 500.ms, curve: Curves.easeOutBack),
          ),
        ],
      ),
    );
  }
}
