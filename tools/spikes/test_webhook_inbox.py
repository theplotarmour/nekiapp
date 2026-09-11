"""Synthetic local RP-06 and inbox-boundary evidence, not sandbox certification."""

import hashlib
import hmac
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from webhook_inbox import FixtureInbox, MAX_BODY_BYTES, verify_raw

ACTIVE = b"synthetic-active-secret-not-a-credential"
PREVIOUS = b"synthetic-previous-secret-not-a-credential"
RAW = b'{"entity":"event","account_id":"acc_synthetic","event":"payment.captured","payload":{"payment":{"entity":{"id":"pay_synthetic","amount":10000}}}}'


def sign(raw, key=ACTIVE):
    return hmac.new(key, raw, hashlib.sha256).hexdigest()


class WebhookInboxTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "synthetic-inbox.sqlite"
        self.inbox = FixtureInbox(self.path)

    def tearDown(self):
        self.inbox.close()
        self.directory.cleanup()

    def receive(self, raw=RAW, event_id="evt_synthetic", **kwargs):
        return self.inbox.receive(raw, kwargs.pop("signature", sign(raw)), event_id,
            scope=kwargs.pop("scope", "synthetic:test"), account_id="acc_synthetic", secrets=(ACTIVE, PREVIOUS), **kwargs)

    def test_known_hmac_vector(self):
        verify_raw(b"Hi There", "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7", (b"\x0b" * 20,))

    def test_active_secret(self):
        self.assertEqual(self.receive()["disposition"], "RECORDED")

    def test_previous_secret(self):
        self.assertEqual(self.receive(signature=sign(RAW, PREVIOUS))["disposition"], "RECORDED")

    def test_wrong_secret(self):
        with self.assertRaisesRegex(ValueError, "SIGNATURE_INVALID"):
            self.receive(signature=sign(RAW, b"wrong"))

    def test_changed_byte(self):
        with self.assertRaises(ValueError):
            self.receive(RAW.replace(b"10000", b"10001"), signature=sign(RAW))

    def test_json_reserialization_changes_signature(self):
        with self.assertRaises(ValueError):
            self.receive(json.dumps(json.loads(RAW)).encode(), signature=sign(RAW))

    def test_invalid_signatures(self):
        for signature in ("", "a" * 63, "g" * 64, None):
            with self.subTest(signature=signature), self.assertRaises(ValueError):
                self.receive(signature=signature)

    def test_missing_secret_fails_closed(self):
        for keys in ((), (b"",)):
            with self.subTest(keys=keys), self.assertRaises(ValueError):
                verify_raw(RAW, sign(RAW), keys)

    def test_event_id_validation(self):
        for event_id in ("", "bad\r\nheader", "x" * 201):
            with self.subTest(event_id=event_id), self.assertRaises(ValueError):
                self.receive(event_id=event_id)

    def test_duplicate_survives_connection_restart(self):
        first = self.receive()
        self.inbox.close(); self.inbox = FixtureInbox(self.path)
        second = self.receive()
        self.assertEqual(first["receipt_id"], second["receipt_id"])
        self.assertEqual(second["disposition"], "DUPLICATE")

    def test_event_id_not_part_of_signature(self):
        first = self.receive()
        second = self.receive(event_id="evt_changed_header")
        self.assertEqual(first["receipt_id"], second["receipt_id"])
        self.assertEqual(second["disposition"], "DUPLICATE")

    def test_same_event_id_different_signed_body_is_preserved(self):
        self.receive()
        result = self.receive(RAW.replace(b"10000", b"10001"))
        self.assertEqual(result["disposition"], "QUARANTINED")
        self.assertEqual(self.inbox.connection.execute("SELECT COUNT(*) FROM inbox").fetchone()[0], 2)

    def test_unknown_event_is_quarantined(self):
        self.assertEqual(self.receive(RAW.replace(b"payment.captured", b"future.event"))["disposition"], "QUARANTINED")

    def test_wrong_account_is_quarantined(self):
        self.assertEqual(self.receive(RAW.replace(b"acc_synthetic", b"acc_other"))["disposition"], "QUARANTINED")

    def test_signed_malformed_json_is_retained(self):
        for raw in (b"{", b'{"event":"one","event":"two"}', b'{"value":NaN}', b"[]", b"\xff",
                    RAW.replace(b'"payment.captured"', b'[]')):
            with self.subTest(raw=raw):
                self.assertEqual(self.receive(raw)["disposition"], "QUARANTINED")

    def test_unsigned_malformed_json_not_retained(self):
        with self.assertRaises(ValueError):
            self.receive(b"{", signature="0" * 64)
        self.assertEqual(self.inbox.connection.execute("SELECT COUNT(*) FROM inbox").fetchone()[0], 0)

    def test_scope_isolates_test_and_live_receipts(self):
        self.assertNotEqual(self.receive()["receipt_id"], self.receive(scope="synthetic:other")["receipt_id"])

    def test_failed_commit_does_not_acknowledge(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.receive(fail_before_commit=True)
        self.assertEqual(self.inbox.connection.execute("SELECT COUNT(*) FROM inbox").fetchone()[0], 0)
        self.assertEqual(self.receive()["disposition"], "RECORDED")

    def test_size_limit(self):
        with self.assertRaises(ValueError):
            self.receive(b"x" * (MAX_BODY_BYTES + 1))

    def test_financial_success_never_claimed(self):
        result = self.receive()
        self.assertTrue(result["durable"])
        self.assertFalse(result["financial_effect_applied"])


if __name__ == "__main__":
    unittest.main()
