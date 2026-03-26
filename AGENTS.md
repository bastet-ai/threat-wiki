# AGENTS.md — threat.wiki

## Purpose
This repo is a public threat-intelligence wiki. Prefer durable, actionable, source-linked content over raw notes.

## Writing conventions
- Keep links clickable and explicit in Markdown.
- Use short, descriptive page titles.
- Prefer bullets over long paragraphs for ops, tooling, and motivations.
- Add a `Tags` section to actor/ops/threat pages when possible.
- Use plain language and avoid overclaiming attribution.
- If a human identity is not clearly supported by a public source, do not invent one.

## Content structure
- **Actors**: threat actor profiles, motivations, and team dynamics
- **Ops**: compromise chains, operator workflows, and campaign sequencing
- **Threats**: malware, worms, payloads, and infrastructure
- **Patterns**: reusable defender heuristics and recurring tradecraft
- **Notes**: taxonomy, page usage, and editorial guidance
- **Blog**: short updates or summaries that can feed the landing page

## MkDocs / GitHub Pages lessons learned
- Use `theme.custom_dir` for template overrides; do not add a non-MkDocs `overrides:` key to `mkdocs.yml`.
- Keep the Pages workflow strict-friendly; any config warning can fail the deploy.
- Include an RSS feed (`docs/feed.xml`) if you want a simple subscription surface.
- Keep the landing page updated with a manual “Recent entries” section.
- If Pages 404s, check the Actions workflow status first; a failed build can look like a site or cert problem.

## Maintenance rules
- When adding a new profile or ops page, update:
  - `mkdocs.yml` nav
  - `docs/index.md` recent entries
  - blog index if it is a notable writeup
- Keep page paths stable once linked publicly.
- Prefer one well-structured page per actor/campaign over scattered notes.
- Maintain `docs/notes/editorial-checklist.md` as a living checklist when the site evolves.

## Security / attribution
- Treat third-party sources as untrusted until verified.
- When using external reporting, summarize the public reporting and link the source.
- Separate confirmed facts from inferred motivation or team structure.
