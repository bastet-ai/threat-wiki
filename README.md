# threat.wiki

Public threat-intelligence wiki for Bastet.

## Scope

This repo is a public, source-linked wiki for durable threat-intelligence coverage.

It is meant to capture:
- threat groups, crews, and shared operator personas
- clearly sourced named people with operational relevance
- operations and compromise timelines
- malware, payloads, worms, and attacker infrastructure
- reusable patterns and editorial notes that help future coverage stay consistent

It is not meant to be:
- a raw note dump
- a rumor tracker
- a place for unsupported human attribution
- a place where one campaign is scattered across many half-pages

## Taxonomy

The current site taxonomy is:
- `Groups`
- `People`
- `Ops`
- `Tools`
- `Patterns`
- `Notes`
- `Blog`

## Taxonomy quirks

- We use `Groups` and `People` instead of a single `Actors` bucket.
- Existing published group pages currently live under `docs/actors/` even though the site labels them as `Groups`. That path is stable until there is an explicit migration plan.
- We use `Tools` for malware, worms, payloads, loaders, and attacker infrastructure instead of a `Threats` section.
- There is no top-level `Orgs` section today. Organizations, projects, vendors, and victims should usually be documented inside the relevant `Ops`, `Groups`, or `Notes` pages unless the taxonomy changes later.
- `People` pages require clear public sourcing. Do not turn a handle, alias, or social-media claim into a human identity without strong public support.

## Repo layout

- [`docs/`](docs/) contains the published wiki content
- [`docs/notes/how-to-use.md`](docs/notes/how-to-use.md) defines section usage
- [`docs/notes/editorial-checklist.md`](docs/notes/editorial-checklist.md) is the publishing checklist
- [`mkdocs.yml`](mkdocs.yml) defines nav and site config
- [`overrides/`](overrides/) and [`docs/stylesheets/extra.css`](docs/stylesheets/extra.css) control the site theme

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contributor workflow, sourcing rules, and how to identify missing groups, people, orgs, or ops.

## Local verification

Verified command:
- `uvx --from mkdocs-material mkdocs build --strict`
