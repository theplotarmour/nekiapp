# ADR-012 — Authentication: phone OTP (MSG91) with server-issued JWT and RBAC

| Status | Accepted |
|---|---|
| Deciders | Tech lead, security review |
| Related | ADR-004; `02-tdd.md §4.4, §16`; `01-prd.md FR-01` |

## Context
Indian consumer norm is phone-first login; onboarding must be ≤ 6 taps. Roles span contributor, volunteer, org_admin, ops roles. Authorization must be server-side with principal-scoped queries. Payment-method changes and account deletion need step-up. Web portals share the identity system.

## Decision
- **Identity:** phone number + 6-digit OTP via **MSG91** (DLT-registered templates), 5-min TTL, 5 attempts then 15-min lockout, rate limits per phone/IP/device. Server-side OTP generation and hashing; provider adapter interface with a second SMS provider fallback.
- **Sessions:** server-issued **JWT access (15 min)** + **rotating refresh (30 d)** bound to device id, reuse detection revokes family. Tokens in Keychain/Keystore. Web portals use httpOnly cookies for refresh.
- **Authorization:** `roles[]` and optional `org_id` claims; per-endpoint policy functions; all queries filtered by principal; RBAC roles per `05-data-model.md §2`.
- **Step-up:** re-OTP or biometric (local) before payment-method changes, account deletion, org bank details.
- Email/password and social login deferred to NEXT.

## Alternatives
- **Firebase Authentication (phone)** — fast to integrate; per-verification cost scales, vendor lock, weaker control over rate-limit/lockout UX, backend still needs its own session/RBAC model. Rejected for control and cost; kept as emergency fallback adapter.
- **Auth0/Clerk/Supabase Auth** — good for email/social; phone OTP in India pricier; extra vendor.
- **Truecaller SDK** — faster login for Android; add in NEXT as an accelerator, not the primary path.
- **Passwordless email magic links** — friction on mobile; not India-first.

## Pros
Full control over abuse controls and UX copy; low per-OTP cost; one identity across app and web; simple to test.

## Cons
DLT registration lead time (2–3 weeks) → start week 1; SMS deliverability variance → fallback provider and resend UX; we own token security.

## Risks
SIM-swap account takeover → step-up on sensitive actions, device binding, notification on new device login. OTP brute force → lockouts and IP limits.

## Consequences
Authz matrix tests (every role × every route) in CI. Audit log on auth events. Public ids opaque to limit IDOR blast radius.

## Migration path
Adding email/social = new `IdentityProvider` producing the same user record; sessions unchanged.
