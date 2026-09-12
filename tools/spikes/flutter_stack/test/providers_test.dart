import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:neki_stack_spike/routes.dart';
import 'package:neki_stack_spike/search.dart';

class FakeSource implements SearchSource {
  final requests = <String, Completer<List<String>>>{};
  final cancelled = <String>[];
  @override
  Future<List<String>> find(String account, String query) =>
      (requests['$account/$query'] = Completer<List<String>>()).future;
  @override
  void cancel(String account, String query) => cancelled.add('$account/$query');
}

void main() {
  late FakeSource source;
  late ProviderContainer container;
  setUp(() {
    source = FakeSource();
    container = ProviderContainer(
      overrides: [searchSourceProvider.overrideWithValue(source)],
    );
  });
  tearDown(() => container.dispose());

  test('empty response is data rather than an initial-page crash', () async {
    final result = container.read(scopedSearchProvider('a', 'empty').future);
    source.requests['a/empty']!.complete([]);
    expect(await result, isEmpty);
  });
  test('late old-query response cannot overwrite the current query', () async {
    final old = container.read(scopedSearchProvider('a', 'old').future);
    final current = container.read(scopedSearchProvider('a', 'new').future);
    source.requests['a/new']!.complete(['new-result']);
    expect(await current, ['new-result']);
    source.requests['a/old']!.complete(['old-result']);
    await old;
    expect(container.read(scopedSearchProvider('a', 'new')).requireValue, [
      'new-result',
    ]);
  });
  test('same query is isolated between accounts', () async {
    final first = container.read(scopedSearchProvider('a', 'q').future);
    final second = container.read(scopedSearchProvider('b', 'q').future);
    source.requests['a/q']!.complete(['private-a']);
    source.requests['b/q']!.complete(['private-b']);
    expect(await first, ['private-a']);
    expect(await second, ['private-b']);
  });
  test('provider disposal invokes source cancellation', () async {
    final subscription = container.listen(
      scopedSearchProvider('a', 'q'),
      (_, _) {},
    );
    subscription.close();
    await container.pump();
    expect(source.cancelled, contains('a/q'));
  });
  test('source error propagates instead of inventing empty success', () async {
    final result = container.read(scopedSearchProvider('a', 'failure').future);
    final assertion = expectLater(result, throwsStateError);
    source.requests['a/failure']!.completeError(StateError('unavailable'));
    await assertion;
  });
  testWidgets('typed generated route builds after a deep-link start', (
    tester,
  ) async {
    final router = GoRouter(
      routes: $appRoutes,
      initialLocation: const ProbeRoute(id: 'synthetic').location,
    );
    addTearDown(router.dispose);
    await tester.pumpWidget(MaterialApp.router(routerConfig: router));
    await tester.pumpAndSettle();
    expect(find.text('Synthetic probe: synthetic'), findsOneWidget);
  });
}
