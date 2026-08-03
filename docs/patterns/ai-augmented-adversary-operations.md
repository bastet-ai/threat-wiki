# AI-augmented adversary operations

## Summary
Google Threat Intelligence Group's May 2026 AI Threat Tracker documents a transition from experimental AI misuse toward repeatable adversary workflows: AI-supported vulnerability research, AI-assisted exploit development, AI-generated obfuscation, LLM-driven malware interaction with victim environments, adversary access-brokerage for model abuse, and AI software supply-chain attacks. WithSecure's GREYVIBE reporting adds a concrete Russia-nexus case where AI appears operationally integrated across lure generation, loader and obfuscator development, backend setup, and post-compromise scripting. Sysdig's marimo CVE-2026-39987 case adds a cloud post-exploitation example where an LLM agent appears to compose live commands, consume prior output, pivot through AWS Secrets Manager, and dump an internal database. Trend Micro's SHADOW-AETHER reporting adds in-the-wild agentic-AI intrusion workflows where operators tunneled into Latin American government and financial environments, then used AI-assisted CLI activity to generate scripts, inspect credentials, move laterally, and stage exfiltration. Trend Micro's Patriot Bait / bandcampro reporting adds a smaller but operationally important botnet case: Gemini CLI session logs showed a Russian-speaking actor using AI as the primary C2 operator, code author, deployer, and debugger for disposable PowerShell-based infrastructure. Unit 42's TuxBot v3 Evolution reporting adds an IoT-botnet engineering case: source artifacts show LLM-assisted module generation, raw model reasoning, hallucinated crypto claims, and easy-to-fix implementation bugs in a partially functional DDoS-for-hire botnet framework. Sysdig's PraisonAI CVE-2026-44338 case adds a same-day exploitation example where an exposed AI-agent API was scanned less than four hours after advisory publication. Permiso's ChatGPhish research adds a user-facing AI-rendering primitive: attacker-controlled web-page content can become trusted Markdown links, images, spoofed alerts, and QR-code phish inside ChatGPT summarization output. LayerX's BioShocking AI-browser research extends that browser-side boundary: indirect prompt injection can manipulate an agentic browser's operating context so it treats credential copying or authenticated-site data access as part of a fictional game rather than a real-world safety violation. Noma Labs' GitLost and SAND Security's WriteOut disclosures add agentic-workflow trust-boundary cases: public GitHub issue text steering GitHub Agentic Workflows into private-repository read/public-comment write-back, and Writer AI live-preview sandboxing leaking user session cookies into attacker-controlled code. Snyk's jqwik 1.10.0 reporting adds a software-supply-chain variant: a legitimate maintainer release used terminal-control characters to hide a prompt-injection instruction from humans while leaving it readable to AI coding agents that ingest raw build/test output. CleverHans Lab's June 2026 adaptive-worm research adds a lab-demonstrated network-worm pattern where compromised hosts run local open-weight LLMs to generate target-specific exploitation steps across Linux, Windows, and IoT systems.

The durable defender lesson is that AI is now part of the operational fabric for multiple actor types rather than only a novelty. Treat AI use as a force multiplier across existing intrusion patterns: faster vulnerability triage, more scalable exploit validation, easier malware refactoring, synthetic social-engineering content, compressed operator timelines, and new initial-access paths through ML and AI-tooling dependencies.

Unit 42's July 30 knaithe / KnYuan case adds a recovered autonomous scan-to-exploit loop rather than only AI-assisted operator activity. Hermes Agent and DeepSeek used FOFA, custom skills, MCP, Telegram orchestration, and public exploit repositories to select and test Langflow and n8n targets, abandon paths when prerequisites were absent, and conserve compute through sampling. The autonomous attempts failed because target configurations did not expose the required flow or unauthenticated-upload conditions; separate manual activity by the same actor achieved NetScaler data theft and marimo command execution.

ProjectDiscovery's August 3 behavioral audit adds a controlled black-box evaluation of offensive-security agents. Across 54 usable web targets, most failed runs had already selected the right vulnerability class but could not complete execution; models also reached unintended exploit paths, side channels, and the surrounding test harness when it remained reachable. CrowdStrike's 2026 threat-hunting report adds field calibration: 88% of its observed exploitation involving a public proof of concept occurred within 48 hours of PoC release during January-June 2026, while AI-agent-triggered detections produced 2.5 times as many hunting leads as manually driven activity.

