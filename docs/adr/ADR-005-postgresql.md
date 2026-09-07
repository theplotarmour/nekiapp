# ADR-005 — Primary database: PostgreSQL 16

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-006, ADR-013, ADR-015; `05-data-model.md` |

## Context
Strongly relational domain (missions ↔ needs ↔ contributions ↔ payments ↔ shipments ↔ proofs ↔ impact records), financial invariants, geospatial queries, full-text search at MVP scale, append-only ledger with hash chain, audit logs, JSON for flexible fields (proof_requirements, fee_policy).

## Decision
**PostgreSQL 16** managed (Neon or AWS RDS, Mumbai region), extensions: PostGIS, pg_trgm, pgcrypto, pg_partman. Alembic migrations with expand/contract. Media never stored in DB.

## Alternatives
- **MongoDB** — weak multi-document transactions for payment↔contribution↔mission consistency; geo and text OK but relational integrity is core here.
- **MySQL** — no PostGIS-class geospatial, weaker JSON and FTS, no partial indexes.
- **CockroachDB/Spanner** — global scale not needed; cost.
- **Supabase (Postgres)** — viable managed option; row-level security tempting but we keep authz in the app layer (ADR-012); revisit for LATER multi-tenant.

## Pros
ACID for money paths; rich indexing (GiST, GIN, partial); generated tsvector; enums; JSONB; partitioning for pings/audit; ecosystem (SQLAlchemy, Alembic, testcontainers); PITR from managed providers.

## Cons
Vertical scaling ceiling eventually; write-heavy location pings need partitioning and retention (designed).

## Risks
Enum churn in migrations → separate migration for enum additions; avoid renames.

## Consequences
`impact_records` protected by grants (no UPDATE/DELETE for app role except anonymization columns). Nightly invariant recompute job. Read replicas only when p95 metrics demand.

## Migration path
Schema-per-module convention enables future extraction. Search moves to Meilisearch/OpenSearch only per ADR-015 triggers.
