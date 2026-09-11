"""Shipment custody and current-assignment field access draft contracts."""

from copy import deepcopy
from contract_identity import ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import COORD, QUANTITY, array
from contract_cases import evidence_ids


def schemas():
    s = {}
    quantity = obj({"need_id": ID, "quantity": QUANTITY, "unit": text(1, 30)})
    quantities = {**array(quantity, 50), "minItems": 1}
    s["PickupSlot"] = obj({"id": ID, "mission_id": ID, "starts_at": TIME, "ends_at": TIME, "available_places": integer(), "version": VERSION})
    s["PickupSlotPage"] = page(ref("PickupSlot"))
    s["ShipmentSummary"] = obj({"id": ID, "contribution_id": ID, "mission_id": ID, "mode": enum("pickup", "dropoff"),
        "status": enum("CREATED", "UNASSIGNED", "VOLUNTEER_ASSIGNED", "PICKUP_READY", "PICKED_UP", "IN_TRANSIT", "ARRIVED", "DELIVERED", "VERIFIED", "CANCELLED"),
        "pickup_window": nullable(obj({"starts_at": TIME, "ends_at": TIME})), "schedule_revision_id": ID,
        "assignment_revision_id": nullable(ID), "custody_revision_id": nullable(ID), "accepted_receipt_id": nullable(ID),
        "delay": nullable(obj({"safe_reason": text(1, 500), "estimated_arrival_at": nullable(TIME), "estimate_as_of": TIME})),
        "safe_recovery_summary": nullable(text(1, 1000)), "version": VERSION}, allOf=[{
            "if": {"properties": {"status": {"enum": ["DELIVERED", "VERIFIED"]}}},
            "then": {"properties": {"accepted_receipt_id": ID}}}])
    s["ShipmentSummaryPage"] = page(ref("ShipmentSummary"))
    address = obj({"line1": text(1, 200), "line2": nullable(text(1, 200)), "locality": text(1, 120),
                   "pincode": text(6, 6, pattern=r"^[1-9][0-9]{5}$"), "point": COORD})
    contact = {"oneOf": [obj({"status": enum("WITHHELD")}), obj({"status": enum("CONSENTED"),
        "display_name": text(1, 120), "phone_e164": text(8, 16, pattern=r"^\+[1-9][0-9]{7,14}$"), "consent_revision_id": ID})]}
    s["ShipmentFieldDetails"] = obj({"shipment_id": ID, "assignment_revision_id": ID, "access_grant_id": ID, "expires_at": TIME,
        "pickup_address": address, "destination_address": address, "pickup_contact": contact,
        "handling_instructions": text(0, 2000), "expected_quantities": quantities, "version": VERSION})
    base = {"expected_version": VERSION, "reason": text(1, 1000)}
    field = {"expected_version": VERSION, "assignment_revision_id": ID, "client_recorded_at": TIME}
    capture = {**field, "evidence_ids": evidence_ids(), "point": nullable(COORD)}
    s["ShipmentCommand"] = obj(base)
    s["ShipmentReschedule"] = obj({**base, "pickup_slot_id": ID, "expected_slot_version": VERSION, "schedule_revision_id": ID})
    s["ShipmentReadiness"] = obj({**field, "schedule_revision_id": ID})
    s["ShipmentPickup"] = obj({**capture, "received_quantities": quantities, "source_acknowledgement_id": ID})
    s["ShipmentDepart"] = obj({**field, "custody_revision_id": ID, "tracking_consent_receipt_id": nullable(ID)})
    s["ShipmentArrival"] = obj(capture)
    s["ShipmentReceiptSubmit"] = obj({**capture, "custody_revision_id": ID, "received_quantities": quantities})
    s["ShipmentReceiptPending"] = obj({"id": ID, "shipment_id": ID, "received_quantities": quantities, "version": VERSION,
        "status": enum("PENDING_ACKNOWLEDGEMENT"), "delivery_accepted": {"type": "boolean", "const": False}})
    s["ShipmentReceiptAccept"] = obj({**base, "receipt_revision_id": ID, "evidence_ids": evidence_ids(), "received_quantities": quantities})
    s["DropoffAccept"] = obj({**base, "source_acknowledgement_id": ID, "evidence_ids": evidence_ids(), "received_quantities": quantities})
    s["ShipmentPingBatch"] = obj({"expected_version": VERSION, "assignment_revision_id": ID, "tracking_consent_receipt_id": ID,
        "samples": {**array(obj({"sample_id": ID, "recorded_at": TIME, "point": COORD,
            "accuracy_m": {"type": "number", "minimum": 0, "maximum": 100000}, "speed_mps": nullable({"type": "number", "minimum": 0, "maximum": 1000}),
            "is_mock_reported": {"type": "boolean"}}), 100), "minItems": 1, "uniqueItems": True}})
    s["ShipmentPingReceipt"] = obj({"operation_id": ID, "status": enum("RECORDED"), "accepted_sample_ids": array(ID, 100),
        "rejected_samples": array(obj({"sample_id": ID, "code": enum("STALE", "INVALID_WINDOW", "DUPLICATE", "ACCURACY_REJECTED")}), 100),
        "delivery_accepted": {"type": "boolean", "const": False}})
    s["ShipmentIssueCreate"] = obj({**base, "category": enum("delay", "missing_items", "damaged_items", "access", "safety", "other"),
        "evidence_ids": array(ID, 50)})
    s["ShipmentIssueReceipt"] = obj({"case_id": ID, "shipment_id": ID, "status": enum("OPEN"), "custody_changed": {"type": "boolean", "const": False}})
    s["ShipmentAssign"] = obj({**base, "volunteer_id": ID, "schedule_revision_id": ID})
    s["ShipmentUnassign"] = obj({**base, "assignment_revision_id": ID, "evidence_ids": evidence_ids()})
    s["ShipmentDelay"] = obj({**base, "estimated_arrival_at": nullable(TIME), "estimate_basis": text(1, 500), "estimate_as_of": TIME})
    exception = {**base, "case_id": ID, "policy_decision_id": ID, "evidence_ids": evidence_ids()}
    s["ShipmentCustodyHandoff"] = obj({**exception, "custody_revision_id": ID, "from_acknowledgement_id": ID, "to_acknowledgement_id": ID,
        "disposition": {"oneOf": [obj({"kind": enum("replacement_volunteer"), "volunteer_id": ID}),
                                   obj({"kind": enum("return_to_source"), "source_receipt_id": ID})]},
        "received_quantities": quantities})
    s["ShipmentOpsPickup"] = obj({**exception, "assignment_revision_id": ID, "occurred_at": TIME,
                                   "source_acknowledgement_id": ID, "received_quantities": quantities})
    s["ShipmentReceiptException"] = obj({**exception, "custody_revision_id": ID, "occurred_at": TIME, "received_quantities": quantities})
    return s


