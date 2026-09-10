"""Organization application, portal, moderation and mission-management schemas."""

from copy import deepcopy

from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import COORD, HTTPS, QUANTITY, array

ORG_STATUS = enum("APPLIED", "UNDER_REVIEW", "NEEDS_MORE_INFORMATION", "VERIFIED", "REJECTED", "SUSPENDED", "EXPIRED")
ORG_TYPE = enum("NGO", "TRUST", "SOCIETY", "SECTION_8", "COMMUNITY_GROUP", "SCHOOL", "OTHER")
MISSION_STATUS = enum("DRAFT", "PENDING_REVIEW", "REJECTED", "PUBLISHED", "FUNDING", "RECRUITING", "ACTIVE", "READY", "IN_PROGRESS", "DELIVERED", "VERIFICATION", "COMPLETED", "PAUSED", "CANCELLED", "FAILED", "EXPIRED", "DISPUTED")


def schemas():
    s = {}
    details = {"name": text(1, 160), "legal_name": text(1, 200), "org_type": ORG_TYPE,
               "registration_number": nullable(text(1, 100)), "contact_email": text(3, 254, format="email"),
               "contact_phone": text(8, 16, pattern=r"^\+[1-9][0-9]{7,14}$"), "description": text(1, 4000),
               "website": nullable(HTTPS), "hq_address_id": ID}
    s["OrgApply"] = obj({**details, "document_ids": {**array(ID, 20), "minItems": 1, "uniqueItems": True}, "consent_receipt_id": ID})
    s["OrgApplicationUpdate"] = obj({**details, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["OrgApplication"] = obj({**details, "id": ID, "status": ORG_STATUS, "submission_revision_id": ID,
                                "document_ids": array(ID, 20), "requested_information": array(text(1, 200), 30),
                                "safe_decision_reason": nullable(text(1, 1000)), "version": VERSION})
    s["OrgResubmit"] = obj({"expected_version": VERSION, "document_ids": {**array(ID, 20), "uniqueItems": True},
                             "consent_receipt_id": ID, "prior_decision_id": ID})
    document = {"kind": enum("registration", "pan", "12a", "80g", "fcra", "bank_proof", "other"), "media_id": ID,
                "issued_at": nullable(TIME), "expires_at": nullable(TIME)}
    s["OrgDocumentCreate"] = obj(document)
    s["OrgDocument"] = obj({**document, "id": ID, "processing_status": enum("PENDING", "PROCESSING", "READY", "REJECTED"), "version": VERSION})
    s["OrgDocumentPage"] = page(ref("OrgDocument"))
    s["OrgProfile"] = obj({**details, "id": ID, "status": ORG_STATUS, "logo_media_id": nullable(ID), "version": VERSION})
    s["OrgProfileUpdate"] = obj({"expected_version": VERSION, "description": text(1, 4000), "website": nullable(HTTPS),
                                 "contact_email": text(3, 254, format="email"), "contact_phone": details["contact_phone"],
                                 "logo_media_id": nullable(ID)}, ["expected_version"], minProperties=2)
    s["OrgSettings"] = obj({"operational_contact_email": text(3, 254, format="email"), "timezone": enum("Asia/Kolkata"), "version": VERSION})
    s["OrgSettingsUpdate"] = obj({"operational_contact_email": text(3, 254, format="email"), "expected_version": VERSION})
    s["BankChangeRequest"] = obj({"expected_version": VERSION, "account_holder": text(1, 200),
                                   "account_number": text(6, 34, writeOnly=True), "bank_code": text(1, 20),
                                   "proof_media_id": ID, "reason": text(1, 1000)})
    s["BankChangeSummary"] = obj({"id": ID, "status": enum("REQUESTED", "UNDER_REVIEW", "APPROVED", "REJECTED"),
                                   "account_holder": text(1, 200), "account_masked": text(5, 30, pattern=r"^\*+[0-9]{4}$"),
                                   "bank_code": text(1, 20), "requested_at": TIME, "version": VERSION})
    s["BankChangePage"] = page(ref("BankChangeSummary"))
    s["OrgDashboard"] = obj({"active_missions": integer(), "contributions_today": integer(), "pending_proof": integer(),
                               "generated_at": TIME, "org_status": ORG_STATUS})
    s["MissionNeedInput"] = {"oneOf": [
        obj({"type": enum("MONEY"), "need_id": ID, "target_paise": integer(1, 9007199254740991), "currency": enum("INR")}),
        obj({"type": enum("ITEM"), "need_id": ID, "item_type_id": ID, "label": text(1, 120),
             "target_quantity": {**QUANTITY, "not": {"enum": ["0", "0.0", "0.00"]}}, "unit": text(1, 30),
             "accepted_conditions": {**array(enum("NEW", "GOOD", "FAIR"), 3), "minItems": 1, "uniqueItems": True}, "allow_dropoff": BOOL}),
        obj({"type": enum("TIME"), "need_id": ID, "role_id": ID, "label": text(1, 120), "requirements": text(1, 1000)}),
    ], "discriminator": {"propertyName": "type"}}
    s["MissionSlotInput"] = obj({"slot_id": ID, "role_id": ID, "starts_at": TIME, "ends_at": TIME,
                                  "capacity": integer(1, 100000), "location_address_id": ID})
    proof = obj({"photos_min": integer(0, 50), "acknowledgement": BOOL, "beneficiary_count": BOOL, "geotag": BOOL})
    draft = {"title": text(1, 90), "category_id": ID, "subcategory_id": nullable(ID), "summary": text(0, 300),
             "story": text(0, 20000), "location_name": text(1, 160), "location_point": COORD,
             "location_address_id": ID, "deadline_at": nullable(TIME), "starts_at": nullable(TIME),
             "hero_media_id": nullable(ID), "gallery_media_ids": {**array(ID, 20), "uniqueItems": True},
             "allow_partial": BOOL, "proof_requirements": proof}
    s["MissionDraftCreate"] = obj({"title": text(1, 90)})
    s["MissionDraftUpdate"] = obj({**draft, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["MissionEditor"] = obj({"id": ID, "organization_id": ID, "status": MISSION_STATUS, "version": VERSION,
                               "submission_revision_id": nullable(ID), "fields": obj(draft, ["title"]),
                               "needs": array(ref("MissionNeedInput"), 50), "slots": array(ref("MissionSlotInput"), 200),
                               "has_contributions": BOOL, "target_edit_mode": enum("draft", "change_request_only")})
    s["MissionEditorPage"] = page(ref("MissionEditor"))
    s["MissionNeedsUpdate"] = obj({"expected_version": VERSION, "needs": array(ref("MissionNeedInput"), 50)})
    s["MissionSlotsUpdate"] = obj({"expected_version": VERSION, "slots": array(ref("MissionSlotInput"), 200)})
    s["MissionSubmission"] = obj({"expected_version": VERSION, "reviewed_draft_version": VERSION})
    s["MissionCommand"] = obj({"expected_version": VERSION, "reason": text(1, 1000)})
    s["MissionEvidenceCommand"] = obj({"expected_version": VERSION, "reason": text(1, 1000),
                                        "evidence_ids": {**array(ID, 50), "minItems": 1, "uniqueItems": True}})
    s["MissionReadinessCommand"] = obj({"expected_version": VERSION, "reason": text(1, 1000),
                                         "readiness_snapshot_id": ID, "partial_fulfilment_decision_id": nullable(ID)})
    s["ReviewHistoryEntry"] = obj({"id": ID, "submission_revision_id": ID, "decision": enum("APPROVED", "NEEDS_MORE_INFORMATION", "REJECTED"),
                                    "safe_reason": text(1, 1000), "requested_information": array(text(1, 200), 30), "decided_at": TIME})
    s["ReviewHistoryPage"] = page(ref("ReviewHistoryEntry"))
    changes = {"needs": array(ref("MissionNeedInput"), 50), "deadline_at": TIME, "location_address_id": ID}
    s["MissionChangeCreate"] = obj({"expected_version": VERSION, "reason": text(1, 1000), "proposed_changes": obj(changes, [], minProperties=1)})
    s["MissionChange"] = obj({"id": ID, "mission_id": ID, "status": enum("REQUESTED", "APPROVED", "REJECTED"),
                               "base_mission_version": VERSION, "reason": text(1, 1000), "proposed_changes": obj(changes, [], minProperties=1), "version": VERSION})
    s["MissionChangePage"] = page(ref("MissionChange"))
    s["OrgContributionSummary"] = obj({"id": ID, "mission_id": ID, "type": enum("MONEY", "ITEM", "TIME"),
                                        "contributor_display": text(1, 160), "is_anonymous": BOOL, "confirmed_at": nullable(TIME),
                                        "amount_paise": nullable(integer(0, 9007199254740991)), "quantity": nullable(QUANTITY), "unit": nullable(text(1, 30))})
    s["OrgContributionPage"] = page(ref("OrgContributionSummary"))
    s["OrgRosterEntry"] = obj({"assignment_id": ID, "volunteer_display": text(1, 160), "role_id": ID, "slot_id": ID,
                                "status": enum("CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "HOURS_VERIFIED", "HOURS_DISPUTED", "NO_SHOW", "CANCELLED_BY_VOLUNTEER", "CANCELLED_BY_ORG"),
                                "verified_seconds": nullable(integer()), "version": VERSION})
    s["OrgRosterPage"] = page(ref("OrgRosterEntry"))
    update = {"body": text(1, 4000), "media_ids": {**array(ID, 10), "uniqueItems": True}, "kind": enum("progress", "delivery", "thanks")}
    s["OrgMissionUpdateCreate"] = obj(update)
    s["OrgMissionUpdateEdit"] = obj({**update, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["OrgMissionUpdate"] = obj({**update, "id": ID, "mission_id": ID, "moderation_status": enum("PENDING", "PUBLISHED", "REJECTED"), "published_at": nullable(TIME), "version": VERSION})
    s["OrgImpactSummary"] = obj({"verified_missions": integer(), "verified_volunteer_seconds": integer(),
                                  "beneficiaries_reported_verified": nullable(integer()), "beneficiary_scope": enum("mission_reported_not_unique_people"), "generated_at": TIME})
    s["ReviewChecklistEntry"] = {"oneOf": [
        obj({"check_id": text(1, 80), "outcome": enum("PASS"), "evidence_id": ID, "exception_decision_id": {"type": "null"}}),
        obj({"check_id": text(1, 80), "outcome": enum("EXCEPTION_APPROVED"), "evidence_id": ID, "exception_decision_id": ID}),
    ]}
    s["OrgReview"] = obj({"application": ref("OrgApplication"), "documents": array(ref("OrgDocument"), 20),
                            "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["OrgReviewPage"] = page(ref("OrgReview"))
    s["MissionReview"] = obj({"mission": ref("MissionEditor"), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["MissionReviewPage"] = page(ref("MissionReview"))
    for name, approve in [("OrgReviewDecision", "VERIFY"), ("MissionReviewDecision", "PUBLISH")]:
        base = {"expected_version": VERSION, "submission_revision_id": ID, "safe_reason": text(1, 1000)}
        s[name] = {"oneOf": [
            obj({**base, "decision": enum(approve), "checklist": {**array(ref("ReviewChecklistEntry"), 100), "minItems": 1}}),
            obj({**base, "decision": enum("NEEDS_MORE_INFORMATION"), "requested_information": {**array(text(1, 200), 30), "minItems": 1}}),
            obj({**base, "decision": enum("REJECT"), "evidence_ids": {**array(ID, 50), "minItems": 1}}),
        ], "discriminator": {"propertyName": "decision"}}
    s["MissionChangeDecision"] = obj({"expected_version": VERSION, "expected_mission_version": VERSION, "decision": enum("APPROVE", "REJECT"),
                                       "reason": text(1, 1000), "participant_notification_plan_id": nullable(ID), "evidence_ids": {**array(ID, 50), "minItems": 1}})
    s["MissionDisputeDecision"] = obj({"expected_version": VERSION, "case_id": ID, "decision": enum("REQUEST_REWORK", "FAIL"),
                                        "reason": text(1, 1000), "evidence_ids": {**array(ID, 50), "minItems": 1}})
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, code="200", errors=()):
        d[op] = (request, code, response, list(errors), effect)
    add("apply_organization", "OrgApply", "OrgApplication", "Create server-owned application before org_admin grant.", "201")
    add("get_org_application", None, "OrgApplication", "Applicant-safe submission view; no restricted reviewer notes.")
    add("edit_org_application", "OrgApplicationUpdate", "OrgApplication", "Edit permitted rework revision; status/approval fields never writable.")
    for op in ("resubmit_org_application", "reapply_organization", "renew_org_application"):
        add(op, "OrgResubmit", "OrgApplication", "Preserve previous review and attach new submission cycle under approved reapplication policy.")
    add("list_own_org_documents", None, "OrgDocumentPage", "Only own application documents; media read authorization separate.")
    add("attach_org_document", "OrgDocumentCreate", "OrgDocument", "Attach owned processed org-document media to current submission.", "201", ["MEDIA_NOT_READY"])
    add("get_own_org_document", None, "OrgDocument", "Metadata only, no permanent private URL.")
    add("get_org_profile", None, "OrgProfile", "Read own profile; not a public serializer.")
    add("update_org_profile", "OrgProfileUpdate", "OrgProfile", "Update allowed profile fields; legal/bank identity requires reviewed workflow.")
    add("get_org_settings", None, "OrgSettings", "Read scoped operational preferences.")
    add("update_org_settings", "OrgSettingsUpdate", "OrgSettings", "Update operational contact, not Finance recipient.")
    add("request_bank_change", "BankChangeRequest", "BankChangeSummary", "Persist encrypted/restricted bank request, invalidate approval as policy requires; does not verify recipient.", "201")
    add("list_bank_change_requests", None, "BankChangePage", "Only own masked bank change history.")
    add("get_org_dashboard", None, "OrgDashboard", "Current scoped operational counts, not fabricated impact.")
    add("list_org_missions", None, "MissionEditorPage", "Read own draft/live missions.")
    add("create_mission_draft", "MissionDraftCreate", "MissionEditor", "Create server-scoped draft; no publication entitlement implied.", "201")
    add("get_mission_editor", None, "MissionEditor", "Own editor view includes draft fields, not other org data.")
    add("edit_mission_draft", "MissionDraftUpdate", "MissionEditor", "Only permitted draft revision; lock fields needing change requests after contributions.")
    add("remove_unsubmitted_draft", None, None, "Remove unsubmitted unused draft; retain required audit.", "204")
    add("edit_draft_needs", "MissionNeedsUpdate", "MissionEditor", "Validate need ownership/units and absence of protected commitments before replacing draft needs.")
    add("edit_draft_slots", "MissionSlotsUpdate", "MissionEditor", "Validate intervals/roles and committed capacity before draft replacement.")
    add("submit_mission", "MissionSubmission", "MissionEditor", "Check complete quantified need and current org verification; freeze reviewed revision.", errors=["MISSION_INCOMPLETE", "ORG_NOT_ELIGIBLE"])
    add("get_mission_feedback", None, "ReviewHistoryPage", "Applicant-safe moderation decisions; no restricted notes.")
    add("revise_rejected_mission", "MissionCommand", "MissionEditor", "Open allowed new draft cycle, preserving prior rejection.")
    add("request_mission_change", "MissionChangeCreate", "MissionChange", "Persist before/after request; never directly mutate live target.", "201")
    add("list_mission_changes", None, "MissionChangePage", "Read own mission change history.")
    add("mark_mission_ready", "MissionReadinessCommand", "MissionEditor", "Revalidate locked per-need snapshot/partial decision; no flag-only readiness.")
    add("start_mission", "MissionEvidenceCommand", "MissionEditor", "Require READY and accepted start evidence.")
    add("declare_mission_delivered", "MissionEvidenceCommand", "MissionEditor", "Actual delivery evidence, not verification or final impact.")
    for op in ("pause_org_mission", "resume_org_mission", "cancel_org_mission", "pause_ops_mission", "resume_ops_mission", "cancel_ops_mission"):
        add(op, "MissionCommand", "MissionEditor", "Explicit actor-scoped lifecycle command; preserve pause/recovery history and recheck current guards.")
    add("list_org_contributions", None, "OrgContributionPage", "Honor anonymous display; no donor phone/address/provider credentials.")
    add("list_org_roster", None, "OrgRosterPage", "Only own mission attendance; no home/GPS disclosure.")
    add("create_mission_update", "OrgMissionUpdateCreate", "OrgMissionUpdate", "Create moderated update with owned media.", "201")
    add("edit_mission_update", "OrgMissionUpdateEdit", "OrgMissionUpdate", "Versioned update rework with moderation history.")
    add("get_org_impact", None, "OrgImpactSummary", "Verified effective outcomes only; beneficiaries are mission reports, not unique persons.")
    for op, schema in [("list_org_review_queue", "OrgReviewPage"), ("get_org_review", "OrgReview"),
                       ("list_mission_review_queue", "MissionReviewPage"), ("get_mission_review", "MissionReview")]:
        add(op, None, schema, "Restricted reviewer scope and evidence, separate from applicant view.")
    add("start_org_review", "VersionCommand", "OrgReview", "Assign/review exact current submission revision.")
    add("decide_org_application", "OrgReviewDecision", "OrgReview", "Apply only explicit review decision; checklist must satisfy current policy.")
    for op in ("suspend_organization", "reopen_org_review"):
        add(op, "MissionEvidenceCommand", "OrgReview", "Reasoned org access/reinstatement review with case evidence; no automatic verification.")
    add("decide_mission_review", "MissionReviewDecision", "MissionReview", "Current eligible org and reviewed submission; no arbitrary status assignment.")
    add("decide_mission_change", "MissionChangeDecision", "MissionChange", "Serialize approval against mission commitments; preserve notifications/consent and before/after revision.")
    add("fail_mission", "MissionEvidenceCommand", "MissionEditor", "Record failure and durable financial/custody recovery; never imply refund completed.")
    add("resolve_mission_dispute", "MissionDisputeDecision", "MissionEditor", "Reviewed case disposition for rework/failure; do not erase verified history.")
    return d


def examples():
    fields = {"name": "Example Organization", "legal_name": "Example Organization", "org_type": "NGO", "registration_number": "SYNTHETIC-001",
              "contact_email": "ops@example.invalid", "contact_phone": "+919000000001", "description": "Synthetic organization application",
              "website": None, "hq_address_id": UUID}
    app = {**fields, "id": UUID, "status": "APPLIED", "submission_revision_id": UUID, "document_ids": [UUID],
           "requested_information": [], "safe_decision_reason": None, "version": 1}
    document = {"kind": "registration", "media_id": UUID, "issued_at": None, "expires_at": None}
    editor = {"id": UUID, "organization_id": UUID, "status": "DRAFT", "version": 1, "submission_revision_id": None,
              "fields": {"title": "Books for Delhi students"}, "needs": [], "slots": [], "has_contributions": False, "target_edit_mode": "draft"}
    need = {"type": "MONEY", "need_id": UUID, "target_paise": 100000, "currency": "INR"}
    slot = {"slot_id": UUID, "role_id": UUID, "starts_at": "2026-09-12T04:30:00Z", "ends_at": "2026-09-12T06:30:00Z", "capacity": 10, "location_address_id": UUID}
    review = {"expected_version": 1, "submission_revision_id": UUID, "safe_reason": "Documents checked", "decision": "VERIFY",
              "checklist": [{"check_id": "registration", "outcome": "PASS", "evidence_id": UUID, "exception_decision_id": None}]}
    change = {"id": UUID, "mission_id": UUID, "status": "REQUESTED", "base_mission_version": 1,
              "reason": "Revised delivery timeline", "proposed_changes": {"deadline_at": "2026-10-10T12:00:00Z"}, "version": 1}
    update = {"body": "Preparing supplies", "media_ids": [], "kind": "progress"}
    e = {"OrgApply": {**fields, "document_ids": [UUID], "consent_receipt_id": UUID}, "OrgApplication": app,
         "OrgApplicationUpdate": {"expected_version": 1, "description": "Updated description"},
         "OrgResubmit": {"expected_version": 1, "document_ids": [UUID], "consent_receipt_id": UUID, "prior_decision_id": UUID},
         "OrgDocumentCreate": document, "OrgDocument": {**document, "id": UUID, "processing_status": "READY", "version": 1},
         "OrgProfile": {**fields, "id": UUID, "status": "VERIFIED", "logo_media_id": None, "version": 1},
         "OrgProfileUpdate": {"expected_version": 1, "description": "Updated description"},
         "OrgSettings": {"operational_contact_email": "ops@example.invalid", "timezone": "Asia/Kolkata", "version": 1},
         "OrgSettingsUpdate": {"operational_contact_email": "ops@example.invalid", "expected_version": 1},
         "BankChangeRequest": {"expected_version": 1, "account_holder": "Example Organization", "account_number": "000000000000", "bank_code": "EXAMPLE",
                               "proof_media_id": UUID, "reason": "Synthetic bank change example"},
         "BankChangeSummary": {"id": UUID, "status": "REQUESTED", "account_holder": "Example Organization", "account_masked": "********0000", "bank_code": "EXAMPLE", "requested_at": NOW, "version": 1},
         "OrgDashboard": {"active_missions": 0, "contributions_today": 0, "pending_proof": 0, "generated_at": NOW, "org_status": "VERIFIED"},
         "MissionDraftCreate": {"title": editor["fields"]["title"]}, "MissionDraftUpdate": {"expected_version": 1, "summary": "Updated summary"},
         "MissionEditor": editor, "MissionNeedInput": need, "MissionSlotInput": slot,
         "MissionNeedsUpdate": {"expected_version": 1, "needs": [need]}, "MissionSlotsUpdate": {"expected_version": 1, "slots": [slot]},
         "MissionSubmission": {"expected_version": 1, "reviewed_draft_version": 1}, "MissionCommand": {"expected_version": 1, "reason": "Operational review"},
         "MissionEvidenceCommand": {"expected_version": 1, "reason": "Evidence reviewed", "evidence_ids": [UUID]},
         "MissionReadinessCommand": {"expected_version": 1, "reason": "Needs reviewed", "readiness_snapshot_id": UUID, "partial_fulfilment_decision_id": None},
         "ReviewHistoryEntry": {"id": UUID, "submission_revision_id": UUID, "decision": "NEEDS_MORE_INFORMATION", "safe_reason": "Update required",
                                "requested_information": ["Updated acknowledgement"], "decided_at": NOW},
         "MissionChangeCreate": {"expected_version": 1, "reason": change["reason"], "proposed_changes": change["proposed_changes"]}, "MissionChange": change,
         "OrgContributionSummary": {"id": UUID, "mission_id": UUID, "type": "MONEY", "contributor_display": "Anonymous contributor", "is_anonymous": True,
                                    "confirmed_at": NOW, "amount_paise": 100000, "quantity": None, "unit": None},
         "OrgRosterEntry": {"assignment_id": UUID, "volunteer_display": "Example volunteer", "role_id": UUID, "slot_id": UUID,
                            "status": "CONFIRMED", "verified_seconds": None, "version": 1},
         "OrgMissionUpdateCreate": update, "OrgMissionUpdateEdit": {"expected_version": 1, "body": "Updated progress"},
         "OrgMissionUpdate": {**update, "id": UUID, "mission_id": UUID, "moderation_status": "PENDING", "published_at": None, "version": 1},
         "OrgImpactSummary": {"verified_missions": 0, "verified_volunteer_seconds": 0, "beneficiaries_reported_verified": None,
                              "beneficiary_scope": "mission_reported_not_unique_people", "generated_at": NOW},
         "OrgReview": {"application": app, "documents": [{**document, "id": UUID, "processing_status": "READY", "version": 1}], "restricted_notes": [], "version": 1},
         "MissionReview": {"mission": editor, "restricted_notes": [], "version": 1}, "OrgReviewDecision": review,
         "MissionReviewDecision": {**review, "decision": "PUBLISH"},
         "MissionChangeDecision": {"expected_version": 1, "expected_mission_version": 1, "decision": "APPROVE", "reason": "Impact reviewed",
                                   "participant_notification_plan_id": UUID, "evidence_ids": [UUID]},
         "MissionDisputeDecision": {"expected_version": 1, "case_id": UUID, "decision": "REQUEST_REWORK", "reason": "Additional evidence needed", "evidence_ids": [UUID]}}
    for name, member in [("OrgDocumentPage", "OrgDocument"), ("BankChangePage", "BankChangeSummary"), ("MissionEditorPage", "MissionEditor"),
                         ("ReviewHistoryPage", "ReviewHistoryEntry"), ("MissionChangePage", "MissionChange"), ("OrgContributionPage", "OrgContributionSummary"),
                         ("OrgRosterPage", "OrgRosterEntry"), ("OrgReviewPage", "OrgReview"), ("MissionReviewPage", "MissionReview")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def negative_cases():
    e = examples(); cases = []
    for schema, key, value, label in [
        ("OrgApply", "status", "VERIFIED", "self-verified application"),
        ("OrgApply", "owner_user_id", UUID, "applicant ownership injection"),
        ("OrgApplication", "restricted_notes", ["private"], "review notes in applicant response"),
        ("OrgProfileUpdate", "settlement_bank_ref", "private", "bank edit bypass"),
        ("BankChangeSummary", "account_number", "000000000000", "raw bank number response leak"),
        ("BankChangeSummary", "account_masked", "000000000000", "unmasked account"),
        ("MissionDraftCreate", "organization_id", UUID, "cross-org draft injection"),
        ("MissionDraftUpdate", "status", "PUBLISHED", "publication bypass"),
        ("MissionDraftUpdate", "raised_amount_paise", 100000, "counter injection"),
        ("MissionNeedInput", "target_paise", 0, "zero target"),
        ("MissionNeedInput", "target_paise", 1.5, "fractional money target"),
        ("MissionCommand", "target_status", "COMPLETED", "arbitrary transition"),
        ("OrgReviewDecision", "decision", "SUSPEND", "wrong review action"),
        ("OrgReviewDecision", "checklist", [], "empty approval evidence"),
        ("OrgContributionSummary", "contributor_phone", "private", "donor phone in org feed"),
        ("OrgRosterEntry", "checkin_point", {"latitude": 28, "longitude": 77}, "GPS in roster"),
        ("MissionEvidenceCommand", "evidence_ids", [], "manual override without evidence"),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, label))
    cases.append(("MissionDraftUpdate", {"expected_version": 1}, "empty draft patch"))
    for outcome in ("FAIL", "EXCEPTION_APPROVED"):
        payload = deepcopy(e["OrgReviewDecision"])
        payload["checklist"][0]["outcome"] = outcome
        cases.append(("OrgReviewDecision", payload, "failed or unapproved exception in approval checklist"))
    return cases
