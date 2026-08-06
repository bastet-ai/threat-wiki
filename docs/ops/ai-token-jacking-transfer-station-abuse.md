# AI token-jacking transfer-station abuse

## Summary
On August 6, 2026, Unit 42 reported a growing set of incident-response cases in which criminals stole developer API keys for commercial AI platforms and used the victims' accounts to fund high-volume model access. Unit 42 calls the activity **token jacking**. The stolen keys were integrated into gray-market AI proxy services known as **transfer stations**, sometimes within minutes of exposure.

Unit 42 says transfer stations can generate tens of millions of API calls per day. In one response pattern, usage reached nearly $1 million in charges before discovery and containment. The report publishes source-IP, domain, and user-agent pivots associated with recent cases, but it does not identify a single operator, victim, affected model provider, initial-access campaign, or universal intrusion chain.

## Tags
- ops
- operations
- AI
- LLM
- credential theft
- API keys
- token jacking
- gray market
- transfer stations
- supply-chain
- npm
- Shai-Hulud
- Miasma
- access brokers
- financial fraud

## Why this matters
- Stolen model-provider keys are immediately monetizable without deploying cryptominers or maintaining access to the victim host. The bill remains with the legitimate account and may grow until a billing cycle or anomaly alert exposes the abuse.
- Unit 42 observed exposed credentials being added to transfer-station infrastructure within minutes. Containment therefore requires rapid provider-side revocation, not only endpoint cleanup.
- Transfer stations commonly use open-source `new-api` or `one-api` proxy software to present one interface across multiple official model APIs, rotate real credentials, meter usage, and issue their own credits.
- Unit 42 says privileged developer accounts obtained through infostealers, phishing, or access brokers can also be used to provision keys, raise spending limits, and disable usage alerts or logging.
- Source repositories, file shares, developer endpoints, CI/CD environments, and package-install paths all become credential sources. Unit 42 specifically warns that self-propagating npm attacks such as Shai-Hulud and Miasma could supply large pools of AI credentials to this market.
- That supply-chain link is a risk assessment, not evidence that the published token-jacking cases were caused by ChainDrop, Shai-Hulud, Miasma, or TeamPCP.
- Developers using discounted transfer stations also expose prompts and outputs to an untrusted intermediary and may receive responses from a cheaper model than the service advertises.

## Observed operating model
1. An attacker steals an already provisioned AI API key or takes over an account able to create keys and change billing controls.
2. The attacker adds the credential to a transfer-station pool. Unit 42 observed this occurring within minutes in some cases.
3. The transfer station proxies customer traffic to official AI services through the stolen credential while presenting its own credits, routing, and pricing.
4. High-volume users consume the victim's quota. Unit 42 observed tens of millions of calls per day and connected malicious queries to hosts running `new-api`.
5. The victim discovers the activity through spend, usage, login, or infrastructure anomalies; cyclic billing and default-unlimited scaling can delay that discovery.

## Confidence and limits
- Unit 42 bases the report on incident-response cases and publishes a concrete indicator set for recent activity.
- The report does not say that every listed source IP or transfer-station domain belongs to one actor or campaign. Infrastructure can be shared, reassigned, proxied, or used by both operators and customers.
- `new-api`, `one-api`, and the reported `Go-http-client/2.0,gzip(gfe)` user agent are not malicious by themselves. Correlate them with unexpected model usage, stolen-key evidence, billing changes, or provider-side authentication events.
- Unit 42 discusses competing nation-state access to frontier models as a possible transfer-station use case; it does not attribute the listed incidents or indicators to a government.
- The report does not name affected AI providers or publish victim identities, exact event timestamps, API methods, request paths, hashes, or malware samples.

## Indicators and hunting pivots

### Transfer-station infrastructure
- `amutes[.]com`
- `abb1[.]life`

### Source IPs associated with malicious API calls
- `3.235.109[.]125`
- `116.105.166[.]148`
- `172.96.142[.]186`
- `38.46.219[.]166`
- `38.46.219[.]163`
- `38.46.219[.]162`
- `23.237.196[.]170`
- `15.204.106[.]173`
- `104.243.42[.]117`
- `198.255.70[.]210`
- `47.88.103[.]81`
- `47.251.72[.]239`

### Source IPs associated with malicious logins or credential theft
- `117.72.74[.]48`
- `207.246.106[.]162`
- `23.236.182[.]215`
- `95.214.112[.]26`

### HTTP pivot
- `Go-http-client/2.0,gzip(gfe)` — user-agent value Unit 42 associated with malicious API calls

Treat all network indicators as historical pivots. Validate ownership and expected business use before blocking, and preserve provider, proxy, DNS, authentication, and billing telemetry.

## Defender actions

### Immediate triage
1. Inventory model-provider and cloud-AI keys across developer endpoints, CI/CD variables, repositories, secret stores, file shares, notebooks, agent runtimes, and local configuration files.
2. Review provider-side API usage by key, model, source address, region, user agent, time, request volume, token volume, and spend. Compare against known workloads and deployment egress.
3. Search authentication and administrative logs for the four malicious-login IPs, unexpected key creation, spending-limit changes, alert suppression, log changes, and privileged-account access.
4. Search API and egress logs for the twelve malicious-call IPs, the two transfer-station domains, and the reported user agent. Require multiple correlated signals before declaring compromise.
5. If a key is exposed or usage is unexplained, disable or revoke it at the provider immediately, preserve evidence, create a replacement with narrower scope, and update only verified workloads.
6. If a developer host, runner, package install, or repository is the suspected source, isolate it and investigate all co-resident cloud, source-control, package-registry, SSH, wallet, and SaaS credentials. Do not rotate only the AI key.
7. Contact the model provider's abuse and billing teams promptly with event times, key identifiers, source addresses, and usage records; do not assume fraudulent charges will be reversed.

### Preventive controls
- Replace long-lived developer keys with short-lived credentials or just-in-time brokered access where the provider supports it.
- Route model access through a controlled AI gateway with machine or workload identity. Keep provider keys out of developer workstations, source trees, notebooks, and build logs.
- Set hard spend and rate limits rather than alert-only thresholds. Alert on deviations from each workload's baseline, new models, new regions, new source networks, and sudden concurrency changes.
- Restrict API keys by project, model, endpoint, source network, and environment where supported. Separate development, CI, testing, and production credentials.
- Prevent privileged developer identities from silently changing billing limits or disabling alerts and logs; require approval and produce independent audit events.
- Restrict model-provider access to known egress and investigate use from residential, hosting, transfer-station, or unexpected geographic networks.
- Deny package lifecycle scripts by default where feasible, apply dependency cooldowns, inspect new package versions, and treat developer-package compromise as a multi-secret exposure.
- Ban unapproved gray-market AI proxies for organizational work. They can observe prompts, return substituted models, and conceal the true provider and data path.

## Open questions
- Which AI providers, model families, organizations, and account types were affected in the reported cases?
- How many incidents and transfer stations underpin the report, and over what observation window?
- Which listed IPs represent operators, proxy infrastructure, transfer-station customers, or credential-access infrastructure?
- Were any recent cases traced to npm supply-chain compromises, infostealers, repositories, access brokers, or phishing?
- What provider-side controls detected or failed to stop the near-$1 million usage event?
- Will providers publish revocation, billing-dispute, source-restriction, and short-lived-credential guidance tailored to these cases?

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- Unit 42: [Token Jacking: Cybercriminals Could Be Stealing Your AI Resources](https://unit42.paloaltonetworks.com/ai-token-jacking/)