def definitions():
    d = {}
    def add(op, request, response, effect, code="200", errors=()):
        d[op] = (request, code, response, list(errors), effect)
    add("list_pickup_slots", None, "PickupSlotPage", "Serviceable scoped slot candidates; no capacity reservation.")
    add("list_assigned_shipments", None, "ShipmentSummaryPage", "Current assigned work; list never includes private pickup address.")
    add("get_shipment", None, "ShipmentSummary", "Participant-safe physical state and independent delay/recovery metadata.")
    add("get_active_field_details", None, "ShipmentFieldDetails", "Current approved assignee and access window only; recheck assignment revision, consent and revocation. Never cache after expiry.", errors=["ASSIGNMENT_ACCESS_EXPIRED"])
    for op in ("reschedule_pickup", "reschedule_ops_pickup"):
        add(op, "ShipmentReschedule", "ShipmentSummary", "Pre-pickup only; atomically replace slot reservations and explicitly reconcile current assignment.", errors=["SLOT_FULL", "RESCHEDULE_NOT_ALLOWED"])
    for op in ("cancel_pickup", "cancel_ops_pickup"):
        add(op, "ShipmentCommand", "ShipmentSummary", "Serialize against pickup, release once and revoke access; after custody use recovery case.", errors=["CUSTODY_ALREADY_TRANSFERRED"])
    add("acknowledge_pickup_readiness", "ShipmentReadiness", "ShipmentSummary", "Current assignment/window acknowledged; no physical pickup claimed.", errors=["ASSIGNMENT_NOT_CURRENT"])
    add("record_pickup", "ShipmentPickup", "ShipmentSummary", "Actual quantities and accepted source acknowledgement transfer custody under lock.", errors=["ASSIGNMENT_NOT_CURRENT", "MEDIA_NOT_READY"])
    add("start_delivery_route", "ShipmentDepart", "ShipmentSummary", "Current custody required; optional tracking requires current foreground consent.", errors=["CUSTODY_NOT_HELD"])
    add("record_arrival", "ShipmentArrival", "ShipmentSummary", "Record arrival evidence only; GPS never establishes destination receipt.", errors=["ASSIGNMENT_NOT_CURRENT"])
    add("submit_delivery_receipt", "ShipmentReceiptSubmit", "ShipmentReceiptPending", "Persist proposed receipt revision; await destination acknowledgement or reviewed exception.", errors=["ASSIGNMENT_NOT_CURRENT", "MEDIA_NOT_READY"])
    add("submit_location_pings", "ShipmentPingBatch", "ShipmentPingReceipt", "Current assignment/access/consent gate before all samples; dedupe IDs and validate time/accuracy. Does not change physical state.")
    add("report_shipment_issue", "ShipmentIssueCreate", "ShipmentIssueReceipt", "Current or historical participant case, without changing custody or physical status.", "201")
    add("acknowledge_delivery", "ShipmentReceiptAccept", "ShipmentSummary", "Destination org accepts exact receipt and actual quantities; end tracking/access window, verification remains separate.")
    add("acknowledge_dropoff", "DropoffAccept", "ShipmentSummary", "Allowed dropoff mode only; org acknowledges actual quantities without creating a courier route.", errors=["DROPOFF_NOT_ALLOWED"])
    add("get_dispatch_board", None, "ShipmentSummaryPage", "Scoped operational board with state/schedule; private access separately authorized.")
    add("assign_pickup_volunteer", "ShipmentAssign", "ShipmentSummary", "Check current approval/clearance/availability under locks; create assignment revision and bounded access grant.", errors=["VOLUNTEER_INELIGIBLE"])
    add("unassign_pickup_volunteer", "ShipmentUnassign", "ShipmentSummary", "Revoke old assignment and access before custody only; recovery handles items already carried.", errors=["CUSTODY_ALREADY_TRANSFERRED"])
    add("record_pickup_delay", "ShipmentDelay", "ShipmentSummary", "Versioned honest estimate on nonterminal shipment, not a physical lifecycle regression.")
    add("record_custody_handoff", "ShipmentCustodyHandoff", "ShipmentSummary", "Two-sided acknowledgements and reviewed disposition; revoke prior access, append custody history. A return is not verified donation.")
    add("record_ops_pickup", "ShipmentOpsPickup", "ShipmentSummary", "Step-up exception with case/policy and actual pickup evidence; no generic status override.")
    add("record_ops_receipt_exception", "ShipmentReceiptException", "ShipmentSummary", "Reviewed receipt exception with quantities and custody evidence; preserve missing-party exception history.")
    return d


