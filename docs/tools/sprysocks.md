# SprySOCKS

## Summary
**SprySOCKS** is a FishMonger backdoor family. ESET's June 2026 analysis expanded it from a previously Linux-only tool into two Windows variants, internally marked `WIN_DRV` and `WIN_PLUS`, attributed to FishMonger with high confidence.

ESET telemetry showed real activity during 2023-2024 against mostly government organizations in Honduras, Taiwan, Thailand, and Pakistan. The durable defender lesson is that SprySOCKS is not just a user-mode RAT: the `WIN_DRV` branch weaponizes kernel drivers to hide processes, files, registry keys, and network connections, and to divert TCP traffic to a hidden local listener.

## Tags
- tools
- malware
- backdoor
- RAT
- SprySOCKS
- FishMonger
- Winnti Group
- I-SOON
- Earth Lusca
- TAG-22
- Aquatic Panda
- Red Dev 10
- China-linked
- espionage
- kernel driver
- driver loading
- DLL side-loading
- process doppelgänging
- TCP traffic diversion
- WebSocket C2
- UDP C2
- government targeting
- Honduras
- Taiwan
- Thailand
- Pakistan
- CVE-2023-24932

## Why this matters
- SprySOCKS now has public Windows coverage in addition to its earlier Linux reporting, so Windows government fleets should not treat the family as Linux-only.
- `WIN_DRV` uses kernel-mode components to hide host and network artifacts, which weakens ordinary user-mode EDR and simple netstat-style checks.
- The traffic-diversion design allows operators to send commands through an arbitrary victim TCP port without exposing the backdoor's real listening port in network telemetry.
- ESET saw limited indicators of a possible UEFI bootkit component in some scenarios; keep that caveated, but preserve firmware and boot evidence when SprySOCKS is suspected.

## Windows variants
### `WIN_PLUS`
- Hardcoded C2 configuration.
- TCP, UDP, and WebSocket communications.
- More than 30 C2 commands covering host discovery, process enumeration, service management, file listing, file creation, deletion, upload/download, and command execution.
- ESET lists `207.148.78[.]36` as a hardcoded C2 IP for the `WIN_PLUS` variant.

### `WIN_DRV`
- Shares the core backdoor functionality with `WIN_PLUS`.
- Adds driver-based hiding for malware network connections, processes, files, and registry keys.
- Loads a kernel driver through a transient `msidiskserver` minifilter service key and a dropped driver path such as `C:\Windows\System32\drivers\fsdiskbit.sys`.
- Decrypts additional payload material from `%SystemRoot%\Fonts\` containers, including `X1B5206BDC1743DD.dat`, `KX1B5206BDC1743DD.dat`, and `KW1B5206BDC1743FP.dat`.
- Uses 128-bit AES-ECB with the key `uXQLESMXGaRMs6BL` for parts of the documented loader chain.
- Injects backdoor shellcode into a spawned `svchost.exe` via process doppelgänging after obtaining a token from `spoolsv.exe`.

## Attack-chain notes
1. Delivery includes legitimate-looking files for DLL side-loading plus encrypted `.dat` containers.
2. The loader persists execution and restarts from `%SystemRoot%\Fonts\`.
3. The `WIN_DRV` loader decrypts and drops DriverLoader as `fsdiskbit.sys`, creates the `msidiskserver` minifilter service key, invokes `NtLoadDriver`, then attempts to delete the service key and driver file.
4. DriverLoader decrypts and manually maps another driver from `C:\Windows\Fonts\KW1B5206BDC1743FP.dat`.
5. The resulting driver layer supports hiding and TCP traffic diversion to the backdoor's hidden listener.

## Defender heuristics
- Hunt for suspicious executable content and encrypted-looking `.dat` files under `%SystemRoot%\Fonts\`, especially names matching `*1B5206BDC1743*`.
- Alert on creation of `C:\Windows\System32\drivers\fsdiskbit.sys` or a `msidiskserver` service/minifilter registry key.
- Review transient driver loads followed by rapid service-key and file deletion.
- Correlate `spoolsv.exe` token use, suspicious `svchost.exe` child creation, and process doppelgänging artifacts.
- Treat inbound random TCP ports that forward to hidden local listeners as suspicious when paired with driver anomalies.
- Inspect kernel-driver signatures for leaked, unexpected, or GitHub-sourced test certificates, especially on systems with weak driver-signature enforcement.
- When SprySOCKS is suspected, collect volatile memory, driver-load telemetry, registry transaction evidence, and boot/firmware state before wiping.

## Public indicators highlighted by ESET
- **C2:** `207.148.78[.]36` (`WIN_PLUS` hardcoded C2 IP).
- **Driver path:** `C:\Windows\System32\drivers\fsdiskbit.sys`.
- **Service key:** `msidiskserver`.
- **Fonts-directory containers:** `%SystemRoot%\Fonts\X1B5206BDC1743DD.dat`, `%SystemRoot%\Fonts\KX1B5206BDC1743DD.dat`, `%SystemRoot%\Fonts\KW1B5206BDC1743FP.dat`.
- **AES key:** `uXQLESMXGaRMs6BL`.
- **Possible firmware angle:** limited ESET telemetry suggesting some scenarios may involve a UEFI bootkit component possibly exploiting CVE-2023-24932.

Use ESET's IOC table as the canonical hash and sample source rather than copying hash lists by hand.

## Related pages
- [FishMonger](../actors/fishmonger.md)
- [RemotePE](remotepe.md)
- [The Gentlemen ransomware](the-gentlemen-ransomware.md)

## Sources
- ESET WeLiveSecurity: <https://www.welivesecurity.com/en/eset-research/fishmongers-arsenal-upgraded-sprysocks-windows/>
