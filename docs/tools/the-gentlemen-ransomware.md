# The Gentlemen ransomware

## Summary
Microsoft Threat Intelligence's May 28, 2026 analysis describes **The Gentlemen** as a Windows-focused ransomware-as-a-service encryptor operated by the financially motivated actor Microsoft tracks as **Storm-2697**. The malware is written in Go, obfuscated with Garble, and combines double-extortion operations with unusually aggressive self-propagation and lateral-movement features.

The durable point for defenders is not just the encryption design. The Gentlemen is built to turn an existing privileged foothold into broad network impact by relaunching itself as SYSTEM, encrypting local and network shares separately, enabling network discovery, and attempting multiple simultaneous lateral-movement paths when operators provide credentials or let it reuse the current session token.

## Tags
- tools
- malware
- ransomware
- RaaS
- The Gentlemen
- Storm-2697
- cybercrime
- double extortion
- Windows
- Go
- Garble
- self-propagation
- lateral movement
- scheduled tasks
- registry persistence
- Defender evasion
- backup disruption
- Curve25519
- XChaCha20
- ESXi
- SystemBC
- Advanced IP Scanner
- ArmCorp
- Qilin
- Spikey Scorpius
- Howling Scorpius
- BreachForums
- GentleKiller
- EDR killer
- BYOVD
- HexKiller
- ThrottleBlood
- HavocKiller
- OxideHarvest

## Why this matters
- Microsoft says The Gentlemen has impacted organizations across education, transportation, healthcare, and financial sectors in North America, South America, Europe, Africa, and Asia.
- The RaaS program reportedly moved from a closed group in mid-2025 to an affiliate model in September 2025, then established a BreachForums partnership to recruit affiliates, penetration testers, and initial-access brokers.
- Unit 42's July 10, 2026 update says public reporting indicates the operators may have been active earlier as **ArmCorp**, an affiliate of **Qilin** (tracked by Unit 42 as **Spikey Scorpius**), before moving into their own RaaS model.
- Unit 42 also reports that the crew has become one of 2026's most active RaaS programs by leak-site volume: a reputable public tracker counted **580 claimed victims across 77 countries** through July 7, including **103 manufacturing victims**, with June 2026 reaching **117 claimed victims**.
- The affiliate economics are an operational signal: Unit 42 notes The Gentlemen advertised an unusually high **90% affiliate payout**, above the 70%-80% split common in many RaaS programs, which may help explain recruitment and victim-volume acceleration.
- The encryptor includes operator-facing switches for encryption scope, speed, delayed execution, network-share-only encryption, full local-plus-share encryption, propagation, persistence, and free-space wiping.
- The malware is designed to maximize blast radius after initial access by combining encryption reliability, recovery denial, and lateral propagation rather than relying on one movement technique.

## Operator controls and execution model
- The binary requires a build-specific `--password` argument before it executes primary functionality.
- `--full` is the likely intended comprehensive mode: it spawns separate child processes for `--system` local-drive encryption and `--shares` mapped / UNC-share encryption.
- `--system` creates and triggers a scheduled task named `gentlemen_system` to rerun the payload as SYSTEM when administrative rights are available.
- `--shares` focuses on mapped network drives and available Universal Naming Convention shares visible to the current user session.
- `--spread <domain/user:password>` enables self-propagation; Microsoft notes it can use supplied credentials or the current session token.
- `--fast`, `--superfast`, and `--ultrafast` tune partial-file encryption percentages for large files, while small files are fully encrypted.
- `--keep` disables self-deletion and `--wipe` wipes free disk space after encryption, increasing recovery difficulty.

## Tradecraft notes
### Operator-maintained EDR killer suite
- ESET's June 18, 2026 analysis describes Gentlemen as unusual among RaaS crews because the operators, not just affiliates, actively develop and maintain an EDR-killer portfolio for affiliates.
- ESET names the in-house framework **GentleKiller** and says it has at least eight variants abusing different vulnerable or malicious drivers.
- The portfolio also operationally integrates third-party or leaked EDR killers: **HexKiller**, **ThrottleBlood**, and **HavocKiller**.
- Broadcom / Symantec's July 9, 2026 GodDamn ransomware reporting adds an important cross-crew pivot for **PoisonX**: Symantec observed PoisonX dropped as `g11.sys` by a defense-evasion binary masquerading as `symantec.exe`, and described the driver as malicious code that appears to have obtained a Microsoft Windows Hardware Compatibility Publisher signature rather than merely abusing an older legitimate vulnerable driver.
- The tools share a defense-evasion layer that impersonates mainly security vendors through fake version metadata plus copied legitimate certificates and icons.
- Gentlemen operators rapidly adopt newly disclosed BYOVD proof-of-concept techniques, in some cases within days of public release.
- ESET also links **OxideHarvest**, a credential stealer maintained by one Gentlemen affiliate, to the broader ecosystem.

### Unit 42 July 2026 operational context
- Unit 42 frames The Gentlemen as active since at least July 2025, with public reporting suggesting earlier activity as ArmCorp inside the Qilin / Spikey Scorpius ecosystem.
- Their ransomware variants span **C** and **Go**, giving operators coverage across Windows, other operating systems, and virtualized infrastructure rather than a single-host Windows-only blast pattern.
- Initial-access routes resemble other high-volume RaaS programs: edge-device exploitation, exposed remote-access services, brute force, leaked / stolen credentials, and initial-access-broker collaboration.
- Unit 42 highlights a custom Go backdoor, GentleKiller, and suspected use of an unspecified zero-day vulnerability as defense-evasion and post-access amplifiers.
- The May 2026 BreachForums partnership with HasanBroker should be treated as a recruiting and access-brokering signal, not just branding.

