#!/usr/bin/env python3
"""Regenerate docs/notes/tag-index.md from page-level `## Tags` sections.

Preserves the established format:
  - `## All tags` list: `- [tag](#anchor) (count)` sorted by Unicode codepoints
    (case-sensitive, as in the existing file).
  - one `## <tag>` section per tag, bullets `- [<page H1>](<relative-path>)`
    sorted by Unicode codepoints of the H1 text.

Page paths in bullets are relative to docs/notes/ (e.g. `../ops/foo.md`).
"""
import os
import re
import sys
import unicodedata


def _slugify(value: str) -> str:
    """MkDocs-Material TOC anchor style: lowercase, keep word chars / hyphens /
    underscores, drop all other punctuation, collapse whitespace to a single
    hyphen (matches the committed tag-index, e.g. ``#2fa-bypass``,
    ``#gl_introduced``)."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("utf-8")
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s_-]", "", value)
    value = re.sub(r"\s+", "-", value)
    return value.strip("-")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "notes", "tag-index.md")

# Pages to skip from the tag index (meta/notes pages don't carry operational tags).
SKIP_DIRS = ("notes",)


def anchor(tag: str) -> str:
    return _slugify(tag)


def iter_pages():
    for dirpath, dirnames, filenames in os.walk(DOCS):
        rel = os.path.relpath(dirpath, DOCS)
        parts = rel.split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            yield os.path.join(dirpath, fn)


def main():
    pages = []
    for path in iter_pages():
        text = open(path, encoding="utf-8").read()
        m = re.search(r"^## Tags\s*$(.*?)(?=^## )", text, re.M | re.S)
        if not m:
            continue
        tags = [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ") and l[2:].strip()]
        if not tags:
            continue
        h1m = re.match(r"^#\s+(.+?)\s*$", text, re.M)
        title = h1m.group(1) if h1m else os.path.splitext(os.path.basename(path))[0]
        rel = os.path.relpath(path, os.path.join(DOCS, "notes"))
        pages.append((tags, title, rel))

    tagmap = {}
    for tags, title, rel in pages:
        for t in tags:
            tagmap.setdefault(t, set()).add((title, rel))

    all_tags = sorted(tagmap.keys(), key=lambda t: t.lower())
    lines = ["# Tag index", "", "Generated from page-level `## Tags` sections. Each tag below links to the pages that currently use it.", "", "## All tags"]
    for t in all_tags:
        lines.append(f"- [{t}](#{anchor(t)}) ({len(tagmap[t])})")
    for t in all_tags:
        lines.append("")
        lines.append(f"## {t}")
        for title, rel in sorted(tagmap[t], key=lambda x: x[0].lower()):
            lines.append(f"- [{title}]({rel})")
    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"OK: {len(all_tags)} tags, {len(pages)} pages -> {OUT}")


if __name__ == "__main__":
    main()
