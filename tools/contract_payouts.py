"""Audited manual payout and Finance reporting draft contracts."""

from copy import deepcopy
from contract_identity import ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import array
from contract_contributions import PAISE, POSITIVE_PAISE
from contract_cases import evidence_ids


def schemas():
    s = {}
    s["PayoutAllocationItem"] = obj({"allocation_id": ID, "expected_allocation_version": VERSION, "amount_paise": POSITIVE_PAISE})
    items = {**array(ref("PayoutAllocationItem"), 100), "minItems": 1, "uniqueItems": True}
    draft = {"organization_id": ID, "bank_revision_id": ID, "currency": enum("INR"), "items": items,
             "reason": text(1, 1000), "source_return_id": nullable(ID)}
    s["PayoutDraftCreate"] = obj(draft)
    s["PayoutDraftEdit"] = obj({"expected_version": VERSION, "bank_revision_id": ID, "items": items, "reason": text(1, 1000)})
    s["PayableAllocation"] = obj({"allocation_id": ID, "organization_id": ID, "contribution_id": ID,
        "available_paise": PAISE, "reserved_paise": PAISE, "consumed_paise": PAISE, "currency": enum("INR"), "version": VERSION})
    s["PayableAllocationPage"] = page(ref("PayableAllocation"))
    s["PayoutTransferAttempt"] = obj({"id": ID, "status": enum("STARTED", "UNCERTAIN", "FAILED", "CONFIRMED"),
        "started_at": TIME, "bank_reference": nullable(text(1, 100)), "value_date": nullable(text(10, 10, format="date")),
        "amount_paise": POSITIVE_PAISE, "bank_revision_id": ID, "reconciliation_case_id": nullable(ID), "version": VERSION},
        allOf=[{"if": {"properties": {"status": {"const": "CONFIRMED"}}},
                "then": {"properties": {"bank_reference": text(1, 100), "value_date": text(10, 10, format="date")}}}])
    s["PayoutReturnFact"] = obj({"id": ID, "transfer_attempt_id": ID, "bank_return_reference": text(1, 100),
        "amount_paise": POSITIVE_PAISE, "recorded_at": TIME, "accounting_decision_id": ID})
    s["PayoutFinanceView"] = obj({"id": ID, **draft, "amount_paise": POSITIVE_PAISE,
        "status": enum("DRAFT", "APPROVED", "PAID", "RECONCILED", "CANCELLED"),
        "approval_snapshot_id": nullable(ID), "approval_requested_at": nullable(TIME), "prepared_by": ID,
        "approved_by": nullable(ID), "transfer_attempts": array(ref("PayoutTransferAttempt"), 100),
        "returns": array(ref("PayoutReturnFact"), 100), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["PayoutFinancePage"] = page(ref("PayoutFinanceView"))
    base = {"expected_version": VERSION, "reason": text(1, 1000)}
    evidenced = {**base, "evidence_ids": evidence_ids()}
    s["PayoutSubmit"] = obj(base)
    s["PayoutApprove"] = obj({**evidenced, "approval_snapshot_id": ID})
    s["PayoutBeginTransfer"] = obj({**base, "approval_snapshot_id": ID, "bank_revision_id": ID})
    s["PayoutUncertain"] = obj({**base, "transfer_attempt_id": ID, "reconciliation_case_id": ID})
    s["PayoutPaid"] = obj({**evidenced, "transfer_attempt_id": ID, "bank_revision_id": ID, "bank_reference": text(1, 100),
        "value_date": text(10, 10, format="date"), "amount_paise": POSITIVE_PAISE, "currency": enum("INR")})
    s["PayoutReconcile"] = obj({**evidenced, "bank_report_id": ID, "reconciliation_snapshot_id": ID})
    s["PayoutCancel"] = obj(evidenced)
    s["PayoutFailure"] = obj({**evidenced, "transfer_attempt_id": ID, "no_transfer_decision_id": ID})
    s["PayoutReturn"] = obj({**evidenced, "transfer_attempt_id": ID, "bank_return_reference": text(1, 100),
        "amount_paise": POSITIVE_PAISE, "currency": enum("INR"), "accounting_decision_id": ID})
    s["PayoutEvidenceCreate"] = obj({**evidenced, "transfer_attempt_id": nullable(ID)})
    s["PayoutEvidenceReceipt"] = obj({"id": ID, "payout_id": ID, "evidence_ids": evidence_ids(), "version": VERSION,
        "status": enum("ATTACHED"), "payment_confirmed": {"type": "boolean", "const": False}})
    s["OrganizationLiability"] = obj({"organization_id": ID, "currency": enum("INR"), "available_principal_paise": PAISE,
        "reserved_principal_paise": PAISE, "consumed_principal_paise": PAISE, "unallocated_capture_recovery_paise": PAISE,
        "platform_funded_recovery_paise": PAISE, "as_of": TIME, "snapshot_id": ID})
    s["OrganizationLiabilityPage"] = page(ref("OrganizationLiability"))
    s["FinanceReconciliationEntry"] = obj({"id": ID, "kind": enum("gateway_capture", "gateway_settlement", "refund", "payout", "bank_return"),
        "subject_id": ID, "expected_paise": PAISE, "observed_paise": nullable(PAISE), "currency": enum("INR"),
        "status": enum("UNMATCHED", "MATCHED", "VARIANCE", "UNCERTAIN"), "case_id": nullable(ID), "snapshot_id": ID, "as_of": TIME})
    s["FinanceReconciliationPage"] = page(ref("FinanceReconciliationEntry"))
    s["PayoutOrganizationView"] = obj({"id": ID, "amount_paise": POSITIVE_PAISE, "currency": enum("INR"),
        "status": enum("DRAFT", "APPROVED", "PAID", "RECONCILED", "CANCELLED"), "transfer_status": enum("NOT_STARTED", "STARTED", "UNCERTAIN", "FAILED", "CONFIRMED"),
        "bank_reference": nullable(text(1, 100)), "value_date": nullable(text(10, 10, format="date")),
        "returned_paise": PAISE, "safe_recovery_summary": nullable(text(1, 1000)), "version": VERSION})
    s["PayoutOrganizationPage"] = page(ref("PayoutOrganizationView"))
    s["OrganizationStatementEntry"] = obj({"id": ID, "kind": enum("allocation_credit", "payout_paid", "refund_consumed", "payout_return", "approved_adjustment"),
        "direction": enum("CREDIT", "DEBIT"), "amount_paise": POSITIVE_PAISE, "recorded_at": TIME, "safe_description": text(1, 500)})
    s["OrganizationStatement"] = obj({"organization_id": ID, "currency": enum("INR"), "snapshot_id": ID, "as_of": TIME,
        "entries": array(ref("OrganizationStatementEntry"), 50), "next_cursor": nullable(text(1, 2048)),
        "has_more": {"type": "boolean"}, "opening_balance_paise": PAISE, "closing_balance_paise": PAISE})
    s["FinanceExportCreate"] = obj({"report": enum("payouts", "liabilities", "reconciliation"), "organization_id": nullable(ID),
        "from_at": TIME, "to_at": TIME, "format": enum("csv"), "purpose": text(1, 500)})
    s["FinanceExport"] = {"oneOf": [
        obj({"id": ID, "status": enum("PENDING", "RUNNING", "FAILED", "EXPIRED"), "safe_message": text(1, 500)}),
        obj({"id": ID, "status": enum("READY"), "media_id": ID, "expires_at": TIME, "snapshot_id": ID}),
    ], "discriminator": {"propertyName": "status"}}
    s["BankChangeReview"] = obj({"request": ref("BankChangeSummary"), "organization_id": ID,
        "proposed_bank_revision_id": ID, "verification_evidence_ids": array(ID, 50),
        "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["BankChangeReviewPage"] = page(ref("BankChangeReview"))
    s["BankChangeDecision"] = {"oneOf": [
        obj({**evidenced, "decision": enum("APPROVE"), "proposed_bank_revision_id": ID, "verification_decision_id": ID}),
        obj({**evidenced, "decision": enum("REJECT"), "proposed_bank_revision_id": ID}),
    ], "discriminator": {"propertyName": "decision"}}
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, status="200", errors=()):
        d[op] = (request, status, response, list(errors), effect)
    add("list_payable_allocations", None, "PayableAllocationPage", "Finance scope; displayed availability is not a reservation.")
    add("list_payouts", None, "PayoutFinancePage", "Scoped payout queue including transfer uncertainty and return history.")
    add("create_payout_draft", "PayoutDraftCreate", "PayoutFinanceView", "Atomically reserve same-org allocation amounts against verified bank revision; sum on server.", "201", ["ALLOCATION_CONFLICT", "BANK_NOT_VERIFIED"])
    add("get_payout", None, "PayoutFinanceView", "Read audited payout and independent transfer attempts/returns.")
    add("edit_payout_draft", "PayoutDraftEdit", "PayoutFinanceView", "Replace reservations under locks only while unsubmitted/editable; invalidate prior review snapshot.", errors=["ALLOCATION_CONFLICT", "BANK_NOT_VERIFIED"])
    add("submit_payout_for_approval", "PayoutSubmit", "PayoutFinanceView", "Create immutable review snapshot and approval request; DRAFT is not APPROVED.")
    add("approve_payout", "PayoutApprove", "PayoutFinanceView", "Approve exact snapshot; current cash/hold policy and distinct approver above 5000000 paise required.", errors=["SECOND_APPROVER_REQUIRED", "PAYOUT_HOLD"])
    add("begin_payout_transfer", "PayoutBeginTransfer", "PayoutFinanceView", "Persist STARTED transfer attempt before bank action, retain reservation; not proof of payment.", errors=["TRANSFER_ALREADY_STARTED", "BANK_REVISION_CHANGED"])
    add("record_uncertain_transfer", "PayoutUncertain", "PayoutFinanceView", "Mark current attempt uncertain; retain all funds and block new transfer/cancellation.")
    add("record_paid_payout", "PayoutPaid", "PayoutFinanceView", "Verify exact bank evidence and recipient/amount; consume reserved principal once.", errors=["TRANSFER_MISMATCH"])
    add("reconcile_payout", "PayoutReconcile", "PayoutFinanceView", "Match bank report and allocations; reconciliation makes no new balance movement.", errors=["PAYOUT_RECONCILIATION_MISMATCH"])
    add("cancel_payout", "PayoutCancel", "PayoutFinanceView", "Cancel only conclusively untransferred payout under lock; release unconsumed reservation.", errors=["TRANSFER_OUTCOME_UNRESOLVED"])
    add("record_transfer_failure", "PayoutFailure", "PayoutFinanceView", "Record conclusive failure with evidence; retain reservation for reviewed retry/cancellation.", errors=["TRANSFER_OUTCOME_UNRESOLVED"])
    add("record_payout_return", "PayoutReturn", "PayoutFinanceView", "Append unique bank return and approved accounting restoration; preserve original paid/reconciled history.")
    add("attach_payout_evidence", "PayoutEvidenceCreate", "PayoutEvidenceReceipt", "Attach scoped processed evidence; does not mark payout paid.", "201", ["MEDIA_NOT_READY"])
    add("get_org_liabilities", None, "OrganizationLiabilityPage", "Snapshot separate principal, reservation and recovery categories; not status-sum liability formula.")
    add("get_finance_reconciliation", None, "FinanceReconciliationPage", "Snapshot explicit expected/observed cash facts and unmatched/uncertain items.")
    add("list_own_org_payouts", None, "PayoutOrganizationPage", "Own organization statement-safe payouts, excluding internal notes, other contributors and bank credentials.")
    add("get_org_statement", None, "OrganizationStatement", "Own immutable snapshot with cursor-bound paginated ledger entries; balances cover statement period, not just page.")
    add("request_finance_export", "FinanceExportCreate", "FinanceExport", "Queue scoped redacted CSV from stable report snapshot; protect spreadsheet formula cells and audit access.", "202")
    add("get_finance_export", None, "FinanceExport", "Status and private media reference only; current Finance grant and expiry checked again on download.")
    add("decide_bank_change", "BankChangeDecision", "BankChangeReview", "Review exact proposed recipient revision; approval invalidates dependent stale payout approvals, never retroactively edits paid recipient.")
    add("list_bank_verification_queue", None, "BankChangeReviewPage", "Finance verification queue with masked account metadata; no raw account export.")
    add("get_bank_change_review", None, "BankChangeReview", "Read verification references scoped to Finance; raw bank handling remains restricted verification workflow.")
    return d


def examples():
    from contract_organizations import examples as org_examples
    item = {"allocation_id": UUID, "expected_allocation_version": 1, "amount_paise": 100000}
    draft = {"organization_id": UUID, "bank_revision_id": UUID, "currency": "INR", "items": [item], "reason": "Approved mission allocation", "source_return_id": None}
    payout = {"id": UUID, **draft, "amount_paise": 100000, "status": "DRAFT", "approval_snapshot_id": None,
        "approval_requested_at": None, "prepared_by": UUID, "approved_by": None, "transfer_attempts": [], "returns": [], "restricted_notes": [], "version": 1}
    base = {"expected_version": 1, "reason": "Evidence reviewed"}; evidenced = {**base, "evidence_ids": [UUID]}
    bank = {"request": org_examples()["BankChangeSummary"], "organization_id": UUID, "proposed_bank_revision_id": UUID,
            "verification_evidence_ids": [UUID], "restricted_notes": [], "version": 1}
    e = {"PayoutDraftCreate": draft, "PayoutDraftEdit": {**base, "bank_revision_id": UUID, "items": [item]}, "PayoutFinanceView": payout,
        "PayableAllocation": {"allocation_id": UUID, "organization_id": UUID, "contribution_id": UUID, "available_paise": 100000, "reserved_paise": 0, "consumed_paise": 0, "currency": "INR", "version": 1},
        "PayoutSubmit": base, "PayoutApprove": {**evidenced, "approval_snapshot_id": UUID},
        "PayoutBeginTransfer": {**base, "approval_snapshot_id": UUID, "bank_revision_id": UUID},
        "PayoutUncertain": {**base, "transfer_attempt_id": UUID, "reconciliation_case_id": UUID},
        "PayoutPaid": {**evidenced, "transfer_attempt_id": UUID, "bank_revision_id": UUID, "bank_reference": "UTR-SYNTHETIC", "value_date": "2026-09-11", "amount_paise": 100000, "currency": "INR"},
        "PayoutReconcile": {**evidenced, "bank_report_id": UUID, "reconciliation_snapshot_id": UUID}, "PayoutCancel": evidenced,
        "PayoutFailure": {**evidenced, "transfer_attempt_id": UUID, "no_transfer_decision_id": UUID},
        "PayoutReturn": {**evidenced, "transfer_attempt_id": UUID, "bank_return_reference": "RETURN-SYNTHETIC", "amount_paise": 100000, "currency": "INR", "accounting_decision_id": UUID},
        "PayoutEvidenceCreate": {**evidenced, "transfer_attempt_id": UUID},
        "PayoutEvidenceReceipt": {"id": UUID, "payout_id": UUID, "evidence_ids": [UUID], "version": 1, "status": "ATTACHED", "payment_confirmed": False},
        "OrganizationLiability": {"organization_id": UUID, "currency": "INR", "available_principal_paise": 100000, "reserved_principal_paise": 0, "consumed_principal_paise": 0, "unallocated_capture_recovery_paise": 0, "platform_funded_recovery_paise": 0, "as_of": NOW, "snapshot_id": UUID},
        "FinanceReconciliationEntry": {"id": UUID, "kind": "payout", "subject_id": UUID, "expected_paise": 100000, "observed_paise": None, "currency": "INR", "status": "UNCERTAIN", "case_id": UUID, "snapshot_id": UUID, "as_of": NOW},
        "PayoutOrganizationView": {"id": UUID, "amount_paise": 100000, "currency": "INR", "status": "APPROVED", "transfer_status": "UNCERTAIN", "bank_reference": None, "value_date": None, "returned_paise": 0, "safe_recovery_summary": "Transfer under reconciliation", "version": 1},
        "OrganizationStatement": {"organization_id": UUID, "currency": "INR", "snapshot_id": UUID, "as_of": NOW, "entries": [], "next_cursor": None, "has_more": False, "opening_balance_paise": 0, "closing_balance_paise": 0},
        "FinanceExportCreate": {"report": "payouts", "organization_id": UUID, "from_at": "2026-09-01T00:00:00Z", "to_at": "2026-09-11T00:00:00Z", "format": "csv", "purpose": "Finance review"},
        "FinanceExport": {"id": UUID, "status": "PENDING", "safe_message": "Export queued"}, "BankChangeReview": bank,
        "BankChangeDecision": {**evidenced, "decision": "APPROVE", "proposed_bank_revision_id": UUID, "verification_decision_id": UUID}}
    for name, member in [("PayableAllocationPage", "PayableAllocation"), ("PayoutFinancePage", "PayoutFinanceView"), ("OrganizationLiabilityPage", "OrganizationLiability"),
                         ("FinanceReconciliationPage", "FinanceReconciliationEntry"), ("PayoutOrganizationPage", "PayoutOrganizationView"), ("BankChangeReviewPage", "BankChangeReview")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples(); uncertain = deepcopy(e["PayoutFinanceView"])
    uncertain.update(status="APPROVED", approval_snapshot_id=UUID, approval_requested_at=NOW, approved_by="22222222-2222-4222-8222-222222222222")
    uncertain["transfer_attempts"] = [{"id": UUID, "status": "UNCERTAIN", "started_at": NOW, "bank_reference": None, "value_date": None,
        "amount_paise": 100000, "bank_revision_id": UUID, "reconciliation_case_id": UUID, "version": 1}]
    returned = deepcopy(uncertain); returned["status"] = "RECONCILED"
    returned["transfer_attempts"][0].update(status="CONFIRMED", bank_reference="UTR-SYNTHETIC", value_date="2026-09-11")
    returned["returns"] = [{"id": UUID, "transfer_attempt_id": UUID, "bank_return_reference": "RETURN-SYNTHETIC", "amount_paise": 100000, "recorded_at": NOW, "accounting_decision_id": UUID}]
    rejected = deepcopy(e["BankChangeDecision"]); rejected["decision"] = "REJECT"; del rejected["verification_decision_id"]
    return {"PayoutFinanceView": {"uncertain": uncertain, "returned": returned}, "BankChangeDecision": {"rejected": rejected},
        "FinanceExport": {"ready": {"id": UUID, "status": "READY", "media_id": UUID, "expires_at": NOW, "snapshot_id": UUID}}}


def parameters():
    return {"get_org_statement": [{"name": "cursor", "in": "query", "schema": text(1, 2048)},
                                   {"name": "limit", "in": "query", "schema": integer(1, 50)}]}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value, label in [
        ("PayoutDraftCreate", "status", "PAID", "paid status injection"),
        ("PayoutDraftCreate", "amount_paise", 1, "client total overrides allocations"),
        ("PayoutDraftCreate", "items", [], "empty payout"),
        ("PayoutDraftCreate", "currency", "USD", "unsupported payout currency"),
        ("PayoutApprove", "approved_by", UUID, "approver impersonation"),
        ("PayoutApprove", "amount_paise", 1, "approval changes total"),
        ("PayoutPaid", "amount_paise", 0, "zero paid amount"),
        ("PayoutPaid", "amount_paise", 1.5, "fractional paid paise"),
        ("PayoutPaid", "bank_reference", "", "missing bank reference"),
        ("PayoutPaid", "value_date", "2026-02-30", "impossible bank date"),
        ("PayoutPaid", "evidence_ids", [], "paid without evidence"),
        ("PayoutCancel", "force", True, "uncertainty bypass"),
        ("PayoutReturn", "amount_paise", -1, "negative return"),
        ("PayoutEvidenceReceipt", "payment_confirmed", True, "attachment claims transfer success"),
        ("PayoutOrganizationView", "restricted_notes", ["internal"], "internal notes leaked"),
        ("PayoutOrganizationView", "account_number", "123456", "raw bank leaked"),
        ("FinanceExportCreate", "format", "sql", "unreviewed export format"),
        ("FinanceExport", "download_url", "https://example.invalid/private", "pending export exposes download"),
        ("BankChangeDecision", "account_number", "123456", "review substitutes recipient"),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, label))
    for schema, key in [("PayoutApprove", "approval_snapshot_id"), ("PayoutBeginTransfer", "bank_revision_id"),
                        ("PayoutFailure", "no_transfer_decision_id"), ("PayoutReturn", "accounting_decision_id"), ("BankChangeDecision", "verification_decision_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing bound decision/revision"))
    payload = deepcopy(e["PayoutDraftCreate"]); payload["items"][0]["amount_paise"] = 0
    cases.append(("PayoutDraftCreate", payload, "zero allocation reservation"))
    payload = deepcopy(example_variants()["PayoutFinanceView"]["returned"])
    payload["transfer_attempts"][0]["bank_reference"] = None
    cases.append(("PayoutFinanceView", payload, "confirmed transfer lacks bank reference"))
    return cases
