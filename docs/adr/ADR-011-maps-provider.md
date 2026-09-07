# ADR-011 — Maps: Google Maps Platform via backend proxy

| Status | Accepted |
|---|---|
| Deciders | Tech lead, designer |
| Related | ADR-006; `02-tdd.md §12` |

## Context
Map surfaces: nearby missions, live tracking with route and ETA, address pin for pickup, organization location. India POI/geocoding quality matters (Delhi addresses are messy). Cost sensitivity: geocoding and directions calls must be cached and proxied to protect keys and enable caching.

## Decision
**Google Maps Platform**: Maps SDK for Android/iOS via `google_maps_flutter` (custom muted style), Geocoding + Places Autocomplete + Directions called **server-side** through `/v1/geo/*` with Redis caching (geocode 24 h, directions 60 s). Mobile holds only the restricted Maps SDK key (bundle-id/package-restricted). ETA computed server-side from Directions on shipment position updates.

## Alternatives
- **Mapbox** — excellent styling and pricing; India address/POI coverage and autocomplete quality weaker in testing; viable fallback.
- **OpenStreetMap tiles + OSRM/Nominatim self-hosted** — free; ops burden; India geocoding quality inconsistent; consider for static/fallback tiles.
- **MapmyIndia (Mappls)** — strong India data; smaller Flutter ecosystem; keep as candidate for NEXT cost review.
- **Apple Maps (MapKit) on iOS** — no Android parity.

## Pros
Best-in-class India geocoding/POI; reliable directions/ETA; familiar UX; solid Flutter plugin.

## Cons
Cost at scale (mitigated by proxy caching, session tokens for autocomplete, rounded coordinates for discovery); vendor lock in styling.

## Risks
Key abuse → restricted keys, server proxy, quotas and alerts on spend.

## Consequences
Map is supplementary: tracking always renders text ETA and timeline; tiles failure → timeline-only layout. Muted map style asset committed to repo.

## Migration path
Geo module abstracts provider; switching geocoding to Mappls or Mapbox is server-side only. Map widget swap is a UI-layer change.
