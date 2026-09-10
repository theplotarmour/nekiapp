# Organization and mission management typed contract

**Status:** P0 review draft, 2026-09-10. Adds 54 operations for applications, organization settings, mission editing and scoped moderation. Total coverage is 119 of 324 inventory operations. No endpoint implementation or policy approval is implied. See the [coverage manifest](openapi-coverage.json) for the exact partition.

Authoring source: [contract_organizations.py](../../tools/contract_organizations.py). Generation and validation use the [shared reproduction commands](identity-contract.md). Contracts follow the [organization transitions](../state-machines/organization-review.md), [mission lifecycle](../state-machines/mission-lifecycle.md) and [authorization matrix](authorization.md).

## Contract behavior

- Applications bind ownership on the server before organization privileges exist. Applicant responses exclude restricted review notes. Document responses contain metadata and media IDs; access to actual media requires separate authorization. Resubmission preserves the prior decision and creates a new submission revision.
- Profile patches cannot set verification, legal identity or bank references. Bank changes use a dedicated sensitive operation, with raw account input restricted to the request and only masked account output. This requests review; it does not verify a payout recipient.
- Mission creation accepts a title and derives the organization from the authenticated scope. Draft patches exclude status and contribution counters. MONEY needs use positive integer paise; ITEM needs use positive decimal quantities and approved condition tokens; TIME needs reference roles with separately defined capacity slots.
- Submission identifies the reviewed draft version. Lifecycle changes use explicit commands with versions, reasons and evidence where required. Readiness references a snapshot and any partial-fulfilment decision. Live target changes are review requests with a base mission version, rather than writable contribution counters.
- Review decisions are explicit VERIFY/PUBLISH, NEEDS_MORE_INFORMATION or REJECT branches. Approval checklist entries must pass or reference an approved exception. Applicant feedback and restricted reviewer views use separate schemas.
- Organization contribution lists exclude donor phone and address fields; roster entries exclude captured GPS. Impact names distinguish mission-reported beneficiaries from unique people and verified seconds from pledged time.

## Remaining runtime and review obligations

Schema validity does not establish ownership, current organization eligibility, document processing, checklist completeness, exception authority or submission freshness. The service must resolve all referenced IDs within the caller's permitted scope and lock the relevant version before changing state. Rejected, suspended and expired organizations cannot bypass their lifecycle through a well-formed approval payload.

The server must enforce slot start before end, role/need relationships, unique need and slot identities, capacity reservations, category parentage, evidence purpose and current media access. Positive targets alone do not prove a complete or feasible mission. Submission must reject incomplete drafts with `MISSION_INCOMPLETE` (422) and ineligible organizations with `ORG_NOT_ELIGIBLE` (403).

Change approval must recheck commitments, accepted participant consent and required notification plans against the current mission version. A nullable notification plan is not permission to skip a required notification. Anonymous display values, contribution type/amount relationships and verified impact totals require semantic checks. Closed response schemas cannot themselves prove correct anonymization or aggregation.

Every state-changing command still requires the shared idempotency, expected-version, audit and outbox protocol. Review history, revocation and durable recovery must be atomic; cancellation or failure does not mean refunds or custody recovery have finished. Exact event payloads, transition-specific error reconciliation, grant policies, checklist taxonomy and PD/FD decisions remain open P0 work.

## Verification

The shared validator passes OpenAPI validation and 1,242 attached request, response and error examples across 119 operations. It rejects 61 negative schema cases and five query boundary cases. Twenty new negative cases cover ownership/status injection, raw bank and private field leakage, invalid targets, arbitrary transitions, empty evidence and failed or unapproved exception checks. These are schema checks; example responses are illustrative shapes, not executed command histories.

The strict completeness gate continues to fail because 205 operations remain untyped. No database, service, provider or browser verification has been performed by this slice.
