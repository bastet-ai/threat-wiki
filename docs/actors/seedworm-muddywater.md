# Seedworm / MuddyWater

## Summary
**Seedworm** is an Iran-linked espionage actor also tracked publicly as **MuddyWater**, **Temp Zagros**, and **Static Kitten**. Broadcom's Symantec and Carbon Black teams reported a first-quarter 2026 campaign affecting at least nine organizations across nine countries and four continents, including a South Korean electronics manufacturer, Middle Eastern government and airport targets, Southeast Asian industrial manufacturers, financial services, education, and professional-services organizations.

The durable intelligence value is the actor's maturing operational hygiene: Node.js-orchestrated PowerShell activity, signed-binary DLL sideloading, credential theft, browser-data theft through ChromElevator, SOCKS5 tunneling, public file-transfer service exfiltration, and repeated low-cadence implant-driven reconnaissance rather than continuous hands-on-keyboard activity. Broadcom separately reported that Seedworm had access in February-March 2026 to U.S. and allied networks including a bank, airport, software supplier with Israeli operations, and non-profit organizations, where it used newly named Deno- and Python-based backdoors before the regional conflict widened.

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
- Deno
- Python
- Dindoor
- Fakeset
- Rclone
- Wasabi
- Backblaze
- United States
- Canada
- Israel
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

### Dindoor and Fakeset prepositioning on U.S. and allied networks
Broadcom also reported Seedworm activity beginning in early February 2026 and continuing into March against a U.S. bank, U.S. airport, U.S. software company with Israeli operations, and U.S. / Canadian non-profit organizations. The timing matters because the intrusions predated and overlapped the wider U.S.-Israel / Iran conflict, leaving the actor positioned inside strategically sensitive environments before destructive or retaliatory cyber operations became a higher concern.

Durable pivots from that activity include:

- **Dindoor**, a previously unknown backdoor using the Deno JavaScript / TypeScript runtime, seen at the Israeli operation of a U.S. software supplier, a U.S. bank, and a Canadian non-profit.
- **Fakeset**, a Python backdoor seen at a U.S. airport and non-profit.
- Code-signing certificates issued to `Amy Cherne` and `Donald Gay`; Broadcom noted prior Seedworm linkage for the `Donald Gay` certificate through Stagecomp / Darkcomp malware.
- Backblaze B2 staging domains including `gitempire.s3.us-east-005.backblazeb2.com` and `elvenforest.s3.us-east-005.backblazeb2.com`.
- Attempted Rclone exfiltration from the software supplier to a Wasabi cloud-storage bucket.

For defenders, this older but previously unreflected reporting is useful because it ties Seedworm's custom backdoor development to cloud-storage staging and exfiltration paths, and it raises the priority of hunting for Deno runtimes, Python backdoors, unusual signed binaries, and Rclone activity in U.S., Israeli, Canadian, aviation, financial, and software-supply-chain networks during periods of Iran-linked geopolitical escalation.

## Defender heuristics
- Hunt for `node.exe` spawning PowerShell, `cmd.exe`, `curl.exe`, signed driver utilities, or endpoint-security binaries in user-profile staging directories.
- Hunt for unexpected `deno.exe`, Python runtimes, or newly introduced JavaScript / TypeScript runtime artifacts on sensitive workstations and servers, especially when paired with signed unknown binaries or cloud-storage staging.
- Flag `fmapp.exe` loading a nearby `fmapp.dll` outside expected Fortemedia installation paths.
- Flag `sentinelmemoryscanner.exe` loading a nearby `sentinelagentcore.dll`, especially outside normal SentinelOne directories or under random user-profile paths.
- Look for Run-key persistence pointing to signed utilities in random `%LOCALAPPDATA%` paths.
- Correlate quick bursts of domain reconnaissance, screenshot capture, `reg save hklm\sam/security/system`, and public-IP checks from the same endpoint.
- Treat `sendit[.]sh`, Wasabi, Backblaze B2, and other cloud-storage uploads from servers or sensitive user workstations as suspicious when paired with compression, credential dumping, Rclone, or Iranian actor TTPs.
- Preserve process trees, script-block logs, PowerShell history, Node.js artifacts, sideloaded DLLs, Run-key values, browser credential access telemetry, and egress records before cleanup.

## Related pages
- [Langflow CVE-2025-34291 exploitation](../ops/langflow-cve-2025-34291-exploitation.md)
- [Screening Serpens](screening-serpens.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- Broadcom / Symantec and Carbon Black: [https://www.security.com/threat-intelligence/iran-seedworm-electronics](https://www.security.com/threat-intelligence/iran-seedworm-electronics)
- Broadcom / Symantec and Carbon Black: [https://www.security.com/threat-intelligence/iran-cyber-threat-activity-us](https://www.security.com/threat-intelligence/iran-cyber-threat-activity-us)
- The Hacker News summary: [https://thehackernews.com/2026/05/muddywater-uses-dll-side-loading-in.html](https://thehackernews.com/2026/05/muddywater-uses-dll-side-loading-in.html)
- Group-IB Operation Olalampo: [https://www.group-ib.com/blog/muddywater-operation-olalampo/](https://www.group-ib.com/blog/muddywater-operation-olalampo/)
