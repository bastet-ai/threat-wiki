# Malicious Google Doc sidebar (Apps Script) funnels victims to AMOS on macOS and a three-stolen-cert Windows chain that installs a rogue Google Trust Services CA, NetSupport Manager, and a Ledger wallet implant (Huntress, Sep 15, 2026)

## Tags
- ops
- operations
- Google Docs
- Google Apps Script
- ClickFix
- AMOS
- Atomic Stealer
- MacSync
- infostealer
- rogue certificate authority
- TLS interception
- local proxy
- certificate forgery
- VirusTotal impersonation
- ClickOnce
- code-signing certificate theft
- Lenovo certificate
- Discord certificate
- MsBuild hollowing
- NetSupport Manager
- rogue RMM
- Ledger wallet implant
- crypto wallet theft
- MetaMask
- Telegram C2
- web reconnaissance
- Russian-speaking indicator
- X DM lure
- social engineering
- Huntress
- MITRE ATT&CK

## Summary

Huntress SOC analysts (Tradecraft Tuesday, published September 15, 2026) documented a post-DEFCON X-DM campaign in which a threat actor posing as **CoinDesk's VP and Head of Marketing** (account `@HartmansDoeke`, using one person's name and another's photograph; scam-flagged posts against the account date back to October 2025 — a "volume play," not DEFCON-specific targeting) sent a **legitimate Google Doc with a malicious custom sidebar** built as a **Google Apps Script bound to the document**. Nothing needed to be downloaded for the sidebar to run: the script executed **client-side in the victim's browser, avoided an OAuth consent prompt**, collected the viewer's public IP, geolocation, browser, and whether **MetaMask/Ethereum, Phantom, Tron, or Solana** wallet extensions were installed, and reported each result to the actor **via the Telegram API** as coded beacons (`VIEW`, `MOBILE`, etc.). Opening the document while signed in — clicking nothing, downloading nothing — was enough to be profiled. The analysts push back on "broken English = scammer": imperfect English can be a deliberate rapport tactic in the AI-grammar era.

The sidebar displayed a fake "decryption failure" with per-OS "remediation" instructions — a **ClickFix lure** plus a "manual update" button — that delivered divergent payloads:

1. **macOS:** a piped-zsh ClickFix chain, or a DMG from the actor's own GitHub repository for the manual path — an **AMOS-family stealer** variant (browser data, crypto wallets, Telegram data, Apple Notes, cookies, login keychain) with Gatekeeper-bypass instructions and a password prompt; Huntress notes kill-chain similarity to the six-stage **MacSync** stealer they covered the prior month. A second lure (DropBox DocSend doc) routed Mac users to the same AMOS payload on another host.
2. **Windows:** the manual path launched an app deployed via **ClickOnce**, signed with a certificate belonging to a small **Norwegian company** (stolen or fraudulently issued) — the first of **three abused code-signing certificates** in the chain; a fake "Google API Connector" update and a fake installation progress bar provided distraction. The ClickFix path ran an encoded PowerShell command fetching a loader with three encrypted payloads — all three already on VirusTotal before Huntress looked, so the kit had run before. Mobile visitors got only a `MOBILE` beacon — the actor saw no value in serving a phone a payload.

The clincher artifact: when a later DocSend sample's endpoint (`web12api[.]com`) returned 404, the analysts reconstructed the registration protocol from the sample's own `@sentry/electron` module and replayed it against a live sibling (`SignNow`), recovering ~5.5 KB of unobfuscated JavaScript, a session token, an archive password, and three payload URLs. The stage-three archives (fetched password-protected from `eu03hub[.]com/get_file`, password included in the C2 response) were:

