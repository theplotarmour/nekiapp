"""Validate P0 schemas/examples and coverage; this never tests running endpoints."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate_spec
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import contract_identity as identity
import contract_discovery as discovery
import contract_organizations as organizations
import contract_contributions as contributions
import contract_cases as case_contracts
import contract_payouts as payouts
import contract_provider as provider
import contract_volunteers as volunteers
import contract_logistics as logistics
import contract_proof as proof
import contract_impact as impact
import contract_admin as admin
import contract_engagement as engagement

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "docs" / "api"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    doc = json.loads((API / "openapi.json").read_text(encoding="utf-8"))
    coverage = json.loads((API / "openapi-coverage.json").read_text(encoding="utf-8"))
    validate_spec(doc)
    registry = Registry().with_resource("urn:neki-contract", Resource.from_contents(doc, default_specification=DRAFT202012))

    def validator(schema):
        reference = "urn:neki-contract" + schema["$ref"]
        return Draft202012Validator({"$ref": reference}, registry=registry, format_checker=FormatChecker())

    for schema in doc["components"]["schemas"].values():
        Draft202012Validator.check_schema(schema)
    inventory = {row["operation_id"]: row for row in csv.DictReader((API / "operations.tsv").open(encoding="utf-8-sig"), delimiter="\t")}
    actual = set()
    example_count = 0
    for path, methods in doc["paths"].items():
        for method, operation in methods.items():
            op_id = operation["operationId"]
            assert op_id not in actual, op_id
            actual.add(op_id)
            row = inventory[op_id]
            assert (row["path"], row["method"].lower()) == (path, method), op_id
            assert operation["x-neki-policy"] == row["policy"], op_id
            if row["policy"] not in {"public", "challenge", "provider", "share_token"}:
                assert operation.get("security", doc["security"]) == [{"BearerAuth": []}], op_id
            if row["policy"] == "public":
                assert operation.get("security") == [], op_id
            if row["policy"] == "share_token":
                assert operation.get("security") == [] and operation.get("x-neki-path-credential") == "token", op_id
                token = next(p for p in operation["parameters"] if p["name"] == "token")
                assert token["required"] and token["in"] == "path" and token["schema"] == impact.SHARE_TOKEN, op_id
            if op_id in {"create_impact_share", "get_shared_impact"}:
                assert operation.get("x-neki-feature-gate") == {"decision": "AP-04", "default": "disabled"}, op_id
            if row["policy"] == "provider":
                assert operation.get("security") == [{"RazorpayWebhookSignature": []}], op_id
                assert operation.get("x-neki-raw-body-signature") is True, op_id
                assert not any(p["name"] in {"Idempotency-Key", "If-Match", "X-Step-Up-Grant"} for p in operation["parameters"]), op_id
                assert any(p["name"] == "x-razorpay-event-id" and p["required"] for p in operation["parameters"]), op_id
                assert "409" not in operation["responses"], op_id
            if row["policy"] in {"self_sensitive", "org_sensitive", "finance_sensitive", "ops_lead", "security"}:
                assert any(p["name"] == "X-Step-Up-Grant" and p["required"] for p in operation["parameters"]), op_id
            if row["profile"] == "query":
                assert not any(p["name"] in {"Idempotency-Key", "If-Match"} for p in operation["parameters"]), op_id
            bodies = [operation.get("requestBody", {})] + list(operation["responses"].values())
            for body in bodies:
                for media in body.get("content", {}).values():
                    assert media.get("examples"), f"missing examples: {op_id}"
                    check = validator(media["schema"])
                    for example in media["examples"].values():
                        check.validate(example["value"])
                        example_count += 1
    assert actual == set(coverage["covered_operations"])
    transport = set(coverage["transport_contracts"])
    assert not actual & transport
    assert set(inventory) - actual - transport == set(coverage["remaining_operations"])
    assert len(transport) == coverage["transport_typed_count"]
    assert len(actual) + len(transport) == coverage["total_contract_count"]
    assert not actual & set(coverage["remaining_operations"])
    assert len(actual) == coverage["typed_count"]
    assert len(inventory) == coverage["inventory_count"]

    good = identity.examples()
    cases = []

    def reject(schema, changes, label):
        value = deepcopy(good[schema])
        value.update(changes)
        cases.append((schema, value, label))

    reject("OtpVerify", {"code": "12345"}, "short OTP")
    reject("OtpVerify", {"code": "12345x"}, "non-digit OTP")
    reject("OtpVerify", {"code": 123456}, "numeric OTP loses leading zero")
    reject("OtpVerify", {"device_id": "not-a-uuid"}, "invalid device identity")
    reject("OtpRequest", {"phone_e164": "9000000001"}, "unqualified phone")
    reject("ProfileUpdate", {"roles": ["super_admin"]}, "role injection")
    reject("ProfileUpdate", {"phone_e164": "+919000000002"}, "phone change through profile")
    reject("ProfileUpdate", {"first_name": ""}, "empty name")
    reject("ProfileUpdate", {"expected_version": -1}, "negative version")
    reject("ProfileUpdate", {"expected_version": 1.5}, "fractional version")
    cases.append(("ProfileUpdate", {"expected_version": 1}, "empty patch"))
    reject("WebSession", {"refresh_token": identity.EXAMPLE_TOKEN}, "web refresh leak")
    reject("WebRefresh", {"refresh_token": identity.EXAMPLE_TOKEN}, "mixed refresh transport")
    reject("RefreshRequest", {"refresh_token": ""}, "empty mobile refresh")
    reject("StepUpRequest", {"biometric_passed": True}, "local biometric bypass")
    reject("StepUpRequest", {"action": "all_actions"}, "unbounded step-up scope")
    reject("ConsentCreate", {"accepted": False}, "false consent receipt")
    reject("ConsentCreate", {"accepted_at": identity.NOW}, "client-chosen consent time")
    reject("DeviceSummary", {"push_token": "private"}, "push token response leak")
    reject("UserProfile", {"token_hash": "private"}, "token hash response leak")
    reject("SelectedLocation", {"pickup_serviceability": "approved"}, "city as pickup approval")
    reject("ConsentReceipt", {"accepted_at": "2026-09-10T17:30:00+05:30"}, "non-UTC wire timestamp")
    duplicated = deepcopy(good["NotificationPreferencesUpdate"]["categories"])
    duplicated[-1] = deepcopy(duplicated[0])
    reject("NotificationPreferencesUpdate", {"categories": duplicated}, "duplicate category")
    cases += discovery.negative_cases()
    cases += organizations.negative_cases()
    cases += contributions.negative_cases()
    cases += case_contracts.negative_cases()
    cases += payouts.negative_cases()
    cases += provider.negative_cases()
    cases += volunteers.negative_cases()
    cases += logistics.negative_cases()
    cases += proof.negative_cases()
    cases += impact.negative_cases()
    cases += admin.negative_cases()
    cases += engagement.negative_cases()
    for schema, value, label in cases:
        assert not validator(identity.ref(schema)).is_valid(value), f"negative case accepted: {label}"
    parameter_cases = [("/search", "q", ""), ("/missions", "radius_km", 51),
                       ("/missions", "min_amount_paise", 1.5), ("/categories", "limit", 51),
                       ("/missions", "contribution_type", "SKILL")]
    for path, name, value in parameter_cases:
        parameter = next(p for p in doc["paths"][path]["get"]["parameters"] if p["name"] == name)
        assert not Draft202012Validator(parameter["schema"]).is_valid(value), (path, name, value)
    print(f"PASS: OpenAPI 3.1 validation; {len(actual)} operations; {example_count} request/response/error examples")
    print(f"PASS: {len(cases)} negative schema cases, {len(parameter_cases)} negative query cases; coverage and policy parameters")
    import validate_realtime
    validate_realtime.main()
    import validate_web
    validate_web.main()
    if coverage['remaining_operations']:
        print(f"NOT COMPLETE: {len(coverage['remaining_operations'])} inventory operations still need typed contracts")
    else:
        print("PASS: inventory contract coverage complete; review and runtime gates remain open")
    print("LIMIT: no runtime security, SMS, session reuse, browser CSRF or database behavior tested")
    if args.require_complete and coverage["remaining_operations"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
