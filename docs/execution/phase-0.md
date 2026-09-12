# Phase 0 execution register

**Started:** 2026-09-10 · **Status:** In progress; exit gate NOT passed.

Authority: [founder decisions](../07-founder-decisions.md) → [PRD](../01-prd.md) → [accepted ADRs](../adr/README.md), followed by the technical/design contracts in the order defined in [delivery plan §1.1](../08-complete-phased-plan.md). This register tracks execution; it cannot approve policy or supersede those sources.

## Verified starting evidence

| Check | Evidence on 2026-09-10 | Implication |
|---|---|---|
| Active Git root | `git rev-parse --show-toplevel` → `D:/Code/neki-app` | Work in this root; historical nested macOS path does not apply here. |
| Starting revision | `816bc68` — Add complete phased delivery plan (P0-P12) | Baseline before this execution slice. |
| Working tree | `git status --short` returned no entries | No pre-existing local changes at start. |
| Source inventory | Two root source specifications, one reference PNG, eight numbered docs, two indexes, 18 ADRs | 30 Markdown source files plus one image before execution additions. Image presence checked; visual inspection remains pending. |
| Product implementation | No `api/`, `app/`, `web/`, `packages/`, or runnable tests | Historical Flutter code is not current implementation. |
| Architecture status | All 18 ADR files contain Accepted status | Creation complete; correctness, research evidence, and provider compatibility are not verified by status labels. |

## Decisions and operating boundary

D1–D7 remain locked: no NEKI wallet; launch fee subsidy; audited manual payouts; Delhi NCR; Razorpay; Flutter Web ops; OTP/profile/application/ops-approved volunteers without government-ID/KYC. No new legal, financial, retention, eligibility, or service-area policy is accepted by this execution slice.

Owners below are accountable **roles**, not assigned people. Named owners, capacity, and dates need founder/team input and remain gate evidence to collect. No accounts, purchases, external messages, deployments, or live funds have been initiated.

Status meanings: **Open** = work/evidence missing; **Partial** = specific correction delivered but closure criteria remain; **Closed** = stated bounded finding resolved with evidence. Gap closure is not a phase pass or implemented feature.

## Gap register

Each row is the matching `NK-GAP-<nn>` ticket; original G definitions remain in document 08 §3. Dependencies refer to gap IDs. Estimates will be recorded after contract/spike scope is known, not copied from obsolete calendar assumptions.

