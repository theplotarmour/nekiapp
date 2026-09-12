"""Verify pinned static research evidence without running upstream application code."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("research_root", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "docs/rnd/open-source-snapshots.json").read_text(encoding="utf-8"))
    assert [row["id"] for row in manifest["repositories"]] == list("ABCDEFGH")
    count = 0
    for row in manifest["repositories"]:
        checkout = args.research_root / row["id"]
        def git(*arguments):
            return subprocess.check_output(["git", *arguments], cwd=checkout)
        assert git("rev-parse", "HEAD").decode().strip() == row["commit"], row["id"]
        assert git("show", "-s", "--format=%cI").decode().strip() == row["commit_date"]
        files = git("ls-tree", "-r", "--name-only", row["commit"]).decode().splitlines()
        licenses = [f for f in files if Path(f).name.lower().startswith(("license", "copying"))]
        tests = [f for f in files if f.endswith("_test.dart") or ".test." in f or ".spec." in f or "/__tests__/" in f]
        assert licenses == row["license_files"], row["id"]
        assert tests == row["test_files"], row["id"]
        for evidence in row["evidence_files"]:
            content = git("show", f"{row['commit']}:{evidence['path']}")
            assert hashlib.sha256(content).hexdigest() == evidence["sha256_git_blob"], evidence["path"]
            assert evidence["url"] == f"{row['url']}/blob/{row['commit']}/{evidence['path']}"
            count += 1
    print(f"PASS: eight pinned source revisions; {count} Git-blob hashes; license/test inventories")
    print("LIMIT: static provenance only; upstream builds/tests and NEKI compatibility not executed")


if __name__ == "__main__":
    main()
