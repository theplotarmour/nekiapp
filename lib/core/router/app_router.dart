import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/navigation/main_nav.dart';
import '../../features/home/home_screen.dart';
import '../../features/missions/missions_screen.dart';
import '../../features/missions/mission_detail_screen.dart';
import '../../features/track/track_screen.dart';
import '../../features/impact/impact_screen.dart';
import '../../features/profile/profile_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) {
          return MainNavigation(navigationShell: navigationShell);
        },
        branches: [
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/',
                builder: (context, state) => const HomeScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/missions',
                builder: (context, state) => const MissionsScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/track',
                builder: (context, state) => const TrackScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/impact',
                builder: (context, state) => const ImpactScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/profile',
                builder: (context, state) => const ProfileScreen(),
              ),
            ],
          ),
        ],
      ),
      GoRoute(
        path: '/mission/:id',
        builder: (context, state) {
          final id = state.pathParameters['id']!;
          return MissionDetailScreen(id: id);
        },
      ),
    ],
  );
});
