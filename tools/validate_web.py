"""Synthetic transport/HTML checks, not policy approval or device association proof."""

import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import contract_web

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags = []; self.canonicals = []; self.data = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag); values = dict(attrs)
        assert tag not in {"script", "iframe", "form"}
        assert not any(name.lower().startswith("on") for name in values)
        if tag == "link" and values.get("rel") == "canonical": self.canonicals.append(values.get("href"))
    def handle_data(self, data):
        self.data.append(data)


def main():
    doc = json.loads((ROOT / "docs/api/web-transports.json").read_text(encoding="utf-8"))
    assert doc == contract_web.document(), "Generated web contract drift"
    registry = Registry().with_resource("urn:neki-web", Resource.from_contents(doc, default_specification=DRAFT202012))
    inventory = {r["operation_id"]: r for r in csv.DictReader((ROOT / "docs/api/operations.tsv").open(encoding="utf-8-sig"), delimiter="\t")}
    coverage = json.loads((ROOT / "docs/api/openapi-coverage.json").read_text(encoding="utf-8"))
    def check(name):
        return Draft202012Validator({"$ref": "urn:neki-web#/schemas/" + name}, registry=registry, format_checker=FormatChecker())
    assert set(doc["operations"]) == {key for key, row in inventory.items() if row["method"] == "PUBLIC_WEB"}
    for key, operation in doc["operations"].items():
        row = inventory[key]
        assert (row["method"], row["path"], row["policy"], row["projection"], row["contract"]) == (operation["inventory_method"], operation["path"], operation["policy"], operation["projection"], operation["source"])
        assert coverage["transport_contracts"][key] == "web-transports.json"
        if "example_response" in operation: check("HtmlResponse").validate(operation["example_response"])
    for schema in doc["schemas"].values(): Draft202012Validator.check_schema(schema)
    count = 0
    for name, examples in doc["examples"].items():
        for value in examples:
            check(name).validate(value); count += 1
            if name == "HtmlResponse":
                parser = PageParser(); parser.feed(value["body"])
                assert parser.tags.count("main") == 1 and parser.tags.count("h1") == 1 and parser.tags.count("title") == 1
                assert len(parser.canonicals) == 1 and parser.canonicals[0].startswith("https://example.invalid/")
    injected = dict(doc["examples"]["PageModel"][0], title='<script>alert("x")</script>', paragraphs=['<img src=x onerror="bad()">'])
    parser = PageParser(); parser.feed(contract_web.render_fixture(injected))
    assert "script" not in parser.tags and "img" not in parser.tags
    assert injected["title"] in "".join(parser.data)
    for name, example in contract_web.negative_cases(): assert not check(name).is_valid(example), name
    print(f"PASS: eight web transports; {count} schema examples; nine rejected cases; seven HTML fixtures and escaped-content check")
    print("LIMIT: synthetic IDs/copy only; no deployed pages, legal approval or actual Android/iOS association verified")


if __name__ == "__main__": main()
