# SPEAKINGSTONE and DARKLANTERN: two more implants in ZBT / MoreQuick router firmware (VulnCheck supply-chain trace)

## Summary
**SPEAKINGSTONE** and **DARKLANTERN** are two additional remote-control implants that VulnCheck found in the firmware of a white-label ZBT cellular router, following its earlier **ENDLESSDOORS** disclosure. Both are written in **Nim**, both communicate over **UDP**, and both are launched by the same connectivity-watchdog binary, `inetdetect`.

**SPEAKINGSTONE** is an outbound phone-home implant (service `yunmgrd`) that beacons to ZBT's cloud infrastructure over UDP and executes arbitrary server-supplied commands, steals PPPoE ISP credentials, can rewrite DNS, and can open a reverse SSH tunnel. **DARKLANTERN** is an unauthenticated WAN listener backdoor (service `infosrvd`, UDP `9992`) that hands a root shell to anyone who can forge a trivially-computable checksum — protected only by a MAC filter with a hard-coded all-zeros bypass.

VulnCheck traced the device to **Shenzhen Zhibotong Electronics (ZBT)** and documented how the same ZBT / **MoreQuick** platforms are resold under many unrelated brands across the United States, Canada, Australia, Germany, and Russia. The same implants that VulnCheck sinkholed on a domain registered inside China are running on a router a U.S. consumer can buy on Amazon.

## Tags
- ops
- operations
- VulnCheck
- Zbtlink
- ZBT
- Shenzhen Zhibotong Electronics
- MoreQuick
- SPEAKINGSTONE
- DARKLANTERN
- ENDLESSDOORS
- router compromise
- embedded Linux
- firmware backdoor
- supply-chain risk
- command and control
- unauthenticated RCE
- root shell
- UDP C2
- outbound C2
- IoT
- white-label
- Nim
- DNS hijack
- PPPoE credential theft
- reverse SSH tunnel
- sinkhole
- firmware supply chain

## Why this matters
- This is the **third** distinct implant family in the ZBT / MoreQuick firmware lineage after ENDLESSDOORS, and it ships across multiple firmware generations — a pattern VulnCheck describes as intentional and not a software defect.
- **DARKLANTERN requires no prior compromise.** It listens on UDP `9992` from the public internet (the default firewall explicitly allows it) and accepts commands as root. No authentication, no encryption, and the only "protection" (a MAC filter) has a hard-coded all-zeros bypass. One 19-byte probe identifies the device; one command packet gives a root shell.
- **SPEAKINGSTONE traverses NAT.** Because it phones home outbound, it stays controllable even when the router is behind firewalls, carrier-grade NAT, or private networks — exactly the placement a cellular CPE gets.
- The implant capabilities go far beyond "support": it can **redirect a router's DNS**, **exfiltrate the WAN PPPoE username and password**, and **open a reverse SSH tunnel** to any device that phones home — silently, remotely, and at root.
- White-label distribution means affected units can carry a brand the buyer has never heard of; a logo or retailer name is not a reliable indicator of origin.

## Device and provenance
VulnCheck's test unit was a **Deep Orange 3G/4G/LTE Router** sold for ~$88 by a small New York company on Amazon. It is a white-label **ZBT-WE826-T2** (ZBT MAC OUI block `78:A3:51`; firmware built 2019, pre-dating ENDLESSDOORS, so that implant was absent — the two new ones were not). The firmware OEM is **MoreQuick** (the hard-coded checksum key `mqonu.com` references it).

