#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check --require-hashes -r requirements.lock
.venv/bin/python scripts/normalize_recent_entries.py --check
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
.venv/bin/python -m mkdocs build --strict --clean
