# Logistics and custody typed contract

**Status:** P0 review draft, 2026-09-11. Adds all 24 logistics-family operations. Total coverage is 241 of 324, with [83 operations remaining](openapi-coverage.json). No dispatch service, tracking server or mobile workflow is implemented.

Authoring source: [contract_logistics.py](../../tools/contract_logistics.py). Governing requirements: [S01–S16](../state-machines/logistics-and-attendance.md), D7, [contribution lifecycle](../state-machines/contributions.md) and [authorization matrix](authorization.md). Use the [shared reproduction commands](identity-contract.md).

## Privacy and current assignment

Shipment summaries contain physical state and independent schedule, delay and recovery metadata. They exclude private addresses and phone numbers. DELAYED is not a physical state, and DELIVERED/VERIFIED require an accepted receipt reference. The existence of a reference does not itself prove acceptance or verification.

Private pickup/destination addresses are confined to active field details, which identify the current assignment revision, access grant and expiry. The request also names the expected assignment revision. Every read must recheck current approval, scoped clearance, assignment, access window and revocation; a cached grant or role is insufficient. A withheld contact cannot contain a phone. The consented branch requires consent provenance, but actual disclosure policy and current consent remain server checks. Privacy review must approve this conditional field scope before runtime use.

Pickup-slot lookup identifies the mission and owned address for serviceability checks. Results show availability only. Cursor/filter scope, current address ownership and serviceability must be revalidated when reserving. Rescheduling atomically replaces the relevant capacity and schedule revision, then explicitly reconciles assignment compatibility. Cancellation/unassignment cannot race past accepted custody.

## Custody, receipts and exceptions

Readiness binds schedule and assignment revisions. Pickup requires actual quantities, source acknowledgement and evidence; beginning a route requires current custody. Arrival evidence is not a receipt. Receipt submission returns PENDING_ACKNOWLEDGEMENT with `delivery_accepted=false`. Destination acceptance binds the exact receipt revision, evidence and actual quantities, ends active tracking/access and leaves proof verification separate.

Drop-off acceptance has its own source acknowledgement and quantity input without fabricating a courier route. The service must require the allowed mode and exact eligible contribution. Zero actual quantities can represent discrepancy evidence; they cannot alone establish successful delivery or verified impact. Need IDs, units, uniqueness, partial quantities and reconciliation against proposed receipts are semantic checks, not guaranteed by array schemas.

Ops exceptions require case/policy/evidence references and step-up. Handoff names both acknowledgements and the old custody revision, with explicit replacement-volunteer or return-to-source disposition. Both parties' acknowledgement identities and authority must be checked; IDs supplied by one operator cannot establish two-party consent by themselves. Prior access is revoked and history appended. A returned item is not a completed donation, and S15 alone does not settle final return/recovery policy under LD-01.

## Location and incident handling

Location batches bind assignment revision and tracking consent. Each sample has a stable ID, timestamp, point, accuracy and device-reported mock status. The service must authorize the whole batch before considering samples, enforce active foreground tracking/time windows, deduplicate sample IDs even when other fields differ, and partition accepted/rejected IDs against the submitted set. Batch and numeric limits are draft wire bounds, not adopted movement/accuracy policy.

Ping acknowledgements cannot claim delivery. Retention, smoothing, stale ETA, consent revocation and map disclosure remain G21/G22/LD-02 work. GPS evidence and mock flags do not establish misconduct or physical receipt. Delay records preserve estimate time/basis and permit an unknown ETA. Issue reports create cases without changing custody; historical participation permits scoped recovery reporting without granting current private tracking access.

Offline custody commands require a stable command identity, current aggregate/assignment revisions and captured evidence. Existing idempotency headers provide the command identity at HTTP submission. Local media must be uploaded and resolved before canonical evidence references are submitted. Pending sync is not accepted pickup. Conflicts preserve evidence for review instead of blindly replaying against a newer revision.

## Verification and remaining work

Shared validation passes 241 operations and 2,793 request/response/error examples and rejects 187 negative schema cases plus five query cases. This slice adds 23 failures covering private summary fields, physical-state misuse, delivery without a receipt, missing custody/consent acknowledgements, empty evidence, false ping/receipt success, invalid coordinates and phone disclosure in the withheld branch.

No database reservation race, revocation, actual custody, two-party acknowledgement, location retention or offline replay was tested. Strict completeness fails with 83 operations untyped. LD/CD/privacy decisions and runtime proof remain open. Proof, impact and remaining administration/transport families follow; P0 is not complete.
