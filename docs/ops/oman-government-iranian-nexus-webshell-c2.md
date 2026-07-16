# Oman government Iranian-nexus webshell C2

## Summary
Hunt.io reported an exposed RouterHosting VPS that revealed an Iranian-nexus intrusion campaign against Omani government entities, centered on the Ministry of Justice and Legal Affairs (`mjla.gov[.]om`). The open directory exposed operator tooling, C2 code, session logs, and evidence of data theft.

The clearest value for defenders is not the victim data itself, which should not be replicated. It is the operational pattern: ASP.NET web shells under DotNetNuke paths, a Python / PowerShell C2 workflow, Chisel tunneling, SQL and identity-data collection, registry-hive theft, and a nearby infrastructure cluster using `dubai-#` hostnames.

Hunt.io places the activity in the broader Iranian state-nexus space because of targeting, regional history, and neighboring infrastructure, but it does **not** make a group-level attribution. It notes overlap with known MOIS-linked clusters such as APT34 / OilRig / Crambus and MuddyWater / Mango Sandstorm without tying the activity to either group.

## Tags
- ops
- operations
- espionage
- Iran-nexus
- Oman
- government
- web shell
- ASP.NET
- DotNetNuke
- Chisel
- PowerShell
- C2
- credential-theft
- data-exfiltration

## Why this matters
- Exposed operator infrastructure can reveal active intrusion sequencing before public victim notifications or formal actor names exist.
- The campaign combines commodity edge / web-app exploitation with targeted scripts against ministry portals and identity data stores.
- The web shell path and C2 behavior give defenders durable hunts without copying or redistributing exposed personal data.
- Hunt.io's attribution caveat is important: regional and tooling overlap are not enough to collapse the activity into APT34 or MuddyWater.

## Reported chain

### Exposed C2 and working directories
- Hunt.io observed `172.86.76[.]127`, a RouterHosting VPS in the UAE, with open-directory exposure on ports `8000` and `8002`.
- The port `8000` directory showed reconnaissance and initial access attempts against multiple Omani government targets.
- The port `8002` directory contained a more organized operator working environment with payloads, scripts, C2 code such as `c2_fixed.py` variants, and a README describing the server as `VPS C2 - 172.86.76[.]127`.
- The `/payloads` directory reportedly included Chisel components for encrypted tunneling.
- The README included listener ports, reverse-shell templates, exfiltration commands, and SCP retrieval paths pointing to `/opt/c2/loot/`.

### Web shells and likely web-app entry points
- Hunt.io recovered an ASP.NET web shell named `hc2.aspx` and found every Ministry of Justice script hardcoding a second shell, `health_check_t.aspx`.
- `health_check_t.aspx` was referenced under `/Portals/0/`, DotNetNuke's default file-storage path.
- The shell command parameter was `c`; without a parameter, Hunt.io says the sample defaulted to host and identity discovery using `whoami /all`, `hostname`, and `ipconfig`.
- Hunt.io found additional scripts targeting CVE-2025-32372, an SSRF flaw in DotNetNuke versions before 9.13.8, and treats that as a possible initial-access path rather than confirmed entry.
- The broader scripts directory contained more than 50 Python scripts covering WAF bypass, Fortinet appliances, Joomla, MSSQL brute forcing, Oracle APEX / ORDS, Spring Boot Actuator endpoints, and national-ID IDOR testing.

### Targeting scope
Hunt.io says filename prefixes in the exposed directory mapped to 12 Omani government entities:

- Ministry of Justice and Legal Affairs: web shell access, database extraction, credential access.
- Royal Oman Police: PKI probing and portal reconnaissance.
- Royal Fleet of Oman: ProxyShell exploitation.
- Tax Authority of Oman: ProxyShell exploitation.
- State Audit Institution: credential brute forcing.
- Royal Court Affairs: Citrix exploitation, authentication reconnaissance, and MOF-based execution.
- Authority for Public Services Regulation: Oracle APEX / ORDS attacks.
- Civil Aviation Authority: portal enumeration.
- Information Technology Authority: admin-panel attack and national-ID IDOR testing.
- Ministry of Finance: Spring Boot Actuator exposure.
- Ministry of Transport, Communications and IT: portal enumeration.
- Office of Public Prosecution: SQL injection, database extraction, and portal attacks.

Hunt.io also notes earlier port `8000` artifacts for Royal Oman Police eVisa brute forcing, Royal Fleet of Oman and Tax Authority Exchange ProxyShell exploitation, and State Audit Institution training-platform brute forcing.

### Credential access, data collection, and lateral movement
- After web shell access, Hunt.io says the operator extracted database schema details and user tables through PowerShell and staged output under the C2 `loot/` path.
- The operator queried DotNetNuke `aspnet_Membership` data for superuser credentials and attempted offline hash cracking.
- Separate queries targeted an `eGov_Person` table for national ID, name, birthdate, and nationality fields. These victim records are not reproduced here.
- Hunt.io reports more than 26,000 Ministry of Justice user records, judicial data, committee decisions, and both SAM and SYSTEM registry hives were extracted.
- A script named `gp_v6_exec.py` used GodPotato through SQL Server `xp_cmdshell`; a later variant moved toward reflective in-memory payload loading after an earlier approach was flagged.

