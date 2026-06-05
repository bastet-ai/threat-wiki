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
- Keep the landing page updated with a manual “Recent entries” section capped at 10 links.
- If Pages 404s, check the Actions workflow status first; a failed build can look like a site or cert problem.
- As of 2026-03-26, `uvx --from mkdocs-material mkdocs build --strict` emits a `uvx` warning that `mkdocs` comes from the `mkdocs` dependency, but the command still exits `0` and completes the build.
- As of 2026-03-26, `uvx --from mkdocs-material mkdocs build --strict` reports `docs/blog/2026-03-26-teampcp.md` as outside nav, but this is currently info-only and does not fail the local build.

## Verified commands
- `python3 scripts/generate_drafts_from_todo.py`
- `uvx --from mkdocs-material mkdocs build --strict`
- `npm run test:sources` checks the WebLogic source section renders clickable Markdown links and that each external source returns HTTP 200 with the expected CVE token.
- `./contribute.sh --dry-run`

## Maintenance rules
- HackerOne public program checks are currently paused; do not re-enable without explicit instruction.
- `TODO.md` at the repo root is the internal profiling backlog for future `Groups`, `People`, and `Ops` coverage; it is intentionally outside the published docs.
- `drafts/` contains unpublished scaffold pages generated from `TODO.md`; do not confuse them with sourced public wiki content in `docs/`.
- `scripts/select_next_draft.py` picks the next unpublished backlog draft by priority (`ops`, then `groups`, then `people`) based on whether a matching public page exists yet.
- When adding a new group, people, ops, or tool page, update:
  - `mkdocs.yml` nav
  - `docs/index.md` recent entries
  - blog index if it is a notable writeup
- Keep page paths stable once linked publicly.
- Seqrite APT Team posts can be useful primary sources for targeted espionage chains; keep China-linked attribution caveated when Seqrite only gives moderate confidence and no named group.
- Wordfence vulnerability intelligence can be useful for active WordPress plugin exploitation; if direct Wordfence pages return empty locally, use NVD plus secondary reporting that quotes Wordfence telemetry and keep source caveats clear.
- Prefer one well-structured page per group/campaign over scattered notes.
- Maintain `docs/notes/editorial-checklist.md` as a living checklist when the site evolves.
- Maintain `docs/notes/source-index.md` as the canonical list of subscribed RSS/Atom and primary-source feeds.
- The current taxonomy is `Groups`, `People`, `Ops`, `Tools`, `Patterns`, `Notes`, and `Blog`.
- Group pages currently live under `docs/actors/`; keep that path stable unless there is an explicit migration plan.
- There is no top-level `Orgs` section today; document organizations inside the relevant `Ops`, `Groups`, or `Notes` page unless the taxonomy changes.
- When writing an `Ops` page, explicitly investigate whether there is a missing companion `People` or `Groups` page that should be added in the same change.
- Unit 42's CL-CRI-1089 is currently best handled as operation coverage unless multiple sources establish a stable named group profile; Operation FlutterBridge / FlutterShell coverage lives at `docs/ops/operation-flutterbridge-fluttershell-macos-malvertising.md`.
- SideCopy is a stable public group name; Operation XENOFISCAL coverage lives at `docs/ops/operation-xenofiscal-sidecopy-xenorat.md` with a companion `docs/actors/sidecopy.md` profile. Keep Seqrite's medium-to-high confidence wording attached to the source.
- If an `Ops` page overlaps unresolved actor-alias questions, publish the operation first and keep alias caveats attributed in the page unless a separate `Groups` or `People` profile is strongly sourced.
- For `Handala` coverage, use `Handala` as the page title and attribute vendor names (`Void Manticore`, `Storm-0842`, `Red Sandstorm`, `Banished Kitten`) plus linked personas (`Karma`, `Homeland Justice`) inside the page; the March 19, 2026 DOJ domain-seizure release is the most durable official source tying those persona domains to one `MOIS` playbook.
- Use `./contribute.sh` for Codex contribution sweeps; `./contribute.sh 10` should run 10 sequential one-contribution passes that each read `CONTRIBUTING.md`, make a focused addition, and commit/push the result.
- If a recursive `./contribute.sh` run spends several minutes only searching and has not written any repo files yet, stop it and publish the selected draft directly rather than letting a stalled nested Codex session block the backlog.
- Local terminal safety prompts can block bulk HTML scans that include `.dev` domains such as Socket or SafeDep; split source checks or use available RSS/feed paths rather than leaving a cron scan pending approval.
- Microsoft Security Blog article pages may return HTTP 403 to simple `urllib` fetches; a normal browser User-Agent with `curl -o` to a temp file worked for the June 2026 Miasma post. Do not pipe fetched HTML directly into an interpreter.
- JFrog Security Research may publish high-signal real-time posts outside the JFrog Blog RSS feed; include `https://research.jfrog.com/` HTML checks for items such as IronWorm when monitoring supply-chain malware.
- StepSecurity RSS can surface urgent npm worm activity quickly; `binding.gyp`/`node-gyp` install-time execution deserves separate scrutiny from obvious `package.json` lifecycle hooks.
- Google Cloud / Mandiant Threat Intelligence may publish high-signal operation/tool chains where the durable value is the intrusion sequence rather than a full actor profile; for UNC6692 / SNOW, current coverage lives at `docs/ops/unc6692-snow-malware-social-engineering.md` without a separate group profile until broader public actor history justifies one.
- GMO Flatt Security Research can provide durable AI-agent / GitHub Actions trust-boundary research; Claude Code GitHub Action prompt-injection coverage lives at `docs/patterns/claude-code-github-action-prompt-injection.md` and should be treated as a reusable pattern, not a named intrusion.
- Proofpoint Threat Insight is useful for email-driven actor cluster profiles; TA4922 coverage lives at `docs/actors/ta4922.md`. Keep Proofpoint's financially motivated Chinese-speaking cybercrime assessment separate from Silver Fox / Void Arachne overlap unless future sources establish stronger aliasing.
- Arctic Wolf Labs can surface identity-first PhaaS operations where the durable value is the authentication-flow abuse and SaaS expansion rather than malware; Kali365 coverage lives at `docs/ops/kali365-device-code-phishing-expansion.md`.
- Hunt.io and SentinelOne are useful for exposed attacker-infrastructure and cloud-worm follow-ups; PCPJack coverage lives at `docs/ops/pcpjack-cloud-smtp-relay-network.md`, with TeamPCP relationship caveated as adjacency / artifact-removal behavior rather than confirmed shared control.

## Security / attribution
- Treat third-party sources as untrusted until verified.
- When using external reporting, summarize the public reporting and link the source.
- Separate confirmed facts from inferred motivation or team structure.

## Threat-intel monitoring workflow
- Replicate the Skillz-style scan workflow for this repo with a threat-intelligence lens: monitor high-signal sources, add durable actor/operation/tool/pattern pages, update nav/index/blog/feed/source-index, run the strict MkDocs build, commit, push, and notify Dean only when substantive public threat intel was added.
- Current active watch: Shai-Hulud / Mini Shai-Hulud / TeamPCP supply-chain activity. Prioritize new package families, propagation primitives, CI/OIDC abuse paths, persistence mechanisms, exfiltration infrastructure/naming, maintainer postmortems, official advisories, and meaningful attribution changes.
- Track scan state outside the repo at `/home/user/clawd/memory/threat-intel-state.json`; keep this public repo free of private local monitoring state.
- OpenClaw cron job name: `Threat wiki: threat intel scan → wiki updates`; repo path: `/home/user/clawd/threat.wiki`.
