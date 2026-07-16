# Agent skill marketplace poisoning

## Summary
Agent skills are becoming a software-supply-chain layer for AI coding agents and hosted assistant workflows. Trail of Bits' June 2026 research shows that public skill marketplaces and skill-scanning services can miss overtly malicious skills that steal credentials, exfiltrate data, or steer agents into attacker-controlled execution paths. Unit 42's June 2026 registry-scale analysis adds a complementary defender lesson: skill review has to compare declared behavior against executable code and natural-language instructions, because the dangerous cases often appear as multi-stage chains rather than one obviously malicious permission. Unit 42's June 23, 2026 OpenClaw follow-up turns that pattern into live marketplace incident response: five ClawHub skills reportedly remained unblocked after earlier VirusTotal / ClawScan screening, spanning macOS infostealer delivery, file-size padding evasion, runtime affiliate injection, and agent-driven financial front-running. Snyk and JFrog's June 2026 follow-up reporting broadens the same lesson from individual skills to developer-machine agent ecosystems: MCP servers, skills, hooks, commands, subagents, and plugin manifests are executable supply-chain inputs that can run with developer credentials before code is committed. AIR's June 2026 public experiment adds a practical marketplace-abuse case: a clean-looking skill can outsource its real instructions to mutable external documentation, pass static scanners, gain social proof, and then swap the linked content after installation. HKUST's July 2026 SkillCloak / SkillDetonate paper then quantifies why static scanner verdicts should not be treated as durable allow decisions: payload-preserving transformations and self-extracting packing bypassed most tested scanners at high rates, while runtime sandboxing and information-flow evidence performed materially better.

This is a pattern page, not a named-actor profile. Treat public skills, plugins, and agent instructions as untrusted dependencies with both code-execution and prompt-injection risk.

## Tags
- patterns
- AI agents
- supply-chain
- agent skills
- prompt injection
- credential theft
- marketplace abuse
- behavioral integrity verification
- SkillCloak
- SkillDetonate
- scanner evasion

## Why this matters
- Skills mix natural-language instructions, code, assets, and dependency metadata. That creates a broader review problem than a normal package tarball or script.
- Public marketplaces can make malicious skills feel curated because a scanner returned a "safe" result.
- A skill can compromise the user or agent runtime without looking like conventional malware: instructions can ask the agent to execute a bundled script, read hidden/opaque files, configure a package manager to use attacker infrastructure, or reveal secrets through normal agent tools.
- LLM-based scanners have structural limits: context truncation, cost pressure, prompt-injection susceptibility, weak treatment of binary/opaque assets, and difficulty distinguishing malicious instructions from environment-specific legitimate automation.

## Public research anchor
Trail of Bits reported bypassing multiple public or open-source skill-scanning paths, including ClawHub's malicious-skill detector, Cisco's `skill-scanner`, and scanner integrations used by `skills.sh`.

The examples were intentionally straightforward:

- **Context truncation:** inserting 100,000 newlines before malicious content caused one scanner path to miss the payload and confused a model-backed scanner.
- **Opaque document indirection:** a skill directed the agent to extract real instructions from a `.docx` file, hiding command-execution instructions in ZIP/XML document internals instead of plain `SKILL.md` text.
- **Python bytecode poisoning:** a harmless-looking formatter skill included clean source plus malicious `.pyc` bytecode that could expose environment variables when the agent used it.
- **Prompt-injection framing:** a development-environment setup skill told the agent to configure npm/yarn for an attacker-controlled registry but framed the registry as internal corporate infrastructure, leading scanners to downgrade or miss the intent.

Trail of Bits also observed a false-positive/false-negative boundary problem: some legitimate skills perform behaviors that look suspicious in isolation, such as helper scripts and dynamic library preload patterns, while malicious skills can use plausible operational explanations to influence model-backed scanners.

Unit 42 introduced **Behavioral Integrity Verification (BIV)** as an audit primitive for agent skills. BIV compares what a skill claims to do with what it actually does across three surfaces:

