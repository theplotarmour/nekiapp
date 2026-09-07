# NEKI — Product Requirements Document (PRD)

| Field | Value |
|---|---|
| Product | NEKI — Humanity, Delivered. |
| Version | 1.0 (MVP definition) |
| Date | 2026-09-07 |
| Status | Draft for review |
| Sources | `NEKI_Master_RND_Architecture_Documentation_Prompt.md`, `NEKI_Complete_UI_UX_Design_Specification.md`, mobile UI board (`c0f5b185-…png`) |
| Companion docs | `02-tdd.md`, `03-user-flows.md`, `04-design-brief.md`, `05-data-model.md`, `06-eng-plan.md` |

---

## 1. Summary

NEKI is a mobile-first marketplace and coordination layer for social impact. Organizations publish **missions** — concrete, quantified needs (200 meals, 500 books, 12 volunteers). Individuals contribute **money, items, time, or skills**. NEKI coordinates execution, tracks fulfilment in real time, collects proof, verifies outcomes, and writes every contribution into a permanent **Impact Ledger**.

Brand promise: **Track every contribution. Verify every mission. See every impact.**

The MVP is a consumer iOS/Android app (Flutter) plus a minimal web portal for organizations and an internal ops console, backed by a FastAPI modular monolith on PostgreSQL/PostGIS.

---

## 2. Problem

| Who | Pain today |
|---|---|
| Contributor | Gives money or goods into a black box. No visibility into delivery or outcome. Low trust, low repeat. |
| Volunteer | Opportunities are scattered, poorly specified, and effort is never recorded or verified. |
| Organization | Publishes vague appeals instead of specific needs; struggles to coordinate pickups, volunteers, and proof. |
| Corporate (later) | Cannot produce auditable CSR/impact reporting from fragmented giving. |

The market has donation apps. It does not have a **need → contribution → execution → proof → verified impact** loop that works like a modern quick-commerce experience.

---

## 3. Vision, thesis, positioning

- **Thesis:** Model the world as *missions with quantified needs*, not NGO profiles with donate buttons.
- **Positioning:** Blinkit-level speed, density, and operational clarity — for doing good. Original NEKI design, terminology, and assets. No cloning of proprietary products.
- **Evolution path:** mission marketplace → coordination layer → trust layer → operating platform for organizational and corporate impact.

### Core product loop (all features must reinforce this)

```
NEED → MISSION → DISCOVERY → CONTRIBUTION / VOLUNTEERING → ASSIGNMENT → EXECUTION → TRACKING → PROOF → VERIFICATION → IMPACT → TRUST → REPEAT
```

---

## 4. Goals, success metrics, non-goals

### 4.1 MVP goals
1. A contributor can discover a mission, contribute money in under 60 seconds, and follow it to verified impact.
2. A contributor can donate items with a scheduled pickup and track the delivery.
3. A volunteer can accept a mission slot, execute it, upload proof, and receive verified hours.
4. An organization can publish a mission, receive contributions, and submit proof through a web portal.
5. Ops can verify organizations, moderate missions, review proof, and resolve failures without touching the database.

### 4.2 Success metrics (first 90 days post-launch, single launch city)

| Metric | Target | Notes |
|---|---|---|
| Mission view → contribution start | ≥ 12% | Funnel event `mission_viewed` → `contribution_started` |
| Contribution start → payment success | ≥ 65% | Checkout completion |
| Median time mission-open → payment success | ≤ 90 s | Speed of checkout |
| Missions with delivery proof uploaded | ≥ 90% of delivered | Trust loop health |
| Proof → verified within 72 h | ≥ 80% | Ops throughput |
| Repeat contribution within 30 days | ≥ 25% | Retention |
| Volunteer no-show rate | ≤ 15% | Ops quality |
| Crash-free sessions | ≥ 99.5% | Stability |
| Home feed p75 time-to-interactive (warm) | ≤ 800 ms | Perf |

### 4.3 Non-goals (MVP)
- Corporate CSR dashboard, employee volunteering programs, corporate surplus intake.
- Skills matching marketplace (UI tab exists; flow ships as "register interest" only).
- Recurring/subscription contributions.
- Wallet / stored-value balance (the `₹1,250` chip in the reference is **not** in MVP — see §12).
- Blockchain, ML ranking, microservices, Kubernetes, Kafka, Elasticsearch.
- Public leaderboards or money-based gamification.
- Acting as a statutory CSR implementing agency.

