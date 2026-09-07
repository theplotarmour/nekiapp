# NEKI — Engineering Plan

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 2026-09-07 |
| Horizon | Phase 0 → MVP launch (Delhi) → NEXT |
| Related | `01-prd.md`, `02-tdd.md`, `03-user-flows.md`, `04-design-brief.md`, `05-data-model.md` |

---

## 1. Repository audit (current state)

| Item | Finding |
|---|---|
| Working tree | `NEKI_Master_RND_Architecture_Documentation_Prompt.md` (2,337 lines), `NEKI_Complete_UI_UX_Design_Specification.md` (4,509 lines), UI board PNG (2.1 MB), `.gitignore` (Flutter template + `.vercel`, `.env*`), `.DS_Store` (should be untracked). |
| History | `0e449c7` "init: neki flutter app with web build for vercel" → `748c5d7` removed the Flutter scaffold (android/, assets incl. `badge_blood.png`, `badge_top100.png`, `badge_tree.png`, `SpaceMono-Regular.ttf`, `analysis_options.yaml`, `README.md`) and added the master prompt → `b178a4f` UI spec → `ba237a5` image. |
| Reusable | Nothing in code. The removed scaffold used Space Mono and gamification badges — both conflict with the design brief; do not restore. `.gitignore` reusable. |
| Stack decisions | None implemented. All choices in `02-tdd.md §22` are proposals pending ADR sign-off. |
| Debt | None yet. Guard: no code before Phase 0 exit. |

Housekeeping tickets: remove `.DS_Store` from git; move source specs into `docs/source/`; rename PNG to `docs/source/ui-board-v1.png`; add repo `README.md` pointing at `docs/`.

---

## 2. Team and working assumptions

| Role | Count | Notes |
|---|---|---|
| Tech lead / backend | 1 | Owns TDD, ADRs, payments |
| Backend engineer | 1 | Missions, dispatch, media, admin API |
| Flutter engineer | 2 | One consumer app, one design system + portals |
| Product designer | 1 | Figma, assets, QA |
| Product / ops lead | 1 (founder) | Org onboarding, verification SOPs, launch content |
| QA (part-time from week 6) | 0.5 | E2E, device lab |

Cadence: 2-week sprints; weekly internal build; demo every sprint. Estimates in engineer-weeks (ew). Total MVP ≈ 20 weeks with this team; critical path is payments → tracking → proof/impact.

---

## 3. Repositories and structure

Monorepo `neki` (simplifies contract codegen and atomic changes):

```
neki/
  docs/                      this doc set, adr/, api-examples/, state-machines/
  api/                       FastAPI modular monolith + workers (Python)
  app/                       Flutter consumer app
  web/                       Flutter Web: org portal + ops console (shared design system via package)
  packages/
    neki_design_system/      Dart package: tokens + widgets (used by app and web)
    neki_api_client/         Generated Dart client from OpenAPI
  infra/                     Terraform, docker-compose, GitHub Actions
  tools/                     scripts: openapi export, seed, fixtures
```

Branching: trunk-based, short-lived branches, PR + 1 review, CI green required. Conventional commits.

---

## 4. Phases, epics, tickets

Ticket ids: `NK-<area>-<n>`. DoD in §7 applies to every ticket.

### Phase 0 — Documentation and decisions (weeks 1–2) · exit: all ADRs accepted, backlog groomed

| Ticket | Scope | Est |
|---|---|---|
| NK-DOC-1 | Write ADR-001…018 from `02-tdd.md §22` | 1.0 ew |
| NK-DOC-2 | Open-source R&D review table (inspect licenses/structure of the 8 listed repos; record findings) | 0.5 |
| NK-DOC-3 | State machine diagrams (mission, contribution, payment, shipment, assignment, verification) as Mermaid in `docs/state-machines/` | 0.3 |
| NK-DOC-4 | OpenAPI v1 skeleton for all MVP endpoints with schemas and error codes | 1.0 |
| NK-DOC-5 | Risk register owners assigned; legal questions Q2/Q6/Q7 sent | 0.2 |
| NK-DES-1 | Figma tokens + component library v1 (light/dark) | designer 2 w |
| NK-DES-2 | P0 screens × states, prototype Journeys A–D | designer 2 w (overlaps Phase 1) |

### Phase 1 — Foundation (weeks 3–6) · exit: signup → Home with real API on staging, CI/CD green

