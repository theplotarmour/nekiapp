# MVP screen and state inventory

Status: **P0 design draft, NK-DES-2.01**. Routes are proposed client destinations, not implemented routes or permission grants. [screens.tsv](screens.tsv) is the screen/sheet/dialog inventory. This document supplies its shared state definitions and acceptance rules. Named designers, prototypes, rendered accessibility checks and formative usability evidence are still outstanding.

The inventory contains 165 rows: 65 consumer, 19 volunteer, 26 organization, 47 operations/Finance, and eight public-web rows. Two public-web rows are association transports, not visible screens. All FR-01–17 and flows F0–F10 have references; reference presence alone does not prove full behavior coverage or design approval.

Authority: founder decisions D1–D7, PRD FR-01–17, [flows F0–F10](../03-user-flows.md), [design brief](../04-design-brief.md), and [delivery plan §5.4](../08-complete-phased-plan.md). Draft API/state-machine decisions remain proposals. Existing flow examples of amounts, ages, geofences, cancellation cutoffs, timers and approval thresholds are not newly approved by this inventory.

## Inventory conventions

Each row has a stable screen ID, surface, proposed route, title, access boundary, requirement IDs, flow references, state profile, related API family and a screen-specific recovery requirement. Routes ending in `/review`, `/filters` or `/decision` may render as sheets/dialogs on large screens; their stable ID remains the same. Consumer and volunteer share one installed app. Organization and operations use separate authenticated Flutter Web shells. Public web paths retain their root transport contracts.

`api_family` identifies related contracts, not an instruction to load every operation in a family. Final action-to-operation mapping belongs to each implementation ticket. Public/read-only pages do not inherit private actions from this column. A local screen uses `none`. No proposed route is an access-control boundary by itself.

Every row inherits loading, error and accessibility requirements below. Its profile adds specific states; its final column specifies a critical branch that must appear in the prototype and acceptance ticket. A list with no initial data is different from a filtered list with zero matches. A denied private resource is different from a transport failure. Neither should expose previously cached private content.

## State profiles

| Profile | Required states | Recovery and truth rules |
|---|---|---|
| BOOT | starting, restored, signed-out, offline-cache, maintenance, update-required | Route only after session resolution; public browsing remains possible where allowed. Never show the previous account's private shell during restoration. |
| AUTH | input, invalid, sending, challenge-issued, verifying, wrong-code, expired, throttled, session-ready, dependency-error | Keep code as text, support paste/autofill and accessible labels. Retry timing comes from the server. A device biometric prompt does not replace a server step-up grant. |
| READ | loading, available, unavailable, forbidden, stale-offline, dependency-error | Public unavailable content uses safe copy; private content is removed on revocation. Show freshness if cached. Retry preserves route context without revealing inaccessible identifiers. |
| LIST | initial-loading, populated, empty, no-matches, refreshing, loading-more, end, next-page-error, stale-offline, forbidden | Preserve already loaded permitted rows on page failure. Reset pagination on query change; ignore stale search responses. Empty state offers a relevant next action. |
| FORM | pristine, editing, invalid, dirty-leave, submitting, saved, version-conflict, forbidden, dependency-error | Keep safe user input on recoverable failure. Show field errors plus summary; restore focus to first error. Refetch before resolving a version conflict; no blind overwrite. Private drafts follow retention policy. |
| COMMAND | ready, confirmation, step-up-required, submitting, accepted-pending, completed, conflict, forbidden, uncertain, failed | Disable duplicate taps but also reuse the command's idempotency key. Timeout shows an uncertain operation with status recovery. Accepted or queued does not mean completed. |
| CHECKOUT | capabilities-loading, quote-ready, quote-expired, review, launching, provider-active, confirming, still-confirming, captured, server-failed, retry-eligible | Show current fee/allocation disclosure. Client callback/cancel is a hint; server status resolves payment truth. Do not launch a second order while the first outcome is unresolved. |
| TRACKING | connecting, live, reconnecting, polling, stale-offline, resync-required, scope-revoked, complete, issue | Show snapshot time and last update. Map failure preserves timeline. Ignore older aggregate versions; clear restricted fields on assignment/access change. Delivered and impact-verified are separate milestones. |
| MEDIA | selecting, local-ready, uploading, retryable-failure, pending-processing, quarantined, ready, rejected, expired-access | Track each attachment independently. Uploaded bytes are not approved evidence. Expired read URLs require fresh authorization. No private images in public error or thumbnail caches. |
| REVIEW | queue-loading, assigned, reading, evidence-pending, decision-ready, step-up-required, submitting, conflict, needs-info, decided, forbidden | Present the exact revision and evidence being reviewed. Reason and required checks accompany decisions. Prevent self-approval where required; a stale review cannot approve a changed revision. |
| REPORT | criteria, submitting, queued, running, ready, failed, expired, revoked | Poll an authorized job; do not resubmit because generation is slow. Download access is independently checked and expires. Filter and export scopes must match. |
| WEB | loading-at-origin, published, unavailable, dependency-error | Server-rendered support/fallback works without an installed app or JavaScript. Only approved public data/copy. Association responses follow the separate web transport contract. |