- **NetSupport Manager 14.10.0004** — legitimate RMM redirected to hostile infrastructure with chat/messaging/connect/disconnect alerts disabled; carries persistence for all three modules (keyboard filter driver, Windows service, Run key, scheduled task self-reinstall). One of its IPs also hosted freshly registered **GTA6Mainserver[.]com / GTA6Mainweb[.]com** (a Grand Theft Auto VI pirated-copy lure on the same host).
- **A rogue certificate authority** — disguised as a Lenovo driver package, signed with a **genuine stolen Lenovo certificate** (third cert), it **hollowed `MsBuild.exe`** (import table reduced to kernel32) and built "purpose-built and working public key infrastructure on your machine": a **self-signed CA in the system root store presenting as Google Trust Services `CN=WR3`**, plus a **forged `www.virustotal.com` leaf certificate** (SAN covers the legitimate domain and localhost), a **hosts-file entry**, and a **"LocalProxy" firewall rule** — producing a locally-answered HTTPS connection that validates. The operator can then **block, read, or fabricate VirusTotal lookups** without certificate warnings (and by extension could MITM crypto domains or AV update signals). The CA is **regenerated per host**, so thumbprint blocklisting is useless; the CA, hosts entry, and firewall rule **persist after reboot** even though the injecting process dies.
- **A Ledger wallet implant** — same crypter/Lenovo-disguise/MsBuild-hollowing technique; creates a Run key named `Ledger Wallet Installer`, searches for Ledger Live / Ledger Wallet installs, hides its bot ID as sixteen hex characters in an `app.crc32` file inside a real application's data folder, and polls the actor's server for commands (observed polling 18 times with empty responses — the channel worked; the operator simply wasn't tasking the host). Ironically its persistence was broken: the Run key pointed at a bare `msbuild` invocation with no arguments, which exits immediately.

Russian-language comments appear throughout the source code and C2 PCAPs — **supporting, not proving, a Russian-speaking operator**; Huntress explicitly declines group attribution ("it could just be a guy in his house using AI to deploy malware"). The campaign's financial/crypto-theft intent is clear from the wallet-extension probing and the Ledger implant. Final twist: when the DM gambit failed, the actor offered the researcher up to **one million dollars** in project funding — "salesman hears no, salesman changes the pitch."

## Why this matters
- **A shared Google Doc is executable content.** A container-bound Apps Script runs in the viewer's browser, can report the viewer's real IP and environment, and can skip the OAuth consent prompt. "Open unknown documents while signed out" removes the Apps Script collection layer at zero cost.
- **The rogue CA is the artifact most likely to survive cleanup.** Killing the process does not remove the root-store CA, the hosts entry, or the firewall rule; only clinical removal or reimaging does. Huntress's own SOC analysts say a rogue CA in the trusted store is not the first thing a triager thinks to check.
- **Per-host CA regeneration defeats thumbprint blocklisting** — hunt the *structure* (new root-CA install events, hosts-file writes, new firewall rules named LocalProxy, `msbuild.exe` with a stripped import table) rather than certificate hashes.
- **Three stolen/forged code-signing certificates in one chain** (Norwegian company, Discord Inc. — signature did not validate, Lenovo — genuine) reinforce that signature presence is not a trust signal.
- **Legitimate-services abuse continues across the chain**: Google Docs as delivery + recon, Dropbox DocSend as a second lure (real marketing carousel as distraction), NetSupport Manager as RMM, Sentry's own SDK used to reconstruct the actor's protocol.
- Distract-and-quiet-fail design: three try/catch blocks with silent returns mean server death, host rejection, and full compromise all render the same empty screen.

## Indicators (as published by Huntress)
| Type | Indicator |
|---|---|
| X account | `@HartmansDoeke` (CoinDesk VP/Head-of-Marketing persona) |
| Payload infra | `web12api[.]com` (+ `SignNow` sibling), `eu03hub[.]com/get_file` |
| Post-compromise lure domains | `GTA6Mainserver[.]com`, `GTA6Mainweb[.]com` |
| Rogue CA | self-signed root in system store, `CN=WR3` (Google Trust Services masquerade) |
| Forged leaf | `www.virustotal.com` (+ localhost) SAN |
| Persistence | Run key `Ledger Wallet Installer` → bare `msbuild`; bot ID as 16 hex chars in `app.crc32` inside a real app's data folder; NetSupport Manager service/filter driver/scheduled task; hosts entry + `LocalProxy` firewall rule |
| Test-traffic note | published Telegram beacon screenshots use documentation range 203.0.113.x (Huntress test traffic) |

## MITRE ATT&CK (selected)
- T1566 / T1655 — phishing via social-media DM and shared document
- T1059.005/.006/.07 — Visual Basic/PowerShell/JavaScript (Apps Script) execution
- T1204.002/.003 — user execution of ClickFix command / malicious file
- T1553.004 / T1588.003 — forged/stolen code-signing certificates
- T1557.001 + T1573 — local TLS-interception proxy via rogue root CA
- T1027.002/.011 — software packing / masquerading (MsBuild hollowing, Lenovo disguise)
- T1219 — NetSupport Manager rogue RMM
- T1112 / T1547.001 — registry Run-key persistence
- T1056.004 / T1005 — credential/clipboard-adjacent collection (AMOS stealer)

## Sources
- Huntress, "Google Doc Sidebar Sends Mac and Windows Users Down Different Paths to Malware" (Susannah Cromek, Ryan Dowd, Jonathan Semon; Tradecraft Tuesday), September 15, 2026 — <https://www.huntress.com/blog/google-doc-sidebar-malware-mac-windows>

## Related
- [Pattern: forging the operating system's own trust primitives](../patterns/forged-platform-trust-primitives-integrity-regeneration-september-2026.md) — this campaign is one of the three sightings behind the synthesis.
- [Talos ClickFix browser crypto-theft via Google Visualization API C2](talos-clickfix-browser-crypto-theft-google-visualization-api-c2-september-2026.md) — same "ClickFix moves into the browser" theme, different pipeline (Tampermonkey/Sheet C2 vs Apps Script sidebar).
- [macOS ClickFix fingerprinting-gate campaign](macos-clickfix-fingerprinting-gate-campaign.md) — the MacSync/AMOS downstream this campaign's macOS branch resembles.
