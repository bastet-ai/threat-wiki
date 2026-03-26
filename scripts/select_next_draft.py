from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = [
    ("ops", ROOT / "drafts" / "ops", ROOT / "docs" / "ops"),
    ("groups", ROOT / "drafts" / "groups", ROOT / "docs" / "actors"),
    ("people", ROOT / "drafts" / "people", ROOT / "docs" / "people"),
]


def extract_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def main() -> int:
    for category, drafts_dir, public_dir in PRIORITY:
        if not drafts_dir.exists():
            continue

        for draft_path in sorted(drafts_dir.glob("*.md")):
            if draft_path.name == "index.md":
                continue

            public_path = public_dir / draft_path.name
            if public_path.exists():
                continue

            title = extract_title(draft_path)
            print(
                "\t".join(
                    [
                        category,
                        draft_path.relative_to(ROOT).as_posix(),
                        public_path.relative_to(ROOT).as_posix(),
                        title,
                    ]
                )
            )
            return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
