# Media and proof typed contracts

**Status:** P0 review draft, 2026-09-12. Adds eight media and 18 proof operations, bringing coverage to 267 of 324 inventory operations. The [manifest](openapi-coverage.json) lists 57 remaining operations. No upload service, media processor or proof-review application exists yet.

Authoring source: [contract_proof.py](../../tools/contract_proof.py). Governing requirements: [VFY01–VFY08](../state-machines/proof-and-impact.md), G21/G24, [authorization](authorization.md) and plan P2/P6. Use the [shared reproduction commands](identity-contract.md).

## Upload, processing and access

Upload authorization binds purpose, subject, declared MIME/size/hash and provenance to a server-owned key and upload session. Clients cannot supply an owner or object key. The 100 MiB schema ceiling is a draft wire bound, not an approved per-purpose upload limit. The service must enforce a measured MIME allowlist and lower purpose-specific limits where appropriate, then inspect actual bytes, hash, dimensions/duration and storage identity at completion. A client completion request cannot assert a clean scan.

Proof-purpose uploads reject an explicit illustration tag. A false tag is not evidence of real capture: provenance, illustration reuse, processed media revisions, consent and review must still be checked on proof submission. Declared MIME is not trusted, and supported video/document formats remain subject to safe processing/preview evidence under P6.

Retry creates a replacement grant only for an eligible unfinished upload, never permission to overwrite frozen evidence. Reprocessing/redaction produces new revisions. Redaction requests bind source revision, case and consent decision; region bounds must also satisfy x+width/y+height within the image, and video frame/range semantics require processor validation. Original immutable proof bytes are not silently rewritten.

Read authorization names an exact revision, rendition and use. Participant evidence requests are restricted to redacted derivatives. The server resolves actual relationship and purpose independently; changing `use` to `review` does not grant reviewer access. Metadata responses exclude raw EXIF and storage keys. Signed URLs require controlled storage hosts, bounded expiry and private cache policy, with response logging redacted. Deletion acknowledgement means pending policy/hold processing, not completed erasure. Already-issued bearer URLs require an explicit expiry/revocation strategy; the JSON response alone cannot revoke them.

## Proof revisions and human review

Drafts identify a typed subject whose mission relation is resolved by the server. Evidence references bind media and consent revisions. Claims distinguish actual quantities from sourced mission-reported beneficiary counts; they do not claim unique people or automatically attribute all beneficiaries to each donor. Required quantities, units, consent, acknowledgements and metadata exceptions must be validated before freezing a submission.

Submission identifies the draft version and requirements revision. Delegated ops require an on-behalf reason enforced by authenticated role context. Submitted revisions cannot be edited through draft routes. Resubmission preserves the prior decision and freezes a new draft revision; deletion only applies to eligible unsubmitted drafts.

The server selects separate submitter and participant views. Participants receive approved derivative references, not original media, claims or reviewer notes merely because they belong to a mission. Derivative IDs still require current media authorization. Scoped reviewers receive separate restricted review data. Automatic hash/location/processing checks remain signals, not human verification.

VERIFY decisions require passing or approved-exception checklist entries, accepted claim revision and disclosure decision. The disclosure decision may deny publication; proof verification does not make private evidence public. Reviewer independence, complete requirements, provenance and actual outcomes remain service checks. Verification emits an issuance intent; it does not claim the final impact record already exists. Appeals and challenges open cases without rewriting historical verification, and accepted appeal review preserves previous decisions.

## Verification and remaining evidence

The shared suite validates 267 operations and 3,090 request/response/error examples, rejecting 209 negative schema cases and five query cases. This slice adds 22 failures covering owner/key injection, invalid upload metadata, client scan claims, raw metadata exposure, arbitrary URL input, illustration-tagged proof, original-media requests from participants, proof-status injection, private participant fields and missing frozen claims/disclosure revisions.

No malicious file, storage policy, scan/transcode, signed-URL expiry, role isolation, actual human review or immutable-record issuance was executed. VD/privacy decisions, purpose/MIME limits, provider compatibility and runtime tests remain open. Strict completeness fails with 57 operations untyped. Impact and remaining administrative/transport contracts follow; P0 is not complete.
