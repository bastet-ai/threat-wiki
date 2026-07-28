# Mirage Kitten

## Summary
**Mirage Kitten** is an espionage-focused threat actor also publicly tracked as **UNC1549**, **Smoke Sandstorm**, and **Nimbus Manticore**. Kaspersky's July 2026 reporting describes targeting across aerospace, aviation, defense, telecommunications, government, financial, and small-business environments in the Middle East and Africa.

Keep the aliases as source-reported equivalences, not as proof that every activity published under each name belongs to one operator. The durable operational pattern is tailored social engineering followed by custom Windows implants and tunnelers that preserve access into selected victim networks.

## Tags
- group
- actor
- Mirage Kitten
- UNC1549
- Smoke Sandstorm
- Nimbus Manticore
- Iran-nexus
- espionage
- Middle East
- Africa
- aerospace
- aviation
- defense
- telecommunications
- spear phishing
- fake recruiting
- tunneling
- targeted operations

## Known activity

### Tailored access and delivery
- Kaspersky describes highly targeted spear phishing, fake recruitment portals, trusted-brand and hiring-platform impersonation, and lookalike videoconferencing pages.
- Some lures redirected selected victims to malicious archives on third-party file-sharing services.
- Kaspersky did not establish the initial-access path for most samples in the July 2026 set. Do not infer that every NightLedger, ArcBridge, or BridgeHead deployment began with the same lure.

### July 2026 malware set
- **NightLedger** is a Windows HTTPS backdoor with host reconnaissance, process and file operations, command execution, DLL loading, screenshot capture, and `NetSetup.log` collection.
- **BridgeHead** is a WebSocket SOCKS5 tunneler with enterprise-proxy traversal and per-victim username checks.
- **ArcBridge** is a separate WebSocket tunneler that supports operator-selected proxy sessions and DNS resolution.
- Kaspersky connected the tools through code, behavioral, infrastructure, and tradecraft similarities with earlier Mirage Kitten implants, including TWOSTROKE, Retrograde / MiniFast / MiniUpdate, LIGHTRAIL, and POLLBLEND.

### Victimology reported by Kaspersky
- Egypt
- Jordanian government and SMB environments
- Tanzanian government and SMB environments
- Pakistani aerospace and aviation organizations
- Ethiopian telecommunications companies
- Burkinabè financial-sector entities

## Defender focus
- Hunt together for legitimate-binary DLL search-order hijacking, unusual WebSocket tunnels from user workstations, Windows-integrated proxy authentication by unexpected DLLs, and long-lived TCP relay behavior.
- Scope recruitment, hiring, and videoconference-themed archive delivery against aerospace, aviation, defense, telecommunications, government, and financial personnel.
- Treat Cloudflare-backed actor domains and Azure-hosted lookalike infrastructure as mutable delivery mechanisms rather than sufficient attribution by themselves.
- Preserve suspicious DLLs, parent binaries, proxy logs, C2 paths, mutexes, usernames, and network-flow records before containment.

## Related pages
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](../ops/mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [NightLedger](../tools/nightledger.md)
- [BridgeHead](../tools/bridgehead.md)
- [ArcBridge](../tools/arcbridge.md)
- [Iran-linked threat landscape: access optionality and evidence quality](../notes/iran-linked-threat-landscape-july-2026.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
