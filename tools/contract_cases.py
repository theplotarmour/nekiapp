"""Draft case, dispute and refund contracts; no provider side effects."""

from copy import deepcopy
from contract_identity import ID, NOW, TIME, UUID, VERSION, enum, nullable, obj, page, ref, text
from contract_discovery import array
from contract_contributions import PAISE, POSITIVE_PAISE


def evidence_ids():
    return {**array(ID, 50), "minItems": 1, "uniqueItems": True}


def schemas():
    s = {}
    subject = {"oneOf": [obj({"type": enum(kind), "id": ID}) for kind in
                         ("contribution", "payment", "shipment", "assignment", "mission")]
               + [obj({"type": enum("account")})], "discriminator": {"propertyName": "type"}}
    s["CaseSubject"] = subject
    s["CaseCreate"] = obj({"subject": ref("CaseSubject"), "category": enum("support", "payment", "delivery", "attendance", "outcome", "privacy"),
        "description": text(1, 4000), "evidence_media_ids": {**array(ID, 20), "uniqueItems": True}})
    s["CaseOwnerView"] = obj({"id": ID, "subject": ref("CaseSubject"), "category": enum("support", "payment", "delivery", "attendance", "outcome", "privacy"),
        "description": text(1, 4000), "status": enum("OPEN", "UNDER_REVIEW", "AWAITING_INFORMATION", "RESOLVED", "CLOSED"),
        "safe_resolution": nullable(text(1, 2000)), "created_at": TIME, "updated_at": TIME, "version": VERSION})
    s["CaseOwnerPage"] = page(ref("CaseOwnerView"))
    s["CaseEvidenceCreate"] = obj({"expected_version": VERSION, "media_ids": {**array(ID, 20), "minItems": 1, "uniqueItems": True},
                                    "description": text(1, 1000)})
    s["CaseEvidenceReceipt"] = obj({"id": ID, "case_id": ID, "media_ids": {**array(ID, 20), "minItems": 1},
        "status": enum("ATTACHED"), "accepted_as_proof": {"type": "boolean", "const": False}, "version": VERSION})
    s["CaseMessageCreate"] = obj({"expected_version": VERSION, "body": text(1, 4000)})
    s["CaseMessage"] = obj({"id": ID, "case_id": ID, "body": text(1, 4000), "author_kind": enum("requester", "support"), "created_at": TIME, "version": VERSION})
    s["CaseHistoryEntry"] = obj({"id": ID, "case_id": ID, "kind": enum("opened", "message", "evidence_attached", "information_requested", "decision", "reopened", "closed"),
        "safe_summary": text(1, 2000), "recorded_at": TIME, "message": nullable(ref("CaseMessage"))})
    s["CaseHistoryPage"] = page(ref("CaseHistoryEntry"))
    refund = {"id": ID, "payment_id": ID, "amount_paise": POSITIVE_PAISE, "currency": enum("INR"),
        "status": enum("REQUESTED", "APPROVED", "SUBMITTED", "UNCERTAIN", "PENDING", "PROCESSED", "FAILED", "CANCELLED"),
        "safe_reason": text(1, 1000), "requested_at": TIME, "processed_at": nullable(TIME),
        "provider_reference": nullable(text(1, 100)), "version": VERSION}
    s["RefundOwnerView"] = obj(refund, allOf=[{
        "if": {"properties": {"status": {"const": "PROCESSED"}}},
        "then": {"properties": {"processed_at": TIME, "provider_reference": text(1, 100)}},
        "else": {"properties": {"processed_at": {"type": "null"}}},
    }])
    s["RefundOwnerPage"] = page(ref("RefundOwnerView"))
    s["RefundRequest"] = obj({"expected_version": VERSION, "case_id": ID, "amount_paise": POSITIVE_PAISE, "currency": enum("INR"),
        "reason_code": enum("duplicate_capture", "ineligible_capture", "cancelled_mission", "failed_fulfilment", "approved_exception"),
        "safe_reason": text(1, 1000), "funding_plan_id": ID, "evidence_ids": evidence_ids()})
    s["RefundFinanceView"] = obj({"refund": ref("RefundOwnerView"), "case_id": ID, "funding_plan_id": ID,
        "funding_reserved_paise": PAISE, "invocation_status": enum("NOT_STARTED", "STARTED", "UNCERTAIN", "CONCLUSIVE"),
        "approval_snapshot_id": nullable(ID), "reconciliation_case_id": nullable(ID),
        "restricted_notes": array(text(1, 2000), 100), "evidence_ids": array(ID, 50), "version": VERSION})
    s["RefundFinancePage"] = page(ref("RefundFinanceView"))
    s["RefundApprove"] = obj({"expected_version": VERSION, "approval_snapshot_id": ID, "reason": text(1, 1000), "evidence_ids": evidence_ids()})
    s["RefundCancel"] = obj({"expected_version": VERSION, "reason": text(1, 1000), "evidence_ids": evidence_ids()})
    s["DisputeReview"] = obj({"id": ID, "case": ref("CaseOwnerView"), "status": enum("OPEN", "UNDER_REVIEW", "AWAITING_INFORMATION", "DECIDED"),
        "restricted_notes": array(text(1, 2000), 100), "evidence_ids": array(ID, 50), "decision_id": nullable(ID), "version": VERSION})
    s["DisputeReviewPage"] = page(ref("DisputeReview"))
    base = {"expected_version": VERSION, "safe_reason": text(1, 1000), "evidence_ids": evidence_ids()}
    s["DisputeDecision"] = {"oneOf": [
        obj({**base, "decision": enum("REQUEST_INFORMATION"), "requested_information": {**array(text(1, 300), 30), "minItems": 1}}),
        obj({**base, "decision": enum("REQUEST_REWORK"), "rework_plan_id": ID}),
        obj({**base, "decision": enum("REFER_RECOVERY"), "recovery_plan_id": ID}),
        obj({**base, "decision": enum("CLOSE_NO_ACTION"), "policy_decision_id": ID}),
    ], "discriminator": {"propertyName": "decision"}}
    s["ProviderDisputeEvidenceCreate"] = obj({"expected_version": VERSION, "provider_dispute_ref": text(1, 100),
        "evidence_ids": evidence_ids(), "submission_consent_id": ID, "reason": text(1, 1000)})
    s["ProviderDisputeEvidenceReceipt"] = obj({"id": ID, "dispute_id": ID, "provider_dispute_ref": text(1, 100),
        "status": enum("ATTACHED_FOR_REVIEW"), "submitted_to_provider": {"type": "boolean", "const": False}, "version": VERSION})
    return s


