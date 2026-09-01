import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/theme/app_theme.dart';

class ImpactScreen extends StatelessWidget {
  const ImpactScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.offWhite,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            const SliverAppBar(
              floating: true,
              backgroundColor: AppTheme.offWhite,
              title: Text('Your Impact', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: AppTheme.richBlack)),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const SizedBox(height: 24),

                    // Gamified Streak Banner
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(colors: [AppTheme.nekiGold, Color(0xFFF1C40F)]),
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [BoxShadow(color: AppTheme.nekiGold.withOpacity(0.3), blurRadius: 15, offset: const Offset(0, 5))],
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(color: Colors.white.withOpacity(0.2), shape: BoxShape.circle),
                            child: const Icon(Icons.local_fire_department, color: Colors.orange, size: 24),
                          ),
                          const SizedBox(width: 16),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('12 Week Streak!', style: TextStyle(color: AppTheme.richBlack, fontWeight: FontWeight.w900, fontSize: 18)),
                              Text('You are in the top 5% of volunteers.', style: TextStyle(color: AppTheme.richBlack.withOpacity(0.8), fontWeight: FontWeight.w500, fontSize: 13)),
                            ],
                          )
                        ],
                      ),
                    ).animate().fade().slideY(begin: 0.1),

                    const SizedBox(height: 32),

                    // Dashboard Stats Grid
                    GridView.count(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      crossAxisCount: 2,
                      mainAxisSpacing: 16,
                      crossAxisSpacing: 16,
                      childAspectRatio: 1.5,
                      children: [
                        _buildStatCard('Meals Served', '482', Icons.soup_kitchen, Colors.orange),
                        _buildStatCard('Animals Fed', '76', Icons.pets, Colors.brown),
                        _buildStatCard('Hours', '88', Icons.access_time, AppTheme.forestGreen),
                        _buildStatCard('Impact Rank', '#42', Icons.emoji_events, AppTheme.nekiGold),
                      ],
                    ).animate().fade(delay: 100.ms).scale(begin: const Offset(0.95, 0.95)),
                    
                    const SizedBox(height: 32),
                    
                    // Recent Badges
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Recent Badges', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
                        Text('View All', style: TextStyle(color: AppTheme.nekiGold, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildBadge(Image.asset('assets/images/badge_blood.png', height: 40), 'Blood Donor'),
                        _buildBadge(Image.asset('assets/images/badge_tree.png', height: 40), 'Tree Planter'),
                        _buildBadge(Image.asset('assets/images/badge_top100.png', height: 40), 'Top 100'),
                        _buildBadge(const Icon(Icons.school, color: AppTheme.nekiGold, size: 28), 'Mentor'),
                      ],
                    ).animate().fade(delay: 200.ms),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 24),
          const Spacer(),
          Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900)),
          Text(title, style: TextStyle(color: Colors.grey.shade600, fontSize: 12, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }

  Widget _buildBadge(Widget iconWidget, String title) {
    return Column(
      children: [
        Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.circle,
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 4, offset: const Offset(0, 2))],
          ),
          alignment: Alignment.center,
          child: ClipOval(
            child: iconWidget,
          ),
        ),
        const SizedBox(height: 8),
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
      ],
    );
  }
}
