"""Public-web transport contracts and synthetic HTML/association fixtures."""

from copy import deepcopy
from html import escape
from contract_identity import ID, UUID, enum, obj, text
from contract_discovery import array, HTTPS


def ref(name):
    return {"$ref": f"#/schemas/{name}"}


def render_fixture(model):
    """Minimal verification fixture, not application UI or approved legal content."""
    title = escape(model["title"])
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in model["paragraphs"])
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{title}</title><meta name="robots" content="noindex">'
        f'<link rel="canonical" href="{escape(model["canonical_url"], quote=True)}">'
        f'</head><body><main><h1>{title}</h1>{paragraphs}'
        '<a href="/help">Help</a></main></body></html>')


def document():
    fingerprint = text(95, 95, pattern=r"^(?:[A-F0-9]{2}:){31}[A-F0-9]{2}$")
    schemas = {
        "MissionPath": obj({"public_id": text(5, 100, pattern=r"^msn_[A-Za-z0-9_-]+$")}),
        "OrganizationPath": obj({"public_id": text(5, 100, pattern=r"^org_[A-Za-z0-9_-]+$")}),
        "PageModel": obj({"title": text(1, 160), "paragraphs": {**array(text(1, 4000), 50), "minItems": 1},
            "canonical_url": HTTPS, "content_revision_id": ID, "state": enum("AVAILABLE", "UNAVAILABLE", "APPROVED_INFORMATION")}),
        "AndroidAssociation": {"type": "array", "minItems": 1, "maxItems": 10, "uniqueItems": True, "items": obj({
            "relation": {"type": "array", "items": enum("delegate_permission/common.handle_all_urls"), "minItems": 1, "maxItems": 1},
            "target": obj({"namespace": enum("android_app"), "package_name": text(3, 200, pattern=r"^[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+$"),
                "sha256_cert_fingerprints": {**array(fingerprint, 10), "minItems": 1, "uniqueItems": True}})})},
        "AppleAssociation": obj({"applinks": obj({"details": {"type": "array", "minItems": 1, "maxItems": 10, "items": obj({
            "appIDs": {**array(text(12, 250, pattern=r"^[A-Z0-9]{10}\.[A-Za-z0-9.-]+$"), 10), "minItems": 1, "uniqueItems": True},
            "components": {"type": "array", "minItems": 2, "maxItems": 2, "uniqueItems": True, "items": obj({"/": enum("/m/*", "/o/*")})}})}})}),
        "HtmlResponse": obj({"status": {"type": "integer", "enum": [200, 404, 503]},
            "headers": obj({"Content-Type": enum("text/html; charset=utf-8"), "Cache-Control": enum("no-store"),
                "Referrer-Policy": enum("no-referrer"), "X-Content-Type-Options": enum("nosniff"),
                "Content-Security-Policy": enum("default-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")}),
            "body": text(1, 250000)}),
    }
    routes = [
        ("mission_web_fallback", "/m/{public_id}", "MissionPath", "Mission", "FR-13"),
        ("organization_web_fallback", "/o/{public_id}", "OrganizationPath", "Organization", "FR-13"),
        ("privacy_page", "/privacy", None, "Privacy", "FR-12"),
        ("terms_page", "/terms", None, "Terms", "FR-12"),
        ("help_page", "/help", None, "Help", "FR-12"),
        ("deletion_help_page", "/account-deletion", None, "Account deletion", "FR-12"),
    ]
    operations = {}
    examples = {"MissionPath": [{"public_id": "msn_synthetic"}], "OrganizationPath": [{"public_id": "org_synthetic"}], "PageModel": [], "HtmlResponse": []}
    for op_id, path, path_schema, title, source in routes:
        canonical = "https://example.invalid" + path.replace("{public_id}", "msn_synthetic" if path_schema == "MissionPath" else "org_synthetic")
        model = {"title": title, "paragraphs": ["Synthetic contract fixture; not approved product or legal copy."], "canonical_url": canonical,
                 "content_revision_id": UUID, "state": "AVAILABLE" if path_schema else "APPROVED_INFORMATION"}
        response = {"status": 200, "headers": {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer", "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"}, "body": render_fixture(model)}
        operations[op_id] = {"method": "GET", "inventory_method": "PUBLIC_WEB", "path": path, "policy": "public", "projection": "public", "source": source,
            "path_schema": ref(path_schema) if path_schema else None, "response_schema": ref("HtmlResponse"), "view_model_schema": ref("PageModel"),
            "success_status": 200, "failure_statuses": [404, 503] if path_schema else [503], "example_response": response}
        examples["PageModel"].append(model); examples["HtmlResponse"].append(response)
    for op_id, path, schema in [("android_app_links", "/.well-known/assetlinks.json", "AndroidAssociation"),
                                ("apple_app_links", "/.well-known/apple-app-site-association", "AppleAssociation")]:
        operations[op_id] = {"method": "GET", "inventory_method": "PUBLIC_WEB", "path": path, "policy": "public", "projection": "public", "source": "FR-13",
            "body_schema": ref(schema), "success_status": 200, "content_type": "application/json", "redirects": "forbidden",
            "failure_statuses": [503], "configuration_gate": "Verified domain/app identifiers and release signing identity required; do not deploy synthetic fixtures"}
    examples["AndroidAssociation"] = [[{"relation": ["delegate_permission/common.handle_all_urls"], "target": {"namespace": "android_app",
        "package_name": "invalid.example.neki", "sha256_cert_fingerprints": [":".join(["00"] * 32)]}}]]
    examples["AppleAssociation"] = [{"applinks": {"details": [{"appIDs": ["ABCDEFGHIJ.invalid.example.neki"], "components": [{"/": "/m/*"}, {"/": "/o/*"}]}]}}]
    unavailable = {"title": "Content unavailable", "paragraphs": ["This content is unavailable."], "canonical_url": "https://example.invalid/m/msn_synthetic", "content_revision_id": UUID, "state": "UNAVAILABLE"}
    examples["PageModel"].append(unavailable)
    missing = deepcopy(examples["HtmlResponse"][0]); missing.update(status=404, body=render_fixture(unavailable)); examples["HtmlResponse"].append(missing)
    return {"format": "neki-web-transport-contract.v1", "status": "review-draft", "operations": operations, "schemas": schemas, "examples": examples,
        "invariants": [
            "Paths are origin-root routes, not /v1 JSON endpoints. Public IDs are opaque names, not authorization or enumeration protection.",
            "Render only published public-safe records; hidden/missing/suspended content uses indistinguishable unavailable response without private metadata.",
            "Escape all content; construct canonical links from configured origin and validated route, never arbitrary Host/query redirects or raw user HTML.",
            "Fallback pages work without app installation or JavaScript; reviewed store links are optional configured destinations, never user return URLs.",
            "Privacy/terms require approved versioned legal copy; help/deletion must expose the real supported workflow and truthful retention/hold limitations. Fixtures are not policy approval.",
            "Association files require correct production app identifiers, signing keys, entitlements/manifest and domain ownership. Serve JSON over HTTPS without redirect or authentication.",
            "Apple paths restrict this draft to public mission/org routes; Android manifest must bound paths equivalently. Do not claim private contribution or share links are associated without separate review.",
            "No synthetic association IDs/fingerprints or draft policy fixtures may pass deployment gates. Header/CSP/cache defaults require final assets and renderer review.",
        ]}


def negative_cases():
    d = document(); e = d["examples"]; cases = []
    for schema, changes in [("MissionPath", {"public_id": "../admin"}), ("OrganizationPath", {"public_id": "msn_other"}),
        ("PageModel", {"pickup_address": "private"}), ("PageModel", {"canonical_url": "javascript:alert(1)"}),
        ("HtmlResponse", {"status": 302})]:
        value = deepcopy(e[schema][0]); value.update(changes); cases.append((schema, value))
    android = deepcopy(e["AndroidAssociation"][0]); android[0]["target"]["sha256_cert_fingerprints"] = ["invalid"]
    cases.append(("AndroidAssociation", android))
    android = deepcopy(e["AndroidAssociation"][0]); android[0]["target"]["namespace"] = "web"
    cases.append(("AndroidAssociation", android))
    apple = deepcopy(e["AppleAssociation"][0]); apple["applinks"]["details"][0]["components"] = [{"/": "/*"}, {"/": "/o/*"}]
    cases.append(("AppleAssociation", apple))
    apple = deepcopy(e["AppleAssociation"][0]); apple["applinks"]["details"][0]["appIDs"] = ["missingteam"]
    cases.append(("AppleAssociation", apple))
    return cases
