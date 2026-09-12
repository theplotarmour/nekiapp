"""Notification reads, single-use connection tickets and provider saved-method views."""

from copy import deepcopy
from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text
from contract_discovery import array


def schemas():
    s = {}
    target = {"oneOf": [obj({"kind": enum(kind), "id": ID}) for kind in
                         ("mission", "contribution", "assignment", "shipment", "case", "impact_record")]
              + [obj({"kind": enum("account")})], "discriminator": {"propertyName": "kind"}}
    s["NotificationView"] = obj({"id": ID, "category": enum("contribution", "tracking", "volunteering", "impact", "account"),
        "title": text(1, 160), "body": text(1, 500), "target": nullable(target), "occurred_at": TIME, "read_at": nullable(TIME),
        "occurrence_id": ID, "version": VERSION})
    s["NotificationPage"] = page(ref("NotificationView"))
    s["NotificationPage"]["properties"].update(snapshot_id=ID, inbox_version=VERSION)
    s["NotificationPage"]["required"] += ["snapshot_id", "inbox_version"]
    s["NotificationUnread"] = obj({"count": integer(), "as_of": TIME, "inbox_version": VERSION})
    s["NotificationReadCommand"] = {"oneOf": [
        obj({"mode": enum("selected"), "notification_ids": {**array(ID, 100), "minItems": 1, "uniqueItems": True}, "expected_version": VERSION}),
        obj({"mode": enum("through_snapshot"), "snapshot_id": ID, "expected_version": VERSION}),
    ], "discriminator": {"propertyName": "mode"}}
    s["NotificationReadResult"] = obj({"marked_count": integer(), "unread_count": integer(), "inbox_version": VERSION})
    s["RealtimeChannel"] = {"oneOf": [obj({"kind": enum(kind), "subject_id": ID}) for kind in
                                      ("shipment", "contribution", "assignment")]
                          + [obj({"kind": enum("own_notifications")})], "discriminator": {"propertyName": "kind"}}
    s["ConnectionTicketRequest"] = obj({"channels": {**array(ref("RealtimeChannel"), 20), "minItems": 1, "uniqueItems": True}, "device_id": ID})
    s["ConnectionTicket"] = obj({"ticket": text(43, 128, pattern=r"^[A-Za-z0-9_-]+$", readOnly=True), "expires_at": TIME,
        "single_use": {"type": "boolean", "const": True}, "websocket_path": enum("/ws"),
        "protocol": enum("neki.realtime.v1"), "authorized_channels": {**array(ref("RealtimeChannel"), 20), "minItems": 1, "uniqueItems": True}})
    s["SavedPaymentMethod"] = obj({"id": ID, "kind": enum("card"), "network": text(1, 60),
        "last4": text(4, 4, pattern=r"^[0-9]{4}$"), "expiry_month": integer(1, 12), "expiry_year": integer(2020, 2200),
        "status": enum("AVAILABLE", "EXPIRED", "REMOVAL_PENDING"), "version": VERSION})
    s["SavedPaymentMethods"] = obj({"availability": enum("AVAILABLE", "UNAVAILABLE"), "safe_reason": nullable(text(1, 300)),
        "items": array(ref("SavedPaymentMethod"), 50), "next_cursor": nullable(text(1, 2048)), "has_more": BOOL},
        allOf=[{"if": {"properties": {"availability": {"const": "UNAVAILABLE"}}},
                "then": {"properties": {"items": {"maxItems": 0}, "has_more": {"const": False}, "next_cursor": {"type": "null"}}}}])
    s["PaymentMethodRemoval"] = obj({"operation_id": ID, "payment_method_id": ID, "status": enum("PENDING"),
        "provider_removal_confirmed": {"type": "boolean", "const": False}})
    return s


