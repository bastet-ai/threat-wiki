from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"

# Bare URLs are not reliably clickable in the rendered MkDocs site. Allow
# Markdown targets ([label](https://...)) and explicit autolinks (<https://...>).
# In page `## Sources` sections, keep the full URL visible as the link text:
#   - Vendor report: [https://example.com/report](https://example.com/report)
BARE_URL_RE = re.compile(r"(?<!\]\()(?<!<)(https?://[^\s<>]+)")
AUTOLINK_RE = re.compile(r"<https?://[^>]+>")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def iter_markdown_lines() -> list[tuple[Path, int, str, str]]:
    findings: list[tuple[Path, int, str, str]] = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        in_fence = False
        in_sources = False
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith("## "):
                in_sources = line.strip() == "## Sources"
                continue

            # Skip inline code spans; indicators and example commands inside code
            # should remain literal rather than becoming active links.
            text_segments = line.split("`")[0::2]
            visible_text_segments = [
                AUTOLINK_RE.sub("", MARKDOWN_LINK_RE.sub("", segment))
                for segment in text_segments
            ]
            if any(BARE_URL_RE.search(segment) for segment in visible_text_segments):
                findings.append((path, line_no, line, "bare http(s) URL outside code"))
                continue

            source_style_autolink = (
                line.startswith("- ")
                and "](" not in line
                and len(AUTOLINK_RE.findall(line)) == 1
                and re.search(r"(?:[:—-])\s*<https?://[^>]+>\s*$", line) is not None
            )
            if source_style_autolink:
                findings.append((path, line_no, line, "source citation uses raw autolink instead of full-URL markdown link"))
                continue

            if in_sources:
                for label, url in MARKDOWN_LINK_RE.findall(line):
                    if label != url:
                        findings.append((path, line_no, line, "source markdown link text is not the full URL"))
                        break
    return findings


def main() -> int:
    findings = iter_markdown_lines()
    if not findings:
        print("Clickable-link audit passed: source links expose full URLs and no bare http(s) URLs appear outside code blocks/spans.")
        return 0

    print("Clickable-link audit failed.", file=sys.stderr)
    for path, line_no, line, reason in findings:
        rel = path.relative_to(ROOT)
        print(f"{rel}:{line_no}: {reason}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
