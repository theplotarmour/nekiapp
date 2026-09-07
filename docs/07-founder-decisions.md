# NEKI — Founder Decisions (locked)

| Field | Value |
|---|---|
| Date locked | 2026-09-07 |
| Source | Founder response to `06-eng-plan.md §11` |
| Effect | Baseline for MVP specification; supersedes defaults in `01-prd.md §12` and `06-eng-plan.md §11` |

## Locked set

| ID | Decision | Final | Status |
|---|---|---|---|
| D1 | Wallet chip in MVP header | Remove wallet entirely — header, profile, navigation, contribution flow. Reconsider only after core contribution loop is proven. | LOCKED |
| D2 | Fee policy + "100%" copy | NEKI absorbs payment gateway fee for launch organizations. UI shows the actual allocation/split on every transaction; the phrase "100% reaches the NGO" is never used unless literally true for that transaction. | LOCKED |
| D3 | Money flow — Route vs manual payouts | Manual payouts for MVP. Every payout recorded in `payouts` with full digital audit trail. Razorpay Route deferred. | LOCKED* |
| D4 | Launch city | Delhi NCR only. | LOCKED |
| D5 | Payment provider | Razorpay, behind a NEKI payment service abstraction. Only methods enabled in the approved Razorpay configuration are shown. | LOCKED |
| D6 | Operations console | Flutter Web. Operational efficiency over visual experimentation. Ops must be able to intervene manually at every step. | LOCKED |
| D7 | Volunteer ID verification | Phone OTP + basic profile + volunteer application → ops review → approved. No government-ID/KYC in MVP; full identity verification deferred to Phase 4+. | LOCKED |

\* D3 is the product/operational decision. The legal structure and money-flow compliance (NEKI's role as facilitator vs donee, GST on fees, 80G handling) must be signed off by a qualified CA/CS/legal advisor **before live funds are accepted**. Tracked as risk R8 in `06-eng-plan.md §9`.

## Operating principle

> Automate what creates scale. Manually operate what creates trust.

## Consequences applied to the doc set

| Doc | Change |
|---|---|
| `01-prd.md` | §12 open questions resolved; FR-07 fee-disclosure example fixed; FR-09 volunteer application/approval step; FR-16 ops console modules include Payouts, Contributors, Reports; non-goals reaffirm no wallet |
| `02-tdd.md` | §10 settlement = manual payouts via `SettlementStrategy.manual`; Route moved to NEXT; §23 open question 1 closed |
| `04-design-brief.md` | Wallet chip already removed; D2 disclosure block format |
| `05-data-model.md` | `payouts` enriched (recipient, operator, reference, notes, status machine); new `payout_items`; new `volunteer_applications` |
| `06-eng-plan.md` | §11 marked locked; NK-API-13 scoped to manual settlement; new NK-API-24 (payouts) and NK-WEB-3 payouts UI; NK-API-18 includes volunteer application + ops approval |
| `adr/ADR-010` | Status → Accepted; Route deferred to NEXT |

## D2 disclosure format (UI contract)

Default (launch organizations):

```
You contribute        ₹1,000
Mission allocation    ₹1,000
Gateway fee           Covered by NEKI
```

When economics differ (per `missions.fee_policy`):

```
Contribution          ₹1,000
Gateway fee           ₹X
Platform fee          ₹Y (if any)
Mission allocation    ₹Z
```

Rendered on Contribute (fee line), Review (full block), receipt, and Impact Record.

## D3 payout record (minimum fields)

Payout ID · Mission ID · Organization ID · Amount · Date · Status · Bank/UTR reference · Recipient (account holder) · Operator · Notes · Linked contributions (via `payout_items`). See `05-data-model.md §4.5`.

## D6 ops console modules

Dashboard · Missions · Organizations · Contributors · Volunteers · Contributions · Payouts · Tracking (dispatch) · Proof · Verification · Reports. Manual interventions available on every aggregate: assign volunteer, change status (with reason), record pickup/delivery, upload proof on behalf of org, verify, approve impact, record payout, refund.

## D7 volunteer flow

```
Phone OTP → basic profile → volunteer application (availability, area, skills, consent) → ops review → APPROVED → eligible for assignment
```
Higher-risk missions (home pickups, minors present) may require additional manual checks per SOP. Phase 4+: identity/document verification, trust profile, automation.
