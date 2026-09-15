# Phase 1 execution register

**Started:** 2026-09-15. **Status:** In progress; P1 acceptance gate not passed.

Entry is the user's explicit instruction to start P1, recorded in the [P0 handoff](p0-handoff.md). Outstanding P0 policy/provider/design evidence remains visible; this is not a retroactive P0 completion claim.

## First implementation slice

| Backlog item | Current state |
|---|---|
| P1-01 repository/bootstrap | API package, Python 3.12.14 pin, uv lockfile, reproducible setup/check commands delivered. Flutter apps/shared packages/infra remain open. |
| P1-03 API factory/config | Lifecycle and pooled DB disposal, redacted configuration failures, safe common errors, UUID correlation, liveness/readiness and exact-origin CORS implemented. Full tracing and domain errors remain open. |
| P1-04 database/migrations | Async transaction context and first event-storage Alembic migration implemented; disposable-DB upgrade/downgrade/reapply and rollback tests supplied. Full domain schema and production grants remain open. |
| P1-19 contract export | Runtime OpenAPI exports two implemented health routes; deterministic export check. Domain export migration and generated Dart client remain open. |
| P1-32 CI | API format/lint/type/contract/unit/PostgreSQL 16 job added. Remote PostgreSQL 16 execution passed; see the exact run/commit evidence below. |

## Acceptance boundaries

The runtime is a backend foundation, not a user-ready app. It has no OTP/session/profile endpoint, policy enforcement service, event consumers, Flutter login/shell or staging deployment. Public readiness checks database reachability and exact migration revision; it is not a launch-readiness endpoint. P1's six end-to-end acceptance scenarios have not passed.

The next implementation slice is P1-02/P1-05–09: local infrastructure and role/session/OTP foundations, with existing D7 and ADR-012 timeouts, reviewed retry semantics, current authorization and test-provider exclusion. Provider-dependent staging acceptance still requires configured accounts.

Reproduce checks with [API README](../../api/README.md). Local PostgreSQL tests own a temporary cluster and never consume the application's database URL. Do not run migration downgrades on live data.


## Local evidence — 2026-09-15

Python 3.12.14 with the committed uv lock: Ruff lint/format and strict mypy pass; runtime OpenAPI regenerates without drift. **19 tests passed** against an isolated PostgreSQL 17.11 cluster, including configuration rejection, secret-safe errors, UUID request IDs, exact-origin preflight, absent-route 404, missing/mismatched schema readiness, migration downgrade/reapply, transaction rollback/commit, event sequence uniqueness, FK enforcement and immutable-event writes. Two upstream Starlette/httpx/AnyIO deprecation warnings remain visible; they are not suppressed. [CI run 34968476360](https://github.com/theplotarmour/nekiapp/actions/runs/34968476360) passed on commit `510f166`: all 19 API tests and all 14 P0 outbox tests passed on PostgreSQL 16.15, alongside format/lint/type/export checks. The initial Linux cluster startup failed; isolating Unix sockets fixed the harness without weakening database assertions. GitHub also reports a Node-20-action deprecation warning; the actions currently run under Node 24.

This is actual P1 backend code and tests, not a design simulation. Its bounded success does not complete P1 authentication, authorization, worker, infrastructure or client acceptance.