---

## 5. Users and personas

### 5.1 Contributor — "Divo" (primary MVP persona)
28, urban India, gives ₹500–₹5,000 a few times a year, distrusts opaque charities, uses Blinkit/Zepto/UPI daily. Wants: fast discovery, exact need, proof of delivery, a personal record.

### 5.2 Volunteer — "Ravi"
Student or young professional. Wants nearby, well-specified, time-boxed missions; clear navigation; simple status updates; verified hours and certificates.

### 5.3 Organization admin — "Meera" (ABC Foundation)
Runs programs, not software. Wants to post exact needs, see contributions arrive, coordinate pickups/volunteers, upload proof from a phone, and get a clean impact record.

### 5.4 Ops / Admin — "NEKI Ops"
Internal. Verifies organizations, moderates missions, reviews proof, resolves failed deliveries and disputes, triggers refunds, watches fraud signals.

### 5.5 Corporate — LATER
CSR manager. Budgets, programs, employee volunteering, surplus, reports. Documented in roadmap; no MVP UI.

---

## 6. Scope ladder

| Tier | Meaning | Contents |
|---|---|---|
| **NOW (Phase 0)** | Documentation | This doc set; ADRs; R&D review; backlog |
| **MVP** | Launch, one city | Consumer app: auth, home, explore, search, category, mission detail, money contribution + payment, item contribution + pickup, volunteer signup, tracking, activity/impact ledger, profile, bookmarks, share, notifications. Org web portal: profile, mission CRUD, contribution list, volunteer roster, proof upload. Ops console: org verification, mission moderation, proof review, disputes/refunds, dispatch overrides. |
| **NEXT** | 3–6 months post-launch | Campaigns (Neki Drives), Give Anything (reverse matching), skills contribution flow, certificates PDF, recurring contributions, organization mobile app, richer volunteer field app, multi-city |
| **LATER** | 6–18 months | Corporate platform (CSR programs, budgets, employee volunteering, surplus), multi-user org roles, public organization pages/SEO, i18n Hindi |
| **EXPERIMENTAL** | Unvalidated | ML ranking, impact scoring, wallet/credits, enterprise "OS for social impact" |

---

## 7. Information architecture (consumer app)

Bottom navigation (fixed by reference): **Home · Explore · Contribute · Activity · Profile**

- **Home** — location, notifications, search, category grid, Today's Highlight, Nearby, Urgent, Continue Your Impact (active contribution), Recently Completed.
- **Explore** — search, filters, category chips, mission list.
- **Contribute** — entry to contribution type chooser (Money / Items / Time / Skills); if opened without a mission, shows "pick a mission" discovery.
- **Activity** — page title "Your Impact": segmented All/Donations/Volunteering/Items, four stats, chronological feed, each row opens an Impact Record.
- **Profile** — avatar, name, stats, My Contributions, My Bookmarks, My Certificates, Payment Methods, Settings, Help & Support.

Secondary: Mission Detail, Contribution flow, Payment, Success, Tracking, Category page, Organization page, Impact Record, Notifications, Search.

---

## 8. Functional requirements

Each feature follows the same template. Analytics events are listed by name; payload schema is in `05-data-model.md §11`. Backend endpoints reference `02-tdd.md §8`.

### FR-01 Onboarding and authentication

- **Purpose:** Get a new user to Home in under 60 seconds with minimal data.
- **User:** Contributor, Volunteer (same account; roles are capabilities, not separate accounts).
- **Preconditions:** App installed; network available.
- **Primary flow:** Splash (≤1.5 s) → Welcome ("A kinder world is a more possible one." / Get Started / Sign In) → Phone number → OTP → Name → Location permission rationale → OS prompt → Notification rationale → OS prompt → Home.
- **Alternative flows:** Sign In (existing phone) skips Name. Email+password deferred to NEXT. "Skip" allowed on both permissions; manual location selection offered.
- **Error states:** Invalid phone; OTP wrong (max 5 attempts, then 15 min lockout); OTP expired (resend after 30 s, max 3 per 10 min); network failure with retry.
- **Loading states:** Button enters loading immediately on tap; OTP auto-read on Android (SMS Retriever) where available.
- **Empty states:** N/A.
- **Offline:** Auth requires connectivity; show "You're offline" with retry. Returning users with a valid refresh token open Home from cache.
- **Permissions:** Location (when-in-use), Notifications. Never requested before rationale screen.
- **Analytics:** `app_opened`, `onboarding_started`, `otp_requested`, `otp_verified`, `otp_failed`, `permission_location_result`, `permission_notification_result`, `onboarding_completed`.
- **Backend:** `POST /v1/auth/otp/request`, `POST /v1/auth/otp/verify`, `POST /v1/auth/refresh`, `GET /v1/me`, `PATCH /v1/me`.
- **Security:** OTP rate-limited per phone and per device; tokens in secure storage (Keychain/Keystore); refresh token rotation; device binding.
- **Acceptance criteria:**
  - New user reaches Home in ≤ 6 taps excluding keyboard input.
  - OTP lockout enforced server-side.
  - Skipping location still shows Home with "Select location" prompt.