| Gap / ticket | Status | Accountable role | Next action and closure evidence | Needed before / dependencies |
|---|---|---|---|---|
| G01 / NK-GAP-01 | Closed | Tech lead | Checked all 18 Accepted labels; corrected document 06's creation/sign-off instructions. Broader NK-DOC-1 validation remains open. | P0 |
| G02 / NK-GAP-02 | Closed | Tech lead | Git root/revision recorded above; root README and document 08 identify current versus historical checkout. | Scaffolding |
| G03 / NK-GAP-03 | Open | Product + tech lead | Size child tickets by role, record actual staffing and capacity forecast; original 84.5 person-weeks is not remaining effort. | P0 |
| G04 / NK-GAP-04 | Open | Tech lead | Inspect eight named repos; commit/date/license evidence and findings in `docs/rnd/open-source-review.md`. | P0; NK-DOC-2 |
| G05 / NK-GAP-05 | Partial | Backend lead | Complete operation/schema/error matrix and reviewed OpenAPI for every §18 family. | P0; G08/G14/G25/G29 |
| G06 / NK-GAP-06 | Closed | Product + design | F3/F9 now require D7 approval; F4 uses Delhi NCR. Reapplication/revocation policies tracked separately in G14/G29. | P0 |
| G07 / NK-GAP-07 | Partial | Product + design | PRD FR-11 and F3 specify metadata only; audit original specs/design screen actions and annotate any remaining launch PDF promises. | P0 |
| G08 / NK-GAP-08 | Open | Product + backend | Review separate skills-interest proposal, consent/CRUD and optional mission relation; then amend schema/API. | P0; G29 |
| G09 / NK-GAP-09 | Partial | Backend + Finance | Prototype same-table allocation/locking constraints with concurrent payout/refund tests; record chosen design. | P3; G10 |
| G10 / NK-GAP-10 | Partial | Finance + backend | Define immutable monetary facts, reserves, subsidy, refund/reversal and available-balance equations with examples. | P3; Finance policy |
| G11 / NK-GAP-11 | Partial | Backend | Specify intent/order/attempt cardinality, retries, expiry and late capture transitions. | P0 design / P3 proof |
| G12 / NK-GAP-12 | Partial | Backend | Design recoverable provider order orchestration and uncertain-outcome reconciliation. | P3; G11/provider spike |
| G13 / NK-GAP-13 | Partial | Backend | Specify sequence/ownership/receipt transaction, poison events and crash recovery; reconcile ADR-014. | P0–P1 |
| G14 / NK-GAP-14 | Partial | Backend + ops | [Transition drafts](../state-machines/README.md) now cover all requested aggregate families; policy decisions, source/schema reconciliation and executable evidence remain open. | P0 |
| G15 / NK-GAP-15 | Open | Product + backend | Approve per-need availability, overfill, reservation and mixed-need completion rules; update all contracts. | P0; G11/G14 |
| G16 / NK-GAP-16 | Open | Finance + product | Map received-by-org milestone to evidenced payout/acknowledgement, with sample timelines. | P3; G10 |
| G17 / NK-GAP-17 | Partial | Backend | Reconcile pending Activity projection versus final append-only impact creation across TDD/schema/flows. | P0; G14 |
| G18 / NK-GAP-18 | Open | Product + ops | Approve beneficiary attribution/deduplication wording and repeated-contributor examples. | P6 |
| G19 / NK-GAP-19 | Partial | Backend + privacy | Specify immutable canonical payload, concurrent append, mutable identity, corrections/checkpoints. | P6; G17/G21 |
| G20 / NK-GAP-20 | Open | Infrastructure + backend | Verify storage APIs in current primary docs; amend ADR-009/TDD and test chosen immutable-key/retention controls. | P0–P1 |
| G21 / NK-GAP-21 | Open | Privacy/legal + ops | Review data-class retention/deletion/holds/redaction register, then amend conflicting sources. | P0 policy / P8 drill |
| G22 / NK-GAP-22 | Open | Backend + privacy | Inventory location stores including devices/events/proof; define and test expiry for each. | P0–P5; G21 |
| G23 / NK-GAP-23 | Open | Privacy + product | Resolve 50 m versus three-decimal disclosure; specify serialization and route leakage tests. | P5; G22 |
| G24 / NK-GAP-24 | Open | Security + ops | Define purpose/owner/role media matrix including org uploader access and redacted home proofs. | P2; G21/G25 |
| G25 / NK-GAP-25 | Partial | Security + Finance | Define scoped actions, reasons, step-up, separation of duties and revocation behavior. | P0–P1 |
| G26 / NK-GAP-26 | Open | Product + backend | Reconcile indexed fields and unbiased ranking policy, then fixtures/query plans. | P2 |
| G27 / NK-GAP-27 | Open | Backend | Specify public versus owner-scoped Home composition, cache keys and invalidation. | P1–P2; G25 |
| G28 / NK-GAP-28 | Open | Tech lead | Record bounded version/provider/deployment spikes with reproducible evidence and unavailable accounts. | P0–P1 |
| G29 / NK-GAP-29 | Open | Backend + product | Model consent, cases, target changes, proof rework, fee revisions, eligibility and approval history. | P0; G14/G21/G25 |
| G30 / NK-GAP-30 | Open | Designer | Inspect board; test 390×844 and 320 px/200% text reflow with actual contrast measurements. | P0–P2 |

## MVP requirement and acceptance coverage

This maps all PRD requirements to a delivery phase and an acceptance scenario to implement. These are planned cases, **none executed**. A–D retain source journey names; E–H below are local acceptance labels, not new product requirements.

