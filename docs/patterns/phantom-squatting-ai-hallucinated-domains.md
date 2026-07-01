# Phantom squatting: AI-hallucinated domains

## Summary
Unit 42's July 1, 2026 research describes **phantom squatting**: registering web domains that large language models hallucinate as plausible portals, API endpoints, documentation hosts, or service URLs for real brands. The pattern extends slopsquatting from package names to web infrastructure. The delivery mechanism can be an AI assistant itself: a developer, employee, or autonomous agent asks for a service endpoint; the model confidently returns a fictitious domain; and a threat actor that pre-registered the hallucinated domain receives the traffic.

Unit 42's measurement gives the pattern defender durability beyond a single phishing campaign. Across 913 global brands and 685,339 URL-generation queries, researchers collected 2.1 million LLM-generated URLs, found 13,229 confirmed malicious URLs, and identified roughly 250,000 unregistered phantom domains available for preemptive registration. Their monitoring reportedly predicted adversary registration of high-priority hallucinated domains 18-51 days ahead of observed weaponization in multiple cases.

This is a pattern page, not a named-actor profile. Treat AI-generated URLs as untrusted supply-chain inputs until resolved against authoritative vendor documentation, DNS ownership, and allowlisted service endpoints.

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
- Unit 42

## Why this matters
- LLMs can generate plausible but nonexistent domains for brands, APIs, portals, documentation, package mirrors, webhook endpoints, and support resources.
- A newly registered phantom domain starts with little or no malicious reputation, so conventional URL filtering, blocklists, and threat feeds may lag behind first use.
- AI coding assistants and autonomous agents can turn hallucinated URLs into execution-time dependencies: fetching API schemas, documentation, scripts, dependencies, or cloud/webhook configuration directly from attacker-controlled infrastructure.
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

## Tradecraft map

### Initial trust path
- AI assistants asked for official login portals, support portals, developer documentation, API references, webhook endpoints, package mirrors, or service configuration examples.
- AI coding assistants suggesting URLs inside source code, CI/CD configuration, documentation, or runbooks.
- Autonomous agents that browse to, fetch, or download from URLs they generated while completing a task.
- Helpdesk, support, or administrative workflows that treat assistant answers as authoritative.

### Attacker prerequisites
- Ability to query one or more LLMs at scale to map repeatable hallucinated domains.
- Domain registration and hosting infrastructure that can be stood up quickly after a high-value hallucination is identified.
- Brand-clone, phishing, malware-delivery, documentation-poisoning, or API-impersonation content ready before or shortly after registration.
- Optional crawler evasion, CAPTCHA, redirect cloaking, or user-agent gating to slow reputation scoring.

### Abuse outcomes
- Credential phishing and session-token theft through fake portals.
- Malware or mobile APK delivery through assistant-recommended brand resources.
- Developer compromise through fake API documentation, SDK download links, package mirrors, setup scripts, or CI/CD webhook examples.
- Agentic compromise when an autonomous tool fetches a schema, script, dependency, or credential-processing endpoint from a phantom domain.
- Data exfiltration if generated service endpoints are embedded into application or pipeline configuration.

## Defender heuristics

### Governance and policy
- Treat AI-generated URLs as suggestions, not authoritative references.
- Require developers and support teams to resolve service URLs from vendor-owned documentation, admin consoles, DNS records, or internal allowlists before use.
- Maintain an allowlist for production API endpoints, package registries, webhook destinations, documentation mirrors, and support portals used by agents or CI/CD.
- For high-value brands and internal products, proactively test common assistant prompts and register or block the highest-confidence hallucinated domains where legally and operationally appropriate.

### Agent and developer controls
- Disable autonomous fetching, script execution, package installation, and credential submission to newly generated domains unless the domain is allowlisted or approved.
- Log assistant-suggested URLs and agent web-fetch destinations; alert when generated domains are newly registered, parked, privacy-shielded, or unrelated to the claimed vendor.
- In code review, flag new domains introduced by AI-generated commits, README updates, CI/CD files, package-manager configuration, MCP manifests, and agent plugin/skill instructions.
- Prefer pinned, vendor-signed SDKs and schemas over assistant-discovered download URLs.

### Detection pivots
- Recently registered domains that combine target-brand tokens with support, admin, portal, marketplace, docs, api, webhook, login, cloud, or developer terms.
- Domains first observed in agent, browser automation, CI/CD, or developer endpoint traffic rather than email click telemetry.
- New domains that redirect to legitimate vendor sites during review but serve different content to human browsers, mobile devices, or specific geographies.
- Agent logs showing repeated failed fetches to nonexistent domains followed by a later successful fetch to a newly registered matching domain.
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
