# Transition review decisions and acceptance cases

**Status:** All PD decisions below are OPEN. No owner approval or runtime test execution is claimed. Accountable roles still require named people. These decisions refine G14/G25/G29 and linked gaps; they do not override D1–D7.

## Decisions needed before implementation

| ID | Conflict or missing rule | Proposed resolution for review | Accountable role / source updates |
|---|---|---|---|
| PD-01 | Org lifecycle and `verification_status` can disagree. | Lifecycle controls current eligibility; review status describes the latest cycle. Define one transactional projection mapping, including suspended/expired/reinstatement review. | Backend + ops; TDD §6, model §4.2 |
| PD-02 | Applicant ownership, duplicate orgs and rejected reapplication are unspecified. | Server-bound applicant ownership before role grant; immutable submission cycles under stable org identity. Agree duplicate detection, reapplication limits and evidence. | Product + ops/security; FR-15, model, API |
| PD-03 | Model says annual verification and first-three-mission probation but expiry/reinstatement evidence is incomplete. | Preserve those as source assumptions pending policy confirmation; define validity basis, renewal, probation checks and decision rights. Never silently auto-verify renewal. | Ops + product; org policy/model |
| PD-04 | Suspension immediately affects access but missions/items may already be in execution. | Immediate authorization denial plus durable scoped recovery queue; agree safe custody handoff, participant copy, refunds and accountable dispatch action. | Ops + security + Finance; F9, authorization/recovery contracts |
| PD-05 | Volunteer application has one row per user but rework/reapplication/consent history is missing. | Stable application identity with immutable cycles and versioned SOP consent. Decide renewed-review triggers, withdrawal, eligibility and reapplication timing. | Product + ops; FR-09, model §4.6 |
| PD-06 | One enhanced-check flag cannot represent mission-specific risk or revocation. | Scoped check record with SOP revision, evidence, validity and result; decide failed-check escalation and reinstatement rights. No MVP government-ID/KYC. | Ops + security; D7 SOP, model/role matrix |
| PD-07 | ACTIVE and PUBLISHED classification/readiness are incomplete. | Money-only FUNDING, time-only RECRUITING, item-only/mixed ACTIVE; recoverable post-publication classification; all collection states eligible for readiness evaluation. | Product + backend; TDD §6.1/model/read API |
| PD-08 | Mission needs-info exists in F8 but no mission enum; draft/rejected edit rights unclear. | DRAFT plus explicit NEEDS_MORE_INFORMATION moderation decision; preserve old submission. Decide whether unverified org can save drafts, reapply, or withdraw pending review. | Product + ops; F7/F8, model/TDD |
| PD-09 | Mixed need completion, partial minima, expired reservations and late contributions can conflict with readiness. | Snapshot per-need feasible readiness with serialized balance/capacity recheck; approve minimums, overfill, readiness invalidation and manual delivery exceptions. No automatic readiness on allow_partial alone. | Product + backend + Finance; G10/G11/G15, needs schema |
| PD-10 | TDD sends rejected proof to DISPUTED, F10 sends rejected proof to DELIVERED. | Distinguish NEEDS_MORE_INFORMATION (rework) from REJECTED (case review); decide exact rejection/appeal effect and proof requirements before accepting M13/M14/M21. | Ops + product; TDD §6, F8/F10, verification contract |
| PD-11 | Terminal recovery, cancellation boundaries and dispute exits are incomplete. | Explicit case decisions and durable financial/custody recovery; no implied refund/reallocation or rewriting final impact. Agree role rights and acceptable outcomes. | Ops + Finance + product; TDD/flows/money contracts |
| PD-12 | “Any active” pause and “previous” resume omit deadline/readiness/actor checks. | Explicit pausable set and saved state/cause; review all guards on resume. Define paused deadlines and who can lift ops versus org pauses. | Ops + backend; TDD/model |
| PD-13 | Targets locked after contributions but approval schema/consent consequences absent. | Structured requested/approved before-after revision; serialize with reservations; define contributor notification/consent and significant location/deadline changes. | Product + ops + backend; FR-15/G29/model |

Acceptance requires recording owner, date, selected rule and rationale here, then reconciling all listed authoritative source sections and linked API/schema/event contracts. A draft recommendation is not an accepted policy.

