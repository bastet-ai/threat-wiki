# TGR-STA-0049: PerfectPioneer and KUKURAT HTTP/3 espionage RATs (Unit 42)

## Tags
- ops
- cyberespionage
- TGR-STA-0049
- REF7707
- Earth Alux
- Ink Dragon
- PerfectPioneer
- KUKURAT
- Squidoor
- HTTP/3
- QUIC
- UDP 443
- RAT
- Go malware
- C++ malware
- DLL side-loading
- web shell
- Godzilla
- Suo5
- ASPXSpy
- isDangerousCommand
- heuristic camouflage
- LSASS dumping
- comsvcs.dll
- DCSync
- Exchange impersonation
- logon script persistence
- PsExec
- Unit 42
- Southeast Asia
- supply-chain-adjacent

## Summary

On November 16, 2026 (23:00:55Z) Unit 42 published **"QUIC and Covert: Novel HTTP/3-Powered RATs Target Southeast Asian Governments"** (Tom Fakterman): a multi-stage cyberespionage campaign against Southeast Asian government entities active since at least July 2025, tracked as **TGR-STA-0049** (also tracked as **REF7707**, **Earth Alux**, **Ink Dragon**), previously known for deploying **Squidoor** (AKA FINALDRAFT) since 2023. The new tradecraft has three durable, hunt-relevant capabilities, each rarely or never seen in the wild before:

1. **HTTP/3 (QUIC over UDP) as primary C2** in both families, with automatic HTTP/2 fallback. Because QUIC runs over UDP/443, TCP-optimized inspection stacks and passive TLS interception frequently do not see it at all; the report observes outbound UDP 443 bypassing DPI entirely on legacy policies.
2. **A built-in operator safety switch** — PerfectPioneer's `isDangerousCommand` routine refuses to execute hard-blocked, noisy/forensics-heavy Windows AND Linux commands from its own C2, so a careless operator cannot arm an alert. A malware family policing ITS operator is a new detection-resistance pattern.
3. **A heuristic camouflage engine** — KUKURAT fabricates benign-looking behavior to move the endpoint's behavioral baseline: 10 decoy HTTP requests per cycle against 15 hard-coded popular domains with random paths, Chrome-lookalike registry writes (`HKCU\Software\Google\Chrome\BrowserCrashRecovery` create-read-delete plus `Google\Update\ClientState` enumeration), and create/delete churn in `%temp%`. Each axis is togglable at runtime via the `set_obfuscation` C2 command.

**Defensive headline: your UDP visibility decides whether this campaign exists in your telemetry.** Block or inspect outbound UDP/443 (forcing the graceful HTTP/2 fallback into decryptable TCP), audit sysvol/GPO logon scripts, alert on `rundll32 comsvcs.dll` ordinal mini-dump (`#+000024`), and audit Exchange `ApplicationImpersonation` + mass `Add-MailboxPermission` loops.

This page is a public-source capture (Unit 42 article text fetched by this wiki at 2026-11-17T00:3xZ, HTTP 200); no payloads were executed or handled by this wiki. Kinship to other tracked actors is NOT asserted beyond the report's own aliases.

## Actor and timeline

| Fact | Value | Source |
|---|---|---|
| Tracker names | TGR-STA-0049 = REF7707 = Earth Alux = Ink Dragon | Unit 42 |
| Active since | at least March 2023 (Squidoor era); current campaign since July 2025 | Unit 42 |
| Targets | Government entities, Southeast Asia (campaign), also South America and Europe historically | Unit 42 |
| Prior tooling | Squidoor / FINALDRAFT backdoor (Windows + Linux) | Unit 42 |
| PerfectPioneer RAT | custom Go, six recovered variants, first spotted July 2025 | Unit 42 |
| KUKURAT | modular C++, two variants (HTTP/2 and HTTP/3), in the wild since March 2026 | Unit 42 |
| Publication | Nov 16, 2026 23:00:55Z, unit42.paloaltonetworks.com/custom-rats-target-southeast-asia-governments/ | this wiki fetch |
| Reported IOC domain (defanged in article) | `www.investigationj6[.]com` | Unit 42 |