- **Tests:** Unit (phone validation, token store), widget (OTP screen states), integration (OTP flow, lockout), E2E (signup → home).

### FR-02 Location selection

- **Purpose:** Drive nearby discovery, pickup addresses, and volunteer matching.
- **User:** All app users.
- **Preconditions:** Signed in.
- **Primary flow:** Home header shows current area name. Tap → bottom sheet: Use current location / Search city or area / Saved addresses. Select → feed refreshes.
- **Alternative flows:** Permission denied → manual search only. Precise vs approximate location both accepted; approximate flagged for pickup flows (pickup requires a full address).
- **Error states:** Geocoding failure; no results.
- **Loading:** Skeleton on feed while refetching.
- **Empty:** "No missions found nearby. Try expanding your location." CTA Explore All.
- **Offline:** Last selected location persists; nearby feed served from cache.
- **Permissions:** Location when-in-use only. No background location for contributors.
- **Analytics:** `location_selected` (method: gps|search|saved; city; no raw coordinates).
- **Backend:** `GET /v1/geo/search?q=`, `GET /v1/geo/reverse?lat&lng` (server-side proxy to maps provider).
- **Security:** Store only city/area + rounded coordinates for discovery; full address only on addresses table with owner scoping.
- **Acceptance:** Manual selection always available; feed radius default 10 km, expandable to 25/50 km.

### FR-03 Home

- **Purpose:** Dense, calm, one-scroll discovery. Prioritize active contribution over generic discovery.
- **User:** Contributor.
- **Preconditions:** Signed in; location known or defaulted to launch city.
- **Primary flow:** Header (menu/avatar, location, bell) → greeting (time-of-day, first name) → search field → 6-tile category grid (Food, Education, Healthcare, Money, Mentoring, Animals; "See All") → Today's Highlight (featured mission) → modules ordered by personalization: Continue Your Impact (if active contribution), Urgent Nearby, Nearby Missions, NEKI Picks, Volunteer This Weekend, Recently Completed, Organizations Near You.
- **Alternative flows:** New user ordering: Categories → Featured → Nearby → Urgent. Pull-to-refresh.
- **Error:** Module-level errors (one failing module does not blank the page). Full-page error only if shell fails and no cache.
- **Loading:** Cached shell renders immediately; skeletons for modules.
- **Empty:** Per-module hidden if empty; never show empty module boxes.
- **Offline:** Render last feed snapshot with offline banner.
- **Analytics:** `screen_view(home)`, `home_module_impression(module)`, `mission_impression(mission_id, module, position)`, `mission_viewed`, `category_selected`.
- **Backend:** `GET /v1/home?lat&lng` returns ordered modules with cursors; `GET /v1/missions?…` per module for "See All".
- **Security:** No PII in module payloads beyond own profile.
- **Acceptance:** First viewport contains header, greeting, search, categories, featured card at 390×844; p75 TTI ≤ 800 ms warm; scroll ≥ 55 fps on mid-range Android.

### FR-04 Explore, search, filters

