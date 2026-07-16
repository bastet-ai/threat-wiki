# ClickFix CPaaS API-driven payload delivery

## Summary
Bert-Jan Pals published research on June 30, 2026 analyzing roughly **3,000 live ClickFix payloads** and multiple ClickFix platforms. The key durable finding: ClickFix is no longer just a static fake-CAPTCHA clipboard trick. Some operators now run **ClickFix payload-as-a-service (CPaaS)** backends that return dynamically generated, uniquely obfuscated PowerShell payloads through API endpoints, localize the lure flow, and adapt execution paths as defenders block older Windows Run-dialog patterns.

The Hacker News amplified the research on July 1, 2026. Treat this as a pattern update for social-engineering-led initial access, compromised-site poisoning, and endpoint detection engineering rather than a single actor attribution.

## Tags
- ops
- operations
- ClickFix
- CPaaS
- payload-as-a-service
- social engineering
- fake CAPTCHA
- clipboard injection
- user execution
- T1204.004
- PowerShell
- Windows Terminal
- Windows Run dialog
- LOLBins
- AMSI bypass
- compromised WordPress
- malware delivery
- API-driven payloads
- dynamic obfuscation
- detection engineering

## Why this matters
- ClickFix operators can separate the visible lure from payload generation, giving defenders fewer static strings to match and making collection-time payloads differ from victim-time payloads.
- Pals observed 100 requested payloads from one CPaaS platform returning 100 unique obfuscated variants while deobfuscating to the same malicious logic.
- The Windows execution model is shifting from classic `Win+R` / Run dialog instructions toward `Win+X` / Windows Terminal flows that can look more legitimate and avoid RunMRU artifacts.
- A newer observed delivery method places a benign-looking orchestrator string in the clipboard and points it at a downloaded archive/script in the user's Downloads folder, reducing direct malicious content in the clipboard and bypassing some AMSI-oriented checks.
- Compromised WordPress sites remain a common delivery layer, so website-exposure management and endpoint telemetry both matter.

## Operational characteristics
- **Technique:** ClickFix maps to MITRE ATT&CK `T1204.004` — User Execution: Malicious Copy and Paste. Victims are instructed to prove they are human, fix an error, or complete a fake verification by pasting a command the page silently wrote to the clipboard.
- **Delivery paths:** Pals described targeted email-driven ClickFix infrastructure and broader browsing-based infections, often through compromised WordPress sites or vulnerable plugins that inject fake CAPTCHA overlays.
- **Localization:** reviewed ClickFix JavaScript supported visitor-language delivery across 25 languages.
- **Execution flows:** older pages guide victims through `Win+R`; newer flows guide victims through `Win+X`, selecting Terminal, and letting PowerShell execute inside Windows Terminal.
- **CPaaS backend:** observed JavaScript loaders called API endpoints such as `/api/index.php?a=init`, included source-host context, used tokens/access control, returned payload fields, and logged request metadata.
- **Dynamic obfuscation:** one CPaaS sample generated distinct payloads using Base64, AES, TripleDES, Rijndael, and Deflate-style obfuscation; deobfuscation produced equivalent malicious code.
- **Stage 2 LOLBins:** Pals' hunting logic covered PowerShell, `cmd`, `msiexec`, `curl`, `wget`, `rundll32`, `regsvr32`, `wscript`, `cscript`, `schtasks`, `bitsadmin`, `mshta`, `certutil`, `wmic`, `net`, `ssh`, and `SyncAppvPublishingServer.vbs`.
- **Downloads-folder bypass pattern:** a newer chain downloaded `tmp.zip`, copied it from `Downloads` to `%TMP%`, extracted it with `tar`, and launched `tmp.ps1` through headless `conhost` + PowerShell. The clipboard text mostly orchestrated local file movement and execution rather than carrying the complete malicious script.
- **No single-family attribution:** the research describes platform tradecraft across live ClickFix campaigns, not one named malware family or one confirmed actor.

## Indicators and pivots
Pals listed multiple payload API server domains. A connection to these domains indicates likely clipboard payload delivery, not guaranteed second-stage execution.

- `comicstar[.]lat`
- `babybon[.]cfd`
- `merkantalolol[.]asia`

Additional defensive pivots:
- Browser or proxy telemetry showing fake-CAPTCHA pages that call `/api/index.php?a=init` or similar payload-init endpoints.
- `explorer.exe` spawning `cmd.exe`, `powershell.exe`, or other LOLBins shortly after browser activity on a verification page.
- `WindowsTerminal.exe` spawning PowerShell immediately after suspicious browser/CAPTCHA interaction.
- Clipboard writes from browser processes followed by Run-dialog, Terminal, or PowerShell execution.
- `powershell -C` commands moving archives from `$HOME\Downloads` into `$env:TMP`, extracting with `tar -xf`, and executing `tmp.ps1`.
- Headless `conhost` launching PowerShell from temporary directories.
- Unusual use of `SyncAppvPublishingServer.vbs`, `mshta`, `bitsadmin`, `certutil`, `regsvr32`, or `rundll32` in user-session execution chains.

## Defender heuristics
- Instrument for the full human-mediated chain: browser page visit → clipboard write → Run dialog or Windows Terminal → LOLBin/network activity.
- Baseline and alert on `WindowsTerminal.exe` → `powershell.exe` launches that occur immediately after suspicious browser interaction, especially when accompanied by clipboard or Downloads-folder activity.
- Monitor Downloads-to-TEMP archive movement and immediate script execution; these chains may evade controls that only inspect the clipboard for obviously malicious PowerShell.
- For web defenders, hunt compromised CMS/WordPress pages for injected CAPTCHA overlays, API-backed payload fetchers, and localized ClickFix JavaScript.
- For SOC playbooks, treat ClickFix as an initial-access family of techniques: collect browser history, clipboard-adjacent telemetry if available, command-line history, RunMRU where present, Terminal process trees, downloaded archives, temporary scripts, and outbound connections to payload APIs.
- Update user training to explicitly warn that legitimate CAPTCHA or verification flows never require pasting commands into Run, Terminal, PowerShell, or shell prompts.
- Do not rely on one payload sample as representative of the campaign; API-driven payload generation means the next request can produce different obfuscation with the same behavior.

## Related pages
- [Ghost CMS CVE-2026-26980 ClickFix poisoning](ghost-cms-cve-2026-26980-clickfix-poisoning.md)
- [Operation Endgame SocGholish disruption](operation-endgame-socgholish-disruption.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)

## Sources
- [Bert-Jan Pals](https://kqlquery.com/posts/clickfix-gift-that-keeps-on-giving/)
- [The Hacker News](https://thehackernews.com/2026/07/researcher-analyzes-3000-live-clickfix.html)
