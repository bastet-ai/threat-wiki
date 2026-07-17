# Siemens ROX II zero-day exploit chain

## Summary
Unit 42 published a 2026-07-17 technical report on three Siemens RUGGEDCOM / ROX II operational-technology switch vulnerabilities: **CVE-2025-40948**, **CVE-2025-40947**, and **CVE-2025-40949**. Chained together, the flaws move from arbitrary file disclosure to root command injection and then persistent root-level command execution through the switch scheduler.

Siemens ProductCERT advisories **SSA-973901**, **SSA-078743**, and **SSA-081142** recommend updating affected RUGGEDCOM ROX II devices to firmware **V2.17.1**. Treat exposed management interfaces on ROX II switches as high-value OT control-plane exposure: these devices can sit in industrial networks where compromise can support persistence, traffic visibility, denial of service, or further movement.

## Tags
- ops
- operations
- Siemens
- RUGGEDCOM
- ROX II
- OT switches
- industrial control systems
- CVE-2025-40948
- CVE-2025-40947
- CVE-2025-40949
- zero-day
- exploit chain
- arbitrary file disclosure
- command injection
- privilege escalation
- persistent root access
- task scheduler abuse
- xz
- critical infrastructure
- Unit 42

## Why this matters
- The chain affects OT switches, not only general-purpose servers; compromise can impact network segmentation, monitoring, and availability in industrial environments.
- Unit 42 rates the vulnerabilities from medium to critical severity: **CVSS 6.8** for CVE-2025-40948, **7.5** for CVE-2025-40947, and **9.1** for CVE-2025-40949.
- The first flaw can expose sensitive local files such as configuration, password hashes, cryptographic material, or topology data.
- The second flaw turns attacker-controlled feature-key content into command execution with root privileges.
- The third flaw lets an authenticated attacker write malicious scheduler entries into the root cron table, giving persistence after initial compromise.

## Reported chain

### CVE-2025-40948: arbitrary file disclosure via privileged `xz` execution
Unit 42 reports that a privileged configuration daemon accepts user-controlled parameters for the Linux `xz` utility. By combining parameters such as `-f`, `-c`, and `-d`, an attacker can use the root-running process to disclose arbitrary files on the switch filesystem.

Defender significance: the primitive is reconnaissance-friendly. It can reveal local credentials, private keys, configuration files, and network context needed to shape later exploitation.

### CVE-2025-40947: feature-key command injection to root
The second flaw is in the ROX II feature-key validation path. Unit 42 says the validation function inserts attacker-controlled signature data into a command string without sufficient sanitization, allowing crafted feature-key content to execute commands as root.

Defender significance: treat evidence of unexpected feature-key uploads or validation activity as potentially equivalent to device-level compromise, especially if followed by new files, scheduler changes, or unexplained management sessions.

### CVE-2025-40949: scheduler command injection for persistence
After privilege escalation, an authenticated attacker can abuse the ROX II web management task scheduler. Unit 42 reports that improper input sanitization allows malicious commands to be injected into the system's root cron table, enabling recurring root-level execution.

Defender significance: persistence may survive normal service restarts and can turn the switch into a durable foothold for data exfiltration, traffic manipulation, or denial-of-service activity.

## Exposure and triage

### Affected / fixed versions
- Siemens ProductCERT advisories cover RUGGEDCOM ROX / ROX II releases before **V2.17.1**.
- Update affected devices to **V2.17.1** or later per Siemens guidance.
- Reduce management-plane reachability while patching; OT switch management should not be reachable from general user networks or the internet.

### Immediate defender actions
- Inventory RUGGEDCOM ROX II devices and confirm firmware version, management-interface exposure, and remote-administration paths.
- Prioritize exposed or cross-zone reachable devices for firmware update or management-plane isolation.
- Review logs for attempts to pass `xz` parameters `-f`, `-c`, and `-d` to the privileged configuration path, especially where file paths point outside expected configuration operations.
- Review feature-key upload / validation events and surrounding management sessions for anomalous inputs or unexpected command side effects.
- Inspect scheduler / cron configuration for unauthorized tasks, especially entries created through web management around suspicious sessions.
- Preserve switch configuration, logs, scheduler state, and firmware/version evidence before remediation if compromise is suspected.
- Rotate credentials and keys exposed in switch configuration only after containment, because CVE-2025-40948 could disclose sensitive local material.
- Validate segmentation controls: management interfaces should require strong authentication, administrative network origin, and logging independent of the potentially compromised switch.

## Related pages
- [Cisco Catalyst SD-WAN Manager CVE-2026-20245 / CVE-2026-20262 exploitation](cisco-catalyst-sd-wan-manager-cve-2026-20245-exploitation.md)
- [Arista EOS CVE-2026-7473 tunnel decapsulation exploitation](arista-eos-cve-2026-7473-tunnel-decap-exploitation.md)
- [Lantronix EDS5000 CVE-2025-67038 exploitation](lantronix-eds5000-cve-2025-67038-exploitation.md)
- [Ubiquiti UniFi OS CVE-2026-34908 / CVE-2026-34909 / CVE-2026-34910 exploitation](ubiquiti-unifi-os-cve-2026-34908-34909-34910-exploitation.md)

## Sources
- Unit 42: [Three Steps to the Terminal: A Siemens ROX II Zero-Day Trilogy](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/)
- Siemens ProductCERT SSA-973901: [Arbitrary File Disclosure Vulnerability in RUGGEDCOM ROX before V2.17.1](https://cert-portal.siemens.com/productcert/html/ssa-973901.html)
- Siemens ProductCERT SSA-078743: [Remote Code Execution Vulnerability in RUGGEDCOM ROX before V2.17.1](https://cert-portal.siemens.com/productcert/html/ssa-078743.html)
- Siemens ProductCERT SSA-081142: [Arbitrary Code Execution Vulnerability in RUGGEDCOM ROX before V2.17.1](https://cert-portal.siemens.com/productcert/html/ssa-081142.html)
