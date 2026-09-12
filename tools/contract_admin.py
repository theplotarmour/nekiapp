"""Scoped operations, access administration and recovery draft contracts."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import array
from contract_cases import evidence_ids
from contract_contributions import PAISE


def schemas():
    s = {}
    s["Liveness"] = obj({"status": enum("alive")})
    s["OperationalHealth"] = obj({"as_of": TIME, "components": array(obj({"name": enum("database", "queue", "media", "webhooks", "realtime"),
        "status": enum("HEALTHY", "DEGRADED", "UNAVAILABLE", "UNKNOWN"), "pending_count": nullable(integer()), "oldest_pending_seconds": nullable(integer())}), 5)})
    s["ScopedUser"] = obj({"id": ID, "display_name": text(1, 160), "account_status": enum("ACTIVE", "SUSPENDED", "DELETION_PENDING"),
        "organization_ids": array(ID, 100), "safe_case_summary": nullable(text(1, 1000)), "version": VERSION})
    s["ScopedUserPage"] = page(ref("ScopedUser"))
    base = {"expected_version": VERSION, "reason": text(1, 1000), "evidence_ids": evidence_ids()}
    s["UserAccessCommand"] = obj({**base, "case_id": ID, "policy_decision_id": ID})
    scope = {"oneOf": [obj({"kind": enum("organization"), "organization_id": ID}),
                        obj({"kind": enum("queue"), "queue_id": ID}), obj({"kind": enum("platform"), "approval_decision_id": ID})]}
    grant = {"user_id": ID, "role": enum("org_admin", "reviewer", "ops", "ops_lead", "finance", "security"),
             "scope": scope, "expires_at": TIME, "authorization_decision_id": ID}
    s["RoleGrantCreate"] = obj({**grant, "reason": text(1, 1000), "evidence_ids": evidence_ids()})
    s["RoleGrantView"] = obj({**grant, "id": ID, "status": enum("ACTIVE", "REVOKED", "EXPIRED"), "version": VERSION})
    s["RoleGrantRevoke"] = obj(base)
    s["FraudSignal"] = obj({"id": ID, "subject_user_id": nullable(ID), "case_id": nullable(ID),
        "category": enum("payment", "media", "location", "account", "repetition"), "status": enum("OPEN", "UNDER_REVIEW", "DISMISSED", "REFERRED"),
        "safe_summary": text(1, 1000), "recorded_at": TIME, "version": VERSION})
    s["FraudSignalPage"] = page(ref("FraudSignal"))
    s["FraudReviewDecision"] = obj({**base, "decision": enum("DISMISS", "REFER_CASE"), "case_id": nullable(ID)}, allOf=[{
        "if": {"properties": {"decision": {"const": "REFER_CASE"}}}, "then": {"properties": {"case_id": ID}}}])
    s["AuditEntry"] = obj({"id": ID, "recorded_at": TIME, "actor_id": ID, "operation_id": text(1, 100),
        "subject_id": ID, "outcome": enum("ACCEPTED", "DENIED", "FAILED"), "safe_reason": nullable(text(1, 1000)), "correlation_id": ID})
    s["AuditPage"] = page(ref("AuditEntry"))
    s["SupportCaseReview"] = obj({"case": ref("CaseOwnerView"), "assigned_agent_id": nullable(ID), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["SupportCasePage"] = page(ref("SupportCaseReview"))
    s["SupportAssign"] = obj({"expected_version": VERSION, "agent_id": ID, "reason": text(1, 1000)})
    s["SupportReply"] = obj({"expected_version": VERSION, "body": text(1, 4000), "visibility": enum("requester")})
    s["SupportReplyMessage"] = {"allOf": [ref("CaseMessage"), {"properties": {"author_kind": enum("support")}}]}
    s["SupportResolve"] = obj({**base, "safe_resolution": text(1, 2000), "resolution_decision_id": ID})
    report = {"subject": {"oneOf": [obj({"kind": enum(kind), "id": ID}) for kind in ("mission", "organization", "mission_update", "proof_derivative") ]},
        "category": enum("privacy", "misleading", "unsafe", "abuse", "other"), "description": text(1, 2000)}
    s["ContentReportCreate"] = obj({**report, "evidence_ids": array(ID, 20)})
    s["ContentReportReceipt"] = obj({"id": ID, "status": enum("RECEIVED"), "content_removed": {"type": "boolean", "const": False}})
    s["ContentReportReview"] = obj({**report, "id": ID, "status": enum("OPEN", "UNDER_REVIEW", "DISMISSED", "ACTION_REQUESTED"),
        "evidence_ids": array(ID, 20), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["ContentReportPage"] = page(ref("ContentReportReview"))
    s["ContentReportDecision"] = obj({**base, "decision": enum("DISMISS", "REQUEST_RESTRICTION"), "policy_decision_id": ID})
    s["OpsExportCreate"] = obj({"report": enum("fulfilment", "verification_sla", "support"), "organization_id": nullable(ID),
        "from_at": TIME, "to_at": TIME, "format": enum("csv"), "purpose": text(1, 500)})
    s["OpsExportView"] = {"oneOf": [obj({"id": ID, "status": enum("PENDING", "RUNNING", "FAILED", "EXPIRED"), "safe_message": text(1, 500)}),
        obj({"id": ID, "status": enum("READY"), "media_id": ID, "expires_at": TIME, "snapshot_id": ID})]}
    s["BlockedEvent"] = obj({"id": ID, "event_type": text(1, 150), "schema_version": integer(1), "aggregate_id": ID,
        "consumer": text(1, 100), "attempt_count": integer(), "safe_failure_code": text(1, 100), "blocked_at": TIME, "version": VERSION})
    s["BlockedEventPage"] = page(ref("BlockedEvent"))
    s["EventRecoveryView"] = obj({"event": ref("BlockedEvent"), "recovery_case_id": nullable(ID), "applied_receipt_ids": array(ID, 100),
        "status": enum("BLOCKED", "REPLAY_QUEUED", "RESOLVED"), "version": VERSION})
    s["EventReplay"] = obj({**base, "consumer": text(1, 100), "recovery_case_id": ID, "remediation_decision_id": ID})
    s["ScopedOperation"] = {"oneOf": [obj({"id": ID, "status": enum("PENDING", "RUNNING", "FAILED", "CANCELLED"), "safe_message": text(1, 500)}),
        obj({"id": ID, "status": enum("SUCCEEDED"), "result": obj({"kind": enum("media", "export", "case", "reconciliation", "event_replay", "payment_method_removal"), "id": ID})})]}
    s["RecoveryJobReceipt"] = obj({"operation_id": ID, "status": enum("PENDING"), "financial_effect_applied": {"type": "boolean", "const": False}})
    s["PaymentReconcileRequest"] = obj({**base, "recovery_case_id": ID})
    s["PaymentRecoveryView"] = obj({"id": ID, "contribution_id": nullable(ID), "provider_payment_ref": text(1, 100), "currency": enum("INR"),
        "captured_paise": PAISE, "allocated_paise": PAISE, "processed_refund_paise": PAISE,
        "status": enum("UNLINKED", "RECONCILING", "RECOVERY_REQUIRED", "RESOLVED"), "case_id": nullable(ID), "version": VERSION})
    s["PaymentRecoveryCase"] = obj({"id": ID, "payment": ref("PaymentRecoveryView"), "status": enum("OPEN", "UNDER_REVIEW", "RESOLVED"),
        "restricted_notes": array(text(1, 2000), 100), "source_evidence_ids": array(ID, 100), "version": VERSION})
    s["PaymentRecoveryPage"] = page(ref("PaymentRecoveryCase"))
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, code="200"):
        d[op] = (request, code, response, [], effect)
    add("get_liveness", None, "Liveness", "Process liveness only; no dependency, version, host or secret disclosure.")
    add("get_operational_health", None, "OperationalHealth", "Scoped sanitized component health; not a public readiness attestation.")
    add("list_users", None, "ScopedUserPage", "Permitted support scope only, without credentials or raw contact data.")
    add("get_scoped_user", None, "ScopedUser", "Subject scope checked before returning case-safe profile.")
    for op in ("suspend_user", "reinstate_user"):
        add(op, "UserAccessCommand", "ScopedUser", "Case/policy-bound access decision; revoke stale sessions/grants and create recovery intent. Reinstatement does not bypass domain review requirements.")
    add("grant_scoped_role", "RoleGrantCreate", "RoleGrantView", "Explicit access-admin step-up, permitted role/scope matrix and no self-escalation; audit exact time-bounded grant.", "201")
    add("revoke_scoped_role", "RoleGrantRevoke", "RoleGrantView", "Revoke grant and propagate current-access denial; cannot remove mandatory last security administrator without policy.")
    add("list_fraud_signals", None, "FraudSignalPage", "Scoped review signals are not findings of misconduct.")
    add("decide_fraud_review", "FraudReviewDecision", "FraudSignal", "Evidence-based dismissal or case referral; no automatic suspension or money movement.")
    add("list_scoped_audit", None, "AuditPage", "Append-only sanitized audit projection, excluding raw bodies and credentials.")
    add("list_support_cases", None, "SupportCasePage", "Assigned/permitted cases only; not unrestricted Finance or private proof access.")
    add("get_support_case", None, "SupportCaseReview", "Current support scope and restricted notes; requester view separate.")
    add("assign_support_case", "SupportAssign", "SupportCaseReview", "Validate agent queue capability and assign under version lock.")
    add("reply_support_case", "SupportReply", "SupportReplyMessage", "Append requester-visible support reply; author derived from current agent.", "201")
    add("resolve_support_case", "SupportResolve", "SupportCaseReview", "Require reviewed resolution; do not imply unresolved refunds/custody jobs completed.")
    add("create_content_report", "ContentReportCreate", "ContentReportReceipt", "Create report against visible subject; no automatic takedown.", "201")
    add("decide_content_report", "ContentReportDecision", "ContentReportReview", "Case disposition with durable restriction intent; removal cannot bypass underlying domain capability.")
    add("list_content_reports", None, "ContentReportPage", "Scoped moderation queue.")
    add("get_content_report", None, "ContentReportReview", "Authorized report and evidence, excluding unrelated subject-private fields.")
    add("create_ops_export", "OpsExportCreate", "OpsExportView", "Queue scoped snapshot CSV with approved redaction and spreadsheet formula neutralization; no Finance report bypass.", "202")
    add("get_ops_export", None, "OpsExportView", "Current report capability and source scope; media download authorizes again.")
    add("list_blocked_events", None, "BlockedEventPage", "Sanitized blocked consumer work; no raw financial/private payload.")
    add("get_event_recovery_details", None, "EventRecoveryView", "Recovery metadata and processing receipts under source capability; never executable payload editing.")
    add("replay_event", "EventReplay", "RecoveryJobReceipt", "Replay exact stored event to permitted consumer after remediation; retain receipts/idempotency and block unauthorized Finance effects.", "202")
    add("get_scoped_operation_job", None, "ScopedOperation", "Submitting principal plus current originating capability/source access; result reference cannot bypass target authorization.")
    add("request_payment_reconciliation", "PaymentReconcileRequest", "RecoveryJobReceipt", "Finance step-up queues authenticated provider lookup; request cannot set captured/refunded status or issue a replacement payment.", "202")
    add("get_payment_recovery", None, "PaymentRecoveryView", "Scoped provider facts with independent allocation/refund totals; no credentials.")
    add("get_payment_recovery_case", None, "PaymentRecoveryCase", "Finance-scoped linkage/recovery evidence.")
    add("list_payment_recovery", None, "PaymentRecoveryPage", "Finance-scoped unresolved/closed recovery queue, preserving late facts.")
    return d


def examples():
    base = {"expected_version": 1, "reason": "Reviewed case", "evidence_ids": [UUID]}
    user = {"id": UUID, "display_name": "Synthetic user", "account_status": "ACTIVE", "organization_ids": [], "safe_case_summary": None, "version": 1}
    grant = {"user_id": UUID, "role": "reviewer", "scope": {"kind": "queue", "queue_id": UUID}, "expires_at": "2026-10-01T00:00:00Z", "authorization_decision_id": UUID}
    from contract_cases import examples as case_examples
    report = {"subject": {"kind": "mission", "id": UUID}, "category": "privacy", "description": "Review identifying content"}
    event = {"id": UUID, "event_type": "SyntheticEvent.v1", "schema_version": 1, "aggregate_id": UUID, "consumer": "synthetic_projection",
        "attempt_count": 3, "safe_failure_code": "REVISION_UNAVAILABLE", "blocked_at": NOW, "version": 1}
    payment = {"id": UUID, "contribution_id": None, "provider_payment_ref": "pay_synthetic", "currency": "INR", "captured_paise": 10000,
        "allocated_paise": 0, "processed_refund_paise": 0, "status": "UNLINKED", "case_id": UUID, "version": 1}
    e = {"Liveness": {"status": "alive"}, "OperationalHealth": {"as_of": NOW, "components": [{"name": "queue", "status": "UNKNOWN", "pending_count": None, "oldest_pending_seconds": None}]},
        "ScopedUser": user, "UserAccessCommand": {**base, "case_id": UUID, "policy_decision_id": UUID},
        "RoleGrantCreate": {**grant, "reason": "Assigned review duty", "evidence_ids": [UUID]}, "RoleGrantView": {**grant, "id": UUID, "status": "ACTIVE", "version": 1}, "RoleGrantRevoke": base,
        "FraudSignal": {"id": UUID, "subject_user_id": UUID, "case_id": None, "category": "repetition", "status": "OPEN", "safe_summary": "Repeated submissions for review", "recorded_at": NOW, "version": 1},
        "FraudReviewDecision": {**base, "decision": "REFER_CASE", "case_id": UUID},
        "AuditEntry": {"id": UUID, "recorded_at": NOW, "actor_id": UUID, "operation_id": "synthetic_review", "subject_id": UUID, "outcome": "ACCEPTED", "safe_reason": None, "correlation_id": UUID},
        "SupportCaseReview": {"case": case_examples()["CaseOwnerView"], "assigned_agent_id": UUID, "restricted_notes": [], "version": 1},
        "SupportAssign": {"expected_version": 1, "agent_id": UUID, "reason": "Assigned queue"}, "SupportReply": {"expected_version": 1, "body": "Review is in progress", "visibility": "requester"},
        "SupportResolve": {**base, "safe_resolution": "Reviewed resolution recorded", "resolution_decision_id": UUID},
        "ContentReportCreate": {**report, "evidence_ids": []}, "ContentReportReceipt": {"id": UUID, "status": "RECEIVED", "content_removed": False},
        "ContentReportReview": {**report, "id": UUID, "status": "OPEN", "evidence_ids": [], "restricted_notes": [], "version": 1},
        "ContentReportDecision": {**base, "decision": "REQUEST_RESTRICTION", "policy_decision_id": UUID},
        "OpsExportCreate": {"report": "fulfilment", "organization_id": UUID, "from_at": "2026-09-01T00:00:00Z", "to_at": NOW, "format": "csv", "purpose": "Operational review"},
        "OpsExportView": {"id": UUID, "status": "PENDING", "safe_message": "Export queued"}, "BlockedEvent": event,
        "EventRecoveryView": {"event": event, "recovery_case_id": UUID, "applied_receipt_ids": [], "status": "BLOCKED", "version": 1},
        "EventReplay": {**base, "consumer": "synthetic_projection", "recovery_case_id": UUID, "remediation_decision_id": UUID},
        "ScopedOperation": {"id": UUID, "status": "PENDING", "safe_message": "Work queued"},
        "RecoveryJobReceipt": {"operation_id": UUID, "status": "PENDING", "financial_effect_applied": False}, "PaymentReconcileRequest": {**base, "recovery_case_id": UUID},
        "PaymentRecoveryView": payment, "PaymentRecoveryCase": {"id": UUID, "payment": payment, "status": "OPEN", "restricted_notes": [], "source_evidence_ids": [], "version": 1}}
    for name, member in [("ScopedUserPage", "ScopedUser"), ("FraudSignalPage", "FraudSignal"), ("AuditPage", "AuditEntry"), ("SupportCasePage", "SupportCaseReview"),
                         ("ContentReportPage", "ContentReportReview"), ("BlockedEventPage", "BlockedEvent"), ("PaymentRecoveryPage", "PaymentRecoveryCase")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    e["SupportReplyMessage"] = {**case_examples()["CaseMessage"], "author_kind": "support"}
    return e


def example_variants():
    return {"ScopedOperation": {"succeeded": {"id": UUID, "status": "SUCCEEDED", "result": {"kind": "event_replay", "id": UUID}}},
        "OpsExportView": {"ready": {"id": UUID, "status": "READY", "media_id": UUID, "expires_at": NOW, "snapshot_id": UUID}}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [("Liveness", "database_url", "private"), ("ScopedUser", "refresh_token", "private"),
        ("RoleGrantCreate", "role", "super_admin"), ("RoleGrantCreate", "scope", {}), ("RoleGrantCreate", "granted_by", UUID),
        ("FraudReviewDecision", "decision", "AUTO_SUSPEND"), ("FraudReviewDecision", "case_id", None),
        ("AuditEntry", "request_body", "private"), ("SupportReply", "author_id", UUID), ("SupportReply", "visibility", "internal"),
        ("ContentReportReceipt", "content_removed", True), ("OpsExportCreate", "report", "bank_accounts"),
        ("EventReplay", "replacement_payload", {}), ("EventReplay", "skip_receipts", True), ("EventReplay", "evidence_ids", []),
        ("ScopedOperation", "result", {"kind": "export", "id": UUID}), ("RecoveryJobReceipt", "financial_effect_applied", True),
        ("PaymentReconcileRequest", "captured_paise", 100), ("PaymentRecoveryView", "provider_secret", "private")]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid administrative authority or sensitive field"))
    return cases
