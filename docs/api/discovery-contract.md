# Address, catalogue and discovery typed contract

**Status:** P0 draft, 2026-09-10. Adds 40 HTTP operations to the 25 identity/preference operations. [Coverage manifest](openapi-coverage.json) lists all remaining operations; public HTML/app association and WebSocket transports remain separate untyped work. No service implementation or privacy enforcement is proved by schema validation.

Authoring source: [contract_discovery.py](../../tools/contract_discovery.py), assembled into [openapi.json](openapi.json). Use the [identity contract reproduction commands](identity-contract.md) for generation/drift and schema validation. Identity schemas remain covered by the same validator.

## Implemented contract shapes

- Addresses: owner-bound create/update/list/default/delete with version checks, six-digit pincode, bounded coordinates and closed request properties. Active shipment address revisions must survive profile-address edits/removal under retention policy.
- Geo: locality search, private reverse lookup and serviceability query; route retrieval requires current assignment revision and authorization. Query POSTs do not require mutation idempotency keys or mutate business state. Serviceability results explicitly say no reservation was created.
- Catalogue: public categories/subcategories/item types and scoped operator CRUD/synonyms. Keep source item conditions NEW/GOOD/FAIR and mission urgency URGENT/THIS_WEEK/FLEXIBLE. All names/URLs/tokens remain data-driven.
- Mission discovery: typed cards/detail, per-need MONEY/ITEM/TIME union, mixed-need examples, published updates and approved redacted proof views. Money uses integer paise, item amounts normalized decimal strings, time availability counts slots. Serviceability and contribution eligibility still require transactional server checks.
- Public Home: independent ready/empty/unavailable modules with module cursors. Private active-contribution modules come only from `/me/home`, never a shared public Home schema. Empty modules are hidden by the client per FR-03.
- Search: stable mixed-kind hit page for missions, organizations and categories; the client may group types. Public query/sort/category/status/organization/type/amount filters are explicit. Filter amount ranges are eligibility/search constraints, not donor-spend ranking inputs.
- Bookmarks: unavailable mission marker retains a removable bookmark without exposing a now-hidden mission. Share metadata contains only safe public title/description/image/link.

## Runtime query invariants still required

OpenAPI validates individual parameter types, not every relationship between parameters. The service must require lat/lng together, reject invalid pair/locality combinations, validate subcategory parentage, check min_amount_paise <= max_amount_paise and validate cursor scope against all filters/projection. Submitted coordinates must be excluded from routine URL/access/analytics logs under G22 policy even where historical GET routes are retained.

Home module pagination calls `/home` with the matching `module` and returned `cursor`; its cursor binds that module and location. A cursor cannot be transplanted between Home, search or mission lists. Proposed Home limits are finalized during pagination review; module cardinality must obey the schema for its content type. Nearest ordering, precise-distance display and map caching/attribution still require the provider and disclosure-policy spike.

Public profile and mission schemas have no raw capture coordinates, pickup address, contributor identity, bank reference or private review documents. This constrains serialized shape; it does not prove an image is redacted or consented, a public URL safe, a cursor authorized or a query correctly scoped. Media processing, scoped read authorization and negative runtime tests remain required. Route and coordinate inputs require current access; a stale token/assignment must fail server-side.

Per-need counts must satisfy approved target/reservation invariants, not merely be nonnegative. A paused/cancelled mission cannot accept a contribution just because an `accepting` field says true. Catalogue response `is_active` and public eligibility checks need runtime filtering. All draft name/string/count limits, token taxonomy and privacy defaults must be reconciled with policy/source documents before P0 gate passage.

## Verification in this slice

The shared validator checks OpenAPI, every attached request/response/error example, inventory coverage, required sensitive grants and public security declarations. Added negative cases reject public pickup/donor/bank/GPS fields, private Home modules, unreviewed public proof, owner injection, invalid coordinate/pincode/paise values, contradictory serviceability and invalid catalogue patches. Query boundary cases reject empty search, oversized pagination/radius, fractional paise and SKILL as an MVP contribution filter.

Identical error-code sets share one schema component to reduce generated repetition; each operation still has its own allowed error responses/examples. No error enum was widened to make unrelated endpoint errors appear supported. The full-coverage gate remains deliberately failing until all inventory operations have typed contracts.
