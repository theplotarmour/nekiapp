"""Fetch the exact Drift web SQLite artifact, with the release-published digest."""

import hashlib
from pathlib import Path
from urllib.request import urlopen

URL = "https://github.com/simolus3/drift/releases/download/drift-2.35.0/sqlite3.wasm"
SHA256 = "13d3f11d05b39ba0618a7115fb41640a5d48b6300f5d3f325f554b42bd6688a4"
target = Path(__file__).resolve().parent / "spikes/flutter_stack/web/sqlite3.wasm"
if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == SHA256:
    print("PASS: matching SQLite Wasm artifact already present")
else:
    with urlopen(URL, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit("SQLite Wasm digest mismatch; artifact not written")
    target.write_bytes(data)
    print("PASS: downloaded release-pinned SQLite Wasm artifact and verified SHA-256")
