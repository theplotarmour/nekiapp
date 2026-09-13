# Current Flutter stack: generation, native tests and browser persistence

Executed 2026-09-13. This closes the older fixture's analyzer-language mismatch and adds bounded browser storage evidence. It does not close the full provider/platform gate or implement NEKI. [Reproduce](../../tools/spikes/flutter_stack/README.md); [exact SDK evidence](../../tools/spikes/flutter_stack/sdk-evidence.json); [resolved dependencies](../../tools/spikes/flutter_stack/pubspec.lock).

## Resolved baseline

| Dependency | Current fixture |
|---|---|
| Flutter / Dart | 3.47.4 / 3.13.3 |
| flutter_riverpod | 3.4.3 |
| riverpod_annotation / generator | 4.0.7 / 4.0.9 |
| Freezed annotation / generator | 3.1.0 / 4.0.1 |
| Drift / drift_dev | 2.35.0 / 2.35.0 |
| go_router / builder | 18.0.1 / 4.5.0 |
| build_runner / analyzer | 2.16.1 / 14.4.0; no language warning |
| sqlite3 | 3.5.2 native assets; no system DLL override |

See the [immutable historical report](flutter-stack-spike.md) for the older set. No dependency overrides were used. Freezed 4's Dart minimum required the isolated SDK update. Stable direct packages resolve a transitive `riverpod_analyzer_utils 1.0.0-dev.12`; review that dependency when selecting the production lockfile.

The Windows SDK archive came from the [official release manifest](https://storage.googleapis.com/flutter_infra_release/releases/releases_windows.json). SHA-256 was verified before extraction: `31173300481bd06e377fd55ee84214689648b1817563efd7b450b7b78bdf351a`. The installed global SDK was unchanged. The web SQLite asset is from [Drift 2.35.0](https://github.com/simolus3/drift/releases/tag/drift-2.35.0), checked against digest `13d3f11d05b39ba0618a7115fb41640a5d48b6300f5d3f325f554b42bd6688a4`. The worker was compiled locally from the pinned graph.

## Compatibility changes and results

- Code generation completed with 21 outputs; removed the obsolete ignored build_runner flag. Typed route classes apply the generated mixin. Riverpod's common `Ref` comes from its annotation package.
- Search explicitly opts out of automatic retry; its error test also checks one source invocation. This is fixture behavior, not a blanket production retry policy.
- `flutter analyze`: no issues. `flutter test --reporter expanded`: **14 tests passed**, covering stale search completion, empty/error results, cancellation, account separation, typed navigation, queue restart, key/hash conflicts, financial-command denial and receipt/version rules.
- Worker JavaScript compilation and web build passed, including the Wasm dry run. This was a JavaScript release build, not browser execution of a `--wasm` app build.

## Browser story and observed evidence

Story: page opens the synthetic local database, enqueues account-owned rows, closes it, reopens on navigation, and clears one account through the UI. There is no backend/API boundary in this fixture.

Agent-browser 0.37.1 used a dedicated Windows Chrome session (`HeadlessChrome/153.0.0.0`), served at loopback with Python HTTP server and no COOP/COEP headers. Selected implementation: `WasmStorageImplementation.sharedIndexedDb`.

| Action | Actual visible result |
|---|---|
| First fresh-context load | `Database ready; restored A=0; pending A=1; pending B=1` |
| Reload same origin/context | `Database ready; restored A=1; pending A=1; pending B=1` |
| Click Clear fixture account A | `Cleared account A; restored A=1; pending A=0; pending B=1` |
| Reload after clearing | `Database ready; restored A=0; pending A=1; pending B=1` |

The final load deliberately creates a new A row after reading its restored count; the zero count proves the previous delete persisted. Typed navigation rendered `Synthetic probe: web`. Initial screenshot was visually inspected; accessibility snapshots confirmed database status and the button. Browser page-error collection was empty and the registered error/unhandled-rejection buffer returned `[]`. Server logs showed 200/304 responses for application, worker and Wasm assets, plus an incidental missing favicon 404. Browser and local server were stopped after verification.

## Remaining boundaries

This proves the exercised package combination and same-context IndexedDB reload/clear behavior. It does not prove OPFS, multiple tabs racing writes, private mode/quota eviction, browser-process restart, other browsers, mobile packaging, migration upgrades, secure credentials, location, Razorpay, FCM or server acceptance of queued actions. Local account keys are not authorization.

ADR-002 and TDD were amended on 2026-09-13 to select this Riverpod 3 compatibility baseline while retaining the accepted architecture. Further mobile/provider packages and production migrations remain unverified and must pass their own gates. The historical report stays pinned to its original Riverpod 2 commit.