def definitions():
    return {
        "create_support_or_dispute_case": ("CaseCreate", "201", "CaseOwnerView", ["MEDIA_NOT_READY"], "Create owner-scoped support case; server validates subject access. No automatic refund or mission status change."),
        "list_own_cases": (None, "200", "CaseOwnerPage", [], "Only current user's safe cases; reviewer notes are excluded."),
        "get_own_case": (None, "200", "CaseOwnerView", [], "Owner recovery access remains subject to current identity and subject policy."),
        "attach_case_evidence": ("CaseEvidenceCreate", "201", "CaseEvidenceReceipt", ["MEDIA_NOT_READY", "CASE_CLOSED"], "Attach owned processed media revisions; attachment does not verify proof or submit externally."),
        "add_case_message": ("CaseMessageCreate", "201", "CaseMessage", ["CASE_CLOSED"], "Append requester message; client cannot impersonate support or choose internal visibility."),
        "get_case_history": (None, "200", "CaseHistoryPage", [], "Paginated owner-safe history; never serialize internal notes or other participants' private evidence."),
        "list_own_refunds": (None, "200", "RefundOwnerPage", [], "Owner refunds for the scoped payment, independent of contribution execution."),
        "get_refund": (None, "200", "RefundOwnerView", [], "Processed means authoritative provider evidence, not guaranteed bank arrival."),
        "request_refund": ("RefundRequest", "201", "RefundFinanceView", ["REFUND_AMOUNT_UNAVAILABLE", "RECOVERY_FUNDING_REQUIRED"], "Lock captured payment and funding plan; reserve amount once. No provider invocation until approval."),
        "list_payment_refunds": (None, "200", "RefundFinancePage", [], "Finance-scoped intent, funding and reconciliation records."),
        "get_refund_recovery": (None, "200", "RefundFinanceView", [], "Preserve uncertainty and funding holds; response excludes provider credentials and raw bank accounts."),
        "approve_refund": ("RefundApprove", "200", "RefundFinanceView", ["REFUND_POLICY_DENIED", "REFUND_AMOUNT_UNAVAILABLE", "RECOVERY_FUNDING_REQUIRED"], "Approve exact current immutable funding/amount snapshot with step-up; atomically persist approval and durable submission work."),
        "cancel_unsent_refund": ("RefundCancel", "200", "RefundFinanceView", ["REFUND_ALREADY_SUBMITTED"], "Cancel only before invocation under lock; timeout or missing provider response never releases funds."),
        "list_disputes": (None, "200", "DisputeReviewPage", [], "Assigned scoped review queue, not global Finance access."),
        "get_dispute": (None, "200", "DisputeReview", [], "Scoped dispute evidence and restricted notes; separate owner serializer."),
        "decide_dispute": ("DisputeDecision", "200", "DisputeReview", [], "Record versioned case decision and durable approved recovery/rework intents. No direct refund, payout or final-impact rewrite."),
        "attach_provider_dispute_evidence": ("ProviderDisputeEvidenceCreate", "201", "ProviderDisputeEvidenceReceipt", [], "Prepare consented scoped evidence for review. External provider submission requires separately approved workflow and evidence redaction."),
    }


