// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'routes.dart';

// **************************************************************************
// GoRouterGenerator
// **************************************************************************

List<RouteBase> get $appRoutes => [$probeRoute];

RouteBase get $probeRoute => GoRouteData.$route(
  path: '/probe/:id',
  hasOverriddenOnExit: false,
  factory: $ProbeRoute._fromState,
);

mixin $ProbeRoute on GoRouteData {
  static ProbeRoute _fromState(GoRouterState state) =>
      ProbeRoute(id: state.pathParameters['id']!);

  ProbeRoute get _self => this as ProbeRoute;

  @override
  String get location =>
      GoRouteData.$location('/probe/${Uri.encodeComponent(_self.id)}');

  @override
  void go(BuildContext context) => context.go(location);

  @override
  Future<T?> push<T>(BuildContext context) => context.push<T>(location);

  @override
  void pushReplacement(BuildContext context) =>
      context.pushReplacement(location);

  @override
  void replace(BuildContext context) => context.replace(location);
}
