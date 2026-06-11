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
- ReliaQuest Threat Research can surface durable incident-response-backed actor clusters and IIS/web-shell tradecraft; OP-512 coverage lives at `docs/actors/op-512.md`, with China-linked attribution kept to ReliaQuest's moderate-to-high-confidence assessment and aliasing kept separate until future public reporting supports it.
- Microsoft Security Blog can provide primary-source AI-agent CI/CD trust-boundary research; the June 5, 2026 Claude Code Action case adds `/proc/self/environ` Read-tool exposure to `docs/patterns/claude-code-github-action-prompt-injection.md` alongside the earlier GMO Flatt GitHub App / issue-triage boundary coverage.
- CISA KEV additions for internet-facing managed-file-transfer or edge services can justify concise ops pages even when public impact is availability-only; SolarWinds Serv-U CVE-2026-28318 coverage lives at `docs/ops/solarwinds-serv-u-cve-2026-28318-exploitation.md`.
- Cisco SD-WAN Manager exploitation advisories can justify concise edge/control-plane ops pages when Cisco confirms exploitation and no direct fix/workaround exists; CVE-2026-20245 coverage lives at `docs/ops/cisco-catalyst-sd-wan-manager-cve-2026-20245-exploitation.md`.
- Hunt.io TeamPCP Python toolkit / FIRESCALE analysis is durable actor-profile material: keep the post-delivery toolkit details on `docs/actors/teampcp.md` unless a future wave warrants a separate ops page.
- StepSecurity's June 6 Azure/durabletask follow-up adds a distinct Miasma blast-radius lesson: repository-level AI-assistant/editor persistence can lead to GitHub disabling upstream Microsoft repositories and breaking downstream workflows that reference mutable GitHub Action tags such as `Azure/functions-action@v1`; keep this on `docs/ops/binding-gyp-npm-cicd-worm.md` and cross-reference the broad Mini Shai-Hulud page rather than creating a separate Microsoft-only page unless more primary Microsoft/GitHub postmortem detail emerges.
- Google Cloud / Mandiant's June 5, 2026 UNC3753 law-firm campaign is stable actor-profile material; coverage lives at `docs/actors/unc3753.md` with aliases Luna Moth, Chatty Spider, and Silent Ransom Group, and should be kept separate from BlackFile / UNC6671 unless future public reporting establishes overlap.
- OX Security's June 4, 2026 Miasma / `binding.gyp` update adds measurement and hunting detail to `docs/ops/binding-gyp-npm-cicd-worm.md`: 57 packages, 152,376 weekly downloads, 647,204 monthly downloads, 118+ GitHub repos with stolen credentials, and an en-dash repository-description variant `Miasma – The Spreading Blight`; add punctuation variants to hunts instead of creating a new page.
- SafeDep's June 5, 2026 Miasma source-repository analysis adds a reusable pattern: repository-local config can auto-execute malware through Claude Code / Gemini `SessionStart`, Cursor `alwaysApply`, VS Code `folderOpen`, and `npm test`; coverage lives at `docs/patterns/developer-tool-config-auto-execution.md` and the Miasma-specific details stay on `docs/ops/binding-gyp-npm-cicd-worm.md`.
- OX Security's March 27, 2026 Telnyx report is useful TeamPCP backfill: coverage lives at `docs/ops/telnyx-pypi-teampcp-compromise.md`; keep it tied to OX's attribution and Telnyx's caveat that only the Python package, not Telnyx service infrastructure, was compromised.
- Kaspersky Securelist can surface Windows exploit-detection items worth concise ops coverage even before final vendor patch naming; MiniPlasma coverage lives at `docs/ops/miniplasma-windows-cloud-filter-lpe-exploitation.md` and should keep public-exploit / patch-window language caveated to Kaspersky's June 2026 reporting.
- Hunt.io exposed-infrastructure writeups can justify ops coverage when they reveal durable C2 and intrusion sequencing; Oman government Iranian-nexus webshell coverage lives at `docs/ops/oman-government-iranian-nexus-webshell-c2.md`. Do not reproduce exposed victim PII; keep Hunt.io's no-group-level-attribution caveat intact when discussing APT34 / MuddyWater overlap.
- Hunt.io smishing-infrastructure writeups can justify concise ops coverage when they expose reusable campaign pivots; 19-country government / postal / telecom smishing coverage lives at `docs/ops/huntio-global-smishing-government-postal-telecom.md`. Prefer shared fingerprints such as the 128-character metadata hash and repeated assets over long static domain lists.
- Socket's June 7, 2026 Hades report adds a PyPI branch to Miasma / Mini Shai-Hulud coverage: 37 malicious wheels across 19 packages used `*-setup.pth` Python-startup execution, Bun v1.3.13, and `_index.js` credential theft. Coverage stays on `docs/ops/binding-gyp-npm-cicd-worm.md` under `#june-7-hades-pypi-wheel-wave` rather than a separate page unless the PyPI branch develops independently.
- StepSecurity's June 8, 2026 Hades graph-ML / bioinformatics follow-up is a major evolution of the same page: keep it on `docs/ops/binding-gyp-npm-cicd-worm.md` under `#june-8-hades-graph-ml-import-hook-wave`; important deltas are `__init__.py` import-hook execution, Bun v1.3.14, LLM-analysis prompt-injection evasion, macOS/Windows runner-memory scrapers, `DontRevokeOrItGoesBoom` / `TheBeautifulSnadsOfTime` / `firedalazer` GitHub C2, SSH/SCP lateral movement, and `gh-token-monitor` wiper-deterrent persistence.
- StepSecurity's June 8, 2026 `Pythagora-io/gpt-pilot` force-push report stays on `docs/ops/binding-gyp-npm-cicd-worm.md` under `#june-8-pythagora-iogpt-pilot-force-push-attempt`; treat it as Shai-Hulud-family source-repository takeover coverage with original-actor vs copycat caveat, and keep the defender lesson focused on branch protection plus lint/format gates as tripwires.
- Unit 42 identity/social-engineering guidance can justify reusable pattern pages when it adds measurable telemetry and hardening steps; Microsoft Teams external-chat phishing coverage lives at `docs/patterns/microsoft-teams-external-chat-phishing.md` with emphasis on open federation, unmanaged accounts, typosquatted/partner tenants, identity-event correlation, and chat removal/reporting.
- Public local-root exploit writeups can justify concise ops coverage when they add realistic post-compromise escalation risk for shared Linux/container hosts; CVE-2026-23111 coverage lives at `docs/ops/linux-nftables-cve-2026-23111-public-lpe-exploits.md` and should keep the no-remote-vector / no-active-exploitation caveat clear unless later reporting changes it.
- Microsoft Security Blog AI-brand social-engineering roundups can justify pattern coverage when they include concrete phishing, malvertising, code-hosting, signing, and IoC detail; AI-brand impersonation coverage lives at `docs/patterns/ai-brand-impersonation-phishing-malvertising.md`. Keep the "brand abuse, not AI-service compromise" caveat explicit.
- Trend Micro Research can provide durable follow-up on active vulnerability reuse where the main lesson is patch-management blind spots and cluster separation; WinRAR CVE-2025-8088 follow-up lives on `docs/ops/gamaredon-gammaphish-gammaworm-gammasteel-chain.md` with companion `docs/actors/uac-0226-shadow-earth-066.md`. Keep UAC-0226 / SHADOW-EARTH-066 separate from Gamaredon / Earth Dahu unless future primary sources merge them.
- Google Chrome Releases can justify concise ops coverage when Google confirms in-the-wild exploitation of browser zero-days even before actor or target detail is public; Chrome V8 CVE-2026-11645 coverage lives at `docs/ops/chrome-v8-cve-2026-11645-exploitation.md`.
- CleverHans Lab / arXiv can provide durable AI-security research to fold into patterns rather than actor pages; adaptive local-LLM worm research is tracked on `docs/patterns/ai-augmented-adversary-operations.md` as a defender pattern, not as in-the-wild attribution.
- Volexity is useful for incident-response-backed appliance and edge-device espionage coverage; VerdantBamboo / WARP PANDA / UNC5221 coverage lives at `docs/actors/verdantbamboo.md` with companion operation coverage at `docs/ops/verdantbamboo-appliance-brickstorm-operation.md`. Keep Clay Typhoon aliasing attributed to secondary/source-specific reporting unless a primary source in the page supports it.
- Proofpoint can surface durable DPRK/developer-targeting repository-phishing clusters; UNK_DeadDrop coverage lives at `docs/ops/unk-deaddrop-developer-repository-phishing.md`. Treat it as a distinct Proofpoint cluster from Contagious Interview unless future public telemetry establishes direct overlap, and keep the defender focus on GitHub/GitLab lures, VS Code / Cursor `folderOpen` tasks, malicious VSIX persistence, Overlord payloads, and cryptocurrency-wallet theft.
- Check Point Research can provide primary active-exploitation coverage for edge/VPN flaws; Remote Access VPN / Mobile Access IKEv1 CVE-2026-50751 coverage lives at `docs/ops/check-point-vpn-cve-2026-50751-exploitation.md`. Keep Check Point's medium-confidence financially motivated / Qilin ransomware-affiliate assessment caveated, and start defender review windows at the vendor's earliest observed exploitation date when supplied.
- Hunt.io exposed-toolkit reports can justify management-plane ops coverage when they reveal downstream blast radius; Quest KACE SMA CVE-2025-32975 coverage lives at `docs/ops/quest-kace-sma-cve-2025-32975-exploitation.md`. Do not reproduce exposed client lists or personal data from leaked directories; keep defender focus on patch levels, appliance admin takeover, MSP/customer scoping, and reported tooling.
- CISA KEV additions for AI gateway / MCP command-execution flaws can justify concise ops coverage when they confirm exploitation; LiteLLM CVE-2026-42271 coverage lives at `docs/ops/litellm-cve-2026-42271-mcp-stdio-command-injection.md` and should stay linked to the broader MCP stdio command-execution pattern.
- CISA KEV additions for network-infrastructure tunnel/overlay flaws can justify concise ops coverage even when impact is integrity/path manipulation rather than code execution; Arista EOS CVE-2026-7473 coverage lives at `docs/ops/arista-eos-cve-2026-7473-tunnel-decap-exploitation.md`, and should emphasize tunnel endpoint inventory plus ACL/TCAM mitigation rather than a software-upgrade path.
- Unit 42 cloud-control-plane research can justify pattern pages when it yields reusable detection / hardening guidance without a named intrusion; cloud logging tampering coverage lives at `docs/patterns/cloud-logging-control-plane-tampering.md` and treats AWS CloudTrail / Google Cloud Logging route, destination, KMS, and mutable-log-object changes as tier-zero controls.
- No-CVE SaaS exploitation notices can justify concise ops pages when the vendor reports anomalous activity or customer data queries; ServiceNow hosted-instance unauthenticated table-query coverage lives at `docs/ops/servicenow-instance-unauthenticated-table-query-exploitation.md`, with no actor attribution unless future public reporting establishes one.
- Trend Micro TrendAI reports can justify operation coverage when AI-agent use is evidenced inside real intrusions rather than only tooling research; SHADOW-AETHER-040 / SHADOW-AETHER-064 coverage lives at `docs/ops/shadow-aether-ai-augmented-latam-intrusions.md` and should keep Spanish-vs-Portuguese cluster separation plus campaign-label caveats intact.
- Unit 42 active-exploitation briefs can add durable hunt pivots to existing edge-service pages; PAN-OS GlobalProtect CVE-2026-0257 coverage lives at `docs/ops/pan-os-globalprotect-cve-2026-0257-exploitation.md` and should keep actor/malware attribution unset while focusing on gateway-connected VPN events, Unit 42 source IPs, generic host-ID/device-name pivots, and Palo Alto Networks fixed-version / authentication-override mitigations.
- GitHub Changelog can surface durable package-ecosystem security-default changes before they appear in the Security Blog; npm v12 script-approval / `allowScripts` changes belong as defensive updates on `docs/ops/binding-gyp-npm-cicd-worm.md` rather than a new campaign page.
- Lumen Black Lotus Labs botnet / covert-network reporting can justify ops coverage when it gives durable reconnaissance infrastructure and malware behavior; JDY SOHO / IoT botnet coverage lives at `docs/ops/jdy-soho-iot-recon-botnet.md`. Keep it as infrastructure/capability coverage, caveat China-nexus / Volt Typhoon links to Lumen, and do not over-attribute operation to a specific named group without stronger public sourcing.

