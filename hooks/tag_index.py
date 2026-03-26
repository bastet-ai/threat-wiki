from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import posixpath
import re

from markdown.extensions.toc import slugify as md_slugify


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
TAG_INDEX_SRC_URI = "notes/tag-index.md"
TAG_INDEX_FILE = DOCS_DIR / TAG_INDEX_SRC_URI
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def slugify_tag(tag: str) -> str:
    return md_slugify(tag, "-")


def find_tags_section(markdown: str) -> tuple[list[str], int, int] | None:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "## Tags":
            continue

        tags: list[str] = []
        end_index = index + 1
        while end_index < len(lines):
            stripped = lines[end_index].strip()
            if not stripped.startswith("- "):
                break
            tags.append(stripped[2:].strip())
            end_index += 1

        if tags:
            return tags, index + 1, end_index

    return None


def parse_tags(markdown: str) -> list[str]:
    section = find_tags_section(markdown)
    if not section:
        return []
    return section[0]


def extract_title(markdown: str, fallback: str) -> str:
    match = TITLE_RE.search(markdown)
    if match:
        return match.group(1).strip()
    return fallback


def iter_tagged_pages() -> list[tuple[str, str, list[str]]]:
    pages: list[tuple[str, str, list[str]]] = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        src_uri = path.relative_to(DOCS_DIR).as_posix()
        if src_uri == TAG_INDEX_SRC_URI:
            continue

        markdown = path.read_text(encoding="utf-8")
        tags = parse_tags(markdown)
        if not tags:
            continue

        title = extract_title(markdown, path.stem.replace("-", " ").title())
        pages.append((src_uri, title, tags))
    return pages


def build_tag_index_markdown() -> str:
    tags_to_pages: dict[str, list[tuple[str, str]]] = defaultdict(list)
    notes_dir = posixpath.dirname(TAG_INDEX_SRC_URI)

    for src_uri, title, tags in iter_tagged_pages():
        relative_link = posixpath.relpath(src_uri, start=notes_dir)
        for tag in tags:
            tags_to_pages[tag].append((title, relative_link))

    lines = [
        "# Tag index",
        "",
        "Generated from page-level `## Tags` sections. Each tag below links to the pages that currently use it.",
        "",
        "## All tags",
    ]

    for tag in sorted(tags_to_pages, key=str.casefold):
        lines.append(f"- [{tag}](#{slugify_tag(tag)}) ({len(tags_to_pages[tag])})")

    for tag in sorted(tags_to_pages, key=str.casefold):
        lines.extend(
            [
                "",
                f"## {tag}",
            ]
        )
        for title, relative_link in sorted(tags_to_pages[tag], key=lambda item: item[0].casefold()):
            lines.append(f"- [{title}]({relative_link})")

    lines.append("")
    return "\n".join(lines)


def on_pre_build(**kwargs) -> None:
    TAG_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    rendered = build_tag_index_markdown()
    existing = TAG_INDEX_FILE.read_text(encoding="utf-8") if TAG_INDEX_FILE.exists() else None
    if rendered != existing:
        TAG_INDEX_FILE.write_text(rendered, encoding="utf-8")


def on_page_markdown(markdown: str, page, **kwargs) -> str:
    if page.file.src_uri == TAG_INDEX_SRC_URI:
        return markdown

    section = find_tags_section(markdown)
    if not section:
        return markdown

    page_dir = posixpath.dirname(page.file.src_uri) or "."
    tag_index_link = posixpath.relpath(TAG_INDEX_SRC_URI, start=page_dir)
    tags, start_index, end_index = section
    lines = markdown.splitlines()
    lines[start_index:end_index] = [
        f"- [{tag}]({tag_index_link}#{slugify_tag(tag)})"
        for tag in tags
    ]

    rendered = "\n".join(lines)
    if markdown.endswith("\n"):
        rendered += "\n"
    return rendered
