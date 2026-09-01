import 'package:hive_flutter/hive_flutter.dart';

class HiveService {
  static const String _missionsBox = 'missionsBox';

  static Future<void> init() async {
    await Hive.initFlutter();
    await Hive.openBox(_missionsBox);
  }

  static Box get missionsBox => Hive.box(_missionsBox);

  // Save raw JSON to cache
  static Future<void> cacheMissions(List<dynamic> data) async {
    await missionsBox.put('cached_missions', data);
  }

  static List<dynamic>? getCachedMissions() {
    return missionsBox.get('cached_missions');
  }
}