- **Purpose:** Marketplace browsing.
- **Primary flow:** Explore tab → search field + filter button + category chips (All, Food, Education, Healthcare, …) → paginated mission cards (image, category badge, title, location, progress %, bookmark).
- **Search:** Suggestions (recent, trending causes, categories, organizations); results grouped Missions / Organizations / Categories; debounce 300 ms; "books near me" resolves category + geo.
- **Filters (bottom sheet):** Cause, Location (near me / city / radius), Contribution type (Money/Items/Time/Skills), Urgency (Urgent / This week / Flexible), Status (Funding / Volunteers needed / Active / Almost complete), Organization (Verified / Community-led), Amount range. Apply / Reset. Active filter count on button.
- **Error/Loading/Empty:** Retry; skeleton cards; "No missions match these filters" with Reset.
- **Offline:** Last result page cached; search disabled with message.
- **Analytics:** `search_started`, `search_completed(query_len, results_count)`, `filter_applied(filters)`, `mission_viewed`.
- **Backend:** `GET /v1/missions` (cursor pagination, filters), `GET /v1/search?q=`, `GET /v1/search/suggest?q=`.
- **Acceptance:** Cursor pagination, 20 per page; ranking per `02-tdd.md §13`; payment amount never a ranking input.

### FR-05 Category page

- **Purpose:** Reusable, data-driven category browsing.
- **Primary flow:** Tap category → header (icon, title, one-line editorial description e.g. "Nourishment for a brighter tomorrow."), subcategory chips (Food: All, Meals, Rations, Kitchen Kits), mission list.
- **Rules:** One `CategoryPage(category)` widget; categories, descriptions, subcategories from API.
- **Backend:** `GET /v1/categories`, `GET /v1/missions?category=&subcategory=`.
- **Analytics:** `category_viewed`, `subcategory_selected`.
- **Acceptance:** Adding a category requires zero app changes.

### FR-06 Mission detail

- **Purpose:** Highest-value screen. Answer: what, why, who, what's needed, progress, how to help, how tracked, how verified.
- **Primary flow:** Hero image with back / bookmark / share overlays → category badge → title → location, date/time → progress (₹12,400 of ₹20,000 · 62%) → stat tiles (Volunteers, Units, Distance) → Why this matters → Requirements cards (Money / Units / Volunteers / Deadline) → Organization card (logo, name, verification status, missions completed, View Organization) → Trust section (only verified claims: Organization verified, Mission documents reviewed, Delivery proof required, Impact verification pending) → Updates/proof (post-delivery) → sticky footer.
- **Sticky footer:** `[Volunteer] [Contribute Now]`; when no volunteer slots: `[Save] [Contribute Now]`. Dynamic by state: Fully funded → "Mission Fully Funded" + Explore Similar; Closed/expired → "Mission Closed"; Completed → "View Impact".
- **Error:** "We couldn't load this mission." Retry. 404 → "This mission is no longer available."
- **Loading:** Hero placeholder + skeleton.
- **Offline:** Cached detail if previously viewed; CTAs disabled with message.
- **Analytics:** `mission_viewed(source)`, `mission_saved`, `mission_shared`, `organization_viewed`, `trust_badge_tapped`, `contribution_started`.
- **Backend:** `GET /v1/missions/{id}`, `GET /v1/missions/{id}/updates`, `POST/DELETE /v1/missions/{id}/bookmark`.
- **Security:** Never expose beneficiary PII or private org documents. Public payload excludes internal notes.
- **Acceptance:** Hero collapses into compact header on scroll; trust badges each open an explanation sheet; all CTAs ≥ 48 px tall.

### FR-07 Money contribution and payment

- **Purpose:** Fastest possible path from intent to confirmed contribution.
- **Preconditions:** Mission status accepts money; user signed in.
- **Primary flow:** Contribute → type tabs (Money selected) → quick amounts ₹500 / ₹1,000 / ₹2,500 / ₹5,000 → Other amount → fee disclosure line → Proceed to Pay (disabled until valid) → Review (mission, type, amount, fee breakdown, payment method) → Confirm → payment provider sheet (UPI, cards, net banking, wallets) → Success screen → Track.
- **Alternative:** Saved payment method; anonymous display toggle (contribution still tied to account); add message to organization (optional, moderated).
- **Fee disclosure (D2):** NEKI absorbs the gateway fee for launch organizations. Every transaction renders an allocation block — Contribute screen (one line), Review (full block), receipt, Impact Record:
  ```
  You contribute        ₹1,000
  Mission allocation    ₹1,000
  Gateway fee           Covered by NEKI
  ```
  When `missions.fee_policy` differs: `Contribution ₹1,000 · Gateway fee ₹X · Platform fee ₹Y · Mission allocation ₹Z`. The phrase "100% reaches the NGO" is never used unless literally true for that transaction. Never hide charges.
