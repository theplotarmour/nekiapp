# Payment webhook transport contract

**Status:** P0 review draft, 2026-09-11. The webhook operation is now typed separately from user APIs. Coverage is 175 of 324 operations; [149 remain](openapi-coverage.json). This slice includes a local executable experiment, not a deployed endpoint or sandbox integration.

## Vendor evidence and transport

Rechecked the [Razorpay validation guide](https://razorpay.com/docs/webhooks/validate-test/) on 2026-09-11: HMAC-SHA256 signs the original request body; retained old secrets are needed for retries signed before rotation; event IDs identify duplicates; delivery order is not guaranteed. [Payment events](https://razorpay.com/docs/webhooks/payments.md) and [refund events](https://razorpay.com/docs/webhooks/refunds.md) were read via their Markdown endpoints because the web reader could not render their response content type. Their provider-owned payloads vary by payment method and may carry personal data.

`POST /payments/webhook` uses the `RazorpayWebhookSignature` security scheme. OpenAPI represents it as a header API-key scheme only because OpenAPI has no native raw-body HMAC scheme: the header is a per-request signature, never a static credential. The route requires the event-ID header and has no bearer, step-up, client idempotency key or expected-version requirement. Signature failures are 401; invalid header framing is 400; the proposed 1 MiB ingress limit produces 413. Storage failure must produce a non-success response so delivery can retry.

Authenticate raw bytes before parsing, transforming or logging the payload. Verify against the endpoint's configured active and retained previous webhook secrets using constant-time comparison. Endpoint configuration binds provider account and environment independently of the payload. Do not use an API secret in place of the webhook secret. Retention and retirement of previous keys need an explicit security policy; the local experiment does not decide that policy.

The intake envelope deliberately preserves vendor extension fields as recursively typed JSON values. This is not a normalized payment/capture contract or a client request that can choose business fields. Unknown events, account mismatches and malformed signed payloads go to restricted durable quarantine. HTTP schema middleware must not reject or reserialize these before authentication/preservation. Body size/depth limits, malformed ingress handling and quarantine limits require operational validation.

## Durable receipt and processing

A 200 receipt means durable intake, duplicate recognition or durable quarantine, with `financial_effect_applied=false`. It never means a contribution was credited or a refund processed. Signed invalid payloads are acknowledged only after their raw evidence and review work are durably retained. Quarantine must be observable and replayable after reviewed correction.

Scope receipts by configured provider/account/environment. Store the body digest and event ID. Because the documented signature covers the body rather than the separate event-ID header, this design additionally deduplicates identical authenticated bytes within scope. A changed event-ID header must not bypass duplicate handling. A reused event ID with different authenticated bytes is preserved as a collision requiring review; do not overwrite the earlier evidence or erase any already-established financial fact.

Inbox deduplication is not financial deduplication. Distinct bodies and event IDs can describe the same payment. The later worker must enforce provider-entity capture/refund identities, exact account/order/payment/amount/currency linkage, late-capture recovery and non-regression. It must not infer completion from event name alone. Canonical normalized entity schemas and worker handlers remain implementation/research work; this slice covers transport intake only.

## Executable local evidence

Run:

```powershell
python -m unittest discover -s tools/spikes -p 'test_webhook_inbox.py' -v
.venv-contracts/Scripts/python tools/build_openapi.py --check
.venv-contracts/Scripts/python tools/validate_openapi.py
```

[webhook_inbox.py](../../tools/spikes/webhook_inbox.py) and [20 tests](../../tools/spikes/test_webhook_inbox.py) exercise synthetic raw HMAC bytes, active/previous keys, tampering, JSON reserialization, invalid headers, unknown/account-mismatched payloads, malformed signed JSON, size rejection, durable duplicates after reopening the connection, changed event-ID headers, collision preservation and an injected pre-commit failure. The cryptographic check also uses a fixed known HMAC vector. Invalid signatures leave no inbox row.

The experiment uses a temporary SQLite database and plaintext synthetic bodies. It does not implement a server, PostgreSQL concurrency, encrypted restricted storage, a worker, financial effects, provider delivery or real key rotation. A connection reopen is not a power-loss test; injected failure before commit is not a proof of every commit-response race. None of RP-01–RP-07 is closed by these tests; RP-06 has local fixture evidence only.

Shared OpenAPI validation passes 175 operations and 1,952 request/response/error examples, rejects 135 negative schema cases and five query cases, and verifies the webhook has its own security declaration and no user mutation headers. Strict completeness still fails with 149 operations untyped. Saved methods and remaining domain/transport families are next. P0 remains open.
