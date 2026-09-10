# NEKI — Technical Design Document (TDD)

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 2026-09-07 |
| Status | Draft for review |
| Scope | MVP platform: Flutter consumer app, org web portal, ops console, FastAPI modular monolith |
| Related | `01-prd.md`, `05-data-model.md`, `06-eng-plan.md` |

---

## 1. Context and constraints

- Greenfield. The repository currently contains only two specification documents and one UI board image. A Flutter scaffold (with a web build targeting Vercel) existed at commit `0e449c7` and was removed in `748c5d7`; nothing from it is reused.
- Constraints from the master prompt: modular monolith, no Kubernetes/Kafka/Elasticsearch/ML at MVP, Flutter mobile, FastAPI backend, PostgreSQL + PostGIS, Redis, object storage for media, WebSockets only where live state matters, cursor pagination, idempotency on important writes, server is source of truth for payments and authorization.
- India-first: INR, UPI, phone-OTP auth, Delhi launch.

---

## 2. System architecture

```
┌──────────────┐  ┌─────────────────┐  ┌────────────────┐
│ Flutter app  │  │ Org portal (web)│  │ Ops console    │
│ iOS/Android  │  │ Flutter Web     │  │ Flutter Web    │
└──────┬───────┘  └────────┬────────┘  └───────┬────────┘
       │ HTTPS/JSON + WSS  │                   │
       ▼                   ▼                   ▼
┌───────────────────────────────────────────────────────┐
│ neki-api  (FastAPI, modular monolith, ASGI/uvicorn)   │
│  auth · users · organizations · missions · needs      │
│  contributions · payments · volunteers · dispatch     │
│  tracking · proof · verification · impact · campaigns │
│  notifications · search · analytics · admin · media   │
│  ── in-process event bus + transactional outbox ──    │
└───────┬───────────────┬──────────────┬────────────────┘
        │               │              │
        ▼               ▼              ▼
┌──────────────┐ ┌────────────┐ ┌────────────────────────┐
│ PostgreSQL 16│ │ Redis 7    │ │ neki-worker (same code,│
│ + PostGIS    │ │ cache/pubsub│ │ arq jobs: outbox relay,│
│ + pg_trgm    │ │ rate-limit │ │ media, notifications,  │
└──────────────┘ │ ws fanout  │ │ reconcile, ranking)    │
                 └────────────┘ └────────────────────────┘
        │
        ▼ external
  Razorpay (payments) · Cloudflare R2 + CDN (media)
  Google Maps Platform (geocode/directions/tiles) · FCM (push) · MSG91 (SMS OTP)
  Sentry · OpenTelemetry → Grafana Cloud · PostHog (product analytics)
```

Single deployable API image; worker is the same image with a different entrypoint. Horizontal scale by adding API replicas behind a load balancer; WebSocket fan-out through Redis pub/sub so any replica can push to any connected client.

---

## 3. Mobile architecture (Flutter)

### 3.1 Stack

| Concern | Choice | Reason |
|---|---|---|
| Language/SDK | Flutter 3.x stable, Dart 3 | Single codebase iOS/Android/web (portal + console reuse design system) |
| State | **Riverpod 2 (code-gen)** | Compile-time safe providers, fine-grained rebuilds, testable without widget tree, `AsyncNotifier` maps cleanly to loading/error/data, easy stream integration for realtime. BLoC evaluated: more boilerplate per feature, weaker DI story. |
| Navigation | **go_router** with typed routes | Deep links (`neki://`, universal links), nested shell for bottom nav, redirect guards for auth |
| Networking | Dio + interceptors (auth, retry, idempotency, logging) + generated client from OpenAPI | Contract-first; generated DTOs avoid hand-written drift |
| Models | Freezed + json_serializable | Immutable, union types for states |
| Local DB | **Drift (SQLite)** | Relational cache for missions/records; typed queries; migrations; works on web via wasm for portal |
| Secure storage | flutter_secure_storage | Tokens |
| Images | cached_network_image + BlurHash placeholders | Progressive load |
| Maps | google_maps_flutter | Route polyline via backend proxy |
| Realtime | web_socket_channel + custom reconnect manager | Fallback polling |
| Push | firebase_messaging | FCM both platforms |
| Analytics | PostHog Flutter SDK behind an `Analytics` interface | Swappable |
| Crash | Sentry Flutter | |
| Payments | razorpay_flutter | Provider SDK handles PCI surface |
| Animations | flutter_animate + implicit animations; Rive for butterfly/success | Restrained motion |

### 3.2 Layering and package layout

```
lib/
  app/                bootstrap, router, theme, l10n
  core/
    design_system/    NekiColors, NekiTypography, NekiSpacing, NekiRadius, NekiShadows, NekiMotion, widgets (NekiButton, NekiCard, …)
    network/          Dio setup, interceptors, ApiError mapping, generated client
    storage/          Drift database, secure storage, cache policies
    realtime/         WsClient, ReconnectPolicy, ChannelSubscription
    offline/          OutboxQueue (pending local actions), SyncCoordinator
    analytics/        Analytics interface, event definitions
    location/         LocationService, permission flows
    auth/             Session, token refresh
  features/
    <feature>/
      data/           repositories impl, DTO↔domain mappers, local DAOs
      domain/         entities, value objects, repository interfaces, use cases
      presentation/   controllers (Riverpod notifiers), screens, widgets
  shared/             cross-feature widgets, formatters (INR, dates), models
```

