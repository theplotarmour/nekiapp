# ADR-002 — State management: Riverpod 3 with code generation

| Status | Accepted |
|---|---|
| Deciders | Flutter lead, tech lead |
| Related | ADR-001, ADR-013; `02-tdd.md §3.3` |

## Context
Requirements: predictable state, minimal rebuilds, unit-testable without widgets, lifecycle awareness (dispose streams), realtime stream merging (WebSocket + REST snapshot), offline queue integration, safe optimistic updates for bookmarks only. Master prompt asks to evaluate Riverpod vs BLoC/Cubit and document reasoning.

## Decision

**2026-09-13 implementation baseline amendment:** retain the accepted Riverpod/codegen architecture and use the [validated current stack](../rnd/flutter-current-stack-spike.md): Flutter 3.47.4, Dart 3.13.3, flutter_riverpod 3.4.3 and the exact fixture lockfile as the starting compatibility reference. Analysis, 14 local tests and Chrome IndexedDB reload/account-clear checks pass. Add production packages only after their compatibility tests; Android/iOS/provider and migration tests remain required. Controller retry behavior must be explicit and tested; never automatically replay financial commands. This engineering amendment does not approve any domain/financial policy.
Use **Riverpod 3.x with `riverpod_generator`** (`@riverpod` notifiers, `AsyncNotifier` for async screens), `Freezed` for immutable state/unions. One controller per screen/feature; repositories injected via providers; `ProviderScope` overrides for tests.

## Alternatives
- **BLoC/Cubit** — explicit event/state and separate dependency-injection choices. References D/E/F demonstrate Cubit/BLoC patterns, but no equivalent-screen benchmark establishes a numerical code-volume penalty. The previous 1.6× claim was unsupported and is withdrawn. The [pinned source review](../rnd/open-source-review.md) also identifies B as a same-domain comparison across state libraries. This evidence correction preserves the accepted Riverpod direction; NEKI-specific compatibility and lifecycle tests remain required.
- **Provider** — predecessor; no compile-time safety, ProviderNotFound at runtime.
- **GetX** — global mutable state, poor testability; violates anti-patterns list.
- **MobX / signals** — smaller community in Flutter; less lifecycle support.

## Pros
Compile-time safe provider graph; auto-dispose; `ref.watch` fine-grained rebuilds; `AsyncValue` maps to loading/error/data; trivially testable (`ProviderContainer`); `family` providers for per-mission controllers; `StreamProvider` for WS channels; DI and state in one system.

## Cons
Code-gen build step; learning curve on `ref` semantics; provider graphs can sprawl without conventions.

## Risks
Over-use of global providers → enforce feature-scoped `providers.dart`, lint rule banning cross-feature provider imports except via domain interfaces.

## Consequences
Widgets never call repositories directly. Screen state = sealed Freezed class with `loading | error | data(empty flag)`. Realtime: `TrackingController` merges `StreamProvider` events with snapshot using `version`. Test target: every controller has unit tests with fake repositories.

## Migration path
Riverpod → BLoC is a controller-layer rewrite only; domain/data layers untouched. Not anticipated.