| PRD | Phase(s) | Contract owner | Acceptance scenario |
|---|---|---|---|
| FR-01 Authentication | P1 | Backend + Flutter | A/B/C/D prerequisite: OTP signup, session restore, denied permissions, token reuse rejection. |
| FR-02 Location | P1/P2 | Product + backend | D: manual Delhi location works; selecting outside the service area does not authorize pickup. |
| FR-03 Home | P2/P3/P5 | Backend + Flutter | D: independent module failures preserve usable feed; account switch exposes no previous user's active contribution. |
| FR-04 Explore/search | P2 | Backend + Flutter | D: filters, pagination, empty/offline states and organization/category search are consistent. |
| FR-05 Categories | P2 | Backend + Flutter | D: API category opens correct missions and empty/error states without hard-coded cause screens. |
| FR-06 Mission detail | P2 | Product + backend | A/B/C: quantified mixed needs show eligible CTAs per type; closed money need does not disable open items/time. |
| FR-07 Money | P3 | Payments + Finance | A: disclosed allocation → checkout → uncertain/late capture recovery → reconciled refund/payout facts; no duplicate charge effect. |
| FR-08 Items | P4/P5 | Dispatch + backend | B: item/address/slot → approved assignment → pickup → acknowledged delivery; failed pickup recovers through ops. |
| FR-09 Volunteering | P4/P6 | Ops + backend | C: application approval → eligible slot → attendance → verified hours; unapproved/suspended booking denied. |
| FR-10 Tracking | P5 | Backend + Flutter | A/B: versioned snapshot/reconnect/offline recovery preserves truth; assignment end revokes location access. |
| FR-11 Impact | P6 | Backend + product | A/B/C: verified completion produces one record; retries, repeated missions, corrections and anonymization preserve integrity. |
| FR-12 Profile/settings | P6/P8 | Product + privacy | G: update preferences, support case and deletion request; scoped retained records follow reviewed policy. |
| FR-13 Bookmarks/share | P2/P6 | Backend + Flutter | D/G: bookmark is owner-scoped; public share fallback exposes no contribution/private proof. |
| FR-14 Notifications | P3–P6 | Product + backend | A/B/C: state-deduplicated notifications follow preferences and quiet hours; deep links enforce access. |
| FR-15 Org portal | P2–P7 | Web + ops | E: apply → document rework → verified org → mission moderation → roster/delivery → proof rework → impact. |
| FR-16 Ops console | P1–P7 | Web + Finance/ops | F: authorized dispatch, review, payout, reconciliation and recovery have reasons/audit; cross-role actions denied. |
| FR-17 Proof | P6 | Ops + backend | H: quarantined/private upload → consent/provenance → review/rework → verified record; unauthorized media access denied. |

## First reviewable work queue

Ordered by dependency; estimates are provisional focused authoring time, exclude owner review and provider waiting, and do not constitute G03 closure. Split further if execution exceeds three engineer-days.

| Child ticket | Outcome / acceptance | Depends on | Role / estimate | Status |
|---|---|---|---|---|
| NK-DOC-1.01 | Verify checkout and ADR existence, correct stale instructions, establish all 30 gap rows and 17 FR mappings. | Existing plan | Tech lead / 1 day | Delivered in this slice; review pending |
| NK-DOC-3.01 | Draft org/application/mission transition tables with actor, prior version, guards, evidence, effects, event, copy, notification and error per row; unresolved policy choices explicitly linked. | G14/G25/G29 review input | Backend + ops / 2 days | Draft delivered; policy/source reconciliation pending |
| NK-DOC-3.02 | Draft per-type contribution/payment attempt/refund/payout transitions and money invariants, including late capture and concurrent reservations. | G10/G11 policy design | Payments + Finance / 3 days | Draft delivered; FD/CD decisions and database/provider proof pending |
| NK-DOC-3.03 | Draft shipment/assignment/proof/correction transitions and typed event envelope/receipt/replay semantics. | NK-DOC-3.01/.02; G13/G17 | Backend + ops / 3 days | Draft delivered; LD/VD decisions, schemas and fault tests pending |
| NK-DOC-2.01 | Inspect first four named research repositories at pinned commits; record licenses, architecture/test evidence and rejected ideas. | Public source availability | Tech lead / 2 days | Ready for research |
| NK-DOC-2.02 | Inspect remaining four repositories with the same evidence; qualify unsupported ADR comparisons. | NK-DOC-2.01 format | Tech lead / 2 days | Open |
| NK-DOC-1.02 | Storage/deployment spike plan and primary-source checks, explicit reproducible account-dependent steps; amend affected ADRs only with evidence. | G20/G28 | Infrastructure / 2 days | Ready for research |
| NK-DOC-4.01 | Operation inventory + authorization/error matrix for every §18 family; no implied unrestricted admin transitions. | Draft transitions + G25 | Backend / 2 days | Inventory/policy/profile draft delivered; schemas and capability grants pending |
| NK-DOC-4.02 | Reviewed OpenAPI schemas/examples, validation and generated-client workflow; reconcile TDD/schema references. | NK-DOC-4.01 | Backend / split after inventory | In progress: identity and discovery slices typed and validated; remaining operations tracked explicitly |
| NK-DES-2.01 | Full route/state inventory covering consumer, volunteer, org, ops/Finance, recovery and inaccessible states. | PRD + F0–F10; G30 | Design + Flutter / 2 days | Ready for drafting |
| NK-DOC-5.01 | Decision-owner register for legal/receipt, retention, pickup/age, refund/payout, capacity and provider onboarding with people/dates. | Founder/team input | Founder + tech lead / 1 day authoring | Open; names/dates unassigned |

