# ADR-015 — Search and discovery: PostgreSQL FTS + pg_trgm + PostGIS with deterministic ranking

| Status | Accepted |
|---|---|
| Deciders | Tech lead, product |
| Related | ADR-005, ADR-006; `02-tdd.md §13` |

## Context
Search must cover missions, organizations, categories, causes, locations ("books near me"), with typo tolerance and deterministic ranking on distance, urgency, freshness, availability, organization reliability, and light user affinity. No ML before data exists. Payment amounts must never influence ranking. MVP scale: hundreds to low thousands of missions in one city.

## Decision
Postgres-native search: generated `tsvector` column (weighted title/summary/story), `pg_trgm` GIN index on title for fuzzy matching, `category_synonyms` table for query expansion, PostGIS distance, and a **config-weighted score** computed in SQL:
`0.30 text + 0.20 proximity + 0.15 urgency + 0.10 freshness + 0.10 availability + 0.10 org_reliability + 0.05 affinity`. Suggestions from `search_queries` (trending, 90 d) + categories + orgs. Home modules are fixed-intent queries plus an ops-curated `featured_missions` table.

## Alternatives
- **Elasticsearch/OpenSearch** — best relevance tooling; another cluster to run; excluded by the master prompt until justified.
- **Meilisearch/Typesense** — lightweight, great typo tolerance and speed; still a second data store to sync; revisit at > 50k active missions or p95 > 200 ms.
- **Algolia** — cost per record/ops; vendor.
- **Vector/semantic search** — no query volume yet to justify; NEXT experiment at most.

## Pros
Zero extra infra; transactional consistency (no index lag); geo and text in one query; ranking transparent and testable; weights tunable via config.

## Cons
Relevance tuning cruder than dedicated engines; Hindi/transliteration support weak in `simple` dictionary (LATER i18n will need `unaccent` and custom dictionaries or an engine).

## Risks
Slow queries as filters compound → covering partial indexes on live statuses; EXPLAIN budgets in CI (≤ 80 ms).

## Consequences
Ranking unit tests with fixture missions assert ordering; "no monetary input" enforced by test. Search analytics captured for future tuning.

## Migration path
`SearchRepository` interface; Meilisearch adapter fed by `MissionPublished/StatusChanged` events when triggers hit.
