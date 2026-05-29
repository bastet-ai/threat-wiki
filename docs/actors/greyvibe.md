# GREYVIBE

## Summary
**GREYVIBE** is a Russia-nexus activity cluster WithSecure reported in May 2026 after observing persistent targeting of Ukraine and Ukraine-related entities since at least August 2025. WithSecure has not tied the cluster definitively to a previously tracked group, but assesses the activity aligns with Russian state intelligence interests while also showing proximity to the Russian-speaking cybercrime ecosystem.

The durable intelligence value is the combination of multi-vector Ukraine-focused delivery, AI-assisted operational development, and custom malware families. GREYVIBE has used spear-phishing, ClickFix-style fake CAPTCHA pages, fake Ukrainian adult-club sites, drone-charity lures, Android spyware, PowerShell RATs, custom JavaScript / PowerShell obfuscators, and post-compromise scripts to collect intelligence from military, government, civilian, and business targets.

## Tags
- Russia-nexus
- Ukraine
- espionage
- cybercrime ecosystem
- AI
- LLM
- ClickFix
- spear-phishing
- Android spyware
- PowerShell
- RAT
- WebSocket C2
- REST C2
- fake CAPTCHA
- fake dating lures
- Google Drive
- 4sync
- Telegram
- WhatsApp
- RDP
- browser credential theft
- XMRig
- UAC-0098
- TrickBot
- PhantomMail
- PhantomClick
- PrincessClub
- DroneLink
- Nebo
- PhantomRelay
- FallSpy
- LegionRelay
- LOOKVALPS
- LOOKVALJS
- DAYLIGHT
- TEASOUP
- ZAPiXDESK
- WireGuard

## Primary motivation
- **Espionage** against Ukraine and Ukraine-related military, government, civilian, and business entities.
- **Hybrid state / cybercrime overlap**, with Russian-language operators, Moscow-time working patterns, and tradecraft that also touches cybercrime infrastructure or tooling lineages.
- **AI-enabled operational acceleration**, using LLMs and generative tooling to compensate for capability gaps, develop lures and infrastructure, and rotate malware or obfuscation artifacts.

## Campaigns and delivery paths
### PhantomMail spear-phishing
Since August 2025, WithSecure observed at least six spear-phishing campaigns. Messages carried links to ZIP or RAR archives hosted on third-party file-sharing services such as Google Drive and 4sync. The archives used PyInstaller or JavaScript loaders to open decoy PDFs or error prompts while starting the PhantomRelay infection chain in the background.

Reported lures impersonated Ukrainian entities including Kyiv City Council, a Ukrainian energy company, the Main Directorate of the State Emergency Service of Ukraine, and the State Service of Special Communications and Information Protection of Ukraine.

### PhantomClick fake CAPTCHA delivery
In October 2025, GREYVIBE experimented with ClickFix-style fake CAPTCHA pages masquerading as Zoom and LAPAS sites. The pages instructed victims in Ukrainian to run commands under a Cloudflare-themed verification pretext, then redirected to legitimate destinations while launching PhantomRelay.

### PrincessClub dating and adult-club lures
The persistent PrincessClub campaign used fake Ukrainian adult-club websites and Telegram personas to target Ukrainian combatants and other victims. Windows visitors received PhantomRelayV1 or LegionRelay; Android visitors received FallSpy. Later lure-site iterations added WebRTC live-call functionality that could capture victim audio and video after infection, blending malware delivery with potential HUMINT collection.

### DroneLink and Nebo associated activity
WithSecure also links GREYVIBE-adjacent activity to:

- **DroneLink**, fake charity sites claiming to support Ukrainian FPV / UAV initiatives, sharing C2 infrastructure and post-compromise tooling such as WireGuard and ZAPiXDESK with PrincessClub and hosting DAYLIGHT-obfuscated LegionRelay scripts.
- **Nebo**, Russian-language FallSpy and fake-login artifacts masquerading as “СПО НЕБО” / “SPO NEBO” and referencing telephone-exchange numbers consistent with Russian military or defense communications environments.

## Malware, loaders, and obfuscators
### PhantomRelay
PhantomRelay is a PowerShell RAT with a two-stage chain: a fingerprinting script followed by the main RAT client. It communicates over WebSockets, supports PowerShell and Windows command execution, and extends functionality through C2-delivered PowerShell modules.

WithSecure separates the family into:

