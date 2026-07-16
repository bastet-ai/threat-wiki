# GodDamn ransomware PoisonX BYOVD activity

## Summary
Broadcom / Symantec reported on July 9, 2026 that **GodDamn ransomware** is the latest rebrand in the **Monster → Beast → GodDamn** ransomware line tracked to developer cluster **Hyadina**. In an early June 2026 intrusion, the operators used AnyDesk remote access, a NirSoft-heavy credential-harvesting toolkit, PsExec lateral movement, and a defense-evasion chain that dropped the **PoisonX** kernel driver as `g11.sys` before ransomware deployment.

The durable signal is the driver and tooling combination. Symantec says PoisonX appears to be a malicious driver whose developers succeeded in getting it signed by Microsoft Windows Hardware Compatibility Publisher, allowing ransomware operators to disable security products at kernel level instead of relying only on known-vulnerable legitimate drivers.

## Tags
- ops
- operations
- ransomware
- GodDamn ransomware
- Beast ransomware
- Monster ransomware
- Hyadina
- PoisonX
- BYOVD
- malicious signed driver
- Microsoft Windows Hardware Compatibility Publisher
- EDR killer
- defense evasion
- AnyDesk
- PsExec
- NirSoft
- Mimikatz
- credential harvesting
- lateral movement
- recovery denial
- Windows
- Broadcom
- Symantec Threat Hunter Team

## Why this matters
- GodDamn is not just a new brand. Symantec found significant code overlap with Beast, tying it to a multi-year ransomware lineage that has repeatedly changed names while preserving tradecraft.
- PoisonX raises the defender priority of signed-driver inventory: the driver behaves like a BYOVD-style EDR killer but appears to be malicious code carrying a Microsoft hardware-compatibility signature.
- The observed intrusion staged credential harvesting and remote-access persistence before encryption, so an encryption event likely means credential theft, lateral movement, and defense impairment already occurred.
- The toolchain overlaps common ransomware affiliate behavior: AnyDesk, PsExec, NirSoft password tools, Mimikatz, network scanning, service installation, reboot orchestration, and delayed encryptor deployment.

## Observed intrusion sequence
1. Symantec observed earliest malicious activity on May 29, 2026, when AnyDesk activity appeared in the target environment. The initial access vector was unknown.
2. On May 30, attackers staged a defense-evasion binary disguised as a Symantec product under `csidl_profile\music\symantec.exe`.
3. That binary dropped the signed **PoisonX** driver to `csidl_system\drivers\g11.sys`.
4. On the same host, attackers staged credential-harvesting tools in a user-profile subdirectory, including NirSoft utilities, Mimikatz, NetScan, and browser / credential-store dumpers.
5. Operators used PsExec for lateral movement, installed AnyDesk on reachable hosts, registered AnyDesk as an auto-start Windows service, killed the running AnyDesk process, waited briefly, and rebooted systems.
6. By the end of June 2, Symantec said the AnyDesk deployment sequence had repeated across at least 10 hosts.
7. On June 3, GodDamn ransomware was detected on a separate network segment associated with a different organizational unit. The encryptor appeared as `encrypter-windows-gui-x86.exe` under user-profile Downloads or Music paths.

## PoisonX and defense evasion
- PoisonX was previously documented by Xcitium as a driver used to disable CrowdStrike Falcon by sending crafted IOCTLs to an undocumented driver interface.
- Symantec says the driver carries a Microsoft Windows Hardware Compatibility Publisher signature and can terminate security-product processes and remove user-mode API hooks, impairing endpoint visibility.
- In the GodDamn intrusion, the defense-evasion dropper hash was `b29f91a440527fb621d106a2048f6379fff3263c60aeda9c82ff8c1d5ae880a8` and the PoisonX `g11.sys` hash was `2d91a78e739891c9854c254f5b2a6b84c0e167dfa253466cbccd2cdd1c20145d`.
- The PoisonX detail also matters for The Gentlemen / GentleKiller coverage: ESET reported PoisonX among drivers abused by The Gentlemen affiliates, showing cross-crew reuse of the same defense-impairment primitive.

## Lineage notes
- **Monster** appeared in March 2022 as a Delphi ransomware family targeting 32-bit Windows and avoiding Commonwealth of Independent States systems.
- **Beast** appeared as a Hyadina rebrand in June 2024, adding broader customization, improved encryption performance, and support for Linux and VMware ESXi targets.
- **GodDamn** appears to be the latest Hyadina iteration. Some attacks use the `.God8Damn` extension, while the Symantec-investigated incident renamed encrypted files with the victim organization's name as the extension.

