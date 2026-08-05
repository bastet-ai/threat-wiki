#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hooks.recent_entries import (  # noqa: E402
    MAX_RECENT_ENTRIES,
    RecentEntriesError,
    recent_entry_count,
    trim_recent_entries,
)

INDEX = ROOT / "docs/index.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enforce the bounded threat.wiki homepage Recent entries block."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of rewriting when the block exceeds the limit",
    )
    args = parser.parse_args()

    original = INDEX.read_text(encoding="utf-8")
    try:
        count = recent_entry_count(original)
        normalized = trim_recent_entries(original)
    except RecentEntriesError as error:
        print(f"recent entries error: {error}", file=sys.stderr)
        return 2

    if args.check:
        if normalized != original:
            print(
                f"Recent entries has {count} links; maximum is {MAX_RECENT_ENTRIES}. "
                "Run python3 scripts/normalize_recent_entries.py.",
                file=sys.stderr,
            )
            return 1
        print(f"Recent entries is bounded at {count}/{MAX_RECENT_ENTRIES} links.")
        return 0

    if normalized != original:
        INDEX.write_text(normalized, encoding="utf-8")
        print(f"Trimmed Recent entries from {count} to {MAX_RECENT_ENTRIES} links.")
    else:
        print(f"Recent entries already contains {count}/{MAX_RECENT_ENTRIES} links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
