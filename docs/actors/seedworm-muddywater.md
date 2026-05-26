# Seedworm / MuddyWater

## Summary
**Seedworm** is an Iran-linked espionage actor also tracked publicly as **MuddyWater**, **Temp Zagros**, and **Static Kitten**. Broadcom's Symantec and Carbon Black teams reported a first-quarter 2026 campaign affecting at least nine organizations across nine countries and four continents, including a South Korean electronics manufacturer, Middle Eastern government and airport targets, Southeast Asian industrial manufacturers, financial services, education, and professional-services organizations.

The durable intelligence value is the actor's maturing operational hygiene: Node.js-orchestrated PowerShell activity, signed-binary DLL sideloading, credential theft, browser-data theft through ChromElevator, SOCKS5 tunneling, public file-transfer service exfiltration, and repeated low-cadence implant-driven reconnaissance rather than continuous hands-on-keyboard activity.

## Tags
- Iran
- MOIS
- espionage
- MuddyWater
- Seedworm
- Static Kitten
- Temp Zagros
- DLL sideloading
- Node.js
- PowerShell
- ChromElevator
- credential theft
- browser credential theft
- SOCKS5
- public file-transfer exfiltration
- sendit.sh
- South Korea
- manufacturing
- education
- public sector
- financial services

## Primary motivation
- **Espionage** against sectors likely to hold intelligence value for Tehran: electronics and industrial manufacturing, government, airports, finance, education, and professional services.
- **Credential and browser-data theft** to support lateral movement and follow-on collection.
- **Operational durability** through redundant tools, signed-binary sideloading, and staging paths that blend with legitimate software and consumer services.

## 2026 campaign tradecraft
### Signed-binary DLL sideloading
Broadcom observed two sideloading pairs:

- `fmapp.exe`, a legitimate Fortemedia audio-driver utility, loading malicious `fmapp.dll`.
- `sentinelmemoryscanner.exe`, a signed SentinelOne component, loading malicious `sentinelagentcore.dll`.

The SentinelOne binary choice is especially useful for defenders: it can confuse path- or signature-based triage because the parent executable looks like endpoint-security software.

### Node.js-orchestrated PowerShell
The campaign repeatedly showed `node.exe` as the parent or grandparent of PowerShell, `cmd.exe`, and sideloaded binaries. Broadcom found a Node.js script embedded in an XML file on a targeted host. This looks like a tactical shift from raw PowerShell execution toward JavaScript-runtime orchestration, adjacent to prior reporting that Seedworm experimented with Deno.

### Credential theft and collection
Observed collection included:

- PowerShell reconnaissance (`whoami`, `ipconfig`, domain group enumeration, WMI antivirus enumeration).
- Screenshot capture early in the intrusion.
- SAM, SECURITY, and SYSTEM hive theft via `reg save`.
- A CredUI-style credential harvester that prompts for Windows credentials and writes passwords to `C:\ProgramData\lopa.txt`.
- A privilege-escalation component attempting Kerberos TGT extraction through GSS-API delegation abuse.
- ChromElevator embedded in malicious DLLs to steal Chromium passwords, cookies, and payment-card data despite App-Bound Encryption protections.

### Exfiltration and staging
- Staging used plaintext HTTP from `179.43.177[.]220:8080` and HTTPS from `timetrakr[.]cloud` in the reported electronics-manufacturer intrusion.
- At least one intrusion exfiltrated data through `sendit[.]sh`, a public file-transfer service.
- The cadence of repeated short recon and periodic re-execution of sideloaded binaries suggests implant timers and tunnel maintenance rather than continuous manual operator presence.

## Defender heuristics
- Hunt for `node.exe` spawning PowerShell, `cmd.exe`, `curl.exe`, signed driver utilities, or endpoint-security binaries in user-profile staging directories.
- Flag `fmapp.exe` loading a nearby `fmapp.dll` outside expected Fortemedia installation paths.
- Flag `sentinelmemoryscanner.exe` loading a nearby `sentinelagentcore.dll`, especially outside normal SentinelOne directories or under random user-profile paths.
- Look for Run-key persistence pointing to signed utilities in random `%LOCALAPPDATA%` paths.
- Correlate quick bursts of domain reconnaissance, screenshot capture, `reg save hklm\sam/security/system`, and public-IP checks from the same endpoint.
- Treat `sendit[.]sh` uploads from servers or sensitive user workstations as suspicious when paired with compression, credential dumping, or Iranian actor TTPs.
- Preserve process trees, script-block logs, PowerShell history, Node.js artifacts, sideloaded DLLs, Run-key values, browser credential access telemetry, and egress records before cleanup.

## Related pages
- [Langflow CVE-2025-34291 exploitation](../ops/langflow-cve-2025-34291-exploitation.md)
- [Screening Serpens](screening-serpens.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- Broadcom / Symantec and Carbon Black: https://www.security.com/threat-intelligence/iran-seedworm-electronics
- The Hacker News summary: https://thehackernews.com/2026/05/muddywater-uses-dll-side-loading-in.html
- Group-IB Operation Olalampo: https://www.group-ib.com/blog/muddywater-operation-olalampo/
