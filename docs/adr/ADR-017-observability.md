# ADR-017 — Observability: Sentry + OpenTelemetry to Grafana Cloud

| Status | Accepted |
|---|---|
| Deciders | Tech lead, devops |
| Related | ADR-004, ADR-018; `02-tdd.md §18` |

## Context
Need crash reporting and performance for Flutter; traces across FastAPI → Postgres → Redis → Razorpay/Maps; business metrics (webhook lag, outbox lag, DLQ depth, payment failure rate, WS connections, dispatch queue age); alerting; `request_id` correlation from app to logs; PII scrubbing.

## Decision
- **Mobile/web:** Sentry (crashes, ANR, performance spans for cold start, screen TTI, checkout), release health, `request_id` breadcrumbs.
- **Backend:** OpenTelemetry SDK with auto-instrumentation (FastAPI, SQLAlchemy, httpx, redis) exporting traces/metrics to **Grafana Cloud** (Tempo/Prometheus/Loki); `structlog` JSON logs shipped to Loki; Sentry also for backend exceptions.
- **Alerts:** Grafana alerting to Slack/phone for the SLOs in `02-tdd.md §18`.
- **Dashboards:** platform health (also surfaced read-only in ops console), payments, realtime, workers.

## Alternatives
- **Datadog** — best integrated; cost prohibitive at seed stage.
- **New Relic** — generous free tier; less OTel-native at the time; viable fallback.
- **Self-hosted Grafana stack** — ops burden; use managed until scale justifies.
- **Only Sentry** — lacks metrics/business dashboards.

## Pros
Vendor-neutral instrumentation (OTel); low cost tiers; strong Flutter Sentry SDK; logs-traces-metrics correlation.

## Cons
Two vendors (Sentry + Grafana Cloud); sampling decisions needed for traces (10% baseline, 100% on errors and payment routes).

## Risks
PII in logs/breadcrumbs → structlog processors redact phone/email/addresses; Sentry `beforeSend` scrubber; tests for scrubbing.

## Consequences
`X-Request-Id` returned on every response and shown in app "Report a problem". SLO dashboards reviewed weekly. On-call runbook references dashboards.

## Migration path
OTel exporters reconfigured to any backend; Sentry replaceable with any crash tool.