- **PhantomRelayLite**, a base variant seen in GREYVIBE development activity and unrelated cybercrime clusters, including Microsoft Teams voice-phishing and KongTuke ClickFix delivery chains.
- **PhantomRelayV1**, the first operational GREYVIBE variant, adding watchdog-style persistence and distinct infrastructure while moving from SAWDUST / CRUDEDUST obfuscation to DAYLIGHT.
- **PhantomRelayV2**, a reconstructed second operational variant preserving the core behavior.

### FallSpy
FallSpy is Android spyware first observed in August 2025. It presents decoy content while collecting contacts, call logs, installed apps, SIM-linked phone numbers, device and network details, Wi-Fi SSID, last-known location, public IP, and media files.

### LegionRelay
LegionRelay is a lightweight PowerShell RAT using REST API methods for C2. Client-side functionality focuses on executing operator-issued PowerShell commands, while operators stage additional scripts for file enumeration, file exfiltration, screenshots, browser-data theft, Telegram and WhatsApp data exfiltration, and RDP setup.

### Custom obfuscators and loaders
WithSecure reports four custom-developed components:

- **LOOKVALPS** for PowerShell.
- **LOOKVALJS** for JavaScript.
- **DAYLIGHT**, active from October 2025 and used on initial-stage and post-compromise PowerShell payloads.
- **TEASOUP**, observed from March 2026 as the successor to LOOKVALJS.

WithSecure assesses with moderate-to-high confidence that these were custom GREYVIBE components and with moderate confidence that several were LLM-assisted.

## AI-enabled tradecraft
WithSecure found indicators of systematic use of Ideogram AI, ChatGPT, and Google Gemini across GREYVIBE activity. Reported use cases include:

- Lure image and website generation for PrincessClub and PhantomClick.
- Obfuscator, loader, LegionRelay, backend, and infrastructure development.
- Post-compromise commands, scripts, and tooling delivered through PhantomRelay and LegionRelay.

For defenders, this matters because the actor may refactor components quickly, rotate generated code, and reduce historical backlinks that normally support clustering.

## Attribution notes
WithSecure assesses GREYVIBE is Russian-speaking and operates broadly in the Moscow time zone based on Russian-language comments, Russian administrative panels, developer and C2 locale evidence, operator communications, and activity timing. The same report assesses high confidence that targeting and actions align with Russian state interests.

Cybercrime-overlap indicators include possible use of a unique ISO builder linked to the TrickBot ecosystem / UAC-0098, PhantomRelayLite reuse in unrelated cybercrime clusters, public upload of development samples, slang-heavy development names, and limited XMRig deployment on LegionRelay-infected systems. WithSecure treats direct UAC-0098 continuation as a low-likelihood hypothesis that still warrants monitoring.

## Defender heuristics
- Treat Ukraine-themed file-sharing links, adult/dating lures, fake charity sites, and ClickFix verification pages as connected investigation pivots when PhantomRelay, FallSpy, or LegionRelay appears.
- Hunt for JavaScript or PyInstaller archive loaders that open decoy PDFs / errors before spawning PowerShell, especially after Google Drive or 4sync downloads.
- Flag PowerShell RAT behavior using WebSockets or simple REST polling paired with dynamic C2-delivered scripts, watchdog persistence, screenshot capture, browser-data theft, Telegram / WhatsApp collection, or RDP setup.
- On Android, prioritize FallSpy-like spyware telemetry: decoy UI followed by contacts, call logs, installed-app inventory, SIM identifiers, location, Wi-Fi SSID, public-IP, and media collection.
- Correlate fake CAPTCHA command execution with Ukrainian-language instructions, Zoom / LAPAS impersonation, and Cloudflare-themed verification copy.
- In Ukraine-related environments, preserve script-block logs, PowerShell transcript data, browser and messaging-app access telemetry, RDP configuration changes, WebRTC lure-site traces, archive contents, and C2 traffic before cleanup.
- Do not rely on static code similarity alone; AI-assisted refactoring and generated obfuscation may cause rapid component drift.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](../ops/apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)
- [Ghostwriter](ghostwriter.md)

## Sources
- WithSecure Labs: https://labs.withsecure.com/publications/greyvibe
- WithSecure GREYVIBE IOCs: https://github.com/WithSecureLabs/iocs/tree/master/GREYVIBE/
- The Hacker News summary: https://thehackernews.com/2026/05/new-russian-linked-greyvibe-targets.html
