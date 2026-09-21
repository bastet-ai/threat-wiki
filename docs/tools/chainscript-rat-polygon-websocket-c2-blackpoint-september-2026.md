# ChainScript: a ClickFix-delivered Node.js RAT that resolves its WebSocket C2 from a Polygon smart contract (Blackpoint APG, Sep 21, 2026)

## Summary

Blackpoint Cyber's Adversary Pursuit Group (Sam Decker, Andi Ursry, Nevan Beal) published (September 21, 2026, relayed by The Hacker News the same day) a previously undocumented Windows remote-access trojan named **ChainScript**: a **Node.js-based full-featured RAT** delivered through **ClickFix-style lures** that impersonate Spotify, Zoom Workplace, and Microsoft Teams installs, and that discovers its live C2 by reading a **Polygon (proof-of-stake Ethereum sidechain) smart contract** — an EtherHiding-class blockchain dead-drop used here specifically to front a **WebSocket** control channel. The Blackpoint disclosure came out in the same news cycle as SentinelOne's ROOFDECK writeup (Nostr-profile C2 bootstrap, on-wiki): two implants disclosed one day apart that both move C2 *discovery* onto immutable public infrastructure. Blackpoint's own framing: **"an emerging pattern of malware using development frameworks and blockchain-based C2 discovery to enable infrastructure rotation and complicate traditional indicator-based detection."**

Capability set (per Blackpoint): interactive CMD and PowerShell, file operations, screenshot capture, arbitrary payload deployment, **cryptocurrency wallet enumeration — both desktop wallet apps and browser extensions**, remote JavaScript execution, **self-update**, and a remote persistence-removal command. The malware appears under rotating build names — **ComponentTask33, UpdateDigital, HostShared, OrchidViolet66** — while masquerading as mainstream collaboration/streaming software.

Blackpoint's canonical post URL was not retrievable by this wiki at capture time (site navigation and sitemaps do not yet expose the APG writeup; only the article's `ChainScript.png` hero image is confirmed live on the site's September 2026 uploads path). This page is built from The Hacker News' Sep 21 report of the research; hash/IOC detail should be backfilled when the canonical post surfaces.

## Tags
- tool
- tools
- RAT
- remote-access-trojan
- Node.js
- JavaScript malware
- ClickFix
- copy-and-paste lures
- fake installer
- MSI
- msiexec
- Polygon
- blockchain C2
- smart contract
- EtherHiding
- decentralized C2
- WebSocket C2
- cryptocurrency wallet theft
- browser extension enumeration
- scheduled task persistence
- Registry Run key
- self-updating malware
- VBScript launcher
- hidden PowerShell
- Blackpoint
- Adversary Pursuit Group
- APG
- cybercrime
- takedown resistance
- Windows malware
- ComponentTask33
- UpdateDigital
- HostShared
- OrchidViolet66
- Spotify masquerade
- Zoom masquerade
- Microsoft Teams masquerade
- AML.T0043
- dead-drop resolution

## Delivery chain (per Blackpoint via THN)

1. **ClickFix lure** → user is talked into running a download; the payload lands as a **Windows installer executed via `msiexec.exe`** (example artifact name: **`ComponentTask33-4d14e6ac.msi`**, disguised as Spotify).
2. The MSI **deploys the Node.js runtime** and launches the ChainScript JavaScript agent through **hidden PowerShell and VBScript stages**.
   - The PowerShell stage drops components (Node runtime, agent source, configuration, auxiliary binaries) across **Microsoft-masquerading paths under `%LOCALAPPDATA%`**.
   - The **VBScript is the persistent launcher** for the agent.
3. **Persistence:** a scheduled task with a **Registry Run key fallback** — user-level, no elevation claimed.
4. **C2:** the agent connects over **WebSockets** and pulls tasking, giving the operator interactive control; supported commands include **self-update** and removal of persistence (clean-exit option).

## The durable design: Polygon contract as a C2 resolver