## Planned adverse and normal cases

These are acceptance specifications for later API/database/UI tests. Documentation consistency checks cannot execute these behaviors.

| Case | Scenario | Required observable result | Transition / gap |
|---|---|---|---|
| SC-01 | Applicant submits org, reviewer requests docs, applicant resubmits, reviewer verifies. | Stable ownership, immutable evidence revisions and decisions; only final approval grants verified capability. | O01–O05; G29 |
| SC-02 | Other org/user guesses application/document ID. | Denied owner-scoped lookup; no document URL or private review notes. | O01–O11; G24/G25 |
| SC-03 | Two reviewers approve/reject the same expected version concurrently. | One decision commits; loser receives version conflict; one history/event per committed decision. | O05/O06, V04/V05 |
| SC-04 | Retry command with same key/hash, then same key/different hash. | Original authorized result without another effect; mismatched hash rejected. | All rows |
| SC-05 | Org suspension races publication or contribution authorization. | Serialization prevents new authorization after suspension wins; pending recovery fan-out cannot reopen access. | O08/M03; G25 |
| SC-06 | Verification expires while mission active; worker restarts. | Badge/access reflect expiry, durable recovery survives; replay does not duplicate participant recovery. | O09/M15; G13 |
| SC-07 | Rejected/suspended volunteer invokes booking with old role token. | Current status denies action; no assignment or capacity reservation created. | V05/V07; D7 |
| SC-08 | Approval, enhanced check and booking race with suspension. | Final assignment requires serialized current approval and applicable clearance; a stale check cannot grant access. | V04/V07/V09 |
| SC-09 | Suspended volunteer carrying items reconnects with queued delivery. | No automatic false completion; dispatch recovery remains visible and custody has a reviewed handoff. | V07; PD-04 |
| SC-10 | User reapplies and reviewer opens an old submission revision. | History retained; old revision cannot be approved as the new submission. | O07/V06/M06 |
| SC-11 | Money target closes while item/time need remains open. | Eligible item/time CTA remains available; mission is not falsely globally fulfilled. | M07/M08; G15 |
| SC-12 | Deadline/readiness evaluation races capture, expired reservation or slot cancellation. | One coherent per-need snapshot; no READY with unmet approved minima, no unaccounted late capture. | M08/M18/M19; G11/G15 |
| SC-13 | Pause twice, then resume after deadline or readiness change. | Saved prior state not overwritten; invalid resume rejected with recovery guidance. | M15/M16; G14 |
| SC-14 | Request proof information, resubmit, then verify. | Old proof decision preserved; no final impact on rework; unique record issuance after accepted completion. | M11–M13; G17 |
| SC-15 | Proof rejected without a resolved rejection/dispute policy. | Dependent implementation remains blocked on PD-10; no test fixture silently chooses one contradictory source. | M14/M21; G14 |
| SC-16 | Cancel/fail mission, provider refund notification delayed. | Mission closed but refund still pending; evidence/history and reconciliation continue. | M17/M20; G10/G11 |
| SC-17 | Target change approval races a new contribution. | Commitment and target revision stay consistent; approval cannot erase already committed quantities/history. | M23; G29 |
| SC-18 | Transaction rolls back after writing state but before outbox commit. | No partial state/history/event; retry can execute once. | All rows; G13 |
| SC-19 | Org/volunteer reinstatement review begins. | Access remains denied until a fresh valid approval; historical approval timestamp does not restore rights. | O11/V08 |
| SC-20 | Unauthorized actor calls a valid transition or requests a cached idempotent response after revocation. | Authorization failure and no sensitive cached response; no state change. | All rows; G25 |

## Review coverage and limits

Organization: all seven declared states appear; 11 transition rows. Volunteer: all five application states appear; nine rows including enhanced-check review. Mission: all 17 declared states appear; 23 rows including target changes. Optional withdrawal, arbitrary terminal reopen and generic status-edit are not enabled by omission; they need reviewed transitions if approved as product behavior.

These tables supply a reviewable initial contract, not exhaustive closure of the complete plan. Foundation policy roles, definitive errors/event schema, schema migrations, SQL concurrency proofs, live provider validation and remaining aggregate catalogues are still outstanding.
