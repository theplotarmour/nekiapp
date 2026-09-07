# ADR-003 — Navigation: go_router with typed routes

| Status | Accepted |
|---|---|
| Deciders | Flutter lead |
| Related | ADR-001, `01-prd.md FR-13/FR-14` |

## Context
Five-tab shell with independent stacks; deep links `neki://mission/{id}`, universal links `https://neki.xyz/m/{id}`; push notification routing; auth redirect guards; full-screen success flow; iOS swipe-back and Android predictive back; web URLs for portals.

## Decision
Use **go_router** with `go_router_builder` typed routes, `StatefulShellRoute.indexedStack` for the bottom nav, `redirect` for auth/onboarding gating, and a central `DeepLinkResolver` mapping `neki://`, `https://neki.xyz/*`, and FCM payloads to typed routes.

## Alternatives
- **auto_route** — richer codegen and nested tabs, heavier generated code, slower builds, smaller maintainer base.
- **Navigator 1.0 imperative** — no URL/deep-link model; unsuitable for web portals.
- **Beamer** — smaller community.

## Pros
Flutter-team maintained; URL-first; typed params prevent stringly-typed bugs; shell routes preserve tab state; works identically on web.

## Cons
Custom transitions per route need `pageBuilder`; shared-element hero across shell branches requires care.

## Risks
Predictive back on Android 14+ requires `android:enableOnBackInvokedCallback` and Flutter ≥ 3.22 behavior; test on device.

## Consequences
Route table is the single source of screen inventory; analytics `screen_view` fires from a `GoRouter` observer. Share links use `public_id`, never uuid.

## Migration path
Route definitions are declarative; moving to another router is mechanical.