def examples():
    quantities = [{"need_id": UUID, "quantity": "2", "unit": "kg"}]
    window = {"starts_at": "2026-09-12T04:30:00Z", "ends_at": "2026-09-12T06:30:00Z"}
    shipment = {"id": UUID, "contribution_id": UUID, "mission_id": UUID, "mode": "pickup", "status": "VOLUNTEER_ASSIGNED",
        "pickup_window": window, "schedule_revision_id": UUID, "assignment_revision_id": UUID, "custody_revision_id": None,
        "accepted_receipt_id": None, "delay": None, "safe_recovery_summary": None, "version": 1}
    base = {"expected_version": 1, "reason": "Operational review"}
    field = {"expected_version": 1, "assignment_revision_id": UUID, "client_recorded_at": NOW}
    capture = {**field, "evidence_ids": [UUID], "point": None}
    exception = {**base, "case_id": UUID, "policy_decision_id": UUID, "evidence_ids": [UUID]}
    address = {"line1": "Synthetic pickup address", "line2": None, "locality": "Delhi", "pincode": "110001", "point": {"latitude": 28.6, "longitude": 77.2}}
    e = {"PickupSlot": {"id": UUID, "mission_id": UUID, **window, "available_places": 2, "version": 1}, "ShipmentSummary": shipment,
        "ShipmentFieldDetails": {"shipment_id": UUID, "assignment_revision_id": UUID, "access_grant_id": UUID, "expires_at": "2026-09-12T07:00:00Z",
            "pickup_address": address, "destination_address": address, "pickup_contact": {"status": "WITHHELD"}, "handling_instructions": "Keep dry", "expected_quantities": quantities, "version": 1},
        "ShipmentCommand": base, "ShipmentReschedule": {**base, "pickup_slot_id": UUID, "expected_slot_version": 1, "schedule_revision_id": UUID},
        "ShipmentReadiness": {**field, "schedule_revision_id": UUID}, "ShipmentPickup": {**capture, "received_quantities": quantities, "source_acknowledgement_id": UUID},
        "ShipmentDepart": {**field, "custody_revision_id": UUID, "tracking_consent_receipt_id": None}, "ShipmentArrival": capture,
        "ShipmentReceiptSubmit": {**capture, "custody_revision_id": UUID, "received_quantities": quantities},
        "ShipmentReceiptPending": {"id": UUID, "shipment_id": UUID, "received_quantities": quantities, "version": 1, "status": "PENDING_ACKNOWLEDGEMENT", "delivery_accepted": False},
        "ShipmentReceiptAccept": {**base, "receipt_revision_id": UUID, "evidence_ids": [UUID], "received_quantities": quantities},
        "DropoffAccept": {**base, "source_acknowledgement_id": UUID, "evidence_ids": [UUID], "received_quantities": quantities},
        "ShipmentPingBatch": {"expected_version": 1, "assignment_revision_id": UUID, "tracking_consent_receipt_id": UUID,
            "samples": [{"sample_id": UUID, "recorded_at": NOW, "point": {"latitude": 28.6, "longitude": 77.2}, "accuracy_m": 20, "speed_mps": None, "is_mock_reported": False}]},
        "ShipmentPingReceipt": {"operation_id": UUID, "status": "RECORDED", "accepted_sample_ids": [UUID], "rejected_samples": [], "delivery_accepted": False},
        "ShipmentIssueCreate": {**base, "category": "access", "evidence_ids": []}, "ShipmentIssueReceipt": {"case_id": UUID, "shipment_id": UUID, "status": "OPEN", "custody_changed": False},
        "ShipmentAssign": {**base, "volunteer_id": UUID, "schedule_revision_id": UUID}, "ShipmentUnassign": {**base, "assignment_revision_id": UUID, "evidence_ids": [UUID]},
        "ShipmentDelay": {**base, "estimated_arrival_at": None, "estimate_basis": "Awaiting route update", "estimate_as_of": NOW},
        "ShipmentCustodyHandoff": {**exception, "custody_revision_id": UUID, "from_acknowledgement_id": UUID, "to_acknowledgement_id": UUID,
            "disposition": {"kind": "replacement_volunteer", "volunteer_id": UUID}, "received_quantities": quantities},
        "ShipmentOpsPickup": {**exception, "assignment_revision_id": UUID, "occurred_at": NOW, "source_acknowledgement_id": UUID, "received_quantities": quantities},
        "ShipmentReceiptException": {**exception, "custody_revision_id": UUID, "occurred_at": NOW, "received_quantities": quantities}}
    for name, member in [("PickupSlotPage", "PickupSlot"), ("ShipmentSummaryPage", "ShipmentSummary")]:
        e[name] = {"items": [deepcopy(e[member])], "next_cursor": None, "has_more": False}
    return e


