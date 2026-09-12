# Impact record and correction contracts

**Status:** P0 review draft, 2026-09-12. Adds all 12 impact-family operations. Total coverage is 279 of 324; the [manifest](openapi-coverage.json) lists 45 remaining operations. No ledger, certificate service or sharing endpoint is implemented.

Source: [contract_impact.py](../../tools/contract_impact.py), [I01–I06 and VD-01–03](../state-machines/proof-and-impact.md), FR-11 and AP-04. Use the [shared reproduction commands](identity-contract.md).

## Original records and effective claims

Record responses separate the original chain entry from the current effective claim projection. The draft immutable payload contains opaque relation/evidence/decision IDs, ledger sequence, entry kind, issued time, attribution revision and a MONEY/ITEM/TIME resource union. It excludes names, phone, exact location and unrestricted narrative. These linkable IDs are not anonymous data; their retention and access remain privacy decisions.

Correction entries require a superseded-entry reference; issuance entries cannot claim one. Responses expose hash-shaped values, but this slice does not choose or implement canonical bytes, genesis, length-prefix encoding, external checkpoints or the append protocol. Example hashes are synthetic format fixtures and are not recomputed integrity evidence. The `impact.v1-draft` schema requires VD-03 review and cross-language vectors before adoption.

Money records state contributed paise, items retain category/unit-specific verified quantities, and time uses integer verified seconds. These resource values do not automatically prove beneficiary attribution. Beneficiary claims retain mission, source decision and observation time and explicitly mean mission-reported counts, not unique people. Null remains distinct from zero.

Summaries derive from current eligible effective records, count supported missions/organizations distinctly and group items by compatible type/unit. They must not multiply the same mission beneficiary report across a donor's repeated contributions. Under-review, withdrawn and corrected claims need the approved VD-02 eligibility rules. A stale rebuild must not overwrite a newer projection revision.

## Corrections and certificates

Correction requests bind both the record version and expected effective version plus source evidence. They do not carry writable totals. Reviewer approval binds a review snapshot and source decision; authenticated reviewer independence is checked server-side. Under ledger-head and effective-version locks, acceptance appends a correction and updates the effective projection and rebuild intent atomically. Original entries remain unchanged. Rejection updates the request history only.

The response contract distinguishes a correction request from its resulting effective entry. The service must ensure APPROVED is not shown before the append/effective update succeeds. Certificate metadata references the current effective entry/version and can become superseded, under review or withdrawn. MVP has no PDF download; `pdf_available` is false. Neither valid JSON nor an issuance-shaped example proves actual verification or final-record availability.

## Conditional sharing

AP-04 remains OPEN. Create/read share operations are explicitly marked disabled by default and include `FEATURE_DISABLED`. This is a specification gate, not runtime enforcement. Revocation remains available to owners if sharing is subsequently disabled.

If approved, creation requires step-up, consent, expiry, exact effective version and a resource-quantity disclosure choice. Public share projection contains no owner ID, chain entries or private evidence IDs. Resource labels must be generated from approved effective claims, not arbitrary contributor text.

The shared-read path authenticates an opaque token rather than a user session. Its token is typed as a bounded base64url string; generation must provide cryptographic entropy and storage must retain only a protected lookup hash. OpenAPI has no path API-key scheme, so `security: []` is accompanied by an explicit path-credential declaration and description. It means no header/cookie credential, not unrestricted access. Every read checks expiry, revocation, consent and current trust. A correction must invalidate or reauthorize a pinned share rather than serving stale claims.

Logs, analytics, browser history/referrers, caching and token-enumeration responses require dedicated privacy/security review. Returned HTTPS URLs need a controlled app host and safe path construction. The schema cannot prove token randomness, revocation or refusal to expose unapproved records.

## Verification and remaining work

The suite validates 279 operations and 3,213 attached examples and rejects 225 negative schema cases plus five query cases. The 16 new failures cover personal fields in immutable payloads, unbound correction entries, invalid sequence/resource combinations, unique-person claims, direct total/original rewrites, PDF claims, share-private fields and missing correction/consent references. Transport checks verify the share token and disabled-by-default declaration.

No hash-chain conformance, PostgreSQL concurrency, issuance atomicity, aggregate rebuild, correction propagation or token authorization has executed. Strict completeness fails with 45 operations untyped. Administration, notifications, realtime, saved methods and web transports remain; P0 is still open.
