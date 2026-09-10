# Contribution lifecycle by type

**Status:** P0 review draft, NK-DOC-3.02. Sources: TDD §6.2, PRD FR-07/08/09/11, flows F1/F2/F3 and plan P3/P4/P6. [Shared command rules](README.md), [financial commands](payments-and-payouts.md) and [money invariants](money-invariants.md) apply. New semantics are proposals, not implemented or accepted schema.

Separate contribution intent, payment facts, physical execution, verified outcome and refund recovery. The current single `contribution_status` enum cannot faithfully represent partial refunds alongside execution. Proposed read contract exposes `lifecycle_status`, payment/refund summaries and `recovery_status` independently; source enum amendments await FD-02 and OpenAPI review. Final immutable records are separate from pending Activity.

All rows use expected version, scoped authorization, audit/history and durable events. Server-generated projections also dedupe the causative event. Different types cannot jump to another type's states. Default errors are `CONTRIBUTION_STATE_CONFLICT` plus shared authorization/version/evidence failures; extra failures appear below.

## Money

| ID / basis | Command: from → to | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failures / decision |
|---|---|---|---|---|---|---|
| C01 Source; proposed reviewed submission | Submit reviewed money: absent / INITIATED → PENDING_PAYMENT | Contributor | Online; final server-validated amount/fee disclosure, owner preferences/message revision, eligible money need and unique intent | P01 creates intent/reservation/attempt atomically; `ContributionPaymentPending.v1` | “Preparing payment”; owner | `NEED_CLOSED`, `DISCLOSURE_CHANGED`; CD-01 |
| C02 Source | Confirm: PENDING_PAYMENT / PAYMENT_FAILED / EXPIRED → CONFIRMED | Capture allocation service | P09/P10 facts and eligible locked allocation; expired/failed route only after approved late-success recovery, never automatic | One accepted allocation, confirmed timestamp and counters; `ContributionConfirmed.v1` (same event as P10, not a second effect) | “Contribution confirmed”; owner + scoped org feed | FD-01/04 |
| C03 Source | Fail local attempt: PENDING_PAYMENT → PAYMENT_FAILED | Reconciler | All attempts conclusively failed, no capture or unknown outcome | Record failed projection, release safe local reservation; `ContributionPaymentFailed.v1` | “Payment not completed”; owner | `PAYMENT_OUTCOME_UNKNOWN` |
| C04 Source | Expire local intent: PENDING_PAYMENT / PAYMENT_FAILED → EXPIRED | Expiry service | Intent deadline reached; close presentation; do not assert provider terminal state | P06 local closure/release, keep reconciliation work; `ContributionExpired.v1` | “Checkout expired” plus separate confirming/recovery state when needed; owner | `DEADLINE_NOT_REACHED`; FD-04 |
| C05 Source; proposed meaning | Allocate to evidenced org payout: CONFIRMED → ALLOCATED | Payout projection handler | Evidenced paid principal allocation covering required amount under partial-payout policy | Store payout links/timeline, no new capture/credit; `ContributionAllocated.v1` | “Sent to organization”; owner after evidence | CD-02; G16 |
| C06 Source | Fulfil: ALLOCATED → FULFILLED | Execution projection handler | Accepted mission execution/delivery facts attributable to contribution; actual quantity | Fulfilment evidence/time; `ContributionFulfilled.v1` | “Delivery reported; verification pending”; owner | `FULFILMENT_EVIDENCE_MISSING`; CD-02 |
| C07 Source | Verify: FULFILLED → VERIFIED | Verification projection handler | Approved current proof/outcome revision and contribution attribution | Verification history; `ContributionVerified.v1` | “Outcome verified”; owner status | `OUTCOME_NOT_VERIFIED`; G17/G18 |

Money execution before the manual payout is reconciled is a real possible ordering. Do not hide delivery evidence while C05 waits. CD-02 must resolve whether ALLOCATED remains a sequential state or becomes a separate financial projection before implementation. No strict enum sequence may discard real evidence.