Rules: `presentation → domain ← data`. Widgets never import Dio or Drift. Repository interfaces live in `domain`; implementations in `data`; wired via Riverpod providers in a feature `providers.dart`. Features: `auth`, `onboarding`, `home`, `explore`, `search`, `category`, `mission`, `contribution`, `payment`, `tracking`, `volunteer`, `impact`, `profile`, `notifications`, `organization` (public page).

### 3.3 State conventions

- Every screen controller is an `AsyncNotifier<State>` (or `Notifier` for pure UI state). UI renders `loading / error / data / empty` from a sealed state; empty is a data variant, not an error.
- Optimistic updates only for reversible, low-risk actions (bookmark, notification read). Never for payments, volunteer confirmation, or proof submission.
- Realtime: `TrackingController` merges REST snapshot + WS events; server `version` field resolves ordering; on reconnect, refetch snapshot.
- Pagination: `PagedState<T>{items, nextCursor, hasMore, isLoadingMore}`.

### 3.4 Local data and offline

| Data | Store | TTL / policy |
|---|---|---|
| Session tokens | Secure storage | Until logout / rotation |
| Profile, preferences | Drift | Refresh on launch |
| Selected location | Drift | Persistent |
| Home feed snapshot | Drift (JSON blob per module) | Stale-while-revalidate, 24 h |
| Viewed mission details | Drift | LRU 100, 7 d |
| Bookmarks, contributions, impact records | Drift | Full sync, delta by `updated_after` |
| Active tracking last state | Drift | Until completed + 7 d |
| Pending uploads (proof photos) | File system + Drift outbox row | Until acked |
| Pending field actions (check-in/out, status) | Drift outbox | Until acked |

Outbox queue: `LOCAL ACTION → PENDING → UPLOADING → ACKED | FAILED(retryable) | REJECTED(conflict)`. Each action carries a client-generated `idempotency_key` and `client_timestamp`. Retry with exponential backoff on connectivity regained. Conflicts (server already advanced state) return `409` with server state; client discards local and shows explanation. Financial actions are never queued.

### 3.5 Error mapping

Backend error contract `{error:{code,message,request_id,details?}}` → `ApiError` sealed class → per-feature copy. Unknown codes fall back to "Something went wrong. Let's try again." Request id shown in Help & Support "Report a problem".

---

## 4. Backend architecture (FastAPI modular monolith)

### 4.1 Stack

Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 (async) + Alembic, asyncpg, redis-py asyncio, `arq` for background jobs, `httpx` outbound, `structlog`, OpenTelemetry SDK, `pytest` + `pytest-asyncio` + `testcontainers`.

### 4.2 Module layout

```
neki_api/
  app.py                 FastAPI factory, router mounting, middleware
  core/                  config, db session, redis, security (JWT, RBAC), errors, idempotency, pagination, events (bus + outbox)
  modules/
    auth/        users/        organizations/   missions/     needs/
    contributions/ payments/   volunteers/      dispatch/     tracking/
    proof/       verification/ impact/          campaigns/    notifications/
    search/      media/        geo/             analytics/    admin/
  each module:
    router.py  (HTTP)   service.py (use cases)  repository.py (SQL)
    models.py (ORM)     schemas.py (Pydantic)   events.py (domain events emitted/consumed)
    policies.py (authorization rules)           tests/
  workers/
    outbox_relay.py  media_pipeline.py  notifications.py  payment_reconcile.py  ranking_refresh.py  retention.py
```

### 4.3 Boundary rules

- Modules communicate through **service interfaces** or **domain events**, never by importing another module's `repository` or ORM models. Cross-module reads needing joins go through read-model queries in the consuming module (allowed inside a monolith) and are marked `# cross-module read` for later extraction.
- Every write use case runs in one DB transaction and appends domain events to `domain_events` (outbox) in the same transaction. The relay worker publishes to in-process handlers and Redis pub/sub (WS fan-out), then marks delivered.
- Extraction criteria: a module becomes a service only when it has (a) independent scaling need proven by metrics, (b) a distinct deploy cadence, or (c) a distinct security boundary. Candidates: `media`, `tracking`, `notifications`.

### 4.4 Authorization

- JWT access token (15 min) + rotating refresh (30 d), device-bound. Claims: `sub`, `roles[]`, `org_id?`.
- Roles: `contributor` (default), `volunteer` (capability flag), `org_admin`, `ops_agent`, `ops_lead`, `finance`, `super_admin`.
- Every endpoint declares a policy; policies check ownership (`contribution.user_id == sub`), org scope (`mission.organization_id == token.org_id`), or role. No client-supplied ids trusted for scoping; all queries filter by principal.

---

## 5. Domain model overview

Core aggregates (DDL in `05-data-model.md`):

- **Organization** — verified publisher of missions.
- **Mission** — quantified need with one or more **Needs** (money target, item type+quantity, volunteer slots), location, deadline, status.
- **Contribution** — a user's pledge against a mission: type MONEY / ITEM / TIME / SKILL; links to **Payment** (money), **Shipment** (item), **Assignment** (time).
- **Shipment** — physical movement with tracking states and **LocationPings**.
- **Assignment** — volunteer slot booking with check-in/out.
- **Proof** — evidence attached to a mission/shipment/assignment; **Verification** — review decision.
- **ImpactRecord** — immutable ledger entry per completed contribution; corrections via **ImpactCorrection** events.
- **Campaign** — grouping of missions (NEXT; schema present, UI absent).
- **DomainEvent** — outbox row.

