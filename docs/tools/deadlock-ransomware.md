# DeadLock ransomware

## Summary
**DeadLock** is a Rust-based, double-extortion ransomware operation that Microsoft Threat Intelligence first observed in July 2025. As of July 2026, its leak site listed more than 80 claimed victims, over half in Europe. Microsoft observed impact across IT, mining, transportation and logistics, manufacturing, healthcare, real estate, and professional services.

The distinctive defender signal is its decentralized recovery stack. A self-contained HTML ransom application reads mutable proxy and blog data from Polygon smart contracts, uses the Session network for encrypted victim-operator chat, and can browse stolen files hosted in Wasabi object storage. The design is more resilient than a conventional leak site, but it still depends on public Polygon RPC services, an off-chain chat proxy, Session nodes, CDNs, and Wasabi storage.

## Tags
- tools
- malware
- ransomware
- DeadLock
- double extortion
- Rust malware
- Windows
- data theft
- data leak site
- recovery denial
- defense evasion
- event log clearing
- process termination
- service impairment
- Polygon
- blockchain C2
- smart contracts
- Session
- onion routing
- Wasabi
- XChaCha20
- Curve25519
- Microsoft Threat Intelligence

## Why this matters
- DeadLock combines sound per-file encryption with selective large-file encryption, recovery impairment, security-service termination, and broad event-log destruction.
- Its resource-aware dispatch throttles new encryption work when memory use exceeds 29% or CPU load exceeds 70%, helping the host remain responsive and potentially reducing obvious resource spikes.
- The recovery application can change its proxy destination through on-chain configuration without changing the victim-facing HTML file.
- More than 80 leak-site claims indicate an established operation, but claims are not independently verified victim counts.
- The recovery stack is decentralized, not infrastructure-free. Defenders and disruption partners still have observable RPC, proxy, messaging, CDN, and object-storage dependencies.

## Pre-encryption behavior
The analyzed sample decrypts an embedded configuration with an eight-byte XOR key and checks the default and UI languages before encryption. Microsoft documented exclusions for Russian, Ukrainian, Belarusian, Tajik, Persian, Armenian, Azeri, Georgian, Kazakh, Kyrgyz, Turkmen, Syriac, Romanian (Moldova), Uzbek, and Arabic locales associated with Oman and Yemen. A match causes self-deletion without encryption. Geofencing is an operational clue, not a reliable attribution by itself.

When no target path is supplied and the process lacks elevation, the sample generates a random eight-uppercase-character `.cmd` file and requests `RunAs` elevation up to ten times. Microsoft's analyzed sample did not successfully relaunch, so complete preparation appears to require an already elevated context. Supplying a target path bypasses preparation and starts encryption on accessible files.

With administrator rights, DeadLock enables `SeDebugPrivilege`, `SeRestorePrivilege`, `SeBackupPrivilege`, `SeTakeOwnershipPrivilege`, `SeAuditPrivilege`, and `SeSecurityPrivilege`. It then:

