# Transition contract catalogue

**Status:** P0 review draft, 2026-09-10. Ticket `NK-DOC-3.01`.

These contracts expand [TDD §6](../02-tdd.md), [data model](../05-data-model.md), and [flows F3/F7/F8/F9](../03-user-flows.md) under [D1–D7](../07-founder-decisions.md) and [plan §5.2](../08-complete-phased-plan.md). They are not implemented behavior or accepted schema amendments.

- [Organization review](organization-review.md)
- [Volunteer approval](volunteer-approval.md)
- [Mission lifecycle](mission-lifecycle.md)
- [Contribution lifecycle by type](contributions.md)
- [Checkout, refund and payout commands](payments-and-payouts.md)
- [Money facts and allocation invariants](money-invariants.md)
- [Planned money/contribution acceptance cases](money-acceptance.md)
- [Decision register and acceptance cases](review-decisions.md)

NK-DOC-3.02 now has initial contribution/payment/refund/payout drafts with [Razorpay documentation evidence and unexecuted sandbox probes](../rnd/payment-provider-spike.md). Shipment, assignment, proof-review, impact-correction and complete event catalogues remain subsequent tickets. Mission and contribution rows reference those contracts without claiming to define them. Financial FD and contribution CD decisions remain open alongside the PD register.

## Reading a transition row

**Source** means the edge/rule already appears in a governing source. **Proposed** means this draft supplies missing semantics. Every row remains a draft for review; a source-backed edge does not make newly specified event names or role assignments accepted. `PD-xx` identifies an unresolved decision in the linked register. No row linked to an unresolved decision is ready for dependent production implementation.

Each row specifies actor, expected version, required guards/evidence, transactional effects, event, display copy, notification recipients and a failure code. Shared rules below apply to **every row**, including creation, same-state commands and scheduler actions. Error/event identifiers introduced here are proposed names pending OpenAPI/event catalogue review.

## Shared command contract

1. Authorize the current authenticated principal against the aggregate's server-resolved owner/org and action policy. Role names in the tables are proposed scoped capabilities under G25; Finance and Super Admin do not inherit a universal status-edit permission. Anonymous users only receive permitted public reads. An applicant may manage its own submission before acquiring an org-admin/volunteer role.
2. Updates carry `expected_version = current aggregate version`; creation uses version 0 and the unique owner/application identity. A successful command advances version exactly once. Concurrent commands with an old version return `409 VERSION_CONFLICT` and an authorized current projection, never private review notes. Worker commands also use a stable command identity and compare current state/version.
3. Idempotency scope is `(principal, operation, key)` plus canonical request hash. An authorized replay with the same hash returns its recorded result without another transition; a different hash returns `409 IDEMPOTENCY_KEY_REUSED`. In-flight handling and retention remain G05/G13 contract work. Recheck current access before returning any stored sensitive response.
4. Validate the allowed prior state, current owner/volunteer/org status, required evidence and policy revision within the write transaction. Serialize competing dependent operations on the relevant records; a preflight check alone cannot authorize publishing, booking or assignment across a concurrent suspension. Exact locking order is a schema/prototype follow-up.
5. Commit state/version, append-only transition/decision history, evidence references, audit context and durable outbox entry together. On validation failure none of those writes commit. Do not send push, call a payment provider, or claim a refund completed inside this transaction.
6. History records actor or service principal, command ID, from/to, previous/new version, reason code, safe applicant-facing explanation, restricted review notes, evidence revision IDs, policy/consent version where relevant, and UTC server time. Captured/client time is separate evidence, never a substitute for commit time. Audit records refer to protected documents instead of copying their contents.
7. Proposed event envelope: event ID, versioned event type, aggregate type/ID/sequence, occurred-at UTC, correlation/causation IDs, transition ID and minimal changed facts. No phone, home address, bank details or review documents in generic events. Ordering, receipt transactions, retries and DLQ remain NK-DOC-3.03/G13 work; this draft does not fix them by naming an envelope.
8. Notification entries below are durable delivery intents after commit, subject to approved channel preferences/quiet-hours policy, deduplicated by event and recipient. Account/queue state remains readable if push fails. Copy must reflect committed server status; notifications never create authorization or verified impact.
9. Defaults: `401 AUTH_REQUIRED`, `403 ACTION_FORBIDDEN`, owner-scoped lookup `404 NOT_FOUND`, `409 VERSION_CONFLICT`, domain-specific state conflict, and `422 EVIDENCE_REQUIRED` for absent/invalid required evidence. Table error lists add domain failures; every row also inherits these defaults. Exact response bodies are pending OpenAPI.

## Schema follow-up, not migrations

The current model lacks explicit aggregate versions, org/application transition histories, mission resume state, reviewed submission revisions and complete consent/check provenance. Proposed additions are recorded per contract. No DDL here is considered executable or canonical until reconciled into document 05 and reviewed with concurrency cases.
