# AryStinger legacy-router recon proxy network

## Summary
QiAnXin XLab reported **AryStinger**, a bot family that compromises legacy routers and NAS devices to build a distributed reconnaissance, tunneling, and proxy network. XLab first observed the router wave on **2026-03-12** from `107.150.106[.]14`, using old Realtek RTL819X-era router flaws (`CVE-2013-3307` and `CVE-2016-5681`) against Linksys and D-Link devices. A related Go-based NAS build appeared on **2026-04-26** and used `CVE-2025-11837` in QNAP Malware Remover.

XLab measured at least **4,300 infected RTL819X-class routers**, with D-Link devices dominant and the D-Link DIR-850L accounting for about 75% of the observed infected router population. XLab said it could not measure the NAS infection scale.

## Tags
- ops
- operations
- AryStinger
- QiAnXin XLab
- router malware
- IoT botnet
- proxy network
- reconnaissance
- operational relay box
- RTL819X
- Linksys
- D-Link
- QNAP
- CVE-2013-3307
- CVE-2016-5681
- CVE-2025-11837
- Dropbear
- gs-netcat
- Protobuf
- XOR

## Why this matters
- AryStinger is closer to reconnaissance and relay infrastructure than a commodity DDoS botnet: infected nodes can scan, fingerprint services, enumerate DNS/subdomains, tunnel traffic, and run operator-supplied tasks.
- The router build demonstrates that decade-old edge-device vulnerabilities still produce useful attacker infrastructure when devices remain internet-exposed and unsupported.
- The Go-based NAS build broadens the risk from consumer routers into storage appliances and supports richer internal/external scanning and payload execution.
- Compromised routers and NAS devices can hide the real attacker origin during pre-intrusion footprinting, creating an operational-relay-box-style layer that defenders may misread as benign residential or small-office traffic.

## Reported infection scope
- XLab measured **4,300+ infected routers** for the RTL819X-class wave; this count does not include NAS infections.
- Observed router models were mostly D-Link:
  - `DIR-850L` — about 75% of observed infections.
  - `DIR-818LW` — about 13%.
  - `DIR-816L`, `DIR-818L`, `DWR-118`, and `DIR-817LW` — smaller observed shares.
- XLab's geography breakdown for infected routers was led by South Korea, China, Sweden, Malaysia, and Singapore.

## Compromise and capability chain
1. **Initial exploitation**
   - RTL819X router build: old Linksys / D-Link issues `CVE-2013-3307` and `CVE-2016-5681`.
   - NAS build: `CVE-2025-11837` in QNAP Malware Remover, a code-injection issue patched before the observed AryStinger NAS wave.
2. **Download and execution**
   - Router spread scripts query `hgodpcx[.]ajb8[.]com` for the current version and fetch a `syswapd0` payload under `/tmp/bin`.
3. **C2 enrollment**
   - Bots communicate with C2 over HTTP or HTTPS using Protobuf-encoded traffic and simple XOR obfuscation; the Go build also uses gzip.
   - XLab reports a hardcoded communication key: `sh_#@!_2024_secret`.
4. **Tasking**
   - Each infected node acts as an "Executor" that can receive chunks of larger scanning jobs.
   - Router build: streamlined C implementation focused on `massdns` and tunnel functionality for constrained hardware.
   - NAS build: Go implementation with IP scanning, DNS scanning, HTTP liveness checks, `fscan`, `ksubdomain`, `httpx`, `Tlsx`, command execution, and source-level Go / Java / Python payload execution.
5. **Persistence / remote access**
   - Router build: Dropbear SSH server on a fixed port, reported as `2332`.
   - NAS build: `gs-netcat` remote access.

## Infrastructure and indicators
Use XLab's full IOC list for hash coverage. High-signal pivots from the public report include:

| Type | Indicator |
| --- | --- |
| Scanner IP | `107.150.106[.]14` |
| C2 | `opi7[.]com` |
| C2 | `xook[.]ajb8[.]com` |
| C2 | `xonice[.]ahb8[.]com` |
| C2 | `eixfi[.]ajb8[.]com` |
| C2 | `dybic[.]ajb8[.]com` |
| C2 | `sdkv1[.]dataexplore[.]cc` |
| C2 | `sdkv1[.]dataexplore[.]co` |
| Downloader | `hgodpcx[.]auq8[.]com` |
| Downloader | `hgodpcx[.]ajb8[.]com` |
| Downloader | `io[.]ary2[.]com` |
| Manifest path | `/prod/RTL819X/{version}/manifest.json` |
| Manifest path | `/prod/standard/{version}/manifest.json` |
| Payload path | `/prod/RTL819X/{version}/syswapd0` |
| Payload path | `/prod/standard/{version}/syswapd0-linux-amd64` |
| Local directory | `/tmp/bin` |
| Process names | `syswapd0h`, `syswapd0w` |
| Hardcoded key | `sh_#@!_2024_secret` |

## Defender heuristics
- Retire or isolate end-of-life Linksys, D-Link, and Realtek RTL819X-era routers that no longer receive firmware fixes; patching policy cannot compensate for unsupported edge devices.
- Disable internet-facing administration on routers and NAS appliances; restrict management to a dedicated internal admin network or VPN.
- Hunt network telemetry for router or NAS egress to `ajb8[.]com`, `ahb8[.]com`, `auq8[.]com`, `ary2[.]com`, `dataexplore[.]cc`, and `dataexplore[.]co` infrastructure, especially Protobuf-like HTTP/HTTPS traffic from devices that should not speak to those domains.
- Inspect affected devices for `/tmp/bin/syswapd0*`, processes named `syswapd0h` or `syswapd0w`, unexpected Dropbear listeners such as TCP `2332`, and `gs-netcat` artifacts.
- Treat scans from residential or small-office router IPs as potentially relay-originated; enrich detections with device fingerprinting, ASN/customer-premise context, and repeated tasking patterns rather than assuming the IP owner is the attacker.
- For QNAP environments, verify Malware Remover is updated past the `CVE-2025-11837` fix and review appliance logs for code-injection attempts beginning around late April 2026.

## Related pages
- [JDY SOHO / IoT reconnaissance botnet](jdy-soho-iot-recon-botnet.md)
- [Dutch Police / NCSC 17-million-device botnet disruption](dutch-police-ncsc-17-million-device-botnet.md)
- [Malicious infrastructure provider concentration](../patterns/malicious-infrastructure-provider-concentration.md)

## Sources
- QiAnXin XLab: https://blog.xlab.qianxin.com/arystinger-botnet-hijacks-legacy-routers-for-global-attacks-en/
- The Hacker News: https://thehackernews.com/2026/06/arystinger-malware-infects-4300-legacy.html
