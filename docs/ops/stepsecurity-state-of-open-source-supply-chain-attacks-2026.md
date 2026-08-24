# StepSecurity annual census: 56 open source supply chain attacks (Aug 2025–Aug 2026)

## Summary
StepSecurity's threat-intelligence team published an annual census of open source supply chain attacks on August 22–23, 2026 (blog date August 22; RSS publication `Sun, 23 Aug 2026 22:40:19 GMT`): **56 distinct malicious supply chain compromises tracked and alerted between August 2025 and August 2026**, roughly one every three days since March 2026, up from roughly one per month a year earlier. The report counts only **deliberately planted compromises** of trusted components (npm, PyPI, RubyGems, Composer, crates.io, GitHub Actions, IDE extensions) — not vulnerabilities and not new-brand typosquats — and every counted incident shipped as a StepSecurity Threat Center alert with an "am I affected" check. The durable value of the census is the **aggregate trend and the taxonomy**: self-propagating worms became the dominant driver of acceleration, GitHub Actions credential theft appears in three distinct forms, and no major package ecosystem or CI/CD platform was spared. Most individual incidents in the census are already documented on dedicated pages; this page records the cross-incident measurements and the three GitHub Actions attack forms as a standing reference.

## Tags
- ops
- supply chain
- npm
- PyPI
- RubyGems
- Composer
- crates.io
- GitHub Actions
- CI/CD credential theft
- Shai-Hulud
- Mini Shai-Hulud
- Team PCP
- Miasma
- ChainDrop
- CanisterWorm
- census
- StepSecurity
- attack-rate
- worm

## Scope and counting rules (what the 56 means)
- **Malicious, not vulnerable:** every counted incident is a compromise with deliberately planted code — not a CVE, not a flaw exploited later in production, and not a suspicious-but-benign event (e.g., unexplained tag movement that resolved as benign is excluded).
- **Trusted components only:** brand-new packages that are malicious from their first version (typosquats, name-confusion, lookalikes) are excluded. The 56 are compromises of components organizations already trusted — the next version of a trusted package, or a repointed tag/mutable reference.
- **Every incident alerted:** each of the 56 produced a Threat Center alert with indicators and an automated exposure check; some are Threat Center alerts without a standalone blog post.
- **Channel scope:** npm, PyPI, RubyGems, Composer, crates.io, GitHub Actions, and IDE-extension channels are all included.

## Attack rate: the 8x acceleration
- **Aug 2025–Jan 2026:** 6 incidents total (roughly one per month).
- **Mar 2026:** 13 incidents in a single month.
- **Apr 2026:** 9; **May 2026:** 9; **Jun 2026:** 10; **Jul 2026:** 6.
- Net: **50 incidents in the six-and-a-half months since February 2026 vs 6 in the first six months of the window — more than an 8x increase.** The report attributes the jump primarily to self-propagation: a single compromised maintainer no longer means one poisoned package, it means every package that maintainer can publish, then every package those downstream victims can publish.

## The worm era (primary acceleration driver)
The census frames self-propagation as "what changed":
- **Shai-Hulud (Sep 2025):** the first ecosystem-scale self-propagating npm worm, compromising 500+ packages by using each victim's stolen npm token to infect the packages the victim maintained.
- **"Sha1-Hulud, the second coming" (Nov 2025):** hit Zapier, ENS Domains, and other prominent npm packages; later detected inside CNCF's Backstage repository. (StepSecurity's own detection claims appear in the "defense" section: its Harden-Runner community tier detected the Sha1-Hulud worm inside CNCF Backstage and captured the axios RAT's live C2 callback there.)
- **CanisterWorm (Mar 2026):** backdoors spread across npm.
- **Mini Shai-Hulud variants (Apr–May 2026):** SAP-related packages in April, then TanStack packages and the AntV ecosystem in May.
- **Miasma (Jun 2026):** forced Microsoft to disable the Azure Functions Action and 72 other repositories; resurfaced in July inside the AsyncAPI ecosystem.
- **ChainDrop (Aug 2026):** Bun-loaded npm worm that harvests CI/CD credentials and uses an Ethereum smart contract as a dead-drop for its C2 address.

Keep these as StepSecurity's framing of incidents the wiki already covers individually: [Shai-Hulud / Mini Shai-Hulud campaign](mini-shai-hulud-npm-pypi-worm-campaign.md), [CanisterWorm](../tools/canisterworm.md), [Miasma / durabletask GitHub enforcement](binding-gyp-npm-cicd-worm.md), [ChainDrop keyv / cacheable worm](chaindrop-keyv-cacheable-npm-worm.md) and its watch topic in [source index](../notes/source-index.md).

## The Team PCP five-day campaign (scale of one actor)
The census re-states the March 19–24, 2026 Team PCP campaign (Trivy GitHub Action with 76 of 77 version tags, Checkmarx KICS Action, `telnyx` PyPI with the stealer hidden in a WAV file, and `LiteLLM`) and folds in the August 2026 CloudSEK victim dataset analyzed by StepSecurity on August 13: **78,330 distinct secrets exfiltrated from the CI/CD pipelines of 2,186 organizations**, spanning every major CI/CD platform, including 92 publicly traded victim companies StepSecurity estimates at a combined $6.2 trillion market capitalization. Stolen material was cloud keys, signing keys, and source-code-control tokens. This is covered in depth on the [Team PCP actor page](../actors/teampcp.md) and the [Trivy / LiteLLM compromise timeline](trivy-lite-llm-compromise-timeline.md).

