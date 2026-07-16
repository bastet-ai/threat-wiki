from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"

# Bare URLs are not reliably clickable in the rendered MkDocs site. Allow
# Markdown targets ([label](https://...)) and explicit autolinks (<https://...>).
BARE_URL_RE = re.compile(r"(?<!\]\()(?<!<)(https?://[^\s<>]+)")


def iter_markdown_lines() -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        in_fence = False
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            # Skip inline code spans; indicators and example commands inside code
            # should remain literal rather than becoming active links.
            text_segments = line.split("`")[0::2]
            if any(BARE_URL_RE.search(segment) for segment in text_segments):
                findings.append((path, line_no, line))
    return findings


def main() -> int:
    findings = iter_markdown_lines()
    if not findings:
        print("Clickable-link audit passed: no bare http(s) URLs outside code blocks/spans.")
        return 0

    print("Clickable-link audit failed: bare http(s) URLs found outside code blocks/spans.", file=sys.stderr)
    for path, line_no, line in findings:
        rel = path.relative_to(ROOT)
        print(f"{rel}:{line_no}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
