# Funnull RingH23 and MacCMS supply-chain attacks

## Summary
**Funnull** is a cybercrime-enabling infrastructure provider also known as Fangneng CDN. QiAnXin XLab reports that, after U.S. Treasury sanctions, Funnull-linked activity resurfaced through a campaign combining compromised GoEdge / CDN management infrastructure, the **RingH23** Linux toolkit, typosquatted CDN domains, and **MacCMS** upgrade-channel poisoning.

The durable threat-intelligence value is the blend of infrastructure-provider compromise and downstream web supply-chain abuse. XLab ties the activity to prior Funnull-linked JavaScript injection operations, including Polyfill.io-style and GoEdge poisoning incidents, and describes payloads that hijack web traffic, replace cryptocurrency wallets, persist on Linux nodes, conceal components with `LD_PRELOAD`, and inject malicious JavaScript into large visitor populations.

## Tags
- ops
- operations
- Funnull
- RingH23
- MacCMS
- GoEdge
- CDN
- supply-chain
- web supply chain
- JavaScript injection
- traffic hijacking
- cryptocurrency theft
- wallet replacement
- typosquatting
- LD_PRELOAD
- rootkit
- Udev persistence
- Nginx module
- Redis backdoor
- cybercrime
- pig-butchering
- infrastructure
- OFAC
- incident response

## Why this matters
- Funnull sits in the infrastructure layer used by scam and cybercrime ecosystems; compromise or operator control of CDN-like services can produce many downstream victims without touching each site directly.
- XLab observed `client.110.nz` with about 1.6 billion passive-DNS resolutions, and estimated that one typosquatted CDN domain may have reached millions of users on a peak day, making the campaign population-scale rather than site-local.
- The campaign uses supply-chain primitives defenders often miss: poisoned CMS upgrade channels, malicious Nginx modules, CDN-domain typosquats, JavaScript injection, and edge-node persistence.
- The payload set supports both monetization and long-lived access: gambling / pornography redirects, cryptocurrency wallet replacement, malicious script injection, Redis-style backdoor control, and userland hiding.
- XLab's attribution pivots connect the activity to scripts used in the February 2024 Polyfill.io supply-chain attack and two official GoEdge poisoning incidents in May 2024.

## Operational characteristics
- **Initial discovery:** XLab detected `download.zhw[.]sh` distributing a low-detection Linux ELF downloader. The sample referenced `client.110[.]nz`, which XLab saw at very high passive-DNS volume.
- **GoEdge management compromise:** XLab says attackers first compromised a GoEdge management node, implanted `infection_init`, and used SSH remote commands to force edge nodes to download and execute `downloader_init`.
- **RingH23 toolkit:** XLab named the toolkit after recurring `RING04H` strings and XOR-23 configuration handling. Components include `udev.sh` / `udev.rules` for Udev persistence, `module.so` / Badnginx2s as a malicious Nginx module, `ring04h_office_bin` / Badredis2s for long-term backdoor control, and `libutilkeybd.so` / Badhide2s as an `LD_PRELOAD` userland rootkit.
- **Traffic and wallet manipulation:** the malicious Nginx module supports traffic hijacking, cryptocurrency wallet replacement, and JavaScript injection into served pages.
- **Typosquatted CDN domains:** injected scripts used lookalike infrastructure such as `code.jquecy[.]com`, `cdn.jsdclivr[.]com`, `cdnjs.clondflare[.]com`, and `static.bytedauce[.]com` to impersonate major JavaScript/CDN providers.
- **MacCMS poisoning:** XLab describes MacCMS upgrade-channel poisoning as a second supply-chain path, letting attackers reach sites through trusted update workflows instead of only direct host compromise.
- **Attribution:** XLab links the JavaScript and infrastructure patterns to Funnull-linked activity, including Polyfill.io-style and GoEdge poisoning operations, and notes Funnull's role as an infrastructure provider for Southeast Asian pig-butchering operations.
- **Sanctions context:** the U.S. Treasury sanctioned Funnull in 2025; XLab assesses the later activity as a resurfacing under a new identity rather than a clean break.

## Defender heuristics
- Treat CDN, edge-cache, GoEdge, and CMS-update infrastructure as Tier-0 for public web integrity; audit them with the same rigor as identity providers and deployment systems.
- Hunt web responses and templates for unexpected script sources that visually imitate trusted CDN brands, especially `jquecy`, `jsdclivr`, `clondflare`, and `bytedauce`-style domains.
- On Linux edge nodes, inspect Nginx module load paths, Redis-adjacent processes, `LD_PRELOAD` configuration, `/etc/ld.so.preload`, Udev rules, suspicious `udev.sh` files, and hidden or renamed binaries containing `ring04h`, `office_bin`, `module.so`, or `libutilkeybd.so` strings.
- Review GoEdge management nodes for unauthorized SSH fan-out, new task modules, unexplained remote command execution, and unexpected downloads from `download.zhw[.]sh` or related domains.
- For MacCMS estates, verify update sources, compare deployed code to trusted release artifacts, and investigate any update that introduced remote JavaScript loaders, obfuscated PHP, or unexpected CDN references.
- Search web analytics, DNS logs, CSP reports, proxy logs, and browser telemetry for typosquatted CDN domains and sudden redirect chains to gambling, pornography, scam, or malware-delivery sites.
- If compromise is confirmed, preserve edge-node disks, memory/process listings, Nginx configuration, CMS update artifacts, web roots, SSH logs, management-plane logs, DNS/proxy evidence, and injected JavaScript before cleanup.
- Rotate credentials and API keys reachable from compromised CDN / CMS / edge nodes, including deployment credentials, origin credentials, database secrets, cloud tokens, and management-plane SSH keys.

## Related pages
- [Ghost CMS CVE-2026-26980 ClickFix poisoning](ghost-cms-cve-2026-26980-clickfix-poisoning.md)
- [Mr_Rot13 cPanel CVE-2026-41940 backdoor campaign](mr-rot13-cpanel-cve-2026-41940-backdoor-campaign.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)

## Sources
- [QiAnXin XLab](https://blog.xlab.qianxin.com/funnull-resurfaces-exposing-ringh23-arsenal-and-maccms-supply-chain-attacks/)
- [U.S. Treasury sanctions notice](https://home.treasury.gov/news/press-releases/sb0149)
