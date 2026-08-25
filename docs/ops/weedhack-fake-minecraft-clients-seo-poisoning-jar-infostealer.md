# Weedhack: fake Minecraft clients and SEO poisoning deliver JAR infostealer

## Summary
McAfee Labs (via The Hacker News, August 24, 2026) reported that several lookalike websites are **still actively distributing the Weedhack malware family** to gamers, masquerading as Minecraft clients. McAfee detected and blocked **more than 6,300 attempts** to reach malicious sites. Weedhack was first documented by McAfee in **June 2026**; it uses **SEO poisoning and YouTube** to redirect traffic to bogus domains that replicate legitimate Minecraft projects — including branding, feature lists, FAQs, installation guides, developer credits, and links to genuine GitHub repositories. The attack is a multi-stage sequence ending in **JAR payloads** that collect system information, **configure Microsoft Defender exclusions**, and steal sensitive data. Notably, **one malicious site was built with Lovable**, an AI-powered website builder — further lowering the barrier to convincing malicious infrastructure. Nearly half of the identified malicious URLs were **Discord links (49.6%)**, followed by **MediaFire (23.4%)** and **GitHub (8.2%)**, showing attackers leveraging familiar platforms alongside fake sites.

## Tags
- ops
- operations
- Weedhack
- Minecraft
- fake Minecraft client
- gaming malware
- JAR payload
- infostealer
- SEO poisoning
- YouTube
- Discord link abuse
- MediaFire
- Lovable
- AI website builder
- Microsoft Defender exclusion
- McAfee Labs
- Java

## Distribution
- **SEO poisoning:** fake domains rank at the top of Google, Bing, Brave, and DuckDuckuck search results for legitimate Minecraft client/mod names (McAfee notes both Xenon Client and Nova Client fakes page-one across all four engines).
- **YouTube redirect:** video links and comments route to the bogus domains.
- **Platform abuse:** Discord links (49.6% of malicious URLs), MediaFire (23.4%), and GitHub (8.2%) carry the payload, so blocklists and URL-reputation feeds must scope these platforms, not just the fake domains.
- **AI-built infrastructure:** at least one fake site was generated with **Lovable** (an AI website builder), meaning malicious infrastructure can now be assembled faster and more convincingly than before.

## Recorded malicious domains
- `glazed-client[.]com` (replicates glazedclient[.]com, a free/open-source Minecraft add-on)
- `radium-client[.]com` (replicates radiumclient[.]com, a paid Minecraft client)
- `seedcrackerx.github[.]io` (replicates seedcrackerx[.]com, Minecraft seed-cracking software)
- `cheatlib[.]xyz` (claims to be a "modern Minecraft mod library" with 1.6M+ downloads)
- `meteorclients[.]com` (replicates meteorclient[.]com)
- `22qq-client[.]com` (impersonates a Minecraft mod for Crystal PvP servers)
- `kryptonclientcrack.lovable[.]app` (replicates kryptonclient[.]org, a paid Minecraft tool for DonutSMP; built on Lovable)
- `nova-client[.]com` (impersonates the open-source Nova Client)
- `xenoclient[.]lol` / `xenonclient[.]com` (impersonate Xenon Client)

## Payload behavior
- Multi-stage download sequence culminating in a **JAR payload** (Java execution chain on Windows).
- The JAR **collects system information** and **steals sensitive data** (infostealer behavior).
- It **sets Microsoft Defender exclusions** — a deliberate AV-evasion step that also leaves a strong forensic artifact.
- Initial documentation (June 2026) confirmed SEO poisoning + YouTube as the primary redirect vectors.

## Defender heuristics
1. **Hunt Microsoft Defender exclusion creation from Java/JAR processes** — a `java` process modifying Defender exclusion paths is a Weedhack signature (and a general gaming-malware indicator).
2. **Scope URL reputation to the abused platforms:** Discord, MediaFire, and GitHub links are the primary payload carriers, so domain-level blocklists of the fake Minecraft sites miss most of the traffic.
3. **Validate download destinations for gaming tools:** check that a "Minecraft client/mod" download resolves to the project's canonical domain (compare against the genuine GitHub/official site), and treat `github[.]io` lookalikes and `.lovable[.]app` subdomains as hostile in gaming contexts.
4. **Treat AI-builder lookalikes as a new infrastructure class:** Lovable/`lovable[.]app` and similar builder-hosted domains are cheap, disposable, and convincing — add builder-platform domains to phishing/typosquat watchlists.
5. **Monitor search rankings for your org's tool names** — if your project is a Minecraft-adjacent name (or any widely searched tool name), check whether SEO-poisoned lookalikes hold top results on major engines; Weedhack's fakes are still live and ranking.

## Related pages
- [OX Security: ClickFix phishing pages hidden in 24 npm packages, using registry mirrors as payload storage](ox-clickfix-phishing-npm-mirror-payload-storage.md)
- [Fake TradingView macOS stealer delivered by paid YouTube ad](fake-tradingview-macos-stealer-malvertising.md)

## Sources
- The Hacker News: [Weedhack Malware Spreads via Fake Minecraft Clients and SEO Poisoning](https://thehackernews.com/2026/08/weedhack-malware-spreads-via-fake.html)
- McAfee Labs: [Weedhack Minecraft malware — fake gaming websites & SEO poisoning](https://www.mcafee.com/blogs/other-blogs/mcafee-labs/weedhack-minecraft-malware-fake-gaming-websites-seo-poisoning/)
