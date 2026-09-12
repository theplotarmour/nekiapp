"""Immutable impact history and independently authorized effective views."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import QUANTITY, array, HTTPS
from contract_contributions import PAISE
from contract_cases import evidence_ids
from contract_proof import SHA

SHARE_TOKEN = text(43, 128, pattern=r"^[A-Za-z0-9_-]+$")


def schemas():
    s = {}
    s["ImpactResource"] = {"oneOf": [
        obj({"type": enum("MONEY"), "contributed_paise": PAISE, "currency": enum("INR")}),
        obj({"type": enum("ITEM"), "item_type_id": ID, "verified_quantity": QUANTITY, "unit": text(1, 30)}),
        obj({"type": enum("TIME"), "verified_seconds": integer()}),
    ], "discriminator": {"propertyName": "type"}}
    s["ImpactBeneficiaryClaim"] = obj({"mission_id": ID, "reported_count": integer(), "source_decision_id": ID,
        "observed_at": TIME, "scope": enum("mission_reported_not_unique_people")})
    claims = {"resource": ref("ImpactResource"), "beneficiary_claim": nullable(ref("ImpactBeneficiaryClaim")), "attribution_revision_id": ID}
    s["ImpactImmutablePayload"] = obj({"schema_version": enum("impact.v1-draft"), "ledger_id": ID, "sequence": integer(1, 9007199254740991),
        "entry_kind": enum("ISSUANCE", "CORRECTION"), "record_id": ID, "contribution_id": ID, "mission_id": ID, "organization_id": ID,
        "verification_decision_ids": evidence_ids(), "evidence_revision_ids": evidence_ids(), "issued_at": TIME, **claims,
        "supersedes_entry_id": nullable(ID)}, allOf=[{
            "if": {"properties": {"entry_kind": {"const": "CORRECTION"}}}, "then": {"properties": {"supersedes_entry_id": ID}},
            "else": {"properties": {"supersedes_entry_id": {"type": "null"}}}}])
    s["ImpactChainEntry"] = obj({"id": ID, "payload": ref("ImpactImmutablePayload"), "entry_hash": SHA, "previous_hash": SHA})
    s["ImpactEffectiveView"] = obj({**claims, "effective_entry_id": ID, "effective_version": VERSION,
        "trust_status": enum("VERIFIED", "UNDER_REVIEW", "CORRECTED", "CLAIM_WITHDRAWN"), "safe_explanation": nullable(text(1, 1000))})
    s["ImpactRecord"] = obj({"id": ID, "original_entry": ref("ImpactChainEntry"), "effective": ref("ImpactEffectiveView"),
        "mission_title": text(1, 160), "organization_name": text(1, 160), "version": VERSION})
    s["ImpactRecordPage"] = page(ref("ImpactRecord"))
    s["ImpactHistoryPage"] = page(obj({"entry": ref("ImpactChainEntry"), "safe_reason": nullable(text(1, 1000)), "is_current_effective": BOOL}))
    s["ImpactSummary"] = obj({"verified_missions_distinct": integer(), "verified_organizations_distinct": integer(),
        "verified_seconds": integer(), "contributed_paise_in_verified_records": PAISE, "currency": enum("INR"),
        "items": array(obj({"item_type_id": ID, "unit": text(1, 30), "verified_quantity": QUANTITY}), 100),
        "mission_reported_beneficiaries": nullable(integer()), "beneficiary_scope": enum("distinct_mission_reports_not_unique_people"),
        "as_of": TIME, "projection_revision_id": ID})
    s["ImpactCorrectionRequest"] = obj({"expected_version": VERSION, "expected_effective_version": VERSION,
        "reason": text(1, 1000), "evidence_ids": evidence_ids(), "source_decision_id": ID})
    s["ImpactCorrectionView"] = obj({"id": ID, "record_id": ID, "base_effective_version": VERSION,
        "status": enum("REQUESTED", "UNDER_REVIEW", "APPROVED", "REJECTED"), "safe_reason": text(1, 1000),
        "effective_entry_id": nullable(ID), "version": VERSION})
    s["ImpactCorrectionReview"] = obj({"request": ref("ImpactCorrectionView"), "source_decision_id": ID,
        "evidence_ids": evidence_ids(), "proposed_claims": obj(claims), "restricted_notes": array(text(1, 2000), 100), "version": VERSION})
    s["ImpactCorrectionPage"] = page(ref("ImpactCorrectionReview"))
    base = {"expected_version": VERSION, "expected_effective_version": VERSION, "safe_reason": text(1, 1000), "evidence_ids": evidence_ids()}
    s["ImpactCorrectionDecision"] = {"oneOf": [
        obj({**base, "decision": enum("APPROVE"), "review_snapshot_id": ID, "source_decision_id": ID}),
        obj({**base, "decision": enum("REJECT")}),
    ], "discriminator": {"propertyName": "decision"}}
    s["CertificateMetadata"] = obj({"id": ID, "record_id": ID, "effective_entry_id": ID, "effective_version": VERSION,
        "status": enum("CURRENT", "UNDER_REVIEW", "SUPERSEDED", "WITHDRAWN"), "verified_seconds": integer(), "issued_at": TIME,
        "pdf_available": {"type": "boolean", "const": False}})
    s["CertificatePage"] = page(ref("CertificateMetadata"))
    s["ImpactShareCreate"] = obj({"expected_version": VERSION, "expected_effective_version": VERSION, "consent_receipt_id": ID,
        "expires_at": TIME, "include_resource_quantity": BOOL})
    s["ImpactShareGrant"] = obj({"id": ID, "share_url": HTTPS, "expires_at": TIME, "effective_version": VERSION, "version": VERSION})
    s["ImpactSharedView"] = obj({"mission_title": text(1, 160), "organization_name": text(1, 160),
        "contribution_type": enum("MONEY", "ITEM", "TIME"), "verified_resource_label": nullable(text(1, 200)),
        "trust_status": enum("VERIFIED", "CORRECTED"), "as_of": TIME})
    return s


def definitions():
    return {
        "get_impact_summary": (None, "200", "ImpactSummary", [], "Owner effective eligible records, deduplicated by mission/org and compatible item units; unknown beneficiaries stay null."),
        "list_impact_records": (None, "200", "ImpactRecordPage", [], "Owner final records with original immutable entry and current effective claims; not pending activity."),
        "get_impact_record": (None, "200", "ImpactRecord", [], "Authorize owner independently of opaque record ID; preserve historical entry when current trust changes."),
        "get_effective_record_history": (None, "200", "ImpactHistoryPage", [], "Ordered owner-safe issuance/correction history; each entry stays immutable."),
        "request_impact_correction": ("ImpactCorrectionRequest", "201", "ImpactCorrectionView", [], "Bind current effective version and source evidence; request does not mutate original or effective record."),
        "list_certificates": (None, "200", "CertificatePage", [], "Owner verified-hours certificate metadata bound to effective record; no MVP PDF."),
        "get_certificate_metadata": (None, "200", "CertificateMetadata", [], "Show current/superseded/withdrawn status after correction; never use obsolete hours as current."),
        "create_impact_share": ("ImpactShareCreate", "201", "ImpactShareGrant", ["FEATURE_DISABLED"], "AP-04 disabled until privacy approval. When enabled, scoped revocable expiring token, exact consent/effective version and safe field projection."),
        "revoke_impact_share": (None, "204", None, [], "Owner may revoke share even after feature disablement; delete grant, not historical impact."),
        "get_shared_impact": (None, "200", "ImpactSharedView", ["FEATURE_DISABLED", "SHARE_UNAVAILABLE"], "AP-04 disabled until approved. Authenticate opaque path token via hashed lookup; check expiry/revocation/current trust and consent. No bearer session required."),
        "list_impact_correction_queue": (None, "200", "ImpactCorrectionPage", [], "Scoped reviewer queue with proposed claims and restricted source evidence."),
        "decide_impact_correction": ("ImpactCorrectionDecision", "200", "ImpactCorrectionView", [], "Independent approval locks current effective version and ledger head; append correction and rebuild intent atomically. Rejection changes request only."),
    }


def examples():
    resource = {"type": "TIME", "verified_seconds": 7200}
    claims = {"resource": resource, "beneficiary_claim": None, "attribution_revision_id": UUID}
    payload = {"schema_version": "impact.v1-draft", "ledger_id": UUID, "sequence": 1, "entry_kind": "ISSUANCE", "record_id": UUID,
        "contribution_id": UUID, "mission_id": UUID, "organization_id": UUID, "verification_decision_ids": [UUID], "evidence_revision_ids": [UUID],
        "issued_at": NOW, **claims, "supersedes_entry_id": None}
    entry = {"id": UUID, "payload": payload, "entry_hash": "a" * 64, "previous_hash": "0" * 64}
    record = {"id": UUID, "original_entry": entry, "effective": {**claims, "effective_entry_id": UUID, "effective_version": 1,
        "trust_status": "VERIFIED", "safe_explanation": None}, "mission_title": "Synthetic mission", "organization_name": "Synthetic organization", "version": 1}
    request = {"id": UUID, "record_id": UUID, "base_effective_version": 1, "status": "REQUESTED", "safe_reason": "Attendance correction requested", "effective_entry_id": None, "version": 1}
    e = {"ImpactImmutablePayload": payload, "ImpactRecord": record,
        "ImpactSummary": {"verified_missions_distinct": 1, "verified_organizations_distinct": 1, "verified_seconds": 7200,
            "contributed_paise_in_verified_records": 0, "currency": "INR", "items": [], "mission_reported_beneficiaries": None,
            "beneficiary_scope": "distinct_mission_reports_not_unique_people", "as_of": NOW, "projection_revision_id": UUID},
        "ImpactHistoryPage": {"items": [{"entry": entry, "safe_reason": None, "is_current_effective": True}], "next_cursor": None, "has_more": False},
        "ImpactCorrectionRequest": {"expected_version": 1, "expected_effective_version": 1, "reason": request["safe_reason"], "evidence_ids": [UUID], "source_decision_id": UUID},
        "ImpactCorrectionView": request, "ImpactCorrectionReview": {"request": request, "source_decision_id": UUID, "evidence_ids": [UUID], "proposed_claims": claims, "restricted_notes": [], "version": 1},
        "ImpactCorrectionDecision": {"expected_version": 1, "expected_effective_version": 1, "safe_reason": "Source correction reviewed", "evidence_ids": [UUID], "decision": "APPROVE", "review_snapshot_id": UUID, "source_decision_id": UUID},
        "CertificateMetadata": {"id": UUID, "record_id": UUID, "effective_entry_id": UUID, "effective_version": 1, "status": "CURRENT", "verified_seconds": 7200, "issued_at": NOW, "pdf_available": False},
        "ImpactShareCreate": {"expected_version": 1, "expected_effective_version": 1, "consent_receipt_id": UUID, "expires_at": "2026-09-20T00:00:00Z", "include_resource_quantity": False},
        "ImpactShareGrant": {"id": UUID, "share_url": "https://example.invalid/shared/impact/" + "a" * 43, "expires_at": "2026-09-20T00:00:00Z", "effective_version": 1, "version": 1},
        "ImpactSharedView": {"mission_title": "Synthetic mission", "organization_name": "Synthetic organization", "contribution_type": "TIME", "verified_resource_label": None, "trust_status": "VERIFIED", "as_of": NOW}}
    for name, member in [("ImpactRecordPage", "ImpactRecord"), ("CertificatePage", "CertificateMetadata"), ("ImpactCorrectionPage", "ImpactCorrectionReview")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples(); reject = deepcopy(e["ImpactCorrectionDecision"])
    reject["decision"] = "REJECT"; del reject["review_snapshot_id"]; del reject["source_decision_id"]
    variants = {}
    for kind, resource in [("money", {"type": "MONEY", "contributed_paise": 10000, "currency": "INR"}),
                           ("item", {"type": "ITEM", "item_type_id": UUID, "verified_quantity": "2.5", "unit": "kg"})]:
        record = deepcopy(e["ImpactRecord"])
        record["original_entry"]["payload"]["resource"] = resource; record["effective"]["resource"] = resource
        variants[kind] = record
    corrected = deepcopy(e["ImpactRecord"])
    corrected["effective"].update(effective_entry_id="22222222-2222-4222-8222-222222222222", effective_version=2, trust_status="CORRECTED", safe_explanation="Hours corrected", resource={"type": "TIME", "verified_seconds": 3600})
    variants["corrected"] = corrected
    return {"ImpactRecord": variants, "ImpactCorrectionDecision": {"rejected": reject}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [("ImpactImmutablePayload", "owner_name", "private"), ("ImpactImmutablePayload", "exact_location", "private"),
        ("ImpactImmutablePayload", "entry_kind", "CORRECTION"), ("ImpactImmutablePayload", "sequence", 0),
        ("ImpactSummary", "beneficiary_scope", "unique_people"), ("ImpactCorrectionRequest", "new_total", 100),
        ("ImpactCorrectionDecision", "rewrite_original", True), ("CertificateMetadata", "pdf_available", True),
        ("ImpactSharedView", "owner_user_id", UUID), ("ImpactSharedView", "evidence_ids", [UUID]),
        ("ImpactSharedView", "trust_status", "UNDER_REVIEW"), ("ImpactShareCreate", "public_forever", True)]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid impact privacy or mutation claim"))
    payload = deepcopy(e["ImpactImmutablePayload"]); payload["resource"]["contributed_paise"] = 100
    cases.append(("ImpactImmutablePayload", payload, "mixed resource quantities"))
    for schema, key in [("ImpactCorrectionDecision", "expected_effective_version"), ("ImpactCorrectionDecision", "review_snapshot_id"), ("ImpactShareCreate", "consent_receipt_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing consent or correction binding"))
    return cases
