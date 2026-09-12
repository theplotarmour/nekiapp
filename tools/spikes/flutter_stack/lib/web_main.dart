// Compile target only until the matching wasm artifact and browser probe run.
import 'package:drift/wasm.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'queue.dart';
import 'routes.dart';

void main() => runApp(const ProviderScope(child: WebProbe()));

class WebProbe extends StatefulWidget {
  const WebProbe({super.key});

  @override
  State<WebProbe> createState() => _WebProbeState();
}

class _WebProbeState extends State<WebProbe> {
  late final router = GoRouter(
    routes: $appRoutes,
    initialLocation: '/probe/web',
  );
  late final Future<String> result = probeDatabase();

  Future<String> probeDatabase() async {
    final opened = await WasmDatabase.open(
      databaseName: 'neki-synthetic-compatibility',
      sqlite3Uri: Uri.parse('sqlite3.wasm'),
      driftWorkerUri: Uri.parse('drift_worker.js'),
    );
    final db = ProbeDatabase(opened.resolvedExecutor);
    try {
      await db.enqueue(
        account: 'synthetic',
        key: 'web-key',
        action: 'check_in',
        payload: 'fixture',
        expectedVersion: 1,
      );
      final count = (await db.pending('synthetic')).length;
      await db.clearAccount('synthetic');
      return 'Synthetic database round-trip: $count pending command';
    } finally {
      await db.close();
    }
  }

  @override
  void dispose() {
    router.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => MaterialApp.router(
    routerConfig: router,
    builder: (context, child) => Column(
      children: [
        Expanded(child: child ?? const SizedBox.shrink()),
        Material(
          child: FutureBuilder<String>(
            future: result,
            builder: (context, snapshot) => Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                snapshot.hasError
                    ? 'Database probe failed'
                    : snapshot.data ?? 'Opening synthetic database',
              ),
            ),
          ),
        ),
      ],
    ),
  );
}