The six PerfectPioneer variants are distinguished by recovered project paths (`D:/proj/http3/newhttp3/agent/`, `PerfectRat`, `RatAAkk-tt`, `rat_http3_ls`, `rat_http3_cc`, `Pioneer`); compilation timestamps were stripped or falsified, so the development chronology is reconstructed from feature sets, not metadata. URL endpoints `/agent/register`, `/agent/heartbeat`, `/agent/tasks`, `/agent/result` OVERLAP between PerfectPioneer and KUKURAT — the report's own artifact linking the two families to one development pipeline.

## Infection vectors

- **Server exploitation (primary):** unpatched Microsoft Exchange and web servers get web shells — custom plus public tooling: **ASPXSpy, Godzilla, Bysunue.aspx, Suo5**. PerfectPioneer is then executed from the web shell for recon.
- **DLL side-loading:** a legitimate, structurally modified executable carries XOR-encrypted shellcode internally; a companion malicious loader DLL reads, decrypts and executes it in memory.
- **Decoy installers:** a working setup wizard runs in the foreground while the RAT writes to disk and executes in the background; one specimen abused a legitimate **Palo Alto Networks GlobalProtect** installer as the visible cover.
- **Phishing:** executables with PDF icons on lookalike government domains; opening the "PDF" launches malware plus a decoy PDF (one observed decoy impersonated a 2025 Myanmar Union Election Commission notice).

## PerfectPioneer RAT (Go)

Native-compiled capability set (no modules): full file ops with chunked transfer + temp-file hygiene, shell execution, process list/kill/start, COM-based process creation, classic `VirtualAllocEx`/`WriteProcessMemory`/`CreateRemoteThread` injection, keylogging, SOCKS5 proxy, screenshots, window enumeration, resource monitoring.

Three self-maintenance routines define its footprint discipline:

- **Reconnection:** tracks an internal `connected` flag; on heartbeat/poll failure it cancels loops and forces clean re-registration.
- **Cleanup:** continuously deletes its temp files, and when RSS exceeds ~100 MB it forces Go GC to shrink the resident footprint.
- **Resource monitoring:** a performance snapshot every 30 s the operator can pull on demand.

**`isDangerousCommand` (variants `Pioneer` and `rat_http3_cc`):** every incoming C2 command is cross-referenced against a hard-coded blocklist of destructive/forensics-heavy commands (both Windows and Linux syntax, implying a parallel Linux build in the same source tree — Go cross-compile) and BLOCKED outright. Read defensively: this is an operational-security control the attacker wrote for itself, and its presence is itself a high-confidence hunting feature for this family.

## KUKURAT (C++, modular)

The static core contains NO post-exploitation code; ~12 named capability DLLs load dynamically from the C2 on demand: screenshots, keylogging, host/port scanning, process management + injection, file upload/download/list/delete/execute, `cmd.exe`/PowerShell execution, PsExec-style lateral movement, SMB credential brute-force, SOCKS tunneling, local privilege elevation, Beacon Object File execution, silent-mode config.

Registration posts hostname, username+integrity, OS/arch, host IP, and a runtime-random agent ID; the C2 returns a JSON runtime config including the camouflage toggles (`obfuscation.network/registry/file`, default off) and tuned timeouts (heartbeat 300 s, 5 command worker threads, module exec 600 s).

Two variants (HTTP/2 vs HTTP/3) differ in exactly the ways an active developer adapts: the HTTP/2 build handles commands in one nested if-else chain; the HTTP/3 build refactors to a function-pointer table AND adds a built-in native `exec` command (`CreateProcessA`, output piped to C2) as a survival option that needs no module fetch.

