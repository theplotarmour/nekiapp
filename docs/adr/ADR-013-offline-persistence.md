# ADR-013 — Offline persistence: Drift (SQLite) with an outbox queue

| Status | Accepted |
|---|---|
| Deciders | Flutter lead |
| Related | ADR-002, ADR-014; `02-tdd.md §3.4, §15`; `01-prd.md §9` |

## Context
Must work offline for: home snapshot, viewed missions, history/impact records, last tracking state, drafts, and volunteer field actions (check-in/out, shipment transitions, proof photos) that queue and sync. Financial actions never queue. Conflicts resolved by server state. Web portals need local cache too (Drift runs on web via wasm/sql.js).

## Decision
**Drift** (SQLite) as the local relational store with typed DAOs and migrations; `flutter_secure_storage` for tokens only; file system for pending upload bytes referenced from an `outbox` table. Outbox rows: `{id, action_type, payload, idempotency_key, client_timestamp, state: PENDING|UPLOADING|ACKED|FAILED|REJECTED, attempts, last_error}`. `SyncCoordinator` drains on connectivity regained with exponential backoff; `409` → REJECTED with server state shown to user. Read caches use stale-while-revalidate with per-table TTLs.

## Alternatives
- **Isar** — fast NoSQL; relational joins (missions↔needs↔records) awkward; maintenance concerns in 2025–26.
- **Hive** — key-value only; no queries; fine for prefs, not for history.
- **sqflite raw** — no type safety, hand-written migrations.
- **ObjectBox** — proprietary sync; overkill.
- **PowerSync/ElectricSQL** — full bidirectional sync engines; attractive later, but MVP needs a narrow, auditable queue for a handful of actions, not general CRDT sync.

## Pros
Type-safe SQL, relational queries for feeds/history, migrations, web support, streams for reactive UI, mature.

## Cons
Code-gen; schema evolution discipline; SQLite on web adds bundle weight (portals only).

## Risks
Queue growth when offline long → cap pending photos (e.g., 50) and surface "Pending sync" UI; never queue money.

## Consequences
Every queued action carries `Idempotency-Key`; server accepts `client_timestamp` ≤ 24 h old and records both timestamps. Tests: airplane-mode E2E for check-in and duplicate prevention.

## Migration path
Adopt a sync engine later by replacing `SyncCoordinator`; table schemas remain.
