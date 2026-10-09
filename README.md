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
- For naming, prefer operator-, maintainer-, project-, or other firsthand source usage over later vendor brands when public sourcing clearly supports it. Attribute alternate names to the report or vendor that used them.
- `People` pages require clear public sourcing. Do not turn a handle, alias, or social-media claim into a human identity without strong public support.

## Repo layout

- [`docs/`](docs/) contains the published wiki content
- [`TODO.md`](TODO.md) is the internal backlog for future group, people, and ops profiling
- [`drafts/`](drafts/) contains unpublished scaffold pages generated from the backlog
- [`scripts/generate_drafts_from_todo.py`](scripts/generate_drafts_from_todo.py) regenerates internal draft scaffolds from `TODO.md`
- [`scripts/select_next_draft.py`](scripts/select_next_draft.py) selects the next unpublished draft to promote into `docs/`
- [`docs/notes/how-to-use.md`](docs/notes/how-to-use.md) defines section usage
- [`docs/notes/editorial-checklist.md`](docs/notes/editorial-checklist.md) is the publishing checklist
- [`mkdocs.yml`](mkdocs.yml) defines nav and site config
- [`overrides/`](overrides/) and [`docs/stylesheets/extra.css`](docs/stylesheets/extra.css) control the site theme

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contributor workflow, sourcing rules, and how to identify missing groups, people, orgs, or ops.

## Local verification

```bash
npm ci
npm run build
npm run deploy:check
npm run test:hosting
npm run dev
```

`npm run build` creates an isolated `.venv`, installs the hash-locked Python
renderer, checks the bounded homepage recents, runs the Python unit tests, and
builds MkDocs strictly into `site/`. Local Workers hosting uses port 8787.

## Cloudflare publishing

The `threat-wiki` Worker serves `site/` through Workers Static Assets. Directory
URLs, group paths under `actors/`, search, the manually maintained feed, template
overrides, and the custom 404 are preserved. Internal `TODO.md`, `drafts/`, source,
and build files are not published. This static site needs no runtime secrets or
database. Wrangler enables Worker logs/traces, but asset-only requests bypass
Worker execution; use Cloudflare HTTP analytics for site traffic.

Cloudflare [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/)
connects `bastet-ai/threat-wiki` to the `threat-wiki` Worker. Every push to `main`
triggers Cloudflare to fetch, build, and deploy the repository with these settings:

- Production branch: `main`
- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Root directory: `/` (repository root)
- Included paths: `*`
- Preview builds: disabled
- Node.js and Python versions: the checked-in `.node-version` and `.python-version`

Cloudflare stores the deployment credential; no Cloudflare secrets are needed in
GitHub. For a normal update, run the validation commands above, commit and push to
`main`, then wait for the Cloudflare build for that commit and verify the public site.

For a deliberate manual recovery, first pause automatic builds in Cloudflare and
wait for any running build to finish. Use an up-to-date `main` checkout and run the
validation commands above before deploying:

```bash
npm run deploy
```

Verify the recovered site before re-enabling automatic builds. Never overlap a
manual production deployment with an automatic build.

GitHub Actions validates and saves the site artifact only; it does not publish to
GitHub Pages. The previous Pages deployment remains available for rollback.
Preview: [threat-wiki.bcrt43.workers.dev](https://threat-wiki.bcrt43.workers.dev/).
Production: [threat.wiki](https://threat.wiki/), attached as an exact custom domain
in `wrangler.jsonc`. The September 2026 cutover changeset added only this hostname
with no conflicting DNS records. Preserve unrelated MX/TXT/DNS records in future
changes. To roll back, first detach this exact custom domain and restore its
previous GitHub Pages DNS configuration; do not delete the zone or Pages deployment.