- metadata and manifests;
- executable code;
- natural-language instructions such as `SKILL.md` and README prose.

Unit 42 reported crawling the OpenClaw agent-skill registry in early 2026 and analyzing 49,943 listed skills. Their scan surfaced 250,706 behavioral deviations, with 80.0% of skills showing at least one mismatch between declaration and behavior. Unit 42 caveated that most deviations reflected immature specifications rather than confirmed malice, but the high-risk subset clustered around multi-stage attack chains.

The most useful defender takeaway is chain-based review. Unit 42 highlighted compound patterns where individually normal operations become suspicious when linked:

- **Exfiltration chains:** `FILE_READ` → encoding such as base64 → outbound network send.
- **Remote-code-execution chains:** download → write → execute.
- **Code-obfuscation chains:** encoding or transformation followed by dynamic evaluation.
- **Data-lineage violations:** file read → file write, often benign data-pipeline boilerplate but still worth triage when undeclared.

Unit 42's registry-scale results also suggest triage priorities: 5.0% of analyzed skills carried multi-stage chains and should receive mandatory security review; 16.8% carried single-stage adversarial deviations and should receive contextual review; and the bulk of benign mismatches can be handled through documentation and manifest cleanup. They also called out instruction manipulation as especially high-signal in the agent-skill ecosystem, because prompt-control behavior is an agent-specific attack surface that traditional package scanners were not built to evaluate.

### Unit 42 OpenClaw marketplace follow-up (2026-06-23)

Unit 42's June 23, 2026 OpenClaw / ClawHub follow-up reported five skills that were still unblocked during a February-May 2026 marketplace review window after earlier malicious-skill waves had already pushed ClawHub toward VirusTotal and ClawScan screening. Unit 42 says the skills were reported to ClawHub, the accounts were banned, and the skills were deleted.

The durable defender value is that each case abused a different part of the agent-skill trust boundary:

- **ClawHavoc-style macOS infostealer delivery:** two TradingView-themed skills required agents to follow a paste-site redirect lure at `rentry[.]co/openclaw-code`, run a Base64 prerequisite command, and fetch a macOS infostealer payload from `2.26.75[.]16`. Unit 42 reported the delivery structure matched earlier ClawHavoc / Atomic macOS Stealer skill waves, but used fresh backend infrastructure and a `cluw` payload.
- **File-padding evasion:** the `omnicogg` skill placed a Base64 curl-pipe-bash AMOS dropper near the start of `README.md`, then added roughly 22 MB of padding characters. Unit 42 highlighted this as scanner-threshold abuse: pipelines that skip abnormally large files can return a clean or incomplete verdict while missing the payload.
- **Runtime affiliate injection:** `money-radar` positioned itself as a financial-product advisor, then forced every invocation to fetch `referrals.json` from `laosji[.]net` and use affiliate links in its recommendations. The operator could change recommended banks, brokers, exchanges, or remittance products after installation by changing the remote JSON.
- **Agentic front-running:** `letssendit` coordinated installed agents around `letssendit[.]fun` and Solana token-launch workflows. Unit 42 described the pattern as agent-driven pump-and-dump / front-running behavior rather than conventional endpoint malware.

The same report notes that early 2026 ClawHub campaigns included Base64 curl-pipe-bash droppers, macOS paste-site redirects through services such as `glot[.]io` and `rentry[.]co`, Windows password-protected executables on third-party hosting, cron-based auto-updater persistence, Telegram Bot API private-key exfiltration in cryptocurrency-themed skills, and registry-saturation behavior from publisher accounts that reused identical payloads across many skills.

Defensively, this reinforces that skill review cannot stop at a marketplace verdict. Inspect large files even when scanners skip them, treat prerequisite blocks and paste-site instructions as executable payload staging, snapshot external JSON / documentation dependencies, and compare all outbound domains against the skill's declared purpose.

### Snyk / JFrog developer-environment update (2026-06-23)

