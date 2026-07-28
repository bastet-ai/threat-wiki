# Mirage Kitten NightLedger, BridgeHead, and ArcBridge campaign

## Summary
Kaspersky GReAT disclosed a previously undocumented **Mirage Kitten** malware set on July 28, 2026. The reporting combines **NightLedger**, a Windows HTTPS backdoor, with **BridgeHead** and **ArcBridge**, two WebSocket tunnelers intended to give operators covert access through selected victim systems.

The report adds durable victimology, command behavior, load paths, mutexes, network protocols, file hashes, and infrastructure. It does not establish initial access for most recovered samples, so the tools should not be forced into one universal intrusion chain.

## Tags
- ops
- operation
- campaign
- Mirage Kitten
- UNC1549
- Smoke Sandstorm
- Nimbus Manticore
- Iran-nexus
- espionage
- Middle East
- Africa
- Egypt
- Jordan
- Tanzania
- Pakistan
- Ethiopia
- Burkina Faso
- aerospace
- aviation
- government targeting
- telecommunications
- financial sector
- spear phishing
- fake recruiting
- NightLedger
- BridgeHead
- ArcBridge
- DLL search-order hijacking
- WebSocket
- SOCKS5
- tunneling
- environmental keying

## Why this matters
- The backdoor and tunnelers provide complementary control: endpoint reconnaissance and tasking through NightLedger, plus operator-selected internal-network reach through BridgeHead and ArcBridge.
- BridgeHead can traverse enterprise proxies using the victim's Negotiate or NTLM context, making outbound activity resemble authenticated corporate traffic.
- Per-victim username checks show that some tunnel builds were tailored after internal reconnaissance and may remain inert outside their intended endpoint.
- Kaspersky observed movement away from Microsoft Azure subdomain-style infrastructure toward Cloudflare-backed domains in some malware, reducing the value of static hosting-provider allow or deny assumptions.

## Reported intrusion and tool chain

### Access and deployment
- Kaspersky says initial access remains unclear for most samples.
- BridgeHead deployments in Egypt and a Pakistan-based aerospace and aviation environment followed tradecraft consistent with highly tailored spear phishing.
- Reported lure themes included recruitment content, trusted hiring brands, and lookalike videoconferencing pages redirecting targets to malicious archives on third-party file-sharing services.

### NightLedger endpoint control
- A malicious `SspiCli.dll` is loaded through a legitimate `AppVShNotify.exe` / `RPCRT4.dll` delay-load path.
- The implant polls HTTPS, parses tasks separated by `#%%#`, and supports command execution, file transfer, directory and process discovery, DLL loading, screenshot capture, process termination, and drive enumeration.
- Collection of `C:\Windows\debug\NetSetup.log` can expose domain-join and network-setup history useful for follow-on movement.

### BridgeHead network access
- Reported deployment paths included `%LocalAppData%\Microsoft\VisualStudio\unbcl.dll` and `C:\program files (x86)\univpn\promote\libwinpthread-1.dll`.
- The client requires a hard-coded substring in the lowercased Windows username before it activates.
- It upgrades to WSS, handles corporate proxy authentication, and relays server-selected SOCKS5 traffic over a compact binary protocol.

### ArcBridge network access
- ArcBridge stores its C2, port, timing, SSL, and likely implant identifier in an embedded configuration block.
- Its public command set includes `OPEN:` for a tunnel session and `DNS:` for name or address resolution.

## Victimology
Kaspersky telemetry identified victims in:
- Egypt;
- government and SMB environments in Jordan and Tanzania;
- aerospace and aviation organizations in Pakistan;
- telecommunications companies in Ethiopia; and
- financial-sector entities in Burkina Faso.

This is observed scope, not a complete victim list.

## Public infrastructure
- `smartconnect[.]azurewebsites[.]net`
- `businessmixture[.]com`
- `global-reds[.]com`
- `maadinglobal[.]com`
- `Business-deegital[.]com`
- `business-deegital[.]azurewebsites[.]net`
- `businessdeegital[.]azurewebsites[.]net`
- `neexportfolio[.]azurewebsites[.]net`
- `neexportfolio[.]com`
- `neexportfolio[.]eastus[.]cloudapp[.]azure[.]com`
- `172[.]86[.]98[.]113`
- `aecert[.]org`
- `realhealthshop[.]com`
- `tjconsultingservices[.]com`
- `thehealth-life[.]com`
- `buisness-centeral-transportation[.]com`
- `healthcarezoom-centeral[.]azurewebsites[.]net`
- `healthcarezoomcenteral[.]azurewebsites[.]net`
- `healthcarezoomcenteral[.]org`
- `toadreport[.]azurewebsites[.]net`
- `business-startup[.]azurewebsites[.]net`
- `businessstartup[.]azurewebsites[.]net`

## Defender heuristics
- Correlate recruitment or videoconference archive delivery with local DLL loads by `AppVShNotify.exe`, new Visual Studio or UniVPN-like DLLs, and WSS sessions.
- Alert on `AppVShNotify.exe` loading an application-local `SspiCli.dll`, especially before HTTPS to business- or healthcare-themed domains.
- Hunt proxy logs for unusual WebSocket upgrades, HTTP 407 followed by Negotiate or NTLM success, the literal `token` authentication message where payload inspection is available, and long-lived relay traffic.
- Search endpoints for the NightLedger and ArcBridge mutexes, BridgeHead paths, custom NightLedger URLs, `#%%#`, and ArcBridge's `<<STARTXX>>` configuration marker.
- Review subsequent access from suspected relay hosts to internal systems. A compromised tunnel endpoint can make operator traffic appear to originate from an authorized workstation.
- Isolate before exercising a victim-keyed sample. Preserve the username context and original binary, but do not execute recovered malware in production to validate the check.

## Attribution and evidence notes
- Kaspersky attributes the malware set to Mirage Kitten from code and behavioral similarity to historical implants and shared tradecraft.
- The report names UNC1549, Smoke Sandstorm, and Nimbus Manticore as aliases.
- Infrastructure overlap, Azure or Cloudflare hosting, and a business-themed domain are not independently sufficient for attribution.
- Public indicators will age; retain the behavior-based detections around DLL loading, proxy-authenticated WebSockets, environmental keying, and internal relay traffic.

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [NightLedger](../tools/nightledger.md)
- [BridgeHead](../tools/bridgehead.md)
- [ArcBridge](../tools/arcbridge.md)
- [Iran-linked threat landscape: access optionality and evidence quality](../notes/iran-linked-threat-landscape-july-2026.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
