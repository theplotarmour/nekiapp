# Planned money and contribution acceptance evidence

**Status:** Not executed. NK-DOC-3.02; plan T01–T16 and P3 gate. These cases define meaningful database, provider and UI evidence; document row counts are not a substitute.

| ID | Trigger / setup | Required result | Evidence / contract |
|---|---|---|---|
| MC-01 | Double final Review tap, same idempotency key/body. | One contribution/attempt/reservation and stable response; no duplicate order invocation attributable to retry. | DB + provider mock invocation count; C01/P01/P02 |
| MC-02 | Same key with changed amount/message revision. | Conflict; original immutable financial request remains unchanged. | API/hash/error fixture; CD-01 |
| MC-03 | Provider accepts order but HTTP response lost; worker crashes. | Persisted receipt recovers original order or remains uncertain; no blind replacement. | Sandbox RP-02 + restart; P04 |
| MC-04 | Close checkout while create request is in-flight. | Order may still be recorded, checkout stays closed and later payment reconciles; no orphan silent capture. | Concurrency barriers + provider fixture; P06/P07 |
| MC-05 | Signed `payment.captured` and `order.paid` for same payment, retries with same/different event IDs. | One capture fact and allocation; every inbox event disposition visible. | DB uniqueness/replay + RP-04 |
| MC-06 | Captured event before delayed authorization/failure. | No status/fact regression or repeated notification; no lost money. | Permutations + provider fixture; P08–P10 |
| MC-07 | Local intent expires/mission cancels before capture arrives. | Capture fact retained; approved eligible recovery or funded refund case, no automatic overfill/reallocation. | API/UI/ledger assertions; FD-01 |
| MC-08 | Second successful payment arrives for one accepted contribution. | Both real captures retained; only one accepted contribution allocation; extra amount in recovery. | Capture/credit totals + Finance queue; P11 |
| MC-09 | Unknown order, wrong account/environment/currency/amount on observation. | No owner success/allocation from untrusted match; quarantine/reconciliation preserves authentic evidence. | Signature/ownership tests; P08/P09 |
| MC-10 | Two payouts concurrently reserve 70000 paise from 100000 credit. | Exactly one reserve commits, no partial payout rows/negative available balance. | Real Postgres concurrent sessions, commit/rollback evidence; Y01 |
| MC-11 | Batch payout has one insufficient allocation among sufficient ones. | Entire batch fails without reserving others; deterministic lock order avoids inconsistent partial outcome. | Real Postgres + deadlock retry; FD-06 |
| MC-12 | Refund and payout reserve same remaining principal concurrently. | No double spend; losing request remains visible with reason. | Real Postgres barriers; R01/Y01 |
| MC-13 | Mark PAID → RECONCILED then try another payout. | Original consumed balance stays unavailable; no parent-status uniqueness loophole. | DB constraint/projection + Y06 |
| MC-14 | Bank transfer performed; operator loses network before recording paid. | Attempt remains uncertain/reserved; no second transfer button until reconciled. | Console + bank evidence replay; Y03–Y05 |
| MC-15 | Bank recipient changes after approval, or preparer approves >₹50,000 alone. | Transfer blocked pending required verified revision/distinct approval; historical snapshot preserved. | Role/step-up/API tests; Y02/Y03 |
| MC-16 | Refund response lost, same body/key retried. | One provider refund and one reserved amount; no release until authoritative result. | RP-05 + DB; R03–R06 |
| MC-17 | Multiple partial refunds followed by excess request. | Sum processed + active reservations cannot exceed actual captured amount; execution history unchanged. | DB concurrency + API/UI; R01 |
| MC-18 | Refund after principal already paid out. | No negative allocation or hidden automatic debt; explicit reviewed funding case. | Finance workflow and immutable facts; FD-02 |
| MC-19 | Previously failed refund later reports processed. | Real refund recorded once; funding discrepancy raised, not discarded. | Reconciliation incident fixture; R07 exception |
| MC-20 | Paid transfer returns, return event/evidence entered twice. | One restoration, original transfer retained, new payout requires new instruction. | DB source uniqueness + Y09 |
| MC-21 | Platform absorbs hypothetical 2360 fee on 100000 contribution. | Mission credit 100000, provider cash 97640, platform expense/cash shortfall separately shown. | Exact paise report recomputation; invariant example |
| MC-22 | Delivery precedes manual payout, or contribution partially refunded during execution. | Actual evidence displayed without falsely completing/refunding the whole lifecycle. | Projection/UI + CD-02 |
| MC-23 | Item pickup races cancellation/rescheduling. | Exactly one accepted custody/capacity outcome; no released capacity for a still-valid old booking. | Real DB sessions + C13/C14 |
| MC-24 | Time booking races suspension/waitlist promotion. | Current approval/capacity serialized; no duplicate assignment or false hours. | DB/API + C15/SC-08 |
| MC-25 | Checkout succeeded but mission not verified. | Thank-you uses contribution confirmation; no final impact record/certificate/completion analytics. | UI/event assertions; C22/G17 |

Record test revision, environment, redacted provider IDs, command, actual output and reviewer when executed. Finance approval, legal sign-off, provider-account capabilities and real bank movements cannot be certified by synthetic fixtures.