- **Error states:**
  - Payment failed → "Your payment could not be confirmed. No contribution has been recorded yet." Try Again / Contact Support.
  - Timeout / webhook delay → "We're confirming your contribution." Poll; never show failure prematurely; never show success without server confirmation.
  - Mission became fully funded during checkout → offer redirect to similar missions; if payment already captured, hold and offer reallocation or refund per policy.
  - Duplicate tap → idempotency key prevents double contribution.
- **Loading:** Button loading state; full-screen "Confirming" state.
- **Offline:** Blocked; explain connectivity required.
- **Analytics:** `contribution_started`, `contribution_type_selected`, `amount_selected(preset|custom)`, `contribution_reviewed`, `payment_started(method)`, `payment_completed`, `payment_failed(code)`, `payment_pending`.
- **Backend:** `POST /v1/missions/{id}/contributions` (Idempotency-Key) → creates contribution `PENDING_PAYMENT` and provider order; `POST /v1/payments/webhook`; `GET /v1/contributions/{id}`.
- **Security:** Server creates provider order with server-side amount; client never sets captured amount; webhook signature verified; amounts reconciled; PCI scope avoided by using provider SDK/tokenization.
- **Acceptance:** Median mission-open → success ≤ 90 s; zero duplicate contributions under double-tap test; delayed-webhook test shows "Confirming" then success.
- **Tests:** Unit (amount validation, fee calc), integration (order create, webhook, reconcile), E2E happy/failure/timeout, security (webhook forgery, IDOR on contribution id).

### FR-08 Item contribution (pickup)

- **Purpose:** Let users give goods with logistics handled.
- **Preconditions:** Mission accepts items of that type; user in serviceable area.
- **Primary flow:** Items tab → select item type (from mission needs) → quantity → condition (New / Good / Fair) → photos (1–5) → pickup address (saved / new with map pin) → pickup window (date + 2-hour slot) → Review → Confirm → Success → Tracking (Created → Volunteer assigned → Pickup ready → Picked up → In transit → Arrived → Delivered → Verified).
- **Alternative:** Drop-off at organization instead of pickup (if org allows). Reschedule pickup before assignment.
- **Error:** Address outside service area; photo upload failure (retry queue); slot unavailable.
- **Empty:** Mission has no item needs → tab hidden.
- **Offline:** Draft persisted locally; submission requires connectivity.
- **Permissions:** Camera/photos.
- **Analytics:** `contribution_started(items)`, `item_type_selected`, `item_photos_added(count)`, `pickup_slot_selected`, `contribution_completed(items)`.
- **Backend:** `POST /v1/missions/{id}/contributions` type=ITEM; `POST /v1/media/upload-url`; `GET /v1/pickup-slots?address_id&mission_id`.
- **Security:** Photos stripped of EXIF GPS before storage; address visible only to assigned volunteer during active window.
- **Acceptance:** Item contribution creates a shipment record and enters dispatch queue; ops can reassign; contributor sees tracking timeline.

### FR-09 Volunteer (time) contribution

- **Purpose:** Fill mission volunteer slots; record verified hours.
- **Preconditions (D7):** User has an approved volunteer application. First tap on any Volunteer CTA without one opens the application (availability, home area, skills, consent to SOP) → status `PENDING_REVIEW` → ops approves/rejects in console → push "You're approved to volunteer". Unapproved users can browse volunteer missions but cannot book slots; pickup shipments are only assignable to approved volunteers.
- **Primary flow:** Mission → Volunteer → role → date → time slot → location & requirements (duration, physical, age) → Confirm → Activity shows upcoming → reminders (24 h, 2 h) → check-in (geofenced QR or organizer confirm) → mission execution → check-out → hours recorded → verification by org → certificate.
- **Alternative:** Waitlist when slots full; cancel up to 12 h before (configurable); no-show recorded. Higher-risk missions flagged `requires_enhanced_check` → ops manual SOP before assignment.
- **Error:** Slot full during confirm; requirements unmet (age).
- **Offline:** Check-in/out and status updates queue locally and sync (see `02-tdd.md §15`).
- **Permissions:** Location during active mission (when-in-use); camera for proof.
- **Analytics:** `volunteer_started`, `volunteer_slot_selected`, `volunteer_confirmed`, `volunteer_checked_in`, `volunteer_checked_out`, `volunteer_cancelled`.
- **Backend:** `POST /v1/missions/{id}/volunteer`, `DELETE …/volunteer`, `POST /v1/assignments/{id}/checkin`, `POST /v1/assignments/{id}/checkout`.
- **Acceptance:** Hours = checkout − checkin, capped at slot length; organizer must verify before hours count toward Impact stats.

