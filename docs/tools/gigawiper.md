# GigaWiper

## Summary
Microsoft Threat Intelligence's July 9, 2026 analysis describes **GigaWiper** as a Windows Golang destructive backdoor observed in compromised environments beginning in October 2025. The implant combines command-and-control, persistence, command execution, file movement, remote interactive control, event-log clearing, and multiple on-demand destructive routines.

The durable defender lesson is that GigaWiper is not a single wiper binary. Microsoft assesses it as an operational platform assembled from at least three malware families: a physical-disk wiper, a Crucio-derived fake-ransomware encryptor, and FlockWiper logic reimplemented in Go.

## Tags
- tools
- malware
- wiper
- destructive malware
- backdoor
- Windows
- Golang
- RabbitMQ
- Redis
- scheduled tasks
- event log clearing
- fake ransomware
- disk wiping
- Crucio
- FlockWiper
- Microsoft Threat Intelligence

## Why this matters
- GigaWiper merges quiet backdoor operation with destructive execution, letting an operator choose espionage, command execution, staging, or one of several destruction modes from the same implant.
- The backdoor embeds a standalone physical-disk wiper as command `1`, while separate commands can sabotage boot/kernel files, encrypt files without preserving keys, wipe only the Windows installation drive, and clear logs.
- The fake-ransomware path renames files with a `.candy` extension but randomly generates encryption material that is not saved, so it functions as irreversible destruction rather than recoverable extortion.
- Microsoft ties the platform to Crucio and FlockWiper through code, execution flow, function names, strings, and `GRAT` references, showing tool consolidation across an actor's destructive malware set.

## Architecture and behavior
### Persistence
- Uses `HKCU\SOFTWARE\OneDrive\Environment` to track execution count.
- Creates a scheduled task named `OneDrive Update` that runs roughly every minute and at startup.
- Later executions identify that the malware is running from Task Scheduler and continue normal operation.

### Command-and-control
- Uses RabbitMQ over AMQP for tasking and Redis for command status/output.
- Microsoft observed hard-coded, AES-decrypted configuration values pointing to `185.182.193[.]21:5544` for RabbitMQ and `185.182.193[.]21:7542` for Redis.
- Declares a fanout exchange named `All` for broadcast commands and a topic exchange named `Topic` for targeted routing-key tasking.

### Destructive commands
- **Command 1 / `WipeMain`:** physical-disk wiper that enumerates drives through WMI, identifies the Windows installation disk, removes partition references from non-Windows drives, overwrites raw disk content, and forces a reboot.
- **Command 2:** disables Windows recovery, changes ownership/permissions on critical boot and kernel files, and deletes them to induce system failure.
- **Command 3 / `RanMain` / `BigBangExtortMain`:** Crucio-derived fake-ransomware routine that AES-CBC encrypts files, deletes originals, renames output with `.candy`, sets a hard-coded warning image as wallpaper, and does not preserve keys or IVs.
- **Command 12 / `WipeCMain`:** FlockWiper-derived logic reimplemented in Go that wipes the Windows installation drive with multi-pass behavior.
- **Command 19:** clears Windows event logs and attempts to delete `C:\Windows\System32\winevt\Logs\Security.evtx` if `wevtutil` clearing fails.
- **Command 20:** starts a TCP server for VNC-like remote control, including keyboard/mouse control and screen streaming, and creates firewall rules that impersonate legitimate Windows firewall rule names.

## Indicators
### Network
- `185.182.193[.]21` — GigaWiper C2
- `212.8.248[.]104` — GigaWiper C2

### Hashes reported by Microsoft
- `633d4cbd496b1094495da89a64f5e6c31a0f6d4d1488411db5b0cba1cfe42001` — GigaWiper backdoor
- `ce9ad5f6c12019f4aae5b189bd8ddf5bb09e75b06a0a587b25a855c65948c913` — GigaWiper backdoor
- `f622ed85ef31ad4ab973f4e74524866fe1bb44f0965ad2b2ad796cd657a05bfd` — GigaWiper backdoor
- `9706a192e2c1a1faaf0a521daf31c2af60ff4590e3f47bbb4abc227f42af0683` — GigaWiper backdoor
- `3c30deb6556a94cfb84ae51798f4aecfae8c7358e55fdb321c5f2376579631cd` — GigaWiper standalone wiper
- `440b5385d3838e3f6bc21220caa83b65cd5f3618daea676f271c3671650ce9a3` — Crucio
- `12c39f052f030a77c0cd531df86ad3477f46d1287b8b98b625d1dcf89385d721` — FlockWiper
- `db41e0da7ab3305be8d9720769c6950b4dc1c1984ef857d3310eb873a0fc7674` — FlockWiper

### Host artifacts
- Registry key: `HKCU\SOFTWARE\OneDrive\Environment`
- Scheduled task: `OneDrive Update`
- Encrypted-file extension: `.candy`
- Log path targeted for deletion: `C:\Windows\System32\winevt\Logs\Security.evtx`
- FlockWiper PDB paths reported by Microsoft: `A:\GRAT\CWipeNew\Release\CWipeNew.pdb`, `E:\files\new\GRAT\CWipe\Release\CWipe.pdb`

## Defender heuristics
- Treat GigaWiper discovery as an active destructive-intrusion emergency, not just malware cleanup. Isolate affected segments, preserve volatile evidence where safe, and prioritize domain, backup, hypervisor, and EDR control planes.
- Alert on scheduled-task creation named `OneDrive Update` from unusual binaries, especially alongside `HKCU\SOFTWARE\OneDrive\Environment` writes.
- Hunt for RabbitMQ/AMQP or Redis traffic from endpoints and servers that do not normally speak those protocols, particularly to the reported C2 IPs and ports `5544` / `7542`.
- Monitor for destructive sequences involving WMI physical-disk enumeration, `DeviceIoControl` disk operations, boot-file permission changes, event-log clearing, and forced reboot.
- Investigate `.candy` file creation as destructive encryption even if no ransom note exists; Microsoft reports the keys are not saved.
- Build detections around event-log clearing plus fallback deletion of `Security.evtx`, firewall-rule creation for an unknown binary, and sudden VNC-like inbound service exposure.
- Because Microsoft describes GigaWiper as a consolidated platform, hunt for related Crucio, FlockWiper, and `GRAT` artifacts during scoping.

## Related pages
- [The Gentlemen ransomware](the-gentlemen-ransomware.md)
- [GodDamn ransomware PoisonX BYOVD activity](../ops/goddamn-ransomware-poisonx-byovd.md)
- [Ababil of Minab MOIS-linked recovery-destruction campaign](../ops/ababil-of-minab-mois-recovery-destruction.md)

## Sources
- Microsoft Security Blog: [https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/)
