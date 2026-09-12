"""Regenerate the isolated Flutter fixture and normalize generated whitespace."""

import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent / "spikes/flutter_stack"
dart = "dart.bat" if os.name == "nt" else "dart"
subprocess.run([dart, "run", "build_runner", "build", "--delete-conflicting-outputs"], cwd=root, check=True)
subprocess.run([dart, "format", "lib", "test", "web/worker.dart"], cwd=root, check=True)
for path in (root / "lib").glob("*.dart"):
    if path.name.endswith((".g.dart", ".freezed.dart")):
        # Freezed disables dart format inside its generated file.
        text = path.read_text(encoding="utf-8")
        normalized = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        path.write_text(normalized, encoding="utf-8", newline="\n")
print("Generated Dart sources and whitespace normalization complete")