The ZBT-WE826 platform is attractive for its cellular SIM connectivity (pipelines, roadside billboards, trains, RVs, cellular failover), which is why it has been resold under many names. VulnCheck ties the platform to brands including **Lippert Components** (WiFi On-The-Go), **Wave WiFi** (MBR 500/550), **OneX** (AU, "RV WIFI Route"), **MOFI** (CA, MOFI4500-4GXeLTE — MOFI's custom firmware had no implants), **Digineo** (DE, AC1200 Pro on ZBT WG3526), **ALLNET** (DE, ALL-WR1200AC-WRT = ZBT WG2626 OEM), and a cluster of brands that are effectively ZBT itself: **WiFlyer**, **WORDFI**, and **HomeMyfi** (all ZBT USPTO trademarks), **Cioswi** (archived support page pointed to `sales03@zbt-china.com`; active AliExpress/Amazon storefronts with Cyrillic text), **CroSkylink** (CS-Z8102AX-M2-T ≈ Zbtlink Z8102AX-T), and **KuWFi** (WG3526 = WiFlyer WG3526 = Zbtlink WG3526).

## SPEAKINGSTONE (phone-home implant)
Runs as the `yunmgrd` service. It is an **outbound** beacon that connects to a configured C2 server and waits for instructions — a deliberately better design than a listener, since it works behind NAT and ordinary stateful firewalls.

- **Primary C2:** `ac-link[.]com` → `47.107.224[.]89` (Alibaba Cloud, Shenzhen). This is the same domain and IP documented in the ENDLESSDOORS research (hardcoded into an ENDLESSDOORS init script).
- **Backup C2 (default when no primary is configured):** `www.findmyipaddr[.]com`. Not a failover — a device using the backup was never configured with a primary. The domain was **unregistered** at analysis time; **VulnCheck registered it and stand up a sinkhole** running a reverse-engineered `zbtProtocol` implementation.
- **Protocol:** UDP to port `10000`, internally named `zbtProtocol`. Outbound messages on the WE826-T2 are XOR-obfuscated with a single byte (`0x1f`); inbound commands are always plaintext. No encryption, no authentication — anyone on the network path can hijack the implants.

Command set (message types):

| msgType | Name | Effect |
|---|---|---|
| `0x1001` | reg | Device-fingerprint beacon (full `/tmp/info.txt`: model, firmware, MAC, uptime, SSID, LAN IP, GPS) |
| `0x2507` | cmdRun | Execute arbitrary commands |
| `0x2502` | pppoe | Exfiltrate WAN PPPoE username and password |
| `0x230b` | dnsSet | Write DNS hijack list, activate via `/usr/sbin/dns.sh` |
| `0x2306` | dnsGet | Return current DNS hijack list |
| `0x2405` | onoff | Open or close a reverse SSH tunnel |
| `0x2406` | sshport | Return current reverse SSH port |
| `0x2602` | setBackup | Update backup C2 server addresses |

**Sinkhole result:** as of August 21, 2026, **392 unique devices** had reported in (collection ongoing). 390 are in China, 83% on China Mobile's network, 304 broadcasting "CMCC" SSIDs; 363 are a single model (**L3_V2_8**, firmware `3.0.0.4.528`) that appears to be a China Mobile carrier CPE. The longest-running device had been beaconing for nearly two years. This is domestic Chinese surveillance technology at scale — and the same implants run on routers sold to U.S. consumers. The primary C2 `ac-link[.]com` is still live, so the full population is unknown and almost certainly much larger.

## DARKLANTERN (WAN listener backdoor)
Runs as the `infosrvd` service on **UDP `9992`**. The default firewall explicitly allows inbound UDP `9992` from anywhere on the internet, so it is reachable by design. Internally the protocol is called "revProto". Two packet types:

- **Info probe:** a fixed 19-byte packet. Send it to UDP `9992` and the device replies on UDP `8897` with model, firmware version, MAC, uptime, and other identifying data — in the clear. No authentication, no challenge, no session.
- **Command packet (type `0x17`):** carries a shell string that the service passes directly to `system("/etc/exec/cmd " + payload)`. A **semicolon in the payload breaks out of the fixed prefix** and executes arbitrary commands. No length limit, no character filtering — one packet for a root shell over the internet.

Two fields gate acceptance, and both are trivially defeated:
- **Token:** a four-byte keyed checksum = last four hex chars of `md5("mqonu.com" + payload)`. The key `mqonu.com` is hard-coded (MoreQuick), so anyone can compute a valid checksum for any payload.
- **MAC filter:** the packet's six-byte MAC field is compared to the device's own MAC in `/tmp/mac.txt` — but a **hard-coded bypass** accepts a packet whose MAC field is all zeros.

**Wild deployment:** between August 18–21, 2026, VulnCheck's scanner identified **203 internet-facing DARKLANTERN instances across 22 countries** (the first public view of the backdoor's deployment). Responding devices self-reported **16 different models**, confirming this is a firmware-level backdoor shipped with multiple products, not one defective device. These are older models (test-device firmware built 2019), likely the tail end of a larger installed base.

