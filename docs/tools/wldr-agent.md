# WLDR agent

## Summary
**WLDR agent** is a bespoke PowerShell-based command-and-control memory implant reported by Cisco Talos in July 2026 and deployed by [UAT-11795](../actors/uat-11795.md) through [Starland RAT](starland-rat.md). Talos tracks the wider framework as **WLDR C2**, based on internal project naming visible in the actor's scripts.

WLDR supports encrypted beaconing, host reconnaissance, task queues, and PowerShell Runspace execution for operator-delivered scripts and payloads.

## Tags
- tools
- malware
- PowerShell
- memory implant
- C2
- encrypted C2
- Runspace
- task queue
- post-exploitation
- UAT-11795
- Starland RAT

## Why this matters
- WLDR turns an initial Starland RAT foothold into an interactive PowerShell post-exploitation channel.
- The implant is memory-resident and receives its C2 address through loader-injected global variables, reducing simple file-artifact visibility.
- Its RunspacePool engine can stream output, errors, and warnings back to C2 in near real time, supporting interactive operator workflows rather than only batch execution.
- The C2 response model is hardware-identifier-bound, so sandbox or curl tests without the expected victim identifier may receive no payload.

## Delivery chain
- In Talos' observed campaign, UAT-11795 used Starland RAT to execute a Windows shell command that downloaded and ran a PowerShell stager.
- The stager resolves PowerShell aliases, builds obfuscated .NET type references, and XOR-decrypts the embedded WLDR downloader.
- The downloader derives a hardware identifier from the C: drive volume serial number and appends it to hardcoded C2 URLs.
- The C2 returns an encrypted JSON envelope only for pre-registered HWIDs.
- The downloader decrypts the envelope with a key derived from hardcoded password `odg5t8mvssvh`, salt, and AES/HMAC-style fields, then executes the WLDR agent in memory.

## Capabilities
- Encrypted HTTP beaconing and C2 registration with victim profile data.
- WMI-based reconnaissance of antivirus products, network adapters, OS version/build, domain membership, CPU, RAM, administrative privilege, and UAC policy.
- Hardware identifier derived from C: drive volume serial number, with registry GUID or hostname checksum fallback.
- Initial HTTP POST containing victim profile, infection identifier, protocol version `2.0.0`, and cryptographic session parameters.
- HTTPS polling every 10 seconds after registration, with Chrome 124-like headers.
- AES-256-CBC with HMAC-SHA256, PBKDF2-SHA256, per-message IVs, and protocol tag `WSv1` bound to MAC computation as reported by Talos.
- Task execution through a primary PowerShell RunspacePool with up to 10 concurrent threads, falling back to standard PowerShell background jobs.

## Defender heuristics
- Hunt for Starland or suspicious shell commands that download additional PowerShell from `eorthopaedics[.]com` `/feed/` or `sastoro[.]com` `/alpha/` paths.
- Treat C2 probes that require an HWID path component as suspicious even when manual validation returns idle or empty responses.
- Monitor for PowerShell processes that perform WMI host inventory followed by encrypted HTTPS polling with Chrome-like headers and 10-second intervals.
- Capture memory and PowerShell script block logs where possible before remediation; WLDR's core payload may not persist as a simple on-disk script.
- Correlate WLDR activity with follow-on CastleStealer or Remcos deployment, since Talos reports both as available payloads in the same campaign.

## Related pages
- [UAT-11795 Starland / WLDR campaign](../ops/uat-11795-starland-wldr-campaign.md)
- [UAT-11795](../actors/uat-11795.md)
- [Starland RAT](starland-rat.md)

## Sources
- Cisco Talos: [https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/](https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/)
