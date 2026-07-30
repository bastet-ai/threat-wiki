# Toy Ghouls GenieLocker ransomware activity

## Summary
Kaspersky disclosed **GenieLocker** on July 30, 2026, a custom ransomware family used by **Toy Ghouls** since March 2026 against organizations in the Russian Federation. Separate PE and ELF builds target Windows, Linux, and VMware ESXi while sharing a libsodium-based cryptographic design.

A March intrusion entered through an external partner's OpenVPN connection with stolen valid credentials. The operators performed discovery and credential access, moved over RDP and SSH, distributed the encryptor with PsExec and PAExec, stopped virtual machines, and encrypted Windows endpoints plus Linux and ESXi storage. Kaspersky found no evidence of exfiltration in that case.

## Tags
- ops
- campaign
- Toy Ghouls
- Bearlyfy
- Labubu
- Laboo.boo
- GenieLocker
- ransomware
- extortion
- Russia targeting
- manufacturing
- construction
- financial services
- retail
- technology sector
- Windows
- Linux
- VMware ESXi
- OpenVPN
- trusted relationship abuse
- valid accounts
- Mimikatz
- KeePassXC
- SoftPerfect Network Scanner
- PsExec
- PAExec
- RDP
- SSH
- reverse SSH tunneling
- backup disruption
- virtualization targeting

## Reported intrusion chain
1. **Initial access:** OpenVPN traffic originated from an external partner's network using stolen, still-valid credentials. Kaspersky assesses abuse of the trusted relationship as likely.
2. **Discovery and credentials:** Operators installed OpenSSH, `socks5.exe`, SoftPerfect Network Scanner, and Mimikatz. Forensics showed access to installed KeePassXC password managers, likely to reach stored databases.
3. **Movement and control:** RDP reached Windows hosts, SSH reached Linux systems, and a reverse SSH tunnel connected to `89[.]125.66.101`.
4. **Deployment:** PsExec and PAExec distributed GenieLocker broadly.
5. **Impact:** The PE build encrypted Windows systems. The ELF build stopped active ESXi virtual machines and encrypted their disks, and could also run on Linux.

## GenieLocker behavior
### Windows
- Requires a secret hex argument whose SHA-256 must match a hard-coded value, limiting unauthorized or sandbox execution.
- Checks `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, known debugger artifacts, and changes to the `.text` section CRC32 every 500 milliseconds.
- Excludes system directories, files, and extensions, then terminates database, productivity, virtualization, and other processes and stops services matching backup, VSS, SQL, Exchange, Sophos, Veeam, and VM workloads.
- Enumerates local and network drives and supports partial encryption through a percentage argument.
- Creates `.lock` and `.journal` sidecars and appends a campaign-specific extension; Kaspersky's analyzed sample used `.03ffc1c4a3da0f02`.

### Linux and ESXi
- Defaults to `/vmfs/volumes`, supports delayed start, worker-count selection, recursive traversal, logging, and double-fork daemonization. In the reported intrusion, operators stopped active virtual machines before encrypting their disks.
- Can modify `/etc/vmware/welcome`; the analyzed sample left the message blank.
- Lacks the Windows build's secret argument, debugger checks, and exclusion lists.
- Its command-line presentation resembles LockBit, consistent with a custom replacement for the third-party encryptors Toy Ghouls previously used.

### Cryptography
Both builds use XChaCha20-Poly1305 for file contents and metadata, with a unique key and nonce per file. Curve25519-XSalsa20-Poly1305 protects each file key with an embedded attacker public key. Partial encryption uses random chunks but always encrypts the first chunk. The Windows default chunk size is `0x1000000`; Linux/ESXi uses `0x400000`.

GenieLocker does not create ransom notes or embed operator contact details. Kaspersky assesses that demands are delivered manually, potentially avoiding detections based on mass note creation.

## Public indicators
### C2
- `89[.]125.66.101`

### Representative MD5 hashes
Kaspersky published a larger canonical set; these identify the analyzed builds:
- Windows: `5D62C1349B8981C396C9A23F4F8F053C`
- Linux/ESXi (`vzdump`): `9201E35E2993612612919A3C71302CAB`

### Host artifacts
- Encrypted extension observed: `.03ffc1c4a3da0f02`
- Sidecars: `<filename>.<extension>.lock` and `<fileext>.<extension>.journal`
- Journal marker: `VCJOURN`
- ESXi target path: `/vmfs/volumes`
- ESXi welcome path: `/etc/vmware/welcome`

## Detection and response
- Hunt for partner-origin VPN sessions followed by SoftPerfect scanning, Mimikatz, KeePassXC process or database access, RDP/SSH fan-out, PsExec/PAExec, and reverse SSH tunnels.
- Alert on mass process termination and service stops involving VSS, Veeam, SQL, Exchange, Hyper-V/VM services, and backup products, especially immediately before broad file writes.
- On ESXi, monitor unexpected VM stop operations, execution from datastore paths, changes to `/etc/vmware/welcome`, new daemonized ELF processes, and high-volume writes under `/vmfs/volumes`.
- Detect the `VCJOURN` marker, campaign-extension sidecars, and large parallel file rewrites; do not depend on ransom-note creation.
- Disable the compromised VPN path, preserve identity, VPN, endpoint, hypervisor, and network evidence, revoke partner and discovered credentials, and scope password-manager exposure.
- Rebuild affected systems from known-good media and restore from offline or immutable backups only after the access path, tunnels, and stolen identities are removed.

## Evidence caveats
- Kaspersky says open-source intelligence attributes GenieLocker activity to Toy Ghouls and that the observed TTPs match earlier group activity.
- The analyzed incident supports partner-credential and VPN abuse; it does not establish compromise of the partner's software or a product supply chain.
- Kaspersky found no exfiltration evidence and describes Toy Ghouls as not using double extortion, but defenders should still test for collection and outbound transfer before declaring data unaffected.
- MD5 values are useful for exact-sample matching but insufficient against rebuilt variants; prioritize behavior and access-path telemetry.

## Related pages
- [Toy Ghouls](../actors/toy-ghouls.md)
- [GenieLocker](../tools/genielocker.md)

## Sources
- Kaspersky, July 30, 2026: [Toy Ghouls’ new toy: the GenieLocker ransomware](https://securelist.com/genielocker-ransomware-for-windows-linux-and-esxi/120843/)
