# Mandiant IR case study: attacker hijacks an ACTIVE AI coding-assistant session and spreads Shai-Hulud across ~100 internal repositories at a SaaS provider (Mandiant AI Risk and Resilience Report 2026, Sep 16, 2026)

## Summary
Mandiant's **AI Risk and Resilience Report 2026** (September 2026 special report; publicly reported by The Hacker News on **September 16, 2026**) contains what appears to be the first incident-response-documented case of an attacker **hijacking a developer's active AI coding-assistant session** and using it as the execution vehicle for a **Shai-Hulud worm deployment**. The victim was an **unnamed software-as-a-service (SaaS) provider**. The mechanism is the trusted-interpreter failure: the AI assistant, operating as a trusted interpreter inside the developer's environment, **recommended installing an external software package that the attacker had poisoned**, and the recommendation was **accepted** — at which point the assistant "inadvertently functioned as a trojan horse." After acceptance, the attacker used the developer's live session to **install an infostealer via a poisoned PyPI package**, **harvest GitHub OAuth tokens**, and **deploy the self-propagating Shai-Hulud worm across approximately 100 internal code repositories**, automating theft of repository secrets and programmatic exfiltration of proprietary product source code. The actor then **poisoned a package inside the organization's own official namespace**, causing a **second infection** when another employee pulled the compromised version. The public case study does **not** say when the intrusion happened or **how the attacker took over the active coding-assistant session** — the open questions that matter most for defenders.

## Tags
- ops
- Shai-Hulud
- supply-chain
- AI
- AI coding assistant
- session hijacking
- trusted interpreter
- infostealer
- PyPI
- GitHub OAuth
- token theft
- worm
- repository secrets
- source code theft
- namespace poisoning
- Mandiant
- incident response
- SaaS provider

## Why this matters
- **The assistant becomes the trojan horse.** Every prior Shai-Hulud / Mini Shai-Hulud wave relied on a human (or CI) *choosing* to install a package, or on a compromised maintainer pushing malicious versions. Here the attacker steers the *recommendation layer itself*: poison what the AI suggests, let the trusted tool do the installing, and the developer's normal trust in the assistant bypasses their own skepticism. The accepted recommendation is the phishing click — except it arrives through a tool the organization deployed on purpose.
- **An active agent session is a privileged session.** The case demonstrates that hijacking the session — not the workstation, not the account — was enough to run installs, harvest OAuth tokens, and deploy a worm. Treat assistant sessions the way you treat an interactive privileged shell.
- **Worm-on-the-inside.** ~100 internal repositories is squarely in the mass-infection scale of the public npm waves, but reached through *one developer session* rather than registry access. Internal repositories are not a safe zone once the worm is inside: the same secret-stealing and self-propagation logic that ran on npm targets private source.
- **Namespace poisoning closes the loop on the victim.** Poisoning a package in the organization's *official* namespace converted the intrusion into a supply-chain event against the victim's own consumers — the second infection came from a colleague pulling the compromised version, not from the attacker touching anything new.

## Case mechanics (as published)
1. **Session hijack.** Attacker gains control of an **active AI coding-assistant session on a developer's workstation** at a SaaS provider. Method and timing not disclosed.
2. **Poisoned recommendation.** The attacker ensures the assistant recommends an **attacker-poisoned external software package**. The recommendation is accepted. Mandiant frames the assistant as a "trusted interpreter" whose accepted recommendation constitutes execution.
3. **Infostealer via poisoned PyPI.** Through the live session the attacker installs an **infostealer using a poisoned PyPI package**.
4. **Credential harvest.** **GitHub OAuth tokens** are stolen from the session/environment.
5. **Worm deployment.** The attacker deploys **Shai-Hulud across ~100 internal code repositories**. The worm **automates theft of repository secrets** and **programmatic exfiltration of proprietary product source code**.
6. **Namespace poisoning / secondary infection.** A package is poisoned **inside the organization's official namespace**; another employee installs the compromised version → second infection.

