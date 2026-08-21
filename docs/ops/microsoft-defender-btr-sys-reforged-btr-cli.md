# BTR Reforged: weaponizing Microsoft Defender's BTR.sys remediation driver as a kernel primitive

## Summary
Check Point Research (Jiří Vinopal) published **"BTR Reforged: Weaponizing Defender's Remediation Driver as a Kernel Operation Primitive"** on **August 20, 2026**, alongside a proof-of-concept tool, **BTR_CLI**. The work is the first full reverse engineering of the **Windows Defender Boot-Time Removal driver, `BTR.sys`** — a legitimate, Microsoft-signed, required Windows component used to finish removing malware after a reboot by deleting locked files and registry entries. The disclosure shows that `BTR.sys` can be repurposed into a **universal, attacker-controlled kernel (Ring 0) operation engine** that performs **arbitrary file and registry operations** on Windows 7 through Windows 11 25H2 — **without exploiting any software flaw, memory corruption, or external driver import**. No evidence of real-world abuse was found as of the report.

## Tags
- ops
- operations
- BTR.sys
- BTR Reforged
- BTR_CLI
- Microsoft Defender
- Boot Time Removal Tool
- MpEngine.dll
- kernel driver
- Ring 0
- arbitrary file deletion
- registry manipulation
- EDR/AV bypass
- RC4 encryption
- Alternate Data Stream
- ADS
- Boot Bus Extender
- BYOVD alternative
- Check Point Research
- Jiří Vinopal
- trusted-component weaponization
- EDR/AV tampering

## What the driver is
- **`BTR.sys`** (Boot Time Removal Tool) is a **required Windows component**, embedded in Defender's `MpEngine.dll` as the `BOOTTIMETOOL` resource.
- It runs at boot (System Start, `Group = Boot Bus Extender`) to delete files/registry entries that were locked while the system was running, completing a prior malware removal.
- Because it is a required Windows component, it **cannot be added to Microsoft's Vulnerable Driver Blocklist or blocked via WDAC** without disrupting Defender itself.
- It is deployed as a **randomized-filename driver** under `System32\drivers` with a **randomized transient service name** (e.g. `HKLM\SYSTEM\CurrentControlSet\Services\mzqnjtaq`), which — in legitimate use — already resembles malicious kernel-loader tradecraft.

## The abuse primitive
- **No vulnerability required.** The driver is instructed to perform arbitrary file/registry operations; there is no exploit, no memory corruption, and no driver imported from outside the machine.
- **Encryption:** the configuration blob is RC4-encrypted with a **hard-coded 256-byte key in the `.rdata` section** of the driver, verified unchanged across the unique 64-bit `BTR.sys` builds (12 `MpEngine.dll` versions → 5 unique `BTR.sys` SHA-256 builds, combined with VirusTotal samples → 18 unique 64-bit builds analyzed, all carrying the same key).
- **Integrity:** a **modified CRC-32 (`~CRC32`)** using the standard polynomial `0xEDB88320` and init `0xFFFFFFFF`, deviating by omitting the final bitwise NOT.
- **Configuration carrier:** an **Alternate Data Stream** (the driver file's `:changelist` stream) holds the encrypted configuration; `Args` points at `<driver>.sys:changelist`.
- **BTR_CLI** locates `MpEngine.dll` under Defender's Definition Updates, extracts the embedded `BTR.sys`, constructs a valid encrypted transaction, and installs the driver as a service via direct HKLM writes (`Type=1`, `Start=1`, `Group="Boot Bus Extender"`) — bypassing the Service Control Manager path.

## Detection and mitigation posture
- **Signature-based blocking is ineffective** — `BTR.sys` is a legitimate Microsoft-signed component.
- A well-crafted weaponization tool deliberately **mimics the operational footprint of legitimate Defender remediation** (randomized driver filename + service, boot-time ADS config, RC4 routines, self-cleanup), so detection must rely on **behavioral/telemetry analysis** (the report uses Sysmon telemetry).
- **WDAC / Vulnerable Driver Blocklist** do **not** help, because blocking the required component breaks Defender.
- The report frames this as a **BYOVD-alternative EDR/AV bypass**: disarm security solutions using a trusted, built-in, Microsoft-signed driver.

## Defender priorities
1. **Alert on Defender-remediation-shaped driver activity at boot:** a randomized-filename `.sys` under `System32\drivers` with a transient randomized service, `Start=1`, `Group=Boot Bus Extender`, and an `:changelist` ADS stream, created shortly before a reboot and self-cleaning after execution. This is the native footprint of legitimate remediation *and* of BTR_CLI-style weaponization — correlate with actual prior Defender remediation events to separate legitimate from malicious.
2. **Hunt for RC4 + ADS + randomized-service triads** in kernel-driver telemetry; the combination of a boot driver, an ADS-stored encrypted config, and a randomized transient service is unusual enough to alert on.
3. **Do not assume "up to date" Defender is safe from LPE** — this is the same threat model as the [RoguePlanet / ShieldBreak (CVE-2026-50656)](microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md) bypass: Defender's own components are the attack surface.
4. **Watch for real-world adoption.** No in-the-wild abuse was observed; Check Point Research states the technique is "currently unknown or unused by threat actors," making proactive detection engineering feasible before weaponization appears. Track researcher follow-ups, threat-actor tooling, and IR cases for BTR.sys-style kernel operations.
5. **Inventory Defender engine/driver versions** and the `MpEngine.dll` `BOOTTIMETOOL` resource to anchor the RC4-key and `~CRC32` details for signature/threat-hunting development.

## Assessment limits
- Research disclosure (Check Point Research, August 20, 2026) with a public PoC (BTR_CLI) and detection guidance; **no in-the-wild exploitation is documented**.
- The "18 unique 64-bit builds, unchanged RC4 key" figure is Check Point's own analysis; treat it as their finding, not independently verified.
- No CVE is assigned (no software flaw is exploited — this is abuse of a trusted component, not a vulnerability).

## Related pages
- [Microsoft Defender CVE-2026-50656 RoguePlanet / ShieldBreak patch bypass](microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md)
- [RedC2 4.0 (RedShell Linux beacon) and the trojanized-npm delivery wave](../tools/redc2.md)

## Sources
- Check Point Research: [BTR Reforged: Weaponizing Defender's Remediation Driver as a Kernel Operation Primitive](https://research.checkpoint.com/2026/btr-reforged-weaponizing-defenders-remediation-driver-as-a-kernel-operation-primitive/) — August 20, 2026
- The Hacker News: [Microsoft Defender's Own Driver Can Be Weaponized to Delete Security Software at Boot](https://thehackernews.com/2026/08/microsoft-defenders-own-driver-can-be.html) — August 21, 2026