### C2 and persistence attempts
- Hunt.io describes a Python HTTP server and PowerShell beacon model.
- The beacon polled `/cmd` every 30 seconds, returned output through `/result`, and chunked base64-encoded results into 1,500-character segments.
- Session logs showed April 10, 2026 operator activity moving from host profiling to network enumeration, database mapping, data extraction, and registry-hive collection.
- C2 ports and functions reported by Hunt.io included:
  - `443`, `4443`, `4444`: reverse-shell listeners.
  - `7777`: Chisel host.
  - `8000`: HTTP file and exfiltration server.
  - `8001`: C2 beacon listener.
  - `8002`: open-directory port.
  - `9002`: registry-hive exfiltration.
  - `9003`: reverse SOCKS5 listener.
- The operator attempted scheduled-task persistence named `MicrosoftEdgeUpdate`; Hunt.io says Defender blocked it and the operator did not retry in the observed logs.
- Hunt.io also found a separate script attempting to forcefully disable antivirus.

## Defender heuristics
- Search ASP.NET / IIS estates for unexpected `.aspx` web shells, especially `hc2.aspx`, `health_check_t.aspx`, and files under DotNetNuke `/Portals/0/` upload paths.
- Review DotNetNuke deployments for CVE-2025-32372 exposure and unexpected server-side requests or file writes before version 9.13.8.
- Hunt for web-server child processes launching `cmd.exe`, `powershell.exe`, `sqlcmd`, `reg.exe`, `schtasks.exe`, or tunneling tools.
- Alert on `xp_cmdshell` execution chains that fetch or run GodPotato-like privilege-escalation payloads.
- Monitor for scheduled-task creation attempts named `MicrosoftEdgeUpdate` from web-server, SQL Server, or PowerShell parent processes.
- Investigate Chisel, reverse SOCKS, or unusual listeners around ports `7777`, `9002`, and `9003` in environments where those services are not expected.
- Treat exposed operator directories as evidence: preserve HTTP access logs, directory listings, payload hashes, and timestamps before takedown or blocking when incident-response obligations allow.
- If victim records or credential dumps are discovered in open infrastructure, minimize handling, avoid redistribution, and coordinate with affected organizations or appropriate national CERT channels.

## Reported indicators

Network infrastructure called out by Hunt.io:

- C2 / exposed VPS: `172.86.76[.]127`
- Resolving domain: `dubai-10.vaermb[.]com`
- Adjacent RouterHosting / UAE cluster:
  - `172.86.76[.]101` / `dubai-1.vaermb[.]com` / `regorixa[.]com`
  - `172.86.76[.]94` / `dubai-2.vaermb[.]com`
  - `172.86.76[.]108` / `dubai-3.vaermb[.]com` / `myjitsi.exceptionnotfound[.]ir`
  - `172.86.76[.]112` / `dubai-4.vaermb[.]com` / `s5.sideliner[.]ir`
  - `172.86.76[.]120` / `dubai-5.vaermb[.]com`
  - `172.86.76[.]121` / `dubai-6.vaermb[.]com`
  - `172.86.76[.]124` / `dubai-7.vaermb[.]com` / `suanefllix[.]com` / `brnettlix[.]com` / `brttfrixx[.]com` / `realprimefix[.]com` / `identificara[.]com`
  - `172.86.76[.]129` / `dubai-8.vaermb[.]com`
  - `172.86.76[.]130` / `dubai-9.vaermb[.]com`
- Additional RouterHosting / Switzerland infrastructure:
  - `45.59.114[.]60` / `shop.exceptionnotfound[.]ir` / `price.exceptionnotfound[.]ir` / `myjitsi.mrnajafipour[.]ir`
- Cloudflare-hosted domain in the surrounding cluster:
  - `104.21.27[.]95`, `172.67.142[.]35` / `tools.exceptionnotfound[.]ir`
- TLS certificate SHA-256 reported for the Switzerland-hosted cluster: `ECC3611F7DCBAA53ACF44E67DE2F10D78A26E03B3C77BA28BBD3EE16B2E66437`

File / path / task markers:

- `hc2.aspx`
- `health_check_t.aspx`
- `/Portals/0/`
- `c2_fixed.py`
- `c2_fixed_v2.py`
- `/opt/c2/loot/`
- `gp_v6_exec.py`
- Scheduled task name: `MicrosoftEdgeUpdate`

## Related pages
- [Seedworm / MuddyWater](../actors/seedworm-muddywater.md)
- [Ababil of Minab MOIS-linked recovery-destruction campaign](ababil-of-minab-mois-recovery-destruction.md)
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)

## Sources
- Hunt.io: [https://hunt.io/blog/iranian-nexus-oman-government-intrusion](https://hunt.io/blog/iranian-nexus-oman-government-intrusion)
