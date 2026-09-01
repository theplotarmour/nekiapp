import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/providers/mission_provider.dart';

class MissionsScreen extends ConsumerWidget {
  const MissionsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final missionsAsync = ref.watch(missionsProvider);
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Row(
          children: [
            // Blinkit style left sidebar
            Container(
              width: 80,
              decoration: BoxDecoration(
                color: Colors.grey.shade50,
                border: Border(right: BorderSide(color: Colors.grey.shade200)),
              ),
              child: ListView(
                children: [
                  _buildSideItem('🔥', 'Urgent', isSelected: true),
                  _buildSideItem('🍲', 'Food'),
                  _buildSideItem('⚕️', 'Medical'),
                  _buildSideItem('🐕', 'Animals'),
                ],
              ),
            ),
            // Right content
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Explore Missions', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900)),
                    const SizedBox(height: 16),
                    Expanded(
                      child: missionsAsync.when(
                        loading: () => const Center(child: CircularProgressIndicator()),
                        error: (err, stack) => Center(child: Text('Error: $err')),
                        data: (missions) {
                          return GridView.builder(
                            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                              crossAxisCount: 2,
                              childAspectRatio: 0.65,
                              crossAxisSpacing: 12,
                              mainAxisSpacing: 12,
                            ),
                            itemCount: missions.length,
                            itemBuilder: (context, index) {
                              final mission = missions[index];
                              return GestureDetector(
                                onTap: () => context.push('/mission/${mission.id}'),
                                child: Container(
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(16),
                                    border: Border.all(color: Colors.grey.shade200),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Container(
                                        height: 90,
                                        decoration: BoxDecoration(
                                          color: Colors.red.shade50,
                                          borderRadius: const BorderRadius.vertical(top: Radius.circular(15)),
                                        ),
                                        alignment: Alignment.center,
                                        child: Text(mission.category == 'Animals' ? '🐕' : '🍲', style: const TextStyle(fontSize: 32)),
                                      ),
                                      Padding(
                                        padding: const EdgeInsets.all(10),
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(mission.title, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13), maxLines: 2),
                                            const SizedBox(height: 4),
                                            Text('Needs ${mission.requiredVolunteers - mission.currentVolunteers} hands', style: TextStyle(color: Colors.grey.shade500, fontSize: 11)),
                                            const SizedBox(height: 12),
                                            Container(
                                              width: double.infinity,
                                              padding: const EdgeInsets.symmetric(vertical: 8),
                                              decoration: BoxDecoration(
                                                color: Colors.green.shade50,
                                                border: Border.all(color: Colors.green.shade600),
                                                borderRadius: BorderRadius.circular(8),
                                              ),
                                              alignment: Alignment.center,
                                              child: Text('ADD', style: TextStyle(color: Colors.green.shade700, fontWeight: FontWeight.w900, fontSize: 12)),
                                            )
                                          ],
                                        ),
                                      )
                                    ],
                                  ),
                                ),
                              );
                            },
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSideItem(String icon, String label, {bool isSelected = false}) {
    return Container(
      decoration: BoxDecoration(
        color: isSelected ? Colors.white : Colors.transparent,
        border: Border(left: BorderSide(color: isSelected ? Colors.green.shade600 : Colors.transparent, width: 4)),
      ),
      padding: const EdgeInsets.symmetric(vertical: 24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(icon, style: const TextStyle(fontSize: 24)),
          const SizedBox(height: 8),
          Text(label, style: TextStyle(fontSize: 10, fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600, color: isSelected ? Colors.black : Colors.grey.shade600)),
        ],
      ),
    );
  }
}
