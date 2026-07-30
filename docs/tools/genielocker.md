# GenieLocker

## Summary
**GenieLocker** is custom Toy Ghouls ransomware active since March 2026. Kaspersky recovered Windows PE and Linux/VMware ESXi ELF variants. Both use libsodium and a common authenticated-encryption design, while the platform-specific builds differ in anti-analysis and operational controls.

## Tags
- tools
- malware
- GenieLocker
- ransomware
- Toy Ghouls
- Windows
- Linux
- VMware ESXi
- XChaCha20-Poly1305
- Curve25519-XSalsa20-Poly1305
- libsodium
- partial encryption
- debugger evasion
- process termination
- service stop
- backup disruption
- virtualization targeting

## Capability profile
- Encrypts with per-file XChaCha20-Poly1305 keys and nonces; encrypts metadata separately and wraps file keys using Curve25519-XSalsa20-Poly1305.
- Supports partial, randomly selected chunk encryption but always damages the first chunk.
- The Windows build requires a secret argument, repeatedly checks for debugging and `.text` modification, stops processes and services, and traverses local and network drives.
- The ELF build defaults to ESXi datastores, can daemonize, delay execution, choose worker counts, and modify the ESXi welcome message. In the reported intrusion, operators stopped active virtual machines before using the build to encrypt their disks.
- Does not drop ransom notes or contain negotiation addresses; operator contact is handled outside the binary.

## Detection pivots
- `VCJOURN` in sidecar journal files.
- `.lock` and `.journal` files adjacent to rapidly rewritten data; one observed encrypted extension was `.03ffc1c4a3da0f02`.
- Windows MD5 `5D62C1349B8981C396C9A23F4F8F053C` and Linux/ESXi MD5 `9201E35E2993612612919A3C71302CAB` for exact analyzed samples.
- Unexpected VM stops, high-volume writes under `/vmfs/volumes`, and changes to `/etc/vmware/welcome`.
- Coordinated termination of VSS, backup, database, Exchange, and virtualization workloads before file encryption.

## Related pages
- [Toy Ghouls GenieLocker ransomware activity](../ops/toy-ghouls-genielocker-ransomware.md)
- [Toy Ghouls](../actors/toy-ghouls.md)

## Sources
- Kaspersky: [Toy Ghouls’ new toy: the GenieLocker ransomware](https://securelist.com/genielocker-ransomware-for-windows-linux-and-esxi/120843/)
