import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/theme/app_theme.dart';
import '../../core/providers/mission_provider.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final missionsAsync = ref.watch(missionsProvider);
    return Scaffold(
      backgroundColor: AppTheme.offWhite,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Header
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Row(
                        children: [
                          Image.asset('assets/images/logo.png', height: 40),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text('Good Morning, Divyom', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppTheme.richBlack), overflow: TextOverflow.ellipsis),
                                const SizedBox(height: 4),
                                Row(
                                  children: [
                                    Icon(Icons.location_on, color: Colors.grey.shade600, size: 14),
                                    const SizedBox(width: 4),
                                    Text('South Delhi, NCR', style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontWeight: FontWeight.w500)),
                                    const Icon(Icons.keyboard_arrow_down, size: 14, color: Colors.grey),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    CircleAvatar(
                      backgroundColor: Colors.grey.shade200,
                      radius: 20,
                      child: const Icon(Icons.person, color: AppTheme.richBlack),
                    )
                  ],
                ),
              ).animate().fade().slideY(begin: -0.1),
            ),
            
            // Search Bar
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 20),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))],
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.search, color: Colors.grey, size: 20),
                      const SizedBox(width: 12),
                      Text("Search Missions...", style: TextStyle(color: Colors.grey.shade500, fontSize: 15, fontWeight: FontWeight.w500)),
                    ],
                  ),
                ),
              ).animate().fade(delay: 100.ms).slideY(begin: 0.1),
            ),

            // Live Stats Banner
            SliverToBoxAdapter(
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [AppTheme.richBlack, Color(0xFF2A2A2A)]),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildStatCol('1,274', 'Active'),
                    _buildStatCol('₹8.2L', 'Raised'),
                    _buildStatCol('6,500', 'Meals'),
                  ],
                ),
              ).animate().fade(delay: 200.ms).scale(begin: const Offset(0.95, 0.95)),
            ),

            // Floating Chips (Blinkit style)
            SliverToBoxAdapter(
              child: SizedBox(
                height: 80,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
                  children: [
                    _buildChip(Icons.local_fire_department, AppTheme.urgentRed, 'Urgent'),
                    _buildChip(Icons.water_drop, AppTheme.urgentRed, 'Blood Needed'),
                    _buildChip(Icons.location_on, AppTheme.nekiGold, 'Nearby'),
                    _buildChip(Icons.verified, AppTheme.forestGreen, 'Verified'),
                    _buildChip(Icons.business, Colors.blue, 'Corporate'),
                  ],
                ),
              ).animate().fade(delay: 300.ms),
            ),

            // Banners
            SliverToBoxAdapter(
              child: SizedBox(
                height: 160,
                child: ListView.separated(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  scrollDirection: Axis.horizontal,
                  itemCount: 2,
                  separatorBuilder: (context, index) => const SizedBox(width: 12),
                  itemBuilder: (context, index) {
                    final isWinter = index == 0;
                    return Container(
                      width: 300,
                      decoration: BoxDecoration(
                        color: isWinter ? AppTheme.nekiGold : AppTheme.urgentRed,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(isWinter ? 'Mega Winter' : 'Emergency', style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w900, height: 1.1)),
                          Text(isWinter ? 'Blanket Drive' : 'Blood Needed', style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w900, height: 1.1)),
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(
                              color: isWinter ? AppTheme.richBlack : Colors.white,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(isWinter ? 'Donate Now' : 'Act Fast', style: TextStyle(color: isWinter ? Colors.white : AppTheme.urgentRed, fontWeight: FontWeight.bold)),
                          )
                        ],
                      ),
                    );
                  },
                ),
              ),
            ),

            // Categories
            SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 4,
                  mainAxisSpacing: 16,
                  crossAxisSpacing: 16,
                  childAspectRatio: 0.8,
                ),
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final categories = [
                      {'name': 'Food', 'icon': 'assets/images/icon_food.png'},
                      {'name': 'Animals', 'icon': 'assets/images/icon_animals.png'},
                      {'name': 'Education', 'icon': 'assets/images/icon_education.png'},
                      {'name': 'Medical', 'icon': 'assets/images/icon_medical.png'},
                      {'name': 'Elderly', 'icon': 'assets/images/icon_elderly.png'},
                      {'name': 'Nature', 'icon': 'assets/images/icon_nature.png'},
                      {'name': 'Disaster', 'icon': 'assets/images/icon_disaster.png'},
                      {'name': 'Clothes', 'icon': 'assets/images/icon_clothes.png'},
                    ];
                    final cat = categories[index];
                    return Column(
                      children: [
                        Container(
                          height: 64,
                          width: 64,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 6, offset: const Offset(0, 3))],
                          ),
                          alignment: Alignment.center,
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(16),
                            child: Image.asset(cat['icon'] as String, fit: BoxFit.cover),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(cat['name'] as String, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey.shade800)),
                      ],
                    );
                  },
                  childCount: 8,
                ),
              ),
            ),

            // Urgent Needs Grid
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 10, 16, 16),
                child: Row(
                  children: [
                    const Icon(Icons.local_fire_department, color: AppTheme.urgentRed, size: 24),
                    const SizedBox(width: 8),
                    const Text('Urgent Near You', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: AppTheme.richBlack)),
                  ],
                ),
              ),
            ),
            
            SliverToBoxAdapter(
              child: SizedBox(
                height: 280, // Increased height for rich images
                child: missionsAsync.when(
                  loading: () => const Center(child: CircularProgressIndicator(color: AppTheme.nekiGold)),
                  error: (err, stack) => Center(child: Text('Error: $err')),
                  data: (missions) {
                    final urgentMissions = missions.where((m) => m.isUrgent).toList();
                    return ListView.separated(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      scrollDirection: Axis.horizontal,
                      itemCount: urgentMissions.length,
                      separatorBuilder: (context, index) => const SizedBox(width: 12),
                      itemBuilder: (context, index) {
                        final mission = urgentMissions[index];
                        final progress = mission.currentVolunteers / mission.requiredVolunteers;
                        return GestureDetector(
                          onTap: () => context.push('/mission/${mission.id}'),
                          child: Container(
                            width: 220,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(20),
                              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 10, offset: const Offset(0, 4))],
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Hero Image
                                Container(
                                  height: 120,
                                  width: double.infinity,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
                                    image: DecorationImage(
                                      image: AssetImage(mission.imageUrl),
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                  child: Align(
                                    alignment: Alignment.topLeft,
                                    child: Container(
                                      margin: const EdgeInsets.all(8),
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                      decoration: BoxDecoration(color: AppTheme.urgentRed, borderRadius: BorderRadius.circular(8)),
                                      child: const Text('URGENT', style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                                    ),
                                  ),
                                ),
                                Padding(
                                  padding: const EdgeInsets.all(12),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(mission.title, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14), maxLines: 2, overflow: TextOverflow.ellipsis),
                                      const SizedBox(height: 6),
                                      Row(
                                        children: [
                                          Icon(Icons.location_on, size: 12, color: Colors.grey.shade500),
                                          const SizedBox(width: 4),
                                          Text('${mission.distance} km away', style: TextStyle(color: Colors.grey.shade500, fontSize: 11)),
                                        ],
                                      ),
                                      const SizedBox(height: 12),
                                      // Progress Bar
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Row(
                                            children: [
                                              Icon(Icons.group, size: 12, color: AppTheme.richBlack),
                                              const SizedBox(width: 4),
                                              Text('${mission.currentVolunteers} Joined', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                            ],
                                          ),
                                          Text('${(progress * 100).toInt()}%', style: TextStyle(color: AppTheme.forestGreen, fontSize: 11, fontWeight: FontWeight.bold)),
                                        ],
                                      ),
                                      const SizedBox(height: 6),
                                      ClipRRect(
                                        borderRadius: BorderRadius.circular(4),
                                        child: LinearProgressIndicator(
                                          value: progress,
                                          minHeight: 6,
                                          backgroundColor: Colors.grey.shade200,
                                          valueColor: const AlwaysStoppedAnimation<Color>(AppTheme.forestGreen),
                                        ),
                                      )
                                    ],
                                  ),
                                )
                              ],
                            ),
                          ).animate().fade(delay: (400 + (index * 100)).ms).slideX(begin: 0.2),
                        );
                      },
                    );
                  },
                ),
              ),
            ),
            
            const SliverToBoxAdapter(child: SizedBox(height: 40)),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCol(String value, String label) {
    return Column(
      children: [
        Text(value, style: const TextStyle(color: AppTheme.nekiGold, fontSize: 20, fontWeight: FontWeight.w900)),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
      ],
    );
  }

  Widget _buildChip(IconData icon, Color iconColor, String label) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.grey.shade300),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: iconColor),
          const SizedBox(width: 6),
          Text(label, style: const TextStyle(fontWeight: FontWeight.w600, color: AppTheme.richBlack, fontSize: 13)),
        ],
      ),
    );
  }
}
