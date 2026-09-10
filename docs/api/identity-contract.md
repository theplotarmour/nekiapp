# Typed identity contract and validation evidence

**Status:** Partial P0 contract, 2026-09-10. Covers the 25 identity/preference operations in `operations.tsv`; 299 other operations remain untyped. No running backend, mobile/web client or provider integration is claimed.

## Artifacts and authoring workflow

- [openapi.json](openapi.json): generated OpenAPI 3.1.1 with closed typed request/response schemas, operation-specific error code enums, examples, parameters and policy/effect references.
- [openapi-coverage.json](openapi-coverage.json): exact covered and remaining operation IDs, including non-HTTP transport work. Missing routes are not generated with placeholder responses.
- [contract_identity.py](../../tools/contract_identity.py): current reviewed-draft schema/example/operation definitions.
- [build_openapi.py](../../tools/build_openapi.py): deterministic assembly from explicit definitions and inventory metadata; `--check` rejects artifact drift.
- [validate_openapi.py](../../tools/validate_openapi.py): OpenAPI validation, JSON Schema/format validation for every attached example, negative schema cases and coverage partition checks. `--require-complete` deliberately fails until all required contracts exist.

This is the contract-first P0 draft workflow from plan §5.2. Until P1, edit the explicit authoring module and regenerate; do not hand-edit generated JSON. Once implemented and reconciled, reviewed FastAPI export becomes canonical and these authoring modules are retired or replaced with export checks. Never maintain two independent manually authored contracts.

Primary format references inspected: [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) and [JSON Schema validation 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation). These define document/schema formats, not proof of NEKI behavior.

## Session transport and security obligations

- Mobile and browser session responses are disjoint (`client_kind`). Mobile may receive refresh token for secure platform storage. Browser JSON rejects a refresh-token field; web access token is held in memory and refresh uses a Secure HttpOnly cookie.
- Web session creation/rotation additionally provides a separate signed, session-bound CSRF cookie readable by the first-party client. Refresh requires matching CSRF header, valid refresh cookie and allowed origin. Cookie settings are specified in response header descriptions; repeated Set-Cookie semantics are not captured as one JSON string.
- OpenAPI cannot conditionally require a cookie/header from a body discriminator alone in this draft. `/auth/refresh` has no bearer requirement because mobile authenticates with the body refresh credential. This does **not** mean anonymous refresh: each transport must authenticate its bound credential. The server must reject mixed transports, missing web cookie/CSRF, wrong origin and mismatched device/session binding. Schema-only tests cannot establish those controls.
- Preserve ADR-012 source timeouts: six-digit OTP, five-minute lifetime, five attempts then 15-minute lockout; access 15 minutes, rotating refresh 30 days. Server returns expiry timestamps; client timers do not grant authorization. Challenge response never confirms whether an account exists.
- Consuming an OTP and issuing the session, rotating a refresh family, detecting token reuse, revoking a session and consuming a step-up grant need transactional runtime tests. Generic idempotency response caching must not expose/reissue old refresh credentials. Failed network responses require a documented auth retry/recovery design, not blind token reuse exceptions.
- Step-up binds current principal/session/action/resource/version and expires. Requesting a challenge does not grant the target action. Local biometrics are not a server proof. Revocation/deletion/cancellation require current scoped grant; role or bank grants are not created by profile fields.
- Removing a device disables delivery registration; it does not imply session logout. Explicit session revoke/logout handles credentials. Device identifiers are correlation/binding inputs, never authentication factors by themselves.

## Schema choices and remaining decisions

Object schemas reject unrecognized properties. Profile mutation cannot set phone, roles, approvals or provider fields. Notification categories require one entry each; version fields are nonnegative integers. Null and absent are distinct; avatar null clears the reference, omitted patch fields remain unchanged. Consent acceptance is true-only and timestamped by the server; historical consent is append-only. Selecting a discovery locality cannot set pickup serviceability.

String length caps, notification category taxonomy, deletion-status vocabulary, locale restriction, supported step-up action names and location-by-locality encoding are explicit **proposals** needing AP-01/AP-02/API review and source reconciliation. No numeric cap here is represented as an independently tested product policy. Server-side semantic checks still need whitespace normalization, challenge/device binding, duplicate command identity, media purpose/ownership, consent version currency and deletion cancellation cutoff. The schema is not sufficient to implement those safely on its own.

## Reproduce

On Windows PowerShell, from repository root:

```powershell
python -m venv .venv-contracts
.venv-contracts/Scripts/python -m pip install -r tools/requirements-contracts-lock.txt
.venv-contracts/Scripts/python tools/check_api_inventory.py
.venv-contracts/Scripts/python tools/build_openapi.py --check
.venv-contracts/Scripts/python tools/validate_openapi.py
```

To intentionally regenerate, run `tools/build_openapi.py` without `--check`. `requirements-contracts.txt` contains direct tooling pins; the lock records the resolved validation environment. These dependencies are not application runtime selections.

Observed checks: 25 typed operations, 263 attached request/response/error examples accepted, 23 invalid schema cases rejected, coverage partition matches the 324-operation inventory. Strict completeness correctly remains failing. No provider, database, browser, session reuse or runtime authorization tests were executed.
