# ADR-006 — Geospatial: PostGIS geography with GiST indexes

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-005, ADR-011 |

## Context
Nearby missions (radius 10/25/50 km), distance in ranking, service-area serviceability for pickups (polygons), geofenced volunteer check-in (300 m), volunteer ping storage, mission clustering on maps.

## Decision
Store points as `geography(Point,4326)`; service areas as `geography(MultiPolygon,4326)`; GiST indexes; `ST_DWithin` for radius filters; `ST_Distance` for ranking; `ST_Covers` for serviceability. Rounded points for user home location; precise only on addresses and proof metadata.

## Alternatives
- **Haversine in SQL/app without index** — full scans; unacceptable past a few thousand missions.
- **Geohash/H3 cells in plain Postgres** — fast approximate filtering; loses polygon coverage and accurate distance; could complement later for caching keys.
- **External geo service (Elasticsearch geo, Redis GEO)** — extra infra; Redis GEO lacks polygons.

## Pros
One database; correct spherical distances; polygon operations; mature.

## Cons
PostGIS on managed providers requires the extension available (Neon/RDS both support). Slight learning curve.

## Risks
Location privacy: precise coordinates must never leak into public payloads → serializers round to 3 dp for tracking, 2 dp for discovery; tests assert.

## Consequences
Feed query: `WHERE ST_DWithin(location_point, :user, :radius_m)` with partial index on live statuses. Ping partitions monthly; drop after 30 d.

## Migration path
If map-tile-scale queries needed (heatmaps), add H3 aggregation tables; PostGIS remains source of truth.
