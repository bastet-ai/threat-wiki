# SPECTRE (cross-platform C backdoor) and the Specter Linux rootkit

## Summary
**SPECTRE** is a new cross-platform backdoor written in C, tracked by Cisco Talos in the activity of **[UAT-10147](../actors/uat-10147.md)**. It pairs a Windows variant with a Linux variant, and its most consequential capability is the **Specter** kernel rootkit, which the Linux SPECTRE binary loads to blind user-level security tooling. Talos named the implant after a debug log recovered from a sample whose header explicitly read "SPECTRE." The implant is significant because it combines cross-platform C2, three injection modalities, credential theft, weighted anti-analysis scoring, and **BYOVD kernel R/W used to unlink EDR kernel callbacks** — a "bring your own vulnerable driver" kill-switch for kernel-callback-based EDR on Windows. Talos assessed with medium confidence that portions of the Specter rootkit (and the custom-compiled Potato tools) were developed with **AI-assisted code generation**.

## Tags
- tools
- malware
- backdoor
- C2
- SPECTRE
- Specter
- rootkit
- Linux rootkit
- ftrace
- IPMODIFY
- BYOVD
- kernel R/W
- EDR bypass
- UAT-10147
- Chinese-speaking
- cybercrime
- cross-platform
- C backdoor
- process hollowing
- APC EarlyBird
- timestomping
- anti-sandbox
- xorshift32
- PEB hash
- NTFS ADS
- IIS
- BadIIS
- SEO fraud
- Potato
- EfsPotato

## Windows variant
- **Language / anti-static:** C, API resolved entirely at runtime via PEB hash walking (DJB2 variant); sensitive literals encrypted at compile time with a per-string **xorshift32 PRNG**, decrypted into thread-local storage just before use and never held plaintext in `.text` / `.rdata`. Static detection is largely ineffective.
- **Anti-analysis:** a weighted scoring routine checks process-name blocklists, RAM, CPU core count, disk space, sleep acceleration, and common sandbox hostnames/usernames; if the cumulative score is **>= 50** points the process self-terminates.
- **C2:** a fallback C2 domain is hardcoded in the binary and recoverable through string decryption. All C2 traffic is **HTTP POST to `/api/v1/register` and `/api/v1/output`**. A specific version also read its C2 configuration from an **NTFS Alternate Data Stream at `C:\Windows\System32\drivers\etc\hosts:cache`**, so the operator can update C2 config by writing the ADS without recompiling (bypasses static firewall blocklists).
- **Commands (45 total; 24 plaintext, 21 encrypted with the xorshift PRNG):** standard shell / file / process ops plus three grouped capability sets:
  - **Process injection** — process hollowing (default target `svchost.exe`), APC **EarlyBird** injection, and an automated on-startup **self-hollow** of `RuntimeBroker.exe` executed straight from `main()` to conceal the implant.
  - **Privilege escalation / credential theft** — named-pipe impersonation to SYSTEM (`\\.\pipe\spectre_<tid>` via `ImpersonateNamedPipeClient`), `RegSaveKeyA` hive dumps of SAM/SYSTEM/SECURITY to `%TEMP%` for offline `secretsdump.py` NT-hash extraction; **Vaultdump** (`cmdkey.exe /list` without LSASS access) and **Chromedump** (copies Chrome/Edge `Login Data` + `Local State` for offline DPAPI/SharpChrome).
  - **BYOVD EDR killer** — downloads a known-vulnerable driver (`RTCore64.sys` / CVE-2019-16098 MSI, or `DBUtil_2_3.sys` / CVE-2021-21551 Dell), installs it as a transient kernel service, and uses kernel R/W plus a hardcoded per-build offset table (13 Windows versions) to unlink `PspCreateProcessNotifyRoutine`, `PspCreateThreadNotifyRoutine`, and `PspLoadImageNotifyRoutine` callbacks — blinding CrowdStrike Falcon, SentinelOne, Microsoft Defender, and similar EDR for the session.

## Linux variant
- Statically linked **ELF x86-64**. On start it runs an eight-factor anti-sandbox scoring engine; at **>= 50** points it exits silently with no observable indicators, then beacons to the hardcoded C2 with a JSON payload.
- **29 commands, none encrypted.** File/process recon, agent management, unrestricted shell, `timestomp` (anti-forensics via `utimensat()`), and the `rootkit_*` command family that drives Specter.

