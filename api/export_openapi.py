"""Export only the routes implemented by FastAPI; unimplemented P0 contracts stay drafts."""

import argparse
import json
from pathlib import Path

from neki_api.config import Settings
from neki_api.main import create_app

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
app = create_app(
    Settings(environment="test", database_url="postgresql+psycopg://export@localhost/export")
)
content = json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"
target = Path(__file__).with_name("openapi.json")
if args.check:
    if not target.exists() or target.read_text(encoding="utf8") != content:
        raise SystemExit("Runtime OpenAPI drift; regenerate api/openapi.json")
else:
    target.write_text(content, encoding="utf8")
print("Runtime OpenAPI: 2 implemented platform routes")
