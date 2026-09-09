# Unit 42: CL-CRI-1171 "Untracked Nightmares" — a pay-per-install marketplace behind commodity-looking loader infections

## Summary
Unit 42's **September 9, 2026** report ("Untracked Nightmares: The Threats Hiding Behind Commodity Infrastructure", Rem Dudas) documents a **pay-per-install (PPI) infection marketplace** tracked as **CL-CRI-1171**, operating "under the radar for at least two years" and distributing an indeterminate number of payloads through a single custom loader the group calls **OfferLoader**. The operation is primarily **cybercrime, financially motivated**, and its two delivery funnels — **11 gaming-optimization YouTube channels** (hundreds of thousands of combined subscribers; notified to YouTube, which terminated them) and a **search-engine-optimization (SEO) poisoning funnel** of trojanized software downloads — target **young gamers** and, on the SEO side, **corporate endpoints including critical infrastructure and government entities**. Two separate intrusion sets in **April 2026** shared one loader delivering **three unrelated malware families** (Insomnia RAT, ARKTunnel, Docro Hijacker); a June 2026 infection delivered two different ones (GCleaner, Socks5Systemz). Unit 42 counts **more than 10,000 distinct OfferLoader samples**, each capable of delivering unique payload combinations — the documented payloads are a small sample of a much larger pipeline.

## Tags
- ops
- operations
- cybercrime
- PPI
- pay-per-install
- loader
- Inno Setup
- steganography
- RAT
- WebSocket
- browser hijacker
- SEO poisoning
- YouTube
- affiliate tracking
- CL-CRI-1171
- OfferLoader
- Insomnia RAT
- ARKTunnel
- Docro Hijacker
- Unit 42

## The operation
- **Structure:** a PPI marketplace — an operator compromises machines and auctions access to multiple buyers; each buyer deploys their own payloads through the same dropper. One endpoint therefore can conceal multiple payloads from unrelated threat actors, each with its own C2 and objective.
- **Discovery:** two "seemingly routine" enterprise infections one week apart (April 2026) — one from a trojanized "Bluetooth Driver for Windows 10.exe" file-sharing archive (affiliate ID `CID=2855`), one from `noiseship[.]cfd` (domain registered 39 days earlier) serving a trojanized `windirstat.exe` (`CID=3075`) — both executed the identical post-exploitation chain. Pivoting on the loader's C2 infrastructure revealed a network of **200+ rotational domains** with a distinctive two-word compound naming pattern (e.g. `bubbleslip`, `churchpail`, `dinosaursjam`) across `.xyz` / `.cfd` / `.space` / `.info`.
- **Gating/evasion:** every tracker URL carries a `click_id` parameter — a Base64 fingerprint of the victim's OS, browser, referring domain, **exact search keyword**, and public IP. Only a valid, fresh `click_id` gets the malware; scanners, crawlers, and analysts receive a **decoy clone of the legitimate WinRAR download page** or broken links. This is why the campaign had almost no public footprint despite high activity. Decoding hundreds of these fingerprints exposed the full YouTube video titles/channels behind the gaming funnel.
- **Scale:** >10,000 unique OfferLoader samples; payload rotation observed **July 2025 – April 2026**; 11 connected YouTube channels with hundreds of thousands of subscribers and millions of views.

## OfferLoader (delivery mechanism)
- A trojanized **Inno Setup** package (chained installers) delivered in a ZIP with social-engineering instructions; the malicious logic lives entirely in the compiled Pascal code section triggered when the install page displays.
- Initial intrusion beacon to `voyagemist[.]space` (another gate: the response file says `ok` — deploy all offers — or `no` — stop).
- Spawns three child processes **`eld0.exe`, `eld1.exe`, `eld2.exe`** — one per "offer" (campaign), each passed affiliate-tracking parameters via command line and then operating as an independent malware campaign with its own infrastructure, C2 protocol, and objective.

