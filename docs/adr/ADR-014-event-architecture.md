# ADR-014 — Event architecture: transactional outbox, in-process handlers, Redis fan-out

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-004, ADR-007, ADR-008; `02-tdd.md §7`; `05-data-model.md §4.10` |

## Context
Every state transition (mission, contribution, payment, shipment, assignment, proof, verification, impact) must produce an event consumed by notifications, tracking, search, impact, analytics, and admin queues. Requirements from the master prompt: producer, payload, consumers, retry, idempotency, ordering, dead-letter. No Kafka at MVP. Must never lose a `PaymentCaptured`.

## Decision

**2026-09-13 engineering amendment:** The [event/recovery protocol](../state-machines/events-and-recovery.md) and [14-test PostgreSQL probe](../rnd/postgres-outbox-spike.md) replace the earlier incomplete cursor/receipt/retry design. Evidence is synthetic PostgreSQL 17.11; target-version, real-handler, grants and external-effect gates remain mandatory.

- **Write:** append an immutable typed event and business/history change in one transaction. Lock the producer aggregate and assign a contiguous event sequence, separately from state version. Unique key includes aggregate type, ID and sequence.
- **Claim:** workers lock runnable aggregate dispatch cursors with `FOR UPDATE SKIP LOCKED`; fetch only the next sequence. Do not independently claim adjacent event rows. Bound each transaction's work for fairness and perform no external network request while holding the cursor.
- **Handle:** retain the cursor in an outer transaction. Handler effects, derived outbox rows, versioned receipts and cursor advance are atomic. Use a savepoint for handler work so a known failure can roll it back while retaining the cursor lock through retry recording. Connection failure rolls back the outer transaction; a stale-head watchdog covers repeated crashes.
- **Retry:** eight total attempts; waits before attempts 2–8 are 1 s, 5 s, 30 s, 300 s, 3600 s, 3600 s and 3600 s. Exhaustion blocks the stream at the original event. Later events cannot leapfrog; other streams continue.
- **Recover:** DLQ is metadata linked to the retained event. Scoped, reasoned ops replay preserves original identity, attempts and audit. No generic skip. Handler plan/version changes need an explicit migration/replay decision.
- **External effects:** persist a unique delivery intent in the handler transaction, then send outside it. Track uncertain outcomes and use provider-supported reconciliation; a local receipt is not a provider delivery acknowledgement. Redis hints are recoverable from authorized durable snapshots.
- **Schema:** minimal allowlisted payload, versioned type, immutable revision references, correlation/causation IDs and transition provenance. Read current state for authorization; read historical immutable facts for financial effects.

## Alternatives
- **Direct in-transaction calls between modules** — simplest; couples modules; any consumer failure rolls back money paths. Rejected for cross-module effects (notifications, search) but allowed for same-aggregate invariants.
- **Kafka/Redpanda** — durable log, consumer groups; ops burden and cost unjustified at MVP; explicitly excluded.
- **Redis Streams as primary bus** — durable-ish but Redis is not our source of truth; used later if consumer groups needed.
- **Postgres LISTEN/NOTIFY** — no durability; used only as an optional wake-up for the relay to cut polling latency.
- **Celery** — heavier than arq, sync-first.

## Pros
One committed local database effect per recorded handler identity when the transaction protocol is enforced; atomic with business writes; simple to test; DLQ visibility for ops; per-aggregate ordering.

## Cons
Polling latency (~250 ms) acceptable; single relay per partition set (scale by hashing aggregate_id to N workers later); at-least-once delivery requires idempotent consumers.

## Risks
External request acceptance can be uncertain. A derived request key helps only when that provider/operation supports it; otherwise use a recorded delivery state and reconciliation. Never assert universal external exactly-once delivery.

## Consequences
The reviewed event/recovery protocol governs ordering; TDD event catalogue and per-event schemas must be reconciled before each handler ships; adding an event requires a handler test and a catalogue entry. Business metrics computed from events.

## Migration path
Relay publishes to a broker instead of in-process handlers when a module is extracted; outbox table unchanged.
