# Razorpay contract evidence and sandbox spike

**Inspected:** 2026-09-10. **Result:** Documentation inspection only; sandbox/account compatibility NOT verified. Supports NK-DOC-3.02 and G11/G12/G28. No credentials, provider mutations or live transactions used.

The web reader could not render the site's `text/markdown` responses. Primary content was retrieved from the corresponding `.md` URLs using HTTP GET. HTML wrappers alone were not treated as evidence.

| Topic | Primary evidence | Contract consequence |
|---|---|---|
| Retry conflict | [Create order](https://razorpay.com/docs/api/orders/create.md) instructs creating a fresh order for each payment attempt. [Orders overview](https://razorpay.com/docs/payments/orders.md) describes combining multiple attempts per order and disallows another attempt while an associated payment is authorized. | Conflicting vendor documentation; do not claim reuse is proven. Sandbox must establish Flutter Checkout behavior and safe retry conditions. Keep all provider payment entities instead of assuming one row per contribution. |
| Uncertain order lookup | [Fetch all orders](https://razorpay.com/docs/api/orders/fetch-all.md) documents receipt filtering and an attempts count. | Persist unique local receipt before sending create request; reconcile returned order identities, amount and currency. Receipt lookup availability does not prove immediate consistency, create idempotency or safe retry after an empty lookup. |
| Duplicate/out-of-order webhooks | [Validation guide](https://razorpay.com/docs/webhooks/validate-test.md) specifies raw-body signature verification, event-ID deduplication, and unordered delivery. | Verify before trusting payload; durable inbox; domain dedupe also uses provider payment/refund identity because different events can describe one effect. Never regress capture on an older authorization/failure notification. |
| Capture observations | [Payment events](https://razorpay.com/docs/webhooks/payments.md) describes capture notifications and event-time snapshots; `payment.captured` and `order.paid` can describe the same capture. | Client callback is only a reconciliation hint. Capture creates one immutable monetary fact even when both events arrive. |
| Refund retry | [Idempotent refunds](https://razorpay.com/docs/api/refunds/normal-refunds-idempotent.md) documents `X-Refund-Idempotency`, fixed-body retries, and pending/processed/failed states. | Persist one provider key and exact request body per logical refund; retain uncertain reservations and reconcile. A timeout must not create a new refund identity. |

## Required sandbox evidence

| Probe | Procedure | Pass evidence / failure action |
|---|---|---|
| RP-01 Order retries | Pin Flutter/plugin/provider config; fail a checkout attempt, inspect all order payments, test documented fresh-order behavior and reuse behavior under controlled conditions. | Record exact request/response IDs with redacted fixtures and SDK versions; resolve documentation conflict before enabling retry UI. |
| RP-02 Lost create response | Drop response after provider accepts request; query using persisted receipt over bounded reconciliation intervals. | Recover exactly the original order with correct amount/currency; if still uncertain, show ops case and block replacement checkout. Empty query alone never passes safe-retry proof. |
| RP-03 Late capture | Expire local reservation, then deliver capture and delayed authorization/failure events in different orders. | Capture retained once; allocation only if still permitted, otherwise recovery/refund liability; no false failure or silent overfill. |
| RP-04 Double event | Replay signed capture and order-paid notifications, including different event IDs for same payment. | One capture fact, one accepted allocation, stable receipt identity. |
| RP-05 Refund uncertainty | Lose refund response and replay same key/body; observe status by provider refund identity. | One refund; reservation persists until authoritative terminal result; retry with changed body rejected. |
| RP-06 Signature rotation | Sign raw-byte fixtures with active/retained previous secret, alter one byte, replay old events after rotation. | Legitimate historical retry follows documented secret policy; forged/mutated body rejected; secrets excluded from fixtures/logs. |
| RP-07 Partial refund and settlement | Capture, partially refund, reconcile settlement fee/tax adjustments and manual payout records. | Exact paise facts and separate customer refund, org liability, platform subsidy and bank movement; no balance derived from mutable payment status. |

Owner: payments/backend + Finance for RP-07. Dates and accounts unassigned. Documentation findings do not prove regional account capabilities, merchant legal role, approval to accept funds, refund speed/SLA, or receipt/tax policy. Those remain the plan's explicit gates.