def examples():
    case = {"id": UUID, "subject": {"type": "payment", "id": UUID}, "category": "payment", "description": "Payment needs review",
            "status": "OPEN", "safe_resolution": None, "created_at": NOW, "updated_at": NOW, "version": 1}
    refund = {"id": UUID, "payment_id": UUID, "amount_paise": 2500, "currency": "INR", "status": "REQUESTED",
              "safe_reason": "Approved partial recovery", "requested_at": NOW, "processed_at": None, "provider_reference": None, "version": 1}
    finance = {"refund": refund, "case_id": UUID, "funding_plan_id": UUID, "funding_reserved_paise": 2500, "invocation_status": "NOT_STARTED",
               "approval_snapshot_id": None, "reconciliation_case_id": None, "restricted_notes": [], "evidence_ids": [UUID], "version": 1}
    review = {"id": UUID, "case": case, "status": "UNDER_REVIEW", "restricted_notes": [], "evidence_ids": [UUID], "decision_id": None, "version": 1}
    message = {"id": UUID, "case_id": UUID, "body": "Please check payment status", "author_kind": "requester", "created_at": NOW, "version": 1}
    e = {
        "CaseCreate": {"subject": case["subject"], "category": "payment", "description": case["description"], "evidence_media_ids": []},
        "CaseOwnerView": case, "CaseEvidenceCreate": {"expected_version": 1, "media_ids": [UUID], "description": "Supporting evidence"},
        "CaseEvidenceReceipt": {"id": UUID, "case_id": UUID, "media_ids": [UUID], "status": "ATTACHED", "accepted_as_proof": False, "version": 1},
        "CaseMessageCreate": {"expected_version": 1, "body": message["body"]}, "CaseMessage": message,
        "CaseHistoryEntry": {"id": UUID, "case_id": UUID, "kind": "message", "safe_summary": "Message added", "recorded_at": NOW, "message": message},
        "RefundOwnerView": refund, "RefundFinanceView": finance,
        "RefundRequest": {"expected_version": 1, "case_id": UUID, "amount_paise": 2500, "currency": "INR", "reason_code": "approved_exception",
            "safe_reason": refund["safe_reason"], "funding_plan_id": UUID, "evidence_ids": [UUID]},
        "RefundApprove": {"expected_version": 1, "approval_snapshot_id": UUID, "reason": "Funding reviewed", "evidence_ids": [UUID]},
        "RefundCancel": {"expected_version": 1, "reason": "Request withdrawn before dispatch", "evidence_ids": [UUID]},
        "DisputeReview": review, "DisputeDecision": {"expected_version": 1, "safe_reason": "Recovery review required", "evidence_ids": [UUID],
                                                   "decision": "REFER_RECOVERY", "recovery_plan_id": UUID},
        "ProviderDisputeEvidenceCreate": {"expected_version": 1, "provider_dispute_ref": "disp_synthetic", "evidence_ids": [UUID], "submission_consent_id": UUID, "reason": "Evidence for review"},
        "ProviderDisputeEvidenceReceipt": {"id": UUID, "dispute_id": UUID, "provider_dispute_ref": "disp_synthetic", "status": "ATTACHED_FOR_REVIEW", "submitted_to_provider": False, "version": 1},
    }
    for name, item in [("CaseOwnerPage", "CaseOwnerView"), ("CaseHistoryPage", "CaseHistoryEntry"), ("RefundOwnerPage", "RefundOwnerView"),
                       ("RefundFinancePage", "RefundFinanceView"), ("DisputeReviewPage", "DisputeReview")]:
        e[name] = {"items": [deepcopy(e[item])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples()
    processed = {**e["RefundOwnerView"], "status": "PROCESSED", "processed_at": NOW, "provider_reference": "rfnd_synthetic"}
    uncertain = deepcopy(e["RefundFinanceView"])
    uncertain["refund"]["status"] = "UNCERTAIN"
    uncertain.update(invocation_status="UNCERTAIN", approval_snapshot_id=UUID, reconciliation_case_id=UUID)
    base = {"expected_version": 1, "safe_reason": "Reviewed case", "evidence_ids": [UUID]}
    return {"RefundOwnerView": {"processed": processed}, "RefundFinanceView": {"uncertain": uncertain},
        "DisputeDecision": {"information": {**base, "decision": "REQUEST_INFORMATION", "requested_information": ["Updated evidence"]},
            "rework": {**base, "decision": "REQUEST_REWORK", "rework_plan_id": UUID},
            "no_action": {**base, "decision": "CLOSE_NO_ACTION", "policy_decision_id": UUID}}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value, label in [
        ("CaseCreate", "owner_user_id", UUID, "case owner injection"),
        ("CaseCreate", "status", "RESOLVED", "requester resolves own case"),
        ("CaseOwnerView", "restricted_notes", ["internal"], "private notes in owner view"),
        ("CaseMessageCreate", "author_kind", "support", "support impersonation"),
        ("CaseEvidenceCreate", "media_ids", [], "empty evidence attachment"),
        ("CaseEvidenceReceipt", "accepted_as_proof", True, "attachment claims verification"),
        ("RefundRequest", "amount_paise", 0, "zero refund"),
        ("RefundRequest", "amount_paise", 0.5, "fractional refund paise"),
        ("RefundRequest", "currency", "USD", "wrong refund currency"),
        ("RefundRequest", "status", "PROCESSED", "manual processed injection"),
        ("RefundRequest", "evidence_ids", [], "refund without evidence"),
        ("RefundOwnerView", "funding_plan_id", UUID, "Finance plan leaked to owner"),
        ("RefundOwnerView", "status", "PROCESSED", "processed without evidence time"),
        ("RefundOwnerView", "processed_at", NOW, "requested refund claims processing"),
        ("RefundFinanceView", "provider_secret", "secret", "provider secret leakage"),
        ("RefundApprove", "amount_paise", 100, "approval changes amount"),
        ("RefundCancel", "force", True, "force cancellation bypass"),
        ("DisputeDecision", "decision", "REFUND_PAID", "dispute fabricates refund"),
        ("DisputeDecision", "evidence_ids", [], "unsupported dispute decision"),
        ("ProviderDisputeEvidenceReceipt", "submitted_to_provider", True, "attachment claims external submission"),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, label))
    for schema, key in [("RefundRequest", "funding_plan_id"), ("RefundApprove", "approval_snapshot_id"), ("DisputeDecision", "recovery_plan_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing bound recovery/approval reference"))
    return cases
