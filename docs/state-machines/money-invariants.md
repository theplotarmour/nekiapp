# Money facts, allocation and recovery contract

**Status:** Technical review draft, NK-DOC-3.02. No financial/legal policy approval or executable schema is claimed. Sources: D2/D3/D5, PRD FR-07/16, plan G09–G12/G16/G17 and P3. [Provider evidence](../rnd/payment-provider-spike.md); [transition commands](payments-and-payouts.md).

## Identity and relational model proposal

- `contribution` is the user's mission/need intent with immutable reviewed amount/currency/fee-policy snapshot. It has multiple checkout attempts over time. A retry never erases a failed/uncertain attempt.
- `checkout_attempt` owns a persisted unique receipt, provider request hash/body, create-orchestration state and at most one linked provider order. A contribution has at most one locally authorized active checkout attempt, enforced under a locked contribution row; an uncertain older attempt blocks a replacement until resolved by approved recovery.
- `provider_order` has unique `(provider, account, environment, order_id)`, receipt and expected amount/currency; it links to its local attempt. `provider_payment` rows independently retain every observed payment ID/order ID. Do not constrain the number of observed payments to one: reconcile late or anomalous payments into recovery rather than reject financial evidence. Provider retry semantics remain RP-01.
- `capture_fact` is unique by provider/account/environment/payment ID and contains captured amount/currency and provider/server observation times. Extra capture cannot become a second accepted contribution allocation; it remains a recorded recoverable liability.
- `refund_intent` identifies one authorized request with immutable amount, source payment, reason, provider idempotency key/body hash and approval. `refund_fact` records confirmed processed amounts by unique provider refund ID. Intent status never subtracts money actually refunded.
- `allocation_credit` records the portion of a capture assigned to this mission/need under the immutable fee snapshot. Monetary source and contribution ownership must be validated before linking. Recovery captures have no normal mission credit until a reviewed command permits it.
- `allocation_balance` is a locked projection per allocation credit containing credited amount, consumed amount, reserved amount and version. A same-row check enforces nonnegative amounts and `consumed + reserved <= credited`. Credits/reductions and every reservation/consumption must use the same transaction protocol.
- `allocation_entries` is append-only history of credit, reserve, release, consume, and evidenced restoration with unique source-operation ID. Reservation rows identify purpose (payout/refund/hold), owner operation, positive amount and lifecycle. `payout_items` link allocation IDs/amounts, not an invalid uniqueness predicate on a parent payout's status.
- `payout` is an audited manual transfer instruction containing bank recipient revision/snapshot, exact allocation set, approvals, transfer attempt identity, UTR/evidence and status. A transfer attempt can be uncertain independently of payout's current display status.

These are proposed schema changes to document 05. They replace neither provider facts nor the full accounting ledger/retention review. No JSON payload is a substitute for required relational ownership, currency, amount and uniqueness constraints.

## Two separate conservation views

For each allocation credit, in integer INR paise:

`credited = available + reserved + consumed`

All terms nonnegative. `available = credited - reserved - consumed`. Reservation includes pending payouts, permitted refund debits and policy holds. Consumed includes paid organization principal and executed refund debit portions allocated to that credit. Reconciliation is a label on evidence; changing PAID → RECONCILED never releases consumption. A failed unsubmitted operation may release its reservation; an uncertain external effect may not.

For an org's unpaid mission principal:

`liability = credits - approved principal reductions - evidenced organization payments + evidenced payout returns`

Reservations reduce spendable availability but not the liability owed. Captured customer money outside mission allocation is a separate recovery liability. Refund customer gross and reduction of org principal can differ under fee/subsidy and post-payout recovery policy; do not subtract the customer refund twice or silently make an allocation balance negative.

Provider settlement cash is a third, independent reconciliation: captures, actual provider refund debits, fees/taxes/adjustments, reserves and bank credits matched to provider reports. Provider settlement does not itself pay an org or fulfil a mission. Only recorded, evidenced manual organization transfers support “Received by organization”.

## Launch fee snapshot (D2)

At ₹1,000 launch contribution, reviewed gross = 100000 paise and mission allocation = 100000 paise. A hypothetical actual gateway fee/tax of 2360 paise is a platform expense/subsidy, not a reduction to mission credit. If the provider remits 97640 paise, NEKI needs separately funded cash for the difference before paying the promised 100000. This illustrative amount is not a provider price quote.

