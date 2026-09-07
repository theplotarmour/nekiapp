# NEKI — Design Brief

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 2026-09-07 |
| Primary reference | UI board `c0f5b185-e8b2-44fa-a0fe-626ee5f561a8.png` (10 screens + brand panel) |
| Source spec | `NEKI_Complete_UI_UX_Design_Specification.md` |
| Audience | Product designer, Flutter engineers, brand/illustration |

---

## 1. Brand foundation

- **Name:** NEKI (wordmark set in a high-contrast italic serif; "Neki" with capital N in the reference).
- **Mark:** Butterfly formed from a stylized human figure with leaf-like wings, warm taupe/bronze (`#A58F78` family). Represents transformation, movement, kindness, connection.
- **Signature:** *Humanity, Delivered.* — letter-spaced small caps under the wordmark.
- **Board headline:** "A Kinder World in Your Hands" (serif, italic emphasis on *Kinder* and *Your*).
- **Board sub-copy:** "Discover. Contribute. Track. Make a real impact." and "The future of helping is visible."
- **Handles seen on board:** `neki.xyz`, `@nekiforindia` (use for share cards/about).
- **Personality:** warm, minimal, elegant, trustworthy, optimistic, soft, modern, human, precise, visible.
- **Emotional arc:** Before — "I can help." During — "I know what's happening." After — "I can see the impact."

### What the app must feel like
A premium consumer product built around doing good: modern commerce density, editorial typography, trustworthy infrastructure. Not an NGO website, donation form, or CSR dashboard.

---

## 2. Reference board teardown

What the board establishes (keep):

| Element | Observation | Decision |
|---|---|---|
| Background | Warm off-white with large blurred pastel spheres (mint, peach, sage) behind phones | Ambient objects on splash/welcome/success only; never behind dense content |
| Primary color | Deep forest green on CTAs, active nav, progress, check states | `#0B5D45` primary |
| Cards | White, 16–20 px radius, near-invisible shadow, generous padding | Level-1 surface spec §5 |
| Category tiles | 6 pastel tiles with soft 3D icons (bowl, book, heart, coins, people, paw) | Category palette §4.3; 3D icon set commissioned |
| Typography | Serif for wordmark/headline/"Thank You!"; clean sans for UI | Instrument Serif + Inter |
| Mission card | Image left (list) or top (featured), category badge, title 2 lines, location pin, thin green progress bar + "% funded" | `NekiMissionCard` variants |
| Mission detail | Full-bleed hero with circular glass controls; white sheet with rounded top; 3 stat tiles; stacked CTAs | Screen brief §7.6 |
| Contribute | Pill segmented Money/Items/Time/Skills; 4 amount chips (selected = green fill); Other amount input; transparency note; dark CTA; glass card with plant illustration | §7.7 |
| Tracking | Map upper half with dotted route, truck marker, green "8 min away" pill; timeline with green checks and "Live" label; volunteer card with avatar | §7.10 |
| Your Impact | Segmented filter; 2×2 stat tiles; Recent Activity list with pastel icon circles | §7.11 |
| Profile | Centered avatar with edit badge; 4 inline stats; list rows with icons + chevrons | §7.13 |
| Thank You | Large glass circle with green check, scattered confetti dots (restrained), serif "Thank You!", dark CTA Share Impact, light CTA Back to Home | §7.9 |
| Bottom nav | 5 items, active = green filled icon + green label | `NekiBottomNav` |

What the board shows that we **change**:

| Element | Issue | Decision |
|---|---|---|
| `₹1,250` header chip | Implies wallet; not in MVP scope | Replace with location pill ("📍 South Delhi ▾"). Wallet deferred (PRD Q1) |
| Hamburger menu top-left on Home | Redundant with bottom nav | Replace with avatar/location; keep bell |
| "100% of your contribution goes to the mission." | Legal/fee accuracy | Dynamic fee line; exact copy only when true |
| Children's faces in mission imagery | Consent + exploitation risk | Photography guidelines §6; org consent attestation; prefer context shots |
| Confetti on Thank You | Risk of gimmick | Max 12 particles, slow drift, 700 ms, none under reduced motion |
| "48 People Helped" | Must be verified data | Show "—" with explainer until verified |

