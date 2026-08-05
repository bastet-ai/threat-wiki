from __future__ import annotations

MAX_RECENT_ENTRIES = 10
RECENT_HEADING = "## Recent entries"


class RecentEntriesError(ValueError):
    """Raised when the homepage Recent entries block is malformed."""


def _section_bounds(lines: list[str]) -> tuple[int, int]:
    headings = [index for index, line in enumerate(lines) if line.strip() == RECENT_HEADING]
    if len(headings) != 1:
        raise RecentEntriesError(
            f"expected exactly one {RECENT_HEADING!r} heading, found {len(headings)}"
        )

    start = headings[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def recent_entry_count(markdown: str) -> int:
    lines = markdown.splitlines()
    start, end = _section_bounds(lines)
    section = lines[start:end]
    entries = [line for line in section if line.startswith("- ")]
    unexpected = [line for line in section if line.strip() and not line.startswith("- ")]
    if unexpected:
        raise RecentEntriesError(
            "Recent entries may contain only Markdown list items and blank lines"
        )
    return len(entries)


def trim_recent_entries(markdown: str, limit: int = MAX_RECENT_ENTRIES) -> str:
    if limit < 1:
        raise ValueError("Recent entries limit must be positive")

    had_trailing_newline = markdown.endswith("\n")
    lines = markdown.splitlines()
    start, end = _section_bounds(lines)
    section = lines[start:end]
    entries = [line for line in section if line.startswith("- ")]
    unexpected = [line for line in section if line.strip() and not line.startswith("- ")]
    if unexpected:
        raise RecentEntriesError(
            "Recent entries may contain only Markdown list items and blank lines"
        )

    replacement = entries[:limit]
    if end < len(lines) and replacement:
        replacement.append("")
    lines[start:end] = replacement
    rendered = "\n".join(lines)
    if had_trailing_newline:
        rendered += "\n"
    return rendered