State precedence: account/session revocation and resource denial clear restricted content first; then version/conflict recovery, operation uncertainty, dependency failure, offline freshness, and ordinary success. A cached success never overrides a current denial. These are client presentation rules; the server still authorizes every action.

## Navigation and cross-surface rules

- Consumer tabs remain **Home, Explore, Contribute, Activity, Profile**. Contribute without a mission starts mission selection; skills interest is separate capture, never a fabricated completed contribution. No wallet/balance or certificate-PDF launch navigation.
- Private impact sharing stays disabled pending AP-04 privacy approval. Public mission/organization sharing remains available; a prototype must not introduce an active private-share route merely because draft endpoints exist.
- Anonymous discovery can prompt authentication at a private action, retaining a validated internal destination. After sign-in, recheck resource availability and eligibility. Never execute the original mutation automatically after authentication.
- Notification/share links enter through the same resource checks as normal navigation. Deleted, hidden, revoked and unknown targets have safe recovery to the appropriate list. Do not place private addresses, tokens or payment data in route/query strings.
- Volunteer application and approval status are reachable before eligibility to book. Pending, rework, rejected and suspended applicants see truthful status and permitted next steps. Reapplication remains conditional on server policy. No government-ID collection in MVP.
- Organization and ops shells show only permitted navigation groups. Hiding a menu is not authorization. Role expiry during a form closes protected evidence and provides safe recovery; it does not silently submit a privileged action.
- Browser back/refresh and mobile process death must recover the server operation, not replay payment, payout, delivery or review commands. Forms distinguish saved drafts from local unsent changes. Nested sheets return focus to their trigger.
- Live maps are supplementary. Location permission denial permits manual city/address entry. Out-of-area discovery does not imply pickup serviceability. Never present an unapproved drop-off or slot option to avoid an error.

## Required prototype journeys

