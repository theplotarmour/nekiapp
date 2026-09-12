"""Check design inventory references; not a usability or implementation test."""

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with (ROOT / "docs/design/screens.tsv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    with (ROOT / "docs/api/operations.tsv").open(encoding="utf-8-sig", newline="") as source:
        operations = list(csv.DictReader(source, delimiter="\t"))
    families = {row["family"] for row in operations} | {"none"}
    surfaces = {"C": "consumer", "V": "volunteer", "O": "organization", "X": "operations", "W": "public-web"}
    profiles = {"BOOT", "AUTH", "READ", "LIST", "FORM", "COMMAND", "CHECKOUT", "TRACKING", "MEDIA", "REVIEW", "REPORT", "WEB"}
    ids, routes, requirements, flows = set(), set(), set(), set()
    for row in rows:
        assert all(isinstance(value, str) and value.strip() for value in row.values()), row
        key = row["screen_id"]
        assert re.fullmatch(r"[CVOXW][0-9]{2}", key) and key not in ids, key
        assert row["surface"] == surfaces[key[0]], key
        route = (row["surface"], row["proposed_route"])
        assert route not in routes and route[1].startswith("/"), route
        assert "?" not in route[1] and "#" not in route[1], route
        assert row["api_family"] in families and row["state_profile"] in profiles, key
        row_requirements = set(row["requirements"].split(","))
        row_flows = set(row["flows"].split(","))
        assert row_requirements <= {f"FR-{n:02}" for n in range(1, 18)}, key
        assert row_flows <= {f"F{n}" for n in range(11)}, key
        ids.add(key); routes.add(route); requirements.update(row_requirements); flows.update(row_flows)
    assert requirements == {f"FR-{n:02}" for n in range(1, 18)}
    assert flows == {f"F{n}" for n in range(11)}
    public_routes = {r["proposed_route"] for r in rows if r["surface"] == "public-web"}
    assert public_routes == {r["path"] for r in operations if r["method"] == "PUBLIC_WEB"}
    doc = (ROOT / "docs/design/screen-state-inventory.md").read_text(encoding="utf-8")
    for referenced_id in re.findall(r"\b[CVOXW][0-9]{2}\b", doc):
        assert referenced_id in ids, referenced_id
    assert all(f"| {profile} |" in doc for profile in profiles)
    print(f"PASS: {len(rows)} unique screen/transport rows; FR-01 through FR-17 and F0 through F10 references; API families and public paths")
    print(dict(Counter(row["surface"] for row in rows)))
    print("LIMIT: reference coverage only; action completeness, prototypes, accessibility and usability remain unverified")


if __name__ == "__main__":
    main()
