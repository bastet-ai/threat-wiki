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
- BreachForums

## Why this matters
- Microsoft says The Gentlemen has impacted organizations across education, transportation, healthcare, and financial sectors in North America, South America, Europe, Africa, and Asia.
- The RaaS program reportedly moved from a closed group in mid-2025 to an affiliate model in September 2025, then established a BreachForums partnership to recruit affiliates, penetration testers, and initial-access brokers.
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
- Alert on unusual combinations of Defender exclusion changes, shadow-copy deletion, event-log clearing, prefetch/log cleanup, PowerShell-history deletion, and mass service termination.
- Review scheduled-task creation and service-control activity from unusual parent processes, especially when followed by `vssadmin`, `wmic`, `wevtutil`, `schtasks`, or PowerShell Defender preference changes.
- Monitor for sudden enabling of network-discovery services and firewall rules on servers where that behavior is not normal.
- Prioritize credentials exposed to affiliates: domain admin, backup admin, hypervisor, EDR, RMM, file-server, and service-account credentials can turn The Gentlemen from host-level encryption into fleet-wide impact.
- Maintain offline / immutable backups and test restore workflows; the malware explicitly targets backup services and recovery artifacts.

## Attribution notes
Microsoft tracks the RaaS operators as **Storm-2697**. Affiliates may vary by intrusion, so distinguish between the platform operator, affiliate hands-on-keyboard behavior, and any initial-access broker involved in a specific incident.

## Related pages
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md)
- [TeamPCP](../actors/teampcp.md)
- [Ababil of Minab MOIS-linked recovery-destruction campaign](../ops/ababil-of-minab-mois-recovery-destruction.md)

## Sources
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/05/28/the-gentlemen-ransomware-dissecting-a-self-propagating-go-encryptor/
