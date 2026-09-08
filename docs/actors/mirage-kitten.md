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
- Tortoiseshell
- Charming Kitten
- GalaxyGato
- Subtle Snail
- Iran-nexus
- espionage
- Middle East
- Africa
- aerospace
- aviation
- defense
- telecommunications
- FinTech
- spear phishing
- fake recruiting
- coding challenge
- Node.js
- JavaScript
- NodeRabbit
- PollCat
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

### August 2026 toolset expansion (Group-IB)
- Group-IB (August 26, 2026) linked the actor to **Tortoiseshell** (Imperial Kitten / Unyielding Wasp) within the **Charming Kitten** cluster and documented a **reverse SSH tunneling utility** (masquerading as the Windows Terminal Server SDK API, to `172.86.98[.]113:443`) and a **TWOSTROKE-like C++ backdoor** mimicking `wtsapi32.dll` with three hard-coded HTTPS C2 servers.
- Aliases surfaced by Group-IB: GalaxyGato, Mirage Kitten, Screening Serpens, Smoke Sandstorm, Subtle Snail, UNC1549.
- Treat the Tortoiseshell / Charming Kitten cluster framing as source-reported linkage, not a multi-agency confirmed alias chain.

### September 2026 Node.js/JavaScript implants (Kaspersky)
- Kaspersky GReAT (September 1, 2026) disclosed **NodeRabbit** (a Node.js RAT) and **PollCat** (a JavaScript RAT), the group's first publicly documented Node.js/JavaScript implants — a departure from its native DLL-search-order-hijacking malware. Both are cross-platform (Windows, Linux, macOS; NodeRabbit also WSL).
- **NodeRabbit** (3 variants) is delivered through trojanized "coding challenge" archives (bundled `colorized_terminal` / `pretty-log` npm packages); variant 3 adds 12 commands (23 total) and developer-workflow persistence (a fake "GitHub Copilot Helper" VS Code extension and `# shepherd-persist` injection into `.git/hooks/post-merge` / `post-checkout`). C2 over Azure + Cloudflare chains.
- **PollCat** is delivered inside a trojanized React `RankChallenge-react` "assessment" with a recruiter-supplied OTP; it registers via `POST /beacon` and treats an **HTTP 400** response (carrying a `socketId`) as success — the same handshake as the group's historical Retrograde/MiniFast. C2 on `sahi-finance[.]com` and `gamebarapp*` Azure domains.
- Delivery is recruiter-themed social engineering (fake "technical assessments" on Amazon S3), targeting **aviation and FinTech** in the Middle East and Africa (Egypt, Ethiopia, Afghanistan observed).
- Lure hosting shifted from prior onlyoffice.com to **Amazon S3**.

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
- **Scope the coding-challenge / "technical assessment" recruiting surface.** A recruiter DM that hands a developer a time-limited coding-challenge ZIP (often on S3) to clone and run is high-risk: block or sandbox execution, and hunt for a `node`/`node.exe` (or renamed copy) spawning from a project's `node_modules/.cache/`, a root `package.json` named `ctf-server`, a recruiter-supplied OTP flow, and a fake "GitHub Copilot Helper" VS Code extension.
- **Inspect developer-workflow persistence** introduced by NodeRabbit v3 / PollCat: `# shepherd-persist` in `.git/hooks/post-merge` / `post-checkout`, `NetSync_<user>` scheduled tasks, `~/.node_packages`, and `com.harsh.requireobject.plist`.
- **C2 telemetry.** Correlate outbound HTTPS to the Azure/Cloudflare C2 domains; for PollCat, a **non-2xx (HTTP 400) JSON response carrying a `socketId`** is a strong C2-protocol indicator.
- Treat Cloudflare-backed actor domains and Azure-hosted lookalike infrastructure (including Azure subdomains that embed the target organization's name) as mutable delivery mechanisms rather than sufficient attribution by themselves.
- Preserve suspicious DLLs, parent binaries, proxy logs, C2 paths, mutexes, usernames, and network-flow records before containment.

## Related pages
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](../ops/mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [Mirage Kitten NodeRabbit / PollCat coding-challenge campaign](../ops/mirage-kitten-noderabbit-pollcat-coding-challenge-september-2026.md)
- [NightLedger](../tools/nightledger.md)
- [BridgeHead](../tools/bridgehead.md)
- [ArcBridge](../tools/arcbridge.md)
- [NodeRabbit](../tools/noderabbit.md)
- [PollCat](../tools/pollcat.md)
- [Iran-linked threat landscape: access optionality and evidence quality](../notes/iran-linked-threat-landscape-july-2026.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
- Kaspersky GReAT, September 1, 2026: [Mirage Kitten targeting aviation and FinTech sectors across the Middle East and Africa with a new malware set](https://securelist.com/mirage-kitten-new-backdoors-noderabbit-pollcat/121244/)
- Group-IB, "Nimbus Manticore Expands Toolset With TWOSTROKE-Like Backdoor and SSH Tunneler" (via The Hacker News, August 26, 2026): [Nimbus Manticore Expands Toolset With TWOSTROKE-Like Backdoor and SSH Tunneler](https://thehackernews.com/2026/08/nimbus-manticore-expands-toolset-with.html)