def example_variants():
    e = examples(); returned = deepcopy(e["ShipmentCustodyHandoff"])
    returned["disposition"] = {"kind": "return_to_source", "source_receipt_id": UUID}
    contact = deepcopy(e["ShipmentFieldDetails"])
    contact["pickup_contact"] = {"status": "CONSENTED", "display_name": "Synthetic contact", "phone_e164": "+919000000001", "consent_revision_id": UUID}
    delayed = deepcopy(e["ShipmentSummary"])
    delayed["delay"] = {"safe_reason": "Route update pending", "estimated_arrival_at": None, "estimate_as_of": NOW}
    return {"ShipmentCustodyHandoff": {"return": returned}, "ShipmentFieldDetails": {"consented_contact": contact}, "ShipmentSummary": {"delayed": delayed}}


def parameters():
    return {"list_pickup_slots": [{"name": "mission_id", "in": "query", "required": True, "schema": ID},
        {"name": "address_id", "in": "query", "required": True, "schema": ID}],
        "get_active_field_details": [{"name": "assignment_revision_id", "in": "query", "required": True, "schema": ID}]}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [
        ("ShipmentSummary", "pickup_address", "private"), ("ShipmentSummary", "volunteer_phone", "private"),
        ("ShipmentSummary", "status", "DELAYED"), ("ShipmentReadiness", "status", "PICKED_UP"),
        ("ShipmentSummary", "status", "DELIVERED"),
        ("ShipmentPickup", "evidence_ids", []), ("ShipmentPickup", "received_quantities", []),
        ("ShipmentReceiptPending", "delivery_accepted", True), ("ShipmentPingReceipt", "delivery_accepted", True),
        ("ShipmentPingBatch", "samples", []), ("ShipmentIssueReceipt", "custody_changed", True),
        ("ShipmentCommand", "force", True), ("ShipmentAssign", "approved", True),
        ("ShipmentReceiptException", "evidence_ids", []), ("ShipmentDelay", "estimated_arrival_at", "soon"),
    ]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid custody/status/private field"))
    for schema, key in [("ShipmentPickup", "assignment_revision_id"), ("ShipmentPickup", "source_acknowledgement_id"),
                        ("ShipmentReceiptAccept", "receipt_revision_id"), ("ShipmentCustodyHandoff", "to_acknowledgement_id"),
                        ("ShipmentCustodyHandoff", "policy_decision_id"), ("ShipmentPingBatch", "tracking_consent_receipt_id")]:
        payload = deepcopy(e[schema]); del payload[key]; cases.append((schema, payload, "missing custody/consent reference"))
    payload = deepcopy(e["ShipmentFieldDetails"]); payload["pickup_contact"]["phone_e164"] = "+919000000001"
    cases.append(("ShipmentFieldDetails", payload, "withheld contact exposes phone"))
    payload = deepcopy(e["ShipmentPingBatch"]); payload["samples"][0]["point"]["latitude"] = 91
    cases.append(("ShipmentPingBatch", payload, "invalid ping coordinates"))
    return cases