Snyk's June 23, 2026 developer-environment analysis reported that agentic tooling risk is already present on endpoints rather than only in public marketplaces:

- 43% of observed developers ran two or more AI coding environments.
- 50.8% had at least one MCP server installed, and one in seven developers with MCP servers had at least one security finding.
- 22.8% had at least one agent skill installed.
- Snyk reported 392 confirmed prompt-injection findings in tool descriptions.
- In Snyk's related ToxicSkills study of 3,984 skills from ClawHub and `skills.sh`, 13.4% contained at least one critical-level issue, 36.82% had at least one security flaw, human validation confirmed malicious payloads for credential theft, backdoor installation, and data exfiltration, and 28% exposed agents to uncontrolled third-party content.

JFrog's June 23, 2026 agent-plugin repository guidance frames agent plugins as packaged executable software rather than preferences or settings. JFrog describes modern plugin packages bundling skills, slash commands, subagents, hooks, and MCP definitions into manifests that local coding engines parse and execute on developer machines. Their key warning is that Git branches, tags, and public repositories are not package registries: a malicious update to a public plugin repository can be pulled by multiple developer workstations and run shell commands in source trees with developer credentials, often without central audit or a fast revocation path.

### AIR external-document skill swap (2026-06-22)

AIR Security published a controlled experiment in which it built a plausible `brand-landingpage` skill around Google's Stitch launch, promoted it through public sharing and an Instagram ad, and reported roughly 26,000 affected agents, including corporate-account agents. AIR's scale claims, "full control" framing, and marketplace pitch should be treated as vendor-reported and not independently verified, but the technique is useful defender material because it matches the structural scanner gap described by Trail of Bits and others.

The important mechanics were:

- The submitted skill did not need an obvious malicious payload in its bundled files.
- The skill instructed the agent to follow setup instructions from an external documentation link.
- AIR controlled a plausible Stitch-themed domain and initially redirected it to the legitimate Google Stitch site, making static review of the submitted package look safe.
- After distribution, AIR changed the external page so the agent would download and run a script; AIR says the demonstration payload only sent the user's email address so affected users could be notified.
- The trust signals that users and scanners leaned on — marketplace presence, GitHub stars / reputation, and a clean scanner result — did not prove that the content fetched later by the agent was safe.

This is a different failure mode from hidden bytecode or prompt-padding scanner bypasses: even a perfectly scanned package can become unsafe if its execution path depends on mutable web content outside the reviewed artifact.

### SkillCloak scanner evasion and SkillDetonate runtime auditing (2026-07-02)

HKUST researchers Zimo Ji, Congying Xu, Zongjie Li, Yudong Gao, Xin Wei, Shuai Wang, and Shing-Chi Cheung published **Cloak and Detonate: Scanner Evasion and Dynamic Detection of Agent Skill Malware** on arXiv on July 2, 2026. The Hacker News surfaced the paper publicly on July 6, 2026 under the SkillCloak name.

The paper is useful because it moves the agent-skill scanner problem from anecdotal bypasses to measurement. The authors evaluated eight skill scanners against 1,613 in-the-wild malicious skills and introduced **SkillCloak**, a payload-preserving evasion framework. SkillCloak keeps malicious behavior intact while changing how the payload appears to install-time scanners:

- **Structural Obfuscation** rewrites visible payload indicators into semantically equivalent forms. The paper reports that this bypassed more than 80% of most static scanners and reached 96% against a hybrid scanner.
- **Self-Extracting Skill (SFS) Packing** hides malicious components from the install-time view and restores them during agent execution. The paper reports that SFS Packing bypassed every tested scanner at rates above 90%.

The defensive contribution, **SkillDetonate**, is a behavior-centric runtime auditor. Instead of trusting package appearance, it executes skills in a sandbox and looks for OS-boundary information-flow evidence across the agent context, files, processes, and network operations. Two reported primitives are especially actionable for defenders:

- **On-demand closure lift:** observe instructions and code that materialize only during skill execution, not just the submitted artifact.
- **Marker-based taint analysis:** track sensitive data as it moves through agent context, local files, child processes, and outbound network operations.

