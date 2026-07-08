# Phantom squatting: AI-hallucinated domains

## Summary
Unit 42's July 1, 2026 research describes **phantom squatting**: registering web domains that large language models hallucinate as plausible portals, API endpoints, documentation hosts, or service URLs for real brands. The pattern extends slopsquatting from package names to web infrastructure. The delivery mechanism can be an AI assistant itself: a developer, employee, or autonomous agent asks for a service endpoint; the model confidently returns a fictitious domain; and a threat actor that pre-registered the hallucinated domain receives the traffic.

Unit 42's measurement gives the pattern defender durability beyond a single phishing campaign. Across 913 global brands and 685,339 URL-generation queries, researchers collected 2.1 million LLM-generated URLs, found 13,229 confirmed malicious URLs, and identified roughly 250,000 unregistered phantom domains available for preemptive registration. Their monitoring reportedly predicted adversary registration of high-priority hallucinated domains 18-51 days ahead of observed weaponization in multiple cases.

A July 2026 Tel Aviv University / Technion / Intuit paper generalizes the same failure mode to **adversarial hallucination squatting (HalluSquatting)** for agentic applications. Instead of only registering hallucinated domains, the attacker probes for predictable hallucinated resource identifiers such as repository names or agent skills, registers the high-probability false resource, and embeds indirect prompt-injection content that can steer the assistant into tool execution or code execution when a user asks the agent to fetch the real trending resource. The authors report demonstrations against AI coding assistants and agent CLIs including Cursor, Cursor CLI, Windsurf, GitHub Copilot, Cline, Gemini CLI, OpenClaw, ZeroClaw, and NanoClaw, with implementation details redacted.

This is a pattern page, not a named-actor profile. Treat AI-generated URLs and resource identifiers as untrusted supply-chain inputs until resolved against authoritative vendor documentation, DNS ownership, namespace ownership, and allowlisted service endpoints.

## Tags
- patterns
- AI agents
- AI tooling
- supply-chain
- phishing
- domain squatting
- hallucination
- zero-reputation infrastructure
- developer tooling
- autonomous agents
- HalluSquatting
- promptware
- agentic botnets
- Unit 42

## Why this matters
- LLMs can generate plausible but nonexistent domains for brands, APIs, portals, documentation, package mirrors, webhook endpoints, and support resources.
- A newly registered phantom domain starts with little or no malicious reputation, so conventional URL filtering, blocklists, and threat feeds may lag behind first use.
- AI coding assistants and autonomous agents can turn hallucinated URLs into execution-time dependencies: fetching API schemas, documentation, scripts, dependencies, or cloud/webhook configuration directly from attacker-controlled infrastructure.
- The same hallucination surface applies to non-domain identifiers. If an agent guesses a repository, skill, plugin, MCP server, package, or setup resource and then fetches it, the attacker-controlled artifact can become a prompt-injection and command-execution bridge.
- The attack path bypasses traditional email-phishing or malvertising delivery. The trusted assistant becomes the traffic source and recommendation layer.
- The defender lead time is measurable if organizations map their own hallucination surface and monitor registration events for high-risk generated domains.

## Public research anchor
Unit 42 defines phantom domains as hallucinated domains that an adversary has weaponized or could weaponize. Their described lifecycle has four phases:

1. **Adversarial hallucination probing:** query LLMs with realistic user, developer, support, or administrative prompts to map the set of domains a model invents for a target brand.
2. **Preemptive registration:** register high-value hallucinated domains, especially those that appear across models, prompts, or low-temperature / precise settings.
3. **AI-mediated delivery:** rely on the LLM or autonomous agent to recommend, fetch, or execute against the attacker-controlled domain during a normal workflow.
4. **Zero-reputation bypass:** exploit the short window where the domain is new, clean, and not yet represented in reputation systems or blocklists.

Unit 42 reports that its framework tested two distinct LLM model families across multiple temperature settings. The results included:

- 2.1 million unique URLs generated from 685,339 URL queries against 913 brands.
- 809,455 generated URLs that resolved to nonexistent destinations, which normalized to about 250,000 registerable phantom domains.
- 13,229 confirmed malicious URLs already present in model outputs.
- 41,313 additional high-risk URLs such as parked domains or pages with insufficient telemetry.
- Nonexistent-domain rates that varied by model and temperature, with the creative temperature setting yielding a larger hallucination surface.

