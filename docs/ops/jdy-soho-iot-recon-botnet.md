# JDY SOHO / IoT reconnaissance botnet

## Summary
Lumen Black Lotus Labs reports a resurgence of **JDY**, a China-nexus reconnaissance botnet that grew from the JDY cluster of the earlier KV-botnet activity into more than **1,500 compromised SOHO and IoT devices**. Black Lotus Labs assesses that JDY supports China-nexus APT activity, including Volt Typhoon-linked ecosystems, by continuously discovering and fingerprinting exposed services for rapid follow-on exploitation.

JDY is best treated as reconnaissance infrastructure rather than an end-stage implant: it distributes targeted scanning across residential and small-business IP space, collects banners, TLS details, protocol metadata, and service fingerprints, then returns structured results to central infrastructure for triage and targeting.

## Tags
- ops
- operations
- botnet
- reconnaissance
- SOHO routers
- IoT
- China-nexus
- Volt Typhoon
- KV-botnet
- JDY
- Lumen Black Lotus Labs

## Why this matters
- JDY shows how disruption of one botnet cluster does not remove the underlying reconnaissance capability; Black Lotus Labs says JDY more than doubled after U.S. takedown activity against the KV cluster.
- Compromised residential and small-business devices weaken geofencing, reputation blocking, and static scanner blocklists because probes can look like ordinary domestic traffic.
- Black Lotus Labs observed vulnerability-focused targeting shortly after public disclosures, including increased Fortinet scanning within hours of CVE-2026-35616 disclosure.
- The botnet reportedly focused heavily on U.S. military and associated networks, making JDY scanning useful as an early warning signal for later China-nexus intrusion attempts.

## Reported infrastructure and malware behavior
- Scale and device mix:
  - More than **1,500** active compromised SOHO / IoT devices.
  - Earlier JDY activity used Cisco RV320 and RV325 routers; the expanded botnet includes devices from Cisco, Araknis, Mimosa Networks, Ubiquiti, DrayTek, Hikvision, and Linksys.
- Architecture:
  - Operators manage C2 and payload infrastructure through concealed Tor nodes.
  - Some victim devices are managed with Platypus, an open-source reverse-shell and host-management tool.
  - Black Lotus Labs identified `149.248.3[.]38` as a JDY payload server hosting Platypus on port `13339`.
- Malware role:
  - Linux scanning agents compiled for MIPS, MIPS64, and MIPSEL architectures.
  - Dropper logic probes device architecture with local utilities, writes payloads under `/etc/` or `/tmp/`, sets execute permissions, launches the malware with C2 and group arguments, then deletes the dropped file.
  - Beacons use HTTPS POST to `/dispatch_service/v2/probe_status`.
  - Tasking is fetched from `/dispatch_service/v2/probe_task/%s?ip=%s&code=%s&v=%s&gid=%d&status=%u`.
  - Task responses are base64-decoded and decrypted with a hard-coded AES key reported by Black Lotus Labs as `0000000000000000bdb718bdf47cbcde`.
  - Fingerprint rules can be updated through `update_dmap_fp_db` and fetched from `/dispatch/v2/dmap/<hex from dmp_fp_digest>`.
  - Scan results are compressed and POSTed to `/data/v2/pscan` as `attr.json`.
- Scanning behavior:
  - If raw sockets are available, JDY performs high-speed SYN scanning with custom TCP packets and a fixed source port of `19000`.
  - Fallback scanning uses standard TCP / SSL connections.
  - For HTTP port `80`, the malware can send crafted ICMP probes before TCP scanning; Black Lotus Labs reports ICMP identifier `19037` and sequence `35765`.

## Defender heuristics
- Treat low-volume, distributed scans from residential / SOHO IPs as potentially relevant when they align with newly disclosed edge-device, VPN, firewall, router, or appliance vulnerabilities.
- Do not rely on geofencing or scanner reputation alone for military, government, telecom, managed-service, edge-service, and critical-infrastructure exposure monitoring.
- Correlate spikes in probes for a product family immediately after public advisory release with vulnerability-management queues and external attack-surface inventory.
- Monitor for JDY protocol paths and artifacts where you control exposed infrastructure, especially:
  - `/dispatch_service/v2/probe_status`
  - `/dispatch_service/v2/probe_task/`
  - `/dispatch/v2/dmap/`
  - `/data/v2/pscan`
  - source port `19000` SYN scans where visible
  - ICMP identifier `19037` / sequence `35765` near HTTP reconnaissance
- For SOHO / branch-office / lab devices under your control, prioritize vendor firmware updates, remove unnecessary internet exposure, rotate credentials, disable legacy remote management, and reboot where vendor guidance says volatile botnet implants may be cleared.
- Follow the U.K. NCSC guidance Black Lotus Labs cites for defending against China-nexus covert networks of compromised edge devices.

## Attribution caveats
- Black Lotus Labs links JDY to China-nexus threat activity and says it likely continues supporting various China-nexus APT actors based on earlier KV-botnet links plus sustained targeting and victimology.
- Keep JDY as infrastructure / capability coverage unless future public reporting attributes operation of the botnet to a specific named group with stronger sourcing.

## Sources
- [Lumen Black Lotus Labs](https://www.lumen.com/blog/en-us/expanded-jdy-iot-and-soho-botnet-enables-rapid-vulnerability-exploitation)
- [U.K. NCSC guidance cited by Black Lotus Labs](https://www.ncsc.gov.uk/guidance/defending-organisations-against-covert-networks-of-compromised-edge-devices)
- [The Hacker News summary](https://thehackernews.com/2026/06/china-linked-jdy-botnet-expands-to-1500.html)