## Selected file indicators
- `csidl_profile\music\symantec.exe` — defense-evasion dropper masquerading as a Symantec product
- `csidl_system\drivers\g11.sys` — PoisonX driver path
- `csidl_profile\downloads\encrypter-windows-gui-x86.exe` — GodDamn encryptor path
- `csidl_profile\music\encrypter-windows-gui-x86.exe` — alternate GodDamn encryptor path
- `141b2190f51397dbd0dfde0e3904b264c91b6f81febc823ff0c33da980b69944` — PsExec / `psexesvc.exe`
- `17fb52476016677db5a93505c4a1c356984bc1f6a4456870f920ac90a7846180` — NetPass / `netpass64.exe`
- `19bab15a34d5ad838ccf4d187eb40379c335fa56446d0f9621865b2767d4ac7d` — WirelessKeyView / `wirelesskeyview64.exe`
- `2d91a78e739891c9854c254f5b2a6b84c0e167dfa253466cbccd2cdd1c20145d` — PoisonX / `g11.sys`
- `31eb1de7e840a342fd468e558e5ab627bcb4c542a8fe01aec4d5ba01d539a0fc` — Mimikatz / `mimik.exe`
- `45126297c07c6ef56b51440cd0dc30acf7b3b938e2e9e656334886fe2f81f220` — AnyDesk / `anydesk.exe`
- `9fae3f15900e13ec3860a109555ecd33ca43d38907c63438c50a2d6d91bfee1d` — NetScan / `netscan.exe`
- `b29f91a440527fb621d106a2048f6379fff3263c60aeda9c82ff8c1d5ae880a8` — defense-evasion tool / `symantec.exe`
- `e097f3b445b63b07afacde8d6a67f0be654dd51e228a3610fb0710a1f7e29a69` — GodDamn ransomware / `encrypter-windows-gui-x86.exe`

## Defender guidance
- Treat discovery of `g11.sys`, the PoisonX hash, or a suspicious Microsoft Hardware Compatibility Publisher-signed driver as an emergency defense-impairment event. Preserve the driver, loader, signature metadata, process tree, and EDR tamper telemetry before cleanup.
- Hunt for `symantec.exe` executing from user-profile Music paths or other non-vendor directories, especially when followed by driver-store writes, service-control activity, or security-product process termination.
- Correlate AnyDesk service installation, PsExec activity, host reboot commands, and NirSoft / Mimikatz execution across hosts. The combination is stronger than any individual tool.
- If GodDamn encryption is found, assume credentials were harvested before encryption. Rotate domain, backup, hypervisor, RMM, VPN, EDR, and local-admin credentials exposed on affected hosts.
- Enforce Microsoft vulnerable-driver blocklist, HVCI / memory integrity where feasible, WDAC or driver allowlisting for servers, and alerting on new kernel-driver loads outside approved vendor paths.
- Validate that EDR tamper-protection alerts still fire when user-mode hooks are removed or security-product processes are killed; PoisonX-style drivers can blind otherwise healthy agents.

## Related pages
- [The Gentlemen ransomware](../tools/the-gentlemen-ransomware.md)
- [Avalon / CrownX malware framework](avalon-crownx-malware-framework.md)
- [Anubis ransomware CitrixBleed 2 / RMM / cloudflared intrusions](anubis-ransomware-citrixbleed2-rmm-cloudflared.md)
- [Storm-2603 parallel SharePoint ransomware intrusion](storm-2603-parallel-sharepoint-ransomware-intrusion.md)

## Sources
- Broadcom / Symantec Threat Hunter Team: [https://www.security.com/threat-intelligence/goddamn-ransomware-beast-rebrand](https://www.security.com/threat-intelligence/goddamn-ransomware-beast-rebrand)
- The Hacker News: [https://thehackernews.com/2026/07/goddamn-ransomware-uses-poisonx-driver.html](https://thehackernews.com/2026/07/goddamn-ransomware-uses-poisonx-driver.html)
- Xcitium Threat Labs: [https://threatlabsnews.xcitium.com/blog/reverse-engineering-a-0-day-poisonx-byovd-driver-bypasses-crowdstrike-edr/](https://threatlabsnews.xcitium.com/blog/reverse-engineering-a-0-day-poisonx-byovd-driver-bypasses-crowdstrike-edr/)
