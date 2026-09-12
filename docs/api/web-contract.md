# Public-web transport draft

Status: P0 review draft; no deployed pages or verified app associations. These eight origin-root GET routes complement the 315 JSON HTTP operations and one WebSocket transport. All 324 inventory operations now have draft contracts; this is schema coverage, not P0 approval or product completion.

`tools/contract_web.py` authors [web-transports.json](web-transports.json). This custom transport document specifies HTML response headers, public page models, unavailable responses, validated public IDs, and Android/Apple association bodies. It is not OpenAPI or an application renderer. The HTML generator exists solely for synthetic contract checks.

| Routes | Contract boundary |
|---|---|
| `/m/{public_id}`, `/o/{public_id}` | Published public-safe content only; hidden, suspended and missing records share the unavailable response. Private addresses, proof and account information cannot be introduced as page-model fields. |
| `/privacy`, `/terms`, `/help`, `/account-deletion` | Approved versioned content and truthful support/deletion instructions required before release. Fixture wording is not approved copy. |
| `/.well-known/assetlinks.json` | Android package and SHA-256 release-signing certificate associations. |
| `/.well-known/apple-app-site-association` | Apple application identifiers and components limited to mission/organization paths in this draft. |

Canonical URLs must come from configured origins and validated routes. Escape rendered text and attribute values. Public IDs confer no authorization. Production rendering still needs approved share metadata, assets, store destinations, accessibility and browser checks. Association deployment requires actual domains, signing identities, application configuration and device verification; synthetic identifiers must never be deployed.

Platform references: [Android association configuration](https://developer.android.com/training/app-links/configure-assetlinks), [Apple associated domains](https://developer.apple.com/documentation/xcode/supporting-associated-domains), and [Apple universal-link debugging](https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links). These specify platform behavior; fixture validation cannot prove domain ownership or installation behavior.

Reproduce from the repository root using the existing contract environment:

```powershell
.venv-contracts/Scripts/python tools/build_openapi.py --check
.venv-contracts/Scripts/python tools/validate_openapi.py --require-complete
.venv-contracts/Scripts/python tools/check_api_inventory.py
```

The web validator checks all eight inventory mappings, 18 schema examples, nine rejected inputs, seven parsed HTML fixtures and escaped hostile content. The shared completeness flag now passes for inventory coverage. Runtime authorization, approved policy content, live domains, devices, client generation and remaining P0 review gates remain unverified.