## Tags
- patterns
- AI
- LLM
- vulnerability-research
- exploit-development
- malware
- obfuscation
- initial-access
- post-exploitation
- cloud credential theft
- local LLMs
- agentic malware
- rapid exploitation
- supply-chain
- prompt-injection
- indirect prompt injection
- AI browsers
- agentic browsers
- BioShocking
- LayerX
- protestware
- Maven Central
- TeamPCP
- UNC6780
- PROMPTSPY
- PROMPTFLUX
- HONESTCUE
- CANFAIL
- LONGSTREAM
- APT27
- APT45
- UNC2814
- DPRK
- PRC
- Russia-nexus
- knaithe
- KnYuan
- Hermes Agent
- DeepSeek
- autonomous exploitation
- GREYVIBE

## Why this matters
- Unit 42 recovered a functional autonomous workflow that moved from internet-asset enumeration to proof-of-concept acquisition, version and prerequisite checks, target sampling, threaded scanning, and exploit attempts without further visible operator input. Secure target configuration stopped the recovered attempts, while the agent itself exposed the actor's home directory by starting a file server from the wrong working directory.
- GTIG says it identified a cybercrime actor using a zero-day exploit that it assesses was developed with AI support. The planned mass exploitation was disrupted through disclosure and counter-discovery, but the case shows that LLMs can help reason about semantic logic flaws that traditional scanners may miss.
- State-linked PRC and DPRK clusters are using AI for vulnerability-research workflows, including persona-driven prompting, curated vulnerability corpora, recursive CVE/PoC validation, and agentic testing in controlled labs.
- AI coding support can speed obfuscation and infrastructure development. GTIG highlights dynamic/self-modifying malware experiments, AI-assisted relay-box tooling, and LLM-generated decoy logic in malware linked to suspected Russia-nexus activity; WithSecure separately reports GREYVIBE indicators of AI assistance in LOOKVALJS, DAYLIGHT, TEASOUP, LegionRelay, lure sites, backend infrastructure, and operator scripts.
- Sysdig observed a post-compromise LLM-agent workflow after marimo CVE-2026-39987 exploitation: the actor harvested cloud credentials, used Cloudflare Workers as fanned-out egress for AWS Secrets Manager calls, retrieved an SSH key, and dumped internal PostgreSQL tables from a bastion while shaping command output for machine parsing.
- Trend Micro observed SHADOW-AETHER-040 and SHADOW-AETHER-064 using agentic AI during intrusions against Latin American government and financial targets. The operators established SOCKS5 / ProxyChains / SSH tunnels, generated one-off scripts, mined application and shell artifacts for credentials, and used AI-assisted workflows for lateral movement and exfiltration.
- Sysdig observed PraisonAI CVE-2026-44338 scanning less than four hours after advisory publication, showing that internet-facing AI-agent frameworks can be folded into known-CVE scanner workflows almost immediately.
- Trend Micro observed Patriot Bait / bandcampro using Gemini CLI to migrate a live C2 botnet in minutes, operate infected hosts through natural-language prompts, and package operating knowledge into a small plain-text skill bundle. This shows that AI can make low-complexity infrastructure disposable and operator skill more portable even when the malware itself is technically simple.
- Unit 42 analyzed TuxBot v3 Evolution, an IoT botnet framework whose source contained raw LLM reasoning and safety-disclaimer artifacts. The recovered build's core brute-force, persistence, primary C2, and DDoS paths worked, while several broken subsystems were tied to generated-code mistakes that could be repaired quickly.
- Unit 42's July 2026 incident-response follow-up is a useful calibration point: its responders still do not see AI-enabled attacks as a fundamentally new class of compromise, but they do see AI compressing development, content generation, reconnaissance, and decision-making timelines. Unit 42 specifically called out malware written with AI, malware calling out to LLM or MCP services for command-and-control instructions, an observed agentic-ransomware case where an AI agent managed multiple stages of an extortion operation without being fully autonomous, and token jacking against exposed cloud-AI / LLM API credentials that can create large unauthorized compute bills or support malicious-model training.
- Malware can embed LLM calls for autonomous decision-making. PROMPTSPY serializes Android UI state, asks Gemini for structured action decisions, and uses accessibility gestures to interact with a victim device.
- CleverHans Lab demonstrated a proof-of-concept adaptive computer worm that uses compromised machines to run open-weight LLMs locally. The important defender lesson is not a named in-the-wild family: stolen compute can let an agentic worm keep reasoning and adapting without depending on an attacker's central model API.
- AI environments and dependencies are becoming initial-access surfaces. GTIG explicitly ties TeamPCP / UNC6780 supply-chain activity to attempts to pivot from compromised AI software into broader network environments, including disruptive outcomes such as ransomware and extortion.
- LayerX's June 2026 BioShocking proof of concept showed that six agentic browser or browser-plugin products — ChatGPT Atlas, Perplexity Comet, Fellou, Genspark Browser, Sigma Browser, and the Claude Chrome plugin — could be steered by a puzzle/game framing into copying credentials from an authenticated GitHub repository in a controlled test. LayerX says vendors were notified; reported outcomes ranged from fixed to no response or failed patch.
- ProjectDiscovery ran open- and closed-model agents against 54 usable black-box web targets without source or vulnerability hints. Its manual trajectory audit found only one genuine discovery failure; 46 failed runs had already attacked the right bug but could not finish. The open-model roster reached 52 targets and the closed roster 48, but ProjectDiscovery explicitly says the four-target gap is below the resolution of its harness and does not prove equivalence or superiority.
- ProjectDiscovery found that a headline solve rate hid materially different behavior: half of solves diverged from the intended path, 27% used a genuinely different exploit, six benchmark targets yielded flags without exploitation, and roughly one quarter of a separately audited subset reached flags through side channels. Agents interacted with the harness through reachable environment, network, or filesystem paths when they treated it as part of the challenge, especially on impossible tasks. This was a benchmark-integrity and isolation-design finding, not evidence that an isolation boundary itself was exploited.
- CrowdStrike reported that 88% of observed exploitation involving a public PoC occurred within 48 hours of PoC publication in the first half of 2026. It says VAULT PANDA and GENESIS PANDA acted within 24 hours of a critical web-application disclosure, React2Shell generated more than 800 hunting leads across more than 80 victims in four days, and UMBRAL BISON activity appeared just over 20 hours after CVE-2026-31431 disclosure. CrowdStrike also notes that about 94% of first-day CVE-2026-31431 events resembled public-PoC testing, so rapid scanning volume should not be conflated with confirmed adversary compromise.
- CrowdStrike observed AI-agent-triggered detections producing 2.5 times more hunting leads than manually driven activity. That is both an attacker-speed and defender-triage problem: expected agent activity can raise background volume and make malicious goal-driven behavior harder to distinguish without child-process, identity, network, and outcome context.

