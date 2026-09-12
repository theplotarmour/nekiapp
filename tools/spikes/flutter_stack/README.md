# Isolated Flutter compatibility fixture

P0 research code, not a production application. [Results and limitations](../../../docs/rnd/flutter-stack-spike.md). Run with the exact Flutter/Dart revisions in `sdk-evidence.json`.

From this directory:

```powershell
flutter pub get --enforce-lockfile
../../../.venv-contracts/Scripts/python ../../generate_flutter_spike.py
flutter analyze
flutter test --reporter expanded
dart compile js web/worker.dart -o web/drift_worker.js
flutter build web --target lib/web_main.dart
```

The queue uses only synthetic field commands; money/refund/payout actions cannot be queued. Native Windows tests deliberately use the operating-system SQLite library. Production native packaging, migrations, retention and server authorization are separate work. The search source is a test override, not a network client.

The web target is a compile probe until a matching `sqlite3.wasm` is provided and served. It shows a database failure if that dependency is missing; a successful web build is not browser database proof. Do not publish this fixture. No production credentials or real data belong here.

Generated `.g.dart` and `.freezed.dart` files are committed for review. After codegen, inspect their diff. Generated web/build assets remain ignored. The analyzer's older-language warning is documented and unresolved; passing fixture tests do not endorse this legacy stack as the production baseline.
