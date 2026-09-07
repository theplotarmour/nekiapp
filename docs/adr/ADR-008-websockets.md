# ADR-008 — Realtime: WebSockets with versioned events and polling fallback

| Status | Accepted |
|---|---|
| Deciders | Tech lead, Flutter lead |
| Related | ADR-007, ADR-014; `02-tdd.md §9`, `03-user-flows.md F5` |

## Context
Tracking is a first-class experience: contributors must see shipment state and volunteer position within ~3 s; contribution status must flip from Confirming to Success without refresh. Volunteers push pings every 10 s while foregrounded. Mobile networks drop; clients miss events; server must remain authoritative.

## Decision
Single **WSS** connection per app session at `/v1/ws`, short-lived token in query, multiplexed channels (`contribution:{id}`, `mission:{id}`, `user:{id}`), server events `{type, version, data, sent_at}`, per-channel monotonically increasing `version`. Client detects gaps → fetches REST snapshot. Fan-out via Redis pub/sub. Heartbeat 25 s / idle close 60 s. Reconnect with jittered exponential backoff 1→30 s; after 3 failures switch to polling `GET …/tracking` every 15 s while screen visible. Volunteer pings are HTTP batches (not WS) for simplicity and retry semantics.

## Alternatives
- **Server-Sent Events** — one-directional, fine for tracking, but Flutter support weaker and no multiplexing standard; would still need HTTP for pings. Marginal gain.
- **FCM data messages only** — 1–10 s+ latency, throttling, unreliable for live ETA.
- **Polling only** — simple but 15 s staleness and battery/network cost; kept as fallback.
- **Third-party realtime (Ably/Pusher/Supabase Realtime)** — faster to ship; adds vendor, cost per connection, and a second auth model. Revisit if WS ops burden grows.
- **MQTT** — good for devices; overkill for app-to-server here.

## Pros
Low latency; bidirectional (ping/pong, subscribe/unsubscribe); works behind Cloudflare; cheap at MVP connection counts (< 5k concurrent).

## Cons
Stateful connections complicate deploys (drain on shutdown); mobile background kills sockets (handled by reconnect + polling); load balancer idle timeouts (configure ≥ 60 s).

## Risks
Event ordering across replicas → `version` assigned in the DB transaction (shipment.version increment), never by the WS server.

## Consequences
UI shows Connecting / Live / Reconnecting / Last updated. Server never assumes delivery. Load test target 5k concurrent sockets per replica.

## Migration path
Swap Redis pub/sub for Streams or managed realtime without changing client protocol.
