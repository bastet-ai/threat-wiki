# Shattering the Dream: Lazarus "Operation Dream Job" job-offer zero-day campaign

## Summary
Check Point Research published "Shattering the Dream – When a Job Offer Becomes a Zero-Day Attack" on August 11, 2026, documenting a wave of the **Lazarus "Operation Dream Job"** campaign active since early 2026. The operation targets the **defense, aerospace, and aviation sectors** (Europe and India emphasized), luring victims with fake recruiter job offers at well-known companies. Two infection chains run in parallel: a **DLL-sideloading chain** (signed PDF viewer + malicious `libmupdf.dll` + encrypted PDF payload) and a newer **trojanized-PDF-viewer chain** (a modified MuPDF-based viewer, "SecurityPDF," that executes payloads from specially crafted PDFs). Both chains converge on the in-memory downloader **MISTPEN**, a new version of Lazarus' kernel-mode rootkit **FudModule** deployed through a new AFD.sys zero-day (**CVE-2026-68820**), the **ForestTiger** backdoor, and a new PHP C2-relay webshell, **RelayShell**, hosted on compromised Roundcube and WordPress servers. Check Point also reports the campaign used **CVE-2025-49113** (Roundcube RCE) to plant RelayShell on webmail servers, and that at least one compromised Western European organization was leveraged as a spear-phishing relay.

This page is the exploitation-context record for **CVE-2026-68820**, the exploited zero-day otherwise tracked on the [CISA KEV August 11 page](cisa-kev-winssock-zero-day-metabase-cisco-august-11-2026.md).

## Tags
- ops
- operations
- Lazarus
- Operation Dream Job
- Shattering the Dream
- FudModule
- MISTPEN
- ForestTiger
- RelayShell
- SecurityPDF
- libmupdf.dll
- Troy
- DLL sideloading
- trojanized PDF viewer
- CVE-2026-68820
- CVE-2025-49113
- AFD.sys
- kernel rootkit
- EDR evasion
- Microsoft Graph
- OneDrive C2
- Roundcube
- SEO poisoning
- spear phishing
- job-offer phishing
- defense sector
- Check Point Research

## Two infection chains
**Chain 1 — DLL sideloading (encrypted ZIP, three files).**
- Encrypted ZIP contains: a legitimate digitally signed PDF viewer executable, a malicious `libmupdf.dll`, and an encrypted payload with a PDF extension (decoy PDF impersonating a job description, e.g. Lockheed Martin-style offer).
- Running the executable loads `libmupdf.dll` via DLL sideloading; the DLL shows the decoy PDF and silently decrypts/executes an embedded in-memory payload: **MISTPEN**.
- MISTPEN sequence: reconnaissance modules → persistence module (installs on disk, survives reboot) → in-memory LPE module exploiting **CVE-2026-68820** in `afd.sys` → **FudModule** rootkit execution with SYSTEM (EDR visibility disabled) → **ForestTiger** backdoor for long-term access.

**Chain 2 — trojanized PDF viewer (SecurityPDF), observed from July 2026.**
- Fraudulent job offers impersonate **Enveil**, a privacy-enhancing-technology company; victims download an encrypted ZIP with two files: **SecurityPDF** and a malicious PDF.
- SecurityPDF is a modified open-source MuPDF-based viewer. Two code paths were patched by the attacker: `File → Open` and drag-and-drop. Any opened PDF containing the marker `This document is encrypted with sumatrapdf reader!!!!!!!!!!!!` triggers extraction of an embedded payload, single-byte XOR decryption (key `0x39`), write to `%TEMP%\new.exe`, and child-process launch.
- `new.exe` reflectively loads a DLL containing the **Troy** backdoor — a previously undocumented Lazarus backdoor first observed in this campaign.
- At least **three SEO-ranked impersonation websites** for Enveil distribute the viewer, some as the top search result for "Enveil SecurityPDF" — separating viewer delivery from PDF delivery and improving credibility/evading phishing detections. Check Point notes Enveil is impersonated, not compromised or targeted.

## MISTPEN
Lightweight in-memory downloader first documented by Mandiant in 2024. It communicates through **Microsoft Graph API** via attacker-controlled files on **OneDrive** (AES-encrypted transport, separate upload/download keys) and reflectively loads PE DLLs into memory without touching disk. Observed in-memory modules:
- **GetInfoPlugin** (`Release_GetInfoPlugin_x64.dll`) — host recon: domain/workgroup, computer name, user, OS build.
- **PvPlugin** (`Release_PvPlugin_x64.dll`) — extended recon with a full process table (PID, PPID, creation time, user/domain, name).
- **OneScreenCapture** (`OneScreenCapture64.dll`) — full-desktop screenshots (all monitors) via USER32/GDI, JPEG + Base64.
- **LPE loader** — a 64-bit DLL loader for the LPE exploit module; relays through a shared RPC buffer to MISTPEN's Graph/OneDrive channel, with GOST-CBC + per-message session key + Base64 encoding on top of the AES transport.