### Defense evasion and recovery denial
- Disables Microsoft Defender real-time monitoring, adds the malware executable to Defender exclusions, and excludes the `C:\` volume from scanning.
- Deletes Volume Shadow Copies using `vssadmin` and `wmic` and clears System, Application, and Security event logs with `wevtutil`.
- Removes forensic artifacts such as prefetch files, Defender diagnostic/support logs, RDP logs, and PowerShell command history across user profiles.
- Terminates or stops processes and services associated with databases, virtualization, backup/recovery tooling, EDR products, SAP, Exchange, Office/email clients, web servers, accounting software, and remote-access tools.

### Persistence
- Creates startup scheduled tasks named `UpdateSystem` and `UpdateUser` for SYSTEM and user-context persistence.
- Writes redundant Run-key persistence values: `GupdateS` under HKLM and `GupdateU` under HKCU.
- Sets `LOCKER_BACKGROUND=1` in background worker contexts to distinguish elevated encryption workers from the original operator-launched process.

### Network discovery and share traversal
- Probes drive letters A through Z to identify mapped network drives.
- Enables Windows network-discovery services such as Function Discovery Resource Publication, Function Discovery Provider Host, SSDP Discovery, and UPnP Device Host.
- Enables the Network Discovery firewall rule group to increase visibility of reachable resources.
- Enumerates volumes through WMI and drive-letter brute force to maximize local encryption coverage.

### Encryption design
- Microsoft reports per-file ephemeral Curve25519 keys paired with the XChaCha20 stream cipher.
- The malware supports configurable partial encryption for large files, while small files are encrypted fully.
- The encryption architecture is paired with process/service killing so databases, backups, mail stores, and Office documents are less likely to remain locked and unencrypted.

## Defender heuristics
- Treat discovery of The Gentlemen on one host as a network-wide ransomware event: immediately segment affected systems and hunt for propagation attempts, not just local encryption.
- Hunt Windows telemetry for `gentlemen_system`, `UpdateSystem`, `UpdateUser`, `GupdateS`, `GupdateU`, and `LOCKER_BACKGROUND` artifacts.
- Add high-severity detections for creation, deletion, or execution of scheduled tasks matching `gentlemen*`, as Unit 42 explicitly calls out this scheduled-task naming pattern.
- Alert on unusual combinations of Defender exclusion changes, shadow-copy deletion, event-log clearing, prefetch/log cleanup, PowerShell-history deletion, and mass service termination.
- Treat vulnerable-driver loading or sudden driver-blocklist bypass behavior immediately before ransomware staging as a high-priority Gentlemen/GentleKiller pivot, especially when binaries impersonate security vendors through copied icons, certificates, or version resources.
- Baseline and enforce Microsoft vulnerable-driver blocklist, HVCI / memory-integrity policy, and EDR tamper-protection controls; operator-maintained EDR killers make defense impairment part of the platform, not an affiliate afterthought.
- Prioritize exposure review and patch validation for edge / remote-access and privilege-escalation vulnerabilities Unit 42 listed in Gentlemen guidance: Fortinet FortiOS/FortiProxy **CVE-2024-55591**, Erlang/OTP SSH **CVE-2025-32433**, Windows SMB Client **CVE-2025-33073**, **React2Shell CVE-2025-55182**, and **ThrottleStop.sys CVE-2025-7771**.
- Review scheduled-task creation and service-control activity from unusual parent processes, especially when followed by `vssadmin`, `wmic`, `wevtutil`, `schtasks`, or PowerShell Defender preference changes.
- Monitor for sudden enabling of network-discovery services and firewall rules on servers where that behavior is not normal.
- Monitor internal reconnaissance tooling such as **Advanced IP Scanner**, anomalous outbound traffic over non-standard ports, and traffic matching known **SystemBC** communication signatures.
- Treat ESXi and virtualization management as tier-0 during Gentlemen response: disable SSH by default, enable it only for explicit maintenance windows, and isolate management interfaces on dedicated management networks.
- Prioritize credentials exposed to affiliates: domain admin, backup admin, hypervisor, EDR, RMM, file-server, and service-account credentials can turn The Gentlemen from host-level encryption into fleet-wide impact.
- Maintain offline / immutable backups and test restore workflows; the malware explicitly targets backup services and recovery artifacts.

## Attribution notes
Microsoft tracks the RaaS operators as **Storm-2697**. Affiliates may vary by intrusion, so distinguish between the platform operator, affiliate hands-on-keyboard behavior, and any initial-access broker involved in a specific incident.

## Related pages
- [GodDamn ransomware PoisonX BYOVD activity](../ops/goddamn-ransomware-poisonx-byovd.md)
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md)
- [TeamPCP](../actors/teampcp.md)
- [Ababil of Minab MOIS-linked recovery-destruction campaign](../ops/ababil-of-minab-mois-recovery-destruction.md)

## Sources
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/05/28/the-gentlemen-ransomware-dissecting-a-self-propagating-go-encryptor/
- ESET WeLiveSecurity: https://www.welivesecurity.com/en/eset-research/killing-me-gently-inside-gentlemens-edr-killer-framework/
- Broadcom / Symantec Threat Hunter Team: https://www.security.com/threat-intelligence/goddamn-ransomware-beast-rebrand
- Unit 42: https://unit42.paloaltonetworks.com/the-gentlemen-ransomware/
