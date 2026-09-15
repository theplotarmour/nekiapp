# PostgreSQL outbox ordering and recovery probe

Executed 2026-09-13 on **PostgreSQL 17.11**, Python 3.11, psycopg/psycopg-binary 3.3.5. All **14 tests passed** (final run 8.669 seconds excluding cluster initialization). This is a synthetic P0 protocol/schema probe, not an application worker, full migration or production authorization proof. ADR-005 still pins PostgreSQL 16; repeat against that target and managed infrastructure before claiming deployment compatibility.

## Reproduction and isolation

```powershell
.venv-contracts/Scripts/python -m pip install -r tools/spikes/requirements-postgres.txt
.venv-contracts/Scripts/python tools/spikes/test_outbox_postgres.py --pg-bin 'C:/Program Files/PostgreSQL/17/bin'
```

The runner uses installed binaries to initialize a new UUID-named cluster under ignored `tools/spikes/.postgres-runtime/`, binds loopback on an ephemeral port, and creates synthetic schemas. It does not consume `DATABASE_URL`, credentials or the existing PostgreSQL service. Local trust authentication is confined to this throwaway loopback cluster; it is not a deployment configuration. Normal database durability settings are retained. Cleanup stops only its own data directory, resolves/checks the cleanup path and removes the owned cluster. A Windows inherited-pipe startup timeout was fixed by directing command output to owned files; the successful run used that fix.

[Executable schema](../../tools/spikes/outbox_schema.sql), [producer/worker model](../../tools/spikes/outbox_probe.py), [tests](../../tools/spikes/test_outbox_postgres.py), [cluster lifecycle](../../tools/spikes/postgres_runtime.py).

## Findings and executed cases

The [PostgreSQL lock documentation](https://www.postgresql.org/docs/17/explicit-locking.html) and [SKIP LOCKED semantics](https://www.postgresql.org/docs/17/sql-select.html) informed the model. The application must lock the stream cursor, not just adjacent event rows. The probe distinguishes state version from event sequence and includes the aggregate namespace in uniqueness/cursor keys.

| Executed case | Observed result |
|---|---|
| Producer abort | Neither business state nor event committed |
| Concurrent producers with a barrier | Two distinct events, contiguous sequences 1/2, state incremented twice |
| One stream locked, second worker active | Other stream progressed; later same-stream event could not leapfrog |
| Handler fails after effect write | Effect and receipt rolled back; one attempt recorded; retry not runnable before due time |
| Connection disappears before commit | Effect rolled back and retry created one receipt/effect |
| Commit succeeds, caller discards acknowledgement | Blind retry found no pending head; original receipt/effect remained singular |
| Eight poison attempts | Original event retained, stream blocked, later event unprocessed, DLQ retained original identity |
| Repair and replay after poison | Same event ID, full failed-attempt history and replay reason retained; two ordered events completed |
| Unknown required handler plan | Failure visible; no receipt or effect falsely marked successful |
| Delayed failure report after success | Committed cursor unchanged; no stale retry/DLQ inserted |
| Evidence rewrite/delete | Database rejected event rewrite and attempt deletion |
| Same UUID under different namespaces | Independent streams both completed |
| Missing head sequence | Explicit sequence-gap error; later event did not execute |
| Database restart | Committed receipt and pending next event survived; second event processed once |

The retry-lock case additionally parks a failing worker **after its handler savepoint rollback and before failure recording**. A competing worker cannot claim its stream during that interval. This makes the failure-recording race observable rather than relying on timing sleeps.

## Protocol correction

The earlier draft proposed rolling back the whole event transaction and then recording its failure. That releases the cursor lock between operations, permitting a competing worker to process the same head before the retry decision is persisted. The probe instead keeps an outer transaction and cursor lock, runs handlers/effects/receipts inside a savepoint, rolls that savepoint back on a known handler failure, and records retry/blocked status before committing the outer transaction. Psycopg's [transaction/savepoint behavior](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) is used explicitly.

A genuine connection/process/database failure may lose the attempt record because the outer transaction also rolls back; durable state remains pending. A production watchdog must detect repeated crashes/stale heads. Do not describe every crash as a counted business-handler retry. Cross-aggregate lock ordering and deadlock retry require additional application-specific tests.

## Limits and remaining gates

The counter handler is synthetic. The schema does not model all NEKI business aggregates, approved per-event payloads, migration compatibility, production grants or all event consumers. `repair_for_test` is a SQL recovery primitive, not authorized ops replay. The sequence-gap error still needs production quarantine/alert plumbing. The receipt PK does not by itself guarantee exactly-once external effects.

Not executed: PostgreSQL 16/PostGIS target, arbitrary process kill or power loss, Redis/arq integration, external delivery uncertainty/reconciliation, scoped replay/step-up API, deployment handler migrations, notification occurrence delivery, cross-aggregate dependency reconciliation, or provider end-to-end cases. EV-01–06 receive bounded database evidence; EV-07–12 remain open except the unknown-handler rejection subcase. G13 remains partial.


## Target-version follow-up — 2026-09-15

[CI run 34968476360](https://github.com/theplotarmour/nekiapp/actions/runs/34968476360) at `510f166` passes all 14 outbox tests on PostgreSQL 16.15/Linux using the same isolated protocol fixture. An initial cluster startup failure was resolved by disabling unnecessary Unix sockets for this TCP-only fixture and exposing startup-log evidence. This closes the target-major-version gap for these synthetic database cases. PostGIS, managed service semantics, production handlers/grants and external delivery remain unverified.