| Ticket | Scope | Est |
|---|---|---|
| NK-INF-1 | Monorepo, docker-compose (Postgres+PostGIS, Redis, ClamAV, MinIO), Makefile | 0.5 |
| NK-INF-2 | Terraform: staging env (managed Postgres, Redis, R2, Fly/ECS), secrets manager, Cloudflare | 1.5 |
| NK-INF-3 | GitHub Actions: lint, tests, OpenAPI export + client codegen diff, container build/scan, Flutter build, golden tests | 1.0 |
| NK-API-1 | FastAPI skeleton: config, DB session, Alembic, error contract, request id, structlog, OTel | 1.0 |
| NK-API-2 | Core: JWT + refresh rotation, RBAC policy layer, rate limiting, idempotency middleware, cursor pagination helper | 1.5 |
| NK-API-3 | Outbox: `domain_events`, relay worker (arq), handler registry, receipts, DLQ, admin replay endpoint | 1.0 |
| NK-API-4 | Auth module: OTP via MSG91, lockout, `/me`, devices, addresses | 1.0 |
| NK-API-5 | Catalogue: categories, subcategories, synonyms, item_types + seeds | 0.5 |
| NK-API-6 | Geo module: geocode/reverse proxy with Redis cache | 0.5 |
| NK-APP-1 | Flutter project, go_router shell with 5 tabs, Riverpod, Dio + interceptors, generated client wiring, Drift setup, secure storage | 1.5 |
| NK-APP-2 | `neki_design_system` v1: tokens, NekiButton/Chip/SearchField/Card/Skeleton/Empty/Error/BottomNav/TopBar, light+dark, golden tests | 2.0 |
| NK-APP-3 | Splash, Welcome, Phone, OTP, Name, permission rationale screens; session persistence | 1.5 |
| NK-APP-4 | Location selection sheet (GPS / search / saved) | 0.5 |
| NK-APP-5 | Analytics interface + PostHog, Sentry, feature flags client | 0.5 |

### Phase 2 — Marketplace (weeks 6–9) · exit: browse, search, mission detail, org page live with seeded missions

| Ticket | Scope | Est |
|---|---|---|
| NK-API-7 | Organizations module (read side), org public page | 0.5 |
| NK-API-8 | Missions module: model, needs, roles/slots, status machine + history, `GET /missions` with filters + PostGIS + ranking, `GET /missions/{id}`, bookmarks, updates | 2.5 |
| NK-API-9 | Home composer: modules, personalization ordering, Redis cache | 1.0 |
| NK-API-10 | Search: FTS + trgm + synonyms, suggest, trending | 1.0 |
| NK-API-11 | Media module: presigned upload, complete, processing worker (scan, EXIF, variants, blurhash), signed URLs | 1.5 |
| NK-APP-6 | Home screen with modules, skeletons, offline snapshot, header compress | 2.0 |
| NK-APP-7 | Explore: list, chips, filter sheet, infinite scroll | 1.5 |
| NK-APP-8 | Search screen: suggestions, grouped results | 1.0 |
| NK-APP-9 | Category page (data-driven) | 0.5 |
| NK-APP-10 | Mission Detail: hero collapse, sections, trust sheet, sticky footer with dynamic CTA, bookmark, share (deep links + universal links config) | 2.5 |
| NK-APP-11 | Organization public page | 0.5 |

### Phase 3 — Contribution and payments (weeks 9–12) · exit: real money in Razorpay test mode end-to-end incl. failure/timeout paths

| Ticket | Scope | Est |
|---|---|---|
| NK-API-12 | Contributions module: create (idempotent), status machine, expiry job, cancel, list/detail | 1.5 |
| NK-API-13 | Payments module: Razorpay order, verify, webhook (signature, dedupe), reconciliation worker, refunds, receipts; `SettlementStrategy` with `ManualPayoutStrategy` only (D3) | 2.0 |
| NK-API-14 | Fee policy engine + disclosure block fields (D2: platform absorbs gateway fee by default; block rendered from data) | 0.5 |
| NK-API-24 | Payouts module (D3): `payouts`/`payout_items`, status machine DRAFT→APPROVED→PAID→RECONCILED, two-person rule, outstanding-liability report per org, CSV export | 1.5 |
| NK-API-15 | Notifications module: templates, FCM sender worker, preferences, in-app center | 1.0 |
| NK-APP-12 | Contribute screen: type tabs, amount chips, other amount, fee line, keyboard-aware CTA | 1.0 |
| NK-APP-13 | Review, Razorpay SDK integration, Confirming state with poll/WS, failure screen, Thank You with motion + reduced-motion | 2.0 |
| NK-APP-14 | Notifications: FCM setup iOS/Android, deep-link routing, in-app center | 1.0 |
| NK-QA-1 | Payment E2E suite: success, failure, cancel, delayed webhook, double tap, app kill mid-checkout | 1.0 |