The important defender point is not the exact count. It is that the hallucination surface is stable enough to prioritize: domains that recur across model families, prompts, and precise configurations are more likely to be returned to real users and therefore more attractive to adversaries.

## Observed abuse patterns
Unit 42's case studies describe both prospective and retrospective validation:

- **Montana Empire phishing kit:** researchers say their pipeline identified a high-risk hallucinated domain 23 days before an adversary registered it and deployed a postal-service marketplace phishing kit. The recovered kit reportedly included an AI coding assistant project directory, linking AI-assisted attack development with AI-hallucinated delivery infrastructure.
- **Postal-service impersonation:** one hallucinated postal-service e-commerce domain was generated across five model/configuration tiers, including a precise setting, then registered and used to host a brand-clone page pushing a malicious Android APK.
- **Banking / database administrator phishing:** Unit 42 reports that a domain used in a UAE bank-themed credential-theft campaign was independently generated later by its pipeline, showing convergence between real attacker infrastructure and model hallucination patterns.
- **Coordinated regional fraud:** multiple phantom domains were registered with matching registrar, nameserver, and privacy-shielding patterns within minutes, then used for localized Bengali-language gambling / jackpot-themed fraud infrastructure.

Unit 42 partially redacted public indicators in the report. For threat.wiki, retain the technique and defender pivots without inventing unredacted domains.

## HalluSquatting / agentic botnet extension

Tel Aviv University, Technion, and Intuit researchers Aya Spira, Stav Cohen, Elad Feldman, Ron Bitton, Avishai Wool, and Ben Nassi published **Beware of Agentic Botnets: Scalable Untargeted Promptware Attacks via Universal and Transferable Adversarial HalluSquatting** in July 2026. Their public site describes responsible disclosure to affected application vendors, foundation-model providers, and marketplace maintainers, plus redaction of directly reproducible exploitation details.

The paper's durable contribution is that hallucination squatting is not limited to domains or package names. The researchers describe a weak-threat-model path where the attacker does not need to email, message, or otherwise directly contact the victim's AI application:

1. **Preparation:** identify a trending external resource such as a repository, agent skill, or plugin that users may ask coding agents to fetch.
2. **Hallucination probing:** query a target agent or foundation model with prompts such as clone, install, fetch, or generate setup commands, then measure which nonexistent identifiers recur.
3. **Squatting:** register the high-probability hallucinated identifier in the relevant namespace and host adversarial instructions or content there.
4. **User trigger:** a legitimate user asks an agent to retrieve the real resource.
5. **Planning and hallucination:** the model plans the task, invents the squatted identifier, and retrieves the attacker-controlled resource.
6. **Context poisoning:** the retrieved content becomes part of the agent's working context and can steer tool use.
7. **Execution:** if the agent has integrated terminal/tool access and permissive approval settings, the poisoned context can lead to remote tool execution, remote code execution, or installation of a bot payload.

The public abstract reports hallucinated resource-generation rates up to 85% in repository-cloning scenarios and up to 100% in skill-installation scenarios, with transferability across foundation models and application layers. The authors say they demonstrated remote tool execution and remote code execution against Cursor, Cursor CLI, Windsurf, GitHub Copilot, Cline, Gemini CLI, OpenClaw, ZeroClaw, and NanoClaw. Treat those as controlled research demonstrations, not evidence of a known in-the-wild botnet.

Defensively, HalluSquatting pushes phantom-squatting controls deeper into the agent planner and tool runtime:

- Force search/lookup before clone, install, fetch, or skill-install actions so the agent resolves real resources instead of relying on generated names.
- Require approval for first-time external resources, especially newly created repositories, skills, plugins, MCP servers, or package names with weak provenance.
- Block auto-run modes from executing commands sourced from newly fetched resources; approvals should show the fetched origin and command text.
- Compare requested resource names against the retrieved namespace, owner, age, popularity, signature/provenance, and maintainer history.
- Log failed/nonexistent resource guesses and later successful fetches of similar newly registered names; this is the repository/skill equivalent of monitoring NXDOMAIN-to-new-registration transitions.

## Tradecraft map