## Specter Linux rootkit
- Deployed as a loadable kernel module **disguised as `acpi_pad.ko`** (mimics the legitimate ACPI power-management module).
- **Persistence:** a fraudulent systemd unit `hardware-monitor.service` ("Hardware Performance Monitor") with **`Before=sysinit.target`**, so it runs at boot before security tooling initializes.
- **Hooking:** instead of patching the syscall table it uses the kernel's native **ftrace** framework with **`FTRACE_OPS_FL_IPMODIFY`** to redirect entry points of six handlers — `hooked_tcp6_seq_show`, `hooked_tcp4_seq_show`, `hooked_tkill`, `hooked_tgkill`, `hooked_kill`, `hooked_getdents64`. Because ftrace is a legitimate debug interface, kernel-integrity checks are minimally noisy.
- **IPC:** user space talks to the module via `kill()` to a **magic PID `0x7A69` (31337)** with real-time signals — signal **62** hides a process from `/proc`, **36** hides the module from `lsmod` (unlinks `THIS_MODULE`), **37** escalates the implant to UID 0 by overwriting the cred struct, **35** is the load-ack handshake.
- **AI-assisted development signals (Talos, medium confidence):** a "product spec"-style feature list at the top of the source (reads like a response to "Write a rootkit with the following features"), rigid uniform decorative separators across 10+ sections, a pedagogical tone explaining basic concepts to oneself, and three explicitly labeled "Method 1/2/3" alternatives — an AI completeness reflex.

## Related campaign tooling
The SPECTRE / Specter implants are delivered inside the broader UAT-10147 web-server campaign (see [campaign page](../ops/uat-10147-spectre-badiis-ai-augmented-web-server-campaign.md)): **BadIIS** MaaS SEO-fraud modules, a C# **ASHX `SeoEngineHandler`** SEO engine (C2 domains on `vn[.]xyz`, targeting the Cốc Cốc crawler), **EfsPotato** / **RustPotato** / **GodPotato** / **JuicyPotato** privilege escalation (custom-compiled EfsPotato/RustPotato PDBs point at `...\Desktop\AI\` build paths), plus commodity **QuasarRAT** (campaign ID contains a derogatory Vietnamese string), **Noodle RAT** (Type `0x03A2` ELF), **Meterpreter**, **Gh0stCringe** (shellcode inside a custom Go loader), and a two-layer **web shell** that authenticates on the `X-ID` HTTP header token `x9` (falling back to a `v` parameter).

## Detection
- **ClamAV signatures:** `Win.Malware.BadIIS-10059985-0`, `Win.Loader.BadiisSet-10060291-1`, `Asp.Rootkit.Badiis-10060290-1`, `Unix.Rootkit.Spectre-10060260-0`, `Unix.Rootkit.Malware-10060258-0`, `Win.Malware.BadPotato-10060230-0`, `Win.Exploit.Marte-10033857-0`, `Win.Tool.GodPotato-10019688-1`, `Win.Tool.juicypotato-10041758-0`, `Unix.Backdoor.Msfvenom-10012672-0`, `Win.Malware.Generic-10060235-0`, `Win.Malware.Generic-10060218-0`, `Win.Malware.Generic-9883082-0`, `Win.Malware.Generic-10060252-0`, `Win.Malware.Generic-10060220-0`, `Win.Malware.Ulise-10056576-0`, `Unix.Trojan.Backdoor-6678692-0`.
- **Snort SIDs:** Snort2 `1:66690`, `1:66688`, `1:66689`; Snort3 `1:66690`, `1:301548`.
- **Hunting pivots:** kernel-callback unlisting on Windows correlated with transient `RTCore64`/`DBUtil` service install (BYOVD); `hosts:cache` NTFS ADS reads/writes; `/api/v1/register` and `/api/v1/output` HTTP POST; a kernel module named `acpi_pad.ko` on systems where ACPI power-management is not the expected user; systemd units ordered `Before=sysinit.target`; `kill()` to PID `31337`; ftrace IPMODIFY hooks on the six named handlers; `utimensat` timestomping; and self-hollow of `RuntimeBroker.exe`.
- **IOC files:** Talos publishes them in the Cisco-Talos/IOCs repository (2026/08): `UAT-10147 deploys SPECTRE.txt` and `UAT-10147 integrates agentic AI.txt`.

## Defender notes
- Treat `acpi_pad.ko` on a host where ACPI thermal management is not operator-controlled as hostile by default; verify module provenance and check for `hardware-monitor.service`.
- Kernel-callback EDR assumes process/thread/image-load notification; a BYOVD unlink removes that for the session. If you rely on kernel-callback EDR, hunt for transient vulnerable-driver service installs and the subsequent loss of callback coverage as a paired signal.
- The NTFS-ADS C2-config channel and the `/api/v1/*` POST beacon are durable, low-noise network/pivot indicators worth alerting on.

## Related pages
- [UAT-10147 SPECTRE / BadIIS / agentic-AI web-server campaign](../ops/uat-10147-spectre-badiis-ai-augmented-web-server-campaign.md)
- [UAT-10147](../actors/uat-10147.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- Cisco Talos: [UAT-10147 deploys SPECTRE: A cross-platform implant with Linux rootkit and BYOVD capabilities](https://blog.talosintelligence.com/uat-10147-deploys-spectre-a-cross-platform-implant-with-linux-rootkit-and-byovd-capabilities/) (Joey Chen, August 20, 2026)
- Cisco Talos: [UAT-10147: Chinese-speaking adversary integrates agentic AI into post-compromise operations](https://blog.talosintelligence.com/uat-10147-chinese-speaking-adversary-integrates-agentic-ai-into-post-compromise-operations/) (Joey Chen, August 20, 2026)
