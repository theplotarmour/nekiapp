# Contribution and checkout typed contract

**Status:** P0 review draft, 2026-09-10. Adds eight contribution and six owner-facing payment operations. Total coverage is 133 of 324 operations; the [manifest](openapi-coverage.json) identifies 191 remaining operations. No payment service or provider integration exists in this slice.

Source: [contract_contributions.py](../../tools/contract_contributions.py), [contribution lifecycle](../state-machines/contributions.md), [payment transitions](../state-machines/payments-and-payouts.md) and [money invariants](../state-machines/money-invariants.md). Use the [shared reproduction commands](identity-contract.md).

## Review and creation

Quotes carry one explicit MONEY, ITEM or TIME selection, owner display preferences, an expiry and a disclosure revision. A quote does not create a reservation. Final confirmation references the quote version, disclosure and consent receipt; clients cannot replace the quoted amount or set a paid status in this command. The service must bind quote ownership and mission, validate consent, recheck eligibility and reserve capacity atomically. Quote validity alone does not guarantee a booking.

MONEY uses positive integer INR paise. ITEM uses positive decimal quantities, condition, processed photo references and separate pickup or drop-off branches. TIME references the approved role and slot. Actual condition, food, serviceability, overlap and volunteer approval policies remain service checks. SKILL is excluded because MVP skills are interest registration, not contributions.

Contribution detail separates lifecycle from captured/allocated money, refund totals and recovery. Examples include a confirmed contribution with a partial refund, item and time records, and both item handover modes. Historical captures and delivery evidence must survive recovery changes. Display edits cannot change financial amounts. Public display and private messages still need server-side authorization and moderation.

## Checkout and evidence

Money confirmation records intent and durable checkout work. A 201 response does not claim that an external provider order exists. Checkout status exposes SDK parameters only in the READY branch with an ORDER_READY attempt. Uncertain or locally closed attempts have no checkout-parameter field. The service must also check current eligibility, expiry and ownership before returning those parameters.

Retry names the previous attempt and disclosure revision. It requires conclusive resolution of older uncertainty under FD-04/RP-01/RP-02; an empty provider lookup or elapsed timeout is insufficient. Cancellation closes local presentation and preserves reconciliation, late captures and liabilities. It cannot promise that a provider operation was cancelled.

Callback verification accepts owner-scoped order/payment/signature evidence and returns a pending operation with `payment_confirmed=false`. The provider signature must be verified against the server-bound order and secret; checking its format is insufficient. Capture and allocation require authoritative provider reconciliation. Rejection of a stale client command must not discard provider observations: the independent inbox/reconciliation path still records them. The webhook transport and saved-payment-method operations remain untyped and cannot inherit the ordinary bearer/idempotency profile without a dedicated transport review.

Launch capabilities enforce no wallet and zero donor gateway fees under D1/D2. Live-payment availability remains false until readiness is established. Payment receipts are acknowledgements, never tax-deduction certificates. Receipt policy for recovery captures remains subject to FD-05.

## Privacy, runtime invariants and outstanding work

Tracking contains scoped milestone evidence and safe explanations, without raw coordinates, volunteer phone or bank information. It must reflect accepted facts and distinguish pending evidence; stage ordering cannot erase delivery while a payout remains unresolved. Shipment access is separately authorized.

The service must enforce type-specific state guards, slot locks, idempotent intent creation, per-capture refund bounds, allocation uniqueness, display consent and verified outcome attribution. Independent financial totals are not interchangeable balances; schema nonnegativity does not prove accounting reconciliation. No SQL constraints, provider calls, concurrency, signature verification or runtime authorization are tested here. FD/CD decisions and exact event/error reconciliation remain open.

Refund cases, Finance payout commands, saved methods and raw provider webhook contracts are the next slices. Provider sandbox and legal/owner gate evidence remain required before live funds.

## Verification

Shared validation passes 133 operations and 1,421 attached request/response/error examples, including discriminated union variants. It rejects 82 negative schema cases and five query cases. The 21 new failures cover client status/amount/owner injection, zero amounts, cross-type fields, unsupported currency/skills, donor gateway fees, wallet support, signature shape, premature capture claims, tax claims and checkout parameters for uncertain orders.

Strict completeness intentionally fails with 191 operations untyped. P0 and later phases remain incomplete.
