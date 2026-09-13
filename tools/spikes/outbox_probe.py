"""Small executable model of ADR-014's proposed DB protocol, not an app worker."""

from datetime import timedelta
from uuid import uuid4

from psycopg.types.json import Jsonb

HANDLERS = ["counter.v1"]
DELAYS = (1, 5, 30, 300, 3600, 3600, 3600)


def create_stream(conn, stream_id, namespace="probe"):
    conn.execute("insert into streams(namespace,id) values (%s,%s)", (namespace, stream_id))
    conn.execute("insert into dispatch_cursors(namespace,stream_id) values (%s,%s)", (namespace, stream_id))


def produce(conn, stream_id, delta=1, namespace="probe", handlers=None):
    version, sequence = conn.execute(
        """update streams set state_value=state_value+%s, version=version+1,
           event_sequence=event_sequence+1 where namespace=%s and id=%s
           returning version,event_sequence""", (delta, namespace, stream_id)
    ).fetchone()
    event_id = uuid4()
    conn.execute(
        """insert into events(id,namespace,stream_id,sequence,aggregate_version,
           event_type,payload,required_handlers,correlation_id,causation_id)
           values (%s,%s,%s,%s,%s,'ProbeChanged.v1',%s,%s,%s,%s)""",
        (event_id, namespace, stream_id, sequence, version, Jsonb({"delta": delta}),
         HANDLERS if handlers is None else handlers, uuid4(), uuid4()),
    )
    return event_id


def claim(conn, now):
    """Hold one cursor lock for the caller's entire effect/receipt transaction."""
    cursor = conn.execute(
        """select c.namespace,c.stream_id,c.last_sequence from dispatch_cursors c
           where not c.blocked and c.next_attempt_at <= %s and exists (
             select 1 from events e where e.namespace=c.namespace and
             e.stream_id=c.stream_id and e.sequence>c.last_sequence)
           order by c.next_attempt_at,c.namespace,c.stream_id
           limit 1 for update of c skip locked""", (now,)
    ).fetchone()
    if cursor is None:
        return None
    namespace, stream_id, last_sequence = cursor
    event = conn.execute(
        """select id,sequence,payload,required_handlers from events
           where namespace=%s and stream_id=%s and sequence=%s""",
        (namespace, stream_id, last_sequence + 1),
    ).fetchone()
    if event is None:
        raise RuntimeError("EVENT_SEQUENCE_GAP")
    return (namespace, stream_id, *event)


def apply(conn, event, fail_after_effect=False):
    namespace, stream_id, event_id, sequence, payload, handlers = event
    if handlers != HANDLERS:
        raise RuntimeError("HANDLER_PLAN_UNSUPPORTED")
    if set(payload) != {"delta"} or type(payload["delta"]) is not int:
        raise RuntimeError("PAYLOAD_INVALID")
    receipt = conn.execute(
        "insert into handler_receipts(event_id,handler) values (%s,%s) on conflict do nothing returning event_id",
        (event_id, HANDLERS[0]),
    ).fetchone()
    if receipt:
        conn.execute("insert into effects(event_id,delta) values (%s,%s)", (event_id, payload["delta"]))
    if fail_after_effect:
        raise RuntimeError("INJECTED_CRASH_BEFORE_COMMIT")
    conn.execute(
        """update dispatch_cursors set last_sequence=%s,failures=0,
           next_attempt_at='-infinity' where namespace=%s and stream_id=%s""",
        (sequence, namespace, stream_id),
    )


def record_failure(conn, event, code, now):
    namespace, stream_id, event_id, sequence, _, _ = event
    last, failures, blocked = conn.execute(
        """select last_sequence,failures,blocked from dispatch_cursors
           where namespace=%s and stream_id=%s for update""", (namespace, stream_id)
    ).fetchone()
    if last != sequence - 1 or blocked:
        return False  # Another worker committed, or this stream already exhausted retries.
    failures += 1
    conn.execute(
        "insert into failed_attempts(event_id,attempt_in_cycle,failure_code,at) values (%s,%s,%s,%s)",
        (event_id, failures, code, now),
    )
    blocked = failures == 8
    due = now if blocked else now + timedelta(seconds=DELAYS[failures - 1])
    conn.execute(
        """update dispatch_cursors set failures=%s,blocked=%s,next_attempt_at=%s
           where namespace=%s and stream_id=%s""", (failures, blocked, due, namespace, stream_id)
    )
    if blocked:
        conn.execute("insert into dead_letters(event_id,failure_code,at) values (%s,%s,%s)", (event_id, code, now))
    return True


def process_one(conn, now, fail_after_effect=False, on_claim=None, on_failure=None):
    # Retain the cursor lock outside a savepoint. Rolling back a handler must not
    # expose its stream before the retry/blocked decision has been committed.
    with conn.transaction():
        event = claim(conn, now)
        if event is None:
            return None
        if on_claim:
            on_claim(event)
        try:
            with conn.transaction():
                apply(conn, event, fail_after_effect=fail_after_effect)
        except RuntimeError as error:
            if on_failure:
                on_failure(event)
            record_failure(conn, event, str(error), now)
            return "failed"
        return event[2]


def repair_for_test(conn, event, reason):
    """SQL recovery primitive only; production requires current scoped ops auth/step-up."""
    namespace, stream_id, event_id, sequence, _, _ = event
    last, blocked = conn.execute(
        "select last_sequence,blocked from dispatch_cursors where namespace=%s and stream_id=%s for update",
        (namespace, stream_id),
    ).fetchone()
    if not blocked or last != sequence - 1:
        raise RuntimeError("REPLAY_STATE_CONFLICT")
    conn.execute("insert into replay_audit(event_id,reason) values (%s,%s)", (event_id, reason))
    conn.execute(
        "update dispatch_cursors set blocked=false,failures=0,next_attempt_at='-infinity' where namespace=%s and stream_id=%s",
        (namespace, stream_id),
    )
