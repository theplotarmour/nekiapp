"""Standalone JSON-frame WebSocket specification; intentionally not OpenAPI/AsyncAPI."""

from copy import deepcopy
from contract_identity import ID, NOW, TIME, UUID, VERSION, enum, integer, obj, text
from contract_discovery import array


def ref(name):
    return {"$ref": f"#/schemas/{name}"}


def document():
    channel = {"oneOf": [obj({"kind": enum(kind), "subject_id": ID}) for kind in ("shipment", "contribution", "assignment")]
               + [obj({"kind": enum("own_notifications")})], "discriminator": {"propertyName": "kind"}}
    correlation = {"request_id": ID}
    event = {"connection_id": ID, "sequence": integer(1, 9007199254740991)}
    schemas = {
        "Channel": channel,
        "Handshake": obj({"query": obj({"ticket": text(43, 128, pattern=r"^[A-Za-z0-9_-]+$")}),
            "headers": obj({"Sec-WebSocket-Protocol": enum("neki.realtime.v1"), "Origin": text(1, 2048, format="uri")}, ["Sec-WebSocket-Protocol"])}),
        "ClientFrame": {"oneOf": [
            obj({**correlation, "type": enum("subscribe"), "channel": ref("Channel")}),
            obj({**correlation, "type": enum("unsubscribe"), "channel": ref("Channel")}),
            obj({**correlation, "type": enum("ping")}),
        ], "discriminator": {"propertyName": "type"}},
        "ServerFrame": {"oneOf": [
            obj({**event, "type": enum("ready"), "expires_at": TIME, "authorized_channels": {**array(ref("Channel"), 20), "minItems": 1, "uniqueItems": True}}),
            obj({**event, **correlation, "type": enum("subscribed", "unsubscribed"), "channel": ref("Channel")}),
            obj({**event, "type": enum("changed"), "channel": ref("Channel"), "aggregate_version": VERSION, "occurred_at": TIME}),
            obj({**event, "type": enum("resync_required"), "channel": ref("Channel"), "reason": enum("GAP", "BACKPRESSURE", "SOURCE_RESTART")}),
            obj({**event, **correlation, "type": enum("pong")}),
            obj({**event, **correlation, "type": enum("error"), "code": enum("INVALID_FRAME", "CHANNEL_DENIED", "LIMIT_EXCEEDED"), "safe_message": text(1, 300)}),
        ], "discriminator": {"propertyName": "type"}},
    }
    c = {"kind": "shipment", "subject_id": UUID}
    e = {"connection_id": UUID, "sequence": 1}
    return {"format": "neki-transport-contract.v1", "status": "review-draft", "operation_id": "connect_realtime", "inventory_method": "WS",
        "path": "/ws", "policy": "socket", "projection": "tracking", "source": "FR-10", "subprotocol": "neki.realtime.v1",
        "handshake": {"method": "GET", "success_status": 101, "schema": ref("Handshake"), "authentication": "single-use session/device-bound query ticket; no bearer/refresh token fallback",
            "failure_statuses": {"400": "Malformed handshake", "401": "Ticket invalid, expired or consumed", "403": "Origin/session/device/access denied", "429": "Connection limit", "503": "Ticket store or service unavailable"}},
        "wire": {"encoding": "UTF-8 JSON text", "max_frame_bytes": 16384, "max_subscriptions": 20, "binary_frames": "reject", "limits_status": "proposed pending load and mobile testing"},
        "close_codes": {"1000": "Normal closure", "1008": "Authentication expiry, revocation, protocol or access violation", "1009": "Frame too large", "1011": "Server failure; obtain new ticket and restore snapshots"},
        "schemas": schemas,
        "examples": {"Handshake": [{"query": {"ticket": "a" * 43}, "headers": {"Sec-WebSocket-Protocol": "neki.realtime.v1", "Origin": "https://app.example.invalid"}}],
            "ClientFrame": [{"request_id": UUID, "type": t, "channel": c} for t in ("subscribe", "unsubscribe")] + [{"request_id": UUID, "type": "ping"}],
            "ServerFrame": [{**e, "type": "ready", "expires_at": NOW, "authorized_channels": [c]},
                *[{**e, "request_id": UUID, "type": t, "channel": c} for t in ("subscribed", "unsubscribed")],
                {**e, "type": "changed", "channel": c, "aggregate_version": 2, "occurred_at": NOW},
                {**e, "type": "resync_required", "channel": c, "reason": "GAP"}, {**e, "request_id": UUID, "type": "pong"},
                {**e, "request_id": UUID, "type": "error", "code": "CHANNEL_DENIED", "safe_message": "Channel unavailable"}]},
        "invariants": [
            "Atomically consume ticket against current session/device/origin and expiry before upgrade; a failed upgrade after consumption requires a new ticket.",
            "Browser Origin must match an exact configured allowlist; a missing Origin is allowed only for the bound native-client session, never by absence alone.",
            "Subscribe only to a subset of ticket-authorized channels after current per-subject authorization; own_notifications derives owner from session.",
            "Recheck authorization before emission; terminate/revoke when session, consent, assignment or capability changes. No grace read of private state.",
            "Every new connection restores authenticated HTTP snapshots. Subscribe first and buffer hints while fetching, then reconcile aggregate versions to avoid a subscribe/snapshot race.",
            "Sequence is connection-local, monotonic across all server frames, and resets per connection; it is not a durable database cursor or global ordering key.",
            "Discard older aggregate versions; gap/resync/backpressure triggers authorized snapshot refresh. Hints cannot certify payment, custody or impact.",
            "On buffer overflow, stop applying partial hints and reconnect/resync; absence of an invalidation is never proof that a cached record remains authorized.",
            "Do not log tickets/full URLs or emit raw GPS, phone, addresses, bank data or private proof. Fields are invalidation hints only.",
        ], "limitations": ["Schema checks do not exercise network handshake, origin policy, atomic ticket consumption, concurrent revocation or durable recovery."]}


def negative_cases():
    d = document(); cases = []
    for schema, index, key, value in [("Handshake", 0, "query", {"access_token": "secret"}),
        ("ClientFrame", 0, "channel", {"kind": "*"}), ("ClientFrame", 0, "user_id", UUID),
        ("ClientFrame", 0, "type", "mark_paid"), ("ServerFrame", 3, "point", {"latitude": 28, "longitude": 77}),
        ("ServerFrame", 3, "sequence", 0), ("ServerFrame", 3, "aggregate_version", -1),
        ("ServerFrame", 0, "ticket", "private"), ("ServerFrame", 6, "stack", "private")]:
        payload = deepcopy(d["examples"][schema][index]); payload[key] = value; cases.append((schema, payload))
    return cases
