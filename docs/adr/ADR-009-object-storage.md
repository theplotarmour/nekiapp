# ADR-009 — Media: Cloudflare R2 with presigned uploads and CDN

| Status | Accepted |
|---|---|
| Deciders | Tech lead |
| Related | ADR-018; `02-tdd.md §11`, `05-data-model.md §8` |

## Context
Mission images (public, cacheable), proof photos/videos (private, signed, 7-year retention, tamper evidence), item photos, org documents, avatars, certificates. Uploads from mobile on flaky networks. Never store blobs in Postgres. Must strip EXIF for privacy but retain capture time/GPS as proof metadata.

## Decision
**Cloudflare R2** (S3-compatible) behind Cloudflare CDN for `public/`; `private/` served via short-lived signed URLs (1 h). Client requests `POST /media/upload-url` → presigned PUT (15 min, content-type and size constrained) → `POST /media/{id}/complete` → worker pipeline (magic-byte validation, ClamAV, EXIF extraction+strip, WebP variants 200/800/1600, BlurHash, sha256 + perceptual hash). Object versioning on `private/proofs`.

## Alternatives
- **AWS S3 + CloudFront** — equivalent; R2 has zero egress fees (media-heavy app) and one vendor with WAF/CDN/Workers. If hosting lands on AWS ECS (ADR-018), S3 in ap-south-1 becomes acceptable; keep code S3-API generic.
- **Upload through API** — doubles bandwidth on API, blocks workers; rejected.
- **Cloudinary/imgix** — great transforms; per-asset pricing scales poorly with proof volume; privacy controls less granular.
- **Firebase Storage** — ties to Firebase auth model; weaker lifecycle/versioning.

## Pros
Zero egress; S3 API portability; Workers for OG share pages; per-prefix lifecycle rules; versioning for evidence integrity.

## Cons
R2 lacks some S3 features (Object Lock at time of writing) → tamper evidence via hash chain in `impact_records` and versioning rather than WORM.

## Risks
Signed URL leakage → 1 h TTL, bound to variant path; proof access audited.

## Consequences
Media table stores variants and hashes; `is_illustration` flag blocks AI/marketing imagery from proof purpose; proof watermark applied in-app, original untouched.

## Migration path
Bucket sync to S3/GCS is a `rclone` job; code uses S3 SDK with endpoint config.