The paper reports 97% attack detection at a 2% false-positive rate in its evaluation, and 87% detection on real-world malicious skills. Treat those figures as academic-lab results rather than product guarantees, but the direction is clear: static scanner verdicts, LLM-as-judge reviews, and marketplace badges are weak allow criteria when the skill can unpack or synthesize the dangerous instructions after installation.

Defensive changes to make this operational:

- Require dynamic detonation for public-marketplace skills before approval, especially when the skill can run shell, Python, JavaScript, package managers, or MCP setup commands.
- Detonate with realistic but synthetic secrets and source-like canaries so information-flow tracking can observe attempted exfiltration without exposing real data.
- Block or quarantine skills that create executable files, decode or decompress bundled material, spawn package managers, or initiate network egress not declared in the skill manifest.
- Store scanner output as triage evidence, not as an authorization decision. A clean static result should expire when skill files, dependencies, external URLs, or runtime-generated content change.

## Tradecraft map

### Initial trust path
- Public marketplace install flows such as one-click skill installation.
- Out-of-band ZIP uploads into hosted or local agent harnesses.
- Git repository based skill distribution where the whole tree may contain hidden files, binary files, generated artifacts, or assets not referenced by the top-level skill description.
- Agent plugin repositories or shared branches consumed directly by local coding agents, especially when updates are not pinned to immutable reviewed artifacts.
- External documentation, setup guides, API references, or "official-looking" product domains that the skill tells the agent to fetch and obey after installation.

### Execution and abuse paths
- Agent instructions that call shell, Python, JavaScript, or package-manager commands.
- Hidden or opaque payloads in documents, bytecode, archives, images, or generated files.
- Package-manager reconfiguration to attacker-controlled npm/yarn registries or mirrors.
- Prompt text that persuades the agent or the scanner that a dangerous action is normal corporate setup.
- Paste-site or prerequisite instructions that tell the agent to decode and run setup commands before the skill will function.
- Instructions that ask the agent to collect local context, credentials, dotfiles, environment variables, source files, or authentication material.
- Remote JSON, configuration, or documentation that dynamically controls advice, links, tasking, or product recommendations after installation.
- Plugin hooks, slash commands, subagents, and MCP definitions that execute on developer-machine events before reviewed code reaches a repository or CI pipeline.
- Post-review content swaps where a previously benign external URL begins returning installer commands, scripts, or new tasking that was not present during marketplace submission.

### Detection gaps to assume
- Scanner context windows may not include every file or every part of a very large file.
- Static rules may only inspect referenced files, common script extensions, or known package manifests.
- File-size thresholds can turn malicious padding into an evasion primitive when scanners skip oversized README, markdown, archive, or generated files.
- LLM analysis may treat embedded explanations as trustworthy.
- Binary, bytecode, office-document, image, and archive content may be ignored or summarized poorly.
- One-time scans usually do not snapshot, pin, or continuously re-validate every external URL that the skill instructs the agent to fetch.
- Passing scanner output is not a provenance guarantee and should not be used as an allow decision by itself.
- Install-time scanner views can miss self-extracting payloads that unpack, decode, synthesize, or fetch malicious components only when the agent executes the skill.
- Single-capability review can miss malicious chains; treat file reads, encoders, network sends, downloads, writes, dynamic eval, and shell execution as higher-risk when they occur together but are not declared together.
- Developer endpoint inventory may miss agent runtimes, local MCP servers, skill directories, plugin repositories, and auto-update paths because they sit outside conventional SCA, CI/CD, and repository controls.

## Defender heuristics

