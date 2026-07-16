# UAT-7810 LONGLEASH ORB network expansion

## Summary
Cisco Talos' July 7, 2026 report says the China-nexus actor tracked as **UAT-7810** is continuing to expand the **LapDogs** Operational Relay Box (ORB) network by compromising internet-facing networking devices. The update is durable because it names an active infrastructure-maintenance role, a successor backdoor framework (**LONGLEASH**) to **ShortLeash**, previously unreported tooling (**DOGLEASH**, **LEASHTEST**, and **JARLEASH**), and router vulnerability families defenders can hunt and patch.

Talos assesses UAT-7810 as likely tasked with building ORB infrastructure later reused by secondary Chinese threat actors. One named consumer of that infrastructure is **UAT-5918**, a China-nexus cluster linked to persistent access against Taiwan critical infrastructure entities since at least 2023.

## Tags
- ops
- UAT-7810
- UAT-5918
- China-nexus
- Operational Relay Box
- ORB network
- LapDogs
- LONGLEASH
- ShortLeash
- DOGLEASH
- LEASHTEST
- JARLEASH
- Linux networking devices
- MIPS embedded devices
- router compromise
- Ruckus routers
- ASUS AiCloud routers
- CVE-2020-22653
- CVE-2020-22658
- CVE-2023-25717
- CVE-2025-2492
- Cisco Talos
- The Hacker News

## Timeline
- **2023:** UAT-5918 activity against Taiwan critical infrastructure is linked to persistent access operations, later reported as using UAT-7810-built ORB infrastructure.
- **2025-06:** The LapDogs ORB network first came to public attention.
- **2026-early:** Campaigns singled out ASUS AiCloud routers vulnerable to CVE-2025-2492, indicating attempted expansion beyond the Ruckus router population.
- **2026-07-07:** Cisco Talos published primary reporting on UAT-7810's LONGLEASH, DOGLEASH, LEASHTEST, JARLEASH, n-day exploitation, and newly identified payload-hosting infrastructure.
- **2026-07-08:** The Hacker News summarized Cisco Talos reporting.

## Activity and tooling
- **UAT-7810 role:** Talos describes UAT-7810 as an APT actor responsible for maintaining and proliferating LapDogs, an ORB network intended to relay traffic and provide operational infrastructure for later intrusions.
- **LONGLEASH:** Successor to **ShortLeash**. ShortLeash can contact an external server, host a web server, and act as both C2 server and client; LONGLEASH adds an executor component for proxying over HTTP, DNS, SOCKS, TCP, ICMP, and UDP, connection management, client authorization, and self-removal if tampering is detected.
- **Relay behavior:** LONGLEASH can act as an intermediate C2 server, relaying commands and data from the primary C2 to peers in the ORB network.
- **DOGLEASH:** Passive Linux backdoor that executes arbitrary shellcode on compromised devices. Talos saw at least four new servers hosting minor DOGLEASH variants for deployment.
- **LEASHTEST:** ELF testing binary for MIPS-based embedded devices, with functionality such as thread, child-process, and async-timer creation. Its presence suggests ongoing validation of MIPS behavior even after LONGLEASH became a fuller backdoor framework.
- **JARLEASH:** Java / JAR administration backdoor observed on at least one of three servers, with file-management, FTP, SFTP, and Netcat capabilities.

## Reported infrastructure and pivots
Talos' primary report adds concrete infrastructure defenders can pivot on when hunting router, wireless-controller, and embedded-Linux compromise:

- `194.233.92[.]26` — UAT-7810 payload-hosting / download infrastructure.
- `217.15.160[.]247` — UAT-7810 payload-hosting / download infrastructure.
- `217.15.164[.]147` — UAT-7810 payload-hosting / download infrastructure; Talos also links it to ASUS AiCloud router exploitation activity in early 2026.
- `95.182.100[.]231` — fourth payload-hosting address found through forensic analysis of compromised networking devices.
- TLS on port `99` was observed on `194.233.92[.]26` and `217.15.164[.]147` with certificate SHA-256 fingerprint `c2ab9adaba93ff094b8f3fc37d906014d870582039d276b7bd03e6fd583d8a15` and subject fields set to `exploit`.

## Exploited / targeted device exposure
Reported UAT-7810 chains have used known flaws in unpatched networking gear:

- **Ruckus wireless routers:** CVE-2020-22653, CVE-2020-22658, and CVE-2023-25717.
- **ASUS AiCloud routers:** CVE-2025-2492.

Treat the vulnerability list as a starting point rather than a complete boundary. ORB builders favor unmanaged, internet-exposed, low-telemetry devices and can expand quickly when firmware remains stale.

## Defender guidance
- Inventory exposed Ruckus and ASUS AiCloud devices, validate firmware levels against the named CVEs, and remove direct internet exposure for management surfaces wherever possible.
- Hunt for unexpected web-server, proxy, SOCKS, DNS, ICMP, TCP, UDP, FTP, SFTP, or Netcat behavior on routers, wireless controllers, and embedded Linux appliances.
- Pivot on the reported payload-hosting IPs and the port-99 `exploit` TLS certificate fingerprint in firewall, proxy, NetFlow, passive-DNS, and exposed-service telemetry.
- Collect volatile state before rebooting suspected ORB nodes: process lists, open sockets, listening ports, filesystem timestamps, startup scripts, web roots, temporary directories, and unusual Java / JAR artifacts.
- Treat compromised network devices as relay infrastructure, not just endpoints. Preserve NAT, firewall, NetFlow, DNS, and upstream ISP logs to identify downstream victim traffic and peer nodes.
- Where firmware integrity cannot be proven, reimage or replace the device, rotate local and upstream credentials, and review adjacent network segments for follow-on access from the compromised appliance.
- Segment and monitor management-plane devices with explicit egress controls; block arbitrary outbound proxying and alert on router-originated connections to uncommon external ports or protocols.

## Related pages
- [JDY SOHO / IoT reconnaissance botnet](jdy-soho-iot-recon-botnet.md)
- [AryStinger legacy-router recon proxy network](arystinger-legacy-router-recon-proxy-network.md)
- [VerdantBamboo appliance BRICKSTORM operation](verdantbamboo-appliance-brickstorm-operation.md)
- [Malicious infrastructure provider concentration](../patterns/malicious-infrastructure-provider-concentration.md)

## Sources
- Cisco Talos: <https://blog.talosintelligence.com/uat-7810/>
- The Hacker News: <https://thehackernews.com/2026/07/china-linked-uat-7810-expands-orb.html>
