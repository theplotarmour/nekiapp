import 'package:dio/dio.dart';
import 'mock_interceptor.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(BaseOptions(
      baseUrl: 'https://api.neki.org/v1',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ));

    // In a real app, you'd have an AuthInterceptor here.
    // For now, we inject a MockInterceptor so the UI can function without a backend.
    _dio.interceptors.add(MockInterceptor());
  }

  Dio get dio => _dio;
}
