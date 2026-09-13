# Isolated Flutter compatibility fixture

P0 research code, not a production application. [Current results](../../../docs/rnd/flutter-current-stack-spike.md) and [historical Riverpod 2 baseline](../../../docs/rnd/flutter-stack-spike.md). Use Flutter 3.47.4 / Dart 3.13.3 at the exact revisions in `sdk-evidence.json`. Keep an isolated SDK; no global upgrade is required.

From the repository root, set the actual SDK location:

```powershell
$spikeSdk = 'D:/Code/neki-research/sdk-3.47.4/flutter/bin'
Push-Location tools/spikes/flutter_stack
& "$spikeSdk/flutter.bat" pub get --enforce-lockfile
Pop-Location
.venv-contracts/Scripts/python tools/generate_flutter_spike.py --dart "$spikeSdk/dart.bat"
.venv-contracts/Scripts/python tools/setup_flutter_web_assets.py
Push-Location tools/spikes/flutter_stack
& "$spikeSdk/flutter.bat" analyze
& "$spikeSdk/flutter.bat" test --reporter expanded
& "$spikeSdk/dart.bat" compile js web/worker.dart -o web/drift_worker.js
& "$spikeSdk/flutter.bat" build web --target lib/web_main.dart
Pop-Location
.venv-contracts/Scripts/python -m http.server 8768 --bind 127.0.0.1 --directory tools/spikes/flutter_stack/build/web
```

Open `http://127.0.0.1:8768` in a fresh browser context. First load displays restored A=0, pending A=1 and B=1. Reload must display restored A=1. Clear fixture account A must display A=0 and B=1; reload then displays restored A=0 before creating its synthetic row again. The selected storage implementation is displayed. This local SQLite test does not call a NEKI API or prove server authorization.

The queue allows only synthetic field commands; money/refund/payout actions are denied. Windows native tests use the sqlite3 package's native asset, without the historical system DLL override. Search is an injected test source, not an HTTP client. Automatic retry is disabled for that source so a failed request is observable and is not silently issued again.

The Wasm setup helper checks the exact release artifact digest before writing it. Compile the worker with the resolved dependencies. Worker, Wasm and web build outputs remain ignored; regenerate after dependency changes. Generated Dart sources are committed and normalized by the generation helper.

Do not publish this fixture or use real data/credentials. Android/iOS execution, web multi-tab/private mode, OPFS, cache migrations and production adapters remain separate gates.
