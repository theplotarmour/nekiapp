# ADR-004 — Backend: FastAPI modular monolith with transactional outbox

| Status | Accepted |
|---|---|
| Deciders | Tech lead, backend engineer |
| Related | ADR-005, ADR-007, ADR-014; `02-tdd.md §4, §7` |

## Context
Master prompt mandates a modular monolith, no Kubernetes/Kafka/microservices prematurely, clear domain boundaries for later extraction. Domains: auth, users, organizations, missions, contributions, payments, volunteers, dispatch, tracking, proof, verification, impact, campaigns, notifications, search, media, geo, analytics, admin. Team: 2 backend engineers. India-first latency (host in ap-south-1 / Mumbai).

## Decision
Single deployable **FastAPI** (Python 3.12, Pydantic v2, SQLAlchemy 2 async, Alembic) organized as `modules/<domain>/{router,service,repository,models,schemas,events,policies}`. Modules communicate via service interfaces or domain events; no cross-module ORM imports. Background work via `arq` workers running the same image. Events persisted in `domain_events` outbox in the same transaction as state changes.

## Alternatives
- **Microservices from day one** — operational overhead, distributed transactions for payments↔contributions↔missions, premature.
- **Django + DRF** — mature admin (tempting for ops console) but sync-first ORM, heavier for WebSockets; FastAPI async fits realtime and outbound provider calls. Ops console is built in Flutter Web anyway (ADR-001).
- **NestJS (TypeScript)** — viable; team Python strength and data/ML adjacency favor Python.
- **Go** — performance headroom not needed at MVP; slower iteration for a 2-person team.

## Pros
One deploy, one DB transaction boundary, simple local dev (docker compose), OpenAPI generated for client codegen, async I/O for provider calls and WS, easy extraction later because boundaries are explicit.

## Cons
Discipline required to keep boundaries; Python GIL means scale by replicas (fine behind LB); type safety weaker than TS/Go (mitigate with mypy strict).

## Risks
Module coupling creep → lint rule (import-linter) enforcing allowed dependency graph; PR review checklist.

## Consequences
Extraction criteria documented: independent scaling need proven by metrics, distinct deploy cadence, or distinct security boundary. First candidates: media processing, tracking WS gateway, notifications. Workers and API share code and image.

## Migration path
Extract a module by (1) moving its tables to a schema, (2) replacing service interface with HTTP/gRPC client, (3) consuming its events over Redis Streams or a broker if volume demands.