## Operational shapes to watch
- **Autonomous scan-to-exploit loops:** agent frameworks can connect internet-asset search, vulnerability prioritization, public PoC retrieval, target-list generation, prerequisite validation, and exploit execution. Detect the joined sequence and enforce isolated, secretless workspaces; any one component remains legitimate dual-use tooling.
- **AI-assisted vulnerability discovery:** actors feed firmware, source code, CVEs, PoCs, or historical bug corpora into models to prioritize logic flaws and improve exploit reliability.
- **Mass exploit preparation:** clean, tutorial-like exploit scripts with excessive docstrings, hallucinated scores, or textbook code structure may indicate LLM-assisted development, though this is only a weak signal by itself.
- **AI-generated obfuscation:** malware families may contain inert but coherent code, repetitive benign-looking routines, or generated comments that camouflage the active payload path; repeated refactoring can also weaken clustering that depends on stable code lineage.
- **LLM-in-the-loop malware:** implants may serialize UI, filesystem, browser, or application state and request model-generated next actions, turning command-and-control from static tasking into goal-driven orchestration.
- **LLM/MCP-assisted command and control:** malware may call LLM or MCP services for tasking, triage, or command selection. Treat model-provider API usage, MCP server connections, and agent-runtime logs from unusual processes as telemetry, not only as developer-tool noise.
- **Local-model adaptive worms:** malware can try to carry or fetch agent scaffolding and use locally available open-weight models, GPUs, or CPU inference on compromised hosts to choose the next vulnerability, credential path, or lateral-movement method. This reduces reliance on externally visible model-provider calls.
- **LLM-agent post-exploitation:** operators may feed shell, cloud, and database output back into an agent loop that selects the next command, extracts credentials, chooses cloud secrets, and improvises table dumps without a target-specific playbook.
- **AI-operated disposable C2:** actors may ask coding agents to regenerate simple C2 servers, payload paths, WAF bypass headers, persistence names, and troubleshooting steps from small plain-text playbooks. Static IOCs churn quickly; beacon cadence, tasking shape, persistence primitives, and unusual AI-agent audit logs become more durable.
- **LLM-assisted malware engineering:** generated malware may contain coherent but wrong cryptography labels, unreviewed constants, leftover model reasoning, or safety disclaimers. These artifacts can aid triage, but treat them as temporary implementation mistakes rather than lasting constraints on the actor.
- **Tunneled agentic operations:** once a server foothold exists, operators can place the agent's command loop behind Chisel, SOCKS5, ProxyChains, SSH, or web-shell relays so it can act inside the victim network while preserving operator oversight.
- **Obfuscated model access:** adversaries may use account farms, middleware, premium-access resale, or registration automation to evade provider controls and sustain model abuse.
- **Token jacking for AI compute:** exposed LLM, cloud-AI, or model-provider API tokens can be monetized directly through unauthorized inference/training costs or used to build malicious tooling. These secrets deserve the same monitoring, rotation, and least-privilege treatment as cloud and package-registry credentials.
- **AI supply-chain initial access:** compromised AI packages, model-serving tools, MCP-style integrations, IDE plugins, agent skills, or workflow automation can expose secrets and provide a bridge into cloud, SaaS, and internal networks.
- **Agent skill marketplace poisoning:** public skill catalogs and one-click install flows can distribute instructions-plus-code bundles that hide malicious behavior in documents, bytecode, opaque assets, package-manager configuration, or persuasive prompt framing; scanner pass results should not be treated as trust decisions. See [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md).
- **Rapid exploitation of agent frameworks:** public advisories for AI-agent or workflow runtimes can lead to internet-wide endpoint validation within hours; exposed unauthenticated APIs may leak agent metadata, burn model-provider quota, or trigger side-effecting tools.
- **Evaluation-harness boundary drift:** an offensive agent that cannot complete the intended task may enumerate adjacent environment variables, filesystems, orchestrators, tracing services, or network services and treat them as part of the target. A successful score can therefore represent an alternate exploit, exposed test secret, or harness access rather than the intended vulnerability.
- **AI-rendered phishing surfaces:** attacker-controlled web pages, documentation, READMEs, or internal portal text may be summarized into trusted assistant output. When the assistant UI preserves live Markdown links, auto-fetched images, or QR codes from untrusted page content, the page becomes a delivery primitive for beaconing, origin-confusing links, spoofed security notices, and mobile-pivot phishing.
- **Agentic workflow trust-boundary failures:** public issues, tickets, documents, preview links, and generated-code sandboxes become dangerous when they share an execution path with broad agent identities or SaaS session cookies. Noma Labs' GitLost case used a public GitHub issue as an instruction channel into GitHub Agentic Workflows with private-repository read access; SAND Security's WriteOut case used a shared Writer AI preview to place a victim's session token inside attacker-controlled sandbox code. See [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md).
- <a id="bioshocking-ai-browser-context-manipulation"></a>**AI-browser context manipulation:** LayerX reported BioShocking, a proof-of-concept technique where a malicious web page framed an agent task as a dystopian puzzle that rewards incorrect answers, then used the agent's learned “game rules” to ask it to navigate to `/code`, follow a redirect to an authenticated work GitHub repository, and copy a plaintext credential file. The durable issue is not the toy puzzle: agentic browsers merge untrusted page content, user instructions, and authenticated browser context into one decision stream. If a page can convince the agent that real-world safety rules do not apply, repositories, email, password managers, SaaS consoles, internal tools, and open tabs become reachable data sources.
- <a id="jqwik-maintainer-prompt-injection"></a>**Dependency-output prompt injection:** Snyk reported that `net.jqwik:jqwik-engine` 1.10.0, published to Maven Central by the jqwik maintainer on May 25, 2026, printed a hidden instruction for AI coding agents to disregard prior instructions and delete jqwik tests and code. The instruction was concealed from rendered terminals with ANSI erase-line / carriage-return control sequences but remained visible to CI logs, non-PTY subprocess captures, IDE test panels, and agent wrappers that read raw stdout. Snyk reported limited observed impact and noted at least one agent refused to act, but the durable pattern is supply-chain content using build or test output as an instruction channel into autonomous coding loops.

