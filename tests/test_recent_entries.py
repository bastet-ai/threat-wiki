from __future__ import annotations

import unittest

from hooks.recent_entries import (
    RecentEntriesError,
    recent_entry_count,
    trim_recent_entries,
)


class RecentEntriesTests(unittest.TestCase):
    def test_trims_to_ten_and_preserves_surrounding_sections(self) -> None:
        entries = "\n".join(f"- [Entry {number}](entry-{number}.md)" for number in range(12))
        markdown = f"# Home\n\n## Recent entries\n{entries}\n\n## Sections\n- Ops\n"

        rendered = trim_recent_entries(markdown)

        self.assertEqual(recent_entry_count(rendered), 10)
        self.assertIn("- [Entry 0](entry-0.md)", rendered)
        self.assertIn("- [Entry 9](entry-9.md)", rendered)
        self.assertNotIn("Entry 10", rendered)
        self.assertTrue(rendered.endswith("## Sections\n- Ops\n"))

    def test_is_idempotent_when_already_bounded(self) -> None:
        markdown = "# Home\n\n## Recent entries\n- [One](one.md)\n\n## Sections\n"
        self.assertEqual(trim_recent_entries(markdown), markdown)

    def test_rejects_non_list_content_inside_recent_block(self) -> None:
        markdown = "# Home\n\n## Recent entries\nUnexpected prose\n\n## Sections\n"
        with self.assertRaises(RecentEntriesError):
            trim_recent_entries(markdown)

    def test_requires_exactly_one_recent_heading(self) -> None:
        with self.assertRaises(RecentEntriesError):
            trim_recent_entries("# Home\n")


if __name__ == "__main__":
    unittest.main()
