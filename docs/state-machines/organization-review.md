# Organization review transitions

**Status:** Review draft. [Shared command rules](README.md) apply to every row. Sources: data model §4.2 `org_status`; PRD FR-15/16; flows F7/F8; plan P2.1/G24/G25/G29.

Use existing states `APPLIED`, `UNDER_REVIEW`, `NEEDS_MORE_INFORMATION`, `VERIFIED`, `REJECTED`, `SUSPENDED`, `EXPIRED`. Display APPLIED as “Application submitted”; do not add a second persisted `PENDING_REVIEW` org state because UI says pending review. `verification_status` is a separate review projection, not an independent source of access rights (PD-01).

All rows require matching expected version and atomic history/audit/outbox under the shared rules. Applicant means server-established submission owner; owner-scoped document access is allowed even before verification, subject to G24 media policy.

| ID / basis | Command: from → to | Actor | Guards and evidence | Atomic effects; proposed event | Display; notification intent | Additional failures / decision |
|---|---|---|---|---|---|---|
| O01 Source | Submit: absent → APPLIED | Authenticated applicant | Required org details, owned processed documents, submission consent; unique live submission identity per PD-02 | Create org and applicant ownership, submission revision and review queue entry; `OrganizationApplied.v1` | “Application submitted”; applicant acknowledgement + ops queue | `ORG_APPLICATION_EXISTS`, `DOCUMENT_NOT_READY`; PD-02 |
| O02 Source | Begin review: APPLIED → UNDER_REVIEW | Scoped ops reviewer | Current submission revision; reviewer assignment | Record review start/reviewer; `OrganizationReviewStarted.v1` | “Under review”; applicant status, no push required | `ORG_STATE_CONFLICT`; PD-01 |
| O03 Source | Request information: UNDER_REVIEW → NEEDS_MORE_INFORMATION | Scoped ops reviewer | Checklist findings, requested fields/documents and safe explanation | Append decision tied to submission revision; `OrganizationInformationRequested.v1` | “More information needed”; applicant actionable request | `REVIEW_REASON_REQUIRED` |
| O04 Source | Resubmit: NEEDS_MORE_INFORMATION → APPLIED | Applicant | Requested fields resolved, new owned document revisions processed; no replacement of prior evidence | New submission revision; requeue; `OrganizationResubmitted.v1` | “Updated application submitted”; applicant + ops queue | `REQUESTED_INFORMATION_MISSING` |
| O05 Source | Verify: UNDER_REVIEW → VERIFIED | Scoped ops reviewer | Completed applicable checklist, current evidence, expiry/probation policy; org type does not imply tax eligibility | Append approval, record validity, grant approved org capability to established owner; update review projection; `OrganizationVerified.v1` | “Organization verified”; applicant | `ORG_REVIEW_INCOMPLETE`; PD-01/PD-03 |
| O06 Source | Reject: UNDER_REVIEW → REJECTED | Scoped ops reviewer | Reason, checklist and reviewed revision | Append rejection; no publication capability; `OrganizationRejected.v1` | “Application not approved” plus safe reason; applicant | `REVIEW_REASON_REQUIRED`; reapplication PD-02 |
| O07 Proposed | Reapply: REJECTED → APPLIED | Applicant | Policy permits reapplication; revised evidence and prior decision reference | Preserve identity/history; new submission revision and queue entry; `OrganizationReapplied.v1` | “Application resubmitted”; applicant + ops queue | `REAPPLICATION_NOT_ALLOWED`; PD-02 |
| O08 Source state; proposed effects | Suspend: VERIFIED → SUSPENDED | Scoped ops lead | Reason and case/evidence reference | Revoke current publication/participation capability; enqueue mission/participant recovery work; `OrganizationSuspended.v1` | “Organization suspended”; org + ops recovery queue; affected participants after scoped recovery decision | `SUSPENSION_REASON_REQUIRED`; PD-03/PD-04 |
| O09 Source state; proposed effects | Expire: VERIFIED → EXPIRED | Expiry service | Approved validity timestamp <= server now; version still current | Invalidate verified badge/capabilities, enqueue affected mission review; `OrganizationVerificationExpired.v1` | “Verification expired”; org renewal request + ops recovery queue | `VERIFICATION_NOT_EXPIRED`; PD-03/PD-04 |
| O10 Proposed | Request renewed review: EXPIRED → APPLIED | Applicant | Renewal policy, revised evidence and consent if required | Preserve prior verification; new submission/review cycle; `OrganizationRenewalSubmitted.v1` | “Renewal submitted”; applicant + ops queue | `RENEWAL_EVIDENCE_REQUIRED`; PD-03 |
| O11 Proposed | Permit reinstatement review: SUSPENDED → UNDER_REVIEW | Scoped ops lead | Case remediation evidence and reason; explicit policy allows review | Record reinstatement review; capabilities stay denied pending O05; `OrganizationReinstatementReviewStarted.v1` | “Reinstatement under review”; org + ops queue | `REINSTATEMENT_NOT_ALLOWED`; PD-03/PD-04 |

No direct rejected/expired/suspended-to-verified command. No public verified badge solely because historical `verified_at` is populated. Renewal-in-progress must not accidentally restore capabilities. Public history and applicant-facing messages exclude restricted review material.

## Required model reconciliation

- Bind applicant ownership server-side independently of org-admin approval; decide live-submission uniqueness and duplicate-organization handling (PD-02).
- Store submission/document revisions and append-only review decisions; a single `review_note` cannot be the full history.
- Define org status versus verification projection mapping, validity policy and revocation timestamps (PD-01/03).
- Suspension/expiry write immediate access denial with durable recovery intent. Async mission fan-out must be retryable; every new contribution/publish authorization reads current org eligibility even while fan-out is pending (PD-04).
- Financial settlement/refunds on suspension are separate reviewed workflows. Organization verification is not legal approval for NEKI to accept live funds or issue tax documentation.