---

## 3. Design principles

1. **Dense but calm.** One-scroll discovery like a commerce app; whitespace does the work, not borders.
2. **Green means action or trust.** Never decorative. One primary CTA per screen.
3. **Serif for feeling, sans for function.** Serif on ≤ 1 element per screen.
4. **Evidence over emotion.** Numbers, progress, proof, timestamps. No guilt copy, no fake urgency.
5. **Every state designed.** Loading, empty, error, offline, success, disabled — before visuals are "done".
6. **Native where it matters.** iOS sheets/swipe-back; Android predictive back/edge-to-edge. Brand is visual; interaction is platform.
7. **Accessible by default.** WCAG AA, 44 px targets, status never color-only, Dynamic Type safe.

---

## 4. Design tokens

### 4.1 Color — light theme (default)

| Token | Hex | Use |
|---|---|---|
| `color.primary` | `#0B5D45` | Primary buttons, active nav, progress fill, verified, links |
| `color.primaryPressed` | `#073D30` | Pressed, deep text on green |
| `color.primarySoft` | `#E7F4ED` | Selected surfaces, success backgrounds, Food tile |
| `color.background` | `#FAF9F6` | App background (warm off-white) |
| `color.surface` | `#FFFFFF` | Cards, sheets |
| `color.surfaceTint` | `#F3F1EC` | Inputs, unselected chips, secondary buttons |
| `color.beige` | `#E8DDCF` | Editorial accents |
| `color.taupe` | `#A58F78` | Brand mark, decorative serif accents, warm metadata |
| `color.textPrimary` | `#171A18` | |
| `color.textSecondary` | `#66706B` | |
| `color.textTertiary` | `#929A95` | Placeholders, timestamps |
| `color.divider` | `#E8EBE8` | Hairlines |
| `color.success` | `#21865B` | Timeline checks, "Live" |
| `color.warning` | `#C28A35` | Delayed, needs info |
| `color.error` | `#C95151` | Failures, destructive |
| `color.info` | `#4D7EA8` | Neutral info |
| `color.overlay` | `rgba(23,26,24,0.40)` | Scrims |
| `color.glass` | `rgba(255,255,255,0.72)` + blur 20 | Floating controls, success card |

### 4.2 Color — dark theme

| Token | Hex |
|---|---|
| `background` | `#121614` (warm charcoal-green) |
| `surface` | `#1B211E` |
| `surfaceTint` | `#232A26` |
| `primary` | `#3FA37C` (brighter green, AA on dark) |
| `primarySoft` | `#173328` |
| `textPrimary` | `#F3F1EC` (warm white) |
| `textSecondary` | `#A9B3AD` |
| `textTertiary` | `#7C867F` |
| `divider` | `#2A322D` |

Never pure black/white. Category pastels desaturate to 18% opacity tints on dark.

### 4.3 Category palette (orientation, not decoration)

| Category | Tile bg (light) | Icon accent | Badge text |
|---|---|---|---|
| Food | `#E7F4ED` mint | `#0B5D45` | FOOD |
| Education | `#FBF1DC` cream | `#B98A2E` | EDUCATION |
| Healthcare | `#FBE6E6` rose | `#C95151` | HEALTHCARE |
| Money | `#E4EDF7` soft blue | `#4D7EA8` | MONEY |
| Mentoring | `#ECE7F7` lavender | `#6E5BB7` | MENTORING |
| Animals | `#E6F2E4` sage | `#3D8A4A` | ANIMALS |
| Environment | `#E3F1E6` natural green | `#2E7D5B` | ENVIRONMENT |
| Disaster Relief | `#F3EBE3` warm gray | `#B8683A` | RELIEF |

Category badges: 10–11 px, 600 weight, letter-spacing 0.6, pill, tile bg + accent text.

### 4.4 Typography

