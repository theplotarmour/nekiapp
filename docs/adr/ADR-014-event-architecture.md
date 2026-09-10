# ADR-014 — Event architecture: transactional outbox, in-process handlers, Redis fan-out

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-004, ADR-007, ADR-008; `02-tdd.md §7`; `05-data-model.md §4.10` |

## Context
Every state transition (mission, contribution, payment, shipment, assignment, proof, verification, impact) must produce an event consumed by notifications, tracking, search, impact, analytics, and admin queues. Requirements from the master prompt: producer, payload, consumers, retry, idempotency, ordering, dead-letter. No Kafka at MVP. Must never lose a `PaymentCaptured`.

## Decision

**2026-09-10 P0 review finding (G13):** The [event/recovery proposal](../state-machines/events-and-recovery.md) addresses missing aggregate locking/cursors, atomic receipt effects, poison-event ordering, external-effect uncertainty and the incomplete retry schedule in this ADR. This note does not accept that amendment or prove current ordering/exactly-once claims. Resolve the proposal and run database fault cases before implementation readiness is claimed.
- **Write:** services append typed events to `domain_events` in the same DB transaction as the state change (outbox). No event emitted outside a transaction.
- **Relay:** `arq` worker polls `PENDING` with `FOR UPDATE SKIP LOCKED` (batch 100, 250 ms), processes events **sequentially per aggregate_id**, invokes registered in-process handlers, publishes to Redis `events.<type>` and `ws.*`, marks `PUBLISHED`.
- **Idempotent handlers:** `event_handler_receipts(event_id, handler)`; handlers check-and-record.
- **Retry:** 1 s, 5 s, 30 s, 5 min, 1 h; max 8 → `domain_events_dlq`; ops console lists and replays.
- **Schema:** `type` versioned (`PaymentCaptured.v1`), payload JSON with ids and minimal denormalized fields; consumers read current state from DB, never trust payload as latest truth.

## Alternatives
- **Direct in-transaction calls between modules** — simplest; couples modules; any consumer failure rolls back money paths. Rejected for cross-module effects (notifications, search) but allowed for same-aggregate invariants.
- **Kafka/Redpanda** — durable log, consumer groups; ops burden and cost unjustified at MVP; explicitly excluded.
- **Redis Streams as primary bus** — durable-ish but Redis is not our source of truth; used later if consumer groups needed.
- **Postgres LISTEN/NOTIFY** — no durability; used only as an optional wake-up for the relay to cut polling latency.
- **Celery** — heavier than arq, sync-first.

## Pros
Exactly-once *effects* via idempotent handlers; atomic with business writes; simple to test; DLQ visibility for ops; per-aggregate ordering.

## Cons
Polling latency (~250 ms) acceptable; single relay per partition set (scale by hashing aggregate_id to N workers later); at-least-once delivery requires idempotent consumers.

## Risks
Handler that performs external side effects (FCM, Razorpay refund) retried → external calls carry idempotency keys derived from event id.

## Consequences
Event catalogue in `02-tdd.md §7.2` is the contract; adding an event requires a handler test and a catalogue entry. Business metrics computed from events.

## Migration path
Relay publishes to a broker instead of in-process handlers when a module is extracted; outbox table unchanged.