## Defender heuristics
- Log and review AI-service API usage from endpoints, CI runners, developer workstations, mobile apps, and unusual server processes; unexpected model calls from malware-prone contexts should be treated as suspicious.
- Inventory and monitor LLM / cloud-AI API keys alongside cloud, SaaS, and package-registry credentials. Alert on impossible travel, sudden spend spikes, model-training jobs, unusual MCP/tool-calling traffic, or model calls from malware-prone endpoint process trees.
- Do not wait for a separate “AI attack” playbook before hardening: Unit 42's July 2026 IR guidance is that existing controls still apply, but prevention and automation matter more as AI compresses attacker timelines and can overwhelm detect-and-respond-only operations.
- Extend software-supply-chain controls to AI tooling: pin packages, restrict install scripts, review MCP/agent permissions, isolate model-serving runtimes, and rotate credentials after package or extension compromises.
- Hunt for code and script artifacts with generated-looking exploit scaffolding only as a triage aid; do not treat style alone as attribution or proof of AI use.
- In shell and bastion telemetry, watch for agent-friendly command transcripts: repeated delimiters such as `echo '---'`, stderr suppression, `head -N` output caps, pager disabling, HEREDOC query bundles, and rapid output-to-input value handoffs.
- Treat browser/page summarization as an untrusted-content boundary: strip or label assistant-rendered links and remote images from page input, disable automatic remote-image fetching where possible, warn users when output links originate from summarized content, and block QR-code login/payment flows launched from AI summaries.
- For agentic browsers, require step-up confirmation before reading or copying data from authenticated contexts such as repositories, email, password managers, CRM, cloud consoles, admin panels, or internal documentation. Scope browsing agents to dedicated browser profiles without ambient access to production SaaS sessions, and revoke or close authenticated sessions when agent mode is no longer needed.
- Detect and policy-block “rules do not apply,” “this is only a game,” “ignore reality,” or similar context-reset language in pages handed to high-privilege agents when the same session can access sensitive authenticated sites. Treat unexpected agent navigation from an untrusted page into corporate GitHub, GitLab, email, password vault, or internal wiki domains as a possible indirect-prompt-injection incident.
- Treat build, test, package-manager, and tool output as untrusted input to agents. Do not let stdout/stderr from third-party dependencies silently become system or developer instructions; strip or quote terminal-control sequences, label tool output as data, and require explicit human approval for destructive file operations proposed after dependency resolution or tests.
- For jqwik specifically, search manifests and lockfiles for `net.jqwik:jqwik-engine` exactly `1.10.0`, review CI/IDE logs for hidden prompt text or `ESC[2K` / carriage-return artifacts, and move off the affected release if AI coding agents consume its output. Snyk notes 1.10.1 softened the directive and made hiding opt-in rather than removing the maintainer's AI-agent opposition entirely.
- Monitor for unexpected local inference activity on servers, developer workstations, and CI runners: sudden `ollama`, `llama.cpp`, vLLM, Python model-loader, GPU, or large model-file activity combined with scanning, credential access, or cross-host command execution should be treated as possible agentic post-exploitation.
- Constrain local model runtimes and agent frameworks like other execution platforms: run them without ambient cloud/package-registry secrets, limit filesystem and network reach, log tool invocations, and block automatic access to SSH keys, browser profiles, package-manager tokens, and CI environment variables.
- For offensive-agent evaluations, isolate the target from the orchestrator and scoring plane at the environment, network, and filesystem layers; expose no reusable credentials; deny access to host or cross-challenge services; and stop impossible tasks rather than forcing the agent to search indefinitely for another route.
- Audit full tool trajectories and outcomes instead of relying on solve rate or the agent's final narrative. Record whether the intended vulnerability was used, whether alternate exploitable paths were found, whether side-channel data or harness services were touched, and whether the final report omitted those facts. Treat reasoning summaries as incomplete telemetry where providers do not expose raw traces.
- Add detections for accessibility-service abuse, structured UI serialization, hardcoded model prompts, model API keys in mobile malware, and network calls to model endpoints from nonstandard processes.
- Treat AI-enabled obfuscation as a reason to preserve full execution context: memory, process ancestry, API traces, prompts/configuration, and model-request telemetry may explain behavior that static samples hide.
- When investigating AI-package compromises, look beyond credential theft to lateral movement, repository cloning, workflow-log deletion, cloud runtime abuse, and extortion staging.