---

## 6. State machines

**P0 review note:** [Detailed transition drafts](state-machines/README.md) expand organization review, volunteer approval and mission lifecycle. The [decision register](state-machines/review-decisions.md) records unresolved source conflicts, including mission readiness/pause and proof rejection. Those drafts are not accepted amendments; do not implement an ambiguous edge below without resolving its linked decision.

### 6.1 Mission

```
DRAFT → PENDING_REVIEW → PUBLISHED → (FUNDING | RECRUITING | ACTIVE) → READY → IN_PROGRESS → DELIVERED → VERIFICATION → COMPLETED
                ↓ REJECTED                ↓ PAUSED ↔                    ↓ FAILED / CANCELLED / EXPIRED / DISPUTED
```

| From | To | Trigger | Guard |
|---|---|---|---|
| DRAFT | PENDING_REVIEW | org submits | required fields, ≥1 need, org VERIFIED |
| PENDING_REVIEW | PUBLISHED / REJECTED | ops decision | audit reason |
| PUBLISHED | FUNDING / RECRUITING / ACTIVE | auto on publish by need types | — |
| FUNDING/RECRUITING | READY | all needs met or org marks ready | partial allowed if `allow_partial` |
| READY | IN_PROGRESS | first shipment picked up / first assignment checked in / org starts | — |
| IN_PROGRESS | DELIVERED | all shipments delivered and assignments checked out, or org marks delivered | — |
| DELIVERED | VERIFICATION | proof submitted | ≥ required proof items |
| VERIFICATION | COMPLETED / DISPUTED | ops verifies / rejects | — |
| any active | PAUSED | org or ops | reason |
| PAUSED | previous | resume | — |
| PUBLISHED…IN_PROGRESS | CANCELLED | org or ops | refunds initiated for captured money |
| FUNDING/RECRUITING | EXPIRED | scheduler at deadline | if not READY; partial handling per `allow_partial` |
| IN_PROGRESS | FAILED | ops | reason; refund/reallocation policy |

Illegal transitions return `409 MISSION_STATE_CONFLICT`. Every transition writes `mission_status_history` and emits `Mission<State>` event.

### 6.2 Contribution

**P0 contract review:** [Per-type contribution draft](state-machines/contributions.md) separates execution from refunds/payouts and pending Activity from final records. The linear money status sequence below cannot represent every partial-refund or delivery-before-payout case; CD-02 must be resolved before implementation. SKILL/REGISTERED remains subject to G08's separate interest model.

```
MONEY:  INITIATED → PENDING_PAYMENT → CONFIRMED → ALLOCATED → FULFILLED → VERIFIED → COMPLETED
                                 ↓ PAYMENT_FAILED / EXPIRED (30 min)        ↓ REFUND_PENDING → REFUNDED
ITEM:   INITIATED → CONFIRMED → SCHEDULED → IN_TRANSIT → DELIVERED → VERIFIED → COMPLETED   | CANCELLED
TIME:   INITIATED → CONFIRMED → UPCOMING → CHECKED_IN → CHECKED_OUT → VERIFIED → COMPLETED   | CANCELLED / NO_SHOW
SKILL:  INITIATED → REGISTERED (MVP terminal)
```

### 6.3 Payment

**P0 contract review:** [Payment/refund/payout commands](state-machines/payments-and-payouts.md) preserve capture facts separately from settlement/refund state and include uncertain order recovery. See [money invariants](state-machines/money-invariants.md) for the proposed replacement of status-based liability calculations in §10; FD decisions and database/provider proof remain open.

```
CREATED → AUTHORIZED → CAPTURED → SETTLED
       ↓ FAILED        ↓ REFUND_INITIATED → REFUNDED / REFUND_FAILED
       ↓ EXPIRED
```
Transitions driven **only** by verified provider webhooks or server-side status fetch during reconciliation. Client "success" callback triggers a status fetch, never a state write.

### 6.4 Shipment (tracking)

**P0 review:** [Shipment/attendance draft](state-machines/logistics-and-attendance.md) proposes orthogonal delay/reschedule/issue/reminder metadata and explicit custody/booking-offer records. The side-state and REMINDED edges below are not safe to implement without LD-01–LD-04 reconciliation.

```
CREATED → VOLUNTEER_ASSIGNED → PICKUP_READY → PICKED_UP → IN_TRANSIT → ARRIVED → DELIVERED → VERIFIED
   ↓ UNASSIGNED (reassign)    ↓ DELAYED / RESCHEDULED / ISSUE_REPORTED (side states with return)    ↓ CANCELLED
```
Each transition: actor (volunteer/org/ops/system), timestamp, optional location, optional note → `shipment_events`; emits `Shipment<State>`; pushes WS event `tracking.updated`.

### 6.5 Assignment (volunteer)

