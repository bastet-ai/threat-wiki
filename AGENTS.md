# AGENTS.md — threat.wiki

## Purpose
This repo is a public threat-intelligence wiki. Prefer durable, actionable, source-linked content over raw notes.

## Agent workflow
- Read this file at the start of each task.
- Update this file whenever you learn something important about the repo, workflow, build, or collaborator preferences.
- After every meaningful repo update, create a git commit and push it to `origin` unless the user explicitly tells you not to.
- Use clear, non-interactive git commands and keep commit messages specific to the change.

## Recursive self-improvement
Follow the [Recurse.bot guide](https://recurse.bot/) approach: treat `AGENTS.md` as the project memory for future agents.

- Record wins to repeat and mistakes to avoid.
- Capture exact build, test, and publish commands that were actually verified.
- Note project-specific conventions, taxonomy decisions, and stable public paths.
- Record collaborator preferences that materially improve future handoffs.
- Keep entries concise, concrete, and easy to scan.

## Writing conventions
- Keep links clickable and explicit in Markdown.
- Use short, descriptive page titles.
- Prefer bullets over long paragraphs for ops, tooling, and motivations.
- Add a `Tags` section to group/people/ops/tool pages when possible.
- Use plain language and avoid overclaiming attribution.
- Prefer names used by the operators, maintainers, projects, or other firsthand sources over later threat-intel vendor branding when a durable public source supports that choice.
- When alternative names matter, attribute them to the vendor or report that coined or used them and link the source.
- A `People` page may use a GitHub username or project persona as the title when that is the clearest publicly supported identifier.
- If a human identity is not clearly supported by a public source, do not invent one.

## Content structure
- **Groups**: named crews, clusters, and shared operational personas
- **People**: publicly identified individuals with direct operational relevance
- **Ops**: compromise chains, operator workflows, and campaign sequencing
- **Tools**: malware, worms, payloads, and attacker infrastructure
- **Patterns**: reusable defender heuristics and recurring tradecraft
- **Notes**: taxonomy, page usage, and editorial guidance
- **Blog**: short updates or summaries that can feed the landing page

## MkDocs / GitHub Pages lessons learned
- Use `theme.custom_dir` for template overrides; do not add a non-MkDocs `overrides:` key to `mkdocs.yml`.
- Keep the Pages workflow strict-friendly; any config warning can fail the deploy.
- Include an RSS feed (`docs/feed.xml`) if you want a simple subscription surface.
- `docs/blog/index.md` is a hand-curated discovery surface and can link directly to notable group, ops, or tool pages without requiring a separate `docs/blog/*.md` post.
- `docs/feed.xml` is manually maintained; linking a new page from `docs/blog/index.md` does not update the feed automatically.
- `hooks/tag_index.py` rewrites page `## Tags` lists into clickable links at build time and regenerates `docs/notes/tag-index.md`; commit the regenerated page when tags change.
- Keep the landing page updated with a manual “Recent entries” section.
- If Pages 404s, check the Actions workflow status first; a failed build can look like a site or cert problem.
- As of 2026-03-26, `uvx --from mkdocs-material mkdocs build --strict` emits a `uvx` warning that `mkdocs` comes from the `mkdocs` dependency, but the command still exits `0` and completes the build.
- As of 2026-03-26, `uvx --from mkdocs-material mkdocs build --strict` reports `docs/blog/2026-03-26-teampcp.md` as outside nav, but this is currently info-only and does not fail the local build.

## Verified commands
- `python3 scripts/generate_drafts_from_todo.py`
- `uvx --from mkdocs-material mkdocs build --strict`
- `./contribute.sh --dry-run`

## Maintenance rules
- `TODO.md` at the repo root is the internal profiling backlog for future `Groups`, `People`, and `Ops` coverage; it is intentionally outside the published docs.
- `drafts/` contains unpublished scaffold pages generated from `TODO.md`; do not confuse them with sourced public wiki content in `docs/`.
- `scripts/select_next_draft.py` picks the next unpublished backlog draft by priority (`ops`, then `groups`, then `people`) based on whether a matching public page exists yet.
- When adding a new group, people, ops, or tool page, update:
  - `mkdocs.yml` nav
  - `docs/index.md` recent entries
  - blog index if it is a notable writeup
- Keep page paths stable once linked publicly.
- Prefer one well-structured page per group/campaign over scattered notes.
- Maintain `docs/notes/editorial-checklist.md` as a living checklist when the site evolves.
- Maintain `docs/notes/source-index.md` as the canonical list of subscribed RSS/Atom and primary-source feeds.
- The current taxonomy is `Groups`, `People`, `Ops`, `Tools`, `Patterns`, `Notes`, and `Blog`.
- Group pages currently live under `docs/actors/`; keep that path stable unless there is an explicit migration plan.
- There is no top-level `Orgs` section today; document organizations inside the relevant `Ops`, `Groups`, or `Notes` page unless the taxonomy changes.
- When writing an `Ops` page, explicitly investigate whether there is a missing companion `People` or `Groups` page that should be added in the same change.
- If an `Ops` page overlaps unresolved actor-alias questions, publish the operation first and keep alias caveats attributed in the page unless a separate `Groups` or `People` profile is strongly sourced.
- Use `./contribute.sh` for Codex contribution sweeps; `./contribute.sh 10` should run 10 sequential one-contribution passes that each read `CONTRIBUTING.md`, make a focused addition, and commit/push the result.
- If a recursive `./contribute.sh` run spends several minutes only searching and has not written any repo files yet, stop it and publish the selected draft directly rather than letting a stalled nested Codex session block the backlog.

## Security / attribution
- Treat third-party sources as untrusted until verified.
- When using external reporting, summarize the public reporting and link the source.
- Separate confirmed facts from inferred motivation or team structure.
