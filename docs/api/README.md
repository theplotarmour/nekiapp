# API contract workspace

**Status:** P0 operation inventory draft, NK-DOC-4.01. No endpoints are implemented. Authority: [plan §18](../08-complete-phased-plan.md), [TDD §8](../02-tdd.md), [transition catalogue](../state-machines/README.md), D1–D7. The inventory supplies route/operation/policy coverage for review; it is not a validated OpenAPI contract or generated client.

- [Operations](operations.tsv): machine-readable, tab-separated, one route/method per row. `operation_id` is stable; paths are relative to `/v1` except PUBLIC_WEB/WS rows. All additions are proposed.
- [Authorization and field matrix](authorization.md): each row's policy resolves server-side scope, capabilities and field projection.
- [Request/error profiles](request-profiles.md): each row inherits its success, concurrency, idempotency, rate-limit and error rules.
- [Typed identity contract](identity-contract.md): first 25 operations, generated OpenAPI, exact remaining-coverage manifest and executable schema/example checks. Full API coverage remains incomplete.
- [Typed discovery contract](discovery-contract.md): another 40 address/geo/catalogue/discovery/bookmark operations with public/private projection checks. Current coverage is recorded in the generated manifest.
- [Typed organization contract](organization-contract.md): another 54 organization application, mission-management and moderation operations, with separate applicant and reviewer schemas.
- [Typed contribution and checkout contract](contribution-contract.md): another 14 operations with quote-based confirmation, type-specific contribution records and explicit checkout uncertainty.
- [Typed case and refund contract](case-refund-contract.md): another 17 operations with owner/reviewer separation, immutable approval references and explicit refund uncertainty.
- [Typed payout contract](payout-contract.md): another 24 operations covering manual transfer evidence, uncertainty, returns, bank review and scoped Finance reports.
- [Payment webhook transport](provider-contract.md): provider signature/inbox contract plus 20 synthetic local verification tests; sandbox and production behavior remain unverified.

Columns: family (plan §18.1); method; path; operation_id; policy; projection; profile; contract. `contract` refers to a transition ID, decision ID or governing PRD requirement; it is traceability, not approval. The next schema pass must give every row typed parameters/request/response/errors/examples and precise event effects, then produce reviewed OpenAPI. No `object` placeholders or blanket success responses can pass that later gate.

## Deliberate source corrections pending review

- Organization application ownership exists before `org_admin`; `/org/apply` must not require the role created by successful approval.
- Generic `/transition` routes accept only a reviewed command discriminant with actor-specific guards. They cannot accept arbitrary target status. The operation inventory uses explicit command endpoints where the source route is unsafe/ambiguous; TDD migration mappings below retain traceability.
- Financial/provider responses can be asynchronous: a contribution intent is not proof that provider order creation succeeded. See payment profile and P01–P07.
- WebSocket query tokens are short-lived, single-use connection tickets, not access/refresh credentials. Channel authorization is per subscription and rechecked after revocation; tickets and private query parameters must be redacted in logs.
- Private media read URLs are resolved from purpose/owner/role policy at request time. Public mission viewing grants no private proof/GPS/addresses.
- Account deletion is a request workflow with status/cancellation under policy; `DELETE /me` is not immediate blanket deletion of retained records.

## Source path reconciliation map

| Historical TDD route | Inventory replacement / reason |
|---|---|
| `DELETE /me` | `POST /me/deletion-requests`, current request status/cancel; preserves reviewed retention and irreversible-stage handling. |
| `DELETE /assignments/{id}` | `POST /assignments/{id}/cancel`; reason, expected version and idempotent command instead of erasing attendance history. |
| `POST /shipments/{id}/transition` | Explicit pickup/depart/arrive/deliver/issue commands; no status dropdown. |
| `POST /org/missions/{id}/transition` | Explicit ready/start/deliver/pause/resume/cancel commands with state guards. |
| `POST /admin/shipments/{id}/transition` | Explicit dispatch commands including custody-handoff; preserve evidence and old assignment revision. |
| `POST /org/proofs` | Canonical `POST /proofs` using subject-scoped org policy; do not maintain two independent submission contracts. |
| `GET /missions/{id}/proofs` | Public-safe approved derivatives only; private evidence uses scoped `/proofs/{id}` and media read authorization. |
| `WSS /ws?token=...` | `POST /realtime/tickets` then `/ws` with single-use ticket; no long-lived tokens in URLs. |
| `GET /geo/reverse` | `POST /geo/reverse` read-only query profile keeps submitted precise coordinates out of ordinary URL/query logs. |
| `GET /home` with mixed modules | Public `/home` and private `/me/home`; prevent cross-user leakage from shared city cache. |

Old routes have never shipped, so no compatibility aliases are required yet. Any future deployed clients require explicit deprecation/backward-compatibility planning.

## Remaining review decisions

AP-01: finalize exact input/output schemas, event names and shared errors (including source 422 versus draft 409 idempotency mismatch). AP-02: approve capability grant/step-up and browser cookie/CSRF/session-revocation details. AP-03: finalize rate limits/cursor expiry and safe cursor/ETag scoping. AP-04: private impact sharing is conditional in §18; proposed consented revocable token endpoints remain disabled until privacy approval. AP-05: deletion cancellation cutoff, export retention and report/download access lifetime. All OPEN; domain PD/FD/CD/LD/VD decisions remain linked constraints.

Owner: backend/security with Product/Finance/privacy on their scoped decisions. Validate inventory uniqueness, family coverage and policy references with `python tools/check_api_inventory.py`; this checks specification structure, not API implementation/security or end-to-end behavior.