**Watchdog persistence:** the agent writes its path to named pipe `WINDOW_SEC_WATCHDOG` every 3 s; a companion watchdog relaunches it after 15 s of silence. One deployment hid the watchdog in `C:\ProgramData\Cyvera\Ransomware\` — the historical Cortex XDR directory name, hiding in a security product's own footprint.

**Recovered module:** `PsExecService.exe` (PDB path `d:\proj\KUKURAT\modules\MyPsExec-master\PsExecService\`, plausibly derived from open-source MyPsExec) registers a Windows service `PsExec` + named pipe `\\.\pipe\PSEXEC`, supports shell/upload/download/dirls, and self-uninstalls after 5 minutes idle.

## Network tradecraft (the durable hunt surface)

- Both families prefer **HTTP/3/QUIC over UDP/443**, auto-falling back to **HTTP/2 over TCP**. The fallback is the defender's lever: **block outbound UDP 443 (or DPI-inspect it) and the campaign degrades into traffic your existing TLS inspection can read.**
- Camouflage noise is designed to defeat behavioral baselining, not signatures: per-cycle decoy requests to 15 popular domains, Chrome-crash-recovery registry mimicry, `%temp%` churn. Host EDR rules keyed on "process writes registry/file" will drown; rules keyed on the SPECIFIC sequences (BrowserCrashRecovery create-read-delete cycles without Chrome as the writer, temp churn loops from unsigned non-browser binaries) survive.

## Post-exploitation and objectives

- **Domain-wide propagation via malicious domain logon scripts** after DC compromise (plus PsExec/WMI/WinRM): every authenticating user's endpoint downloads and executes KUKURAT. Alert on startup processes running under domain-user SIDs at logon (the report shows this exact alert firing).
- **Credential theft:** LSASS dump via `rundll32.exe C:\windows\System32\comsvcs.dll, #+000024 <lsass_pid> <out> full` — the MiniDump export invoked by its ORDINAL to dodge string-based detection; plus Mimikatz, ProcDump, SharpDPAPI, and manual SAM/SYSTEM hive dumps.
- **DCSync** against the DC for domain hashes.
- **Mailbox takeover:** enumerate `ApplicationImpersonation` role holders via Exchange Management Shell; failing that, loop `Get-Mailbox -ResultSize Unlimited | Add-MailboxPermission -AccessRights FullAccess -AutoMapping:$False` to grant one owned account everything.
- **Exfiltration:** mass collection of `.pdf/.docx/.xlsx/.png` whose filenames signal international-relations and internal-political content = the intelligence objective behind all the stealth.

## Hunt and hardening checklist

- **Edge:** log/inspect or block outbound UDP/443; QUIC blocked forces the HTTP/2 fallback into TCP visibility. Inventory which egress paths allow UDP 443 uninspected TODAY.
- **AD:** continuously audit sysvol + GPO for logon-script changes (diff on a schedule, don't trust absence); alert on processes spawned at authentication with domain-user SIDs.
- **EDR:** behavioral rule for `rundll32.exe` + `comsvcs.dll` with numeric export (`#+000024`-class) arguments; rules for `BrowserCrashRecovery` write-read-delete cycles from non-Chrome binaries; named-pipe sightings `WINDOW_SEC_WATCHDOG` and `\\.\pipe\PSEXEC`; service named `PsExec` with 5-minute self-delete.
- **Exchange:** scheduled audit of `ApplicationImpersonation` assignments; alert on scripted `Add-MailboxPermission` loops; web-shell detection on Exchange front ends (ASPXSpy/Godzilla/Bysunue.aspx/Suo5 family).
- **Fidelity note:** payload analysis, IOCs (defanged domain above included), and per-variant command tables are the Unit 42 article's; this wiki captured the write-up and asserts nothing beyond it. No attribution beyond the report's aliases is claimed.

## Monitor forward

- KEV watch: nothing in this campaign is KEV-listed as of read (KEV held `2026.11.13`/`1,781`, `2026-11-17T00:3xZ` grep of this family's CVEs N/A — exploitation-in-the-wild for the Exchange vector is described but no CVE was named in the article).
- Watch for follow-on reporting that names C2 IPs/URLs beyond `www.investigationj6[.]com`; blocklists here age by the week, the TTP table above is the durable asset.
- Re-read if Squidoor/FINALDRAFT tooling under TGR-STA-0049 intersects any on-wiki npm/PyPI supply-chain cluster (no intersection observed at capture; kinship NOT asserted).
