"""Owner contribution and checkout contracts; provider inbox remains a separate slice."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import QUANTITY, array

PAISE = integer(0, 9007199254740991)
POSITIVE_PAISE = integer(1, 9007199254740991)
POSITIVE_QUANTITY = {**QUANTITY, "not": {"enum": ["0", "0.0", "0.00"]}}


def schemas():
    s = {}
    display = {"anonymous": BOOL, "message": nullable(text(1, 1000)), "message_visibility": enum("organization", "private")}
    selection = [
        obj({"type": enum("MONEY"), "need_id": ID, "amount_paise": POSITIVE_PAISE, "currency": enum("INR")}),
        obj({"type": enum("ITEM"), "need_id": ID, "quantity": POSITIVE_QUANTITY, "unit": text(1, 30),
             "condition": enum("NEW", "GOOD", "FAIR"), "photo_media_ids": {**array(ID, 10), "minItems": 1, "uniqueItems": True},
             "fulfilment": {"oneOf": [
                 obj({"mode": enum("pickup"), "address_id": ID, "pickup_slot_id": ID}),
                 obj({"mode": enum("dropoff"), "dropoff_location_id": ID}),
             ]}}),
        obj({"type": enum("TIME"), "need_id": ID, "role_id": ID, "slot_id": ID}),
    ]
    s["ContributionSelection"] = {"oneOf": selection, "discriminator": {"propertyName": "type"}}
    s["ContributionQuoteRequest"] = obj({"selection": ref("ContributionSelection"), "display": obj(display)})
    s["ContributionQuote"] = obj({"id": ID, "mission_id": ID, "selection": ref("ContributionSelection"),
        "display": obj(display), "disclosure_revision_id": ID, "expires_at": TIME, "reservation_created": {"type": "boolean", "const": False},
        "fee_policy": enum("platform_absorbs_gateway_fee"), "donor_gateway_fee_paise": {"type": "integer", "const": 0}, "version": VERSION})
    s["ContributionCreate"] = obj({"quote_id": ID, "quote_version": VERSION, "disclosure_revision_id": ID,
                                    "consent_receipt_id": ID})
    s["ContributionDisplayUpdate"] = obj({**display, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["ContributionCancel"] = obj({"expected_version": VERSION, "reason": text(1, 1000)})
    s["ContributionPaymentSummary"] = obj({"captured_paise": PAISE, "allocated_paise": PAISE,
        "refund_requested_paise": PAISE, "refund_processed_paise": PAISE, "currency": enum("INR"),
        "recovery_status": enum("NONE", "RECONCILING", "REQUIRES_REVIEW", "REFUND_PENDING", "RESOLVED")})
    common = {"id": ID, "mission_id": ID, "need_id": ID, "display": obj(display), "created_at": TIME,
              "confirmed_at": nullable(TIME), "version": VERSION, "impact_record_id": nullable(ID)}
    s["ContributionDetail"] = {"oneOf": [
        obj({**common, "type": enum("MONEY"), "amount_paise": POSITIVE_PAISE, "currency": enum("INR"),
             "lifecycle_status": enum("PENDING_PAYMENT", "PAYMENT_FAILED", "EXPIRED", "CANCELLED", "CONFIRMED", "ALLOCATED", "FULFILLED", "VERIFIED", "COMPLETED"),
             "payment": ref("ContributionPaymentSummary"), "checkout_id": ID}),
        obj({**common, "type": enum("ITEM"), "quantity": POSITIVE_QUANTITY, "unit": text(1, 30),
             "received_quantity": nullable(QUANTITY), "verified_quantity": nullable(QUANTITY), "shipment_id": ID,
             "lifecycle_status": enum("CONFIRMED", "SCHEDULED", "IN_TRANSIT", "DELIVERED", "VERIFIED", "COMPLETED", "CANCELLED"),
             "recovery_status": enum("NONE", "RETURN_PENDING", "REQUIRES_REVIEW", "RESOLVED")}),
        obj({**common, "type": enum("TIME"), "assignment_id": ID, "slot_id": ID, "role_id": ID,
             "verified_seconds": nullable(integer()),
             "lifecycle_status": enum("CONFIRMED", "UPCOMING", "CHECKED_IN", "CHECKED_OUT", "VERIFIED", "COMPLETED", "CANCELLED", "NO_SHOW"),
             "recovery_status": enum("NONE", "ATTENDANCE_DISPUTED", "REQUIRES_REVIEW", "RESOLVED")}),
    ], "discriminator": {"propertyName": "type"}}
    s["ContributionPage"] = page(ref("ContributionDetail"))
    s["ContributionHistoryEntry"] = obj({"id": ID, "recorded_at": TIME, "effective_at": nullable(TIME),
        "kind": enum("intent", "payment", "allocation", "refund", "shipment", "attendance", "verification", "correction", "cancellation"),
        "safe_summary": text(1, 500), "evidence_status": enum("PENDING", "ACCEPTED", "SUPERSEDED"), "version": VERSION})
    s["ContributionHistoryPage"] = page(ref("ContributionHistoryEntry"))
    s["ContributionTracking"] = obj({"contribution_id": ID, "as_of": TIME, "version": VERSION,
        "stages": array(obj({"key": enum("confirmed", "funds_sent", "scheduled", "picked_up", "delivered", "attendance", "verified", "record_ready"),
            "state": enum("PENDING", "IN_PROGRESS", "EVIDENCED", "NEEDS_ATTENTION", "NOT_APPLICABLE"),
            "occurred_at": nullable(TIME), "safe_detail": text(1, 500)}), 8),
        "recovery_summary": nullable(text(1, 500)), "shipment_id": nullable(ID), "assignment_id": nullable(ID)})
    s["PaymentCapabilities"] = obj({"provider": enum("razorpay"), "currency": enum("INR"),
        "live_payments_enabled": BOOL, "fee_policy": enum("platform_absorbs_gateway_fee"),
        "donor_gateway_fee_paise": {"type": "integer", "const": 0}, "wallet_supported": {"type": "boolean", "const": False},
        "saved_methods_available": BOOL, "unavailable_reason": nullable(text(1, 300)), "version": VERSION})
    s["CheckoutAttempt"] = obj({"id": ID, "contribution_id": ID,
        "state": enum("INTENT_RECORDED", "CREATE_REQUESTED", "CREATE_UNCERTAIN", "ORDER_READY", "CREATE_FAILED", "LOCALLY_CLOSED"),
        "created_at": TIME, "version": VERSION, "payment_status": enum("NOT_OBSERVED", "CONFIRMING", "AUTHORIZED", "CAPTURED", "FAILED", "RECOVERY_REQUIRED"),
        "safe_reason": nullable(text(1, 500))})
    s["CheckoutAttemptPage"] = page(ref("CheckoutAttempt"))
    checkout_common = {"contribution_id": ID, "attempt": ref("CheckoutAttempt"), "version": VERSION}
    s["CheckoutStatus"] = {"oneOf": [
        obj({**checkout_common, "presentation": enum("WAIT", "CLOSED", "COMPLETE", "SUPPORT"),
             "safe_message": text(1, 500)}),
        obj({**checkout_common, "attempt": {"allOf": [ref("CheckoutAttempt"), {"properties": {"state": enum("ORDER_READY")}}]},
             "presentation": enum("READY"), "expires_at": TIME,
             "checkout": obj({"provider": enum("razorpay"), "public_key_id": text(1, 100), "provider_order_id": text(1, 100),
                              "amount_paise": POSITIVE_PAISE, "currency": enum("INR")})}),
    ], "discriminator": {"propertyName": "presentation"}}
    s["CheckoutRetry"] = obj({"expected_version": VERSION, "previous_attempt_id": ID, "disclosure_revision_id": ID})
    s["CheckoutCallback"] = obj({"expected_version": VERSION, "attempt_id": ID, "provider_order_id": text(1, 100),
        "provider_payment_id": text(1, 100), "provider_signature": text(64, 64, pattern=r"^[a-fA-F0-9]{64}$", writeOnly=True)})
    s["PaymentVerificationPending"] = obj({"operation_id": ID, "status": enum("PENDING"), "payment_confirmed": {"type": "boolean", "const": False}})
    s["PaymentReceipt"] = {"oneOf": [
        obj({"status": enum("PENDING", "UNAVAILABLE"), "payment_id": ID, "safe_reason": text(1, 300)}),
        obj({"status": enum("ISSUED"), "payment_id": ID, "receipt_id": ID, "contribution_id": ID,
             "issued_at": TIME, "amount_paise": POSITIVE_PAISE, "currency": enum("INR"),
             "kind": enum("payment_acknowledgement"), "tax_deduction_certificate": {"type": "boolean", "const": False}}),
    ], "discriminator": {"propertyName": "status"}}
    return s


def definitions():
    return {
        "quote_contribution": ("ContributionQuoteRequest", "201", "ContributionQuote", ["NEED_CLOSED", "CONTRIBUTION_NOT_ELIGIBLE"], "Create owner-bound expiring review quote; no funds, contribution or slot reservation."),
        "create_contribution": ("ContributionCreate", "201", "ContributionDetail", ["NEED_CLOSED", "QUOTE_EXPIRED", "DISCLOSURE_CHANGED", "SLOT_FULL", "CONTRIBUTION_NOT_ELIGIBLE"], "Resolve immutable quote and consent; recheck eligibility under locks. Money records intent and durable checkout work; item/time atomically reserve capacity. No client-supplied paid status."),
        "list_contributions": (None, "200", "ContributionPage", [], "Owner activity with independent payment, execution and recovery projections."),
        "get_contribution": (None, "200", "ContributionDetail", [], "Owner detail; captured money and processed refunds remain historical facts."),
        "edit_contribution_display": ("ContributionDisplayUpdate", "200", "ContributionDetail", [], "Versioned permitted display changes; financial intent remains immutable and private messages do not become public."),
        "cancel_contribution": ("ContributionCancel", "200", "ContributionDetail", ["CANCELLATION_NOT_ALLOWED", "PAYMENT_OUTCOME_UNKNOWN"], "Serialize cancellation against custody/check-in. Money closes local checkout only; retain reconciliation and late-capture recovery."),
        "get_tracking_snapshot": (None, "200", "ContributionTracking", [], "Participant-scoped evidence timeline; no raw GPS, home address, bank data or promise inferred from client actions."),
        "get_contribution_history": (None, "200", "ContributionHistoryPage", [], "Owner-safe append-only history; retain corrections and actual event times."),
        "get_payment_capabilities": (None, "200", "PaymentCapabilities", [], "Report configured availability; live payment gate, no wallet and platform-absorbed launch gateway fees."),
        "get_checkout_status": (None, "200", "CheckoutStatus", [], "Expose SDK parameters only for currently eligible ORDER_READY checkout. Closed and uncertain attempts never return usable checkout parameters."),
        "list_checkout_attempts": (None, "200", "CheckoutAttemptPage", [], "Retain every attempt and uncertainty; failures cannot erase captures."),
        "start_checkout_retry": ("CheckoutRetry", "201", "CheckoutAttempt", ["PAYMENT_OUTCOME_UNKNOWN", "DISCLOSURE_CHANGED", "NEED_CLOSED"], "New local attempt only after older uncertainty is conclusively resolved and retry policy permits; duplicate taps replay same command."),
        "verify_checkout_callback": ("CheckoutCallback", "202", "PaymentVerificationPending", [], "Validate owner/order/signature binding then enqueue authoritative provider reconciliation. Callback acknowledgement is never capture/allocation proof."),
        "get_payment_receipt": (None, "200", "PaymentReceipt", [], "Owner payment acknowledgement after accepted matched capture; no tax eligibility implied. Unallocated recovery captures require reviewed receipt policy."),
    }


def examples():
    display = {"anonymous": True, "message": None, "message_visibility": "private"}
    selection = {"type": "MONEY", "need_id": UUID, "amount_paise": 10000, "currency": "INR"}
    detail = {"id": UUID, "mission_id": UUID, "need_id": UUID, "display": display, "created_at": NOW,
        "confirmed_at": None, "version": 1, "impact_record_id": None, "type": "MONEY", "amount_paise": 10000,
        "currency": "INR", "lifecycle_status": "PENDING_PAYMENT", "checkout_id": UUID,
        "payment": {"captured_paise": 0, "allocated_paise": 0, "refund_requested_paise": 0,
                    "refund_processed_paise": 0, "currency": "INR", "recovery_status": "NONE"}}
    attempt = {"id": UUID, "contribution_id": UUID, "state": "CREATE_UNCERTAIN", "created_at": NOW, "version": 1,
               "payment_status": "NOT_OBSERVED", "safe_reason": "Payment setup is being checked"}
    history = {"id": UUID, "recorded_at": NOW, "effective_at": None, "kind": "intent",
               "safe_summary": "Preparing payment", "evidence_status": "PENDING", "version": 1}
    return {
        "ContributionSelection": selection,
        "ContributionQuoteRequest": {"selection": selection, "display": display},
        "ContributionQuote": {"id": UUID, "mission_id": UUID, "selection": selection, "display": display,
            "disclosure_revision_id": UUID, "expires_at": NOW, "reservation_created": False,
            "fee_policy": "platform_absorbs_gateway_fee", "donor_gateway_fee_paise": 0, "version": 1},
        "ContributionCreate": {"quote_id": UUID, "quote_version": 1, "disclosure_revision_id": UUID, "consent_receipt_id": UUID},
        "ContributionDisplayUpdate": {"expected_version": 1, "anonymous": True},
        "ContributionCancel": {"expected_version": 1, "reason": "Plans changed"},
        "ContributionDetail": detail, "ContributionPage": {"items": [detail], "next_cursor": None, "has_more": False},
        "ContributionHistoryPage": {"items": [history], "next_cursor": None, "has_more": False},
        "ContributionTracking": {"contribution_id": UUID, "as_of": NOW, "version": 1, "stages": [],
            "recovery_summary": "Payment setup is being checked", "shipment_id": None, "assignment_id": None},
        "PaymentCapabilities": {"provider": "razorpay", "currency": "INR", "live_payments_enabled": False,
            "fee_policy": "platform_absorbs_gateway_fee", "donor_gateway_fee_paise": 0, "wallet_supported": False,
            "saved_methods_available": False, "unavailable_reason": "Live payment readiness is not approved", "version": 1},
        "CheckoutAttempt": attempt, "CheckoutAttemptPage": {"items": [attempt], "next_cursor": None, "has_more": False},
        "CheckoutStatus": {"contribution_id": UUID, "attempt": attempt, "version": 1, "presentation": "WAIT", "safe_message": "Checking payment setup"},
        "CheckoutRetry": {"expected_version": 1, "previous_attempt_id": UUID, "disclosure_revision_id": UUID},
        "CheckoutCallback": {"expected_version": 1, "attempt_id": UUID, "provider_order_id": "order_synthetic",
            "provider_payment_id": "pay_synthetic", "provider_signature": "a" * 64},
        "PaymentVerificationPending": {"operation_id": UUID, "status": "PENDING", "payment_confirmed": False},
        "PaymentReceipt": {"status": "ISSUED", "payment_id": UUID, "receipt_id": UUID, "contribution_id": UUID,
            "issued_at": NOW, "amount_paise": 10000, "currency": "INR", "kind": "payment_acknowledgement", "tax_deduction_certificate": False},
    }


def example_variants():
    e = examples()
    item = {"type": "ITEM", "need_id": UUID, "quantity": "2.5", "unit": "kg", "condition": "NEW",
            "photo_media_ids": [UUID], "fulfilment": {"mode": "pickup", "address_id": UUID, "pickup_slot_id": UUID}}
    dropoff = {**item, "fulfilment": {"mode": "dropoff", "dropoff_location_id": UUID}}
    time = {"type": "TIME", "need_id": UUID, "role_id": UUID, "slot_id": UUID}
    result = {"ContributionQuoteRequest": {}, "ContributionQuote": {}, "ContributionDetail": {}}
    for name, selection in [("item_pickup", item), ("item_dropoff", dropoff), ("time", time)]:
        for schema in ("ContributionQuoteRequest", "ContributionQuote"):
            payload = deepcopy(e[schema]); payload["selection"] = selection
            result[schema][name] = payload
    base = {key: deepcopy(e["ContributionDetail"][key]) for key in
            ("id", "mission_id", "need_id", "display", "created_at", "confirmed_at", "version", "impact_record_id")}
    result["ContributionDetail"]["item"] = {**base, "type": "ITEM", "quantity": "2.5", "unit": "kg",
        "received_quantity": None, "verified_quantity": None, "shipment_id": UUID, "lifecycle_status": "CONFIRMED", "recovery_status": "NONE"}
    result["ContributionDetail"]["time"] = {**base, "type": "TIME", "assignment_id": UUID, "slot_id": UUID, "role_id": UUID,
        "verified_seconds": None, "lifecycle_status": "CONFIRMED", "recovery_status": "NONE"}
    partial = deepcopy(e["ContributionDetail"])
    partial.update(lifecycle_status="CONFIRMED", confirmed_at=NOW)
    partial["payment"].update(captured_paise=10000, allocated_paise=10000, refund_processed_paise=2500)
    result["ContributionDetail"]["partial_refund"] = partial
    ready = {"contribution_id": UUID, "version": 1, "attempt": {**e["CheckoutAttempt"], "state": "ORDER_READY", "safe_reason": None},
             "presentation": "READY", "expires_at": NOW, "checkout": {"provider": "razorpay", "public_key_id": "rzp_test_synthetic",
             "provider_order_id": "order_synthetic", "amount_paise": 10000, "currency": "INR"}}
    result["CheckoutStatus"] = {"ready": ready, "closed": {**deepcopy(e["CheckoutStatus"]), "presentation": "CLOSED",
        "attempt": {**e["CheckoutAttempt"], "state": "LOCALLY_CLOSED"}, "safe_message": "Checkout closed; payment checked separately"}}
    result["PaymentReceipt"] = {"pending": {"status": "PENDING", "payment_id": UUID, "safe_reason": "Confirming payment"}}
    return result


def negative_cases():
    e = examples(); cases = []
    for schema, key, value, label in [
        ("ContributionSelection", "type", "SKILL", "skills are interest only"),
        ("ContributionSelection", "amount_paise", 0, "zero money"),
        ("ContributionSelection", "amount_paise", 1.5, "fractional paise"),
        ("ContributionSelection", "currency", "USD", "unsupported currency"),
        ("ContributionCreate", "status", "CONFIRMED", "client confirmation injection"),
        ("ContributionCreate", "amount_paise", 1, "quote amount replacement"),
        ("ContributionCreate", "owner_user_id", UUID, "owner injection"),
        ("ContributionQuote", "reservation_created", True, "quote reserves capacity"),
        ("ContributionQuote", "donor_gateway_fee_paise", 100, "launch gateway fee charged to donor"),
        ("ContributionDetail", "verified_seconds", 60, "cross-type execution fields"),
        ("ContributionDisplayUpdate", "amount_paise", 200, "financial edit bypass"),
        ("ContributionTracking", "volunteer_phone", "private", "private tracking data"),
        ("PaymentCapabilities", "wallet_supported", True, "wallet prohibition"),
        ("CheckoutCallback", "provider_signature", "untrusted", "malformed signature"),
        ("CheckoutCallback", "captured", True, "callback asserts capture"),
        ("PaymentVerificationPending", "payment_confirmed", True, "acknowledgement claims capture"),
        ("PaymentReceipt", "tax_deduction_certificate", True, "receipt asserts tax eligibility"),
    ]:
        value_payload = deepcopy(e[schema]); value_payload[key] = value
        cases.append((schema, value_payload, label))
    payload = deepcopy(e["CheckoutStatus"])
    payload["checkout"] = {"provider": "razorpay", "public_key_id": "key", "provider_order_id": "order",
                           "amount_paise": 10000, "currency": "INR"}
    cases.append(("CheckoutStatus", payload, "uncertain checkout exposes SDK parameters"))
    ready = deepcopy(example_variants()["CheckoutStatus"]["ready"])
    ready["attempt"]["state"] = "CREATE_UNCERTAIN"
    cases.append(("CheckoutStatus", ready, "ready presentation for uncertain order"))
    item = deepcopy(example_variants()["ContributionQuoteRequest"]["item_pickup"])
    item["selection"]["quantity"] = "0.00"
    cases.append(("ContributionQuoteRequest", item, "zero item quantity"))
    item = deepcopy(example_variants()["ContributionQuoteRequest"]["item_dropoff"])
    item["selection"]["fulfilment"]["address_id"] = UUID
    cases.append(("ContributionQuoteRequest", item, "pickup field in dropoff"))
    return cases
