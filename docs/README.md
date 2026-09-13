# NEKI — Documentation index

**NEKI — Humanity, Delivered.** Track every contribution. Verify every mission. See every impact.

| # | Document | Purpose |
|---|---|---|
| 01 | [Product Requirements (PRD)](01-prd.md) | Problem, personas, scope ladder (NOW/MVP/NEXT/LATER), 17 functional requirements with states/analytics/acceptance, NFRs, open questions |
| 02 | [Technical Design (TDD)](02-tdd.md) | System architecture, Flutter + FastAPI design, state machines, event model, API inventory, realtime, payments, media/proof, security, privacy, testing, ADR summary |
| 03 | [User Flows](03-user-flows.md) | Step-by-step flows for contributor, volunteer, organization, ops; realtime states; edge-case matrix |
| 04 | [Design Brief](04-design-brief.md) | Brand, reference-board teardown, tokens (color/type/spacing/motion), component library, per-screen briefs, accessibility, handoff |
| 05 | [Data Model](05-data-model.md) | Enums, ER diagram, tables by domain, core DDL, invariants, Redis keys, storage layout, analytics schema |
| 06 | [Engineering Plan](06-eng-plan.md) | Repo audit, team, phases and tickets, milestones, DoD, CI gates, risk register, release plan, locked decisions |
| 07 | [Founder Decisions](07-founder-decisions.md) | D1–D7 locked 2026-09-07: no wallet, NEKI absorbs gateway fee, manual payouts, Delhi NCR, Razorpay, Flutter Web ops, phone + ops-approved volunteers |
| 08 | [Complete Phased Delivery Plan](08-complete-phased-plan.md) | Detailed P0–P12 execution plan: document gaps, capacity-based schedule, work packages, dependencies, acceptance gates, API/data inventory, full requirement/ticket mapping, adverse-case tests, risks, launch and expansion |
| adr | [ADR index](adr/README.md) | ADR-001…018 |

Source inputs (root of repo): `NEKI_Master_RND_Architecture_Documentation_Prompt.md`, `NEKI_Complete_UI_UX_Design_Specification.md`, UI board `c0f5b185-e8b2-44fa-a0fe-626ee5f561a8.png`.

ADRs 001–018 and transition drafts in `state-machines/` are present. The eight-repository R&D report, typed contract workspace and validation fixtures are present; production runtime verification and source reconciliation remain separate work.

For the proposed delivery sequence and revised staffing/timing assumptions, start with document 08. Document 06 retains the original ticket IDs and estimates; document 07 governs locked founder decisions.

Execution started on 2026-09-10. The [Phase 0 execution register](execution/phase-0.md) tracks the current checkout, gap ownership, requirement acceptance coverage, next tickets, and gate evidence. Phase 0 remains open.

The [transition contract drafts](state-machines/README.md) cover organization review, volunteer approval, mission and contribution lifecycles, checkout, refunds and manual payouts, with shared command rules, unresolved decisions and planned acceptance cases. [Razorpay evidence](rnd/payment-provider-spike.md) records documentation findings and required sandbox probes. Drafts do not amend accepted source contracts until reviewed.

The [API contract workspace](api/README.md) adds a machine-readable operation inventory, route/field authorization and request/error profiles. All 324 inventoried operations have typed draft coverage and structural/example validation; approval, source reconciliation and executable API verification remain pending.

[Open-source inspection](rnd/open-source-review.md) records all eight named repositories at pinned revisions, license evidence, source-level findings and rejected patterns. Static provenance is verified; compatibility and runtime behavior remain separate P0 work.

[MVP screen/state inventory](design/screen-state-inventory.md) maps consumer, volunteer, organization, operations/Finance and public-web destinations to requirements, shared states and recovery branches. This is a design draft; prototypes and usability evidence remain open.

[Current Flutter stack spike](rnd/flutter-current-stack-spike.md) passes analysis, 14 tests and Chrome IndexedDB reload/account-clear checks. The [historical baseline](rnd/flutter-stack-spike.md) is preserved. [PostgreSQL outbox evidence](rnd/postgres-outbox-spike.md) records 14 isolated ordering/recovery tests; production target/provider gates remain open.


[Interactive journey review](design/prototype/README.md) covers nine simulated journeys, alongside [tokens/asset handoff](design/asset-handoff.md) and measured contrast. [Operating policy draft](policies/foundation-draft.md) separates proposed operating rules from unapproved values. The [P1 backlog](execution/phase-1-backlog.md) supplies 33 dependency-linked tickets, estimates and a capacity/cost model; no P1 completion is implied.
