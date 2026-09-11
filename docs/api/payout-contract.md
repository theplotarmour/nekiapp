# Payout and Finance typed contract

**Status:** P0 review draft, 2026-09-11. Adds all 24 payout-family operations, bringing coverage to 174 of 324 inventory operations. [Exact coverage](openapi-coverage.json) lists 150 remaining operations. These are contracts, not implemented banking or accounting workflows.

Source: [contract_payouts.py](../../tools/contract_payouts.py), [Y01–Y09 payout transitions](../state-machines/payments-and-payouts.md), [money invariants and FD decisions](../state-machines/money-invariants.md), D3 and the [authorization matrix](authorization.md). Run the [shared reproduction commands](identity-contract.md).

## Draft, approval and transfer

Draft creation specifies one organization, a verified bank revision and positive allocation amounts with allocation versions. The server computes the total, locks all source balances, verifies same-organization INR scope and reserves atomically. Duplicate allocation IDs must be rejected even when two entries have different amounts; JSON array uniqueness alone is insufficient. Displayed availability is not a reservation.

Draft replacement must atomically release/replace the relevant reservations and invalidate old review snapshots. Submission creates an immutable review snapshot without approving the payout. Approval binds that snapshot, evidence and expected version; it cannot change total or impersonate the approver. Current holds, cash coverage and bank validity are rechecked. The source rule requires a distinct approver above 5,000,000 paise; approver identity and independence must be established by the server, not client assertions. FD-03 still needs the precise lower-value and approval policy.

Beginning a transfer persists an attempt before the external bank action. Its result is not a paid confirmation. Uncertain attempts preserve all reservations and require a reconciliation case. Failure requires conclusive no-transfer evidence; timeout cannot establish failure. Cancellation must serialize against invocation and deny unresolved or successful transfers.

Paid recording requires the exact attempt, bank revision, amount, INR currency, bank reference, value date and evidence. The server verifies the evidence and recipient, then consumes the reservation once. Reconciliation references a bank report and snapshot but makes no additional balance movement. Method-specific evidence remains FD-03/06 work; a typed reference is not proof of bank settlement.

Returns append unique bank-return facts and approved accounting treatment while retaining original paid/reconciled history. Return totals cannot exceed eligible transfers, and replay cannot restore funds twice. A later replacement payout references the return and creates a new instruction; it must not mutate the original recipient or payment. Example variants preserve both an uncertain attempt and a reconciled payout with a return.

## Bank review and reporting

Bank decisions bind the proposed revision and verification decision. They cannot substitute an account number during approval. Masked review summaries reference verification evidence; actual verification still requires a restricted procedure and current evidence. A bank change invalidates dependent stale approvals without rewriting paid history.

Organization payout responses exclude internal notes, preparer/approver identities, allocation-level contributor data and raw accounts. Organization statements have a cursor bound to an immutable snapshot. Opening/closing balances cover the statement period, not each page. The service must define the period and ledger mapping under FD-06, preserve ordering and prevent pagination across another organization's snapshot. `cursor` and `limit` are explicitly typed on the statement route.

Finance liability reports separate available, reserved and consumed principal from unallocated captures and platform-funded recovery. These are distinct accounting categories, not quantities to sum blindly. Reconciliation reports retain expected and observed facts plus unmatched/variance/uncertain states. Actual accounting equality, approved adjustments, receivables, holds and cash reconciliation remain database/service obligations.

CSV export requests specify a bounded scope, report, period and purpose. The worker must validate the date range and approved retention limits, capture a stable snapshot, apply field filtering and neutralize spreadsheet formula cells. Ready exports return a private media reference with expiry; every download rechecks current authorization. A media ID never grants access by itself. Examples illustrate schema branches, not completed asynchronous operations.

## Verification and limits

The shared suite validates 174 operations and 1,941 request/response/error examples. It rejects 131 negative schema cases and five query cases. The 26 new failures cover injected paid status, client totals/approvers, unsupported currency, empty or zero allocations, missing bound decisions, invalid dates/amounts, unsupported paid claims, force cancellation, private fields and export format changes.

The generator now merges operation-specific query parameters across authoring modules and rejects duplicate parameter definitions by operation. Existing discovery query checks still pass.

Strict completeness fails with 150 operations untyped. No transfer, database lock, bank verification, CSV generation or authorization has executed. PostgreSQL concurrency proof, funding/approval policy, provider sandbox evidence and live-funds sign-off remain open. Provider transport and the remaining domain families are next; P0 is not closed.
