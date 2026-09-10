# Request, response and error profiles

**Status:** Review draft. All operation inventory rows inherit a profile below plus their route policy and domain command guards. Requests use `/v1`, JSON snake_case, UTC timestamps, INR integer paise and typed IDs. Web public fallback and WebSocket frames have separate transport contracts. Source conflicts require AP-01 reconciliation before implementation.

## Profiles

| Profile | Success / input behavior | Idempotency / concurrency | Rate-limit class |
|---|---|---|---|
| read | 200 typed resource; 404 if unavailable in scope | Safe read; ETag only with authorized projection/version | public_read or private_read by policy |
| list | 200 `{items,next_cursor,has_more}`; cursor + bounded limit | Cursor bound to owner/projection/filter/sort; stable sort tie-breaker; no cross-user cursor reuse | public_read or private_read |
| query | 200 typed scoped query/access result via POST to avoid sensitive URL parameters | No expected aggregate version for read-only queries; reauthorize every call, audit restricted access; no business lifecycle mutation | private_read; separate geo/media quotas |
| create | 201 typed created resource + version | Idempotency-Key required; same hash replays; create uniqueness authoritative | write |
| update | 200 updated typed resource + version | Expected version and Idempotency-Key; reject stale write | write |
| command | 200 committed result or 202 durable job when asynchronous, explicitly fixed per final schema | Expected version + Idempotency-Key + reason/evidence for reviewed transition | write; sensitive_write by policy |
| delete | 204 logical removal or 202 tracked retention job as finalized per route | Idempotency-Key and expected version; never silently remove immutable history | write |
| auth | 200 challenge/session-specific response | OTP request/verify, refresh/reuse semantics separate; no generic response cache with live credentials | auth_challenge |
| upload | 201 purpose-bound upload authorization | Idempotency-Key; server key/content type/size/expiry, complete validates actual bytes | media_write |
| provider | 2xx only after validated durable receipt or known duplicate | Raw-body signature, account/environment, unique provider event identity; no browser CSRF exemptions beyond this route | provider_ingress |
| ping | 202 bounded accepted location batch | Current assignment revision, sequence/batch identity, timestamp/accuracy bounds; only active foreground scope | location_write |
| ticket | 201 short-lived connection ticket | Authenticated POST; no refresh-token leakage; connection ticket single-use | socket_ticket |
| socket | Upgrade + typed subscribe/unsubscribe/ping/resync frames | Per-channel current scope; monotonic versions and snapshot gap recovery | socket_frames |
| page | 200 safe HTML/share metadata, or typed JSON app-association document; 404 when absent | Public cache only after privacy/visibility checks; no private owner data | public_read |

`command` and `delete` allow two outcomes during inventory drafting only: OpenAPI must pin each route's synchronous/asynchronous success responses and typed result before gate passage. Optional query/body fields and exact schemas are not inferred from path names.

Default list proposal: limit 20, maximum 50, preserving TDD. Invalid/tampered/mismatched cursor returns `400 CURSOR_INVALID`; expired cursor returns `410 CURSOR_EXPIRED` with restart guidance. Cursor encoding is opaque integrity-protected data, not permission. Private responses use `Cache-Control: private, no-store` unless a documented owner-scoped cache is justified.

## Common error envelope

```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "This item changed. Refresh before trying again.",
    "request_id": "req_example",
    "details": {"current_version": 4},
    "retryable": false
  }
}
```

Details are typed/allowlisted per error and projection; never return hidden owner IDs, raw provider payloads or internal stack traces. Conflict response can include the safe current resource only after authorization. Domain codes from transition drafts must be enumerated per operation during schema authoring; generic 500 is not a substitute.

| HTTP | Code / meaning | Client action |
|---|---|---|
| 400 | `REQUEST_INVALID`, `CURSOR_INVALID` | Correct input; no state mutation. |
| 401 | `AUTH_REQUIRED`, `SESSION_EXPIRED` | Authenticate or authorized refresh once; do not replay sensitive writes with changed body. |
| 403 | `ACTION_FORBIDDEN`, `STEP_UP_REQUIRED`, `VOLUNTEER_INELIGIBLE` | Explain authorized safe reason and eligibility/re-auth path. |
| 404 | `NOT_FOUND` | Resource absent or outside owner visibility; don't leak existence. |
| 409 | `VERSION_CONFLICT`, `IDEMPOTENCY_KEY_REUSED`, state/capacity/allocation conflicts | Refresh/review; never silently increment expected_version on an old field action. |
| 410 | `CURSOR_EXPIRED`, `SHARE_REVOKED` where safe to disclose | Restart list or stop share access. |
| 413 / 415 | `PAYLOAD_TOO_LARGE`, `MEDIA_TYPE_UNSUPPORTED` | Correct upload; no processing/verified claim. |
| 422 | `EVIDENCE_REQUIRED`, amount/consent/semantic validation | Correct required fields/evidence. |
| 429 | `RATE_LIMITED` | Honor Retry-After; retained logical command identity for safe retry. |
| 503 | `DEPENDENCY_UNAVAILABLE` | Follow retry guidance; accepted uncertain external requests remain 202 operation state, not false failed money. |

TDD currently uses 422 `IDEMPOTENCY_MISMATCH`; draft transition catalogue uses 409 `IDEMPOTENCY_KEY_REUSED`. AP-01 proposes the latter consistently before any endpoint ships. In-flight duplicate proposal: 409 `REQUEST_IN_PROGRESS` + Retry-After or stored 202 operation link; choose one per command schema. Completed result retention is distinct from permanent domain/provider dedupe; the source 24-hour cache is not permission to duplicate a payout after expiry.

## Rate-limit review baseline

Preserve TDD's proposed anonymous 60/min/IP, authenticated 300/min/user, and OTP 3/10min/phone + 10/hour/IP as source assumptions to spike; not validated production limits. Separate high-cost geocoding, upload, location batching, sensitive mutations, exports and connection/frame limits. Rate state must not create cross-tenant information leaks. Provider ingress needs signature and durable abuse controls; IP filtering alone cannot authenticate a webhook. AP-03 finalizes limits and retry policies after compatibility/load tests.

Sensitive mutations require server reauthentication bound to action/resource, exact approved financial revision and expiry. Web cookie requests need reviewed CSRF/origin/CORS protection; mobile secure-storage tokens follow the same server action authorization. Step-up is not a user-provided boolean.
