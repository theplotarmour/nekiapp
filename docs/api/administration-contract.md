# Administration and recovery contracts

**Status:** P0 review draft, 2026-09-12. Adds 30 administration operations, bringing typed coverage to 309 of 324. The [manifest](openapi-coverage.json) identifies 15 remaining operations. Existing domain moderation operations remain in their respective modules. No administrative service is implemented.

Source: [contract_admin.py](../../tools/contract_admin.py), [authorization matrix](authorization.md), [event recovery](../state-machines/events-and-recovery.md), G25/G29 and FR-16. Use the [shared reproduction commands](identity-contract.md).

## Access and operations

Public liveness reveals only that the process is alive. Sanitized dependency/queue health is restricted to operations and is not an enterprise-readiness claim. User search/detail is scoped to permitted support work and excludes credentials and raw contact information. Suspension/reinstatement bind case and policy decisions; reinstatement cannot replace volunteer, organization or Finance approval requirements.

Role grants specify a target user, reviewed role, explicit organization/queue/platform scope, authorization decision and expiry. Platform scope requires an additional approval reference. The role taxonomy is a draft allowlist requiring G25 review; it is not a complete role-to-capability implementation. The server must prohibit self-escalation, validate delegation boundaries and role/scope combinations, enforce approver independence where required and propagate revocation. Neither a target user ID nor an approval-shaped request grants authority by itself. Domain approval roles must still obey their organization/volunteer lifecycle prerequisites.

Fraud signals remain evidence for review, not automatic misconduct findings. Decisions dismiss or refer a case; they cannot directly suspend users or move funds. Audit reads expose sanitized metadata rather than raw request bodies or credentials. Audit actor/service-principal identities and retention require canonical model reconciliation; no audit mutation route is introduced.

## Support, reports and exports

Support actions validate current agent/queue capability and case assignment. Replies derive the support author from authentication and explicitly target the requester; clients cannot impersonate authors. Resolution requires a reviewed decision and cannot declare unresolved refunds or custody recovery complete. Restricted internal notes remain distinct from requester messages.

Content reports create review work, not immediate removal. Operations can request a restriction under a policy decision; underlying source-domain capabilities and privacy/recovery effects must still be enforced. Proposed report categories/statuses remain review drafts.

Ops exports permit fulfilment, verification-SLA and support reports only. They cannot request Finance reports or bank accounts. Workers must validate date ranges, bound retention, capture a stable authorized snapshot, sanitize fields and neutralize spreadsheet formula cells. Ready responses expose private media references; source capability is checked again on access. These schemas do not implement CSV generation or access controls.

## Event and payment recovery

Blocked-event reads expose safe event/consumer metadata and processing receipts, not executable payloads. Replay binds the stored event, consumer, remediation decision, case and expected version. It cannot replace payloads or skip receipts. The service must validate a permitted registered consumer rather than trust the string, retain canonical event bytes and idempotency, and enforce source capability. An ops-lead label must not authorize Finance replay effects. Replay acknowledgement is queued work, not an applied financial effect.

Operation-job reads require the submitting principal plus current originating capability and source access. A successful result contains a typed reference, never a free-form result blob or unrestricted URL. Following the reference requires target authorization as well.

Payment reconciliation is Finance-sensitive and queues authenticated provider lookup. Clients cannot set capture/refund amounts through that command. Recovery views preserve independent capture, allocation and processed-refund values and unlinked captures. Schema nonnegativity does not establish accounting equality, authoritative provider evidence or recovery completion. Source transitions and exact domain error reconciliation still need implementation review.

## Verification

Validation passes for 309 operations and 3,528 attached request/response/error examples; 244 negative schema cases and five query cases are rejected. The 19 new failures cover secret leakage, unbounded role authority, author impersonation, automatic fraud/takedown claims, Finance export bypass, replay payload/receipt overrides and premature financial success.

No role-grant enforcement, session revocation, case messaging, export, replay or provider reconciliation has run. Strict completeness fails with 15 operations untyped: saved methods, notifications/realtime and web transports. P0 remains open, including policies, source reconciliation, research and runtime evidence.