## The three documented payload operations
### Operation A — Insomnia RAT (cross-platform, dual-runtime backdoor)
- An upgraded **Node.js backdoor** (lineage noted by Walmart Global Tech in 2025; previously Windows/Linux/FreeBSD single-payload) now targets **Windows and macOS** with platform-specific C2 server lists, **plus a companion Python agent** as a redundant fallback. Named for the C2 User-Agent `insomnia/2023.4.0 Windows`.
- `t.ps1` disables Defender protections (excludes the whole `C:\` drive, suppresses notifications), installs Python and Node.js (Node hidden from Add/Remove Programs via `SystemComponent=1`), and drops `a.dll` + downloads `aa.js` from `stryper[.]info`.
- Node agent: collects MachineGuid/UUID/hostname/OS; HTTPS POST to `/d` for commands (payload types `node`, `cmd`, `ps1`, `sh`, `ow` self-update + download URL); results to `/e`. Persistence: scheduled task **"Maps Performance Task"** under `\Microsoft\Windows\Maps\` (hourly + startup, SYSTEM).
- Python agent (from `aa.amazingshield[.]xyz`): same `/d`/`/e` C2 protocol; second scheduled task **"OOBETaskScheduler"** under `\Microsoft\Windows\Servicing\`; C2 domain `crowdstri[.]com` — a **deliberate typosquat of `crowdstrike[.]com`** to blend into logs.
### Operation B — ARKTunnel (previously unreported WebSocket tunneling RAT)
- `eld1.exe` extracts a ZIP from a **BMP image via LSB steganography** → `ProcorTrex.zip` → **`wscl.exe`**.
- Installs as a Windows service **`wscl-13` or `msvcsrvc`** with delayed autostart; supports **TCP and UDP tunneling** and file execution.
- C2 `reg.pcsdkflyer[.]ca` is decoded from a 39-byte config blob (Base64 + XOR). PE metadata carries fabricated company names; at least **50 samples over a year**, rotating four corporate identities: "EarthLink" (May 2025, coincidental — not the ISP), "EarthChain" (May 2025–Apr 2026, coincidental), **EarthKark** (fake, Feb–Jun 2026), **TamarkLark** (fake, Mar–Jun 2026). Despite a full year of development and 50 samples, ARKTunnel attracted **no public reporting or dedicated tracking** — each sample individually flagged as a generic trojan.
### Operation C — Docro Hijacker (Chrome browser hijacker; first in-the-wild deployment of a modern variant)
- `eld2.exe` (Inno Setup) → `eld2.tmp` (beacons to affiliate tracker `extentrack[.]com`) → drops **`Adblock.dll`**, which bypasses Chrome's **Secure Preferences HMAC-SHA256** integrity check: it extracts Chrome's HMAC key from `resources.pak`, computes valid signatures for modified preference values, and writes them into the Secure Preferences file (anti-tamper bypass).
- Actions: (1) **search hijack** — default search provider changed to `mqsearch[.]com`; (2) installs the **`docro`** Chrome Manifest V3 extension at `C:\ProgramData\DocsHelper\docro\`, which uses the `declarativeNetRequest` API with rules fetched hourly from `vendralo[.]info` to rewrite search-result pages (injecting ads, rewriting affiliate links, redirecting clicks across 190+ Google ccTLD search domains; script loaded from `drelto[.]info/farlix` within the search engine's own origin context — visually indistinguishable from the legitimate page).
- Silent extension updates via `vendralo[.]info/extensionInstaller/updateChromeExtension`; install telemetry to `finersto[.]com` and `extentrack[.]com`. 50+ unique samples contacting `mqsearch[.]com` per VirusTotal. Revives a browser-hijacking technique first seen in 2015 (modern PoC detailed by Synacktiv in 2025); this is the **first documented in-the-wild deployment** of the updated technique.

## Why it matters
- The campaign is a reminder that **commodity-looking loader infections are not minor events**: the loader's deliberate simplicity (no sophisticated evasion, all logic in the packaged Pascal section) plus heavy gating made it exceptionally hard to track, while it quietly delivered possibly thousands of rotational malware bundles — including two previously undocumented families.
- The `click_id` victim-fingerprint gate and decoy pages are a reusable, low-cost anti-scanner technique: security tooling that walks URLs without solving the fingerprinting step only ever sees the decoy.
- The PPI model means **one infection vector can seed multiple unrelated actor payloads on the same host**; hunting one family does not cover the others.

## Defender priorities
1. **Hunt the loader, not the payload:** Inno-Setup-style installers whose payload set changes per download; scheduled tasks **`Maps Performance Task`** (`\Microsoft\Windows\Maps\`) and **`OOBETaskScheduler`** (`\Microsoft\Windows\Servicing\`); processes `eld0.exe` / `eld1.exe` / `eld2.exe`; C2 User-Agent **`insomnia/2023.4.0 Windows`** on HTTPS `/d` and `/e` paths.
2. **Network indicators:** `voyagemist[.]space`, `stryper[.]info`, `aa.amazingshield[.]xyz`, `crowdstri[.]com` (CrowdStrike typosquat), `reg.pcsdkflyer[.]ca`, `mqsearch[.]com`, `vendralo[.]info`, `drelto[.]info`, `finersto[.]com`, `extentrack[.]com`, `noiseship[.]cfd`.
3. **Browser:** unexpected `docro` extension under `C:\ProgramData\DocsHelper\`; `Adblock.dll` loaded into Chrome; default-search-provider changes to `mqsearch[.]com`; Secure Preferences modification events.
4. **Initial-access hygiene:** the SEO-poisoning funnel targets searches for legitimate utilities (WinDirStat, Bluetooth drivers, game "optimization" tools) — treat top-organic results for software downloads from obscure domains as untrusted; prefer vendor-direct download paths.
5. **Treat the YouTube gaming funnel as an active initial-access vector** for consumer and unmanaged endpoints; the 11 channels were terminated by YouTube, but re-registrations and SEO-adjacent Blogspot-style relay pages may persist.

## Assessment limits
- Cluster name **CL-CRI-1171** follows Unit 42's attribution framework; this is **cybercrime activity with no state attribution asserted**.
- The documented payloads are explicitly "only a small sample" of the loader's delivery history; GCleaner and Socks5Systemz (June 2026) and most other delivered families are not analyzed in the report.
- Palo Alto Networks product coverage claims (Advanced WildFire, Advanced URL/DNS Security, Cortex XDR/XSIAM) are vendor statements from the same post.

## Related pages
- [CISA KEV September 8, 2026: four exploited flaws](cisa-kev-stylesmuggler-nable-windows-lpe-september-8-2026.md)
- [Unit 42: two LLM-orchestrated LATAM intrusion campaigns (CL-CRI-1131 / CL-CRI-1163)](unit42-clcri-1131-1163-llm-orchestrated-latam-campaigns-september-2026.md)
- [RMM phishing campaign spanning 46 countries: verbatim disposable infrastructure (ANY.RUN)](rmm-phishing-campaign-46-countries-verbatim-disposable-infra-anyrun-september-2026.md)
- [Counterfeit installers: deceptive software-download campaign (Microsoft Silver Fox / Yinhu)](microsoft-counterfeit-installers-silver-fox-yinhu-fake-download-campaign-september-2026.md)

## Sources
- Unit 42: ["Untracked Nightmares: The Threats Hiding Behind Commodity Infrastructure"](https://unit42.paloaltonetworks.com/ppi-network-malware-campaign-analysis/) (September 9, 2026; Rem Dudas)
