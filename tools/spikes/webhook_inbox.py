"""P0 local experiment only. SQLite fixtures are not the production inbox."""

import hashlib
import hmac
import json
import re
import sqlite3
import uuid

MAX_BODY_BYTES = 1048576  # Proposed limit, requires measured provider payload review.


def verify_raw(raw, signature, secrets):
    if not isinstance(raw, bytes) or not raw or len(raw) > MAX_BODY_BYTES:
        raise ValueError("WEBHOOK_BODY_INVALID")
    if not secrets or any(not isinstance(key, bytes) or not key for key in secrets):
        raise ValueError("WEBHOOK_SECRET_CONFIGURATION_INVALID")
    if not isinstance(signature, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", signature):
        raise ValueError("WEBHOOK_SIGNATURE_INVALID")
    supplied = bytes.fromhex(signature)
    results = [hmac.compare_digest(hmac.digest(key, raw, "sha256"), supplied) for key in secrets]
    if not any(results):
        raise ValueError("WEBHOOK_SIGNATURE_INVALID")


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError("non-JSON numeric constant")


class FixtureInbox:
    """Exercises commit/digest behavior with synthetic data, no financial writes.

    Real storage needs PostgreSQL, encryption/retention, ingress limits, durable
    workers, observability and domain dedupe. Raw bytes here are plaintext fixtures.
    """

    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute("""CREATE TABLE IF NOT EXISTS inbox (
            receipt TEXT PRIMARY KEY, scope TEXT NOT NULL, event_id TEXT NOT NULL,
            digest TEXT NOT NULL, body BLOB NOT NULL, quarantined INTEGER NOT NULL,
            UNIQUE(scope, digest))""")

    def close(self):
        self.connection.close()

    def receive(self, raw, signature, event_id, *, scope, account_id, secrets, fail_before_commit=False):
        verify_raw(raw, signature, secrets)  # Never parse/reencode before authentication.
        if not isinstance(event_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,200}", event_id):
            raise ValueError("WEBHOOK_HEADERS_INVALID")
        if not scope or not account_id:
            raise ValueError("WEBHOOK_ENDPOINT_CONFIGURATION_INVALID")
        quarantined = False
        try:
            payload = json.loads(raw, object_pairs_hook=strict_object, parse_constant=invalid_constant)
            # This experiment queues only known event envelopes. It deliberately
            # does not normalize payment entities or decide capture eligibility.
            quarantined = (not isinstance(payload, dict) or payload.get("entity") != "event"
                or payload.get("account_id") != account_id or not isinstance(payload.get("payload"), dict)
                or not isinstance(payload.get("event"), str)
                or payload.get("event") not in {"payment.authorized", "payment.captured", "payment.failed", "order.paid",
                    "refund.created", "refund.processed", "refund.failed", "refund.speed_changed"})
        except (ValueError, UnicodeError, RecursionError):
            quarantined = True
        digest = hashlib.sha256(raw).hexdigest()
        with self.connection:
            self.connection.execute("BEGIN IMMEDIATE")
            existing = self.connection.execute("SELECT receipt, quarantined FROM inbox WHERE scope=? AND digest=?", (scope, digest)).fetchone()
            if existing:
                result = {"receipt_id": existing[0], "durable": True, "disposition": "QUARANTINED" if existing[1] else "DUPLICATE", "financial_effect_applied": False}
            else:
                collision = self.connection.execute("SELECT 1 FROM inbox WHERE scope=? AND event_id=?", (scope, event_id)).fetchone()
                quarantined = quarantined or bool(collision)
                receipt = str(uuid.uuid4())
                self.connection.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (receipt, scope, event_id, digest, raw, int(quarantined)))
                result = {"receipt_id": receipt, "durable": True, "disposition": "QUARANTINED" if quarantined else "RECORDED", "financial_effect_applied": False}
            if fail_before_commit:
                raise sqlite3.OperationalError("injected commit failure")
        return result  # Return only after successful transaction exit/commit.