def definitions():
    return {
        "list_notifications": (None, "200", "NotificationPage", [], "Owner inbox; recheck source authorization before composing private content or target. No arbitrary URL or private media payload."),
        "get_unread_count": (None, "200", "NotificationUnread", [], "Current owner count and inbox revision; suppression/delivery is separate from read status."),
        "mark_notifications_read": ("NotificationReadCommand", "200", "NotificationReadResult", [], "Mark only owned selected IDs or exact prior snapshot; concurrent new arrivals remain unread. No push delivery claims."),
        "create_connection_ticket": ("ConnectionTicketRequest", "201", "ConnectionTicket", [], "Authorize explicit subjects with current session/device/origin and assignment access; issue short-lived hashed single-use ticket. No wildcard channel or durable message guarantee."),
        "list_payment_methods": (None, "200", "SavedPaymentMethods", [], "Owner provider-supported masked card metadata only. Unavailable is explicit; no fabricated saved methods or NEKI wallet. Actual token/card vault stays provider-side."),
        "remove_payment_method": (None, "202", "PaymentMethodRemoval", [], "Step-up and ownership required; disable local reuse immediately, enqueue provider removal and retain uncertainty until confirmed. Never delete payment history."),
    }


def examples():
    notification = {"id": UUID, "category": "tracking", "title": "Pickup update", "body": "Your pickup schedule was updated",
        "target": {"kind": "shipment", "id": UUID}, "occurred_at": NOW, "read_at": None, "occurrence_id": UUID, "version": 1}
    return {"NotificationView": notification, "NotificationPage": {"items": [notification], "next_cursor": None, "has_more": False, "snapshot_id": UUID, "inbox_version": 1},
        "NotificationUnread": {"count": 1, "as_of": NOW, "inbox_version": 1},
        "NotificationReadCommand": {"mode": "selected", "notification_ids": [UUID], "expected_version": 1},
        "NotificationReadResult": {"marked_count": 1, "unread_count": 0, "inbox_version": 2},
        "ConnectionTicketRequest": {"channels": [{"kind": "own_notifications"}], "device_id": UUID},
        "ConnectionTicket": {"ticket": "a" * 43, "expires_at": NOW, "single_use": True, "websocket_path": "/ws",
            "protocol": "neki.realtime.v1", "authorized_channels": [{"kind": "own_notifications"}]},
        "SavedPaymentMethods": {"availability": "UNAVAILABLE", "safe_reason": "Saved methods are not enabled", "items": [], "next_cursor": None, "has_more": False},
        "SavedPaymentMethod": {"id": UUID, "kind": "card", "network": "Synthetic network", "last4": "0000", "expiry_month": 12, "expiry_year": 2030, "status": "AVAILABLE", "version": 1},
        "PaymentMethodRemoval": {"operation_id": UUID, "payment_method_id": UUID, "status": "PENDING", "provider_removal_confirmed": False}}


def example_variants():
    e = examples()
    return {"NotificationReadCommand": {"snapshot": {"mode": "through_snapshot", "snapshot_id": UUID, "expected_version": 1}},
        "SavedPaymentMethods": {"available": {"availability": "AVAILABLE", "safe_reason": None, "items": [e["SavedPaymentMethod"]], "next_cursor": None, "has_more": False}}}


def negative_cases():
    e = examples(); cases = []
    for schema, key, value in [("NotificationView", "pickup_address", "private"), ("NotificationView", "target", {"url": "https://example.invalid"}),
        ("NotificationReadCommand", "notification_ids", []), ("NotificationReadCommand", "all_users", True),
        ("ConnectionTicketRequest", "channels", [{"kind": "*"}]), ("ConnectionTicketRequest", "user_id", UUID),
        ("ConnectionTicket", "single_use", False), ("ConnectionTicket", "refresh_token", "private"),
        ("SavedPaymentMethod", "pan", "private"), ("SavedPaymentMethod", "provider_token", "private"), ("SavedPaymentMethod", "last4", "000000"),
        ("SavedPaymentMethods", "items", [e["SavedPaymentMethod"]]), ("PaymentMethodRemoval", "provider_removal_confirmed", True)]:
        payload = deepcopy(e[schema]); payload[key] = value; cases.append((schema, payload, "invalid private data or authority claim"))
    return cases
