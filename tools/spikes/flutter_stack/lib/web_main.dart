// Synthetic browser persistence probe, not a product UI.
import 'package:drift/wasm.dart';
import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'queue.dart';
import 'routes.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SemanticsBinding.instance.ensureSemantics();
  runApp(const ProviderScope(child: WebProbe()));
}

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
  late Future<String> result = probeDatabase();

  Future<String> probeDatabase({bool clear = false}) async {
    final opened = await WasmDatabase.open(
      databaseName: 'neki-synthetic-compatibility',
      sqlite3Uri: Uri.parse('sqlite3.wasm'),
      driftWorkerUri: Uri.parse('drift_worker.js'),
    );
    final db = ProbeDatabase(opened.resolvedExecutor);
    try {
      final restored = (await db.pending('synthetic-a')).length;
      if (clear) {
        await db.clearAccount('synthetic-a');
      } else {
        for (final account in ['synthetic-a', 'synthetic-b']) {
          await db.enqueue(
            account: account,
            key: 'web-key',
            action: 'check_in',
            payload: 'fixture',
            expectedVersion: 1,
          );
        }
      }
      final countA = (await db.pending('synthetic-a')).length;
      final countB = (await db.pending('synthetic-b')).length;
      return '${clear ? 'Cleared account A' : 'Database ready'}; restored A=$restored; pending A=$countA; pending B=$countB; storage=${opened.chosenImplementation}';
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
              child: Column(
                children: [
                  Text(
                    snapshot.hasError
                        ? 'Database probe failed: ${snapshot.error}'
                        : snapshot.data ?? 'Opening synthetic database',
                  ),
                  ElevatedButton(
                    onPressed: snapshot.connectionState != ConnectionState.done
                        ? null
                        : () => setState(() {
                            result = probeDatabase(clear: true);
                          }),
                    child: const Text('Clear fixture account A'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    ),
  );
}