## File hashes
| File | Alias | SHA256 |
|---|---|---|
| `yunmgrd` | SPEAKINGSTONE | `b77811db4d218c65670a6c9a5b33c30ff81c6d779e15d658643138771178a818` |
| `infosrvd` | DARKLANTERN | `7e2e036fec2fe7ab4bbd43978d9296563894c92a112f5ac2f39957f12108e245` |
| `inetdetect` | watchdog (launches both) | `ae6c356f1f09260b859f84d994ef8423540a6c0bdf98510d86b85834283e4926` |

## Public network indicators
Treat these as detection and investigation pivots; IP ownership and DNS answers change, and blocking alone does not make an affected router trustworthy.

| Role | Endpoint | Reported resolution / hosting |
|---|---|---|
| SPEAKINGSTONE primary C2 | `ac-link[.]com` | `47.107.224[.]89` — Alibaba Cloud, Shenzhen |
| SPEAKINGSTONE backup C2 | `www.findmyipaddr[.]com` | Unregistered at analysis; now VulnCheck sinkhole |
| DARKLANTERN | any host responding on **UDP `9992`** (probe) / **UDP `8897`** (reply) | Internet-facing; 203 instances / 22 countries at last scan |
| SPEAKINGSTONE | outbound **UDP `10000`** to configured C2 | Phone-home beacon; model/fingerprint payload |

Also monitor the ZBT web interface and public-key fingerprints VulnCheck lists for asset discovery (FOFA/ZoomEye/Censys/Shodan pivots in the source post).

## Defender guidance
1. **Inventory by model and hardware identity, not brand.** Search cellular-CPE, RV/vehicle, branch, hotel, and pipeline/asset-management inventories for ZBT / MoreQuick model numbers (WE826, WG3526, WG2626, Z8102AX, WE1326, WE2426, WE5926, etc.) and for MAC OUI `78:A3:51`. Reseller logos are unreliable.
2. **Alert on the published endpoints and ports.** Correlate egress and inbound with device identity: outbound UDP `10000` to `ac-link[.]com` / `findmyipaddr[.]com`, and any internet-facing UDP `9992`/`8897`. Alert rather than silently block so deployed devices can be found.
3. **Block inbound UDP 9992 at the perimeter.** DARKLANTERN is only reachable when the device has a public (or port-forwarded) UDP `9992`. If a router in your estate answers a 19-byte probe on that port, it is compromised-by-design and must be isolated.
4. **Inspect and preserve evidence.** If shell access is available, capture `ps` (look for `yunmgrd`, `infosrvd`, `inetdetect`), network connections, startup scripts, the filesystem artifacts, firmware version, and the SHA256 hashes above before changing state.
5. **Isolate and replace.** Move suspected devices to a restricted network with deny-by-default egress. For any production or sensitive use, replace the device; do not rely on deleting a startup script as durable remediation.
6. **Rotate what the implants can reach.** Assume PPPoE/ISP credentials, Wi-Fi/VPN/admin credentials, and any DNS trust stored on or traversing an affected router are compromised when exposure cannot be ruled out; a DNS-redirect or reverse-SSH capability means downstream devices are also in scope.

## Assessment limits
- VulnCheck attributes the firmware to ZBT / Shenzhen Zhibotong Electronics and MoreQuick (OEM), but it does not identify the operator of the configured primary C2 or document malicious tasking received by deployed devices.
- The two implants are "shipped by design"; the white-label population beyond the named brands is unknown, and matching a reseller brand or hardware appearance alone is not confirmation.
- The DARKLANTERN scan (203 instances, 22 countries) and the SPEAKINGSTONE sinkhole (392 devices, near-uniformly China Mobile carrier CPEs) are point-in-time views of a still-moving population; the live primary C2 implies a larger, uncounted base.
- No CVE is assigned to these two implants in the cited source (ENDLESSDOORS was CVE-2026-66747). Treat this as a device-trust problem, not a patchable flaw.

## Source
- VulnCheck: [Chinese Implants in the Supply Chain](https://www.vulncheck.com/blog/zbt-darklantern-speakingstone) — August 27, 2026 (Jacob Baines). Follow-up to the [ENDLESSDOORS implant in Zbtlink router firmware](endlessdoors-zbtlink-router-firmware-implant.md) page.