```
REQUESTED → CONFIRMED → REMINDED → CHECKED_IN → CHECKED_OUT → HOURS_VERIFIED
         ↓ WAITLISTED → CONFIRMED          ↓ NO_SHOW          ↓ HOURS_DISPUTED
         ↓ CANCELLED_BY_VOLUNTEER / CANCELLED_BY_ORG
```

### 6.6 Verification (org, mission, proof)

**P0 review:** [Proof/impact draft](state-machines/proof-and-impact.md) distinguishes media processing, immutable submission reviews, final record issuance and append-only corrections. Organization credential expiry is not automatic expiry of historical proof.

```
NOT_REVIEWED → UNDER_REVIEW → VERIFIED | NEEDS_MORE_INFORMATION → UNDER_REVIEW | REJECTED
VERIFIED → EXPIRED (org docs expiry, annual)
```

---

## 7. Event model

### 7.1 Mechanism

**P0 blocker G13:** [Event/recovery proposal](state-machines/events-and-recovery.md) adds an aggregate dispatch cursor, transactional handler receipts, poison-event blocking and durable external-effect intents. SKIP LOCKED over event rows alone does not establish the ordering claimed below. The proposal also resolves the incomplete retry schedule; ADR acceptance and database crash/concurrency proof remain pending.
Transactional outbox: `domain_events(id, type, aggregate_type, aggregate_id, payload jsonb, occurred_at, published_at, attempts)`. Relay worker polls (`FOR UPDATE SKIP LOCKED`, batch 100, 250 ms), dispatches to registered handlers in order per aggregate, publishes to Redis channel `events.<type>`, marks published. Handler failures retry with backoff (1 s, 5 s, 30 s, 5 min, 1 h; max 8) then move to `domain_events_dlq` with error; ops console shows DLQ and allows replay. Handlers are idempotent (keyed on event id in `event_handler_receipts`).

### 7.2 Catalogue (MVP)

The table below is historical shorthand. In particular, PaymentCaptured must not issue a pending immutable impact record; pending Activity is a projection. The [producer/consumer map](state-machines/events-and-recovery.md) and linked transition names form the expanded review draft. Exact event schemas and name reconciliation are still required before generated contracts.

| Event | Producer | Payload (key fields) | Consumers |
|---|---|---|---|
| `MissionSubmitted` | missions | mission_id, org_id | admin (queue), notifications (ops) |
| `MissionPublished` | missions | mission_id, category, geo | search (index), analytics |
| `MissionStatusChanged` | missions | mission_id, from, to, reason | notifications (contributors), impact, analytics |
| `ContributionCreated` | contributions | contribution_id, mission_id, user_id, type, amount/qty | payments (create order), dispatch (item), volunteers (time), analytics |
| `PaymentCaptured` | payments | payment_id, contribution_id, amount, provider_ref | contributions (→CONFIRMED), missions (raised_amount), notifications, impact (pending record) |
| `PaymentFailed` / `PaymentRefunded` | payments | … | contributions, notifications, missions |
| `ShipmentCreated` / `VolunteerAssigned` / `PickupCompleted` / `DeliveryStarted` / `DeliveryCompleted` | dispatch/tracking | shipment_id, contribution_id, state, actor, at, geo? | tracking (WS), notifications, contributions, missions |
| `AssignmentConfirmed` / `CheckedIn` / `CheckedOut` | volunteers | assignment_id, user_id, mission_id, at | notifications, missions, impact |
| `ProofUploaded` | proof | proof_id, subject_type, subject_id, media_ids | verification (queue), media (processing) |
| `VerificationDecided` | verification | subject, decision, reviewer_id, reason | missions, organizations, impact, notifications |
| `MissionCompleted` | missions | mission_id | impact (finalize records), notifications, analytics |
| `ImpactRecordCreated` / `ImpactRecordCorrected` | impact | record_id, contribution_id, summary | notifications, analytics |

