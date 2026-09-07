# ADR-016 — Product analytics: PostHog behind an Analytics interface

| Status | Accepted |
|---|---|
| Deciders | Product, tech lead |
| Related | `01-prd.md §10`; `05-data-model.md §11` |

## Context
Need funnels (Home → Mission → Contribution → Payment → Tracking → Verified Impact), retention cohorts, feature flags/experiments, session replay is *not* wanted for privacy. Payload rules: no phone, exact amounts, coordinates, beneficiary data. Server-side critical events should be reconcilable against client events.

## Decision
**PostHog** (cloud EU/US or self-hosted later) via the Flutter SDK, wrapped in an `Analytics` interface with typed event definitions (`analytics/events.dart`) generated from a single YAML taxonomy shared with the backend. Server mirrors critical funnel events to `funnel_events` and to PostHog via server SDK for reconciliation. Pseudonymous `user_pseudo_id`; PII scrubbing in the interface layer; session replay disabled; autocapture disabled.

## Alternatives
- **Firebase Analytics / GA4** — free; weak funnels and export; sampling; event property limits.
- **Mixpanel/Amplitude** — strong funnels; cost grows with MTU; Amplitude's free tier viable — kept as fallback.
- **Self-built (events table + Metabase)** — full control; slower iteration for product; we keep `funnel_events` anyway.
- **Segment as router** — extra cost; premature.

## Pros
Funnels, cohorts, flags, and experiments in one tool; open source (self-host option for data residency); good Flutter SDK; typed taxonomy prevents drift.

## Cons
Another vendor; must guard payloads; cost scales with events (batching, sampling of impressions).

## Risks
PII leakage through free-text properties → allowlist of property keys enforced in `Analytics` wrapper and a CI lint on the taxonomy.

## Consequences
Every feature ticket lists events; `screen_view` from router observer; `mission_impression` sampled 1:1 at MVP, sampled later. Feature flags for kill switches come from PostHog *and* server `feature_flags` (server wins for payments/tracking).

## Migration path
Interface swap; historical export via PostHog API to warehouse.
