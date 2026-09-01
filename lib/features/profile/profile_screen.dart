import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.offWhite,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            const SliverAppBar(
              backgroundColor: AppTheme.offWhite,
              title: Text('Profile', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 24)),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  children: [
                    // Profile Header
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 40,
                          backgroundColor: AppTheme.nekiGold.withOpacity(0.2),
                          child: const Text('DS', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.nekiGold)),
                        ),
                        const SizedBox(width: 20),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Divyom Sharma', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900)),
                            const SizedBox(height: 4),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(6)),
                              child: Text('✓ Verified Volunteer', style: TextStyle(color: Colors.green.shade700, fontSize: 12, fontWeight: FontWeight.bold)),
                            )
                          ],
                        )
                      ],
                    ),
                    const SizedBox(height: 32),
                    
                    // Quick Stats
                    Row(
                      children: [
                        _buildQuickStat('Hours', '88'),
                        Container(width: 1, height: 40, color: Colors.grey.shade300),
                        _buildQuickStat('Missions', '12'),
                        Container(width: 1, height: 40, color: Colors.grey.shade300),
                        _buildQuickStat('Level', 'Gold'),
                      ],
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Menu
                    _buildMenuSection('Account', [
                      _buildMenuItem(Icons.account_balance_wallet, 'Neki Wallet', subtitle: '₹1,400 balance'),
                      _buildMenuItem(Icons.emoji_events, 'Certificates & Badges', badge: 'New'),
                      _buildMenuItem(Icons.favorite, 'Saved Missions'),
                      _buildMenuItem(Icons.history, 'Donation History'),
                    ]),
                    
                    _buildMenuSection('Preferences', [
                      _buildMenuItem(Icons.language, 'Language', subtitle: 'English'),
                      _buildMenuItem(Icons.dark_mode, 'Dark Mode', isToggle: true),
                      _buildMenuItem(Icons.notifications, 'Notifications'),
                    ]),
                    
                    _buildMenuSection('Support', [
                      _buildMenuItem(Icons.business, 'Switch to NGO Mode'),
                      _buildMenuItem(Icons.help, 'Help & Support'),
                      _buildMenuItem(Icons.logout, 'Log Out', isDestructive: true),
                    ]),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildQuickStat(String label, String value) {
    return Expanded(
      child: Column(
        children: [
          Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildMenuSection(String title, List<Widget> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: AppTheme.richBlack)),
        const SizedBox(height: 12),
        Container(
          margin: const EdgeInsets.only(bottom: 24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 10)],
          ),
          child: Column(children: items),
        ),
      ],
    );
  }

  Widget _buildMenuItem(IconData icon, String title, {bool isDestructive = false, String? subtitle, String? badge, bool isToggle = false}) {
    return Material(
      color: Colors.transparent,
      child: ListTile(
        leading: Icon(icon, color: isDestructive ? AppTheme.urgentRed : AppTheme.richBlack),
        title: Text(title, style: TextStyle(fontWeight: FontWeight.w600, color: isDestructive ? AppTheme.urgentRed : AppTheme.richBlack)),
        subtitle: subtitle != null ? Text(subtitle, style: TextStyle(color: Colors.grey.shade500, fontSize: 12)) : null,
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (badge != null)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(color: AppTheme.urgentRed, borderRadius: BorderRadius.circular(10)),
                child: Text(badge, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
              ),
            if (isToggle)
              Switch(value: false, onChanged: (v) {}, activeColor: AppTheme.nekiGold)
            else if (!isDestructive)
              const Icon(Icons.chevron_right, size: 20, color: Colors.grey),
          ],
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        onTap: () {},
      ),
    );
  }
}
