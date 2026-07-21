# C0XMO Gafgyt DD-WRT botnet

## Summary
**C0XMO** is a cross-architecture Gafgyt-family Linux botnet observed by FortiGuard Labs in March 2026. The campaign gained initial access to a Japanese technology company by exploiting **CVE-2021-27137**, a stack-based buffer overflow in the DD-WRT UPnP/SSDP parser. CISA added the vulnerability to the Known Exploited Vulnerabilities catalog on 2026-07-21 with a 2026-07-24 remediation due date.

The bot combines multi-path persistence, competitor removal, 19 DDoS methods, and a separately downloaded Python scanner. The scanner propagates through weak Telnet/SSH credentials, exposed Android Debug Bridge, and a collection of router, DVR, GLPI, and other HTTP exploits. This makes C0XMO both an active DD-WRT exploitation case and a reusable IoT/Linux propagation framework.

## Tags
- ops
- operations
- C0XMO
- Gafgyt
- botnet
- IoT botnet
- DD-WRT
- CVE-2021-27137
- CISA KEV
- active exploitation
- UPnP
- SSDP
- UDP/1900
- Linux malware
- DDoS
- Telnet
- SSH
- Android ADB
- weak credentials
- cron persistence

## Exploited DD-WRT vulnerability
- **Affected code:** DD-WRT changeset `45723` and earlier; the vendor fix is changeset `45724`.
- **Precondition:** UPnP must be enabled. DD-WRT disables it by default and normally listens only on internal interfaces.
- **Entry point:** an unauthenticated, oversized `ST:uuid:` value in an SSDP `M-SEARCH` request to UDP port `1900` reaches an unsafe copy into a fixed-size buffer.
- **Impact:** the overflow can crash the UPnP service and, depending on device architecture and exploit mitigations, permit code execution.
- **Observed use:** FortiGuard Labs reported C0XMO delivery through this flaw; CISA's KEV addition independently elevates it to a confirmed active-exploitation priority.

Do not interpret the usual LAN-only binding as proof of safety. Exposed or misconfigured UPnP, compromised internal hosts, and downstream products shipping DD-WRT can all make the path reachable.

## Malware behavior

### Cross-architecture delivery
FortiGuard identified builds for ARM, Motorola 68000, MIPS R3000, PowerPC, SuperH, x86, and AMD64. The compromised host downloaded the selected binary to `/tmp/.cache`.

### Persistence and self-preservation
C0XMO:
- copies itself to `/tmp/.sys`, `/var/tmp/.sys`, `/dev/shm/.sys`, and, where available, `$HOME/.sys`;
- sets copied files executable;
- creates a cron entry intended to run it every 15 minutes;
- appends execution commands to shell startup files such as `~/.profile`, `~/.bashrc`, and `~/.bash_profile`; and
- re-executes itself if the malware process terminates.

### Competitor removal
The bot scans `/proc`, kills blacklisted processes, deletes matching executables, and removes competing persistence from cron, `rc.local`, init scripts, system services, and shell profiles. Its blacklist spans other botnets, network services, programming tools, and red-team utilities. This behavior can erase evidence and disrupt legitimate administration as well as rival malware.

### Command and DDoS functions
After a custom handshake, the bot identifies itself to the C2 as `BOT` and accepts heartbeat, scanning-control, and attack commands. FortiGuard documented 19 DDoS methods, including UDP, TCP, SYN, ICMP, NTP and memcached amplification, game-service floods, HTTP floods, and Cloudflare-oriented HTTP methods.

## Propagation scanner
C0XMO downloads a separate Python scanner from `217.160.125[.]125:15527`. The script installs `requests`, `paramiko`, and `beautifulsoup4`, then performs multithreaded random scanning across remote-access, web-management, and ADB ports.

Propagation paths include:
- hard-coded weak credentials against Telnet and SSH;
- exposed Android Debug Bridge;
- CVE-2021-27137 DD-WRT UPnP exploitation;
- D-Link HNAP command execution, including CVE-2015-2051;
- GLPI htmLawed CVE-2022-35914 and barcode-injection paths;
- AVTECH DVR vulnerabilities including CVE-2025-34054 / CVE-2016-15047;
- NVMS-9000, broadband-router, Zyxel SysTools, CGI, HNAP, and UPnP injection paths.

