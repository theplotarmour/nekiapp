# ADR-018 — Deployment: containers on Fly.io (or ECS Fargate), Terraform, GitHub Actions

| Status | Accepted (platform choice finalized in Phase 1 spike) |
|---|---|
| Deciders | Tech lead, devops |
| Related | ADR-004, ADR-009, ADR-017; `02-tdd.md §21` |

## Context
Small team, single region (India), modular monolith + workers, WebSockets (sticky-less thanks to Redis fan-out), managed Postgres/Redis, media on R2, web portals static. Requirements: reproducible envs (dev/staging/prod), zero-downtime deploys, migrations as pre-deploy step, kill switches, backups with PITR, no Kubernetes.

## Decision
- **Compute:** Docker images for `neki-api` and `neki-worker` (same image, different entrypoint). Primary target **Fly.io** (Mumbai `bom` region, Machines, built-in LB with WS support, simple scaling). Fallback/alternate evaluated in a Phase 1 spike: **AWS ECS Fargate** in `ap-south-1` behind ALB if Fly Mumbai capacity or compliance requires AWS.
- **Data:** managed Postgres (Neon or RDS) with PITR 7 d; managed Redis (Upstash/ElastiCache).
- **Edge:** Cloudflare DNS, WAF, CDN, R2, Workers (OG share pages).
- **Web portals:** Vercel or Cloudflare Pages (static Flutter Web builds).
- **IaC:** Terraform for all cloud resources; secrets in provider secret manager; no secrets in repo.
- **CI/CD:** GitHub Actions — lint/test/contract/codegen-diff/scan → build → deploy staging on `main`; prod on tag with manual approval; Alembic migration job before rollout; health-gated rolling deploy.
- **Mobile:** Fastlane; TestFlight/Play Internal weekly; phased rollout; Codemagic or GitHub macOS runner for iOS.

## Alternatives
- **Kubernetes (EKS/GKE)** — excluded by master prompt; unnecessary for one service + workers.
- **Render / Railway** — similar simplicity; India region availability weaker.
- **Bare VM + docker compose** — cheapest; manual ops, no rolling deploys; acceptable for dev only.
- **Serverless (Lambda/Cloud Run)** — WebSockets and long-running workers awkward; cold starts.

## Pros
Minutes to deploy; scale by replica count; managed data with backups; WS-friendly LB; Terraform reproducibility; low fixed cost.

## Cons
Fly.io maturity/incident history → health checks, multi-machine, and ECS fallback plan. Two clouds (Fly + Cloudflare + managed DB vendor) to coordinate.

## Risks
Data residency expectations for Indian users → keep DB and compute in India regions; document in privacy policy.

## Consequences
Environments: `dev` (compose), `staging`, `prod`. Monthly restore drill. Feature flags for payments/tracking kill switches read from server table. Deploy checklist in runbook.

## Migration path
Same images run on ECS/Kubernetes; Terraform modules swapped; no application changes.