### FR-10 Tracking

- **Purpose:** Reassurance: "I know what's happening."
- **Preconditions:** Contribution with a physical or scheduled execution component.
- **Primary flow:** Map (upper half: origin, route, mover marker, destination, ETA bubble "8 min away") → headline ("Your contribution is on the way") → mission + location → timeline (Order confirmed 10:14 AM ✓, Picked up 10:28 AM ✓, On the way · Live, Delivered ○, Verified ○) → mover card (first name, avatar, message, ETA) → actions (Contact support, Report issue, View route; Call volunteer only when volunteer consented).
- **Money-only contributions:** No map; timeline: Payment confirmed → Received by organization → Resources procured/deployed (org update) → Delivery proof → Verified.
- **States:** Confirmed, Preparing, Assigned, Picked Up, On the Way, Arrived, Delivered, Verification, Verified, Completed; exceptional: Delayed, Rescheduled, Issue Reported, Verification Required, Cancelled. Every state has explanatory copy.
- **Realtime:** WebSocket; states Connecting / Live / Reconnecting / Last updated HH:MM; fallback polling every 15 s.
- **Error:** Map unavailable → timeline-only layout.
- **Offline:** Last known state with timestamp: "Connection interrupted. Showing latest update from 10:42 AM."
- **Analytics:** `tracking_opened`, `tracking_status_viewed(state)`, `tracking_issue_reported`.
- **Backend:** `GET /v1/contributions/{id}/tracking`, `WS /v1/ws?channels=contribution:{id}`.
- **Security:** Volunteer location shared only during active leg, rounded to ~50 m for contributors, full precision for ops; retention 30 days.
- **Acceptance:** State change appears on contributor device within 3 s p95 when connected.

### FR-11 Activity / Your Impact / Impact Ledger

- **Purpose:** Pride and proof; the contributor's permanent record.
- **Primary flow:** Activity tab ("Your Impact") → segmented All / Donations / Volunteering / Items → stats (Missions Supported, People Helped, Hours Volunteered, NGOs Supported) → Recent Activity feed → tap → Impact Record (NEKI ID `NK-XXXXXX`, contribution, mission, organization, location, delivered date, proof gallery, impact summary, verification status).
- **Rules:** Stats count only platform-recorded, verified values. "People Helped" shown only when organization-reported beneficiary count is verified; otherwise the tile shows "—" with explanation. Never fabricate.
- **Verification states (exact language):** Not Reviewed, Under Review, Verified, Needs More Information, Rejected, Expired.
- **Error/Loading/Empty:** Retry; skeleton; new user empty: "Your impact story starts with your first mission." CTA Explore.
- **Offline:** Full history cached.
- **Analytics:** `impact_viewed`, `impact_record_opened`, `impact_shared`, `certificate_opened`.
- **Backend:** `GET /v1/impact/summary`, `GET /v1/impact/records`, `GET /v1/impact/records/{id}`.
- **Acceptance:** Every completed contribution has exactly one immutable impact record; corrections produce correction events visible in record history.

### FR-12 Profile and settings

- **Primary flow:** Avatar, name, impact statement, four stats → My Contributions, My Bookmarks, My Certificates, Payment Methods, Settings (profile, privacy: profile visibility, contribution visibility, impact sharing, location, notifications; language; delete account), Help & Support, About NEKI.
- **Backend:** `GET/PATCH /v1/me`, `GET /v1/me/bookmarks`, `GET /v1/me/payment-methods`, `DELETE /v1/me` (30-day grace).
- **Acceptance:** Privacy defaults conservative (profile private, contributions private, impact sharing off).

### FR-13 Bookmarks and share

- Bookmark toggle with fill animation, toast "Saved to your missions" + Undo. Share via native sheet with deep link `https://neki.xyz/m/{public_id}` (universal/app link) and preview card (title, need, location, progress, "Humanity, Delivered."). Never include private contribution data in shares.
- **Analytics:** `mission_saved`, `mission_unsaved`, `mission_shared(channel)`.

### FR-14 Notifications

