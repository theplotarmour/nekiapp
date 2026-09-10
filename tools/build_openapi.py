"""Assemble the explicitly authored P0 OpenAPI slices; missing operations stay missing."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import contract_identity as identity

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "docs" / "api"


def build():
    inventory = list(csv.DictReader((API / "operations.tsv").open(encoding="utf-8-sig"), delimiter="\t"))
    definitions = identity.definitions()
    examples = identity.examples()
    schemas = identity.schemas()
    errors = {
        "400": ["REQUEST_INVALID", "CURSOR_INVALID"],
        "401": ["AUTH_REQUIRED", "SESSION_EXPIRED", "REFRESH_INVALID", "REFRESH_REUSED"],
        "403": ["ACTION_FORBIDDEN", "STEP_UP_REQUIRED", "OTP_LOCKED"],
        "404": ["NOT_FOUND", "LOCALITY_NOT_FOUND"],
        "409": ["VERSION_CONFLICT", "IDEMPOTENCY_KEY_REUSED", "REQUEST_IN_PROGRESS", "DELETION_NOT_CANCELLABLE", "CONSENT_VERSION_CHANGED"],
        "410": ["CURSOR_EXPIRED"],
        "422": ["EVIDENCE_REQUIRED", "OTP_INVALID", "OTP_EXPIRED", "MEDIA_NOT_READY"],
        "429": ["RATE_LIMITED", "OTP_RATE_LIMITED"],
        "503": ["DEPENDENCY_UNAVAILABLE"],
    }
    code_status = {code: status for status, codes in errors.items() for code in codes}
    doc = {"openapi": "3.1.1", "info": {"title": "NEKI API — partial P0 review contract", "version": "0.0.1-draft",
           "description": "Explicit identity/preference slice only. No server exists; uncovered inventory operations are reported separately."},
           "servers": [{"url": "/v1"}], "security": [{"BearerAuth": []}], "paths": {},
           "components": {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}, "schemas": schemas},
           "x-neki-status": "partial-review-draft"}
    for row in inventory:
        op_id = row["operation_id"]
        if op_id not in definitions:
            continue
        request, status, response, domain_errors, effects = definitions[op_id]
        op = {"operationId": op_id, "summary": op_id.replace("_", " ").capitalize(), "tags": [row["family"]],
              "description": effects, "x-neki-policy": row["policy"], "x-neki-projection": row["projection"],
              "x-neki-source": row["contract"], "x-neki-effects": effects,
              "x-neki-rate-class": "auth_challenge" if row["profile"] == "auth" else "private_read" if row["method"] == "GET" else "write",
              "parameters": [], "responses": {}}
        if row["policy"] == "public" or op_id in {"request_otp", "verify_otp", "refresh_session"}:
            op["security"] = []
        for name in re.findall(r"\{([^}]+)\}", row["path"]):
            op["parameters"].append({"name": name, "in": "path", "required": True, "schema": identity.ID})
        if row["profile"] == "list":
            op["parameters"] += [{"name": "cursor", "in": "query", "schema": identity.text(1, 2048)},
                                 {"name": "limit", "in": "query", "schema": {**identity.integer(1, 50), "default": 20}}]
        if row["method"] != "GET" and row["profile"] != "auth":
            op["parameters"].append({"name": "Idempotency-Key", "in": "header", "required": True, "schema": identity.ID})
        if row["policy"] == "self_sensitive":
            op["parameters"].append({"name": "X-Step-Up-Grant", "in": "header", "required": True, "schema": identity.text(32, 4096)})
        if row["method"] == "DELETE":
            op["parameters"].append({"name": "If-Match", "in": "header", "required": True,
                                     "schema": identity.text(3, 24, pattern=r'^"[0-9]+"$'),
                                     "description": "Quoted current aggregate version, e.g. \"1\"."})
        if request:
            content = {"schema": identity.ref(request), "examples": {"example": {"value": examples[request]}}}
            if request in {"OtpRequest", "OtpVerify", "RefreshRequest"}:
                web = dict(examples[request], client_kind="web")
                web.pop("refresh_token", None)
                content["examples"]["web"] = {"value": web}
            op["requestBody"] = {"required": True, "content": {"application/json": content}}
        headers = {"Cache-Control": {"schema": {"type": "string"}, "example": "private, no-store"},
                   "X-Request-Id": {"schema": identity.text(1, 100)}}
        success = {"description": effects, "headers": headers}
        if response:
            success["content"] = {"application/json": {"schema": identity.ref(response), "examples": {"example": {"value": examples[response]}}}}
        if response == "SessionResult":
            success["content"]["application/json"]["examples"]["web"] = {"value": examples["WebSession"]}
            headers["Set-Cookie"] = {"schema": {"type": "string"}, "description": "Web transport only: repeated Set-Cookie headers issue/rotate __Host-neki_refresh (Secure; HttpOnly; SameSite=Strict; Path=/; no Domain) and a separate Secure SameSite signed session-bound CSRF cookie readable by the first-party client. Refresh token never enters web JSON. Header repetition is a transport rule, not a comma-joined cookie value."}
        if op_id in {"verify_otp", "refresh_session"}:
            op["x-neki-browser-origin-check"] = True
        if op_id == "refresh_session":
            op["description"] += " Mobile branch authenticates refresh_token in body. Web branch requires both refresh cookie and matching signed CSRF header; neither branch is anonymous. Transport must match original session binding."
            op["parameters"] += [{"name": "__Host-neki_refresh", "in": "cookie", "schema": identity.text(32, 4096),
                                  "description": "Required for client_kind=web; forbidden as mobile authentication fallback."},
                                 {"name": "X-CSRF-Token", "in": "header", "schema": identity.text(32, 4096),
                                  "description": "Required and session-bound for client_kind=web; same-origin validation required."}]
        if op_id == "logout_session":
            headers["Set-Cookie"] = {"schema": {"type": "string"}, "description": "Clear web refresh cookie; revocation is still server-side."}
        op["responses"][status] = success
        common = ["REQUEST_INVALID", "RATE_LIMITED", "DEPENDENCY_UNAVAILABLE"]
        if op.get("security", doc["security"]):
            common += ["AUTH_REQUIRED", "SESSION_EXPIRED", "ACTION_FORBIDDEN"]
        if "{id}" in row["path"] or op_id == "get_deletion_status":
            common += ["NOT_FOUND"]
        if row["profile"] == "list":
            common += ["CURSOR_INVALID", "CURSOR_EXPIRED"]
        if row["method"] != "GET" and row["profile"] != "auth":
            common += ["VERSION_CONFLICT", "IDEMPOTENCY_KEY_REUSED", "REQUEST_IN_PROGRESS", "EVIDENCE_REQUIRED"]
        if row["policy"] == "self_sensitive":
            common += ["STEP_UP_REQUIRED"]
        by_status = {}
        for code in sorted(set(common + domain_errors)):
            by_status.setdefault(code_status[code], []).append(code)
        for error_status, codes in by_status.items():
            schema_name = f"{op_id}_error_{error_status}"
            schemas[schema_name] = identity.obj({"error": identity.obj({
                "code": identity.enum(*codes), "message": identity.text(1, 300), "request_id": identity.text(1, 100),
                "retryable": identity.BOOL,
                "details": identity.obj({"current_version": identity.VERSION, "retry_after_seconds": identity.integer(1, 86400)}, []),
            })})
            op["responses"][error_status] = {"description": ", ".join(codes),
                "content": {"application/json": {"schema": identity.ref(schema_name), "examples": {
                    code.lower(): {"value": {"error": {"code": code, "message": code.replace("_", " ").capitalize(),
                        "request_id": "req_synthetic", "retryable": code in {"RATE_LIMITED", "REQUEST_IN_PROGRESS", "DEPENDENCY_UNAVAILABLE"}, "details": {}}}}
                    for code in codes}}}}
            if error_status in {"429", "503"} or "REQUEST_IN_PROGRESS" in codes:
                op["responses"][error_status]["headers"] = {"Retry-After": {"schema": identity.integer(1, 86400)}}
        doc["paths"].setdefault(row["path"], {})[row["method"].lower()] = op
    missing = [row["operation_id"] for row in inventory if row["operation_id"] not in definitions]
    coverage = {"status": "partial-review-draft", "inventory_count": len(inventory), "typed_count": len(definitions),
                "covered_operations": sorted(definitions), "remaining_operations": missing,
                "limitations": ["Schema validation is not implementation proof", "AP and domain policy decisions remain open",
                                "Public web and WS need separate transport schemas", "FastAPI export becomes canonical only after P0 review and implementation"]}
    return doc, coverage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail on generated contract drift without writing")
    args = parser.parse_args()
    for path, value in zip([API / "openapi.json", API / "openapi-coverage.json"], build()):
        data = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != data:
                raise SystemExit(f"Generated contract drift: {path.relative_to(ROOT)}")
        else:
            path.write_text(data, encoding="utf-8")
    print("OpenAPI generation/drift check passed")


if __name__ == "__main__":
    main()