| Role | Family | Size / line | Weight | Use |
|---|---|---|---|---|
| Display XL | Instrument Serif (italic allowed) | 48 / 52 | 400 | Board-style statements — marketing only |
| Display L | Instrument Serif | 40 / 44 | 400 | Welcome headline |
| Display M | Instrument Serif | 32 / 38 | 400 | "Thank You!", impact storytelling |
| Heading XL | Inter | 28 / 34 | 600 | Screen titles when large (Explore, Your Impact) |
| Heading L | Inter | 24 / 30 | 600 | Mission title on detail |
| Heading M | Inter | 20 / 26 | 600 | Section titles, greeting name |
| Heading S | Inter | 17 / 22 | 600 | Card titles, sheet titles |
| Body L | Inter | 17 / 24 | 400 | Long copy |
| Body M | Inter | 15 / 22 | 400/500 | Default UI text |
| Body S | Inter | 13 / 18 | 400/500 | Metadata, list secondary |
| Caption | Inter | 12 / 16 | 500 | Timestamps, labels |
| Micro | Inter | 11 / 14 | 600 | Badges, nav labels |
| Numerals | Inter tabular (`tnum`) | inherit | 600–700 | Amounts, stats |

Rules: one serif element per screen max; no uppercase beyond badges; INR formatting `₹12,400` with Indian grouping; numerals tabular in stats and progress.

Fallbacks: Instrument Serif → Georgia; Inter → SF Pro / Roboto. Bundle fonts; no runtime download.

### 4.5 Spacing, radius, elevation, motion

Spacing scale: `4 8 12 16 20 24 32 40 48 64`. Screen horizontal padding 20 (16 below 360 px). Card internal padding 16. Section gap 24–32.

Radius: `xs 8 · sm 12 · md 16 · lg 20 · xl 24 · xxl 28 · pill 999`. Controls 12–16; cards 16–20; sheets/hero 24–28; chips pill.

Elevation:
- Level 0 background; Level 1 card `0 4 18 rgba(20,40,30,0.06)`; Level 2 floating/glass `0 8 28 rgba(20,40,30,0.10)` + blur 20. No borders on cards except 1 px `divider` on inputs.

Motion tokens: `instant 100 · quick 160 · normal 220 · smooth 320 · hero 500–700`. Enter: ease-out; exit: ease-in; springs (stiffness 400, damping 30) for buttons, cards, bookmark, success check. Reduced motion → fades ≤ 150 ms, no translation.

Haptics: light on chip select and bookmark; medium on payment success and tracking milestone; none elsewhere.

---

## 5. Component library (`core/design_system`)

| Component | Variants | States required |
|---|---|---|
| `NekiButton` | primary (green), secondary (surfaceTint, dark text), tertiary (text), destructive; sizes 48/56; optional trailing arrow | default, pressed (scale 0.98 + primaryPressed), disabled (40% opacity), loading (spinner replaces label, width fixed), success (check morph) |
| `NekiChip` | filter, category, amount, segmented item | selected (green fill, white text), unselected (surfaceTint), disabled, with count |
| `NekiSegmentedControl` | 2–4 items, pill track | selected slides with spring |
| `NekiSearchField` | leading magnifier, trailing clear/filter | idle, focused (1 px primary ring), filled, disabled |
| `NekiAmountField` | ₹ prefix, tabular numerals, inline validation | error below field |
| `NekiMissionCard` | compact (list, 88 px image left), standard (Explore), featured (hero image top), horizontal (module carousel), near-complete, volunteer | loading skeleton, pressed, bookmarked, closed/funded overlay |
| `NekiCategoryCard` | tile (icon + label) | pressed |
| `NekiProgressBar` | money, units | animates fill on first appearance (320 ms) |
| `NekiStatusBadge` | category, LIVE, URGENT, VERIFIED, COMPLETED | text + icon, never color-only |
| `NekiVerificationBadge` | org verified, mission verified, delivery proof, impact verified | tappable → explanation sheet |
| `NekiStatTile` | number + label | skeleton, "—" with tooltip |
| `NekiTimeline` | steps with done/current/future | current pulses (reduced-motion: static ring) |
| `NekiTrackingMap` | route, mover, ETA chip | loading, unavailable fallback |
| `NekiBottomNav` | 5 items, badge | active/inactive |
| `NekiTopBar` | large title / compact; glass overlay variant for hero | |
| `NekiBottomSheet` | drag handle, title, scroll, sticky CTA | |
| `NekiEmptyState` | illustration (butterfly optional), title, body, CTA | |
| `NekiErrorState` | title, body, Retry, request id | |
| `NekiSkeleton` | card, list row, stat | subtle shimmer 1.2 s |
| `NekiToast` | info, success, with Undo | |
| `NekiAvatar` | 32/48/80, edit badge | |
| `NekiSectionHeader` | title + "See All" | |
| `NekiProofCard` | thumbnail grid, watermark overlay, verification state | |
| `NekiImpactRecordCard` | NK id, summary, state | |

