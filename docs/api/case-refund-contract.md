# Cases, disputes and refunds typed contract

**Status:** P0 review draft, 2026-09-11. All 17 inventory operations in the cases family now have typed request/response/error contracts. Total coverage is 150 of 324 operations. This is contract coverage, not implemented support or payment functionality. The [manifest](openapi-coverage.json) lists the remaining 174 operations.

Authoring source: [contract_cases.py](../../tools/contract_cases.py). Use the [shared reproduction commands](identity-contract.md). Governing sources are [refund transitions R01–R08](../state-machines/payments-and-payouts.md), [money invariants](../state-machines/money-invariants.md), [PD-11](../state-machines/review-decisions.md) and the [authorization matrix](authorization.md).

## Case and dispute boundaries

Case creation identifies a contribution, payment, shipment, assignment, mission or the current account. Ownership comes from authentication, never a request field. The service must verify the caller's relationship to the subject; knowing a public mission ID does not authorize access to its other participants. Draft categories and OPEN/UNDER_REVIEW/AWAITING_INFORMATION/RESOLVED/CLOSED statuses require Product/Ops review; they are proposed taxonomy, not approved persistence enums.

Requester messages cannot select a support author or internal visibility. Evidence attachments require owned, processed media and return `accepted_as_proof=false`; attachment is not verification. Owner views and paginated history exclude restricted notes. Scoped reviewer views are separate schemas. History contents, free-text redaction, media access and participant isolation still require runtime checks.

Ops-lead dispute decisions explicitly request information, request rework, refer recovery or close with a policy decision. Evidence and the relevant plan reference are mandatory. These decisions record case outcomes and durable follow-up intent; they cannot directly issue a refund, mark a payout paid or rewrite final impact. Mission transitions remain separate versioned domain commands. PD-11 must approve the allowed dispositions and closure conditions before implementation.

Provider-dispute evidence attachment records a review package and returns `submitted_to_provider=false`. It is not an external submission endpoint. Provider submission requires reviewed consent, evidence scope/redaction and a separately specified provider workflow. The schema's consent ID does not prove consent is current or sufficient.

## Refund commands and projections

Refund requests identify a captured payment via the path, its expected version, a case, a positive INR amount, evidence and an approved funding plan. The service must lock payment/refund balances and funding sources, validate availability and reserve the requested amount atomically. Duplicate commands replay the original result. Proposed reason-code and funding-plan vocabularies remain subject to FD-02/03.

Approval binds an immutable approval snapshot and expected refund version with step-up. That snapshot must identify the exact amount, funding sources, provider request body and stable idempotency key. Approval cannot patch an amount or recipient. Cancellation is only allowed before invocation, serialized against the worker; timeout, missing response or an uncertain provider result cannot justify releasing funds.

Owner refund responses expose safe reasons and authoritative processing references, without funding plans, internal notes or provider credentials. PROCESSED requires a processing timestamp and provider reference; other states cannot claim a processing timestamp. The service must independently verify provider identity, amount and evidence. A reference string alone proves nothing, and processed does not guarantee a bank-arrival date.

Finance responses retain funding reservations, invocation state, approval snapshot and reconciliation linkage. UNCERTAIN keeps its funding hold; the example demonstrates that shape but does not prove a balance invariant. A late authoritative processed fact after an apparent failure must be recorded with reconciliation, rather than discarded to preserve a prior status. Partial refunds do not erase capture or delivery history.

## Verification and remaining evidence

OpenAPI and attached examples pass for 150 operations and 1,625 request/response/error examples. The validator rejects 105 negative schema cases and five query cases. This slice adds 23 failures covering owner/status injection, support impersonation, private Finance fields, unsupported amounts/currency, missing funding and approval references, premature processed claims, forced cancellation and false provider-submission claims.

Strict completeness still fails with 174 operations untyped. No database reservation, worker race, authorization, provider refund or external evidence submission has run. Finance approval policies, immutable snapshot modeling, exact transition errors/events, provider sandbox probes and P0 owner/legal gates remain open. Payout and provider transport contracts are next.
