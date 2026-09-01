import '../models/mission.dart';
import '../network/dio_client.dart';
import '../storage/hive_service.dart';

class MissionRepository {
  final ApiClient _apiClient;

  MissionRepository(this._apiClient);

  Future<List<Mission>> getMissions() async {
    try {
      // 1. Try to fetch fresh data from API
      final response = await _apiClient.dio.get('/missions');
      final data = response.data['data'] as List<dynamic>;
      
      // 2. Cache it instantly in Hive for next time
      await HiveService.cacheMissions(data);

      return data.map((json) => Mission.fromJson(json)).toList();
    } catch (e) {
      // 3. If offline, fallback to Hive cache
      final cachedData = HiveService.getCachedMissions();
      if (cachedData != null) {
        return cachedData.map((json) => Mission.fromJson(json)).toList();
      }
      throw Exception('Failed to load missions and no offline cache available.');
    }
  }
}