### Phase 4 — Items, volunteering, dispatch (weeks 12–15) · exit: item pickup and volunteer slot flows work with volunteer-executed pickup on staging

| Ticket | Scope | Est |
|---|---|---|
| NK-API-16 | Item contribution path: pickup slots, addresses, shipment creation | 1.0 |
| NK-API-17 | Dispatch module: assign/reassign, shipment transitions with actor rules, events, delays/reschedule | 1.5 |
| NK-API-18 | Volunteers module: `volunteer_applications` + ops approval (D7), roles/slots capacity, assignments (APPROVED guard), waitlist, check-in geofence, check-out, hours | 2.0 |
| NK-APP-15 | Items flow: item pick, qty, condition, photos (upload queue), address, slot, review | 2.0 |
| NK-APP-16 | Volunteer flow: application screen + pending/approved states (D7), role/date/slot sheet, assignment detail, check-in/out, offline outbox for field actions | 2.5 |
| NK-APP-17 | Volunteer pickup flow: assigned shipment view, transitions with photos, ping batching | 1.5 |

### Phase 5 — Tracking and realtime (weeks 14–16) · exit: contributor sees live state ≤ 3 s; fallback polling verified

| Ticket | Scope | Est |
|---|---|---|
| NK-API-19 | WS gateway: auth, channels, Redis fan-out, versioning, resync; tracking snapshot endpoint; ETA via Directions cache | 2.0 |
| NK-APP-18 | Tracking screen: map, route, mover interpolation, timeline, connection states, money-only variant | 2.5 |
| NK-APP-19 | Continue Your Impact module + returning-user priority | 0.5 |
| NK-QA-2 | Realtime/offline tests: disconnect, backoff, polling, resync; Toxiproxy | 0.5 |

### Phase 6 — Proof, verification, Impact Ledger (weeks 16–18) · exit: completed mission produces immutable NK record visible in app

| Ticket | Scope | Est |
|---|---|---|
| NK-API-20 | Proof module: submit, auto-checks (time window, geofence, phash), consent attestation | 1.0 |
| NK-API-21 | Verification module: queues, decisions, subject transitions, notifications | 1.0 |
| NK-API-22 | Impact module: record creation on completion, hash chain, corrections, summaries materialization, certificates (metadata only) | 1.5 |
| NK-APP-20 | Activity / Your Impact: segments, stats with "—" rule, feed, Impact Record screen, proof gallery with watermark overlay, share | 2.0 |
| NK-APP-21 | Profile: header, stats, rows, settings (privacy, notifications, delete account), help with request id | 1.5 |

### Phase 7 — Organization portal and ops console (weeks 10–19, parallel track on web engineer) · exit: ops can run launch without DB access

| Ticket | Scope | Est |
|---|---|---|
| NK-WEB-1 | Flutter Web shell reusing design system; auth for org_admin/ops roles | 1.0 |
| NK-WEB-2 | Org: apply + documents, dashboard, mission editor with needs builder, submit, contributions, assignments + attendance confirm, updates, proof upload with consent, impact | 4.0 |
| NK-WEB-3 | Ops (D6 Flutter Web): dashboard, missions (moderation + manual status/pickup/delivery/proof/impact actions), organizations verification queue, contributors, volunteers application queue (D7), contributions, **payouts** (D3: create/approve/pay/reconcile, liability report), dispatch board, proof review (side-by-side + auto-checks), verification, disputes/refunds, fraud signals, reports (CSV), health (outbox/DLQ/webhook lag), audit viewer | 6.0 |
| NK-API-23 | Admin API endpoints + audit log + fraud signal generators (velocity, dup image, speed, mock) | 2.0 |

### Phase 8 — Hardening and launch (weeks 18–20) · exit: closed beta in Delhi with 3 orgs, 10 missions