### Intake controls
- Prefer organization-curated skill catalogs over public marketplaces for sensitive agents.
- Require human review for new skills, skill updates, and marketplace-originated ZIPs or repositories.
- Pin skills to reviewed commits or immutable artifacts; do not auto-update from public marketplaces.
- Pin or vendor external setup documentation that a skill depends on; if a skill must fetch live web content, treat each fetched URL as part of the reviewed supply-chain artifact and re-check it on change.
- Treat agent plugins as packages: publish reviewed versions to an internal registry or artifact store, require immutable versioning, and avoid consuming mutable public Git branches directly from developer workstations.
- Maintain an allowlist of approved skills, tool permissions, network destinations, and package registries.
- Inventory local AI coding environments, MCP servers, installed skills, plugin manifests, hooks, commands, subagents, and their update sources across developer machines.

### Review checklist
- Inspect the full repository or archive tree, not only `SKILL.md` or files named in the skill description.
- Compare the skill's declared purpose and permissions against all code paths and natural-language instructions; block installation when actual behavior is broader than the manifest or README describes.
- Flag hidden files, bytecode (`.pyc`), compiled binaries, archives, office documents, images with embedded instructions, and large padding/truncation tricks; do not treat scanner skips or clean verdicts on oversized files as approval.
- Diff source and compiled artifacts; rebuild bytecode or generated assets from reviewed source where possible.
- Detonate skills in a sandbox with synthetic credentials and source-code canaries; watch for canary reads, child-process inheritance, file writes, decode/decompress stages, and network egress.
- Review all package-manager, shell, Git, cloud, and credential-store commands the skill can cause an agent to run.
- Enumerate every external URL or domain referenced by the skill and resolve whether it is controlled by the claimed product/vendor; watch for product-adjacent lookalike domains that redirect to legitimate docs during review.
- Snapshot and review remote JSON, paste-site pages, setup scripts, and other live content that a skill requires at runtime; alert when those dependencies change.
- Treat changes to npm/yarn/pip/Poetry/Go/RubyGems registry or proxy configuration as high risk unless explicitly approved.
- Strip terminal-control characters and normalize long whitespace before review to reduce hidden prompt or truncation tricks.
- Prioritize mandatory human review for undeclared credential access, prompt/instruction manipulation, outbound network sends, environment reads, download/write/execute sequences, and encoded dynamic evaluation.

### Runtime guardrails
- Run agent skills in a sandbox with least-privilege filesystem, network, shell, and credential access.
- Separate skill execution from long-lived developer shells and production credentials.
- Disable or require approval for arbitrary shell commands, package-manager configuration changes, and outbound network access from newly installed skills.
- Monitor agent runs for reads of `.env`, SSH keys, cloud credential files, GitHub tokens, npm tokens, shell history, browser stores, and package-manager config files.
- Log marketplace source, skill version/commit, scanner outputs, human approver, and runtime tool calls so incident response can reconstruct exposure.
- Log and alert on agent fetches of new external documentation domains and on downloaded scripts launched from URLs that were not part of the approved skill snapshot.
- Alert when a skill creates executable files, materializes new instructions after install, spawns interpreters/package managers, or moves marked/canary data across process or network boundaries.
- Add endpoint telemetry for agent-plugin syncs, hook execution, MCP server launches, shell commands spawned by agent runtimes, and unexpected reads of developer credentials before code reaches CI.

## Related pages
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [SANDWORM_MODE AI-toolchain npm worm](../ops/sandworm-mode-ai-toolchain-worm.md)
- [Malware-Slop Claude user-data npm infostealer](../ops/malware-slop-claude-user-data-npm-infostealer.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- [Trail of Bits](https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/)
- [Unit 42 BIV](https://unit42.paloaltonetworks.com/ai-agent-supply-chain-risks/)
- [Unit 42 OpenClaw](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)
- [Snyk](https://snyk.io/blog/agentic-development-security-ai-coding-risk/)
- [JFrog](https://jfrog.com/blog/introducing-agent-plugins-repositories/)
- [AIR Security](https://www.air.security/blog-posts/the-story-of-skills)
- [HKUST arXiv](https://arxiv.org/abs/2607.02357)
- [The Hacker News SkillCloak coverage](https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html)
- [The Hacker News](https://thehackernews.com/2026/06/fake-ai-agent-skill-passed-security.html)