Ordering: guaranteed per aggregate id (relay processes one aggregate's events sequentially). Cross-aggregate ordering not guaranteed; consumers read current state, never assume.

---

## 8. API design

### 8.1 Conventions
- Base `https://api.neki.xyz/v1`; JSON; snake_case; ISO-8601 UTC; money as integer paise with `currency: "INR"`.
- Auth: `Authorization: Bearer <jwt>`. Public read endpoints (mission detail, org page) allow anonymous.
- Pagination: `?cursor=&limit=` (default 20, max 50) → `{items, next_cursor, has_more}`. Cursors opaque (base64 of sort key + id).
- Idempotency: `Idempotency-Key: <uuid>` required on `POST` for contributions, volunteer requests, proofs, check-in/out, mission completion. Server stores key → response for 24 h; same key + same body → replay response; same key + different body → `422 IDEMPOTENCY_MISMATCH`.
- Errors: `{ "error": { "code": "MISSION_UNAVAILABLE", "message": "…", "request_id": "req_…", "details": {…} } }`. HTTP: 400 validation, 401, 403, 404, 409 state conflict, 422 semantic, 429, 5xx.
- Rate limits (Redis token bucket): anonymous 60/min/IP; authenticated 300/min/user; OTP request 3/10 min/phone, 10/h/IP; webhook allowlisted provider IPs.
- Versioning: path `/v1`; additive changes only; breaking → `/v2`.
- OpenAPI generated by FastAPI is the contract; Flutter client generated in CI from it.

### 8.2 Endpoint inventory (MVP)

**Auth / me**
`POST /auth/otp/request` · `POST /auth/otp/verify` · `POST /auth/refresh` · `POST /auth/logout` · `GET /me` · `PATCH /me` · `DELETE /me` · `GET/PUT /me/notification-preferences` · `GET /me/addresses` · `POST /me/addresses` · `DELETE /me/addresses/{id}` · `GET /me/bookmarks` · `GET /me/payment-methods` · `POST /me/devices` (FCM token)

**Discovery**
`GET /home` · `GET /categories` · `GET /missions` (filters: `category, subcategory, contribution_type, urgency, status, verified_only, lat, lng, radius_km, min_amount, max_amount, sort`) · `GET /missions/{id}` · `GET /missions/{id}/updates` · `GET /missions/{id}/proofs` · `POST|DELETE /missions/{id}/bookmark` · `GET /organizations/{id}` · `GET /organizations/{id}/missions` · `GET /search?q=` · `GET /search/suggest?q=` · `GET /geo/search` · `GET /geo/reverse`

**Contribute**
`POST /missions/{id}/contributions` (body: `type`, `amount_paise?`, `item{need_id, quantity, condition, media_ids}`, `pickup{address_id, slot_id}?`, `anonymous`, `message?`) → 201 `{contribution, payment_intent?}` · `GET /contributions` · `GET /contributions/{id}` · `POST /contributions/{id}/cancel` · `GET /pickup-slots` · `GET /contributions/{id}/tracking`

**Payments**
`POST /payments/{id}/verify` (client post-checkout signal → server fetches status) · `POST /payments/webhook` (provider) · `GET /payments/{id}/receipt`

**Volunteer**
`POST /missions/{id}/volunteer` (role_id, slot_id) · `DELETE /assignments/{id}` · `GET /assignments` · `POST /assignments/{id}/checkin` · `POST /assignments/{id}/checkout` · `POST /shipments/{id}/transition` (volunteer-executed pickups: state, lat, lng, note) · `POST /shipments/{id}/pings` (batched)

**Proof / impact**
`POST /media/upload-url` → `{upload_url, media_id, headers}` · `POST /media/{id}/complete` · `POST /proofs` · `GET /impact/summary` · `GET /impact/records` · `GET /impact/records/{id}` · `GET /certificates` · `GET /certificates/{id}`

**Notifications**
`GET /notifications` · `POST /notifications/read`

**Realtime**
`WSS /ws?token=&channels=contribution:{id},mission:{id}` → server events `tracking.updated`, `contribution.updated`, `mission.updated`, `notification.new`; client `ping`; server `pong`, `resync_required`.

**Organization portal (`/org/*`, role org_admin)**
`POST /org/apply` · `GET /org/me` · `PATCH /org/me` · `POST /org/documents` · `GET /org/dashboard` · `GET|POST /org/missions` · `GET|PATCH /org/missions/{id}` · `POST /org/missions/{id}/submit` · `POST /org/missions/{id}/transition` · `GET /org/missions/{id}/contributions` · `GET /org/missions/{id}/assignments` · `POST /org/assignments/{id}/confirm-attendance` · `POST /org/missions/{id}/updates` · `POST /org/proofs` · `GET /org/impact`

**Ops console (`/admin/*`, ops roles)**
`GET /admin/queues/organizations` · `POST /admin/organizations/{id}/decision` · `GET /admin/queues/missions` · `POST /admin/missions/{id}/decision` · `GET /admin/queues/proofs` · `POST /admin/proofs/{id}/decision` · `GET /admin/dispatch` · `POST /admin/shipments/{id}/assign` · `POST /admin/shipments/{id}/transition` · `GET /admin/disputes` · `POST /admin/payments/{id}/refund` · `GET /admin/users` · `POST /admin/users/{id}/suspend` · `GET /admin/fraud/signals` · `GET /admin/health` · `GET /admin/events/dlq` · `POST /admin/events/{id}/replay` · `GET /admin/audit`

---

## 9. Realtime

- One WS connection per app session, multiplexed channels. Auth via short-lived token in query (WS headers unreliable on some clients); server validates and subscribes to Redis channels `ws.contribution.{id}` etc. based on authorization (user must own contribution or be assigned volunteer/org/ops).
- Server pushes `{type, version, data, sent_at}`. Client tracks `version` per channel; gap → request `GET` snapshot.
- Heartbeat: client ping 25 s; server closes idle at 60 s.
- Reconnect: exponential backoff 1 → 30 s with jitter; UI states Connecting / Live / Reconnecting / Last updated.
- Fallback: if WS fails 3 times, poll `GET /contributions/{id}/tracking` every 15 s while screen visible; stop when backgrounded.
- Volunteer location pings: batched every 10 s while shipment `PICKED_UP`/`IN_TRANSIT` and app foregrounded (background location not requested in MVP; ETA gaps acceptable). Server stores in Redis (`shipment:{id}:loc`, TTL 5 min) and appends downsampled (1/min) rows to `location_pings`. Contributor stream receives position rounded to 3 decimals (~100 m) and ETA from Directions API cached 60 s.

---

## 10. Payments (Razorpay)

Flow:
1. `POST /missions/{id}/contributions` → server validates mission accepts money, computes fee split from mission/org policy, creates `contribution(PENDING_PAYMENT)` + `payment(CREATED)` + Razorpay Order (amount server-side, `receipt=contribution.public_id`, notes with ids). Returns `order_id`, `key_id`, amount.
2. App opens Razorpay Checkout with order id. On success callback app calls `POST /payments/{id}/verify` with `razorpay_payment_id`, `razorpay_signature` → server verifies HMAC and fetches payment from Razorpay; if captured → state `CAPTURED` (idempotent).
3. Webhook `payment.captured` / `payment.failed` / `refund.processed` → signature verified (`X-Razorpay-Signature`), event id deduped (`payment_webhook_events`), state transitions applied. Webhook is authoritative; verify endpoint is an accelerator.
4. Reconciliation worker every 5 min: payments `CREATED`/`AUTHORIZED` older than 10 min → fetch status → transition or `EXPIRED` (release contribution; mission raised_amount unaffected because only CAPTURED counts).
5. Refunds: ops-initiated or automatic on mission cancellation; refund request to Razorpay; state via webhook.
6. Settlement to organizations (**D3 locked**): funds settle to NEKI's Razorpay account; Finance records **manual payouts** in the ops console → `payouts` (`DRAFT → APPROVED → PAID → RECONCILED`) with `payout_items` linking each payout to the confirmed contributions it settles. `SettlementStrategy` interface has one implementation in MVP (`ManualPayoutStrategy`); `RazorpayRouteStrategy` is NEXT. Reconciliation report: Σ CAPTURED − REFUNDED per org − Σ PAID payouts = outstanding liability. Legal structure sign-off (CA/CS) required before live funds — risk R8.
7. Fee policy (**D2 locked**): default `fee_policy = {platform_fee_bps: 0, gateway_fee_borne_by: "platform"}`; contribution stores `fee_gateway_paise` (provider-reported, absorbed) and `amount_to_mission_paise = amount_paise`. Disclosure block rendered from these fields, never hard-coded copy.

Invariants: `mission.raised_amount = SUM(payments CAPTURED − REFUNDED)` recomputed nightly and on each event; client never sends amounts to be trusted; duplicate order creation blocked by idempotency key; 30-minute expiry on unpaid contributions; Σ `payout_items.amount_paise` per payout = `payouts.amount_paise`; a contribution appears in at most one PAID payout.

---

## 11. Media and proof pipeline

```
App → POST /media/upload-url (mime, bytes, purpose: mission_image|proof|item_photo|avatar|org_document)
    → server creates media(PENDING), returns presigned PUT (R2, 15 min, size-limited)
App → PUT bytes → POST /media/{id}/complete
Worker: fetch → validate magic bytes → virus scan (ClamAV container) → strip EXIF (retain capture time + GPS into proof metadata columns for proof purpose only, never in file) → resize variants (thumb 200, card 800, full 1600, WebP) → BlurHash → CDN URLs → media(READY) | media(REJECTED)
```

- Access: mission images public via CDN; proof media served through signed URLs (1 h) to contributors of that mission, org, ops; org documents ops-only; item photos org/volunteer/ops.
- Proof integrity: perceptual hash stored; duplicates across missions flagged to fraud signals; proof renders with watermark overlay in app (not baked) "Proof · NK-XXXXXX · <date>". AI-generated marketing assets tagged `is_illustration=true` and never allowed as proof purpose.
- Retention: proof 7 years (audit); item photos 180 d after completion; avatars until account deletion; deleted accounts → media purged in 30 d.
- Limits: image ≤ 10 MB, video ≤ 100 MB / 60 s (proof only), 5 photos per item contribution.

---

## 12. Location and maps

- Permissions: contributors when-in-use only; volunteers when-in-use during active shipment/assignment. No background location in MVP (trade-off: ETA freezes when volunteer backgrounds app; mitigated by "Last updated" label and push nudge).
- Storage: user home location as city + rounded point (2 decimals); addresses full precision, owner-scoped; volunteer pings downsampled, 30-day retention; proof capture GPS as metadata, ops-visible only.
- Geofencing: check-in allowed within 300 m of mission location (server-checked); outside → organizer manual confirm required.
- Spoofing signals: impossible speed (> 120 km/h between pings), mock-location flag (Android `isFromMockProvider`), pings inconsistent with check-in geofence → flag to fraud queue; never auto-punish.
- Maps provider: Google Maps Platform (Maps SDK, Geocoding, Directions) proxied through backend for geocode/directions with caching (Redis 24 h geocode, 60 s directions).
- Map UX fallbacks: tiles fail → static timeline; no permission → manual location.

---

## 13. Search and feed ranking

- Storage: PostgreSQL `tsvector` (`title`, `description`, `category`, `org name`, `tags`) with `pg_trgm` for typo tolerance; PostGIS `geography` for distance. No Elasticsearch until > ~50k active missions or latency > 200 ms p95.
- Query parsing: extract "near me" / city tokens → geo filter; category synonyms table (`books → Education/School Supplies`).
- Deterministic ranking score (weights in config):

```
score = 0.30·text_relevance + 0.20·proximity(1/(1+km/5)) + 0.15·urgency(deadline ≤ 48h:1, ≤7d:0.6, else 0.2)
      + 0.10·freshness(published ≤ 3d) + 0.10·availability(remaining/target) + 0.10·org_reliability(completion rate, proof rate)
      + 0.05·user_affinity(categories interacted)
```
Hard rules: no monetary input to score; completed missions excluded from default results but reachable via status filter.
- Home modules are queries with fixed intents (nearby: distance sort within 10 km; urgent: deadline ≤ 72 h; picks: ops-curated `featured_missions`; recently completed: `completed_at` desc with proof).

---

## 14. Notifications

- FCM via `firebase_messaging`; device tokens per user/device in `devices`. Categories with user toggles. Templates in `notification_templates` keyed by event; worker renders with deep link (`https://neki.xyz/c/{public_id}` → `neki://contribution/{id}`).
- Quiet hours 22:00–08:00 local for non-critical categories. Dedup: one push per (user, contribution, state).
- In-app center: `notifications` table, `read_at`.

---

## 15. Offline and sync (server side)

- `GET` endpoints support `If-None-Match`/ETag and `updated_after` deltas for history collections.
- Outbox writes carry `Idempotency-Key`; server returns `409` with current resource on state conflict so client can reconcile.
- Volunteer field actions accepted with `client_timestamp` ≤ 24 h old; server timestamps authoritative; both stored.

---

## 16. Security threat model and controls

| Threat | Controls |
|---|---|
| Account takeover (OTP) | Rate limits per phone/IP/device, 6-digit OTP 5-min TTL, lockout, refresh rotation with reuse detection, device binding, re-auth for payment method changes and account deletion |
| Payment manipulation | Server-side amounts, provider signature verification, webhook dedupe, reconciliation, no client-driven state |
| Fake organizations | Document review, registration cross-check (Darpan/12A/80G where applicable), ops checklist, probation (first 3 missions reviewed with stricter proof) |
| Fake missions | Mandatory review before publish, quantified needs, deadline, proof requirements, org reliability score |
| Fake proof | EXIF capture time/GPS checks, perceptual-hash duplicate detection, geofence, human review, AI-illustration tag blocking |
| Location spoofing | Speed/mock checks, geofence + organizer confirm, ops flags |
| API abuse | Rate limiting, pagination caps, query cost limits, WAF at edge |
| Media abuse | Type/size validation, virus scan, presigned scoped uploads, moderation queue for public images |
| Privilege escalation / IDOR | Policy layer on every endpoint, principal-scoped queries, opaque public ids, authorization tests per endpoint |
| Replay | Idempotency keys, webhook event ids, JWT `jti` + short TTL |
| Webhook forgery | HMAC verification, provider IP allowlist, secret rotation |
| Secrets | Cloud secret manager, no secrets in repo/app, mobile has only publishable keys |
| Data in transit/at rest | TLS 1.2+, HSTS, certificate pinning for API in app, DB encryption at rest, encrypted backups |
| Audit | `audit_log` for all admin/org mutations and auth events; immutable append |

Additional: dependency scanning (pip-audit, `dart pub outdated` + OSV), SAST in CI, external pentest before public launch.

---

## 17. Privacy and data retention

| Data | Purpose | Retention | Notes |
|---|---|---|---|
| Phone, name | Account | Life of account + 30 d | Hash phone for analytics |
| Home location (city, rounded) | Discovery | Until changed | |
| Addresses | Pickups | Until deleted by user | Shared with assigned volunteer during window only |
| Volunteer location pings | Tracking | 30 d | Rounded to contributors |
| Payment data | Receipts | 7 y (finance) | Only provider ids + amounts; no card data |
| Proof media + metadata | Trust | 7 y | Beneficiary faces: org must confirm consent; blur tool in portal |
| Beneficiary counts | Impact | Permanent (aggregate) | No beneficiary names/PII stored in MVP |
| Analytics | Product | 13 months | Pseudonymous |
| Audit logs | Security | 3 y | |

Consent captured at signup (ToS/Privacy), at location permission, at proof upload (org attests consent). Account deletion: soft-delete → 30 d grace → hard purge with impact records anonymized (contributor becomes "Anonymous contributor"), never deleted (ledger immutability).

---

## 18. Observability

- Logs: structured JSON, `request_id` propagated to app (`X-Request-Id`), PII scrubbed.
- Traces: OpenTelemetry auto-instrumentation FastAPI/SQLAlchemy/httpx/redis → Grafana Tempo.
- Metrics: RED per endpoint; business gauges (contributions/min, payment failure rate, webhook lag, outbox lag, DLQ depth, WS connections, dispatch queue age).
- Alerts: webhook lag > 60 s, DLQ > 0 for 10 min, payment failure rate > 10% / 15 min, p95 latency > 800 ms, error rate > 1%, DB connections > 80%.
- Mobile: Sentry crashes + performance (cold start, screen TTI), custom spans for feed and checkout; frame-drop metric sampled.
- Dashboards: platform health (ops console embeds key numbers), funnel (PostHog).

---

## 19. Testing strategy

| Layer | Backend | Mobile |
|---|---|---|
| Unit | Services, state machines, ranking, fee calc (pytest) | Domain, use cases, controllers (Riverpod `ProviderContainer`), formatters |
| Integration | Router + DB via testcontainers Postgres/Redis; webhook fixtures; outbox relay | Repositories with fake API + Drift in-memory |
| Contract | Schemathesis against OpenAPI; generated client compile check | Generated client from same spec; golden JSON fixtures |
| Widget | — | All screens × states (loading/empty/error/data/offline); golden tests for design system components light/dark |
| E2E | — | Patrol/integration_test on real devices: signup, browse, search, mission, contribute (Razorpay test mode), payment failure, volunteer accept, check-in, proof upload, view impact |
| Performance | Locust: home feed 500 rps, checkout 50 rps, WS 5k connections | DevTools profiling budgets in CI on Pixel 6a / iPhone 12 |
| Offline | Toxiproxy scenarios | Airplane-mode E2E: queued check-in syncs, no duplicate contributions |
| Security | Authz matrix tests per endpoint (every role × every route), webhook forgery, IDOR fuzz | Token storage, pinning, no secrets in bundle |

Coverage gates: backend 85% lines on `modules/*`, mobile 80% on `domain` + `presentation` controllers. Critical journeys must have E2E before release.

---

## 20. Performance budgets

| Item | Budget |
|---|---|
| API p95 (read) | ≤ 250 ms |
| API p95 (contribution create) | ≤ 600 ms incl. provider order |
| Home feed query | ≤ 80 ms DB |
| WS event delivery | ≤ 3 s p95 |
| App cold start (mid Android) | ≤ 1.5 s first frame, ≤ 2.5 s interactive |
| Home warm TTI | ≤ 800 ms p75 |
| Frame budget | 16 ms; jank < 1% |
| App size | ≤ 35 MB Android download |
| Images | WebP variants, ≤ 120 KB card image |

---

## 21. DevOps, environments, CI/CD

- Environments: `dev` (docker compose local), `staging`, `prod`. IaC via Terraform.
- Hosting (MVP): containers on a managed platform (Fly.io or AWS ECS Fargate — ADR-018), managed Postgres (Neon/RDS) with PITR, managed Redis, Cloudflare in front (WAF, CDN, R2). Web portals on Vercel (matches prior repo history) or Cloudflare Pages.
- CI (GitHub Actions): lint/format (ruff, dart format/analyze), unit + integration tests, OpenAPI export → client codegen → diff check, container build + scan, Flutter build (Android AAB, iOS via macOS runner), golden tests, size check.
- CD: staging on merge to `main`; prod on tag with manual approval; DB migrations as pre-deploy job (Alembic, expand/contract).
- Mobile release: Fastlane; internal track / TestFlight weekly; phased rollout 10% → 50% → 100%; remote-config kill-switches for payments and tracking.
- Backups: daily full + PITR 7 d; restore drill monthly.

---

## 22. Architecture Decision Records (summary)

| ADR | Decision | Key alternatives rejected |
|---|---|---|
| 001 | Flutter for mobile + web portals | React Native (weaker web reuse of design system), native ×2 (cost) |
| 002 | Riverpod 2 code-gen | BLoC (boilerplate), GetX (untestable globals) |
| 003 | go_router typed routes | auto_route (heavier codegen), Navigator 1 (no deep links) |
| 004 | FastAPI modular monolith with outbox | Microservices (premature), Django (sync-first) |
| 005 | PostgreSQL 16 | MongoDB (relational needs, transactions) |
| 006 | PostGIS geography + GiST | Haversine in app (no index) |
| 007 | Redis for cache, rate limit, pub/sub, ephemeral location | Memcached (no pub/sub) |
| 008 | WebSockets for tracking with polling fallback | SSE (no client→server), FCM-only (latency) |
| 009 | Cloudflare R2 + CDN, presigned uploads | Direct-to-API uploads (bandwidth) |
| 010 | Razorpay; manual payouts (D3); Route deferred to NEXT | Stripe India (UPI coverage), Cashfree (second choice) |
| 011 | Google Maps Platform via backend proxy | Mapbox (weaker India POI), OSM tiles (ETA quality) |
| 012 | Phone OTP via MSG91 + server-issued JWT | Firebase Auth (lock-in, cost), email/password (friction) |
| 013 | Drift (SQLite) + outbox table for offline | Hive/Isar (no relational queries) |
| 014 | Transactional outbox + in-process handlers + Redis pub/sub | Kafka (ops burden), direct calls (no durability) |
| 015 | Postgres FTS + pg_trgm + PostGIS | Elasticsearch/Meilisearch (premature) |
| 016 | PostHog for product analytics behind interface | Firebase Analytics (weak funnels), Mixpanel (cost) |
| 017 | Sentry + OpenTelemetry + Grafana Cloud | Datadog (cost) |
| 018 | Containers on Fly.io/ECS, Terraform, GitHub Actions | Kubernetes (premature) |

Full ADRs to be written in `docs/adr/ADR-0xx.md` using Context / Decision / Alternatives / Pros / Cons / Risks / Consequences / Migration path.

---

## 23. Open technical questions

1. ~~Razorpay Route vs manual payouts~~ — resolved by D3: manual payouts in MVP (`07-founder-decisions.md`). Remaining: legal sign-off on money-flow structure before live funds.
2. Background location for volunteers in NEXT — battery and policy review.
3. ClamAV self-host vs managed scanning cost at launch volumes.
4. Ops console as Flutter Web vs lightweight admin framework; default Flutter Web for design-system reuse, revisit if velocity suffers.
5. Certificate PDF generation (server-side WeasyPrint) — NEXT unless volunteers demand at launch.
