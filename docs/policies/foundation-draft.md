# Foundation operating policy draft

Prepared 2026-09-13 for P0. This is a concrete operating proposal and implementation boundary, **not approved legal advice, provider activation, a signed SOP or an assigned operating team**. D1–D7 remain locked. Numeric legal/financial/eligibility/retention thresholds cannot be inferred from illustrative fixtures.

## Approval record and enforcement

Every policy revision records a stable key, revision, scope, proposed values, author, reviewer/decision, effective date, source evidence and superseded revision. Operational commands bind the effective revision at authorization and retain the decision's evidence reference. A future revision does not rewrite historical consent, allocation or approval facts. Missing, expired or conflicting policies produce a specific unavailable/review-required result; a client-selected value never activates a policy.

Public browsing can proceed independently of approvals for contributing, booking, home pickup or live money. Staging uses explicit synthetic fixtures. Test identities, deterministic OTP, fake provider outcomes and synthetic evidence cannot be configured as production adapters.

| Policy | Proposed operating rule | Values/decision still needed | Linked decisions |
|---|---|---|---|
| Organization onboarding | Applicant owns submissions until reviewed membership is granted. Preserve submission and document revisions, reviewer findings and reasons. Reinstatement always requires a current approval. | Named review lead; duplicate-org resolution; renewal validity and probation rules; reapplication timing | PD-01–04 |
| Volunteer eligibility | Phone + profile + application + ops approval. Persist SOP consent revisions. Home pickup requires a scoped current enhanced-check result; suspension stops new assignments and raises custody recovery. No government-ID/KYC. | Minimum age/attestation and exceptions; check evidence, validity and escalation; reapplication/withdrawal timing | PD-05–06, D7 |
| Mission readiness | Each need has its own units, target, permitted commitment ceiling and approved readiness minimum. Lock relevant capacity/funds when authorizing. Readiness uses a consistent snapshot; a money target reaching its limit does not close unrelated item/time needs. | Partial minimums, permitted overfill, reservation expiry and late-capture treatment, deadlines and pause/resume policy | PD-07–09, PD-12–13, G15 |
| Mission changes/recovery | Keep immutable reviewed publication/target revisions. Revalidate participant commitments when material targets, location or deadlines change. Cancellation leaves financial/custody recovery outstanding until separately resolved. | Materiality and participant consent rules; who can approve each change; terminal recovery outcomes | PD-11–13 |
| Pickup and dispatch | Authorize only against approved zone geometry, slot capacity, current volunteer eligibility and assignment. Restrict home/contact details to the currently authorized operational scope. Preserve custody through failures and handoff. | Exact service polygons, capacity, booking/cancellation cutoffs, staffed hours, escalation delays and contact consent | Logistics decisions, D4 |
| Attendance | Record server receipt and reported action time separately; pending offline actions are not verified attendance. Accepted check-out intervals are reviewed before hours/impact issuance. | Check-in/out windows, missed checkout evidence, no-show policy, waitlist offer lifetime and appeal | Attendance decisions |
| Proof and impact | Preserve submission/check/decision revisions; distinguish information requests from rejection/case review. Illustrations cannot qualify as proof. Only accepted source evidence creates final impact; corrections append and preserve originals. | Required evidence by mission risk; missing metadata handling; appeal owner/timing; attribution/deduplication wording | PD-10, proof/impact decisions |
| Money/refunds | Server binds reviewed allocation/fee facts and provider identifiers. A timeout is uncertain, never automatic failure or permission to repeat a financial request. Refund eligibility and amount need explicit authorized evidence. | Qualified review of NEKI's legal role; refund grounds/windows; fee/subsidy handling; reserves and reconciliation rules | Financial decisions, D2/D5 |
| Manual payouts | Draft, independent approval, transfer evidence and reconciliation are separate facts. Bind bank/economic revision; changes invalidate prior approval. Record operator, recipient, reference and contribution allocations. | Cadence, amount thresholds, reserve amounts, operator/approver roster, bank-change verification and failed/returned transfer handling | Financial decisions, D3 |
| Receipts/tax documents | Payment acknowledgement and eligible organization tax documentation are separate document types. Do not label a generic acknowledgement as an 80G certificate. | Advisor-approved entity/receipt wording, issuer responsibilities and document requirements | D3 legal gate |
| Support/moderation | Cases have owner, category, restricted evidence, reasoned resolution and participant-visible status. No generic arbitrary state edit. Surface staffing/unavailable status honestly. | Named queue owner, response/escalation targets, after-hours coverage, appeals and emergency redirection wording | G25/G29 |
| Consent/privacy/deletion | Version consent documents and purpose. Separate mutable identifying projections from immutable transaction/impact facts. Legal holds and retained records require reviewed grounds and scoped access. | Reviewed ToS/privacy/SOP versions; retention durations per class, legal grounds/holds, processors/regions, deletion deadlines | G21–24 |