## GitHub Actions: three distinct attack forms
The report isolates GitHub Actions as a primary target and names three durable forms:
1. **Mutable Action version tags:** a compromised maintainer repoints every existing tag to malicious code; every workflow using the Action picks it up on the next run with no repository change. Reported instances: Trivy (76 of 77 tags), Checkmarx KICS, `actions-cool/issues-helper`, `codfish/semantic-release-action`, `simonecorsi/mawesome`, and `xygeni-action`. All except `xygeni-action` have dedicated wiki pages (see [actions-cool](actions-cool-github-actions-tag-compromise.md), [codfish semantic-release-action](codfish-semantic-release-action-tag-compromise.md), [simonecorsi/mawesome](simonecorsi-mawesome-github-action-compromise.md), [Trivy](trivy-compromise.md)).
2. **Runner memory scraping from compromised packages:** payloads that dump credentials from the GitHub Actions runner's worker-process memory at install time (Shai-Hulud family, Team PCP stealers, ChainDrop all worked this way).
3. **Stolen developer credentials → workflow-planting harvest:** with a developer's GitHub credentials, attackers push a new workflow file on a new branch across every repository the developer can access; each planted workflow runs immediately and exfiltrates the repository's pipeline secrets. StepSecurity credits Miasma with this pattern ("planting workflows with stolen credentials until Microsoft had to disable 73 repositories") and notes the "Hades campaign" used the same pattern.

Form 3 generalizes the [Megalodon workflow-backdooring](megalodon-github-actions-workflow-backdooring.md) pattern; defender controls named in the report (egress policy at the runner, secret-exfiltration workflow-run policy, registry proxying) are product claims and should be treated as vendor guidance, not verified telemetry.

## Blast radius per incident
- **axios:** over 100 million weekly downloads; `axios@1.14.1` and `axios@0.30.4` pulled a fake dependency that dropped a cross-platform remote access trojan on install, called home, then erased its own traces. The census adds that StepSecurity's AI Package Analyst flagged the release and its Harden-Runner captured the live C2 callback during a GitHub Actions run in CNCF's Backstage repository — evidence "the malware tried to delete." Tracked on the [Operation DangerousPassword / axios compromise](operation-dangerouspassword-axios-npm-compromise.md) page.
- **intercom-client:** 361,000 weekly downloads hijacked in April 2026 (cross-registry `intercom-client` / PyPI `lightning` chain on the [Mini Shai-Hulud campaign page](mini-shai-hulud-npm-pypi-worm-campaign.md)).
- Pattern: attackers target components with the largest downstream reach; "at least one of these channels is in your build."

## No ecosystem is exempt
Beyond npm (still the biggest target), the census highlights: Microsoft's `durabletask` PyPI compromise, SleeperGem backdooring `git_credential_manager` and `fastlane` RubyGems, the Laravel-Lang Composer tag rewrite, and the Rust `arrayref` / `internment` / `append-only-vec` build-time droppers (August 2026). Each has a dedicated page: [durabletask / Miasma binding-gyp](binding-gyp-npm-cicd-worm.md), [SleeperGem](sleepergem-rubygems-maintainer-account-compromise.md), [Laravel-Lang](laravel-lang-composer-tag-rewrite-compromise.md), [arrayref / proc-macro1](arrayref-proc-macro1-rust-crate-supply-chain-attack.md).

## AI on both sides
- **Offense:** `hackerbot-claw`, an AI-powered bot, actively exploited GitHub Actions workflow vulnerabilities at Microsoft, Datadog, and CNCF projects ([HackerBot Claw campaign](hackerbot-claw-github-actions-exploitation-campaign.md), [HackerBot Claw actor profile](../actors/hackerbot-claw.md)). The Miasma worm specifically targeted AI coding agents.
- **Defense:** StepSecurity reports an AI Package Analyst flagged the axios release and an agentic triage loop; both are vendor claims with no independent telemetry in the public post.

## Assessment limits
- This is a **vendor census from a single vendor's alert pipeline.** The 56-incident count, monthly rates, and 8x framing are StepSecurity's measurements and definitions, not an industry-wide census; another vendor's counting rules would produce different numbers.
- **Individual incidents are documented elsewhere with their own primary sources.** Treat this page as the aggregate/taxonomy layer; prefer the per-incident pages (linked above) for indicators, timelines, and root cause.
- The "three recurring weaknesses" section in the post is rendered client-side and its card contents were not retrievable at capture time; do not cite specific weakness names from this post without re-fetching the page.
- Defensive-control claims (Harden-Runner detections, Secure Registry proxying, Threat Center "am I affected") are vendor product assertions, not verified independent telemetry.

## Related pages
- [Team PCP actor profile](../actors/teampcp.md)
- [Shai-Hulud / Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Miasma / durabletask GitHub enforcement](binding-gyp-npm-cicd-worm.md)
- [arrayref / proc-macro1 Rust crate supply-chain attack](arrayref-proc-macro1-rust-crate-supply-chain-attack.md)
- [Trivy compromise](trivy-compromise.md)
- [HackerBot Claw GitHub Actions exploitation campaign](hackerbot-claw-github-actions-exploitation-campaign.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [Operation DangerousPassword / axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)

## Sources
- StepSecurity: [The State of Open Source Supply Chain Attacks](https://www.stepsecurity.io/blog/state-of-open-source-supply-chain-attacks) (Varun Sharma, blog-dated August 22, 2026; RSS published `Sun, 23 Aug 2026 22:40:19 GMT`)
- StepSecurity RSS: <https://www.stepsecurity.io/blog/rss.xml>
