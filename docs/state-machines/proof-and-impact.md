# Proof review and immutable impact

**Status:** P0 review draft, NK-DOC-3.03. Sources: PRD FR-11/17, TDD §6.6, model §4.7/4.8, plan G17–G24 and P6. [Shared rules](README.md) apply to every row. This draft does not approve retention/attribution policy or change the current schema.

## Proof submission and review

Media processing and proof verification are separate. A clean file is not verified proof. A proof submission freezes references to immutable processed media revisions, subject/mission linkage, consent and claim versions. Polymorphic subjects require explicit valid foreign-key relations or a validated subject registry, not arbitrary IDs plus a mission supplied by the client. Submitters/participants see only their scoped projections; home imagery requires redacted derivatives and purpose-based access (G24).

| ID | Command: prior → result | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failure / decision |
|---|---|---|---|---|---|---|
| VFY01 | Submit: absent → NOT_REVIEWED | Scoped org/volunteer, or ops on behalf with reason | Subject eligible, processed/scanned media, correct ownership/relations, non-illustration provenance, required consent; metadata exceptions explicit | Freeze submission/evidence revision, queue review; `ProofSubmitted.v1` | “Proof submitted”; submitter + review queue | `PROOF_NOT_READY`, `SUBJECT_SCOPE_DENIED`; VD-01 |
| VFY02 | Start: NOT_REVIEWED → UNDER_REVIEW | Scoped reviewer | Current submission revision, authorized evidence access, reviewer assignment | Review-start history; `ProofReviewStarted.v1` | “Under review”; submitter status | `REVIEW_REVISION_CHANGED` |
| VFY03 | Request info: UNDER_REVIEW → NEEDS_MORE_INFORMATION | Scoped reviewer | Checklist findings and safe requested evidence | Append decision, preserve submission; `ProofInformationRequested.v1` | “More information needed”; submitter request, contributor generic pending status | `REVIEW_REASON_REQUIRED` |
| VFY04 | Resubmit: NEEDS_MORE_INFORMATION → UNDER_REVIEW | Scoped submitter | Requested evidence complete, new processed revisions and consent, prior decision reference | New immutable submission cycle; `ProofResubmitted.v1` | “Updated proof under review”; submitter + reviewer queue | `REQUESTED_INFORMATION_MISSING` |
| VFY05 | Verify: UNDER_REVIEW → VERIFIED | Scoped authorized human reviewer | Accepted checklist/metadata exceptions, actual quantities and beneficiary claim provenance; current revision | Append verification, emit causal completion intent; `ProofVerified.v1` | “Proof verified”; submitter; owner final notification only after record issuance | `PROOF_CHECKS_INCOMPLETE`; VD-01/02 |
| VFY06 | Reject: UNDER_REVIEW → REJECTED | Scoped reviewer | Evidence/reason, safe explanation and appeal policy | Preserve rejected evidence; mission dispute/rework intent under PD-10; `ProofRejected.v1` | Submitter rejection/recovery; contributor safe review status | `REVIEW_REASON_REQUIRED`; PD-10 |
| VFY07 | Reopen appeal: REJECTED → UNDER_REVIEW | Scoped independent ops reviewer | Accepted appeal evidence and policy, no overwrite of old decision | New review cycle; `ProofAppealOpened.v1` | “Proof appeal under review”; submitter + review queue | `APPEAL_NOT_ALLOWED`; VD-01 |
| VFY08 | Challenge verified proof: VERIFIED → VERIFIED | Scoped case reporter/reviewer | Case evidence; historical verification stays recorded | Open case/current trust projection, pause dependent unissued records as policy requires; `VerifiedProofChallenged.v1` | “Outcome under review” if case accepted; relevant parties | `CHALLENGE_SCOPE_DENIED`; VD-02 |

EXPIRED in the shared verification enum applies to time-limited org credentials, not automatic expiry of historical delivered evidence. Do not expire completed proof merely because media access URLs expired. Retention, revocation/redaction and proof challenges use separate records. Automatic hash/GPS checks cannot substitute for human trust decisions or prove beneficiary uniqueness.

## Impact issue/correction commands