The scanner maintains blacklist and failure files to avoid selected ranges, known bot nodes, prior failures, honeypots, and research infrastructure. Successful access triggers architecture detection and retrieval of the matching payload.

## Detection and triage
- Inventory DD-WRT and DD-WRT-derived devices; identify firmware older than changeset `45724` and any enabled UPnP service.
- Review firewall, IDS, router, and packet telemetry for oversized SSDP `M-SEARCH` requests containing long `ST:uuid:` values on UDP/1900.
- Hunt Linux and embedded systems for `/tmp/.cache`, `/tmp/.sys`, `/var/tmp/.sys`, `/dev/shm/.sys`, `$HOME/.sys`, and `/tmp/scanner.py`.
- Audit user crontabs, `~/.profile`, `~/.bashrc`, `~/.bash_profile`, `rc.local`, init scripts, and system services for unfamiliar hidden-binary execution.
- Investigate unexpected `pip` installation of `requests`, `paramiko`, or `beautifulsoup4` on routers, appliances, and minimal Linux systems.
- Look for high-volume outbound scans targeting ports `23`, `22`, `80`, `443`, `8080`, `5555`, `5511`, `5554`, `4443`, `81`, `8000`, `7547`, `8081`, `8443`, and `8888`.
- Treat unexplained termination of network services, admin tools, scanners, or rival botnet processes as a possible C0XMO behavior, not merely system instability.

## Public infrastructure
Defang and validate these pivots in context; hosting addresses may be reassigned.

- `85.215.131[.]70` — bot C2 reported by FortiGuard
- `217.160.125[.]125:15527` — scanner and payload distribution
- `176.100.37[.]91` — campaign IOC

FortiGuard also published a larger set of SHA-256 hashes in the source report. Prefer the complete vendor IOC list for blocking and retrospective hunting rather than copying an incomplete subset.

## Response guidance
1. Update affected DD-WRT devices to a build containing changeset `45724` or later; verify the effective firmware after reboot.
2. Disable UPnP unless there is a documented need. Restrict SSDP to required local segments and prevent internet exposure of UDP/1900.
3. Disable unused Telnet, SSH, ADB, and web-management services; remove default or weak credentials and restrict management access to trusted networks.
4. If exploitation or C0XMO artifacts are present, isolate the device and preserve volatile network/process evidence before rebooting where feasible.
5. Reflash or factory-reset compromised embedded devices from trusted firmware, restore a reviewed configuration, rotate management credentials, and inspect adjacent systems for scanner-driven propagation.
6. Check for service disruption and security-control removal caused by competitor-killing logic. A missing rival sample does not mean the host is clean.

## Attribution caveats
FortiGuard described the malware as a Gafgyt variant and observed the source address for the Japanese victim's exploitation in Germany. Hosting geography does not identify the operator, and no named actor attribution was published.

## Related pages
- [JDY SOHO / IoT reconnaissance botnet](jdy-soho-iot-recon-botnet.md)
- [AryStinger legacy-router recon proxy network](arystinger-legacy-router-recon-proxy-network.md)
- [xlabs_v1 DDoS-for-hire IoT botnet](xlabs-v1-ddos-for-hire-iot-botnet.md)
- [TuxBot v3 Evolution IoT botnet framework](tuxbot-v3-evolution-iot-botnet.md)

## Sources
- FortiGuard Labs: [Inside the Cross-Platform Propagation of a New Gafgyt Variant C0XMO](https://www.fortinet.com/blog/threat-research/inside-cross-platform-propagation-of-new-gafgyt-variant-c0xmo)
- CISA: [Known Exploited Vulnerabilities catalog](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- SSD Secure Disclosure: [DD-WRT UPnP Buffer Overflow](https://ssd-disclosure.com/ssd-advisory-dd-wrt-upnp-buffer-overflow/)
- DD-WRT: [changeset 45724](https://svn.dd-wrt.com/changeset/45724)
- NVD: [CVE-2021-27137](https://nvd.nist.gov/vuln/detail/CVE-2021-27137)
