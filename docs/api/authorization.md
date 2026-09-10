# Route and field authorization matrix

**Status:** Proposed G25/G24 contract. Names below are policy identifiers in `operations.tsv`, not role grants or implemented middleware. Current actor, owner/org membership, suspension, action capability and record version are evaluated server-side. Reject denied cross-owner lookups without revealing object existence. Mutations never trust request `user_id`, `organization_id`, role or fee fields as authority.

## Policies

| Identifier | Required principal and scope | Restrictions |
|---|---|---|
| public | Anonymous or authenticated | Only published/visible/eligible safe projection; no personalized caching mixed into public response. |
| challenge | OTP/refresh/session challenge subject | Verify credential/challenge, attempt/rate/expiry/reuse rules; no logged secrets; not a generic public write. |
| self | Authenticated current user | Own resources only; suspension-aware policy allows recovery/logout/support/deletion but not prohibited participation. |
| self_sensitive | Current user plus server-verified step-up | Bound to user/session/action/resource and short expiry; use once where required. Device biometrics alone are insufficient. |
| applicant | Authenticated application owner | Server-established ownership; org application actions allowed before org_admin. Own documents only, no public verification rights. |
| org | Active org member with scoped capability | Server resolves org and checks current eligibility for publication/participation; review/recovery reads remain available under suspension policy. |
| org_sensitive | Org member with scoped capability and server step-up | Own bank-change request and similar sensitive edits; submitting never verifies the bank or grants Finance approval. |
| org_attendance | Scoped org attendance verifier | Only own mission assignments; reason/evidence and no self-verification. No global volunteer history or unrelated locations. |
| volunteer | Authenticated current approved volunteer | Assignment/slot-specific scope, current approval and enhanced-check eligibility; rejected/suspended application status itself uses self. |
| field | Currently assigned approved volunteer | Assignment revision, mission, allowed time window and purpose; revocation takes effect on next action/read. No historical address access by old role. |
| participant | Contributor/assigned volunteer/scoped org member for this subject | Different projection per relationship; membership is not equal access to all proof fields. |
| proof_submitter | Subject-authorized org/volunteer or delegated ops capability | Correct subject/mission link, media ownership and consent; acting on behalf records reason. |
| reviewer | Ops reviewer with specific org/mission/proof/application review capability | Assigned/scoped queue, independent verification where required; no payout authority. |
| ops | Ops agent with named operational/support capability | Restricted assigned queue/case/mission; cannot approve Finance transfers or unrestricted role grants. |
| ops_lead | Ops lead with the specific sensitive capability and step-up | Required reason/case; suspension/reinstatement, dispute and custody exceptions; not universal status editing. |
| finance | Finance scoped to operation and org/payment/period | Masked bank view by default; no proof/home GPS access. Mutations bind exact reviewed allocation snapshot. |
| finance_sensitive | Finance capability plus server step-up | Payout approval/execution/reconciliation/refund and bank verification; enforce distinct approver >₹50,000 and change-triggered renewed approval. |
| security | Explicit access-administration capability and step-up | Grant/revoke only allowed roles, no self-escalation; sensitive grant audit and revocation propagation. Super Admin label alone grants no universal bypass. |
| provider | Verified configured provider account/environment | Raw-body signature and provider identity, replay-safe inbox; no end-user bearer token fallback. |
| media_owner | Owner or purpose-authorized reviewer/participant | Check processing state, media purpose and relationship each read; upload ownership does not grant arbitrary public publishing. |
| share_token | Explicitly consented current revocable token | Only frozen safe sharing projection; no owner identity/proof inference beyond consent; disabled pending AP-04. |
| socket | Authenticated single-use connection ticket | Current session, origin where applicable, channel relationship and revocation; no wildcard private subscription. |
| operation_owner | Authenticated submitting principal with current originating capability | Job ownership and current access to source objects; Finance jobs remain Finance-scoped, ops jobs ops-scoped, no cross-role result leak. |