| ID | Command: prior → result | Actor | Guards/evidence | Atomic effects; proposed event | Copy; notification | Additional failure / decision |
|---|---|---|---|---|---|---|
| I01 | Issue: no final record → issued | Impact service | Contribution VERIFIED, required mission/outcome decisions, accepted quantities/attribution, no unresolved blocking case; unique contribution key | Under chain-head + contribution locks append record/entry and C22 completion, owner projection, outbox atomically; `ImpactRecordCreated.v1` | “Your verified impact record is ready”; owner | `IMPACT_EVIDENCE_INCOMPLETE`; VD-02/03 |
| I02 | Request correction: issued → issued + request | Scoped owner/org/ops | Reason and supporting evidence, current effective revision | Correction request only; no public change; `ImpactCorrectionRequested.v1` | “Correction requested”; requester + review queue | `CORRECTION_SCOPE_DENIED` |
| I03 | Accept correction: issued revision → next effective revision | Scoped independent reviewer + impact service | Accepted source decision, allowed field/claim, expected record effective version, full before/after provenance | Append correction chain entry + effective view update + summary rebuild intent; original record unchanged; `ImpactRecordCorrected.v1` | “Impact record updated” with safe history; owner + affected org | `CORRECTION_CONFLICT`; VD-02/03 |
| I04 | Reject correction: pending request → rejected | Scoped reviewer | Reviewed evidence and safe reason | Request decision history only; `ImpactCorrectionRejected.v1` | “Correction request reviewed”; requester | `REVIEW_REASON_REQUIRED` |
| I05 | Anonymize projection: linked owner → anonymized | Privacy service following authorized policy | Approved deletion case, data-class policy/holds; stop access first as required | Remove/restrict mutable identity references and personal derivatives under retention workflow; immutable payload bytes unchanged; `ImpactIdentityAnonymized.v1` | Deletion-case status to authorized requester | `RETENTION_DECISION_REQUIRED`; G21/VD-03 |
| I06 | Checkpoint: uncheckpointed prefix → attested prefix | Integrity service | Recomputed contiguous head/sequence verified | Record external signed checkpoint receipt in separate store; `ImpactCheckpointRecorded.v1` | Ops integrity status only | `LEDGER_INTEGRITY_MISMATCH`; VD-03 |

I01 can be retried after commit/response loss: unique contribution + stored issuance result returns existing record, no second chain entry. A later mission or payment dispute does not delete the record; I03 must correct the effective trust/outcome claims. C22 and I01 are one issuance transaction, not two independent state mutations. If architecture separates them later, the completion/read-copy contract must be amended to avoid a completed contribution without its record.

## Canonical payload proposal

Use a versioned schema and deterministic JSON canonicalization. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) defines JSON canonicalization rules; library conformance and cross-language golden vectors must be tested before adoption. Represent quantities as normalized decimal strings and money/time as bounded integers or normalized integer strings under the schema; no uncontrolled binary floats, NaN or mixed representations. Fix timestamps to UTC schema format and distinguish absent versus null explicitly.

Proposed immutable payload contains opaque record/mission/org/evidence revision IDs, contribution type, actual resource quantities/units, verification-decision IDs, timestamps and attribution schema/version. Exclude names, phone, email, exact location, unrestricted narrative and mutable identity links. Opaque IDs can still be personal data when linkable: the privacy owner must review retention/pseudonymization, not call the chain anonymous by default. Store owner membership, display names, public copy and redacted proof access in separately authorized mutable projections.

Proposed entry hash: `SHA256(domain_separator || length_prefixed(canonical_payload_bytes) || previous_hash_bytes)`. Envelope includes ledger ID, sequence, entry kind, record ID and schema version within canonical bytes. Specify genesis value, byte encoding and length prefix in the schema spike; do not hash the mutable database row. Record and correction entries share the same append protocol so corrections cannot silently bypass integrity. A head row is locked per ledger, sequence allocated transactionally, and `(ledger_id, sequence)` is unique. No timestamps as append-order keys.

This detects changes against a trusted checkpoint; a database attacker who can rewrite the entire chain can recompute hashes. External checkpoints therefore need a separate controlled trust boundary, key rotation and restore checks, not a second table with identical credentials.

## Attribution and summary proposal

Count supported missions and orgs distinctly per owner across eligible verified records, and sum actual verified service quantities only once. Do not sum item units across incompatible categories. Beneficiaries are verified mission-reported counts with source/date and wording; do not multiply one mission claim for repeated contributions, claim globally unique people, or attribute every mission beneficiary as personally delivered by each donor. Missing values remain unknown, including zero versus absent. VD-02 must approve exact display and aggregation rules.

Materializations rebuild from current effective verified records and accepted corrections, replacing totals rather than blindly adding deltas twice. Rebuilds are versioned; a late job cannot overwrite a newer correction. Certificate metadata references effective verification; no MVP PDF download. Redaction/removal must propagate to cached views, signed-access grants and restored backups under the approved privacy workflow while preserving only what the retention policy allows.

| Decision | Review required | Owner |
|---|---|---|
| VD-01 | Required proof by purpose, acceptable missing metadata, redaction, reviewer independence and appeals. | Ops + privacy/product |
| VD-02 | Beneficiary attribution, claim revocation, completed-record challenge, correction and dependent issuance rules. | Product + ops |
| VD-03 | Canonical schema/hash byte format, checkpoint trust/key boundary, privacy data classes and deletion-compatible references. | Backend + security/privacy |

All decisions OPEN; schema reconciliation, canonicalization vectors, real DB concurrency and privacy/restore drills remain required.