### Related context from the same report
- Mandiant/GTIG separately state that **UNC6780 (TeamPCP)** — the actor publicly linked to the March 2026 Shai-Hulud wave and CI/CD secrets campaigns — implemented **more than half a dozen different methods to exploit AI tools and the open-source ecosystem**, including **manipulating the behavior of AI coding assistants and LLM security scanners through prompt injection** (incidents following the March 2026 supply-chain compromises). The Shai-Hulud case study itself is not explicitly attributed to UNC6780 in the public text.
- A separate Mandiant OffSec assessment in the same report shows the adjacent **confused-deputy** failure: a role-confusion prompt injection convinced an internal CI/CD chatbot (allowed GitHub as an external domain) to **clone sensitive internal repositories and push them to an attacker-controlled external endpoint** using a PAT for an external repo the testers controlled.
- Another case in the report: an actor **poisoned an internal AI repository and tampered with the assistant's underlying CLI hooks**, achieving RCE **natively through the AI platform's standard operational workflow** — turning the assistant's extensibility framework into the exploitation vector.

## Defensive controls (Mandiant's published recommendations for this case)
- **IDE and CLI verification hooks:** validate all AI-recommended third-party software dependencies against **cryptographic checksums and approved allowlists** before installation.
- **Isolate local credentials:** prevent assistant extensions from accessing raw API keys, long-lived OAuth tokens, or secrets (just-in-time secrets management).
- **Contain egress:** route all workstation dependency traffic through **secure internal repositories** (e.g., an internal artifact registry), so a poisoned package name resolves to your mirror — or to nothing.
- Broader report guidance for AI platforms: require **digital signatures on AI assistant binaries, CLI helper tools, plugins, and MCP servers**; govern internal AI repositories with multi-party approval for skill/hook changes; treat **AI coding assistants and MCP servers as privileged sessions**.

## Defender translation
- **Detection surface:** AI-assistant parentage on package installs. An `npm install` / `pip install` / `uv add` whose process ancestry runs through a coding-assistant CLI or its helper is dual-use signal — log it, alert on it for non-interactive windows, and reconcile recommended packages against your allowlist.
- **The allowlist is the control.** Checksum verification catches tampering with known-good names; only an **approved-registry/allowlist policy** catches attacker-*chosen* names, which is what this case used.
- **OAuth-token blast radius:** GitHub OAuth tokens harvested from developer workstations can read and write repositories without ever touching SSO. Scope device/OAuth grants, monitor for token use from new IPs, and prefer short-lived, per-repository grants.
- **Internal-namespace exposure:** your official-namespace packages are an attacker's second-stage lever once any developer host is compromised. Publishing credentials on developer workstations should be zero-touch (CI-only, OIDC-federated).
- **Open questions to monitor:** how the session was hijacked (session-token theft? localhost API exposure of the assistant's control plane? social engineering of the recommendation flow?), when the intrusion occurred, whether the actor was UNC6780/TeamPCP or another group, and whether other victims show the same "assistant recommended a poisoned package" tell.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md)
- [TeamPCP](../actors/teampcp.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [Developer tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [@zereight/mcp-gitlab unauthenticated SSE PAT exfiltration](../tools/zereight-mcp-gitlab-cve-2026-61560-unauthenticated-sse-pat-exfiltration-september-2026.md)
- [Bifrost CVE-2026-90898 unauthenticated MCP stdio RCE](../tools/bifrost-cve-2026-90898-mcp-stdio-unauthenticated-rce.md)

## Sources
- Mandiant special report, *AI Risk and Resilience Report 2026* (September 2026), Case study 1 "Weaponizing active developer AI sessions to deploy the 'Shai-Hulud worm'": <https://cloud.google.com/security/resources/ai-risk-and-resilience-2026>
- The Hacker News, "Attacker Hijacks AI Coding Assistant Session, Spreads Shai-Hulud Across About 100 Repositories" (September 16, 2026): <https://thehackernews.com/2026/09/attacker-hijacks-ai-coding-assistant.html>
- Prior edition for baseline (2025): <https://cloud.google.com/security/resources/ai-risk-and-resilience>
- Mandiant mitigation guidance for supply-chain compromise (linked from the report's defensive-controls block): <https://cloud.google.com/blog/topics/threat-intelligence/mitigation-guidance-for-supply-chain-compromise>