- empties recycle bins;
- disables and stops services including `windefend`, `vss`, `swprv`, `wbengine`, `vmcompute`, `vmms`, `adws`, `ntds`, and `kdc`;
- terminates security, backup, cloud-sync, remote-access, shell, and indexing processes;
- clears named classic Windows event logs;
- sets every channel under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WINEVT\Channels` to `Enabled=0` and replaces `ChannelAccess`;
- enumerates and clears registered channels through `wevtapi.dll`, including third-party and custom logs.

This sequence means responders should assume backup, Active Directory, Hyper-V, endpoint visibility, and forensic logging may have been impaired before the first encrypted file is noticed.

## Encryption design
DeadLock renames files to `<filename>.<UID>.dlock` and uses a distinct key set for each file:

- XChaCha20 encrypts file content;
- a random ephemeral Curve25519 keypair derives a per-file shared secret;
- NaCl `crypto_box` using XSalsa20-Poly1305 wraps the content key and nonce;
- Windows CryptoAPI supplies random material;
- a structured footer stores the ephemeral public key, wrapped metadata, format markers, and chunk parameters.

Microsoft assessed the cryptographic construction as sound and found no practical decryption path without the operator private key. The sample encrypts smaller files fully and uses percentage-based or interval-based 512-byte block encryption for larger files, including a special mode above roughly 1 GB. Partial encryption renders large databases, virtual disks, and backups unusable while reducing time and I/O.

## Post-encryption artifacts
- `C:\ProgramData\<UID>.ico` and `HKLM\SOFTWARE\Classes\.dlock\DefaultIcon` brand encrypted files.
- `C:\ProgramData\<UID>.bmp` is set as the desktop wallpaper through `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Wallpaper`.
- `HOW_RECOVER.<UID>.txt` is written to encrypted directories during a second traversal pass.
- `RECOVERY_CHAT.<UID>.html` is written to drive roots and Desktop folders.
- A looping batch file deletes the encryptor and then itself.

The delayed text-note behavior matters in laboratories and early containment: a host can already be encrypting even if `HOW_RECOVER.*.txt` has not appeared.

## Decentralized recovery architecture

### Polygon configuration and blog storage
The HTML application performs read-only `eth_call` requests against public Polygon RPC endpoints. Microsoft identified:

- chat-proxy contract `0x8EF7c3e531d871D3B9D559722DE77EB1dEc19dAe`, selector `0x933a9ce8`;
- blog contract `0x757984507c82c8dA1d3969c535dB5706eEE6426C`, selector `0xd4070542`.

The page rotates across `polygon-bor-rpc.publicnode[.]com`, `polygon.drpc[.]org`, `polygon-pokt.nodies[.]app`, `polygon-rpc[.]com`, `1rpc[.]io/matic`, and `polygon.meowrpc[.]com`. The actor can update the chat proxy on-chain, while the blog contract returns paginated posts and attachment metadata.

### Session chat
The current proxy relays onion-wrapped requests between the browser and the Session swarm network. Victim credentials deterministically derive the Session identity and keypair; messages are signed with Ed25519 and sealed to Curve25519 recipient keys. This removes account registration and reduces dependence on a single messaging server, while preserving a detectable custom proxy dependency.

### Wasabi-hosted stolen data
The HTML app contains an S3-compatible browser that parses Wasabi credentials from supplied URIs, signs AWS4-HMAC-SHA256 requests, lists bucket contents, and generates presigned downloads. This allows browsable leak hosting without a conventional attacker-operated file server. It also creates response opportunities around exposed Wasabi credentials, bucket access logs, object takedown, and presigned-URL telemetry.

## Indicators
- `a1fdf65020ce4a0f0940c793c6425baf8a0b994ec48b9baaf72788661a9d29f4` — SHA-256, analyzed DeadLock encryptor
- `deadlock.liveblog365[.]com` — reported leak-site domain
- `dlock.liveblog365[.]com` — reported leak-site domain
- `deadblogdbdu5wprek7wa2o4ce7rnt6u6ntqeud3hzjjcveosgpsqqqd[.]onion` — reported leak-site onion service
- `deadlockblog.great-site[.]net` — reported leak-site domain
- `deadlockblog.medianewsonline[.]com` — reported leak-site domain
- `.dlock` — encrypted-file suffix following a victim UID
- `HOW_RECOVER.<UID>.txt` — text ransom note
- `RECOVERY_CHAT.<UID>.html` — interactive recovery application
- `dDlK` — encrypted-footer validation marker

Treat public RPC hosts and legitimate Session or Wasabi services as contextual pivots, not standalone malicious indicators.

## Defender guidance
- Isolate affected hosts while preserving volatile evidence. DeadLock disables logging and self-deletes, so capture memory, process state, service configuration, registry changes, open connections, and the recovery HTML before reboot or cleanup.
- Hunt for broad event-channel disabling, `ChannelAccess` replacement, simultaneous backup/AD/Hyper-V/security service stops, recycle-bin emptying, suspicious wallpaper changes, and `.dlock` renames.
- Alert when an unknown local HTML file makes Polygon RPC calls, invokes the two contracts/selectors, contacts a newly resolved proxy, emits Session-style onion requests, or signs S3-compatible requests to Wasabi.
- Block or monitor the identified contract calls and custom proxy at controlled egress points, while avoiding indiscriminate blocking of legitimate Polygon, Session, or Wasabi use.
- Maintain immutable, offline, separately credentialed backups and test restoration. DeadLock explicitly targets VSS and backup services and terminates cloud-sync clients.
- Use EDR tamper protection, EDR block mode, controlled folder access, and application controls. Validate visibility when Windows event channels are disabled rather than assuming absence of logs means absence of activity.
- If encryption is confirmed, investigate prior data staging and exfiltration and rotate credentials exposed on affected hosts. Double extortion means restoration alone does not close the incident.

Microsoft Defender identifies samples as `Ransom:Win32/Deadlock.*` and publishes DeadLock-specific prevention and detection alerts.

## Related pages
- [The Gentlemen ransomware](the-gentlemen-ransomware.md)
- [GigaWiper](gigawiper.md)
- [GodDamn ransomware PoisonX BYOVD activity](../ops/goddamn-ransomware-poisonx-byovd.md)
- [Cloud logging control-plane tampering](../patterns/cloud-logging-control-plane-tampering.md)

## Sources
- Microsoft Threat Intelligence: [https://www.microsoft.com/en-us/security/blog/2026/08/10/deadlock-ransomware-breaking-down-a-rust-based-encryptor-with-decentralized-recovery-infrastructure/](https://www.microsoft.com/en-us/security/blog/2026/08/10/deadlock-ransomware-breaking-down-a-rust-based-encryptor-with-decentralized-recovery-infrastructure/)
