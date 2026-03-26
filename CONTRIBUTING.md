# Contributing

Help expand coverage by finding and documenting missing groups, people, orgs, and ops with durable, source-linked writeups.

## What to contribute

Prioritize contributions that close obvious coverage gaps:
- missing **groups**: crews, clusters, or shared personas that already appear in reporting or in existing ops pages but do not have a dedicated profile
- missing **people**: GitHub usernames, maintainer personas, or publicly identified individuals with direct operational relevance when public sourcing clearly supports them
- missing **orgs**: projects, vendors, maintainers, or victims that matter to understanding an operation but are only partially documented
- missing **ops**: compromise chains or campaign timelines that have enough public reporting to support a concise, durable page

## Before you write

- Search the repo first so you do not duplicate an existing page.
- Prefer primary sources and investigative writeups over commentary.
- Make sure the subject is supported well enough to survive beyond one news cycle.
- Prefer one strong page over several thin stubs.

## Taxonomy guide

Use the current sections consistently:
- **Groups**: named crews, clusters, or shared operational personas
- **People**: publicly identified individuals or project personas only when public sourcing clearly supports the identity
- **Ops**: compromise chains, campaign sequencing, and operational timelines
- **Tools**: malware, loaders, payloads, implants, worms, and attacker infrastructure
- **Patterns**: reusable heuristics and recurring tradecraft
- **Notes**: taxonomy, editorial guidance, and reference material
- **Blog**: short updates or summaries that support discoverability

## Taxonomy quirks

- The site uses `Groups` and `People` instead of a combined `Actors` section.
- Group pages currently live under `docs/actors/` for path stability. Use that path unless there is an explicit migration plan.
- A `People` page may use a GitHub username or project persona as the page title when that is the strongest public identifier. Do not upgrade that into a verified offline identity without stronger sourcing.
- There is no top-level `Orgs` section today. Put organization context in the most relevant `Ops`, `Groups`, or `Notes` page.
- `Tools` is the bucket for malware and attacker infrastructure, even if another project might call that `Threats`.

## Writing rules

- Keep links clickable and explicit in Markdown.
- Use short, descriptive page titles.
- Prefer bullets over long paragraphs for ops, tooling, and motivations.
- Add a `Tags` section to group, people, ops, and tool pages when useful.
- Separate confirmed facts from inference.
- Do not invent a human identity when public sources only support a group, alias, or persona.

## Companion pages

When you add or expand an `Ops` page, explicitly check whether there is also a missing companion `People` or `Groups` page:
- add the companion page in the same contribution when the relationship is operationally central and public sourcing is strong
- prefer a GitHub username, maintainer persona, or other public handle when that is the clearest supported identifier
- keep unsupported real-world identity claims inside the op context or leave them out entirely

## When adding a new page

If you add a new group, people, ops, or tool page, also update:
- [`mkdocs.yml`](mkdocs.yml) nav
- [`docs/index.md`](docs/index.md) recent entries
- [`docs/blog/index.md`](docs/blog/index.md) if the writeup is notable

Keep page paths stable once linked publicly.

## How to handle missing orgs

Because there is no dedicated `Orgs` section yet:
- add the organization context to the relevant `Ops` page if it explains the compromise chain or impact
- add it to a `Groups` page if the organization is central to the group’s targeting or operating history
- add it to `Notes` only when the information is editorial, taxonomic, or reference-oriented

If you find repeated need for standalone organization coverage, raise that as a taxonomy change rather than inventing an ad hoc section.

## Review checklist

Before you submit:
- run through [`docs/notes/editorial-checklist.md`](docs/notes/editorial-checklist.md)
- make sure sources are linked inline
- make sure facts and inference are clearly separated
- make sure any named person is strongly and publicly sourced
- make sure any new op was checked for an associated missing group or people page

## Local verification

Verified command:
- `uvx --from mkdocs-material mkdocs build --strict`