- ChainScript uses an **EtherHiding-style** technique: the **active WebSocket infrastructure is stored in (or resolved through) a Polygon smart contract**, not embedded in the binary. Blackpoint: *"By separating backend discovery from the malware itself and using the Polygon contract as an external resolver, the operator can redirect infected hosts to new infrastructure while retaining the same implant and reconnect workflow."*
- Practical consequences:
  - **Domain/IP blocklists are one step behind by design** — the implant's only built-in dependency is a contract address (+ a public JSON-RPC endpoint), and the operator rotates the *pointed-to* infrastructure with one on-chain transaction.
  - The **contract address is the durable indicator**, not the sockets it currently returns — same monitoring posture this wiki already applies to Aeternum (Polygon `getDomain()`, selector `0xb68d1809`), MovieReaper (Solana account data), and GoCaracal (`eth_getStorageAt` fallback). ChainScript extends the on-chain-resolver family from loaders/backdoors into a **commodity-accessible full RAT delivered by ClickFix** — the pattern is leaving the advanced-actor tier.
  - Egress monitoring on **JSON-RPC calls to public Polygon endpoints from non-crypto workstations** is the behavioral detection; the WebSocket reconnect pattern after a contract read is the second stage.

## Why this matters

- **Node.js as the implant runtime is now a distinct malware class.** Signed-runtime trust (this wiki's Symantec node.exe pattern page, the npmjs.it.com Gradle-cache agent) plus JavaScript's built-in WebSocket/client library makes a RAT *shorter to write* — Blackpoint groups ChainScript with the broader development-framework malware trend; Trend Micro's RedC2/RedShell npm cluster is the same build shape from the registry side.
- **The wallet-enumeration scope (desktop apps + browser extensions) places ChainScript in the crypto-theft monetization lane** while its RAT generality means anything on the host is in scope.
- **Two same-week disclosures, two decentralized C2-bootstrap designs (Polygon contract, Nostr profile field):** C2 *disruption* economics have flipped — seizing domains no longer severs command channels. Hunt posture must shift from blocklists to: contract/relay read behavior, process-lineage anomalies (`msiexec` → hidden PowerShell → `node.exe` on workstations with no dev purpose), `%LOCALAPPDATA%` writes under Microsoft-ish names, scheduled tasks whose target is a VBScript.
- No actor attribution is published; no victim counts; assessment is a cybercrime-adjacent commodity RAT given the ClickFix delivery and consumer-brand masquerade.

## Same-cycle context: PasteSwitch (compromised HBO Max Reddit account pushing ClickFix ads)

THN's same-day report bundles Blackpoint's writeup with **PasteSwitch** (Hudson Rock + ADAMnetworks): the verified official **HBO Max Reddit account (`u/hbomax`) was compromised and used to serve 108 malicious ads over a 48-hour window in mid-September 2026**, launching ClickFix into infostealers on both platforms — **macOS: MacSync, AMOS (Atomic macOS Stealer), fake wallet apps harvesting recovery phrases; Windows: Amatera Stealer plus crypto clippers AnimateClipper and ZigClipper**. Seqrite Labs data puts MacSync infections US-first, then UK/DE/JP/CA/FR/SG/AU/IN/NL. Verified-account hijack bypasses the "official source" heuristic the ClickFix class usually needs to defeat; how the account fell and how many users were led to the fake-update path is not public. (Both stealer branches are on-wiki individually — AMOS tool page, MacSync via Microsoft — PasteSwitch is recorded here as the delivery incident, not a new capability.)

## Detection and hunt

- Process lineage: **`msiexec.exe` → hidden PowerShell → `node.exe`** on non-development workstations; `wscript.exe`/VBScript launchers parenting long-lived `node.exe` with outbound WebSocket connections.
- Persistence: scheduled tasks and Run keys pointing at VBS/Node in `%LOCALAPPDATA%` folders with Microsoft-masquerade naming; build-name strings `ComponentTask33` / `UpdateDigital` / `HostShared` / `OrchidViolet66` in file names, task names, or installers.
- Network: **JSON-RPC POSTs to public Polygon RPC endpoints** from browsers-absent hosts; WebSocket sessions to freshly-contracted endpoints with no DNS history preceding them (the socket target can arrive contract-resolved, skipping your DNS logs — that gap is itself the signal).
- On-chain: monitor the deployed contract addresses when extracted — treat contract address + RPC fetch pattern as the durable IoC pair (Aeternum precedent).
- Self-update channel = re-infection after manual removal; remediation must kill the scheduled task AND the Node agent directory together.

## Sources

- The Hacker News, "ClickFix Lures Deploy ChainScript RAT Using Polygon to Rotate C2 Infrastructure" (Ravie Lakshmanan, Sep 21, 2026) — reporting Blackpoint APG research by Sam Decker, Andi Ursry, Nevan Beal
- Blackpoint Cyber blog (canonical APG post; URL not retrievable at capture — backfill hashes/IOCs)
- Same-cycle: THN coverage of Hudson Rock / ADAMnetworks "PasteSwitch" and Seqrite Labs MacSync telemetry (Sep 21, 2026)
