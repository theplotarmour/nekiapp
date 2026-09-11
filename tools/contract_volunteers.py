"""Volunteer review, skills interest and attendance draft contracts."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import COORD, array
from contract_cases import evidence_ids


def schemas():
    s = {}
    availability = obj({"weekdays": {**array(enum("mon", "tue", "wed", "thu", "fri", "sat", "sun"), 7), "minItems": 1, "uniqueItems": True},
        "slots": {**array(enum("morning", "afternoon", "evening"), 3), "minItems": 1, "uniqueItems": True}})
    fields = {"home_locality_id": ID, "skills": {**array(text(1, 80), 30), "uniqueItems": True}, "availability": availability}
    s["VolunteerApply"] = obj({**fields, "sop_consent_receipt_id": ID})
    s["VolunteerInformationUpdate"] = obj({**fields, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["VolunteerResubmit"] = obj({"expected_version": VERSION, "prior_decision_id": ID, "sop_consent_receipt_id": ID})
    s["VolunteerApplication"] = obj({**fields, "id": ID, "status": enum("PENDING_REVIEW", "NEEDS_MORE_INFORMATION", "APPROVED", "REJECTED", "SUSPENDED"),
        "submission_revision_id": ID, "identity_verification": enum("none"), "safe_reason": nullable(text(1, 1000)), "version": VERSION})
    s["VolunteerReview"] = obj({"application": ref("VolunteerApplication"), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["VolunteerReviewPage"] = page(ref("VolunteerReview"))
    decision = {"expected_version": VERSION, "submission_revision_id": ID, "safe_reason": text(1, 1000)}
    s["VolunteerDecision"] = {"oneOf": [
        obj({**decision, "decision": enum("APPROVE"), "checklist": {**array(ref("ReviewChecklistEntry"), 100), "minItems": 1}}),
        obj({**decision, "decision": enum("NEEDS_MORE_INFORMATION"), "requested_information": {**array(text(1, 300), 30), "minItems": 1}}),
        obj({**decision, "decision": enum("REJECT"), "evidence_ids": evidence_ids()}),
    ], "discriminator": {"propertyName": "decision"}}
    s["VolunteerReviewHistory"] = page(obj({"id": ID, "submission_revision_id": ID, "decision": enum("APPROVE", "NEEDS_MORE_INFORMATION", "REJECT", "SUSPEND", "REOPEN"),
        "safe_reason": text(1, 1000), "requested_information": array(text(1, 300), 30), "decided_at": TIME}))
    base = {"expected_version": VERSION, "reason": text(1, 1000)}
    evidenced = {**base, "evidence_ids": evidence_ids()}
    s["VolunteerAccessDecision"] = obj({**evidenced, "case_id": ID})
    check_scope = obj({"mission_id": ID, "risk_category_id": ID, "sop_revision_id": ID})
    check = {"scope": check_scope, "outcome": enum("CLEARED", "NEEDS_REVIEW", "NOT_CLEARED"), "valid_until": TIME, "safe_reason": text(1, 1000)}
    s["EnhancedCheckRecord"] = obj({**check, "expected_version": VERSION, "evidence_ids": evidence_ids()})
    s["EnhancedCheckView"] = obj({**check, "id": ID, "version": VERSION})
    s["EnhancedCheckPage"] = page(ref("EnhancedCheckView"))
    interest = {"skill": text(1, 120), "mission_id": nullable(ID), "availability": availability, "note": nullable(text(1, 1000))}
    s["SkillInterestCreate"] = obj({**interest, "consent_receipt_id": ID})
    s["SkillInterestUpdate"] = obj({**interest, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["SkillInterest"] = obj({**interest, "id": ID, "status": enum("REGISTERED"), "created_at": TIME, "version": VERSION,
        "contribution_created": {"type": "boolean", "const": False}, "impact_created": {"type": "boolean", "const": False}})
    s["SkillInterestPage"] = page(ref("SkillInterest"))
    s["SkillDemandPage"] = page(obj({"skill": text(1, 120), "interest_count": integer(), "as_of": TIME}))
    s["VolunteerRolePublic"] = obj({"id": ID, "mission_id": ID, "name": text(1, 120), "requirements": text(1, 2000),
        "enhanced_check_required": BOOL, "minimum_age": nullable(integer(1, 100))})
    s["VolunteerRolePage"] = page(ref("VolunteerRolePublic"))
    s["VolunteerSlotPublic"] = obj({"id": ID, "mission_id": ID, "role_id": ID, "starts_at": TIME, "ends_at": TIME,
        "location_label": text(1, 160), "available_places": integer(), "waitlist_available": BOOL, "version": VERSION})
    s["VolunteerSlotPage"] = page(ref("VolunteerSlotPublic"))
    booking = {"role_id": ID, "slot_id": ID, "expected_slot_version": VERSION, "sop_consent_receipt_id": ID}
    s["VolunteerBook"] = obj(booking)
    s["VolunteerWaitlist"] = obj({**booking, "waitlist_consent_receipt_id": ID})
    s["BookingRequest"] = obj({"id": ID, "mission_id": ID, "role_id": ID, "slot_id": ID,
        "status": enum("REQUESTED", "WAITLISTED", "CONFIRMED", "CANCELLED_BY_VOLUNTEER", "CANCELLED_BY_ORG"),
        "assignment_id": nullable(ID), "created_at": TIME, "version": VERSION}, allOf=[{
            "if": {"properties": {"status": {"const": "CONFIRMED"}}}, "then": {"properties": {"assignment_id": ID}},
            "else": {"properties": {"assignment_id": {"type": "null"}}}}])
    s["BookingRequestPage"] = page(ref("BookingRequest"))
    s["SlotOffer"] = obj({"id": ID, "booking_request_id": ID, "slot_id": ID, "expires_at": TIME,
        "status": enum("ACTIVE", "ACCEPTED", "DECLINED", "EXPIRED"), "version": VERSION})
    s["SlotOfferPage"] = page(ref("SlotOffer"))
    s["SlotOfferAccept"] = obj({"expected_version": VERSION, "sop_consent_receipt_id": ID})
    s["AttendanceCommand"] = obj(base)
    s["AssignmentView"] = obj({"id": ID, "contribution_id": ID, "mission_id": ID, "role_id": ID, "slot_id": ID,
        "status": enum("CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "HOURS_VERIFIED", "HOURS_DISPUTED", "NO_SHOW", "CANCELLED_BY_VOLUNTEER", "CANCELLED_BY_ORG"),
        "starts_at": TIME, "ends_at": TIME, "location_label": text(1, 160), "checked_in_at": nullable(TIME), "checked_out_at": nullable(TIME),
        "provisional_seconds": nullable(integer()), "verified_seconds": nullable(integer()), "attendance_revision_id": nullable(ID), "version": VERSION},
        allOf=[{"if": {"properties": {"status": {"const": "HOURS_VERIFIED"}}}, "then": {"properties": {
            "checked_in_at": TIME, "checked_out_at": TIME, "verified_seconds": integer(), "attendance_revision_id": ID}}}])
    s["AssignmentPage"] = page(ref("AssignmentView"))
    s["AttendanceCapture"] = obj({"expected_version": VERSION, "client_recorded_at": TIME, "point": COORD,
        "accuracy_m": {"type": "number", "minimum": 0, "maximum": 100000}, "is_mock_reported": BOOL})
    s["OrganizerAttendance"] = obj({**evidenced, "occurred_at": TIME, "exception_policy_id": ID})
    interval = {"starts_at": TIME, "ends_at": TIME}
    s["AttendanceVerify"] = obj({**evidenced, "attendance_revision_id": ID, "accepted_interval": obj(interval), "policy_revision_id": ID})
    s["AttendanceDispute"] = obj({**evidenced, "attendance_revision_id": ID})
    s["AttendanceNoShow"] = obj({**evidenced, "policy_revision_id": ID})
    s["AttendanceCorrection"] = obj({**evidenced, "case_id": ID, "accepted_interval": obj(interval), "policy_revision_id": ID})
    s["AttendanceResolution"] = obj({**evidenced, "case_id": ID, "attendance_revision_id": ID, "accepted_interval": obj(interval), "policy_revision_id": ID})
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, status="200", errors=()):
        d[op] = (request, status, response, list(errors), effect)
    add("submit_volunteer_application", "VolunteerApply", "VolunteerApplication", "Bind unique user application and consent after OTP/profile checks; no government-ID collection.", "201")
    add("get_volunteer_application", None, "VolunteerApplication", "Applicant-safe current revision; approval is separate from enhanced clearance.")
    add("update_volunteer_information", "VolunteerInformationUpdate", "VolunteerApplication", "Permitted rework revision only; no approval/capability input.")
    for op in ("resubmit_volunteer_application", "reapply_volunteer"):
        add(op, "VolunteerResubmit", "VolunteerApplication", "New permitted submission cycle preserving prior decision and consent history.")
    add("get_volunteer_review_history", None, "VolunteerReviewHistory", "Safe append-only applicant feedback excluding internal evidence/notes.")
    add("get_enhanced_check_status", None, "EnhancedCheckPage", "Own scoped safe check outcomes; no blanket global clearance.")
    add("list_volunteer_review_queue", None, "VolunteerReviewPage", "Scoped reviewer queue.")
    add("get_volunteer_review", None, "VolunteerReview", "Current review revision and restricted notes for assigned reviewer.")
    add("decide_volunteer_application", "VolunteerDecision", "VolunteerReview", "Current revision/checklist/consent required; approval atomically grants capability.")
    for op in ("suspend_volunteer", "reopen_volunteer_review"):
        add(op, "VolunteerAccessDecision", "VolunteerReview", "Versioned case decision; suspension denies access immediately with durable assignment recovery; reopening does not restore approval.")
    add("record_enhanced_check", "EnhancedCheckRecord", "EnhancedCheckView", "Record mission/risk/SOP-scoped outcome and validity with evidence; not a global suspension decision.", "201")
    add("create_skill_interest", "SkillInterestCreate", "SkillInterest", "Register consented interest only; no contribution, booking or impact.", "201")
    add("list_skill_interests", None, "SkillInterestPage", "Own interest records.")
    add("get_skill_interest", None, "SkillInterest", "Owner-scoped interest detail.")
    add("update_skill_interest", "SkillInterestUpdate", "SkillInterest", "Versioned owner edit under consent policy.")
    add("delete_skill_interest", None, None, "Remove active interest under retention policy without fabricating contribution cancellation.", "204")
    add("list_skill_demand", None, "SkillDemandPage", "Scoped aggregate interest demand; no private notes or contributor identities.")
    add("list_volunteer_roles", None, "VolunteerRolePage", "Browse published eligible roles without volunteer approval.")
    add("list_volunteer_slots", None, "VolunteerSlotPage", "Safe slot availability, never proof of reservation.")
    add("book_volunteer_slot", "VolunteerBook", "BookingRequest", "Same canonical TIME booking service as contribution creation; serialize role/slot capacity and approval checks.", "201", ["VOLUNTEER_INELIGIBLE", "SLOT_FULL", "BOOKING_EXISTS"])
    add("join_waitlist", "VolunteerWaitlist", "BookingRequest", "Explicit consented waitlist request; no contribution or booked capacity until accepted offer.", "201", ["VOLUNTEER_INELIGIBLE", "WAITLIST_NOT_ALLOWED"])
    add("list_own_assignments", None, "AssignmentPage", "Owner assignments without stored GPS evidence.")
    add("get_assignment", None, "AssignmentView", "Current participant scope; own attendance summary, not arbitrary volunteer private data.")
    for op in ("cancel_assignment", "cancel_org_assignment"):
        add(op, "AttendanceCommand", "AssignmentView", "Actor determines cancellation category; serialize cutoff/custody/check-in and release capacity once.", errors=["CANCELLATION_NOT_ALLOWED"])
    add("list_booking_requests", None, "BookingRequestPage", "Owner requests including waitlisted states distinct from assignments.")
    add("get_booking_request", None, "BookingRequest", "Owner request projection; no false confirmed assignment.")
    add("cancel_booking_request", "AttendanceCommand", "BookingRequest", "Cancel open request and active offer under shared locks.", errors=["CANCELLATION_NOT_ALLOWED"])
    add("list_slot_offers", None, "SlotOfferPage", "Owner offers; expiry checked on server when accepted.")
    add("accept_slot_offer", "SlotOfferAccept", "AssignmentView", "Recheck unexpired offer, approval, enhanced clearance and overlap; consume held place and create contribution/assignment once.", errors=["OFFER_EXPIRED", "VOLUNTEER_INELIGIBLE"])
    add("decline_slot_offer", "AttendanceCommand", "SlotOffer", "Close active offer and release its held capacity exactly once.")
    for op in ("check_in", "check_out"):
        add(op, "AttendanceCapture", "AssignmentView", "Accept only current assigned volunteer and valid attendance window; geofence/interval/SOP checks. Client queued location is evidence, not acceptance.", errors=["CHECKIN_NOT_ELIGIBLE", "ATTENDANCE_INTERVAL_INVALID"])
    add("dispute_hours", "AttendanceDispute", "AssignmentView", "Preserve previous hours decision; block new final issuance and route existing record to correction.")
    for op in ("confirm_org_checkin", "confirm_org_checkout"):
        add(op, "OrganizerAttendance", "AssignmentView", "Reasoned scoped organizer exception with evidence; no automatic full-slot credit.", errors=["ATTENDANCE_INTERVAL_INVALID"])
    add("verify_attendance", "AttendanceVerify", "AssignmentView", "Independent verifier accepts actual interval under cap/rounding policy; derive integer seconds server-side.")
    add("record_no_show", "AttendanceNoShow", "AssignmentView", "Slot end/grace and no accepted check-in under lock; never infer from missing client sync alone.")
    add("correct_attendance", "AttendanceCorrection", "AssignmentView", "Append evidenced no-show correction and route interval to verification; preserve original decision.")
    add("resolve_hours_dispute", "AttendanceResolution", "AssignmentView", "Independent case resolution creates new interval decision and durable impact correction if previously issued.")
    return d


def examples():
    availability = {"weekdays": ["sat", "sun"], "slots": ["morning"]}
    fields = {"home_locality_id": UUID, "skills": ["packing"], "availability": availability}
    application = {**fields, "id": UUID, "status": "PENDING_REVIEW", "submission_revision_id": UUID, "identity_verification": "none", "safe_reason": None, "version": 1}
    base = {"expected_version": 1, "reason": "Evidence reviewed"}; evidence = {**base, "evidence_ids": [UUID]}
    interval = {"starts_at": "2026-09-12T04:30:00Z", "ends_at": "2026-09-12T06:30:00Z"}
    check = {"scope": {"mission_id": UUID, "risk_category_id": UUID, "sop_revision_id": UUID}, "outcome": "CLEARED", "valid_until": "2026-10-12T00:00:00Z", "safe_reason": "Scoped check completed"}
    interest = {"skill": "packing", "mission_id": None, "availability": availability, "note": None}
    booking = {"role_id": UUID, "slot_id": UUID, "expected_slot_version": 1, "sop_consent_receipt_id": UUID}
    assignment = {"id": UUID, "contribution_id": UUID, "mission_id": UUID, "role_id": UUID, "slot_id": UUID, "status": "CONFIRMED", **interval,
        "location_label": "Mission activity location", "checked_in_at": None, "checked_out_at": None, "provisional_seconds": None,
        "verified_seconds": None, "attendance_revision_id": None, "version": 1}
    e = {"VolunteerApply": {**fields, "sop_consent_receipt_id": UUID}, "VolunteerInformationUpdate": {"expected_version": 1, "skills": ["packing", "teaching"]},
        "VolunteerResubmit": {"expected_version": 1, "prior_decision_id": UUID, "sop_consent_receipt_id": UUID}, "VolunteerApplication": application,
        "VolunteerReview": {"application": application, "restricted_notes": [], "version": 1},
        "VolunteerDecision": {"expected_version": 1, "submission_revision_id": UUID, "safe_reason": "Application checked", "decision": "APPROVE",
            "checklist": [{"check_id": "sop", "outcome": "PASS", "evidence_id": UUID, "exception_decision_id": None}]},
        "VolunteerReviewHistory": {"items": [], "next_cursor": None, "has_more": False}, "VolunteerAccessDecision": {**evidence, "case_id": UUID},
        "EnhancedCheckRecord": {**check, "expected_version": 1, "evidence_ids": [UUID]}, "EnhancedCheckView": {**check, "id": UUID, "version": 1},
        "SkillInterestCreate": {**interest, "consent_receipt_id": UUID}, "SkillInterestUpdate": {"expected_version": 1, "note": "Available weekends"},
        "SkillInterest": {**interest, "id": UUID, "status": "REGISTERED", "created_at": NOW, "version": 1, "contribution_created": False, "impact_created": False},
        "SkillDemandPage": {"items": [{"skill": "packing", "interest_count": 10, "as_of": NOW}], "next_cursor": None, "has_more": False},
        "VolunteerRolePublic": {"id": UUID, "mission_id": UUID, "name": "Packing volunteer", "requirements": "Follow the packing SOP", "enhanced_check_required": False, "minimum_age": None},
        "VolunteerSlotPublic": {"id": UUID, "mission_id": UUID, "role_id": UUID, **interval, "location_label": "Mission activity location", "available_places": 2, "waitlist_available": True, "version": 1},
        "VolunteerBook": booking, "VolunteerWaitlist": {**booking, "waitlist_consent_receipt_id": UUID},
        "BookingRequest": {"id": UUID, "mission_id": UUID, "role_id": UUID, "slot_id": UUID, "status": "REQUESTED", "assignment_id": None, "created_at": NOW, "version": 1},
        "SlotOffer": {"id": UUID, "booking_request_id": UUID, "slot_id": UUID, "expires_at": "2026-09-12T00:00:00Z", "status": "ACTIVE", "version": 1},
        "SlotOfferAccept": {"expected_version": 1, "sop_consent_receipt_id": UUID}, "AttendanceCommand": base, "AssignmentView": assignment,
        "AttendanceCapture": {"expected_version": 1, "client_recorded_at": NOW, "point": {"latitude": 28.6, "longitude": 77.2}, "accuracy_m": 20, "is_mock_reported": False},
        "OrganizerAttendance": {**evidence, "occurred_at": NOW, "exception_policy_id": UUID},
        "AttendanceVerify": {**evidence, "attendance_revision_id": UUID, "accepted_interval": interval, "policy_revision_id": UUID},
        "AttendanceDispute": {**evidence, "attendance_revision_id": UUID}, "AttendanceNoShow": {**evidence, "policy_revision_id": UUID},
        "AttendanceCorrection": {**evidence, "case_id": UUID, "accepted_interval": interval, "policy_revision_id": UUID},
        "AttendanceResolution": {**evidence, "case_id": UUID, "attendance_revision_id": UUID, "accepted_interval": interval, "policy_revision_id": UUID}}
    for name, member in [("VolunteerReviewPage", "VolunteerReview"), ("EnhancedCheckPage", "EnhancedCheckView"), ("SkillInterestPage", "SkillInterest"),
                         ("VolunteerRolePage", "VolunteerRolePublic"), ("VolunteerSlotPage", "VolunteerSlotPublic"), ("BookingRequestPage", "BookingRequest"),
                         ("SlotOfferPage", "SlotOffer"), ("AssignmentPage", "AssignmentView")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples(); base = {"expected_version": 1, "submission_revision_id": UUID, "safe_reason": "Further review"}
    return {"VolunteerDecision": {"information": {**base, "decision": "NEEDS_MORE_INFORMATION", "requested_information": ["Update availability"]},
        "rejected": {**base, "decision": "REJECT", "evidence_ids": [UUID]}}, "BookingRequest": {
        "waitlisted": {**e["BookingRequest"], "status": "WAITLISTED"}, "confirmed": {**e["BookingRequest"], "status": "CONFIRMED", "assignment_id": UUID}},
        "AssignmentView": {"verified": {**e["AssignmentView"], "status": "HOURS_VERIFIED", "checked_in_at": "2026-09-12T04:30:00Z",
            "checked_out_at": "2026-09-12T06:30:00Z", "provisional_seconds": 7200, "verified_seconds": 7200, "attendance_revision_id": UUID}}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [
        ("VolunteerApply", "status", "APPROVED"), ("VolunteerApply", "government_id", "private"),
        ("VolunteerApply", "owner_user_id", UUID), ("VolunteerApplication", "identity_verification", "kyc"),
        ("VolunteerApplication", "restricted_notes", ["internal"]), ("VolunteerDecision", "checklist", []),
        ("EnhancedCheckRecord", "scope", {}), ("SkillInterest", "impact_created", True), ("SkillInterest", "contribution_created", True),
        ("SkillInterestCreate", "amount_paise", 100), ("VolunteerSlotPublic", "volunteer_phone", "private"),
        ("VolunteerBook", "user_id", UUID), ("VolunteerBook", "status", "CONFIRMED"),
        ("BookingRequest", "status", "CONFIRMED"), ("BookingRequest", "assignment_id", UUID),
        ("AssignmentView", "checkin_point", {"latitude": 28, "longitude": 77}),
        ("AssignmentView", "status", "HOURS_VERIFIED"),
        ("AttendanceCapture", "accuracy_m", -1), ("AttendanceCapture", "verified_seconds", 7200),
        ("AttendanceCapture", "geofence_passed", True), ("OrganizerAttendance", "evidence_ids", []),
        ("AttendanceVerify", "verified_by", UUID), ("AttendanceVerify", "verified_seconds", 7200),
        ("AttendanceResolution", "impact_record_status", "COMPLETED"), ("AttendanceCommand", "target_status", "HOURS_VERIFIED"),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid scope/proof/status field"))
    for schema, key in [("VolunteerApply", "sop_consent_receipt_id"), ("VolunteerWaitlist", "waitlist_consent_receipt_id"),
                        ("AttendanceVerify", "attendance_revision_id"), ("AttendanceResolution", "case_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing consent or evidence revision"))
    return cases