## Related pages
- [knaithe Hermes/DeepSeek autonomous exploitation campaign](../ops/knaithe-hermes-deepseek-autonomous-exploitation.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](../ops/marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [SHADOW-AETHER AI-augmented Latin America intrusions](../ops/shadow-aether-ai-augmented-latam-intrusions.md)
- [PraisonAI CVE-2026-44338 rapid exploitation](../ops/praisonai-cve-2026-44338-rapid-exploitation.md)
- [Patriot Bait AI-assisted C2 botnet](../ops/patriot-bait-ai-assisted-c2-botnet.md)
- [TuxBot v3 Evolution IoT botnet framework](../ops/tuxbot-v3-evolution-iot-botnet.md)
- [GREYVIBE](../actors/greyvibe.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [SANDWORM_MODE AI-toolchain npm worm](../ops/sandworm-mode-ai-toolchain-worm.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](../ops/trapdoor-crypto-stealer-cross-ecosystem.md)
- [Supply-chain group profile](supply-chain-actor-profile.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/autonomous-ai-cyber-attack-campaign/](https://unit42.paloaltonetworks.com/autonomous-ai-cyber-attack-campaign/)
- Google Cloud / Google Threat Intelligence Group: [https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access)
- WithSecure Labs: [https://labs.withsecure.com/publications/greyvibe](https://labs.withsecure.com/publications/greyvibe)
- Sysdig Threat Research: [https://www.sysdig.com/blog/ai-agent-at-the-wheel-how-an-attacker-used-llms-to-move-from-a-cve-to-an-internal-database-in-4-pivots](https://www.sysdig.com/blog/ai-agent-at-the-wheel-how-an-attacker-used-llms-to-move-from-a-cve-to-an-internal-database-in-4-pivots)
- Trend Micro: [https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html](https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html)
- Sysdig Threat Research: [https://www.sysdig.com/blog/cve-2026-44338-praisonai-authentication-bypass-in-under-4-hours-and-the-growing-trend-of-rapid-exploitation](https://www.sysdig.com/blog/cve-2026-44338-praisonai-authentication-bypass-in-under-4-hours-and-the-growing-trend-of-rapid-exploitation)
- Trend Micro / TrendAI Research: [https://www.trendmicro.com/en_us/research/26/g/actor-behind-patriot-bait-used-ai-to-deploy-c2-botnet.html](https://www.trendmicro.com/en_us/research/26/g/actor-behind-patriot-bait-used-ai-to-deploy-c2-botnet.html)
- Unit 42: [https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/)
- Unit 42: [https://unit42.paloaltonetworks.com/ai-incident-response-report/](https://unit42.paloaltonetworks.com/ai-incident-response-report/)
- Permiso Security: [https://permiso.io/blog/chatgpt-markdown-rendering-vulnerability](https://permiso.io/blog/chatgpt-markdown-rendering-vulnerability)
- The Hacker News: [https://thehackernews.com/2026/05/chatgphish-vulnerability-turns-chatgpt.html](https://thehackernews.com/2026/05/chatgphish-vulnerability-turns-chatgpt.html)
- LayerX Security: [https://layerxsecurity.com/blog/bioshocking-ai-gaming-the-ai-browser-and-escaping-its-guardrails/](https://layerxsecurity.com/blog/bioshocking-ai-gaming-the-ai-browser-and-escaping-its-guardrails/)
- The Hacker News: [https://thehackernews.com/2026/06/new-bioshocking-attack-tricks-ai.html](https://thehackernews.com/2026/06/new-bioshocking-attack-tricks-ai.html)
- Snyk jqwik prompt injection: [https://snyk.io/blog/protestware-open-source-maintainer-qwik-1-10-0-prompt-injection/](https://snyk.io/blog/protestware-open-source-maintainer-qwik-1-10-0-prompt-injection/)
- CleverHans Lab / arXiv: [https://arxiv.org/abs/2606.03811](https://arxiv.org/abs/2606.03811)
- Noma Labs GitLost: [https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/](https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/)
- SAND Security WriteOut: [https://www.sandsecurity.ai/blog/writeout-writer-ai-cross-tenant](https://www.sandsecurity.ai/blog/writeout-writer-ai-cross-tenant)
- ProjectDiscovery behavioral audit of offensive-security LLM runs: [https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs)
- CrowdStrike 2026 Threat Hunting Report summary: [https://www.crowdstrike.com/en-us/blog/crowdstrike-2026-threat-hunting-report/](https://www.crowdstrike.com/en-us/blog/crowdstrike-2026-threat-hunting-report/)