“Scoped capability” is an enforceable server permission plus resource relationship, not freeform role text. Runtime must have a complete action-to-capability grant table and tests before these policies can be accepted. Scheduler/service commands use dedicated internal principals, not undocumented public admin endpoints.

## Projection allowlists

| Projection | Permitted fields / explicit exclusions |
|---|---|
| public | Published mission/org/category content, approximate public location, per-need quantities/availability, public-safe verification labels and consented/redacted derivatives; no donor identity, exact pickup/home location, bank details or review documents. |
| self | Own profile/preferences/devices/addresses, owned contribution amounts/fee disclosure/status and own cases; no tokens/OTP hash/provider secret/card data. |
| session | Access/session result per client transport; never return refresh credentials through generic profile JSON. Mobile secure-storage versus web HTTP-only cookie/CSRF contract AP-02. |
| application | Applicant's own submission, revision, requested information and safe decision reason; restricted fraud/reviewer notes excluded. |
| org | Own org editor/settings/dashboard/roster/mission progress; contribution display respects anonymous preference; no payment credentials or other contributors' homes. |
| attendance | Scoped roster, accepted attendance and provisional/verified hours; exact check location restricted to authorized review purpose, not routine roster export. |
| field | Minimum active pickup destination/contact/custody data permitted by consent/window; no stale/unrelated addresses, donor payment data or other assignments' proof. |
| tracking | Owner-specific snapshot/timeline/version with approved approximate position; no precise route/origin from generic events. Org and volunteer views use separate scoped serializers. G23 precision still unresolved. |
| proof | Submitter/reviewer/current participant-specific evidence projection; raw capture GPS and home photos only where specifically authorized. Public or ordinary participant receives approved redacted derivatives. |
| review | Reviewer-required docs/checklists/history; restricted notes never copied into applicant/public response. |
| finance | Captures/refunds/payouts/allocation facts and audit references, masked bank snapshot, scoped statement/report; bank evidence URL separately authorized. |
| audit | Capability-scoped who/what/when/why and safe metadata; no raw secrets/request bodies. Sensitive audit subsets independently authorized. |
| impact | Effective verified record, correction history, sources and metadata; owner/consented public versions differ, no private identity link or raw proof metadata by default. |
| media | Opaque ID, processing/rejection state and authorized short-lived access; never expose bucket credentials, arbitrary object keys or permanently public private URLs. |
| notification | Recipient-scoped title/body/status and safe subject link; destination independently authorizes access, stored deep link does not grant it. |
| operation | Accepted command/job ID, status, current authorized version and safe error/recovery link; not raw provider/worker payload. |
| health | Public liveness is minimal; admin readiness/queue diagnostics omit secrets and private data. |

## Required negative checks

- User A cannot read/mutate B's address, contribution, receipt, notification, application, support case or idempotency replay.
- Org A cannot read B's drafts/documents/roster/finance; org membership alone cannot view donor home proof.
- Revoked volunteer cannot fetch a fresh read URL, location or socket subscription even with a cached assignment/token.
- Anonymous mission view and shared Home cache cannot contain owner active-contribution modules. Authenticated personalized Home must be private/no-store or correctly owner-scoped.
- Ops cannot approve/pay a payout; Finance cannot see unrelated GPS/proof; Super Admin cannot bypass the reviewed action capability/step-up requirements.
- CSV export repeats source scope, sanitizes spreadsheet-formula-like values, logs download and expires access; asynchronous job ownership checked at result retrieval.
- Bank recipient revision change invalidates approval; self-approval above the threshold denied; a mobile biometric flag cannot satisfy server step-up.
- Public share revocation and privacy redaction invalidate subsequent reads and cached signed-access issuance. Restored data must respect deletion suppression policy.

These checks are planned acceptance obligations, not executed tests. Exact capability grants and privacy/retention decisions are AP-02/AP-05 and G21/G24/G25 work.
