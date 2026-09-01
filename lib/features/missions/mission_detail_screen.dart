import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/theme/app_theme.dart';
import '../../core/providers/mission_provider.dart';

class MissionDetailScreen extends ConsumerWidget {
  final String id;
  const MissionDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final missionsAsync = ref.watch(missionsProvider);
    return Scaffold(
      backgroundColor: Colors.white,
      body: missionsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
        data: (missions) {
          final mission = missions.firstWhere((m) => m.id == id);
          final progress = mission.currentVolunteers / mission.requiredVolunteers;
          
          return CustomScrollView(
            slivers: [
              SliverAppBar(
                expandedHeight: 350,
                pinned: true,
                backgroundColor: Colors.white,
                leading: Container(
                  margin: const EdgeInsets.all(8),
                  decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4)]),
                  child: IconButton(icon: const Icon(Icons.arrow_back, color: AppTheme.richBlack), onPressed: () => context.pop()),
                ),
                actions: [
                  Container(
                    margin: const EdgeInsets.all(8),
                    decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4)]),
                    child: IconButton(icon: const Icon(Icons.share, color: AppTheme.richBlack), onPressed: () {}),
                  ),
                ],
                flexibleSpace: FlexibleSpaceBar(
                  background: Image.asset(
                    mission.imageUrl,
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(
                              mission.title,
                              style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: AppTheme.richBlack),
                            ),
                          ),
                          if (mission.isUrgent)
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(color: AppTheme.urgentRed, borderRadius: BorderRadius.circular(8)),
                              child: const Text('URGENT', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
                            )
                        ],
                      ).animate().fade().slideY(begin: 0.1),
                      
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Icon(Icons.location_on, size: 16, color: Colors.grey.shade500),
                          const SizedBox(width: 4),
                          Text('${mission.location} • ${mission.distance} km away', style: TextStyle(color: Colors.grey.shade500, fontWeight: FontWeight.w600)),
                        ],
                      ).animate().fade().slideY(begin: 0.1),
                      
                      const SizedBox(height: 24),
                      
                      // Fund / Volunteer Stats (Amazon Style)
                      Row(
                        children: [
                          Expanded(
                            child: Container(
                              padding: const EdgeInsets.all(16),
                              decoration: BoxDecoration(color: AppTheme.offWhite, borderRadius: BorderRadius.circular(16)),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('Volunteers', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.w600, fontSize: 12)),
                                  const SizedBox(height: 4),
                                  Text('${mission.currentVolunteers} / ${mission.requiredVolunteers}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
                                  const SizedBox(height: 8),
                                  LinearProgressIndicator(value: progress, backgroundColor: Colors.grey.shade300, color: AppTheme.forestGreen, minHeight: 6),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Container(
                              padding: const EdgeInsets.all(16),
                              decoration: BoxDecoration(color: AppTheme.offWhite, borderRadius: BorderRadius.circular(16)),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('Funds Raised', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.w600, fontSize: 12)),
                                  const SizedBox(height: 4),
                                  const Text('₹4,200', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
                                  const SizedBox(height: 8),
                                  LinearProgressIndicator(value: 0.76, backgroundColor: Colors.grey.shade300, color: AppTheme.nekiGold, minHeight: 6),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ).animate().fade(delay: 100.ms),

                      const SizedBox(height: 32),
                      
                      const Text('Mission Overview', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                      const SizedBox(height: 12),
                      Text(
                        mission.description,
                        style: TextStyle(color: Colors.grey.shade700, fontSize: 15, height: 1.6),
                      ).animate().fade(delay: 200.ms),

                      const SizedBox(height: 32),

                      // Fake Map Placeholder
                      Container(
                        height: 150,
                        width: double.infinity,
                        decoration: BoxDecoration(
                          color: Colors.grey.shade200,
                          borderRadius: BorderRadius.circular(16),
                          image: const DecorationImage(
                            image: NetworkImage('https://maps.googleapis.com/maps/api/staticmap?center=28.5355,77.3910&zoom=14&size=600x300&maptype=roadmap&markers=color:red%7C28.5355,77.3910&key=FAKE_KEY'), 
                            fit: BoxFit.cover,
                          )
                        ),
                        child: Center(
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(20)),
                            child: const Text('View on Map', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          )
                        ),
                      ).animate().fade(delay: 300.ms),

                      const SizedBox(height: 120), // padding for bottom sheet
                    ],
                  ),
                ),
              )
            ],
          );
        },
      ),
      bottomSheet: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 20, offset: const Offset(0, -5))],
        ),
        child: SafeArea(
          child: Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.offWhite,
                    foregroundColor: AppTheme.richBlack,
                    elevation: 0,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: Colors.grey.shade300)),
                  ),
                  child: const Text('Contribute Funds', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.forestGreen,
                    foregroundColor: Colors.white,
                    elevation: 0,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: const Text('Join Mission', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
