# Volunteer application and approval transitions

**Status:** Review draft. [Shared command rules](README.md) apply to every row. Sources: D7; PRD FR-09/16; data model §4.6; flows F3/F9; plan G14/G25/G29.

Use existing states `PENDING_REVIEW`, `NEEDS_MORE_INFORMATION`, `APPROVED`, `REJECTED`, `SUSPENDED`. An unsent local form is not an approved volunteer or a new server status. `identity_verification=none` remains MVP scope; no government-ID/KYC collection is introduced.

Every row checks expected version and atomically writes history/audit/outbox. Volunteer approval is separate from assignment lifecycle and from mission-specific enhanced-check clearance.

| ID / basis | Command: from → to | Actor | Guards and evidence | Atomic effects; proposed event | Display; notification intent | Additional failures / decision |
|---|---|---|---|---|---|---|
| V01 Source | Submit: absent → PENDING_REVIEW | Authenticated user | OTP/basic profile; availability, home area, skills and versioned SOP consent; unique user application | Create application/submission revision, queue review; `VolunteerApplicationSubmitted.v1` | “Application under review”; applicant + ops queue | `VOLUNTEER_APPLICATION_EXISTS`, `CONSENT_REQUIRED`; PD-05 |
| V02 Source state; proposed edge | Request information: PENDING_REVIEW → NEEDS_MORE_INFORMATION | Scoped ops reviewer | Requested information and safe reason tied to reviewed revision | Append review decision; `VolunteerInformationRequested.v1` | “More information needed”; applicant request | `REVIEW_REASON_REQUIRED` |
| V03 Source state; proposed edge | Resubmit: NEEDS_MORE_INFORMATION → PENDING_REVIEW | Applicant | Requested information supplied, revised consent if required | New revision, preserve prior decision, requeue; `VolunteerApplicationResubmitted.v1` | “Updated application under review”; applicant + ops queue | `REQUESTED_INFORMATION_MISSING`; PD-05 |
| V04 Source | Approve: PENDING_REVIEW → APPROVED | Scoped ops reviewer | Current reviewed revision, required basic checks and consent | Append approval and grant volunteer capability; `VolunteerApproved.v1` | “You're approved to volunteer”; applicant | `VOLUNTEER_REVIEW_INCOMPLETE`; PD-05/PD-06 |
| V05 Source | Reject: PENDING_REVIEW → REJECTED | Scoped ops reviewer | Decision reason and reviewed evidence | Append rejection; no volunteer capability; `VolunteerRejected.v1` | “Application not approved” plus safe explanation; applicant | `REVIEW_REASON_REQUIRED` |
| V06 Proposed | Reapply: REJECTED → PENDING_REVIEW | Applicant | Reapplication policy allows; revised evidence | Reuse application identity, append new submission cycle; `VolunteerReapplied.v1` | “Application resubmitted”; applicant + ops queue | `REAPPLICATION_NOT_ALLOWED`; PD-05 |
| V07 Source state; proposed effects | Suspend: APPROVED → SUSPENDED | Scoped ops lead | Reason/case evidence | Deny current booking/assignment access, revoke role capability and create active-assignment recovery intent; `VolunteerSuspended.v1` | “Volunteer access suspended”; volunteer + dispatch recovery queue | `SUSPENSION_REASON_REQUIRED`; PD-04/PD-06 |
| V08 Proposed | Reopen review: SUSPENDED → PENDING_REVIEW | Scoped ops lead | Remediation and reinstatement policy; safe explanation | New review cycle; keep capability revoked until V04; `VolunteerReinstatementReviewStarted.v1` | “Reinstatement under review”; volunteer + ops queue | `REINSTATEMENT_NOT_ALLOWED`; PD-05/PD-06 |
| V09 Source concept; proposed command | Record enhanced check: APPROVED → APPROVED | Scoped ops reviewer | Mission/risk scope, current SOP revision, evidence and outcome | Versioned enhanced-check decision separate from base approval; `VolunteerEnhancedCheckRecorded.v1` | “Additional check completed” or “Additional review needed”; volunteer safe outcome + relevant dispatch queue | `ENHANCED_CHECK_EVIDENCE_REQUIRED`; PD-06 |

## Authorization and recovery contract

- Browse before approval. Booking, waitlist promotion and pickup assignment require current APPROVED status plus role/slot/mission eligibility and the required enhanced check. A stale token role or cached screen is insufficient.
- Enhanced-check failure does not silently become global suspension. Deny the applicable high-risk assignment; the approved policy determines whether a separate V07 is needed (PD-06).
- Reassignment and suspension must conflict safely with assignment creation. After suspension commits, the former volunteer cannot obtain new private pickup data or have queued commands automatically accepted. Offline UI must show rejected/pending work honestly.
- Handling a volunteer already carrying donated items requires a dispatch safety handoff policy (PD-04). Do not treat access revocation as evidence that physical custody has transferred.
- Existing verified hours/history remain historical facts; suspension does not rewrite impact. Corrections need the separate impact contract.

## Required model reconciliation

Keep the existing unique `user_id` application identity; append submission/review cycles instead of overwriting `reviewed_by/review_note`. Add consent document/version, approval/revocation history, and a scoped enhanced-check record with validity and policy provenance. The existing single `enhanced_check_status` flag cannot prove every assignment's clearance. SOP changes, voluntary withdrawal, and profile changes that trigger renewed review need PD-05 decisions before implementation.
