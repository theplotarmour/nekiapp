# ADR-001 — Flutter for mobile and web surfaces

| Status | Accepted (proposed 2026-09-07) |
|---|---|
| Deciders | Tech lead, Flutter lead, founder |
| Related | ADR-002, ADR-003, ADR-013; `02-tdd.md §3` |

## Context
NEKI needs iOS and Android consumer apps with premium motion and density, plus an organization portal and an ops console. Team is small (2 mobile engineers). The design system (`04-design-brief.md`) must be identical across surfaces. Prior repo history shows a Flutter scaffold with a Vercel web build, so Flutter familiarity exists.

## Decision
Use **Flutter 3.x (stable) / Dart 3** for the consumer app (iOS 15+, Android 8+) and for the org portal and ops console as Flutter Web, sharing a `neki_design_system` Dart package.

## Alternatives
- **React Native + separate React web** — two design-system implementations; motion/gesture fidelity requires native modules; Expo web is not production-grade for dense admin UIs.
- **Native Swift + Kotlin** — best platform fidelity; 2× cost; no web reuse; team size prohibits.
- **Kotlin Multiplatform + Compose Multiplatform** — iOS still maturing (2026); smaller talent pool in India than Flutter.
- **PWA only** — no reliable push on iOS, poor maps/camera, weak store presence.

## Pros
Single codebase; high-fidelity custom rendering (matches editorial design without platform widget fights); strong animation primitives; hot reload; mature ecosystem for maps, payments (razorpay_flutter), FCM; web reuse for portals.

## Cons
Flutter Web has larger initial payload and weaker SEO (acceptable: portals are authenticated, public mission pages served by a lightweight server-rendered page in NEXT). Platform-specific look needs deliberate work (predictive back, iOS sheets). Binary size ~15–20 MB baseline.

## Risks
- Flutter Web performance for ops console tables → mitigate with virtualization; fallback to a lightweight admin framework if velocity suffers (see `02-tdd.md §23`).
- Plugin quality for background location (not needed in MVP).

## Consequences
All UI teams work in Dart. Design tokens live in one package. CI needs macOS runner for iOS. Public share pages (`neki.xyz/m/{id}`) need a separate SSR/static solution for link previews (Open Graph) — small Cloudflare Worker.

## Migration path
If web portals outgrow Flutter Web: keep API contracts; rebuild portal in React/Next reusing tokens exported as JSON from `neki_design_system`. Consumer app decision is long-lived.
