# Storm-2603 parallel SharePoint ransomware intrusion

## Summary
Microsoft Incident Response published Cyberattack Series No. 9 on June 22, 2026, describing a ransomware investigation where **Storm-2603** activity overlapped with a second, unrelated actor in the same environment. The case is durable because it shows how one intrusion can contain multiple simultaneous activity streams: internet-facing SharePoint exploitation and reconnaissance, legitimate remote-access tooling, BYOVD defense evasion, credential theft, DLL sideloading, and ransomware impact.

Track this as an operation page rather than a standalone actor profile for now. Microsoft names Storm-2603 for the ransomware activity, but the second activity stream remains unnamed in the public report.

## Tags
- ops
- operations
- Storm-2603
- ransomware
- SharePoint
- CVE-2025-49706
- CVE-2025-49704
- CVE-2025-11371
- local-file-inclusion
- Velociraptor
- Cloudflare Tunnel
- Zoho Assist
- Visual Studio Code Remote SSH
- BYOVD
- NSecKrnl.sys
- DLL sideloading
- NTDS.dit
- credential-theft
- parallel-intrusion
- incident-response

## Why this matters
- Microsoft DART found two unrelated threat actors operating **simultaneously**, not sequentially, which can make timeline reconstruction and attribution misleading if teams stop at the first explanation.
- Storm-2603 had been targeting on-premises SharePoint servers since mid-2025 with publicly disclosed vulnerabilities and additional local-file-inclusion reconnaissance.
- The actor blended legitimate administrative and response tooling into the intrusion: Velociraptor, Cloudflare tunneling, Zoho Assist, and VS Code Remote SSH.
- The second actor's DLL sideloading and custom backdoors complicated detection and attribution while the ransomware stream continued toward impact.
- The case reinforces a core IR rule: preserve and correlate endpoint, identity, network, and cloud telemetry before collapsing all artifacts into one actor narrative.

## Reported chain
### Storm-2603 activity
1. Microsoft reports Storm-2603 targeting on-premises SharePoint servers since mid-2025, including exploitation of CVE-2025-49706 and CVE-2025-49704.
2. In the reported case, initial access was likely attempted through CVE-2025-11371, which Microsoft describes in the report as an unauthenticated local-file-inclusion flaw. Requests for `win.ini` and `web.config` suggested LFI probing; exploitation was not confirmed in the blog summary.
3. The actor deployed **Velociraptor** with SYSTEM privileges to collect data and map the environment.
4. The actor established multiple remote access paths:
   - Cloudflare tunnel deployment.
   - Zoho Assist remote management through the Velociraptor agent.
   - Visual Studio Code Remote SSH tunnel to a command-and-control endpoint.
5. Persistence and escalation included new local and domain administrator accounts.
6. Defense evasion included loading the vulnerable driver `NSecKrnl.sys` to tamper with memory and disable endpoint protections.
7. Microsoft reports lateral movement through WinRM and eventual ransomware payload execution.

### Unnamed parallel actor activity
Microsoft's report also shows an activity stream that did not match Storm-2603's known playbook:

- DLL sideloading where `ulib.dll` was proxied through `replace.exe` on one device, detected through an AppError event.
- Unsigned `srvcli.dll` staged under `%LOCALAPPDATA%\Temp` and `C:\Users\Public\Documents`.
- `NTDS.dit` archive creation as `NTDS.zip` on multiple devices.
- VPN ingress from external VPS infrastructure.

## Defender heuristics
### Exposure and patching
- Prioritize internet-facing SharePoint inventory, patch validation, and exploit telemetry review.
- Treat LFI-style probes for `win.ini`, `web.config`, and similar configuration files as meaningful reconnaissance when observed against collaboration or web application servers.
- Keep vulnerable-driver blocklists, HVCI, and tamper protection enforced where possible; review exceptions that allow known-vulnerable drivers to load.

### Tooling abuse
- Establish an allowlist and business owner for Velociraptor, Zoho Assist, Cloudflare Tunnel, VS Code Remote SSH, and similar remote-management paths.
- Alert when response tools or developer tunnels appear for the first time on servers, run as SYSTEM, or launch shortly after web-server exploitation signals.
- Correlate remote-access installation events with privileged account creation, domain-admin group changes, and outbound tunnel establishment.

### Credential and directory response
- Hunt for `NTDS.dit`, `NTDS.zip`, Volume Shadow Copy access, and domain-controller archive creation outside approved backup workflows.
- Review new local administrators, new domain administrators, and privileged sign-ins around the first known SharePoint reconnaissance window.
- Reset and rotate credentials only after containment planning; premature rotation can tip active actors while leaving tunnel or admin persistence intact.

### Timeline reconstruction
- Do not assume all artifacts belong to the ransomware actor. Split timelines by tooling, host clusters, ingress paths, and payload families.
- Preserve endpoint crash / AppError telemetry, DLL load events, RMM logs, tunnel logs, identity logs, and cloud sign-in data before rebuilding affected systems.
- Look for evidence that one actor's activity masked another's: overlapping C2, duplicate persistence, conflicting toolchains, or credential theft that predates ransomware staging.

## Related pages
- [FortiBleed Fortinet credential exposure](fortibleed-fortinet-credential-exposure.md)
- [Operation Endgame SocGholish disruption](operation-endgame-socgholish-disruption.md)
- [PAN-OS GlobalProtect CVE-2026-0257 exploitation](pan-os-globalprotect-cve-2026-0257-exploitation.md)
- [ClickOnce COM hijacking abuse](../patterns/clickonce-com-hijacking-abuse.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/06/22/one-intrusion-two-cyberattackers-uncovering-parallel-threat-activity/>
- Microsoft Cyberattack Series No. 9 PDF: <https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/bade/documents/products-and-services/en-us/security/Cyberattacks-Series-Report-Q4.pdf>