| Ticket | Scope | Est |
|---|---|---|
| NK-QA-3 | Full E2E on device lab (Pixel 6a, Samsung A-series, iPhone 12/15), accessibility audit (TalkBack/VoiceOver, 200% text), performance profiling vs budgets | 1.5 |
| NK-SEC-1 | Authz matrix tests all roles × routes; webhook forgery; IDOR fuzz; dependency scan; external pentest | 1.5 |
| NK-INF-4 | Prod env, backups + restore drill, alerts, on-call runbook, kill switches | 1.0 |
| NK-REL-1 | Store listings, privacy labels, universal links, Fastlane, TestFlight/Internal track, phased rollout | 1.0 |
| NK-OPS-1 | Verification SOP, proof review SOP, dispatch SOP, refund policy, support macros | founder |
| NK-CNT-1 | Launch content: 3 verified orgs onboarded, 10 missions with consented photography | founder + designer |

---

## 5. Milestones

| Week | Milestone | Demo |
|---|---|---|
| 2 | M0 Docs and ADRs accepted | Architecture walkthrough |
| 6 | M1 Foundation | Signup → Home (seeded) on staging; CI green |
| 9 | M2 Marketplace | Browse/search/detail with real media pipeline |
| 12 | M3 Money loop | ₹ contribution end-to-end in test mode with all failure paths |
| 15 | M4 Items + volunteers | Pickup scheduled, volunteer assigned, transitions from volunteer phone |
| 16 | M5 Live tracking | Two phones: volunteer moves, contributor sees it |
| 18 | M6 Impact | Mission completed → NK record, proof, verified stats |
| 19 | M7 Ops-ready | Ops console runs the full loop without DB |
| 20 | M8 Closed beta | 50 invited contributors, Delhi |
| 24 | Public launch (Delhi) | Phased rollout |

---

## 6. Dependencies and critical path

```
ADRs → API skeleton → Auth → Missions → Contributions → Payments → Tracking → Proof/Impact → Ops console → Beta
                    ↘ Design system → Home/Explore/Detail → Contribute/Success → Tracking UI → Impact UI
```
External blockers: Razorpay account + KYC (start week 1; Route not needed for MVP per D3); MSG91 DLT registration for OTP SMS (2–3 weeks; start week 1); Apple Developer + Play Console accounts; Google Maps billing; CA/CS/legal sign-off on money-flow structure and 80G handling before closed beta accepts live funds (week 20).

---

## 7. Definition of Done (every ticket)

UI implemented per design QA · loading/empty/error/offline states · accessibility (labels, 44 px, Dynamic Type 200%, reduced motion) · analytics events wired · backend endpoint with policy + validation · tests (unit + integration; E2E for critical flows) · performance checked against budget · docs updated (OpenAPI, ADR if architecture changed) · observability (logs/metrics/traces) · security review for anything touching auth, money, media, location.

---

## 8. Quality gates in CI

- Backend: ruff, mypy strict on `modules/*`, pytest ≥ 85% coverage on modules, Schemathesis contract run, migration up/down check, container vulnerability scan (no HIGH).
- Mobile: `dart analyze` zero warnings, `dart format` check, unit/widget ≥ 80% on domain + controllers, golden tests light/dark, size budget ≤ 35 MB, generated client in sync with OpenAPI (diff fails build).
- Both: secrets scan (gitleaks), dependency audit, conventional commit lint.

---

## 9. Risk register

