# Agent skill marketplace poisoning

## Summary
Agent skills are becoming a software-supply-chain layer for AI coding agents and hosted assistant workflows. Trail of Bits' June 2026 research shows that public skill marketplaces and skill-scanning services can miss overtly malicious skills that steal credentials, exfiltrate data, or steer agents into attacker-controlled execution paths. Unit 42's June 2026 registry-scale analysis adds a complementary defender lesson: skill review has to compare declared behavior against executable code and natural-language instructions, because the dangerous cases often appear as multi-stage chains rather than one obviously malicious permission.

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

## Tradecraft map

### Initial trust path
- Public marketplace install flows such as one-click skill installation.
- Out-of-band ZIP uploads into hosted or local agent harnesses.
- Git repository based skill distribution where the whole tree may contain hidden files, binary files, generated artifacts, or assets not referenced by the top-level skill description.

### Execution and abuse paths
- Agent instructions that call shell, Python, JavaScript, or package-manager commands.
- Hidden or opaque payloads in documents, bytecode, archives, images, or generated files.
- Package-manager reconfiguration to attacker-controlled npm/yarn registries or mirrors.
- Prompt text that persuades the agent or the scanner that a dangerous action is normal corporate setup.
- Instructions that ask the agent to collect local context, credentials, dotfiles, environment variables, source files, or authentication material.

### Detection gaps to assume
- Scanner context windows may not include every file or every part of a very large file.
- Static rules may only inspect referenced files, common script extensions, or known package manifests.
- LLM analysis may treat embedded explanations as trustworthy.
- Binary, bytecode, office-document, image, and archive content may be ignored or summarized poorly.
- Passing scanner output is not a provenance guarantee and should not be used as an allow decision by itself.
- Single-capability review can miss malicious chains; treat file reads, encoders, network sends, downloads, writes, dynamic eval, and shell execution as higher-risk when they occur together but are not declared together.

## Defender heuristics

### Intake controls
- Prefer organization-curated skill catalogs over public marketplaces for sensitive agents.
- Require human review for new skills, skill updates, and marketplace-originated ZIPs or repositories.
- Pin skills to reviewed commits or immutable artifacts; do not auto-update from public marketplaces.
- Maintain an allowlist of approved skills, tool permissions, network destinations, and package registries.

### Review checklist
- Inspect the full repository or archive tree, not only `SKILL.md` or files named in the skill description.
- Compare the skill's declared purpose and permissions against all code paths and natural-language instructions; block installation when actual behavior is broader than the manifest or README describes.
- Flag hidden files, bytecode (`.pyc`), compiled binaries, archives, office documents, images with embedded instructions, and large padding/truncation tricks.
- Diff source and compiled artifacts; rebuild bytecode or generated assets from reviewed source where possible.
- Review all package-manager, shell, Git, cloud, and credential-store commands the skill can cause an agent to run.
- Treat changes to npm/yarn/pip/Poetry/Go/RubyGems registry or proxy configuration as high risk unless explicitly approved.
- Strip terminal-control characters and normalize long whitespace before review to reduce hidden prompt or truncation tricks.
- Prioritize mandatory human review for undeclared credential access, prompt/instruction manipulation, outbound network sends, environment reads, download/write/execute sequences, and encoded dynamic evaluation.

### Runtime guardrails
- Run agent skills in a sandbox with least-privilege filesystem, network, shell, and credential access.
- Separate skill execution from long-lived developer shells and production credentials.
- Disable or require approval for arbitrary shell commands, package-manager configuration changes, and outbound network access from newly installed skills.
- Monitor agent runs for reads of `.env`, SSH keys, cloud credential files, GitHub tokens, npm tokens, shell history, browser stores, and package-manager config files.
- Log marketplace source, skill version/commit, scanner outputs, human approver, and runtime tool calls so incident response can reconstruct exposure.

## Related pages
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [SANDWORM_MODE AI-toolchain npm worm](../ops/sandworm-mode-ai-toolchain-worm.md)
- [Malware-Slop Claude user-data npm infostealer](../ops/malware-slop-claude-user-data-npm-infostealer.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- Trail of Bits: https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/
- Unit 42: https://unit42.paloaltonetworks.com/ai-agent-supply-chain-risks/

