"""Provider-owned webhook envelope, authenticated before parsing."""

from copy import deepcopy
from contract_identity import ID, UUID, enum, integer, obj, ref, text


def schemas():
    # Vendor extension fields are JSON values, never business commands. Keeping
    # them at intake is deliberate; normalized domain validation happens later.
    value = {"oneOf": [{"type": "null"}, {"type": "boolean"}, {"type": "number"}, {"type": "string"},
                       {"type": "array", "items": ref("ProviderJsonValue")},
                       {"type": "object", "additionalProperties": ref("ProviderJsonValue")}]}
    return {
        "ProviderJsonValue": value,
        "RazorpayEnvelope": obj({"entity": enum("event"), "account_id": text(1, 100), "event": text(1, 150),
            "contains": {"type": "array", "items": text(1, 100), "maxItems": 100},
            "payload": {"type": "object", "additionalProperties": ref("ProviderJsonValue")},
            "created_at": integer(0, 9007199254740991)}, ["entity", "account_id", "event", "payload"],
            additionalProperties=ref("ProviderJsonValue"),
            description="Provider-owned extension-tolerant intake, not a normalized payment schema. Verify original bytes before parsing. Unknown events or invalid entities are durably quarantined, never applied to balances."),
        "WebhookReceipt": obj({"receipt_id": ID, "durable": {"type": "boolean", "const": True},
            "disposition": enum("RECORDED", "DUPLICATE", "QUARANTINED"), "financial_effect_applied": {"type": "boolean", "const": False}}),
    }


def definitions():
    return {"ingest_payment_webhook": ("RazorpayEnvelope", "200", "WebhookReceipt",
        ["WEBHOOK_SIGNATURE_INVALID", "WEBHOOK_HEADERS_INVALID", "WEBHOOK_BODY_TOO_LARGE"],
        "Authenticate exact raw bytes using configured webhook secret set. Commit inbox/duplicate/quarantine receipt before 200; durable failure returns 503. No capture credit, refund completion or user authentication at intake.")}


def examples():
    return {"RazorpayEnvelope": {"entity": "event", "account_id": "acc_synthetic", "event": "payment.captured",
        "contains": ["payment"], "created_at": 1789084800, "payload": {"payment": {"entity": {
            "id": "pay_synthetic", "entity": "payment", "amount": 10000, "currency": "INR", "status": "captured",
            "order_id": "order_synthetic", "captured": True, "created_at": 1789084800}}}},
        "WebhookReceipt": {"receipt_id": UUID, "durable": True, "disposition": "RECORDED", "financial_effect_applied": False}}


def example_variants():
    unknown = deepcopy(examples()["RazorpayEnvelope"])
    unknown.update(event="future.vendor_event", payload={"future_entity": {"entity": {"new_field": [True, None, 1, "value"]}}})
    return {"RazorpayEnvelope": {"unknown_quarantine": unknown}, "WebhookReceipt": {
        kind.lower(): {"receipt_id": UUID, "durable": True, "disposition": kind, "financial_effect_applied": False}
        for kind in ("DUPLICATE", "QUARANTINED")}}


def parameters():
    return {"ingest_payment_webhook": [{"name": "x-razorpay-event-id", "in": "header", "required": True,
                                       "schema": text(1, 200, pattern=r"^[A-Za-z0-9_-]+$")} ]}


def negative_cases():
    cases = []
    for key, value in [("durable", False), ("financial_effect_applied", True), ("disposition", "PAID")]:
        payload = deepcopy(examples()["WebhookReceipt"]); payload[key] = value
        cases.append(("WebhookReceipt", payload, "intake cannot assert nondurable or financial success"))
    payload = deepcopy(examples()["RazorpayEnvelope"]); payload["payload"] = []
    cases.append(("RazorpayEnvelope", payload, "non-object provider payload goes to raw quarantine"))
    return cases
