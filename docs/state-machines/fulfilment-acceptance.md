# Planned fulfilment and integrity checks

**Status:** Not executed. Complements SC/MC/EV catalogues; NK-DOC-3.03. Run API/database/UI and media/restore evidence at the relevant P4–P8 gates.

| ID | Scenario | Required result |
|---|---|---|
| FC-01 | Pickup races cancellation/reassignment. | One accepted version/custody outcome; old volunteer loses current private access. |
| FC-02 | Delayed/rescheduled/issue event after delivery. | Delivery does not regress; report may open a case without changing physical fact. |
| FC-03 | Offline pickup/delivery replay after assignment revoked. | Pending/rejected action honestly shown; evidence can be reviewed by ops; no blind new-version retry. |
| FC-04 | Partial delivery, refused goods or custody handoff. | Actual quantities and current custodian recorded; no full-donation claim on returned goods. |
| FC-05 | Drop-off acknowledged by wrong org or contributor alone. | No accepted receipt or fake volunteer movement. |
| FC-06 | Waitlist offer races direct booking or another offer. | Capacity exclusively reserved once; failed acceptance cannot overbook. |
| FC-07 | Offer accepted after expiry/suspension. | Rejected with reason; reservation released at most once; no contribution created. |
| FC-08 | Reminder provider fails. | Confirmed volunteer can still check in; reminder is not lifecycle prerequisite. |
| FC-09 | Forgotten checkout, geofence exception or no-show corrected. | Evidence/reason and reviewer retained; bounded actual hours, no automatic full-slot credit. |
| FC-10 | Hours verified twice or disputed after record issuance. | One original hours effect; later effective correction updates summary without rewriting record. |
| FC-11 | Upload marked clean but no human proof decision. | No verified badge or final impact; illustration upload cannot become proof. |
| FC-12 | Proof subject belongs to other mission/org. | Subject FK/ownership checks reject; no private signed URL or reviewer data leak. |
| FC-13 | Reviewer verifies old proof revision while rework submitted. | Version conflict; current submission cannot inherit stale approval. |
| FC-14 | Missing geotag/capture timestamp or duplicate image. | Explicit reviewed exception/rework; absent metadata never silently marked valid. |
| FC-15 | Two workers issue same contribution record or different records at same chain head. | One record per contribution, contiguous unique append sequence and correct hashes. |
| FC-16 | Record/correction canonicalization differs between runtimes. | Golden bytes/hashes identical; invalid quantity/time representations rejected. |
| FC-17 | Account deletion or proof redaction then restore from backup. | Reviewed identity/media removal propagates; allowed immutable payload hashes remain valid. |
| FC-18 | Attacker rewrites record and recomputes local chain. | Trusted external checkpoint detects changed prefix; independent trust boundary actually tested. |
| FC-19 | Correction jobs arrive out of order or repeat. | Effective view and summary reflect latest accepted revision without double-counting. |
| FC-20 | Multiple donors/repeated contributions share one beneficiary claim. | No multiplied or globally unique beneficiary claim; unknown remains unknown. |

Attach build/revision, command, fixture/seed, runtime environment and actual output when run. The schema/decision drafts do not pass these gates by themselves.
