# ADR-007 — Redis for cache, rate limiting, pub/sub, and ephemeral location

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-008, ADR-014; `05-data-model.md §7` |

## Context
Needs: API rate limits (OTP abuse), hot-path caches (home modules, mission detail, geocode/directions), WebSocket fan-out across API replicas, latest volunteer position with short TTL, job queues for workers, idempotency fast path. Master prompt: evaluate Redis; no Kafka.

## Decision
Managed **Redis 7** (single primary + replica, Mumbai). Uses: token-bucket rate limits, JSON caches with event-driven invalidation, pub/sub channels `ws.*` and `events.*`, hash `shipment:{id}:loc` TTL 5 min, `arq` queues, `idem:{key}` 24 h. Redis is never the source of truth; every value is reconstructible from Postgres.

## Alternatives
- **Memcached** — no pub/sub, no data structures.
- **Postgres LISTEN/NOTIFY for fan-out** — works at small scale but ties WS servers to DB connections; payload limits; chosen as fallback if Redis unavailable.
- **NATS / Redis Streams as broker** — Streams considered for the outbox relay; deferred until event volume needs consumer groups.
- **Kafka** — explicitly excluded at MVP.

## Pros
One component covers five needs; low latency; ubiquitous client support; cheap managed tiers.

## Cons
Pub/sub is fire-and-forget (acceptable: clients resync via `version` and snapshots). Cache invalidation logic must be event-driven and tested.

## Risks
Treating Redis as durable → code review rule: no write to Redis without a Postgres source or TTL.

## Consequences
WS gateway subscribes per channel on demand; unsubscribes on last client. Cache keys namespaced per environment. Rate limit config in code with per-route overrides.

## Migration path
Streams or a broker replace pub/sub for the outbox relay when consumer groups or replay across services are needed (post-extraction).