## Security / attribution
- Treat third-party sources as untrusted until verified.
- When using external reporting, summarize the public reporting and link the source.
- Separate confirmed facts from inferred motivation or team structure.

## Threat-intel monitoring workflow
- Replicate the Skillz-style scan workflow for this repo with a threat-intelligence lens: monitor high-signal sources, add durable actor/operation/tool/pattern pages, update nav/index/blog/feed/source-index, run the strict MkDocs build, commit, push, and notify Dean only when substantive public threat intel was added.
- Current active watch: Shai-Hulud / Mini Shai-Hulud / TeamPCP supply-chain activity. Prioritize new package families, propagation primitives, CI/OIDC abuse paths, persistence mechanisms, exfiltration infrastructure/naming, maintainer postmortems, official advisories, and meaningful attribution changes.
- Track scan state outside the repo at `/home/user/clawd/memory/threat-intel-state.json`; keep this public repo free of private local monitoring state.
- OpenClaw cron job name: `Threat wiki: threat intel scan → wiki updates`; repo path: `/home/user/clawd/threat.wiki`.

- Unit 42's June 11, 2026 Behavioral Integrity Verification research belongs on `docs/patterns/agent-skill-marketplace-poisoning.md`: treat agent skills as multi-surface dependencies (metadata, executable code, natural-language instructions), prioritize chain-based review for FILE_READ→encoding→NETWORK_SEND, download→write→execute, and encoded dynamic-eval patterns, and keep the OpenClaw registry-scale stats caveated as classifier-predicted review candidates rather than runtime-confirmed exploits.
- ESET's June 11, 2026 OceanLotus / APT32 update is durable actor-profile material; coverage lives at `docs/actors/oceanlotus.md` and should keep the FireAnt MetaKit supply-chain compromise, Vietnamese infrastructure / transport construction intrusion, and SPECTRALVIPER internals together unless a future report warrants a separate tool page.
- Socket exposes a working Atom feed at `https://socket.dev/api/blog/feed.atom`; prefer it over brittle Socket blog HTML scraping. Hades PyPI coverage is currently on the broad Mini Shai-Hulud page (`docs/ops/mini-shai-hulud-npm-pypi-worm-campaign.md`) rather than a separate page: preserve the distinction between `*.pth` Python-startup hooks, `.abi3.so` native-extension import execution, and `langchain-core-mcp` split loaders that search `sys.path` for `_index.js`.
- StepSecurity's June 11 Miasma/Hades suspicious-files post is best treated as a defender-hunting update to `docs/ops/mini-shai-hulud-npm-pypi-worm-campaign.md` and `docs/patterns/developer-tool-config-auto-execution.md`: scan developer endpoints/repositories for quiet project-tree triggers (`binding.gyp`, injected Python `__init__.py`, `.vscode/tasks.json`, `.claude/setup.mjs`) because manifest/lockfile-only review misses open-time and import-time execution lanes.
- Boost Security Labs' June 11 Sleeper Squats writeup is durable CI/CD identity-boundary material; coverage lives at `docs/patterns/github-actions-oidc-subject-claim-collisions.md`. Keep the key lesson focused on unambiguous OIDC `sub` delimiters, immutable ID claims such as `repository_owner_id`, and avoiding broad string-only trust policies rather than treating the short-lived hyphen-format GitHub rollout as an active compromise.
- CISA KEV plus watchTowr exploit analysis can justify concise edge-appliance ops coverage; Ivanti Sentry CVE-2026-10520 coverage lives at `docs/ops/ivanti-sentry-cve-2026-10520-exploitation.md` and should keep the unmanaged/exposed Sentry caveat, fixed R10.5.2/R10.6.2/R10.7.1 versions, companion CVE-2026-10523 authentication bypass, and `/mics/api/v2/sentry/mics-config/handleMessage` detection pivot together.