Golden tests light + dark for every component at 1.0× and 1.6× text scale.

---

## 6. Iconography, illustration, photography

- **Icons:** Lucide set, 1.75 px stroke, 24 px grid; filled variants for active nav. No mixed families.
- **3D category icons:** commissioned set (bowl, book, heart, coins, mentor pair, paw, tree, first-aid, water drop, school bag, care package, butterfly). Soft, rounded, matte, single warm light from top-left, no photoreal, no glossy. PNG @1/2/3× on transparent, 96 px base. Spec sheet per asset: id, purpose, ratio, subject, composition, background, lighting, brand constraints, negatives, usage.
- **Ambient spheres:** 3 blurred blobs (mint `#CFE8DA`, peach `#F2D9C7`, sage `#DCE7D6`) at 30–40% opacity, blur 40–60, 8–16 px float over 6–10 s with randomized phase. Only on Splash, Welcome, Thank You, empty states.
- **Butterfly motion:** Rive asset, wing flutter + slow drift; Splash, Welcome, Success, empty states only.
- **Photography:** documentary, warm natural light, context over faces, dignity-first. No staged suffering; no children's faces without documented consent; prefer hands, food, kits, classrooms, activity. Card crops 4:3 (list) and 16:10 (featured); subject center-safe area; overlay gradient only when text sits on image.
- **Proof imagery** is never stylized; rendered with "Proof · NK-XXXXXX · date" overlay and capture metadata; AI illustration forbidden as proof.

---

## 7. Screen briefs (P0)

Each brief: purpose · hierarchy · components · notes from board · states.

### 7.1 Splash
Hope. Background + ambient spheres fade (200 ms), butterfly Rive (600 ms), wordmark rises (220 ms), signature (160 ms). Total ≤ 1.5 s; skip if session valid and cache warm (show 400 ms brand frame only).

### 7.2 Welcome
Possibility. Large butterfly + wordmark centered top third; Display L serif "A kinder world is a more possible one."; primary pill button "Get Started →" (56 px); tertiary "Already have an account? **Sign In**". Ambient spheres allowed.

### 7.3 Auth (Phone → OTP → Name)
Minimal white screens, Heading L title, one input, primary CTA docked above keyboard. OTP 6 boxes 48×56, auto-advance, resend timer. Error text below field in `error`.

### 7.4 Home
Discovery. Board layout retained with header change:
- Row 1: avatar (32) · location pill ("📍 South Delhi ▾") · bell (badge only when actionable).
- Greeting: Heading M "Hi, Divo" + "Good Morning 👋"; Body S secondary "Small acts. Big change."
- Search field (48 px, radius 16).
- Category grid 3×2 tiles (aspect 1:0.9, radius 20, icon 40, label Body S 500).
- Section header "Today's Highlight · See All"; featured card (image 16:10, FOOD badge, bookmark glass button, title Heading S, location + "62% funded", progress bar).
- Modules: Continue Your Impact (when active; pinned first, green-tinted card with timeline glyph + "Track now →"), Urgent Nearby (horizontal cards), Nearby Missions (compact list), Volunteer This Weekend, Recently Completed (with proof thumbnails), Organizations Near You.
- Header compresses on scroll (greeting collapses, search sticks). Pull-to-refresh.
States: skeleton modules; per-module error hidden; offline banner; empty city → "No missions near you yet" + Explore All.

### 7.5 Explore
Curiosity. Heading XL "Explore" + search icon; search field + filter button with count; category chips (All selected green); compact mission cards (image 88 px left, badge, title 2 lines, location, progress + %). Infinite scroll; skeleton; empty; filter sheet (PRD FR-04).