## Data-class retention register for review

| Data class | Operational purpose | Minimization and deletion design | Required decision |
|---|---|---|---|
| Phone/profile/session/device | Authentication and account recovery | Hash refresh/OTP material, revoke credentials immediately, retain minimal abuse evidence separately | Profile/device/abuse retention and deletion basis |
| Precise addresses/contact | Authorized pickup and delivery | Keep separate from public location; revoke access on assignment end; never put in shared events/analytics | Address reuse consent, expiry and case/hold exceptions |
| Live GPS, route cache, offline pings | Active assignment tracking | Inventory device, API, Redis, DB, logs, backups and provider caches; purge each store, not only Redis | Collection cadence, TTL, stale display and disclosure precision |
| Private documents and raw media | Organization/proof review | Quarantine, purpose-bound access, immutable revision keys; separate public derivatives | Retention by purpose, consent withdrawal, rejected-file deletion and legal holds |
| Review/consent/case history | Explain authorized decisions | Immutable evidence references with separately controlled identity; redact public projections | Access, retention and appeal/hold grounds |
| Payment/refund/payout facts | Financial reconciliation and records | Immutable amount/provider/allocation facts; restrict bank and identity joins | Advisor-approved periods, mandatory fields and deletion exceptions |
| Impact canonical payload | Integrity and corrections | Exclude mutable name/contact; append corrections; identity mapping separately governed | Residual identifiability, permitted disclosure and retention |
| Events/receipts/audit | Reliable processing and accountability | Allowlist event payloads and safe failure codes; no serialized private model rows | Retention/archival by event class and incident need |
| Analytics/crash/search logs | Product reliability and aggregate analysis | Prohibit phone, address, exact GPS, signed URLs and free-text evidence; aggregate where possible | Consent basis, retention, processor regions and opt-out behavior |
| Backups/exports | Recovery and authorized reporting | Restrict access, expire copies, carry deletion/hold instructions through restores | PITR window, export expiry and restoration suppression workflow |

No blanket 24-hour, 90-day or three-year rule is accepted from old example tables. Deletion jobs must enforce the approved class-specific register and prove restore behavior before P8 closure.

## Roles and decision separation

Contributor access is owner-scoped; a volunteer's eligibility does not imply an org/ops role. Organization administrators act only within current reviewed membership. Ops agents can prepare/review within an assigned scope; ops leads authorize the designated escalations. Finance authorization is separate from ordinary ops access. A super-admin label is not a reason to bypass financial separation of duties, suspension or private-media purpose checks.

Consequential decisions carry reason and expected version. An author must not approve their own payout; replaying an old authorization cannot make a changed bank revision valid. Step-up scope/lifetime and role roster require security/operations review. Synthetic test roles are not real operator assignments.

## Required handoff from founder/team

Record the named product/operations decision owner, Finance approver, qualified advisor, provider onboarding owner and target dates. Resolve the values above in the existing [transition decision register](../state-machines/review-decisions.md) and linked financial/logistics/proof catalogues, then update authoritative contracts. External messages, onboarding purchases and funds are not performed by authoring this draft.

Until then: **operating policy draft delivered; approval and actual staffing remain open**. P0 cannot be declared passed from this document alone.