Partial refund does not move a still-active contribution to terminal REFUNDED. Track requested/processed/refundable amounts and execution independently. A full refund before execution closes contribution eligibility under FD-02; a later full refund cannot erase delivered/verified history. Capture outside eligibility surfaces P11 recovery even if contribution lifecycle remains EXPIRED/CANCELLED. Skills interest never enters these money states.

## Items

| ID / basis | Command: from → to | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failures / decision |
|---|---|---|---|---|---|---|
| C08 Source | Confirm items: absent / INITIATED → CONFIRMED | Contributor | Current item need/condition/food policy; owned processed photos, serviceable address/slot or allowed drop-off; sufficient need/capacity under locks | Contribution + shipment + capacity reservation + dispatch work once; `ItemContributionConfirmed.v1` | Pickup/drop-off confirmation; owner + dispatch | `ITEM_NOT_ELIGIBLE`, `SLOT_FULL`, `AREA_UNSERVICEABLE` |
| C09 Source | Schedule: CONFIRMED → SCHEDULED | Shipment projection handler | Accepted slot/dispatch scheduling evidence | Store shipment/slot revision; `ContributionScheduled.v1` | “Pickup scheduled”; owner | `SHIPMENT_NOT_SCHEDULED` |
| C10 Source | Begin movement: SCHEDULED → IN_TRANSIT | Shipment projection handler | Accepted pickup/custody transfer by authorized volunteer; client queue is not evidence | Movement projection/time; `ContributionInTransit.v1` | “Items picked up”; owner | `PICKUP_NOT_ACCEPTED` |
| C11 Source; proposed drop-off edge | Deliver: IN_TRANSIT / CONFIRMED / SCHEDULED → DELIVERED | Shipment/drop-off handler | IN_TRANSIT needs accepted destination receipt; other states only for allowed drop-off with org acknowledgement, not a fake courier | Delivered quantity/evidence; `ItemContributionDelivered.v1` | “Items received; verification pending”; owner + org | `RECEIPT_REQUIRED`, `DROPOFF_NOT_ALLOWED` |
| C12 Source | Verify: DELIVERED → VERIFIED | Verification handler | Accepted relevant proof revision, actual quantities and consent | Verification projection and attribution; `ContributionVerified.v1` | “Delivery verified”; owner status | `OUTCOME_NOT_VERIFIED` |
| C13 Source; proposed bounded set | Cancel: CONFIRMED / SCHEDULED → CANCELLED | Contributor before cutoff or scoped ops exception | No pickup/custody transfer; cancellation policy and reason; serialize against pickup | Release exact capacity/need reservation, cancel shipment/dispatch intent; `ItemContributionCancelled.v1` | “Pickup cancelled”; owner + dispatch | `CUSTODY_ALREADY_TRANSFERRED`; CD-03 |
| C14 Source concept | Reschedule: CONFIRMED / SCHEDULED → same | Contributor before assignment or scoped ops | New slot/serviceability eligible, old assignment policy, reason for exception | Acquire new/release old capacity and shipment revision atomically; `ItemContributionRescheduled.v1` | “Pickup rescheduled” with date/window; owner + dispatch | `SLOT_FULL`, `RESCHEDULE_NOT_ALLOWED`; CD-03 |

After pickup, cancellation is a custody-return case in the shipment contract, not C13. The original contribution remains traceable until return/disposition evidence is accepted. Partial received quantities must not count as the originally promised quantity without verification.

## Time

