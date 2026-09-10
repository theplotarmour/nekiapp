# Durable events, consumers and recovery

**Status:** Proposed ADR-014/TDD §7 amendment for G13, NK-DOC-3.03. No runtime proof yet. Technical choices below are reviewable designs; infrastructure compatibility and real Postgres crash/concurrency tests remain gate evidence. [Shared transition rules](README.md) define producer authorization/audit.

## Evidence and design boundary

[PostgreSQL SELECT documentation](https://www.postgresql.org/docs/16/sql-select.html) explains that SKIP LOCKED skips conflicting row locks and is useful for queue-like consumers. That alone does not order events for an aggregate: workers could lock adjacent event rows separately. [PostgreSQL locking documentation](https://www.postgresql.org/docs/16/explicit-locking.html) describes row locks and deadlock handling; the design below uses a dedicated dispatch cursor and retries aborted transactions. This is a NEKI proposal, not a guarantee supplied automatically by arq or Redis.

## Event envelope and schemas

| Field | Required contract |
|---|---|
| event_id | UUID unique; never regenerated for retry/replay. |
| type | Exact versioned name, e.g. `ShipmentDelivered.v1`; unknown versions fail into visible blocked processing. |
| aggregate_type / aggregate_id | Server-produced identity; aggregate namespace included so equal UUIDs of different types do not collide. |
| aggregate_sequence | Positive contiguous event sequence assigned under producer aggregate lock, independent of server timestamp and worker delivery time. |
| aggregate_version | Committed state revision; distinguish from event sequence if a command emits multiple events. |
| occurred_at | UTC server commit-associated timestamp; captured/client time, when needed, is separate evidence. |
| correlation_id / causation_id | Request/job trace and causing command/event; no sensitive values. |
| transition_id | Durable history entry providing restricted evidence provenance. |
| payload | Reviewed allowlist per event type: stable object/revision IDs and necessary committed facts. No generic serialized model row. |
| schema_version | Versioned typed schema; changes that alter consumer meaning require a new compatible event type/version. |

Unique `(aggregate_type, aggregate_id, aggregate_sequence)` and event ID. Schema validates before producer commit; outbox insert and business transition are one transaction. Financial facts are not recomputed from mutable status. Events carry enough immutable source/revision references to reconstruct their specific transition even when the aggregate has advanced.

## Processing protocol

1. Producer locks its aggregate, validates the command, advances state/version and event sequence, and appends history/audit/outbox atomically. Creating the aggregate also creates its independent dispatch cursor. Producer sequencing does not lock the dispatch cursor, avoiding a producer/worker root-lock inversion.
2. Workers select runnable **dispatch cursor rows**, not arbitrary event rows, with SKIP LOCKED. Cursor key is aggregate namespace/ID; it stores last fully handled sequence, next-attempt time and blocked reason. A worker holds this cursor's transaction lock while applying a bounded event batch. No external network request occurs while this lock is held.
3. Fetch exactly `last_handled_sequence + 1`. If not yet committed, leave the cursor unchanged. A proven missing sequence while later events exist is an integrity fault, not permission to skip. Maintain fair bounded batches so a busy stream does not starve other aggregates.
4. Process that event's reviewed required handler set. Each database handler commits its business effect, derived outbox events and unique `(event_id, handler_name, handler_version)` receipt in the same transaction as cursor advance. A transaction crash rolls back all those changes; commit-response loss is safe because the receipt and cursor already advanced. Record applicable handler set/version for deployment compatibility.
5. Handlers lock target aggregates in a documented consistent order. Cross-stream target contention/deadlock can abort the transaction; retry the entire transaction with no receipt-only success. Do not mark completion in a `finally` block. Read latest state for current authorization/projection, but use immutable event facts/revision references for transition effects; never lose a historical capture because current state says refunded.
6. Database handler success may create a durable **external delivery intent** with unique effect identity. Committing that intent is the handler's local completion; it is not proof that SMS/push/provider received it. A separate worker sends after commit, tracks provider request/response/uncertainty and reconciles using provider-supported mechanisms. See payment/refund contract for external money requests.
7. On handler error, rollback event/handler effects, then record failed attempt and next-attempt time under the cursor lock only if its expected sequence is still pending. Proposed complete schedule: eight total attempts, waits before attempts 2–8 of 1 s, 5 s, 30 s, 300 s, 3600 s, 3600 s, 3600 s. This resolves the source's five-delay/eight-attempt ambiguity and requires acceptance. Jitter bounds/alerts remain infrastructure config review.
8. Exhaustion blocks this aggregate cursor at the failed event and records DLQ metadata linked to the original immutable event; do not delete/move away its sole source row. Other aggregates continue. Subsequent events on this stream do not leapfrog the poison event. Monitor oldest pending/blocked age, not only queue length.
9. Scoped ops replay requires reason, current policy/step-up where applicable and corrected cause. Reuse original event ID, preserve failed attempts/audit, reset retry scheduling under cursor lock. Existing committed handler receipts remain. No generic skip button; irrecoverable event handling needs an explicitly reviewed compensation procedure preserving financial truth.
10. Deploys drain bounded transactions gracefully; a killed worker releases its DB lock. New handler versions require explicit replay/migration decisions: silently changing a handler's version must not apply historical side effects twice. Do not change the required handler set for an in-flight event without a migration plan.

The protocol guarantees ordered committed database handling within a source aggregate **if implemented and proven**. It does not guarantee cross-aggregate ordering, global exactly-once delivery or FCM/SMS arrival order. External consumers may dedupe/version independently; realtime clients compare snapshot versions and recover gaps. If durable external effects require ordered sending, give that delivery stream its own cursor and head-blocking policy.

## Producer/consumer map

Exact event names appear in each linked transition table. This map defines required consumer responsibilities for this domain slice; it is not a substitute for per-event machine-readable schemas in NK-DOC-4.

| Producer / contract | Payload allowlist beyond envelope | Required database consumers / effect | External delivery |
|---|---|---|---|
| [Organization review](organization-review.md) | org ID, review/ownership revision, from/to, safe reason code | Org eligibility projection, recovery queue on suspension/expiry, scoped review queues | Applicant decision notification; never include private documents |
| [Volunteer approval](volunteer-approval.md) | application/user opaque ID, review/check revision, from/to | Current eligibility and dispatch recovery; do not grant future bookings from old approval events | Applicant result, scoped ops queue |
| [Mission](mission-lifecycle.md) | mission/org IDs, need/target/submission/proof revisions, from/to | Public search/home invalidation, readiness/recovery tasks, impact eligibility on completion | Scoped participants; public card only through safe read serializer |
| [Contribution](contributions.md) | contribution/mission/need IDs, type, evidence revision | Owner Activity, verified-only summary/issuance eligibility, need counters using source facts | Confirmation separate from final impact notification |
| [Checkout/payment/refund](payments-and-payouts.md) | intent/capture/refund/allocation IDs, currency and immutable paise when needed | Allocation/recovery/finance projections; no duplicate mission credit | Durable provider request intent with stable key; owner-safe notification |
| [Payout](payments-and-payouts.md) | payout/allocation/transfer fact IDs, from/to | Liability and received-by-org projection from actual evidence | Org/Finance notification; no bank data in generic event |
| [Shipment](logistics-and-attendance.md) | shipment/contribution IDs, custody/assignment/schedule/receipt revisions, from/to | Tracking snapshot, contribution projection, dispatch and private-access revocation | Versioned WS hint and owner notification without home/GPS data |
| [Attendance](logistics-and-attendance.md) | booking/assignment/slot IDs, interval/verification revision | Capacity/offer state, contribution hours, correction intent after review | Reminders/offers with occurrence identity; scoped roster updates |
| [Proof](proof-and-impact.md) | proof/subject/submission/decision IDs, safe outcome | Proof queue, mission/fulfilment eligibility and case/correction work | Submission/decision notification; signed media resolved at read time |
| [Impact](proof-and-impact.md) | record/correction/effective revision/ledger sequence IDs | Effective summaries and certificate metadata, privacy/integrity work | Final-record ready only after commit; safe sharing projection |

Derived same-aggregate state changes must use the same version/sequence protocol. For cross-aggregate dependencies that are not ready, record durable pending work with the expected source facts; retries/related events re-evaluate it. A valid delivery event cannot be discarded permanently just because an assignment projection is late. Reconciliation periodically detects orphan references, stuck dependencies and projection drift.

## Notifications and offline/version recovery

Replace the source's lifetime uniqueness `(user, subject, template)` with durable occurrence-based identity: event/occurrence + recipient + channel/template version. A second legitimate reschedule/rework/offer must notify; replay of the same occurrence must not. Suppression decisions (preferences/quiet hours) are recorded separately from sent status. Recheck access before materializing private notification content or issuing a signed URL.

Realtime is a hint, not the durable record. Snapshots carry owner-scoped aggregate version; old events never regress a client. Sequence gaps trigger authenticated snapshot fetch. Redis restart may lose ephemeral hints without losing database events. Offline commands retain expected assignment version and must not silently change their meaning after revocation.

## Acceptance cases (not executed)

| ID | Fault / scenario | Required evidence |
|---|---|---|
| EV-01 | Two workers race adjacent events on one aggregate. | Real DB barriers show sequence N commits before N+1; separate aggregate still progresses. |
| EV-02 | Crash before business/outbox commit. | Neither state nor event persists. |
| EV-03 | Crash after handler write but before receipt/cursor commit. | Handler effect rolls back; replay applies once. |
| EV-04 | Lose commit acknowledgement, then replay. | Receipt/cursor prevent repeat effect; original event ID retained. |
| EV-05 | Poison event exhausts eight attempts. | Aggregate blocked visibly; later same-stream event not executed, other streams continue. |
| EV-06 | Ops repairs cause and replays. | Same event ID, full attempts/audit, no duplicate committed receipt/effect. |
| EV-07 | External send succeeds then response lost. | Delivery stays uncertain and reconciles; no blanket exactly-once claim for provider lacking dedupe. |
| EV-08 | New handler version deployed with pending events. | Recorded handler set and migration policy preserve one financial effect. |
| EV-09 | Two legitimate reschedules with same template. | Both occurrence notifications created; replay of either no-ops. |
| EV-10 | Cross-stream prerequisites arrive out of order. | Deferred work eventually reconciles and updates correct state; no historical evidence dropped. |
| EV-11 | Consumer reads captured event after refund already applied. | Capture/refund facts separately retained; correct allocation/recovery without regression. |
| EV-12 | Redis outage/reconnect and stale private notification. | Durable DB state survives; current auth checked; client restores snapshot without private leak. |

Remaining: per-event JSON schemas, actual handler registry/error contracts, live Postgres concurrency/crash proof, Redis/arq compatibility, metrics thresholds and reviewed ADR amendment. G13 is partial, not closed.