### Initial trust path
- AI assistants asked for official login portals, support portals, developer documentation, API references, webhook endpoints, package mirrors, or service configuration examples.
- AI coding assistants suggesting URLs inside source code, CI/CD configuration, documentation, or runbooks.
- Autonomous agents that browse to, fetch, or download from URLs they generated while completing a task.
- Agentic coding tools asked to clone repositories, install skills/plugins, fetch MCP servers, or generate setup commands for resources not grounded in a verified search result.
- Helpdesk, support, or administrative workflows that treat assistant answers as authoritative.

### Attacker prerequisites
- Ability to query one or more LLMs at scale to map repeatable hallucinated domains.
- Domain registration and hosting infrastructure that can be stood up quickly after a high-value hallucination is identified.
- Ability to register hallucinated resource identifiers in public namespaces such as Git repositories, skill marketplaces, plugin stores, package registries, or documentation hosts.
- Brand-clone, phishing, malware-delivery, documentation-poisoning, or API-impersonation content ready before or shortly after registration.
- Indirect prompt-injection content that can influence an agent after retrieval, plus an execution path where the agent is allowed to invoke terminal, package-manager, or install tools.
- Optional crawler evasion, CAPTCHA, redirect cloaking, or user-agent gating to slow reputation scoring.

### Abuse outcomes
- Credential phishing and session-token theft through fake portals.
- Malware or mobile APK delivery through assistant-recommended brand resources.
- Developer compromise through fake API documentation, SDK download links, package mirrors, setup scripts, or CI/CD webhook examples.
- Agentic compromise when an autonomous tool fetches a schema, script, dependency, or credential-processing endpoint from a phantom domain.
- Agentic botnet seeding when hallucinated repositories or skills cause assistants to execute attacker-supplied install commands on developer machines.
- Data exfiltration if generated service endpoints are embedded into application or pipeline configuration.

## Defender heuristics

### Governance and policy
- Treat AI-generated URLs as suggestions, not authoritative references.
- Require developers and support teams to resolve service URLs from vendor-owned documentation, admin consoles, DNS records, or internal allowlists before use.
- Maintain an allowlist for production API endpoints, package registries, webhook destinations, documentation mirrors, and support portals used by agents or CI/CD.
- For high-value brands and internal products, proactively test common assistant prompts and register or block the highest-confidence hallucinated domains where legally and operationally appropriate.

### Agent and developer controls
- Disable autonomous fetching, script execution, package installation, and credential submission to newly generated domains unless the domain is allowlisted or approved.
- Disable unattended clone/install/fetch workflows for agent-generated repository, skill, plugin, MCP, and package names until an authoritative lookup confirms the namespace owner and resource existence.
- Log assistant-suggested URLs and agent web-fetch destinations; alert when generated domains are newly registered, parked, privacy-shielded, or unrelated to the claimed vendor.
- Log agent-suggested resource identifiers and compare them with actual fetched repositories/skills/packages; alert on typo-like, newly created, low-popularity, or owner-mismatched resources.
- In code review, flag new domains introduced by AI-generated commits, README updates, CI/CD files, package-manager configuration, MCP manifests, and agent plugin/skill instructions.
- Prefer pinned, vendor-signed SDKs and schemas over assistant-discovered download URLs.

### Detection pivots
- Recently registered domains that combine target-brand tokens with support, admin, portal, marketplace, docs, api, webhook, login, cloud, or developer terms.
- Domains first observed in agent, browser automation, CI/CD, or developer endpoint traffic rather than email click telemetry.
- New domains that redirect to legitimate vendor sites during review but serve different content to human browsers, mobile devices, or specific geographies.
- Agent logs showing repeated failed fetches to nonexistent domains followed by a later successful fetch to a newly registered matching domain.
- Agent logs showing repeated failed clone/install attempts for nonexistent repositories, skills, plugins, or packages followed by a successful fetch from a newly created or unfamiliar namespace.
- Sudden references to unfamiliar domains in generated code, runbooks, incident tickets, AI chat transcripts, or MCP/tool outputs.

## Related pages
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Cloud bucket namespace hijacking](cloud-bucket-namespace-hijacking.md)
- [AI-brand impersonation phishing and malvertising](ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Unit 42: https://unit42.paloaltonetworks.com/phantom-squatting/
- HalluSquatting research site: https://sites.google.com/view/agentic-botnets/home
- The Hacker News HalluSquatting coverage: https://thehackernews.com/2026/07/new-hallusquatting-attack-could-trick.html
