# RemotePE

## Summary
**RemotePE** is a Lazarus-linked, memory-only remote access trojan documented by Fox-IT / NCC Group in May 2026. It is delivered through a three-stage chain: `DPAPILoader` decrypts a victim-bound payload with Windows DPAPI, `RemotePELoader` contacts operator infrastructure and retrieves the final payload, and RemotePE runs entirely in memory without being written to disk.

Fox-IT ties the toolset to a North Korea-aligned Lazarus subgroup overlapping AppleJeus, Citrine Sleet, UNC4736, and Gleaming Pisces reporting, with observed targeting of financial, cryptocurrency, and DeFi organizations. The durable defender lesson is that this toolset is built for quiet long-term access: environmental keying, low file-system footprint, userland-hook/ETW evasion, and actor-in-the-loop payload delivery make disk-only triage weak.

## Tags
- tools
- malware
- RAT
- RemotePE
- DPAPILoader
- RemotePELoader
- Lazarus
- AppleJeus
- Citrine Sleet
- UNC4736
- Gleaming Pisces
- North Korea
- cryptocurrency
- financial sector
- DeFi
- DPAPI
- environmental keying
- memory-only malware
- EDR evasion
- ETW patching
- HellsGate
- TartarusGate
- libpeconv
- pe_to_shellcode
- C2
- long-term access
- espionage
- financial theft

## Why this matters
- RemotePE is intentionally resistant to simple malware collection: encrypted payload blobs are bound to victim DPAPI keys, so copied disk artifacts may not decrypt or execute elsewhere.
- The final RAT is retrieved by RemotePELoader and executed only in memory, reducing recoverable payload artifacts in ordinary filesystem evidence.
- The toolset uses operator-controlled delivery, configurable sleep/wake behavior, and low VirusTotal exposure, consistent with selective use against high-value targets.
- Fox-IT observed overlap with previously reported Lazarus financial/crypto intrusion activity, including social engineering against DeFi-sector personnel.

## Attack chain
1. **Initial access / staging:** prior access lets the operator place a DPAPI-encrypted payload and configuration on the victim host. Earlier public reporting linked the broader cluster to social engineering over Telegram and fake scheduling domains.
2. **DPAPILoader:** a DLL such as `Iassvc.dll` runs as a masqueraded Windows service named `Internet Authentication Service`, decrypts a payload using DPAPI, XORs it with `0x8D`, and reflectively loads it with `libpeconv`.
3. **RemotePELoader:** the second-stage loader reads a shared DPAPI-protected configuration, applies evasion, checks in to C2, and waits for an operator-delivered encrypted PE payload.
4. **RemotePE:** the final C++ RAT runs from memory, polls C2 for commands, and supports configuration changes, command execution, DLL module registration, file operations, process control, sleep/exit commands, and ping.

## Operational characteristics
- **Persistence masquerade:** Fox-IT observed `C:\Windows\System32\Iassvc.dll` registered as service `Ias` / `Internet Authentication Service`, intentionally close to legitimate IAS naming and `iassvcs.dll`.
- **Victim-bound encryption:** DPAPILoader and configuration artifacts use Windows DPAPI plus XOR `0x8D`, making samples hard to analyze without victim keys.
- **Unexpected payload storage:** the incident sample searched `C:\ProgramData\Microsoft\Windows\DeviceMetadataStore\en-US*.*`, skipping legitimate Cabinet files and selecting non-CAB payload/configuration blobs by size.
- **EDR evasion:** RemotePELoader remaps clean copies of loaded DLLs using HellsGate/TartarusGate-style direct syscalls and patches `EtwEventWrite` to suppress ETW events.
- **C2 blending:** RemotePELoader and RemotePE use HTTP POSTs, Microsoft-looking cookie names such as `MicrosoftApplicationsTelemetryDeviceId`, encrypted message bodies, and JSON keys such as `odata.metadata`.
- **Memory-only final stage:** RemotePE is AES-GCM delivered, reflectively loaded, and never written to disk by the normal chain.
- **Plugin capability:** RemotePE can register and invoke DLL modules at runtime; Fox-IT notes the module expectations resemble shellcodified DLL workflows.
- **Secure-delete behavior:** its file-delete command overwrites files seven times before renaming and deleting them, echoing patterns seen in PondRAT and POOLRAT / SIMPLESEA.
- **Out-of-band wake trigger:** RemotePE watches for Windows event `554D5C1F-AABE-49E4-AB57-994D22ECED28` to restart controller threads.

## Defender heuristics
- Hunt for suspicious services named `Ias` or `Internet Authentication Service` whose `ServiceDll` points to `Iassvc.dll` rather than the legitimate `iassvcs.dll` path.
- Review `C:\ProgramData\Microsoft\Windows\DeviceMetadataStore\` for non-CAB files, unusually large encrypted-looking blobs, or artifacts not matching expected Microsoft device metadata packages.
- Preserve DPAPI material during incident response; copying the encrypted payload alone may not be enough to reconstruct the chain.
- Monitor for unsigned or suspicious DLLs loaded by `svchost.exe` service groups or sideloaded through security-product processes such as the Fox-IT-observed ESET `edp.exe` case.
- Correlate ETW disruption, clean-DLL remapping behavior, direct-syscall patterns, and reflective PE loading with suspicious service persistence.
- Inspect DNS/SNI/proxy logs for Fox-IT C2 domains such as `aes-secure[.]net`, `azureglobalaccelerator[.]com`, and `devicelinkintel[.]com`; treat hits as high-severity until scoped.
- Where TLS inspection is available, look for unusual HTTP cookies including `MicrosoftApplicationsTelemetryDeviceId`, `MSCC`, `MSFPC`, `HASH`, `LV`, `LUE`, `MS0`, `at_check`, and `ai_session`, especially when paired with `odata.metadata` JSON responses.

## Public indicators highlighted by Fox-IT
- **Domains:** `livedrivefiles[.]com`, `aes-secure[.]net`, `azureglobalaccelerator[.]com`, `msdeliverycontent[.]com`, `akamaicloud[.]com`, `intelcloudinsights[.]com`, `devicelinkintel[.]com`.
- **Host indicators:** `Iassvc.dll`; event name `554D5C1F-AABE-49E4-AB57-994D22ECED28`.
- **Sample hashes:** Fox-IT published SHA-256 hashes for DPAPILoader, decrypted RemotePELoader, and four RemotePE samples; use their IOC table as the canonical hash source.

## Related pages
- [3CX desktop app compromise](../ops/3cx-desktop-app-compromise.md)
- [ROADtools](roadtools.md)
- [First VPN](first-vpn.md)

## Sources
- Fox-IT / NCC Group: <https://blog.fox-it.com/2026/05/22/remotepe-the-lazarus-rat-that-lives-in-memory/>
- The Hacker News: <https://thehackernews.com/2026/05/lazarus-deploys-remotepe-memory-only.html>
