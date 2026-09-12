# Flutter stack compatibility spike

Executed 12–13 September 2026 under P0 §5.3. [Fixture](../../tools/spikes/flutter_stack/README.md) is isolated under `tools/spikes/flutter_stack`; it is not the application scaffold. No provider account, real user data, production database or live financial action was involved.

**Result:** dependency resolution, four generators, static analysis, 14 native/widget tests, Drift worker compilation and a Flutter JavaScript web build passed. This is a **partial compatibility result**, not approval of this package set for production. The older generator analyzer warns that it does not fully support the installed Dart language version. Browser database execution, mobile packaging, migration/encryption, and current-stack evaluation remain open.

## Tested versions

[SDK evidence](../../tools/spikes/flutter_stack/sdk-evidence.json) records Flutter **3.44.1**, framework revision `924134a44c189315be2148659913dda1671cbe99`, Dart **3.12.1**, stable channel. No global SDK upgrade was performed. The fixture bounds Dart to `>=3.12.1 <3.13.0`; reproduction should use this exact recorded SDK, not merely another SDK satisfying the range.

| Package | Exact direct constraint |
|---|---|
| flutter_riverpod / riverpod_annotation | 2.6.1 / 2.6.1 |
| riverpod_generator | 2.6.5 |
| freezed / freezed_annotation | 3.0.6 / 3.0.0 |
| drift / drift_dev | 2.26.1 / 2.26.1 |
| go_router / go_router_builder | 14.8.1 / 2.8.1 |
| build_runner | 2.4.15 |
| sqlite3, test-only direct dependency | 2.9.4 |

The committed [pubspec.lock](../../tools/spikes/flutter_stack/pubspec.lock) records resolved transitive versions and hosted archive hashes, including analyzer 7.6.0 and source_gen 2.0.0. Native database tests explicitly load Windows system `winsqlite3.dll`; the observed file version was 3.51.1. This does **not** test how SQLite is bundled on Android/iOS or establish a reproducible SQLite binary on every Windows installation.

## Dependency failures that changed the test candidate

1. Drift/drift_dev 2.35.0 with go_router_builder 2.8.1 failed dependency resolution: the former generator requires source_gen 3+, while the route generator requires a version below 3. No dependency override was used.
2. Replacing Drift with 2.26.1 exposed another incompatibility: riverpod_generator 2.6.5 requires riverpod_analyzer_utils 0.5.10, which requires Freezed 3 annotations. The initial Freezed 2.5.8 / annotation 2.4.4 pair could not resolve.
3. Freezed 3.0.6 / annotation 3.0.0 resolved together with the Riverpod 2 and Drift 2.26.1 candidate. Code generation succeeded but warned: analyzer language version **3.9.0**, SDK language version **3.12.0**. This warning remains a foundation-selection concern even though these fixtures compile.

Version metadata was inspected through the primary pub.dev package/version APIs for the named packages. Reproduction of the failures requires temporarily restoring those candidate constraints in an isolated copy, not changing the committed passing fixture. See [Riverpod generator 2.6.5](https://pub.dev/packages/riverpod_generator/versions/2.6.5), [Freezed 3.0.6](https://pub.dev/packages/freezed/versions/3.0.6), [Drift generator 2.26.1](https://pub.dev/packages/drift_dev/versions/2.26.1), and [route generator 2.8.1](https://pub.dev/packages/go_router_builder/versions/2.8.1).

Fixture integration fixes: import Riverpod's `Ref` explicitly, and hide Drift's `JsonKey` where Freezed's generated annotations share a library. These were compile-time fixture errors, not upstream package defects. Generated sources are committed and must be reproduced from their annotations/schema rather than hand edited.

Run `tools/generate_flutter_spike.py` from the repository root for committed generation: it runs build_runner, formats Dart, then removes trailing whitespace from generated files (Freezed disables the Dart formatter in its output). Four generated Dart files reproduced without drift before normalization; the checked-in workflow includes whitespace normalization as a deterministic final generation step.

## Executed checks

| Check | Result and actual scope |
|---|---|
| `flutter pub get` | Resolved 92 dependencies with the committed constraints; lockfile retained. |
| `dart run build_runner build --delete-conflicting-outputs` | Riverpod provider, Freezed union, Drift table/database and typed GoRouter route generation succeeded. Analyzer/SDK warning above remains. |
| `flutter analyze` | No issues found in the fixture after integration fixes. |
| `flutter test --reporter expanded` | 14 tests passed: six provider/route tests and eight local database tests. |
| `dart compile js web/worker.dart -o web/drift_worker.js` | Drift web worker compiled using the resolved dependencies. Generated JS is ignored and reproducible. |
| `flutter build web --target lib/web_main.dart` | JavaScript release output built; Flutter's Wasm dry run also succeeded. No actual `--wasm` release or browser runtime test claimed. |

Provider tests cover empty results, late old-query completion, account-key separation, disposal cancellation hook, source-error propagation and a typed-route deep-link widget start. They do not exercise a real Dio cancellation, authenticated router guard, paginated HTTP server or OS universal link.

Database tests create a real file-backed local SQLite database through Drift, close/reopen it, deduplicate repeated keys, reject changed payloads, refuse three representative financial actions, scope receipts to an account, retain a rejected reason, reject stale accepted versions and clear one account without deleting another. Receipt inputs are synthetic; no server signature, real synchronization worker, cross-process race, media bytes, TTL, encryption or schema migration is tested. The fixture's erasure method is not a production retention policy.

## Web and foundation follow-up

The [Drift web guide](https://drift.simonbinder.eu/platforms/web/) requires matching SQLite Wasm and worker artifacts and appropriate serving configuration. This turn compiled the worker and application but did **not** fetch/serve the matching `sqlite3.wasm`. The browser database probe will not succeed until that artifact is supplied. Test actual persistence, reload/reopen, private browsing/storage failure, account clearing, multi-tab behavior and access revocation; verify MIME type and chosen storage backend. A web build alone cannot prove those outcomes.

ADR-002's Riverpod 2 direction is unchanged. The evidence now requires an explicit foundation choice: evaluate a current mutually compatible generator stack, or validate an SDK/package baseline whose analyzer supports its SDK. Do not independently upgrade generators or add analyzer/source_gen overrides to force a solve. Any chosen upgrade must regenerate and rerun these tests plus browser/mobile probes, update the lockfile and record the ADR rationale.

Next gates remain: current-stack comparison, real browser Drift behavior, Android/iOS build and secure-storage packaging, offline media/migrations and synchronization against server contracts. Other P0 policy/design/schema/provider requirements remain independent. No P1 entry or production readiness is claimed.
