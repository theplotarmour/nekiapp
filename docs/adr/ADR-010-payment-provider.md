# ADR-010 — Payments: Razorpay (Orders + Webhooks; Route pending legal)

| Status | Accepted — D3/D5 locked 2026-09-07 (`07-founder-decisions.md`); legal sign-off on money-flow structure required before live funds |
|---|---|
| Deciders | Tech lead, founder, finance/legal |
| Related | `01-prd.md FR-07, Q2, Q6, Q7`; `02-tdd.md §10` |

## Context
India launch; UPI is the dominant method, plus cards, net banking, wallets. Contributions are typically ₹500–₹5,000. Fees must be disclosed exactly. Server must be the source of payment truth. Money may need to reach organizations' bank accounts with a platform fee retained (marketplace model), or land in NEKI's account with periodic payouts, depending on legal structure.

## Decision
**Razorpay** as MVP provider (D5): server-created Orders (amount server-side), Razorpay Checkout via `razorpay_flutter`, HMAC signature verification on client callback, **webhooks as authoritative** (`payment.captured`, `payment.failed`, `refund.processed`) with event-id dedupe, reconciliation worker every 5 min, refunds API. Only payment methods enabled in the approved Razorpay configuration are offered (remote config). Settlement (D3): funds settle to NEKI's account; Finance records **manual payouts** in the ops console (`payouts` + `payout_items`, DRAFT→APPROVED→PAID→RECONCILED, two-person rule above ₹50,000). `SettlementStrategy` interface ships with `ManualPayoutStrategy`; `RazorpayRouteStrategy` deferred to NEXT. Fee policy (D2): NEKI absorbs gateway fees for launch organizations; disclosure block rendered from stored fee fields.

## Alternatives
- **Stripe India** — restricted onboarding and UPI coverage limitations for new Indian entities; better DX.
- **Cashfree** — strong UPI and payouts; comparable; kept as second choice/fallback adapter.
- **PhonePe / Paytm PG** — narrower method coverage and weaker docs.
- **Juspay Hyperswitch (orchestration)** — flexibility across PGs; premature complexity.

## Pros
Broad method coverage; mature webhooks; Route for split settlements; test mode; wide Flutter usage in India.

## Cons
Route eligibility and KYC per organization adds onboarding friction; webhook delays happen (designed for: Confirming state, never false failure).

## Risks
- Legal: NEKI's role (facilitator vs donee) affects 80G receipts and GST on platform fee → decision needed by week 6; both paths designed.
- Provider outage → kill switch disables money contributions gracefully.

## Consequences
Amounts in paise; `fee_policy` per mission drives disclosure; "100% goes to the mission" copy only when platform absorbs gateway fee. No card data ever touches NEKI. Idempotency key per contribution attempt; 30-minute expiry on unpaid orders.

## Migration path
`PaymentProvider` and `SettlementStrategy` interfaces; adding Cashfree is an adapter plus webhook route. Historical payments keep `provider` column.