| Prototype | Screen sequence and essential adverse branch | Completion evidence |
|---|---|---|
| A — Money | C12 → C20 → C21 → C22 → C23 → C24 → C25 → C42; quote expiry, provider cancel/late capture, process death and refund status | Confirmation uses server payment truth; verified record appears only after verification. |
| B — Items | C12 → C27 → C28 → C29 → C30 → C24 → C25; unserviceable address, slot loss, attachment processing, pickup no-show | Pending sync and accepted pickup are visually different; contributor sees delivery/verification separation. |
| C — Time | C12 → V01 → V02 → V03 → V04 → V05 → V06 → V07 → C42; approval pending/revoked, waitlist, missed check-out | Hours remain unverified until attendance approval. Certificate metadata has no unavailable PDF action. |
| D — Discovery | C08 → C09/C10 → C11 → C12/C13; empty city, search race, no matches, permission denial, private bookmark login | Search and manual Delhi location work; no previous account's private module appears. |
| E — Organization publish | O01 → O02 → O03 → O04 → O07 → O08 → O09 → O10; document rework, moderation feedback, forbidden target edits | Server-approved revision is the one published; draft and public preview are labeled. |
| F — Proof review | O17/O18 → X10 → X11 → X12 → C42; quarantined media, missing consent, rework and stale decision | Requirements, evidence revision and decision reason are visible; public view hides internal review details. |
| G — Payout approval | X16 → X17 → X18 → X19 → X20 → X21; self-approval denial, bank change, uncertain transfer, returned payment | Draft/approved/transfer-started/paid/reconciled remain distinct; timeout never invites a blind duplicate transfer. |
| H — Volunteer recovery | V09 → V10 → V11 → V12 → V13 → V14 → V15; offline capture, revoked assignment, out-of-order receipt, no-show custody handoff | Pending actions can reconcile or reject with recovery; private route disappears after access ends. |
| I — Account/support | C49 → C53/C54 → C55; step-up failure, deletion hold/cutoff, retained finance record | Copy describes actual deletion/retention status; no promise of immediate blanket deletion. |

Screen sequences identify the principal path; sheets and permission prompts from the TSV remain included. These are prototype requirements, not records of completed usability sessions.

## Layout, accessibility and interaction acceptance

Validate consumer and volunteer screens at 320, 360, 390 and 412 px widths; portals at 768, 1280 and 1440 px, with narrow-screen safe alternatives. Test all surfaces at 200% text scaling, light/dark, reduced motion, keyboard and screen reader. No completed check is implied by this document.

| Component/context | Required behavior |
|---|---|
| Sticky CTA and keyboard | Content reserves footer space; CTA expands with text and remains above keyboard/safe area. Back and submit remain reachable at 320 px. |
| Tables/review panes | Preserve row identity and primary action in a stacked narrow layout; horizontal scroll only for genuinely tabular comparisons. Evidence viewer and decision controls remain keyboard reachable. |
| Errors and asynchronous status | Field errors are linked to controls; focus summary after invalid submit. Announce meaningful completion/error once without continuously announcing location pings. |
| Sheets/dialogs | Label title, trap focus where modal, Escape/back dismiss when safe, dirty-form confirmation when needed, return focus on exit. Do not dismiss uncertain operations as if cancelled. |
| Maps/evidence | Text timeline, address access status and ETA alternatives. Evidence images need meaningful context; illustration cannot stand in for mission proof. |
| Status and amounts | Text/icon accompany color. Monetary values use proper units; approximate/organization-reported/verified claims remain labeled. Skeletons cannot imply verified statistics. |
| Touch and typography | Minimum 44×44 target, primary controls 48+; headings/labels wrap; no clipped amount or action at 200% text. Measure actual color contrast separately. |

## Reconciliation still required

The source flow's single contribution-success milestone and Activity-to-record shortcut must distinguish pending contributions from issued impact records. The original design's skills fulfillment and certificate download examples are deferred; MVP captures skills interest and certificate metadata. Pickup rescheduling, attendance overrides, proof checks, age and consent thresholds remain governed by reviewed policy, not hard-coded from example copy.

Next deliverables: component variants/token contrast evidence, linked prototypes for all rows used in A–I, assets with provenance, and formative sessions with contributor, volunteer, organization and ops representatives. Record observed failures and design changes before closing NK-DES-2 or the P0 gate. Structural inventory validation only checks IDs, references and coverage bookkeeping.

Reproduce the reference checks from the repository root with `.venv-contracts/Scripts/python tools/check_screen_inventory.py`. The check rejects duplicate IDs/routes, unknown API families, missing requirement/flow references, undefined state profiles and mismatched public-web paths. It does not validate the correctness or completeness of a screen design.