| ID / basis | Command: from → to | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failures / decision |
|---|---|---|---|---|---|---|
| C15 Source | Confirm booking: absent / INITIATED → CONFIRMED | Approved volunteer | Current D7 approval, scoped enhanced checks, eligible mission/role/slot, no disallowed overlap/duplicate; online capacity lock | Assignment + contribution + slot reservation once; `TimeContributionConfirmed.v1` | “You're booked”; volunteer + org roster | `VOLUNTEER_NOT_APPROVED`, `SLOT_FULL`, `BOOKING_CONFLICT`; CD-04 |
| C16 Source | Publish upcoming: CONFIRMED → UPCOMING | Assignment handler | Accepted assignment and scheduled window | Upcoming projection/reminder intents; `ContributionUpcoming.v1` | Date/time/location; volunteer | `ASSIGNMENT_NOT_CONFIRMED` |
| C17 Source | Check in: UPCOMING → CHECKED_IN | Attendance handler | Accepted server check-in (geofence or authorized organizer exception); current assignment/approval; offline client action still pending | Store accepted attendance evidence/times; `ContributionCheckedIn.v1` | “Checked in”; volunteer + org | `CHECKIN_NOT_ACCEPTED`; attendance policy |
| C18 Source | Check out: CHECKED_IN → CHECKED_OUT | Attendance handler | Accepted checkout or audited organizer correction; valid interval/cap | Store claimed/accepted times and provisional hours; `ContributionCheckedOut.v1` | “Hours awaiting verification”; volunteer + org | `ATTENDANCE_INTERVAL_INVALID` |
| C19 Source | Verify hours: CHECKED_OUT → VERIFIED | Attendance verification handler | Organizer verification and bounded actual hours, dispute resolution if needed | Verified hours projection exactly once; `ContributionVerified.v1` | “Hours verified”; volunteer | `HOURS_NOT_VERIFIED` |
| C20 Source | Cancel booking: CONFIRMED / UPCOMING → CANCELLED | Volunteer within cutoff or org/ops exception | No check-in; approved cutoff/exception and reason | Cancel assignment/release slot; queue waitlist offer under policy; `TimeContributionCancelled.v1` | “Booking cancelled”; volunteer + org | `CANCELLATION_CUTOFF_PASSED`; CD-04 |
| C21 Source | Record no-show: UPCOMING → NO_SHOW | Scoped org/ops or reviewed attendance service | Slot ended plus reviewed grace/attendance evidence; no accepted check-in | No-show decision, no verified hours; `ContributionNoShowRecorded.v1` | “Attendance not recorded” with correction/support path; volunteer + org | `NO_SHOW_NOT_ESTABLISHED`; CD-04 |

Waitlisting is an assignment interest/offer state, not a confirmed contribution or verified service. Promotion requires current eligibility and user acceptance if the proposed offer policy is adopted; C15 occurs only after accepted booking. Reminders do not change contribution lifecycle. Check-in/out, no-show correction and organizer adjustments need the detailed assignment contract (NK-DOC-3.03).

## Shared completion and skills boundary

| ID / basis | Command: from → to | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failures / decision |
|---|---|---|---|---|---|---|
| C22 Source | Issue final record: VERIFIED → COMPLETED | Impact service | Verified completion criteria, unique contribution record, canonical attribution and correction rules | Append immutable record or durable issuance protocol with atomic completion; `ContributionCompleted.v1` | “Your verified impact record is ready”; owner only after record accessible | `IMPACT_EVIDENCE_INCOMPLETE`; G17/G19 |

Do not emit `contribution_completed` analytics on checkout success or pickup booking: use the appropriate confirmed event; final completion is C22. Pending Activity may display transaction/assignment evidence without a final immutable record. MVP certificate metadata follows verified hours; PDF remains NEXT.

SKILL/REGISTERED in the source enum remains reserved pending G08. Proposed `skill_interests` CRUD with optional mission context, consent and no fabricated contribution/impact record belongs to API/schema closure. No production skills contribution endpoint is authorized by this draft.

## Open contribution decisions

| ID | Resolution proposed / missing policy | Accountable role |
|---|---|---|
| CD-01 | Submit financially immutable intent on final Review confirmation; before that use an owner draft/quote. Resolve old F1 order-before-Review timing, anonymous/message edits and quote expiry. | Product + backend |
| CD-02 | Prefer independent allocation/payout, execution and refund projections over strict money enum ordering. Define partial payout/fulfilment attribution and final completion requirements. | Backend + product/Finance |
| CD-03 | Item prohibitions/food expiry, cutoff exceptions, partial receipt/returns and custody recovery. No invented numeric eligibility limits. | Ops + product |
| CD-04 | Overlap, waitlist offer/expiry, cancellation/no-show grace, QR adoption, attendance correction and appeal. Preserve source 12-hour cutoff as assumption until reviewed. | Ops + product |

All CD decisions OPEN. This slice completes the initial type-level draft, not acceptance of all dependent assignment/shipment/impact policies.