### 7.6 Mission Detail
Trust. Full-bleed hero (4:3 to 16:10 by height), glass circular back/heart/share (44 px). Content sheet overlaps hero by 24 px with radius 28. Order: category badge → Heading L title (2–3 lines) → location · date/time row → Body M "Why this matters" excerpt (3 lines, expandable) → amount row `₹12,400 of ₹20,000` (Heading S tabular) + `62%` right → progress bar → 3 stat tiles (12 Volunteers · 200 Meals · 1.2 km From you) → Requirements cards → Organization card → Trust section (verified claims only) → Updates/Proof (after delivery) → spacer for sticky footer.
Sticky footer: `[Volunteer for this mission]` secondary + `[Contribute Now]` primary; tertiary "Save for later" shown on first view (as on board), collapsing into the heart control after scroll. Dynamic CTA by state (Fully Funded / Closed / View Impact). Hero collapses into compact top bar with title on scroll.

### 7.7 Contribute
Agency. Heading L "Contribute"; segmented pills Money · Items · Time · Skills (Money default; hide tabs the mission does not accept). Money: 4 amount chips in a row (selected green), "Other amount" label + ₹ field, fee line Body S secondary (dynamic), primary "Proceed to Pay →" (56), then glass info card with plant illustration: "Your kindness creates real change." Items/Time flows per PRD; Skills shows "Register your skill" interest form (MVP). Keyboard-aware CTA.

### 7.8 Review / Payment / Confirming
Confidence. Review: summary list (Mission, Type, Amount, Fee, Location, Payment method, Anonymous toggle) + "Confirm Contribution" primary. Payment handled by provider sheet. Confirming: spinner ring in glass circle, Heading M "We're confirming your contribution.", Body S "This usually takes a few seconds." No cancel for first 20 s; then "Contact support" tertiary.

### 7.9 Thank You (Success)
Gratitude. Glass circle 160 px with green check drawn in 400 ms + spring; ≤ 12 confetti dots drifting 700 ms; Display M serif "Thank You!"; Body M "Your contribution brings us one step closer to a kinder world."; primary "Share Impact" with share glyph; secondary "Back to Home"; tertiary "Track contribution". Haptic medium. Reduced-motion: static check, fade only.

### 7.10 Tracking
Reassurance. Top bar "‹ Tracking ⋮". Map 48% height: muted style, dotted route, origin/destination dots, mover marker (truck or volunteer glyph), green pill "8 min away", glass recenter/photo buttons. Sheet: Heading S "Your contribution is on the way", Body S "Providing 200 meals · New Delhi", timeline (✓ Order confirmed 10:14 AM · ✓ Picked up 10:28 AM · ● On the way **Live** · ○ Delivered · ○ Verified), volunteer card (avatar 40, "Ravi has picked up your contribution and is on the way.", "ETA: 8 minutes"), actions row (Contact support · Report issue). Connection state chip top-right of sheet. Money-only variant: no map; timeline fills screen with organization update cards.

### 7.11 Activity — Your Impact
Pride. Heading XL "Your Impact" + filter icon; segmented All · Donations · Volunteering · Items; 2×2 stat tiles (Heading L tabular number, Body S label); "Recent Activity" list: pastel icon circle (category), title "Contributed ₹1,000", subtitle "to Community Kitchen", timestamp Caption tertiary; tap → Impact Record. Stats "—" with info when unverified. Empty: butterfly illustration + "Your impact story starts with your first mission." + Explore CTA.

### 7.12 Impact Record
Card stack: NEKI ID `NK-48291` (tabular), status badge (Verified / Under Review …), Contribution, Mission, Organization (with verification badge), Location, Delivered date, Proof gallery (`NekiProofCard`), Impact summary ("87 students received educational material" — only verified), History (corrections listed). Share (excludes amount unless toggled). Download receipt.

### 7.13 Profile
Belonging. Centered avatar 80 with edit badge; Heading M name; Body S "Making a kinder world ✨" (editable); inline 4 stats; list rows (My Contributions, My Bookmarks, My Certificates, Payment Methods, Settings, Help & Support) with Lucide icons in surfaceTint circles and chevrons; footer "NEKI · Humanity, Delivered. · v1.0".

