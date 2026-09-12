# Realtime WebSocket transport

**Status:** P0 review draft, 2026-09-12. [realtime.json](realtime.json) specifies the `connect_realtime` inventory operation separately from OpenAPI. It is a custom `neki-transport-contract.v1` document with JSON Schema message definitions, not an AsyncAPI document or implemented service. Coverage is 315 JSON HTTP operations plus one WebSocket transport; eight public-web operations remain.

Authoring source: [contract_realtime.py](../../tools/contract_realtime.py). The shared builder generates the document and coverage mapping. [validate_realtime.py](../../tools/validate_realtime.py) checks the inventory mapping, schema validity, examples and negative cases. The main OpenAPI validator invokes this transport validator as well, while keeping HTTP and transport counts distinct.

## Handshake and authorization

The proposed endpoint is `/ws` with `neki.realtime.v1` subprotocol and a required single-use ticket query parameter. Obtain the ticket through the authenticated HTTP ticket operation. Atomically consume it against current session, device, expiry and authorized channels before upgrading. A failed upgrade after consumption requires a new ticket. Header/query tokens must be redacted from logs, traces and diagnostics.

Browser Origin must match an exact configured allowlist. Absence of Origin is permitted only for a ticket bound to an approved native-client session; absence alone cannot bypass the browser rule. Authentication failures, access denial, limits and unavailable ticket storage have distinct documented handshake responses. Actual upgrade headers and WebSocket protocol handling must be delegated to a tested server implementation.

Subscriptions are restricted to the ticket's explicit channel set and current subject authorization. The own-notifications channel derives its owner from the session. Recheck access before each emission; session, assignment, consent or capability revocation closes the relevant access. An issuance-time role check is insufficient. The protocol has no wildcard, caller-selected owner or client business-mutation frame.

## Frames and reconnect

Client frames subscribe, unsubscribe or ping. Server frames acknowledge readiness/subscription, signal a versioned change, request resynchronization, pong or return a safe protocol error. Frames contain IDs and aggregate versions, not raw GPS, pickup addresses, private proof, bank facts or arbitrary business payloads. They are invalidation hints; authenticated HTTP reads provide authoritative snapshots.

Connection-local sequence numbers cover all server frames and restart with a new connection. They are not durable event cursors or database ordering keys. Every new connection restores snapshots. Subscribe first and buffer hints during the snapshot fetch, then reconcile aggregate versions; otherwise an update between fetch and subscription could be lost. Discard stale versions. Sequence gaps, source restarts and bounded-buffer overflow require snapshot refresh or reconnection, never fabricated continuity.

Frame size, subscription count, idle/expiry and backpressure policies require load/mobile review. The 16 KiB frame and 20-subscription limits are proposed bounds. Binary application frames are rejected. Protocol/access violations, oversized frames and server failure have documented close behavior. Transport ping/pong and fragmentation handling remain the server library's responsibility; application pings do not replace WebSocket control frames.

## Verification and outstanding work

Run `.venv-contracts/Scripts/python tools/validate_realtime.py` or the shared OpenAPI validator. Eleven handshake/frame examples pass; nine negative cases reject token fallback, wildcard channels, owner injection, business commands, private payloads, invalid sequence/version and secret/error-stack leakage.

These are schema checks, not a network or client state-machine test. Atomic ticket races, exact-origin checks, revocation, subscription/snapshot buffering, missed events, Redis restart, slow consumers and mobile reconnect must be verified against the eventual service. Schema success cannot close EV-12, AP-02 or P5. Strict inventory completeness remains incomplete for eight web transports, and P0 remains open.
