"""Media processing and human proof review are separate contracts."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import HTTPS, QUANTITY, array
from contract_cases import evidence_ids

PURPOSE = enum("mission_image", "proof", "item_photo", "avatar", "org_document", "org_logo", "update_image")
SHA = text(64, 64, pattern=r"^[a-f0-9]{64}$")


def schemas():
    s = {}
    s["MediaSubject"] = {"oneOf": [obj({"type": enum(kind), "id": ID}) for kind in
                                   ("mission", "contribution", "shipment", "assignment", "organization")]
                           + [obj({"type": enum("self")})], "discriminator": {"propertyName": "type"}}
    s["MediaUploadRequest"] = obj({"purpose": PURPOSE, "subject": ref("MediaSubject"), "declared_mime": text(1, 150),
        "declared_bytes": integer(1, 104857600), "sha256": SHA, "is_illustration": BOOL, "consent_receipt_id": nullable(ID)},
        allOf=[{"if": {"properties": {"purpose": {"const": "proof"}}}, "then": {"properties": {"is_illustration": {"const": False}}}}])
    s["MediaUploadGrant"] = obj({"media_id": ID, "upload_session_id": ID, "method": enum("PUT"), "upload_url": HTTPS,
        "expires_at": TIME, "required_headers": array(obj({"name": text(1, 100), "value": text(1, 1000)}), 20),
        "max_bytes": integer(1, 104857600), "version": VERSION})
    s["MediaComplete"] = obj({"expected_version": VERSION, "upload_session_id": ID})
    s["MediaStatus"] = obj({"id": ID, "purpose": PURPOSE, "status": enum("AUTHORIZED", "UPLOADED", "PROCESSING", "READY", "REJECTED", "DELETION_PENDING", "DELETED"),
        "revision_id": nullable(ID), "safe_reason": nullable(text(1, 500)), "is_illustration": BOOL, "version": VERSION})
    s["MediaReadRequest"] = obj({"revision_id": ID, "rendition": enum("original", "safe_preview", "redacted"),
        "use": enum("own_submission", "review", "participant_evidence", "profile")}, allOf=[{
            "if": {"properties": {"use": {"const": "participant_evidence"}}},
            "then": {"properties": {"rendition": {"const": "redacted"}}}}])
    s["MediaReadGrant"] = obj({"media_id": ID, "revision_id": ID, "rendition": enum("original", "safe_preview", "redacted"),
        "read_url": HTTPS, "expires_at": TIME, "cache_policy": enum("private_no_store")})
    s["MediaRetry"] = obj({"expected_version": VERSION, "previous_upload_session_id": ID})
    s["MediaReprocess"] = obj({"expected_version": VERSION, "source_revision_id": ID, "reason": text(1, 1000)})
    s["MediaRedactionRequest"] = obj({"expected_version": VERSION, "source_revision_id": ID, "case_id": ID, "reason": text(1, 1000),
        "regions": {**array(obj({"frame_at_ms": nullable(integer()), "x": {"type": "number", "minimum": 0, "maximum": 1},
            "y": {"type": "number", "minimum": 0, "maximum": 1}, "width": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
            "height": {"type": "number", "exclusiveMinimum": 0, "maximum": 1}, "action": enum("blur", "cover")}), 100), "minItems": 1},
        "consent_decision_id": ID})
    s["MediaOperation"] = obj({"operation_id": ID, "media_id": ID, "status": enum("PENDING"), "completed": {"type": "boolean", "const": False}})
    s["ProofSubject"] = {"oneOf": [obj({"type": enum(kind), "id": ID}) for kind in ("mission", "contribution", "shipment", "assignment")],
                          "discriminator": {"propertyName": "type"}}
    s["ProofRequirements"] = obj({"mission_id": ID, "requirements_revision_id": ID,
        "requirements": array(obj({"id": ID, "kind": enum("photo", "video", "document", "acknowledgement", "quantity", "beneficiary_claim", "capture_location"),
            "required": BOOL, "safe_description": text(1, 1000), "minimum_count": integer(0, 100)}), 100), "version": VERSION})
    media = obj({"media_id": ID, "media_revision_id": ID, "consent_receipt_id": ID})
    claims = obj({"quantities": array(obj({"need_id": ID, "quantity": QUANTITY, "unit": text(1, 30)}), 50),
        "beneficiaries": nullable(obj({"reported_count": integer(), "source_evidence_id": ID, "observed_at": TIME,
            "scope": enum("mission_reported_not_unique_people")}))})
    draft = {"requirements_revision_id": ID, "media": array(media, 50), "claims": claims,
        "acknowledgement_ids": array(ID, 50), "metadata_exception_request": nullable(obj({"reason": text(1, 1000), "evidence_ids": evidence_ids()}))}
    s["ProofDraftCreate"] = obj({"subject": ref("ProofSubject"), "requirements_revision_id": ID})
    s["ProofDraftEdit"] = obj({**draft, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["ProofDraft"] = obj({"id": ID, "subject": ref("ProofSubject"), **draft, "version": VERSION})
    s["ProofDraftPage"] = page(ref("ProofDraft"))
    s["ProofSubmit"] = obj({"draft_id": ID, "expected_draft_version": VERSION, "requirements_revision_id": ID,
        "on_behalf_reason": nullable(text(1, 1000))})
    status = enum("NOT_REVIEWED", "UNDER_REVIEW", "NEEDS_MORE_INFORMATION", "VERIFIED", "REJECTED")
    common = {"id": ID, "subject": ref("ProofSubject"), "status": status, "submission_revision_id": ID,
              "safe_status_message": text(1, 1000), "version": VERSION}
    s["ProofSubmitterView"] = obj({**common, "view": enum("submitter"), **draft, "requested_information": array(text(1, 1000), 30)})
    s["ProofParticipantView"] = obj({**common, "view": enum("participant"),
        "approved_derivatives": array(obj({"media_id": ID, "media_revision_id": ID, "disclosure_decision_id": ID}), 50)})
    s["ProofScopedView"] = {"oneOf": [ref("ProofSubmitterView"), ref("ProofParticipantView")], "discriminator": {"propertyName": "view"}}
    s["ProofScopedPage"] = page(ref("ProofScopedView"))
    s["ProofVersionPage"] = page(ref("ProofSubmitterView"))
    s["ProofResubmit"] = obj({"expected_version": VERSION, "prior_decision_id": ID, "draft_id": ID, "expected_draft_version": VERSION})
    case = {"expected_version": VERSION, "submission_revision_id": ID, "reason": text(1, 1000), "evidence_ids": evidence_ids()}
    s["ProofCaseRequest"] = obj(case)
    s["ProofCaseReceipt"] = obj({"case_id": ID, "proof_id": ID, "status": enum("OPEN"), "verification_changed": {"type": "boolean", "const": False}})
    s["ProofReview"] = obj({"submission": ref("ProofSubmitterView"), "restricted_notes": array(text(1, 2000), 100),
        "checks": array(obj({"check_id": text(1, 100), "result": enum("PASS", "FAIL", "REQUIRES_HUMAN_REVIEW"), "evidence_revision_id": ID}), 100), "version": VERSION})
    s["ProofReviewPage"] = page(ref("ProofReview"))
    s["ProofStartReview"] = obj({"expected_version": VERSION, "submission_revision_id": ID})
    decision = {"expected_version": VERSION, "submission_revision_id": ID, "safe_reason": text(1, 1000)}
    s["ProofDecision"] = {"oneOf": [
        obj({**decision, "decision": enum("VERIFY"), "checklist": {**array(ref("ReviewChecklistEntry"), 100), "minItems": 1},
            "accepted_claim_revision_id": ID, "disclosure_decision_id": ID}),
        obj({**decision, "decision": enum("NEEDS_MORE_INFORMATION"), "requested_information": {**array(text(1, 1000), 30), "minItems": 1}}),
        obj({**decision, "decision": enum("REJECT"), "evidence_ids": evidence_ids()}),
    ], "discriminator": {"propertyName": "decision"}}
    s["ProofAppealOpen"] = obj({**case, "case_id": ID, "policy_decision_id": ID})
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, code="200", errors=()):
        d[op] = (request, code, response, list(errors), effect)
    add("authorize_upload", "MediaUploadRequest", "MediaUploadGrant", "Authorize immutable purpose/subject and server-owned object key; declared MIME/hash/size are not validation of actual bytes.", "201")
    add("complete_upload", "MediaComplete", "MediaStatus", "Check uploaded bytes/key/version/checksum and queue scan/transcoding; duplicate completion cannot create a second asset revision.")
    add("get_media_status", None, "MediaStatus", "Current purpose/owner-authorized metadata only; no storage key, EXIF or private URL.")
    add("authorize_media_read", "MediaReadRequest", "MediaReadGrant", "Authorize current purpose/relationship/processing and permitted rendition. Requesting original does not grant it; no arbitrary supplied URL fetch.", errors=["MEDIA_NOT_READY"])
    add("retry_media_upload", "MediaRetry", "MediaUploadGrant", "Refresh expired upload session only for eligible unfinished asset; never overwrite a frozen evidence revision.")
    add("request_media_deletion", None, "MediaOperation", "Record policy-scoped deletion request with retention/hold checks; acknowledgement is not completed removal.", "202")
    add("reprocess_media", "MediaReprocess", "MediaOperation", "Create new derived revision through safe processing; preserve frozen evidence provenance.", "202")
    add("request_media_redaction", "MediaRedactionRequest", "MediaOperation", "Review purpose/regions/consent and queue redacted derivative; never mutate immutable proof bytes.", "202")
    add("get_proof_requirements", None, "ProofRequirements", "Subject-scoped current requirements; response does not authorize other participants' evidence.")
    add("create_proof_draft", "ProofDraftCreate", "ProofDraft", "Server resolves subject/mission relation and submitter scope; new editable draft, not proof verification.", "201")
    add("list_proof_drafts", None, "ProofDraftPage", "Only authorized submitter drafts.")
    add("get_proof_draft", None, "ProofDraft", "Current draft subject authorization.")
    add("edit_proof_draft", "ProofDraftEdit", "ProofDraft", "Versioned draft only; frozen submissions never patched.")
    add("remove_proof_draft", None, None, "Delete unsubmitted draft under retention rules; no deletion of reviewed evidence/history.", "204")
    add("submit_proof", "ProofSubmit", "ProofSubmitterView", "Freeze subject, processed non-illustration evidence revisions, claims and consent; delegated ops must supply reason.", "201", ["PROOF_NOT_READY", "SUBJECT_SCOPE_DENIED"])
    add("list_scoped_proofs", None, "ProofScopedPage", "Server chooses submitter or participant projection per subject, never generic mission membership.")
    add("get_scoped_proof", None, "ProofScopedView", "Participants see approved derivatives only; original metadata remains restricted.")
    add("list_proof_versions", None, "ProofVersionPage", "Authorized submitter immutable submission cycles; current media read policy applies independently.")
    add("resubmit_proof", "ProofResubmit", "ProofSubmitterView", "Freeze new complete revision preserving prior decision and evidence.", errors=["PROOF_NOT_READY"])
    add("request_proof_appeal", "ProofCaseRequest", "ProofCaseReceipt", "Open appeal request; no automatic rejection reversal.", "201")
    add("list_proof_review_queue", None, "ProofReviewPage", "Assigned reviewer queue with scope-specific evidence.")
    add("get_proof_review", None, "ProofReview", "Restricted review metadata; automatic checks are review signals only.")
    add("start_proof_review", "ProofStartReview", "ProofReview", "Assign exact current submission revision under lock.")
    add("decide_proof", "ProofDecision", "ProofReview", "Human scope/independence/checklist and accepted claims required; verification emits issuance intent, never falsely announces final record.")
    add("open_proof_appeal_review", "ProofAppealOpen", "ProofReview", "Independent accepted appeal opens a new review cycle, preserving rejected decision.")
    add("challenge_verified_proof", "ProofCaseRequest", "ProofCaseReceipt", "Open scoped challenge without erasing historical verification; apply approved trust/issuance hold workflow.", "201")
    return d


def examples():
    subject = {"type": "shipment", "id": UUID}
    draft_fields = {"requirements_revision_id": UUID, "media": [{"media_id": UUID, "media_revision_id": UUID, "consent_receipt_id": UUID}],
        "claims": {"quantities": [{"need_id": UUID, "quantity": "2", "unit": "kg"}], "beneficiaries": None},
        "acknowledgement_ids": [UUID], "metadata_exception_request": None}
    common = {"id": UUID, "subject": subject, "status": "NOT_REVIEWED", "submission_revision_id": UUID, "safe_status_message": "Awaiting review", "version": 1}
    submitter = {**common, "view": "submitter", **draft_fields, "requested_information": []}
    participant = {**common, "view": "participant", "approved_derivatives": []}
    case = {"expected_version": 1, "submission_revision_id": UUID, "reason": "Please review evidence", "evidence_ids": [UUID]}
    e = {"MediaUploadRequest": {"purpose": "proof", "subject": subject, "declared_mime": "image/jpeg", "declared_bytes": 1024,
            "sha256": "a" * 64, "is_illustration": False, "consent_receipt_id": UUID},
        "MediaUploadGrant": {"media_id": UUID, "upload_session_id": UUID, "method": "PUT", "upload_url": "https://storage.example.invalid/synthetic-upload",
            "expires_at": NOW, "required_headers": [{"name": "Content-Type", "value": "image/jpeg"}], "max_bytes": 1024, "version": 1},
        "MediaComplete": {"expected_version": 1, "upload_session_id": UUID},
        "MediaStatus": {"id": UUID, "purpose": "proof", "status": "PROCESSING", "revision_id": None, "safe_reason": None, "is_illustration": False, "version": 1},
        "MediaReadRequest": {"revision_id": UUID, "rendition": "redacted", "use": "participant_evidence"},
        "MediaReadGrant": {"media_id": UUID, "revision_id": UUID, "rendition": "redacted", "read_url": "https://storage.example.invalid/synthetic-read", "expires_at": NOW, "cache_policy": "private_no_store"},
        "MediaRetry": {"expected_version": 1, "previous_upload_session_id": UUID}, "MediaReprocess": {"expected_version": 1, "source_revision_id": UUID, "reason": "Regenerate safe preview"},
        "MediaRedactionRequest": {"expected_version": 1, "source_revision_id": UUID, "case_id": UUID, "reason": "Protect identifying details",
            "regions": [{"frame_at_ms": None, "x": 0.1, "y": 0.1, "width": 0.2, "height": 0.2, "action": "blur"}], "consent_decision_id": UUID},
        "MediaOperation": {"operation_id": UUID, "media_id": UUID, "status": "PENDING", "completed": False},
        "ProofRequirements": {"mission_id": UUID, "requirements_revision_id": UUID, "requirements": [{"id": UUID, "kind": "photo", "required": True, "safe_description": "Actual receipt evidence", "minimum_count": 1}], "version": 1},
        "ProofDraftCreate": {"subject": subject, "requirements_revision_id": UUID}, "ProofDraftEdit": {"expected_version": 1, "claims": draft_fields["claims"]},
        "ProofDraft": {"id": UUID, "subject": subject, **draft_fields, "version": 1},
        "ProofSubmit": {"draft_id": UUID, "expected_draft_version": 1, "requirements_revision_id": UUID, "on_behalf_reason": None},
        "ProofSubmitterView": submitter, "ProofParticipantView": participant, "ProofScopedView": participant,
        "ProofResubmit": {"expected_version": 1, "prior_decision_id": UUID, "draft_id": UUID, "expected_draft_version": 1},
        "ProofCaseRequest": case, "ProofCaseReceipt": {"case_id": UUID, "proof_id": UUID, "status": "OPEN", "verification_changed": False},
        "ProofReview": {"submission": submitter, "restricted_notes": [], "checks": [], "version": 1},
        "ProofStartReview": {"expected_version": 1, "submission_revision_id": UUID},
        "ProofDecision": {"expected_version": 1, "submission_revision_id": UUID, "safe_reason": "Evidence accepted", "decision": "VERIFY",
            "checklist": [{"check_id": "receipt", "outcome": "PASS", "evidence_id": UUID, "exception_decision_id": None}], "accepted_claim_revision_id": UUID, "disclosure_decision_id": UUID},
        "ProofAppealOpen": {**case, "case_id": UUID, "policy_decision_id": UUID}}
    for name, member in [("ProofDraftPage", "ProofDraft"), ("ProofScopedPage", "ProofParticipantView"), ("ProofVersionPage", "ProofSubmitterView"), ("ProofReviewPage", "ProofReview")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples(); base = {"expected_version": 1, "submission_revision_id": UUID, "safe_reason": "Review decision"}
    return {"ProofScopedView": {"submitter": e["ProofSubmitterView"]}, "ProofDecision": {
        "information": {**base, "decision": "NEEDS_MORE_INFORMATION", "requested_information": ["Receipt required"]},
        "rejected": {**base, "decision": "REJECT", "evidence_ids": [UUID]}}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [
        ("MediaUploadRequest", "object_key", "other-owner/key"), ("MediaUploadRequest", "owner_user_id", UUID),
        ("MediaUploadRequest", "declared_bytes", 0), ("MediaUploadRequest", "sha256", "bad"),
        ("MediaUploadRequest", "is_illustration", True), ("MediaReadRequest", "rendition", "original"),
        ("MediaComplete", "scan_status", "CLEAN"), ("MediaStatus", "raw_exif", {"gps": "private"}),
        ("MediaReadRequest", "url", "https://example.invalid/arbitrary"), ("MediaOperation", "completed", True),
        ("ProofDraftCreate", "mission_id", UUID), ("ProofDraftEdit", "status", "VERIFIED"),
        ("ProofParticipantView", "media", e["ProofSubmitterView"]["media"]), ("ProofParticipantView", "restricted_notes", ["private"]),
        ("ProofDecision", "decision", "EXPIRED"), ("ProofDecision", "checklist", []),
        ("ProofCaseReceipt", "verification_changed", True), ("ProofSubmit", "impact_record_id", UUID),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid proof/media authority or private field"))
    for schema, key in [("ProofSubmit", "expected_draft_version"), ("ProofDecision", "accepted_claim_revision_id"),
                        ("ProofDecision", "disclosure_decision_id"), ("ProofResubmit", "prior_decision_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing frozen revision or decision"))
    return cases
