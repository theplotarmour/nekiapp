"""Validate custom realtime frame specification, not a running WebSocket service."""

import csv
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import contract_realtime

ROOT = Path(__file__).resolve().parents[1]


def main():
    doc = json.loads((ROOT / "docs/api/realtime.json").read_text(encoding="utf-8"))
    assert doc == contract_realtime.document(), "Generated realtime drift"
    registry = Registry().with_resource("urn:neki-realtime", Resource.from_contents(doc, default_specification=DRAFT202012))
    row = next(r for r in csv.DictReader((ROOT / "docs/api/operations.tsv").open(encoding="utf-8-sig"), delimiter="\t") if r["operation_id"] == doc["operation_id"])
    assert (row["method"], row["path"], row["policy"], row["projection"], row["contract"]) == (doc["inventory_method"], doc["path"], doc["policy"], doc["projection"], doc["source"])
    def check(name):
        return Draft202012Validator({"$ref": "urn:neki-realtime#/schemas/" + name}, registry=registry, format_checker=FormatChecker())
    for schema in doc["schemas"].values():
        Draft202012Validator.check_schema(schema)
    count = 0
    for name, examples in doc["examples"].items():
        for example in examples:
            check(name).validate(example); count += 1
    negative = contract_realtime.negative_cases()
    for name, example in negative:
        assert not check(name).is_valid(example), (name, example)
    coverage = json.loads((ROOT / "docs/api/openapi-coverage.json").read_text(encoding="utf-8"))
    assert coverage["transport_contracts"] == {doc["operation_id"]: "realtime.json"}
    print(f"PASS: realtime inventory mapping; {count} handshake/frame examples; {len(negative)} rejected cases")
    print("LIMIT: no network, ticket-store, browser-origin, revocation or reconnect behavior executed")


if __name__ == "__main__":
    main()
