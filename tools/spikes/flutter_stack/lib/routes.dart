import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

part 'routes.g.dart';

@TypedGoRoute<ProbeRoute>(path: '/probe/:id')
class ProbeRoute extends GoRouteData {
  const ProbeRoute({required this.id});
  final String id;

  @override
  Widget build(BuildContext context, GoRouterState state) =>
      Scaffold(body: Center(child: Text('Synthetic probe: $id')));
}