- Categories: Contribution (picked up), Tracking (8 minutes away), Verification (verified), Impact (₹1,000 supported 200 meals), Volunteer (starts tomorrow 10 AM), Account/security.
- Every notification deep-links. User can toggle categories. No engagement-bait notifications.
- In-app notification center (bell) lists last 30 days.
- **Backend:** FCM; `GET /v1/notifications`, `POST /v1/notifications/read`; `PUT /v1/me/notification-preferences`.

### FR-15 Organization web portal (MVP-minimal)

- **Users:** Organization admin (single user per org in MVP).
- **Flows:** Apply (org details, registration number, documents upload) → status Pending Review → Verified; Dashboard (active missions, contributions today, pending proof); Missions (create/edit: title, category, subcategory, description/why it matters, location, needs: money target / item type+quantity / volunteer slots+schedule, deadline, images, proof requirements) → Submit for review → Published; Contributions list; Volunteer roster + attendance confirm; Proof upload per mission/delivery (photos, acknowledgement doc, beneficiary count) → Submit for verification; Impact view; Profile & settings.
- **Acceptance:** Org cannot publish without ops approval of both org and mission; org cannot edit quantified targets after contributions exist without ops approval.

### FR-16 Ops / Admin console (mandatory for launch)

- **Platform (D6):** Flutter Web. Operational efficiency over visual polish.
- **Modules:** Dashboard; Missions (moderation queue, manual status change with reason, record pickup/delivery, upload proof on behalf of org, approve impact); Organizations (verification queue: documents, checklist, approve / needs info / reject, audit trail); Contributors (search, contribution history, suspend); Volunteers (application review queue per D7, approve/reject, enhanced-check flag, assignment history); Contributions (list, detail, cancel); **Payouts (D3):** create payout for an organization from confirmed money contributions → select linked contributions → record amount, date, bank/UTR reference, recipient, operator, notes → status `DRAFT → APPROVED → PAID → RECONCILED` (Finance role approves; two-person rule for > ₹50,000); Tracking/dispatch board (unassigned pickups, assign/reassign approved volunteer, delay/reschedule); Proof review queue (side-by-side proof vs requirements, auto-checks, approve / needs info / reject); Verification (org/mission/proof/hours decisions); Disputes and refunds (Razorpay refund trigger, reason codes); Fraud signals; Reports (contributions, payouts, fulfilment, verification SLAs; CSV export); Platform health (queue depths, webhook lag, DLQ).
- **Rules:** All actions audited (who, what, when, why). RBAC: Ops Agent, Ops Lead, Finance, Super Admin. No production DB edits for normal operations. Manual does not mean informal: every manual intervention carries a reason and appears in the aggregate's history.

### FR-17 Proof and verification

- **Proof types:** delivery photo(s), receipt/acknowledgement document, beneficiary count, geotag (from device at capture, then stripped from public copies), volunteer check-in/out, organization attestation.
- **Rules:** Marketing imagery and proof are visually and technically distinct (proof carries capture metadata, watermark "Proof · NK-XXXXXX", never AI-generated). Unreviewed content is never rendered as verified. Verification checklist automated where possible (timestamp within window, geotag within mission radius, image hash uniqueness) plus human review.
- **Backend:** `POST /v1/proofs`, `GET /v1/missions/{id}/proofs`, admin review endpoints.

---

## 9. Non-functional requirements

| Area | Requirement |
|---|---|
| Performance | Cold start to first frame ≤ 1.5 s (mid-range Android); Home warm TTI ≤ 800 ms p75; scroll jank < 1% frames; image progressive load; map first render ≤ 1.2 s |
| Availability | API 99.9% monthly; payment webhook processing lag p95 ≤ 5 s |
| Realtime | Tracking event to device ≤ 3 s p95; reconnect with exponential backoff (1, 2, 4, 8, 16 s cap 30 s); fallback polling 15 s |
| Offline | Cached home, mission details viewed, history, tracking last state; queued volunteer field actions with retry and conflict handling |
| Accessibility | WCAG AA contrast; 44×44 min touch targets (48 preferred); full semantics; Dynamic Type up to 200% without truncating CTAs; reduced-motion honored; status never color-only |
| Security | See `02-tdd.md §16`: RBAC, server-side authz, signed uploads, webhook verification, rate limits, audit logs, secure token storage, TLS 1.2+, secrets in manager |
| Privacy | Data minimization; precise location never stored beyond operational need (30 d); beneficiary PII never public; account deletion within 30 days; consent records |
| i18n | English MVP; all strings externalized; INR formatting; Hindi in LATER |
| Platform | iOS 15+, Android 8+ (API 26); Android predictive back, edge-to-edge; iOS swipe back, sheets, haptics |
| Compliance | Payment provider handles PCI; 80G receipt generation only when org eligible (flag on org) |