| # | Risk | P | I | Early signal | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R1 | Low mission liquidity at launch | H | H | < 10 live missions in Delhi at beta | Founder onboards 5 orgs before beta; NEKI-run seed missions; campaigns in NEXT | Founder |
| R2 | Fake / low-quality organizations | M | H | Documents mismatch, no track record | Verification SOP, probation, reliability score, ops queue | Ops |
| R3 | Fake missions or proof | M | H | Duplicate images, geotag mismatch | Moderation before publish, auto-checks, human review, fraud signals | Ops/Eng |
| R4 | Payment reconciliation bugs (double charge, lost webhook) | M | H | Drift in nightly recompute; DLQ growth | Idempotency, webhook dedupe, reconciliation worker, E2E suite, kill switch | Tech lead |
| R5 | Volunteer no-shows break pickups | H | M | No-show rate > 15% | Reminders, reassign SOP, waitlist, partner courier in NEXT | Ops |
| R6 | Beneficiary privacy exposure via proof | M | H | Faces of minors in proof | Consent attestation, blur tool, ops checklist, signed URLs | Ops/Design |
| R7 | Location abuse or spoofing | L | M | Impossible speed, mock flag | Signals, geofence + organizer confirm | Eng |
| R8 | Regulatory uncertainty (donee status, 80G, Route) | M | H | Legal answers late | Decide by week 6; manual payout fallback designed | Founder/Legal |
| R9 | Low retention | M | H | 30-day repeat < 15% | Impact notifications, verified records, "Continue Your Impact" | Product |
| R10 | Operational cost of pickups | M | M | Cost/pickup > ₹150 | Drop-off option, slot batching, partner courier | Ops |
| R11 | App performance on low-end Android | M | M | Jank > 1%, cold start > 2 s | Budgets in CI, profiling on Pixel 6a/A-series | Flutter |
| R12 | Backend scaling on WS | L | M | WS p95 > 3 s | Redis fan-out, replica scaling, polling fallback | Backend |
| R13 | Notification overload | M | M | Opt-out rate > 10% | Category toggles, dedupe, quiet hours | Product |
| R14 | Vendor lock/outage (Razorpay, Maps, MSG91) | L | M | Provider incidents | Adapters behind interfaces; second SMS provider; static map fallback | Tech lead |
| R15 | Scope creep from LATER features | H | M | Corporate asks during MVP | Scope ladder enforced; NEXT backlog | Product |

---

## 10. Release plan

1. **Internal alpha (week 16)** — team + 5 friendly orgs' staff; TestFlight/Internal track; Razorpay test mode.
2. **Closed beta (week 20)** — 50 invited contributors, 3 verified orgs, 10 missions, live payments with ₹ caps (max ₹2,000/contribution, ₹20,000/day platform) via feature flags; ops on-call; daily reconciliation review.
3. **Open beta Delhi (week 22)** — remove caps gradually; phased rollout 10/50/100%; store listing live; support macros.
4. **Public launch Delhi (week 24)** — marketing; monitor R1/R9 metrics weekly.
5. **NEXT (months 4–6)** — campaigns, Give Anything, skills flow, certificates PDF, org mobile app, second city.

Rollback: kill switches for payments/tracking; previous app build kept in phased rollout; DB migrations backward-compatible.

---

## 11. Founder decisions — LOCKED 2026-09-07

Full text and rationale: `07-founder-decisions.md`.

| # | Decision | Final | Plan impact |
|---|---|---|---|
| D1 | Wallet | Removed everywhere in MVP | No wallet tickets; header = location pill |
| D2 | Fee policy | NEKI absorbs gateway fee for launch orgs; actual allocation block shown on every transaction | NK-API-14 renders block from `fee_policy`; copy lint bans "100%" string |
| D3 | Money flow | Manual payouts recorded in `payouts` + `payout_items`; Route → NEXT; legal sign-off before live funds | NK-API-13 drops Route; new NK-API-24 Payouts module; NK-WEB-3 Payouts UI; R8 stays open until CA/CS sign-off |
| D4 | Launch city | Delhi NCR only | Service-area polygon seed; feed default city |
| D5 | Payment provider | Razorpay behind `PaymentProvider` interface; approved methods only | NK-API-13 as planned; method list from remote config |
| D6 | Ops console | Flutter Web; manual intervention on every aggregate | NK-WEB-3 module list expanded (Contributors, Payouts, Reports) |
| D7 | Volunteer verification | Phone OTP + application → ops review → approved; KYC Phase 4+ | NK-API-18 adds `volunteer_applications` + approval endpoints; NK-APP-16 adds application screen; NK-WEB-3 adds Volunteers queue |

Remaining external blocker: **legal/CA sign-off on money-flow structure (D3\*)** before closed beta accepts live payments (week 20). Owner: founder.

---

## 12. Immediate next actions (this week)

1. Accept or amend ADR list; create `docs/adr/` with ADR-001…018.
2. Move source specs to `docs/source/`; untrack `.DS_Store`; add repo `README.md`.
3. Start vendor onboarding: Razorpay account + KYC, MSG91 DLT, Apple/Google developer accounts, Google Maps billing, Cloudflare account. Engage CA/CS for money-flow structure review (D3 legal caveat).
4. Designer starts Figma tokens + component library from `04-design-brief.md §4–5`.
5. Tech lead writes OpenAPI v1 skeleton from `02-tdd.md §8`.
6. Founder shortlists 5 Delhi organizations for verification pilot and photography consent.
