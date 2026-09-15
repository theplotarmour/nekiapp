# NEKI API foundation

Python **3.12.14**, FastAPI, SQLAlchemy async/psycopg and Alembic. `uv.lock` pins the resolved runtime and development dependencies. This is the first P1 implementation slice: application lifecycle, configuration validation, request IDs, safe errors, liveness/readiness and event-storage migration. OTP, profiles, authorization, worker processing and all contribution workflows remain unimplemented.

## Bootstrap

Install uv 0.12.15 and Python 3.12.14, then from `api/`:

```powershell
uv sync --locked
$env:NEKI_ENVIRONMENT = 'local'
$env:NEKI_DATABASE_URL = 'postgresql+psycopg://YOUR_USER:YOUR_PASSWORD@127.0.0.1:5432/YOUR_DATABASE'
.venv/Scripts/python -m alembic upgrade head
.venv/Scripts/python -m neki_api
```

Replace the example with a dedicated local database. Never point local migrations/tests at production. No database is created or migrated during application startup. Deployment migration credentials should be supplied to the migration process separately from the limited runtime role. The local entry point binds only `127.0.0.1:8000`, disables proxy-header trust and raw access logging, and selects the Windows event loop required by psycopg.

- `/health/live`: process/application alive, independent of database connectivity.
- `/health/ready`: 200 only when the DB is reachable and its Alembic revision exactly matches this release. Missing/mismatched migration or DB outage returns a redacted 503. This does not validate provider readiness or launch authorization.
- `/docs` and `/openapi.json`: available only in local/test. Unimplemented `/v1` routes return 404, not placeholder success.

## Configuration boundary

All settings use the `NEKI_` prefix. `DATABASE_URL` is required and must select `postgresql+psycopg` and a named database. Staging/production require a credential-bearing URL with `sslmode=verify-full`, exact HTTPS CORS origins, and reject the test SMS adapter. Payments cannot be enabled in this slice. Unknown settings supplied to the configuration constructor are rejected; secrets are masked in validation errors. No `.env` is automatically loaded.

`NEKI_ALLOWED_ORIGINS` is a JSON array of exact origins, for example `["http://localhost:3000"]` locally. CORS is not authentication or CSRF protection; no authenticated browser mutation endpoints exist yet. `NEKI_DATABASE_TIMEOUT_SECONDS` bounds readiness and statement waiting; the connection pool is bounded with no overflow.

Request IDs are UUIDs: valid inbound IDs are retained for correlation, invalid ones replaced. Responses use `no-store`, `nosniff` and the request-ID header. Error bodies never include raw validation input, driver messages or exception traces. Unhandled failures log the correlation ID only; richer sanitized tracing remains a later P1 task.

## Verify

```powershell
.venv/Scripts/ruff check .
.venv/Scripts/ruff format --check .
.venv/Scripts/mypy
.venv/Scripts/python export_openapi.py --check
$env:NEKI_TEST_PG_BIN = 'C:/Program Files/PostgreSQL/17/bin'
.venv/Scripts/python -m pytest -q
```

Database tests create an isolated loopback cluster from the supplied binaries, with unique test databases and cleanup. They never read an existing application DSN. Without `NEKI_TEST_PG_BIN`, PostgreSQL cases are explicitly skipped; such a run is not full integration evidence. Windows local evidence currently uses PostgreSQL 17.11; [CI](https://github.com/theplotarmour/nekiapp/actions/runs/34968476360) passed all 19 API tests and 14 outbox protocol tests against the accepted PostgreSQL 16 baseline. Local trust authentication in the isolated fixture is not deployment configuration.

`api/openapi.json` is generated exclusively from implemented FastAPI routes. Use `export_openapi.py` without `--check` after intentional route changes. `docs/api/openapi.json` remains the unimplemented P0 contract draft; migrate each implemented domain into the runtime export and reconcile its contract before generating a production Dart client. The two platform health routes do not imply implementation of the 324 draft operations.

Downgrade tests run only on disposable empty/synthetic databases. The initial downgrade drops event tables; never run it against real event history without a reviewed recovery plan. Production grants, complete event registry/handlers, provider integrations, PostGIS, Docker/staging provisioning and mobile/web app bootstrap remain open.
