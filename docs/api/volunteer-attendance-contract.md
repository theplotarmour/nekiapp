# Volunteer, skills interest and attendance contracts

**Status:** P0 review draft, 2026-09-11. Adds 43 operations: 13 volunteer application/review, six skills-interest and 24 booking/attendance operations. Coverage is 217 of 324 operations, with [107 remaining](openapi-coverage.json). No service or approval workflow is implemented.

Authoring source: [contract_volunteers.py](../../tools/contract_volunteers.py). Sources: D7, [volunteer transitions V01–V09](../state-machines/volunteer-approval.md), [booking/attendance A01–A15](../state-machines/logistics-and-attendance.md), G08 and [authorization](authorization.md). Use the [shared reproduction commands](identity-contract.md).

## Application and scoped approval

Applications reference a home locality, skills, availability and SOP consent. Ownership comes from the current user; government-ID fields and client approval status are excluded. Identity verification remains `none` for MVP. Structured weekday/daypart tokens and limits are proposed contract defaults pending source/policy review.

Applicant views exclude restricted reviewer notes. Decisions bind the reviewed submission revision; approval requires a nonempty passing/approved-exception checklist. Rejection and information requests have separate required evidence or requested information. Resubmission preserves earlier decisions. Suspension must immediately deny participation and enqueue assignment/custody recovery; reopening review does not restore approval.

Enhanced checks bind mission, risk category, SOP revision and validity. They do not replace basic approval or automatically suspend the volunteer globally. The service must validate reviewer scope, consent, evidence ownership, validity and current eligibility. A well-formed ID or CLEARED outcome cannot prove any of those checks.

Skills registration creates an interest record with no contribution or impact. Operations demand is a scoped aggregate without private notes or identities. Consent, withdrawal/retention, taxonomy normalization and any suppression of small aggregates remain G08/privacy decisions. There is no MVP skills booking or payment flow.

## Booking and attendance

Public roles/slots expose safe requirements, display location and available places. Availability is not a reservation. The role's optional minimum age is a policy value, not an invented eligibility default. Booking and contribution-based TIME submission must use the same canonical transactional service and user/slot uniqueness constraints, even if callers use different routes or idempotency keys.

Booking requests precede assignments. REQUESTED/WAITLISTED requests cannot carry assignment IDs; CONFIRMED requests must. Joining a waitlist requires explicit consent and creates neither a contribution nor occupied booked capacity. Offer acceptance rechecks expiry, current approval, scoped checks and overlap while consuming its held place. Decline/cancel releases only the matching reservation and queues the next candidate under reviewed LD-03 policy.

Volunteer check-in/out capture client time, point, accuracy and device-reported mock status as evidence. Clients cannot submit verified seconds, verifier identity or a passed-geofence flag. Current assignment, server time/window, source 300 m geofence, accuracy policy and interval checks determine acceptance. Device flags are review signals, not misconduct proof. Requiring location in these capture branches is a draft wire choice; organizer exceptions have a separate evidence/policy command. QR remains conditional and unimplemented.

Organizer confirmation requires a reason, evidence, occurrence time and exception-policy reference. Verification/resolution binds the attendance revision and accepted interval; the server derives integer seconds under the approved cap/rounding policy. HOURS_VERIFIED responses require timestamps, a duration and a revision. The schema cannot compare timestamp order, derive the duration, validate an exception or establish verifier independence.

No-show decisions require slot-end/grace and absence of accepted attendance, serialized against late sync. Correction preserves the original decision and returns the interval for review. Hours disputes preserve earlier verification and create durable correction work when impact was already issued. Zero-hour acceptance, grace, cancellation cutoffs and interval policy remain CD-04/LD-04 decisions.

Assignment responses exclude captured GPS and other volunteers' contact details. Precise attendance evidence needs restricted retention and access controls. Offline actions stay pending until accepted and cannot retry blindly with a refreshed version. Suspension must prevent new private access and queued acceptance while preserving historical verified facts and safe custody recovery.

## Verification and outstanding gates

OpenAPI validation passes for 217 operations and 2,464 request/response/error examples. It rejects 164 negative schema cases and five query cases. The 29 new failures cover self-approval/KYC/ownership injection, reviewer-note exposure, unscoped checks, fabricated skills impact, waitlist assignment claims, GPS response leakage, client geofence/hours assertions, missing consent/evidence revisions and unsupported verified attendance.

Examples cover review branches, waitlisted/confirmed requests and verified attendance; they are shapes, not executed transitions. No database capacity lock, permission enforcement, geofence, mobile offline replay or verifier-independence test has run. Strict completeness fails with 107 operations untyped. P0 remains open; logistics, proof, impact and remaining transport/administration contracts follow.
