import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../network/dio_client.dart';
import '../repositories/mission_repository.dart';
import '../models/mission.dart';

// Provides the global Dio Client
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

// Provides the Repository
final missionRepositoryProvider = Provider<MissionRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return MissionRepository(apiClient);
});

// Provides the async stream of missions to the UI
final missionsProvider = FutureProvider<List<Mission>>((ref) async {
  final repository = ref.watch(missionRepositoryProvider);
  return await repository.getMissions();
});