## P0 gate evidence checklist

| Required evidence (plan §5.5) | Current result |
|---|---|
| Scope/source/decision register | Initial register delivered; policy decisions still open. |
| All MVP behaviors have contract owner and acceptance | FR coverage mapped to roles/scenarios; detailed contracts and named owners missing. |
| Research/provider/version evidence | Partial: Razorpay primary documentation inspected, retry conflict recorded, seven sandbox probes specified but not executed. Other provider/version and eight-repository evidence missing. |
| Transition/event catalogue and revised schema | Partial: 139 command rows across org/volunteer/mission, contributions, money, logistics/attendance and proof/impact; event processing/consumer map drafted. 30 PD/FD/CD/LD/VD decisions open and 77 planned cases; accepted per-event schemas, source reconciliation and revised DDL missing. |
| OpenAPI/errors/auth matrix | Partial: 324 operation rows spanning all 22 plan families, route/field policies and request/error profiles. Structural validator passes. 279 domain and provider-intake operations typed in OpenAPI with 3,213 validated examples, 225 rejected negative schema cases and five rejected query cases; 45 operations remain untyped. Provider intake has 20 passing synthetic local HMAC/SQLite tests, not sandbox or financial-effect proof. Final grants, source reconciliation, runtime checks and full per-operation event schemas missing. |
| Design states/prototypes/assets/usability evidence | Missing; no design validation claimed. |
| Operating policy drafts and approved foundation blockers | Missing; no operational thresholds silently adopted. |
| ADR contradictions reconciled | Creation finding corrected; substantive validation remains open. |
| Sized Phase 1 backlog and staffing/cost model | Missing; original tickets are scope references, not ready sprint commitments. |
| Named external/legal/provider owners and dates | Unassigned. Live-funds approval remains a later explicit gate. |

NK-DOC-3.01 draft delivered: [catalogue](../state-machines/README.md), [open decisions and planned cases](../state-machines/review-decisions.md). Source-backed rules and proposed resolutions are distinguished; no policy approvals or runtime tests are claimed. NK-DOC-3.02 draft delivered: [contributions](../state-machines/contributions.md), [financial commands](../state-machines/payments-and-payouts.md), [money invariants](../state-machines/money-invariants.md), [25 planned cases](../state-machines/money-acceptance.md) and [provider evidence](../rnd/payment-provider-spike.md). G09–G12 are partial: proposed fixes exist, but no SQL/sandbox proof or Finance review. NK-DOC-3.03 draft delivered: [logistics/attendance](../state-machines/logistics-and-attendance.md), [proof/impact](../state-machines/proof-and-impact.md), [events/recovery](../state-machines/events-and-recovery.md) and [fulfilment checks](../state-machines/fulfilment-acceptance.md). G13/G17/G19 are partial, not proven. NK-DOC-4.01 draft delivered: [API workspace](../api/README.md). G05/G25 are partial; inventory rows do not prove an implemented endpoint or complete permission enforcement. NK-DOC-4.02 started: [typed identity contract and reproduction](../api/identity-contract.md), [exact coverage](../api/openapi-coverage.json). Strict completeness deliberately fails. [Discovery schema slice](../api/discovery-contract.md) delivered with public/private projection checks. [Organization and mission-management slice](../api/organization-contract.md) delivered with applicant/reviewer separation and guarded decision shapes. [Contribution and checkout slice](../api/contribution-contract.md) delivered with quote-based confirmation, independent payment recovery and checkout uncertainty. [Case and refund slice](../api/case-refund-contract.md) delivered with separate owner/Finance projections and bound approval snapshots. [Payout and Finance slice](../api/payout-contract.md) delivered with transfer uncertainty, return history and scoped reports. [Provider intake slice](../api/provider-contract.md) delivered with signature transport and 20 local fixture tests. RP-06 remains open pending sandbox evidence. [Volunteer/skills/attendance slice](../api/volunteer-attendance-contract.md) delivered with 43 operations and separate booking/assignment/evidence shapes. [Logistics slice](../api/logistics-contract.md) delivered with 24 operations and private field/custody/receipt boundaries. [Media/proof slice](../api/media-proof-contract.md) delivered with 26 operations and distinct upload, processing, participant and reviewer boundaries. [Impact slice](../api/impact-contract.md) delivered with 12 operations separating original/effective claims and conditional sharing. Next slices: administration, notifications/realtime, saved methods and web transports. Provider/research and owner decisions remain independent P0 work. Research and screen-state drafting can proceed independently. P0 remains open.
