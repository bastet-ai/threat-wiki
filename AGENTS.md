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
- Keep the landing page updated with a manual “Recent entries” section.
- If Pages 404s, check the Actions workflow status first; a failed build can look like a site or cert problem.

## Verified commands
- `uvx --from mkdocs-material mkdocs build --strict`

## Maintenance rules
- When adding a new group, people, ops, or tool page, update:
  - `mkdocs.yml` nav
  - `docs/index.md` recent entries
  - blog index if it is a notable writeup
- Keep page paths stable once linked publicly.
- Prefer one well-structured page per group/campaign over scattered notes.
- Maintain `docs/notes/editorial-checklist.md` as a living checklist when the site evolves.
- Maintain `docs/notes/source-index.md` as the canonical list of subscribed RSS/Atom and primary-source feeds.
- The current taxonomy is `Groups`, `People`, `Ops`, `Tools`, `Patterns`, `Notes`, and `Blog`.
- Keep the existing `docs/actors/` path stable for already-published group pages unless there is an explicit migration plan.

## Security / attribution
- Treat third-party sources as untrusted until verified.
- When using external reporting, summarize the public reporting and link the source.
- Separate confirmed facts from inferred motivation or team structure.
