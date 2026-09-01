import 'package:dio/dio.dart';

class MockInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (options.path.contains('/missions')) {
      final mockResponse = Response(
        requestOptions: options,
        statusCode: 200,
        data: {
          'data': [
            {
              'id': '1',
              'title': 'Community Kitchen For Daily Wagers',
              'description': 'Help serve warm, nutritious meals to 500 daily wage workers. We need volunteers to help cook, pack, and distribute.',
              'category': 'Food',
              'location': 'South Delhi',
              'distance': 1.2,
              'requiredVolunteers': 40,
              'currentVolunteers': 38,
              'isUrgent': true,
              'imageUrl': 'assets/images/neki_hero_food_1780739844525.png',
            },
            {
              'id': '2',
              'title': 'Emergency Blanket Distribution',
              'description': 'The cold wave is hitting hard. Join us tonight to distribute 1000 blankets across homeless shelters in the city.',
              'category': 'Relief',
              'location': 'Connaught Place',
              'distance': 3.5,
              'requiredVolunteers': 100,
              'currentVolunteers': 45,
              'isUrgent': true,
              'imageUrl': 'assets/images/neki_banner_blanket_1780739942349.png',
            },
            {
              'id': '3',
              'title': 'Feed Stray Animals',
              'description': 'Local strays need food. We will be covering 4 zones to feed stray dogs and cows.',
              'category': 'Animals',
              'location': 'Gurugram Sector 14',
              'distance': 5.0,
              'requiredVolunteers': 20,
              'currentVolunteers': 8,
              'isUrgent': false,
              'imageUrl': 'assets/images/neki_hero_animals_1780739861306.png',
            },
            {
              'id': '4',
              'title': 'Weekend Slum Library Mentoring',
              'description': 'Spend 2 hours teaching basic reading and math to underprivileged children.',
              'category': 'Education',
              'location': 'Noida Sector 62',
              'distance': 8.1,
              'requiredVolunteers': 15,
              'currentVolunteers': 14,
              'isUrgent': false,
              'imageUrl': 'assets/images/neki_hero_education_1780739877042.png',
            },
            {
              'id': '5',
              'title': 'Rural Medical Checkup Camp',
              'description': 'Calling doctors, nurses, and volunteers for a general checkup camp outside the city.',
              'category': 'Medical',
              'location': 'Haryana Border',
              'distance': 25.0,
              'requiredVolunteers': 50,
              'currentVolunteers': 30,
              'isUrgent': true,
              'imageUrl': 'assets/images/neki_hero_medical_1780739903405.png',
            },
            {
              'id': '6',
              'title': 'Winter Clothes Sorting',
              'description': 'Help sort and pack donated winter clothes for distribution to orphanages.',
              'category': 'Clothes',
              'location': 'Saket',
              'distance': 2.3,
              'requiredVolunteers': 25,
              'currentVolunteers': 10,
              'isUrgent': false,
              'imageUrl': 'assets/images/neki_hero_clothes_1780739919291.png',
            }
          ]
        }
      );
      return handler.resolve(mockResponse);
    }
    return handler.next(options);
  }
}