Persist disclosure policy/version, gross, mission allocation, donor-borne fees if any and platform-borne fee policy at intent creation. Actual provider fees have their own later facts; estimates cannot be represented as reconciled charges. A different fee policy requires the plan's reviewed change and fresh user disclosure before payment, not mutation of a past transaction.

## Concurrency protocol proposal

1. Acquire contribution/payment roots and affected allocation balance rows in a documented deterministic ID order across refund, payout and capture allocation commands. Recheck active intent, scope, current version and source fact.
2. Reserve only where all requested allocation rows have sufficient available balance. Update balance + reservation + history/audit/outbox atomically; if any row fails, roll back the entire batch.
3. Approval must bind to exact allocation, amount, recipient revision and policy. After approval those fields cannot be edited. Bank change needs renewed independent verification and approval.
4. Before the manual operator leaves the console to execute a transfer, record the transfer attempt and keep its reservations. A lost acknowledgement creates an uncertain case, not a retryable fresh payment. A separate authorized reconciliation command records confirmed bank evidence.
5. On evidenced payment, atomically convert reserved to consumed without changing available. On reconciliation, no allocation movement. On proven pre-transfer cancellation/failure, release only unused reservations. A returned transfer can restore credit only once against bank return evidence; annotate the original paid history instead of deleting it.
6. Refund reservation and payout reservation compete for the same available principal. Refund after payout cannot consume the same principal again; require a separately approved platform-funded recovery and org receivable/return treatment. No automatic clawback or offset is assumed.

No transaction can make a provider API or bank action atomic with local writes. The recovery protocol must survive commit-success/response-loss on either side. Application locks alone do not suffice if administrative/worker paths bypass the shared database invariant.

## Worked invariant cases

| Case (paise) | Before | After / required result |
|---|---|---|
| Launch capture | Credit 0 | Credit 100000, available 100000; actual fee expense tracked separately. |
| Two simultaneous 70000 payout reservations | Available 100000 | Exactly one succeeds; available 30000/reserved 70000. Loser gets allocation conflict. |
| Partial payout recorded | Reserved 70000 | Consumed 70000, reserved 0, available 30000. |
| PAID → RECONCILED | Consumed 70000 | No balance change. |
| Refund 20000 from remaining principal | Available 30000 | Reserve 20000 then consume on processed refund; available 10000. Customer refund fact separately recorded. |
| Refund 50000 after payout | Available 10000 | Cannot reserve 50000 from this credit; open explicit funded-recovery decision, preserve request. |
| Extra/late capture after closed need | Existing accepted credit 100000 | Record extra capture once in recovery; do not overfill credit or fabricate another completed contribution. |
| Paid transfer returned 70000 | Consumed 90000 total including refund | Verified unique return can restore 70000 under recovery policy; no second restoration on replay. |

## Open financial decisions

| ID | Needed rule / proposed boundary | Accountable role |
|---|---|---|
| FD-01 | Late/extra capture: propose refund recovery by default; any reallocation requires explicit user consent and a new scoped allocation decision. Decide deadline and notification path. | Product + Finance |
| FD-02 | Refund eligibility, partial allocation split, actual nonrefundable fee treatment and post-payout recovery funding/receivable rules. Never infer legal entitlement or automatic org debt. | Finance + advisor/product |
| FD-03 | Payout cadence, holds/reserves/cash coverage and bank-verification/step-up procedure. Existing >₹50,000 two-person source rule remains; define approver independence and lower-value policy. | Finance + security |
| FD-04 | Local 30-minute expiry is an intent/reservation rule, not provider expiry. Decide when checkout can safely reopen and how long uncertain operations remain in queue. | Payments + product; RP-01/RP-02 |
| FD-05 | Receipt/tax document issuer, eligible copy, numbering and retention. Product approval of manual payouts is not advisor approval for live funds. | Founder + advisor/Finance |
| FD-06 | Accept projection/entry model, multi-credit payout atomicity, crash reconciliation, disputed bank-transfer duplicate handling and return evidence. | Backend + Finance |

All FD decisions OPEN. Before production use: reconcile document 05, prove actual Postgres concurrency/constraints and real sandbox behavior, obtain Finance acceptance and live-funds sign-off at its gate. Mathematical examples are not accounting/legal advice or runtime test evidence.
