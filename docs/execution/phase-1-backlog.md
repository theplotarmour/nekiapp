# Phase 1 implementation backlog

Prepared 2026-09-13 from [P1 scope and gate](../08-complete-phased-plan.md#6-phase-1--build-the-platform-and-design-foundation). These are engineering estimates in person-days, including review and local tests, not calendar promises. P0 is still open. Accountable roles are not assigned people. No ticket below is marked implemented.

## Work in dependency order

| Ticket | Deliverable and observable acceptance | Depends on | Role | Days |
|---|---|---|---|---:|
| P1-01 | Pinned monorepo/bootstrap, environment validation, format/lint commands; clean checkout reaches local health check | P0 foundation gate | Platform | 2 |
| P1-02 | Local Postgres/PostGIS, Redis, private storage emulator and scanner; health checks and isolated synthetic seeds | P1-01 | Platform | 2 |
| P1-03 | FastAPI factory, safe errors/request IDs, config validation, readiness, graceful shutdown; missing secrets reject startup outside test | P1-01 | Backend | 2 |
| P1-04 | SQLAlchemy sessions and Alembic foundation; apply/rollback on empty DB and FK/uniqueness checks | P1-02, P1-03, reviewed schema | Backend | 3 |
| P1-05 | Current-principal policy service, scoped roles, suspension/revocation; cross-user/org and stale-token denials | P1-04, permission matrix | Backend | 3 |
| P1-06 | MSG91/test OTP adapters, hashed challenges, expiry and resend/attempt limits; test provider cannot boot in production | P1-03, P1-04, SMS spike | Backend | 3 |
| P1-07 | Phone/IP/device rate limiting with fail-closed outage behavior; concurrent attempts cannot bypass limits | P1-02, P1-06 | Backend | 2 |
| P1-08 | Access token and rotating refresh family, hashed refresh credentials, reuse revocation, logout; concurrent refresh outcomes documented and tested | P1-05, P1-06 | Backend | 3 |
| P1-09 | Browser cookie/CORS/CSRF boundary, mobile token contract; cross-origin mutation and cookie flags tested | P1-08 | Backend/security | 2 |
| P1-10 | Me/profile/preferences/consent endpoints with version conflicts and data minimization; owner-only reads/writes | P1-05, P1-08 | Backend | 3 |
| P1-11 | Addresses, selected area and device registration; precise fields stay private; invalid geography/push ownership rejected | P1-10, map spike | Backend | 3 |
| P1-12 | Scoped idempotency, request hash, in-flight recovery and bounded response cache; revoked user cannot read cached result | P1-04, P1-05 | Backend | 3 |
| P1-13 | Cursor pagination, ETags/deltas, INR/UTC validation; stable tie ordering and tampered cursor rejection | P1-03, P1-04 | Backend | 2 |
| P1-14 | Atomic business/history/outbox writes and aggregate sequence; rollback and concurrent writers verified on Postgres | P1-04, reviewed event protocol | Backend | 3 |
| P1-15 | Ordered worker cursor and handler receipt transactions; parallel workers and crash-before/after-commit proof | P1-14 | Backend | 3 |
| P1-16 | Retry schedule, blocked-stream DLQ, scoped audited replay and watchdog; poison stream cannot leapfrog | P1-05, P1-15 | Backend | 3 |
| P1-17 | External delivery intents plus Redis hints; uncertain delivery/reconnect does not erase durable state | P1-15, provider adapters | Backend | 3 |
| P1-18 | Categories/synonyms/item types, reviewed service polygon, templates and server flags; synthetic fixtures cannot enable live money | P1-04, approved service area | Backend/product | 2 |
| P1-19 | Exported OpenAPI subset and generated Dart client; deterministically regenerate and compile with drift check | P1-03, reviewed contract workflow | Backend/Flutter | 3 |
| P1-20 | Shared theme/tokens, text styles, button/input/card/status primitives; light/dark and text-scale tests | P0 design handoff, P1-01 | Flutter/design | 3 |
| P1-21 | Navigation, sheets/dialogs, loading/empty/error/toast/avatar components; keyboard/focus and reduced-motion checks | P1-20 | Flutter/design | 3 |
| P1-22 | Riverpod repositories/controllers, Dio interceptors, serialized refresh and secure token storage; no credentials in logs/cache | P1-08, P1-09, P1-19 | Flutter | 3 |
| P1-23 | Welcome/phone/OTP/name flow with recovery and limits; real staging signup reaches named profile | P1-10, P1-20, P1-22 | Flutter | 3 |
| P1-24 | Permission explanations, manual location, skippable push; denied permissions preserve discovery | P1-11, P1-23 | Flutter | 2 |
| P1-25 | Five-tab retained shell and typed deep links; auth redirect restores intended destination and rejects private malformed links | P1-21, P1-22 | Flutter | 3 |
| P1-26 | Drift migrations/cache/queue, account switching and logout cleanup; restart, stale receipts, ownership and migration fixtures | P1-22, P1-25, offline spike | Flutter | 3 |
| P1-27 | Externalized strings, Indian money/plurals/dates and semantics; narrow width, 200% text and screen-reader pass | P1-20, P1-25 | Flutter/design | 2 |
| P1-28 | Privacy-allowlisted analytics, crash/trace wrapper and server flags; payload tests exclude phone, address, GPS and media URLs | P1-18, P1-22 | Platform/Flutter | 2 |
| P1-29 | Org/ops login and current-role navigation; forbidden deep link, keyboard and logout verified | P1-05, P1-09, P1-21, P1-22 | Flutter web | 3 |
| P1-30 | Read-only audit, health and DLQ portal views, pagination and redaction; unauthorized operators denied | P1-13, P1-16, P1-29 | Backend/Flutter web | 3 |
| P1-31 | Reviewed staging Terraform and secret references, migration job, backups and readiness-gated rollout | P1-02, P1-03, deployment spike/accounts | Platform | 3 |
| P1-32 | CI format/type/test/integration/contract/client-drift/secret/dependency/container checks and Android/iOS/web smoke builds | P1-19, P1-25, P1-29 | Platform | 3 |
| P1-33 | Staging acceptance suite for all six P1 gate scenarios, clean-bootstrap proof and recovery runbook | P1-01…32 | QA + leads | 3 |

Total engineering estimate: **89 person-days**. Individual tickets must be refined after the dependency spikes; split any ticket that exceeds three days during implementation. A ticket can be split without relaxing its acceptance criteria. Provider onboarding, policy decisions, hardware/account waits and participant research are not included in those 89 days.

## Capacity and cost model

Use five working days/week and explicitly account for support, review and coordination: effective weekly capacity = assigned full-time equivalents × 5 × availability fraction. Calendar floor = remaining person-days / effective weekly capacity; the actual schedule is longer where dependencies or specialist availability constrain concurrency.

| Illustrative staffing | Availability | Effective days/week | Effort-only floor for 89 days |
|---|---:|---:|---:|
| One engineer | 70% | 3.5 | 25.5 weeks |
| Two engineers | 70% | 7 | 12.8 weeks |
| Four engineers | 70% | 14 | 6.4 weeks |

These scenarios are not the actual team and do not translate AI session time into human delivery guarantees. Assign each role to a person, remove double-counting of shared roles, and schedule the dependency graph before publishing a date. The original W4–7 window is not a verified commitment.

Delivery cost = sum(ticket days × assigned role day rate) + provider setup + staging usage + devices/testing + contingency. Rates, currency, account budgets and contingency are **unassigned**, so no monetary total is invented. Maintain separate launch fee-subsidy funding (D2); it is not an engineering hosting expense.

## Exit review

P1 closes only with the six plan acceptance scenarios on staging, generated-client/build reproducibility, current authorization enforcement, and persisted worker recovery. Screenshots, local fake OTP, a successful deployment or this backlog alone cannot pass that gate. Later P2–P7 tickets inherit these foundations and their own domain acceptance gates.
