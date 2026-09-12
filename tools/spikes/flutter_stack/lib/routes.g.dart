// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'routes.dart';

// **************************************************************************
// GoRouterGenerator
// **************************************************************************

List<RouteBase> get $appRoutes => [$probeRoute];

RouteBase get $probeRoute => GoRouteData.$route(
  path: '/probe/:id',

  factory: $ProbeRouteExtension._fromState,
);

extension $ProbeRouteExtension on ProbeRoute {
  static ProbeRoute _fromState(GoRouterState state) =>
      ProbeRoute(id: state.pathParameters['id']!);

  String get location =>
      GoRouteData.$location('/probe/${Uri.encodeComponent(id)}');

  void go(BuildContext context) => context.go(location);

  Future<T?> push<T>(BuildContext context) => context.push<T>(location);

  void pushReplacement(BuildContext context) =>
      context.pushReplacement(location);

  void replace(BuildContext context) => context.replace(location);
}
