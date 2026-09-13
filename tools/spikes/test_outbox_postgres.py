"""Run with --pg-bin; creates/destroys only its own loopback cluster."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Barrier, Event
import unittest
from uuid import uuid4

import psycopg
from psycopg import sql

from outbox_probe import (
    DELAYS, apply, claim, create_stream, process_one, produce,
    record_failure, repair_for_test,
)
from postgres_runtime import PostgresRuntime

NOW = datetime(2026, 9, 13, tzinfo=timezone.utc)


class OutboxTests(unittest.TestCase):
    runtime = None

    def connection(self):
        conn = psycopg.connect(self.runtime.dsn)
        conn.execute(sql.SQL("set search_path to {} ").format(sql.Identifier(self.schema)))
        conn.execute("set statement_timeout = '10s'")
        conn.commit()
        return conn

    def setUp(self):
        self.schema = "probe_" + uuid4().hex
        with psycopg.connect(self.runtime.dsn) as conn:
            conn.execute(sql.SQL("create schema {} ").format(sql.Identifier(self.schema)))
        with self.connection() as conn:
            conn.execute(Path(__file__).with_name("outbox_schema.sql").read_text())
        self.a = uuid4()
        with self.connection() as conn:
            create_stream(conn, self.a)

    def tearDown(self):
        with psycopg.connect(self.runtime.dsn) as conn:
            conn.execute(sql.SQL("drop schema {} cascade").format(sql.Identifier(self.schema)))

    def scalar(self, query, args=()):
        with self.connection() as conn:
            return conn.execute(query, args).fetchone()[0]

    def enqueue(self, count=1, stream=None, namespace="probe", handlers=None):
        with self.connection() as conn:
            return [produce(conn, stream or self.a, namespace=namespace, handlers=handlers) for _ in range(count)]

    def test_producer_rollback_keeps_state_and_event_atomic(self):
        with self.assertRaisesRegex(RuntimeError, "producer crash"):
            with self.connection() as conn:
                produce(conn, self.a)
                raise RuntimeError("producer crash")
        self.assertEqual(self.scalar("select state_value from streams"), 0)
        self.assertEqual(self.scalar("select count(*) from events"), 0)

    def test_concurrent_producers_assign_contiguous_unique_sequences(self):
        barrier = Barrier(2)

        def writer():
            with self.connection() as conn:
                barrier.wait(timeout=10)
                return produce(conn, self.a)

        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs = [pool.submit(writer) for _ in range(2)]
            ids = [job.result(timeout=15) for job in jobs]
        self.assertEqual(len(set(ids)), 2)
        self.assertEqual(self.scalar("select array_agg(sequence order by sequence) from events"), [1, 2])
        self.assertEqual(self.scalar("select state_value from streams"), 2)

    def test_locked_stream_cannot_leapfrog_but_other_stream_can_progress(self):
        self.enqueue(2)
        b = uuid4()
        with self.connection() as conn:
            create_stream(conn, b)
        second_id = self.enqueue(stream=b)[0]
        with self.connection() as first:
            first.execute("select 1 from dispatch_cursors where stream_id=%s for update", (self.a,))
            with self.connection() as second:
                self.assertEqual(process_one(second, NOW), second_id)
            with self.connection() as second:
                self.assertIsNone(process_one(second, NOW))
            self.assertEqual(self.scalar("select last_sequence from dispatch_cursors where stream_id=%s", (self.a,)), 0)
        with self.connection() as conn:
            process_one(conn, NOW)
        with self.connection() as conn:
            process_one(conn, NOW)
        self.assertEqual(self.scalar("select last_sequence from dispatch_cursors where stream_id=%s", (self.a,)), 2)
        self.assertEqual(self.scalar("select count(*) from effects"), 3)

    def test_handler_exception_rolls_back_effect_and_receipt_but_records_failure(self):
        self.enqueue()
        with self.connection() as conn:
            self.assertEqual(process_one(conn, NOW, fail_after_effect=True), "failed")
        self.assertEqual(self.scalar("select count(*) from effects"), 0)
        self.assertEqual(self.scalar("select count(*) from handler_receipts"), 0)
        self.assertEqual(self.scalar("select last_sequence from dispatch_cursors"), 0)
        self.assertEqual(self.scalar("select count(*) from failed_attempts"), 1)
        with self.connection() as conn:
            self.assertIsNone(process_one(conn, NOW))
        with self.connection() as conn:
            self.assertIsNotNone(process_one(conn, NOW + timedelta(seconds=1)))
        self.assertEqual(self.scalar("select count(*) from effects"), 1)

    def test_retry_decision_keeps_cursor_locked_against_competing_worker(self):
        self.enqueue(2)
        claimed, release = Event(), Event()

        def parked_failure():
            def park(_):
                claimed.set()
                if not release.wait(timeout=10):
                    raise RuntimeError("test barrier timeout")
            with self.connection() as conn:
                return process_one(conn, NOW, True, on_failure=park)

        with ThreadPoolExecutor(max_workers=1) as pool:
            job = pool.submit(parked_failure)
            try:
                self.assertTrue(claimed.wait(timeout=10))
                with self.connection() as conn:
                    self.assertIsNone(process_one(conn, NOW))
            finally:
                release.set()
            self.assertEqual(job.result(timeout=15), "failed")
        with self.connection() as conn:
            self.assertIsNone(process_one(conn, NOW))
        self.assertEqual(self.scalar("select count(*) from failed_attempts"), 1)
        self.assertEqual(self.scalar("select count(*) from effects"), 0)

    def test_disconnect_after_effect_before_commit_rolls_back_and_retries(self):
        self.enqueue()
        conn = self.connection()
        event = claim(conn, NOW)
        apply(conn, event)
        conn.close()  # An uncommitted session disappearing must release locks and effects.
        self.assertEqual(self.scalar("select count(*) from effects"), 0)
        with self.connection() as retry:
            self.assertEqual(process_one(retry, NOW), event[2])
        self.assertEqual(self.scalar("select count(*) from handler_receipts"), 1)

    def test_commit_then_lost_ack_does_not_repeat_effect(self):
        event_id = self.enqueue()[0]
        conn = self.connection()
        apply(conn, claim(conn, NOW))
        conn.commit()
        conn.close()  # Caller discards acknowledgement and blindly retries.
        with self.connection() as retry:
            self.assertIsNone(process_one(retry, NOW))
        self.assertEqual(self.scalar("select event_id from effects"), event_id)
        self.assertEqual(self.scalar("select count(*) from handler_receipts"), 1)

    def test_poison_blocks_head_then_replay_preserves_attempts_and_identity(self):
        ids = self.enqueue(2)
        current = NOW
        event = None
        for index in range(8):
            with self.connection() as conn:
                def capture(value):
                    nonlocal event
                    event = value
                self.assertEqual(process_one(conn, current, True, capture), "failed")
            if index < 7:
                self.assertEqual(self.scalar("select next_attempt_at from dispatch_cursors"), current + timedelta(seconds=DELAYS[index]))
                current += timedelta(seconds=DELAYS[index])
        self.assertTrue(self.scalar("select blocked from dispatch_cursors"))
        self.assertEqual(self.scalar("select count(*) from effects"), 0)
        self.assertEqual(self.scalar("select count(*) from failed_attempts"), 8)
        self.assertEqual(self.scalar("select event_id from dead_letters"), ids[0])
        with self.connection() as conn:
            self.assertIsNone(process_one(conn, current + timedelta(days=1)))
        with self.connection() as conn:
            repair_for_test(conn, event, "Synthetic handler repaired")
        with self.connection() as conn:
            self.assertEqual(process_one(conn, current), ids[0])
        with self.connection() as conn:
            self.assertEqual(process_one(conn, current), ids[1])
        self.assertEqual(self.scalar("select event_id from replay_audit"), ids[0])
        self.assertEqual(self.scalar("select count(*) from failed_attempts"), 8)
        self.assertEqual(self.scalar("select count(*) from effects"), 2)

    def test_unsupported_handler_plan_cannot_silently_skip_effect(self):
        self.enqueue(handlers=["counter.v2"])
        with self.connection() as conn:
            self.assertEqual(process_one(conn, NOW), "failed")
        self.assertEqual(self.scalar("select count(*) from handler_receipts"), 0)
        self.assertEqual(self.scalar("select failure_code from failed_attempts"), "HANDLER_PLAN_UNSUPPORTED")

    def test_stale_failure_cannot_block_already_committed_event(self):
        self.enqueue()
        with self.connection() as conn:
            event = claim(conn, NOW)
            apply(conn, event)
        with self.connection() as conn:
            self.assertFalse(record_failure(conn, event, "late failure", NOW))
        self.assertEqual(self.scalar("select count(*) from failed_attempts"), 0)

    def test_event_and_attempt_history_cannot_be_rewritten(self):
        self.enqueue()
        with self.assertRaises(psycopg.errors.CheckViolation):
            with self.connection() as conn:
                conn.execute("update events set payload='{}'")
        with self.connection() as conn:
            process_one(conn, NOW, True)
        with self.assertRaises(psycopg.errors.CheckViolation):
            with self.connection() as conn:
                conn.execute("delete from failed_attempts")

    def test_same_uuid_in_different_namespace_is_an_independent_stream(self):
        self.enqueue()
        with self.connection() as conn:
            create_stream(conn, self.a, "other")
        self.enqueue(namespace="other")
        with self.connection() as conn:
            process_one(conn, NOW)
        with self.connection() as conn:
            process_one(conn, NOW)
        self.assertEqual(self.scalar("select count(*) from effects"), 2)

    def test_sequence_gap_cannot_execute_a_later_event(self):
        with self.connection() as conn:
            conn.execute("update streams set event_sequence=1")  # Explicit integrity-corruption fixture.
        self.enqueue()
        with self.assertRaisesRegex(RuntimeError, "EVENT_SEQUENCE_GAP"):
            with self.connection() as conn:
                process_one(conn, NOW)
        self.assertEqual(self.scalar("select count(*) from effects"), 0)

    def test_database_restart_preserves_outbox_and_committed_receipts(self):
        ids = self.enqueue(2)
        with self.connection() as conn:
            self.assertEqual(process_one(conn, NOW), ids[0])
        self.runtime.restart()
        with self.connection() as conn:
            self.assertEqual(process_one(conn, NOW), ids[1])
        self.assertEqual(self.scalar("select count(*) from effects"), 2)
        self.assertEqual(self.scalar("select count(*) from handler_receipts"), 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pg-bin", required=True, help="Directory containing initdb, pg_ctl and postgres")
    args = parser.parse_args()
    runtime = PostgresRuntime(args.pg_bin)
    try:
        runtime.start()
        OutboxTests.runtime = runtime
        print(runtime.run("postgres", "--version").stdout.strip(), flush=True)
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(OutboxTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        runtime.close()
    raise SystemExit(0 if result.wasSuccessful() else 1)
