from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
TODO_FILE = ROOT / "TODO.md"
DRAFTS_DIR = ROOT / "drafts"

CATEGORIES = {
    "Groups": "groups",
    "People": "people",
    "Ops": "ops",
}

ITEM_RE = re.compile(r"^- \[ \] (.+)$")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.replace("&", " and ")
    value = value.replace("/", " ")
    value = value.replace(":", " ")
    value = value.replace("`", "")
    value = value.replace("→", " ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def parse_todo() -> dict[str, list[dict[str, str]]]:
    items: dict[str, list[dict[str, str]]] = defaultdict(list)
    current_category: str | None = None
    current_section: str | None = None

    for raw_line in TODO_FILE.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("## "):
            heading = raw_line[3:].strip()
            current_category = heading if heading in CATEGORIES else None
            current_section = None
            continue

        if current_category and raw_line.startswith("### "):
            current_section = raw_line[4:].strip()
            continue

        if not current_category:
            continue

        match = ITEM_RE.match(raw_line)
        if not match:
            continue

        items[current_category].append(
            {
                "label": match.group(1).strip(),
                "section": current_section or "Uncategorized",
            }
        )

    for category, category_items in items.items():
        seen: dict[str, int] = defaultdict(int)
        for item in category_items:
            base_slug = slugify(item["label"])
            seen[base_slug] += 1
            suffix = "" if seen[base_slug] == 1 else f"-{seen[base_slug]}"
            item["slug"] = f"{base_slug}{suffix}"

    return items


def draft_readme() -> str:
    return """# Drafts

Unpublished draft scaffolds generated from [`TODO.md`](../TODO.md).

These files are internal working pages, not finished public wiki entries. Use them to collect naming decisions, aliases, sources, timelines, and related links before promoting material into [`docs/`](../docs/).

## Sections

- [Groups drafts](groups/index.md)
- [People drafts](people/index.md)
- [Ops drafts](ops/index.md)

## Regenerate

- `python3 scripts/generate_drafts_from_todo.py`
"""


def category_index(category: str, items: list[dict[str, str]]) -> str:
    lines = [
        f"# {category} drafts",
        "",
        "Internal draft scaffolds generated from [`TODO.md`](../../TODO.md).",
        "",
        "Do not treat these files as published coverage. Promote material into `docs/` only after it is sourced and reviewed.",
    ]

    sections: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in items:
        sections[item["section"]].append(item)

    for section, section_items in sections.items():
        lines.extend(["", f"## {section}"])
        for item in section_items:
            lines.append(f"- [{item['label']}]({item['slug']}.md)")

    lines.append("")
    return "\n".join(lines)


def group_template(item: dict[str, str]) -> str:
    return f"""# {item['label']}

Status: internal draft scaffold generated from [`TODO.md`](../../TODO.md). Do not publish or move this into `docs/` until it is sourced and reviewed.

## Scope
- Backlog bucket: `{item['section']}`
- TODO: define the boundary of this group, crew, cluster, or shared persona.
- TODO: decide whether this label should remain the primary title or be replaced by a more firsthand source-supported name.

## Naming
- TODO: choose the primary title using operator, maintainer, project, or other firsthand source naming when durable public sourcing supports it.
- TODO: list alternate names, who used them, and the report or advisory link for each alias.

## Summary
- TODO

## Activity and tradecraft
- TODO

## Related ops
- TODO

## Related people
- TODO

## Sources
- TODO
"""


def people_template(item: dict[str, str]) -> str:
    return f"""# {item['label']}

Status: internal draft scaffold generated from [`TODO.md`](../../TODO.md). Do not publish or move this into `docs/` until it is sourced and reviewed.

## Identity scope
- Backlog bucket: `{item['section']}`
- TODO: define whether this page tracks a real-world individual, a GitHub persona, a maintainer identity, or another public operational persona.
- TODO: narrow or split the page if this backlog item should become multiple people pages instead of one.

## Naming
- TODO: choose the primary title using operator, maintainer, project, or other firsthand source naming when durable public sourcing supports it.
- TODO: list alternate names, who used them, and the report or advisory link for each alias.

## Operational relevance
- TODO

## Related groups and ops
- TODO

## Sources
- TODO
"""


def ops_template(item: dict[str, str]) -> str:
    return f"""# {item['label']}

Status: internal draft scaffold generated from [`TODO.md`](../../TODO.md). Do not publish or move this into `docs/` until it is sourced and reviewed.

## Summary
- Backlog bucket: `{item['section']}`
- TODO: define the specific breach, compromise chain, or campaign scope this page should cover.

## Naming
- TODO: prefer the name used by operators, maintainers, victims, or other firsthand sources when durable public sourcing supports it.
- TODO: if alternate vendor or researcher names matter, attribute each alias to the report or advisory that used it.

## Timeline
- TODO

## Related groups and people
- TODO

## Defender takeaways
- TODO

## Sources
- TODO
"""


TEMPLATES = {
    "Groups": group_template,
    "People": people_template,
    "Ops": ops_template,
}


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    items_by_category = parse_todo()

    write_if_missing(DRAFTS_DIR / "README.md", draft_readme())

    for category, dirname in CATEGORIES.items():
        category_dir = DRAFTS_DIR / dirname
        category_dir.mkdir(parents=True, exist_ok=True)
        items = items_by_category.get(category, [])
        desired_names = {"index.md"} | {f"{item['slug']}.md" for item in items}

        for existing in category_dir.glob("*.md"):
            if existing.name not in desired_names:
                existing.unlink()

        (category_dir / "index.md").write_text(
            category_index(category, items),
            encoding="utf-8",
        )

        template = TEMPLATES[category]
        for item in items:
            draft_path = category_dir / f"{item['slug']}.md"
            write_if_missing(draft_path, template(item))


if __name__ == "__main__":
    main()
