# TWINLOOT: modular Python implant running M365 C2 inside trusted Microsoft services

## Summary
**TWINLOOT** is a previously undocumented, modular, **PyArmor-hardened Python implant framework** disclosed by Ontinue's Cyber Defense Center after discovery during an investigation into an ongoing campaign in **July 2026**. Its defining characteristic is that it operates its **entire command-and-control infrastructure inside trusted Microsoft services**, making traffic virtually indistinguishable from legitimate activity:

- **Tasking** flows through **SharePoint Online file dead-drops via the Microsoft Graph API**.
- **Interactive operator access** routes through **WebRTC DataChannels relayed by Microsoft Teams TURN servers**.
- Graph-API traffic is driven through a **headless instance of the victim's own Edge browser**, connected over Chrome DevTools Protocol (CDP).

Ontinue describes it as the first such tool to combine **Microsoft 365 dead-drop C2, Teams TURN relay abuse, and headless-browser transport** under a single umbrella.

## Tags
- ops
- operations
- TWINLOOT
- Python implant
- PyArmor
- Microsoft 365
- SharePoint
- Graph API
- WebRTC
- Teams TURN relay
- headless browser
- CDP
- dead-drop
- credential theft
- fake lock screen
- reverse SOCKS5
- persistence
- STAC4749
- Ghost Calls
- Backdoor.Turn
- msaRAT
- Chaos ransomware
- Ontinue

## Initial access
Assessed to be **social engineering via Microsoft Teams**: the actor masquerades as IT support and persuades a target to run a **PowerShell command** that downloads an archive containing the Python runtime and a **~39 MB compiled payload (`bootstrap-fat.pyc`)** that serves as the loader for TWINLOOT. The operator is characterized as knowledgeable in offensive tradecraft and Microsoft cloud architecture.

## C2 architecture
TWINLOOT runs **two parallel channels** from the victim machine:
1. **SharePoint dead drop** — authenticates to an attacker-controlled Azure tenant and polls a SharePoint location via the Graph API (driven through headless Edge + CDP; the tab is navigated to `graph.microsoft[.]com` and the Drive API is used to interact with the actor's SharePoint).
2. **Teams TURN relay** — interactive operator access over WebRTC DataChannels relayed by Microsoft Teams TURN servers, using the `aiortc` library.

This is the same class of technique Praetorian codenamed **"Ghost Calls"** (TURN relay abuse). Ontinue notes multiple actors converged on it within a year of its public disclosure:
- **Backdoor.Turn** (previously documented) conceals C2 inside Teams relay infrastructure but uses a **QUIC session** rather than WebRTC DataChannels.
- **msaRAT** — a Rust-based RAT attributed to the **Chaos ransomware group**, observed using the same TURN method but against **Twilio instead of Teams**, implemented on the Tokio async runtime controlling a headless browser; its DLL (`lib.dll`) is delivered via an MSI installer and performs C2 exclusively through CDP, offloading HTTP to the browser and signaling via Cloudflare Workers.

Ontinue flags the convergence: two unrelated actors independently arrived at "drive the victim's own browser as a C2 transport" within the same month.

## Capabilities
- Harvest **Windows credentials using pixel-perfect fake lock screens**.
- **Reverse SOCKS5 pivot** into victim networks (an integrated SOCKS5 multiplexer).
- **Arbitrary command execution**.
- Reconnaissance, discovery, and **screenshot capture**.
- **EtherHiding-style fallback** to obtain runtime configuration if the Azure Blob Storage dead-drop method fails (unused in the observed build, suggesting active development).

## Persistence
Persistence is build-flagged (`PERSIST_ENABLED=True|False`) and uses four methods. The most novel is an **offline-built mandatory Windows profile hive**: the implant builds a full Windows profile hive entirely offline using `RegLoadAppKeyW` and Microsoft's offline registry library `offreg.dll` (`ORCreateKey`, `ORSetValue`, `ORSaveHive`), then writes the result to `%USERPROFILE%\NTUSER.MAN`. Because Windows loads `NTUSER.MAN` (mandatory profile override) **before** `NTUSER.DAT`, its contents take precedence — a method Ontinue says is the **first recorded malicious in-the-wild use** of this persistence technique.

## Attribution and assessment limits
- **Not attributed to a named actor.** Ontinue says it shares operational parallels with the cluster **STAC4749** (known for orchestrating Teams voice-phishing campaigns to deploy Chaos ransomware): Teams vishing delivery, PyArmor-obfuscated Python backdoor, reverse SOCKS5 proxy, HKCU Run-Key persistence, and an adjacent timeline.
- However, the **underlying implementation differs substantially**: STAC4749 uses PyInstaller packaging, Go-based implants, standalone SOCKS5 tooling, and `.top` domains behind Cloudflare, whereas TWINLOOT uses raw `.pyc` execution, pure Python, an integrated SOCKS5 multiplexer, and drop-caught aged domains with SharePoint dead-drop C2. Ontinue notes that "if these are the same operator, the tooling was rebuilt from scratch rather than evolved."
- The observed build's EtherHiding fallback is unused, indicating the framework is still being developed.

## Defender priorities
1. **Hunt for the Teams initial-access vector**: unsolicited "IT support" Teams messages that ask a user to run a PowerShell one-liner downloading a ~39 MB `.pyc`/archive.
2. **Detect headless-browser C2 transport**: an Edge/Chrome process launched headless with its remote-debugging interface enabled and CDP connections, especially one navigating to `graph.microsoft[.]com` and issuing Drive API calls out of band.
3. **Track the TURN/WebRTC relay abuse class ("Ghost Calls")**: WebRTC DataChannel sessions relayed through Teams/Twilio TURN for interactive operator access; also watch for Backdoor.Turn (QUIC) and msaRAT (Twilio + Cloudflare Workers + CDP) variants.
4. **Hunt the `NTUSER.MAN` mandatory-profile persistence**: presence of `%USERPROFILE%\NTUSER.MAN` on a system where it was not deliberately placed; offline `RegLoadAppKeyW` / `offreg.dll` usage is a strong tell.
5. **Watch for pixel-perfect fake lock screens** used to harvest Windows credentials, and reverse SOCKS5 pivot activity.
6. **Assess STAC4749 / Chaos overlap** when a campaign shows Teams vishing delivery plus a PyArmor Python backdoor, even if the tooling was rebuilt.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [PTC Windchill / FlexPLM CVE-2026-12569 exploitation](ptc-windchill-flexplm-cve-2026-12569-exploitation.md)
- [Microsoft Q2 2026 email and Teams phishing landscape](microsoft-q2-2026-email-teams-phishing-landscape.md)

## Sources
- The Hacker News: [TWINLOOT Abuses SharePoint and Teams to Steal Credentials and Move Across Networks](https://thehackernews.com/2026/08/twinloot-abuses-sharepoint-and-teams-to.html) — August 18, 2026, citing Ontinue technical report
- Praetorian "Ghost Calls" (TURN relay abuse technique, 2025)
- Cisco Talos: msaRAT / Chaos ransomware TURN-relay observations (late July 2026)
