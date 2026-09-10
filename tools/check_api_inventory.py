"""Validate the P0 operation inventory, not API implementation or authorization."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "docs" / "api"
FAMILIES = {
    "identity", "preferences", "geo", "catalogue", "discovery", "bookmarks",
    "org_application", "org_missions", "contributions", "payments", "cases",
    "payouts", "skills", "volunteers", "assignments", "logistics", "media",
    "proof", "impact", "notifications", "realtime", "admin",
}
COLUMNS = ["family", "method", "path", "operation_id", "policy", "projection", "profile", "contract"]
METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "WS", "PUBLIC_WEB"}


def table_ids(path: Path, heading: str) -> set[str]:
    section = path.read_text(encoding="utf-8-sig").split(heading, 1)[1].split("\n## ", 1)[0]
    return set(re.findall(r"^\| ([a-z_]+) \|", section, re.MULTILINE))


def main() -> int:
    errors: list[str] = []
    with (API / "operations.tsv").open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            print("FAIL: unexpected inventory columns", file=sys.stderr)
            return 1
        rows = list(reader)

    policies = table_ids(API / "authorization.md", "## Policies")
    projections = table_ids(API / "authorization.md", "## Projection allowlists")
    profiles = table_ids(API / "request-profiles.md", "## Profiles")
    refs: set[str] = set()
    sources = list((ROOT / "docs" / "state-machines").glob("*.md"))
    sources += [ROOT / "docs" / "01-prd.md", ROOT / "docs" / "07-founder-decisions.md",
                ROOT / "docs" / "08-complete-phased-plan.md", API / "README.md"]
    for file in sources:
        refs.update(re.findall(r"\b(?:FR-|PD-|FD-|CD-|LD-|VD-|AP-|VFY|[OMVCPRYSAI]|G|D)\d{1,2}\b",
                               file.read_text(encoding="utf-8-sig")))
    route_seen: set[tuple[str, str]] = set()
    id_seen: set[str] = set()
    counts: Counter[str] = Counter()
    for line, row in enumerate(rows, 2):
        if None in row or any(not row.get(column) for column in COLUMNS):
            errors.append(f"line {line}: missing or extra TSV columns")
            continue
        counts[row["family"]] += 1
        if row["family"] not in FAMILIES:
            errors.append(f"line {line}: unknown family {row['family']}")
        if row["method"] not in METHODS or not row["path"].startswith("/"):
            errors.append(f"line {line}: invalid method/path")
        # Parameter-name differences must not hide conflicting route patterns.
        route = (row["method"], re.sub(r"\{[^}]+\}", "{}", row["path"]))
        if route in route_seen:
            errors.append(f"line {line}: duplicate route pattern {route}")
        route_seen.add(route)
        op = row["operation_id"]
        if op in id_seen or not re.fullmatch(r"[a-z][a-z0-9_]+", op):
            errors.append(f"line {line}: duplicate/invalid operation id {op}")
        id_seen.add(op)
        for column, allowed in [("policy", policies), ("projection", projections), ("profile", profiles)]:
            if row[column] not in allowed:
                errors.append(f"line {line}: unknown {column} {row[column]}")
        for ref in row["contract"].split("/"):
            if ref not in refs:
                errors.append(f"line {line}: unresolved contract reference {ref}")
        if row["method"] == "GET" and row["profile"] not in {"read", "list"}:
            errors.append(f"line {line}: GET has a mutation profile")
        if row["method"] == "WS" and (row["profile"], row["policy"]) != ("socket", "socket"):
            errors.append(f"line {line}: WS requires socket policy/profile")
        if row["policy"] == "public" and row["projection"] not in {"public", "health"}:
            errors.append(f"line {line}: public operation exposes a private projection")
    missing = FAMILIES - counts.keys()
    if missing:
        errors.append(f"missing plan families: {sorted(missing)}")
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(rows)} distinct operations; all {len(FAMILIES)} plan families represented")
    print("PASS: unique routes/IDs, policy/projection/profile references and source identifiers")
    print("LIMIT: structural inventory check only; not OpenAPI/schema, runtime auth or end-to-end proof")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
