# Architecture Decision Records

Format per ADR: Context · Decision · Alternatives · Pros · Cons · Risks · Consequences · Migration path. Status values: Proposed, Accepted, Superseded.

| ADR | Title | Status |
|---|---|---|
| [001](ADR-001-flutter.md) | Flutter for mobile and web surfaces | Accepted |
| [002](ADR-002-state-management.md) | Riverpod 2 with code generation | Accepted |
| [003](ADR-003-navigation.md) | go_router with typed routes | Accepted |
| [004](ADR-004-modular-monolith.md) | FastAPI modular monolith with transactional outbox | Accepted |
| [005](ADR-005-postgresql.md) | PostgreSQL 16 | Accepted |
| [006](ADR-006-postgis.md) | PostGIS geography with GiST | Accepted |
| [007](ADR-007-redis.md) | Redis for cache, rate limiting, pub/sub, ephemeral location | Accepted |
| [008](ADR-008-websockets.md) | WebSockets with versioned events and polling fallback | Accepted |
| [009](ADR-009-object-storage.md) | Cloudflare R2 with presigned uploads and CDN | Accepted |
| [010](ADR-010-payment-provider.md) | Razorpay; manual payouts (D3); Route → NEXT | Accepted (legal sign-off before live funds) |
| [011](ADR-011-maps-provider.md) | Google Maps Platform via backend proxy | Accepted |
| [012](ADR-012-authentication.md) | Phone OTP (MSG91) + server JWT + RBAC | Accepted |
| [013](ADR-013-offline-persistence.md) | Drift (SQLite) with outbox queue | Accepted |
| [014](ADR-014-event-architecture.md) | Transactional outbox, in-process handlers, Redis fan-out | Accepted |
| [015](ADR-015-search-architecture.md) | Postgres FTS + pg_trgm + PostGIS ranking | Accepted |
| [016](ADR-016-analytics.md) | PostHog behind an Analytics interface | Accepted |
| [017](ADR-017-observability.md) | Sentry + OpenTelemetry to Grafana Cloud | Accepted |
| [018](ADR-018-deployment.md) | Containers on Fly.io/ECS, Terraform, GitHub Actions | Accepted (platform spike) |

Adding an ADR: copy the template headings, number sequentially, link from this table and from `docs/02-tdd.md §22`.