---

## 10. Analytics event taxonomy (consumer)

Lifecycle: `app_opened`, `screen_view`, `onboarding_completed`, `location_selected`
Discovery: `home_module_impression`, `mission_impression`, `mission_viewed`, `category_viewed`, `search_started`, `search_completed`, `filter_applied`, `organization_viewed`
Engagement: `mission_saved`, `mission_unsaved`, `mission_shared`, `trust_badge_tapped`
Contribution: `contribution_started`, `contribution_type_selected`, `amount_selected`, `item_type_selected`, `pickup_slot_selected`, `contribution_reviewed`, `payment_started`, `payment_completed`, `payment_failed`, `payment_pending`, `contribution_completed`, `contribution_cancelled`
Volunteer: `volunteer_started`, `volunteer_slot_selected`, `volunteer_confirmed`, `volunteer_checked_in`, `volunteer_checked_out`, `volunteer_cancelled`
Tracking: `tracking_opened`, `tracking_status_viewed`, `tracking_issue_reported`
Impact: `impact_viewed`, `impact_record_opened`, `impact_shared`, `certificate_opened`
Proof: `proof_uploaded`, `proof_upload_failed`
Notifications: `notification_received`, `notification_opened`

Rules: no payment credentials, no raw coordinates (city/area only), no beneficiary data, user id pseudonymized.

---

## 11. Business metrics

- **Marketplace:** mission views, contribution conversion, volunteer conversion, fulfilment rate, time-to-fulfilment, mission liquidity (open needs vs contributions/week).
- **Trust:** proof completion rate, verification completion time, dispute rate, refund rate.
- **Retention:** 30/90-day repeat contribution, repeat volunteer, repeat mission creation per org.
- **B2B:** organizations onboarded, active orgs (≥1 published mission / 30 d), campaigns (NEXT), corporate accounts (LATER).

---

## 12. Assumptions and open questions

Founder decisions D1–D7 locked 2026-09-07 — see `07-founder-decisions.md`.

| # | Item | Resolution | Status |
|---|---|---|---|
| Q1 | `₹1,250` header chip in reference | **D1:** No wallet anywhere in MVP (header, profile, nav, contribution). Header shows location pill. | Locked |
| Q2 | "100% goes to the mission" | **D2:** NEKI absorbs gateway fee for launch organizations. Every transaction shows actual allocation block (contribution / gateway fee / mission allocation). "100%" phrasing never used unless literally true. | Locked |
| Q3 | Launch city | **D4:** Delhi NCR only. | Locked |
| Q4 | Logistics for item pickup | Volunteer-executed pickups in MVP (volunteers ops-approved per D7); partner courier API in NEXT. | Assumed |
| Q5 | Payment provider | **D5:** Razorpay behind NEKI payment service; only approved-config methods shown. | Locked |
| Q6 | Tax receipts (80G) | Generated by organization, surfaced by NEKI if org flagged eligible. NEKI is not the donee. Subject to legal sign-off with D3. | Pending legal |
| Q7 | Legal entity / money flow | **D3:** Manual payouts to organizations, every payout recorded in `payouts` + `payout_items`. Razorpay Route deferred to NEXT. Legal structure must be signed off by CA/CS/legal before live funds. | Locked (legal sign-off pending) |
| Q8 | Skills tab | Visible; flow ships as "Register your skill" interest capture only. | Assumed |
| Q9 | Beneficiary counts | Org-reported, ops-verified; displayed with "reported by organization" label until verified. | Assumed |
| Q10 | Volunteer identity | **D7:** Phone OTP + basic profile + volunteer application → ops review → approved. No KYC in MVP; identity verification Phase 4+. | Locked |

---

## 13. Risks

Full register with probability/impact/mitigation in `06-eng-plan.md §9`. Top five: low mission liquidity at launch; fake or low-quality organizations; payment/webhook reconciliation bugs; volunteer no-shows breaking pickups; beneficiary privacy exposure through proof photos.