## FudModule (new version, deployed via CVE-2026-68820)
- FudModule is a Lazarus privilege-escalation tool used since ~2021; the 2024 variant exploited **CVE-2024-38193**, another `afd.sys` use-after-free.
- The new version targets a distinct, previously undocumented `afd.sys` use-after-free — **CVE-2026-68820** — assigned by Microsoft after responsible disclosure and patched in the August 11, 2026 Patch Tuesday. Check Point confirmed active in-the-wild use.
- The sample enforces a minimum of **Windows 11 build 26100 (24H2)** with explicit support for build **26200 (25H2)**; testing on a fully patched Windows 11 system confirmed it targets a vulnerability separate from CVE-2025-60719 (an earlier AFD.sys UAF fixed in November 2025, not linked to an actor).
- Post-exploitation strings such as "enable_god_mode passed" and a main function matching prior FudModule builds support the attribution; FudModule is a kernel-mode rootkit used to obtain SYSTEM and disable EDR visibility.

## RelayShell (new PHP C2-relay webshell)
RelayShell is a previously undocumented PHP web shell, deployed on compromised **Roundcube** and **WordPress/PrestaShop** servers, that repurposes the servers as C2 relay nodes. Unlike a command-execution web shell, it is a communication relay with two modes selected by the password in the HTTP POST:
- **Victim mode** — creates a PHP session for the infected endpoint, decrypts a hidden configuration (custom substitution cipher, external file) containing a backbone URL and a unique PID, and announces the new session to the backbone (an upstream RelayShell instance).
- **Operator mode** — session auth/selection over `.ses` files, connectivity check/cleanup, log retrieval, file upload (Base64 filename + content), and self-delete/file removal.
- File-based channel: `send`/`receive` commands exchange data through `<session_id><object>.log` temporary files (object `1` = victim, `2` = operator).
- Check Point assesses the actor harvested compromised-organization credentials (e.g. via MISTPEN collection) to authenticate to target Roundcube instances, then exploited **CVE-2025-49113** (post-authentication Roundcube RCE) to deploy RelayShell. The same web shell was also observed on compromised **PrestaShop** sites.

## Amplification and attribution notes
- **Reputation abuse:** in at least one case a compromised Western European organization was leveraged to conduct a spear-phishing campaign, extending reach by borrowing the victim's reputation and trust.
- **Attribution:** Check Point attributes the wave to **Lazarus** (ForestTiger, FudModule, MISTPEN lineage, and the previously documented 2025 ESET-documented Dream Job campaign). No new actor label was introduced.
- **CVE linkage:** CVE-2026-68820 is the same flaw CISA added to KEV on August 11, 2026; this campaign is the confirmed exploitation context. The Roundcube vector (CVE-2025-49113) is otherwise tracked on the [UNK Masstraction university-mailserver campaign page](unk-masstraction-roundcube-university-mailserver-campaign.md).

## Defender priorities
1. **Patch CVE-2026-68820 immediately** on Windows 11 24H2/25H2 (and confirm across the fleet) — it is a confirmed in-the-wild LPE to SYSTEM with EDR-visibility impact, and the BOD 26-04 outer bound is 2026-08-25.
2. **Hunt the MISTPEN channel:** Microsoft Graph / OneDrive file-based C2 from endpoint processes — unexplained OneDrive file creates/reads by user-mode processes, Graph API traffic from non-browser processes.
3. **Webmail exposure:** audit internet-facing Roundcube/PrestaShop/WordPress for the RelayShell web shell and patch **CVE-2025-49113**; treat an unexplained PHP relay pattern (per-session `.ses` files, `*.log` exchange files, external substitution-cipher config) as a C2 relay, not a classic backdoor.
4. **Phishing-lure coverage:** extend email/link policy review to job-offer/LinkedIn-adjacent lures and to third-party "vendor" download sites that rank in search results (SEO-poisoned impersonation domains distributing trojanized PDF viewers); watch for the `This document is encrypted with sumatrapdf reader!!!!!!!!!!!!` PDF marker and `%TEMP%\new.exe` creation.
5. **EDR-visibility check:** after any suspected FudModule deployment, validate kernel-driver and sensor integrity (rootkit-class EDR degradation); a host that "looks clean" after this chain may not be.

## Related pages
- [CISA KEV August 11 additions: Windows WinSock zero-day, Metabase, and Cisco ASA/FTD](cisa-kev-winssock-zero-day-metabase-cisco-august-11-2026.md)
- [UNK Masstraction Roundcube university-mailserver campaign](unk-masstraction-roundcube-university-mailserver-campaign.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)

## Sources
- Check Point Research: [Shattering the Dream – When a Job Offer Becomes a Zero-Day Attack](https://research.checkpoint.com/2026/shattering-the-dream-when-a-job-offer-becomes-a-zero-day-attack/) — published 2026-08-11
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (CVE-2026-68820, added 2026-08-11)
- Microsoft: [August 2026 Patch Tuesday](https://msrc.microsoft.com/update-guide/releaseNote/2026-Aug) (CVE-2026-68820 fix)
- CVE record: [CVE-2025-49113](https://www.cve.org/CVERecord?id=CVE-2025-49113) (Roundcube RCE used as the RelayShell delivery vector)