### 7.14 Category page
"‹ Food ⋮" top bar; header row with 3D icon tile 56 + Heading L "Food" + Body S "Nourishment for a brighter tomorrow."; subcategory chips (All · Meals · Rations · Kitchen Kits); compact mission list. Fully data-driven.

### 7.15 System screens
Empty, error, offline, permission rationale, notification center, search suggestions — all use `NekiEmptyState`/`NekiErrorState` with mature copy (no "Oops").

---

## 8. Motion specification

| Moment | Spec | Purpose | Reduced motion |
|---|---|---|---|
| Page push | 320 ms, slide 24 px + fade, ease-out; iOS native swipe-back | Continuity | Fade 150 ms |
| Home → Mission | Shared hero image transition 320 ms | Spatial link | Fade |
| Card press | Scale 0.98, 100 ms in / 160 out, spring | Feedback | None |
| Bookmark | Heart fill + scale 1.2→1.0 spring 220 ms; toast | Confirmation | Fill only |
| Chip select | Background slide 160 ms | Feedback | Instant |
| Progress bar | Fill 320 ms ease-out on first visible | Comprehension | Instant |
| Success check | Path draw 400 ms + spring scale; particles 700 ms | Reward | Static |
| Timeline current | Pulse ring 1.6 s loop | Liveness | Static ring + "Live" text |
| Map marker | Interpolate position 1 s linear between pings | Smooth tracking | Jump |
| Ambient spheres | translateY 8–16 px, rotate 2–4°, 6–10 s, random phase | Warmth | Static |
| Butterfly | Rive idle 4 s loop | Brand | Static frame |
| Skeleton | Shimmer 1.2 s, opacity 0.6→1 | Loading | Static |

No animation may delay a tap response; CTAs respond immediately.

---

## 9. Accessibility requirements

- Contrast: all text AA on its surface (primary green on white 7.9:1; secondary text 4.6:1; verify pastel badge text ≥ 4.5:1 or darken accent).
- Targets ≥ 44×44; key controls 48.
- Semantics: every icon button labeled; mission card summarized as one accessible node ("Provide 200 meals to underprivileged children, Food, New Delhi, 62 percent funded, bookmarked"); progress announces value; timeline states announced.
- Dynamic Type to 200%: layouts reflow; two-line CTAs; stat tiles wrap 2→1 column.
- Reduced motion honored per §8.
- Status never color-only: badges carry text/icon; timeline uses check/ring/outline.
- Maps: text ETA and timeline always present; map is supplementary.
- Focus order logical; keyboard navigation on web portals.

---

## 10. Copy voice

Short, direct, warm, confident, transparent. Examples: "Your contribution is on the way." · "Delivery confirmed. Impact verification is in progress." · "Impact verified." · "No missions match these filters." · "Something went wrong. Let's try again." Forbidden: exclamation-heavy praise, guilt, fake countdowns, "100%" claims without basis, "Oops".

---

## 11. Anti-patterns (hard no)

Excessive gradients · neon green · stock charity imagery · dashboard widgets on mobile · full-app glassmorphism · heavy shadows · badge clutter · animation everywhere · dense tables on mobile · crypto-style impact scores · donation leaderboards · purple SaaS look · cartoon charity graphics · FABs everywhere · rainbow semantic colors.

---

## 12. Deliverables and handoff

1. Figma file: tokens (color/type/spacing/radius/effects) as variables, light + dark; component library with variants and states matching §5; 15 P0 screens × states (default, loading, empty, error, offline) at 390×844 and 360×800; tablet reference for Home and Mission.
2. Prototype: Journeys A–D clickable.
3. Asset pack: butterfly SVG + Rive; wordmark SVG; 12 3D category icons @1/2/3×; ambient sphere PNGs; app icon (Android adaptive foreground/background/monochrome, iOS 1024); splash assets; share card template 1200×630.
4. Motion spec sheet per §8 with Lottie/Rive files where applicable.
5. Photography brief and consent checklist for launch organizations.
6. Design QA checklist per screen (spacing, type, radius, shadow, states, a11y, platform) — signed before "done".
