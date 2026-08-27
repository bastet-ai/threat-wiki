# ENDLESSDOORS implant in Zbtlink router firmware

## Summary
**ENDLESSDOORS** is VulnCheck's name for an unauthenticated remote-control implant that its researchers found enabled by default in firmware for 20 Zbtlink router models. The userland `kworker` process runs as root, connects outbound to fixed command-and-control endpoints, and executes arbitrary server-supplied commands through `popen()`. A reserved `rctlbash` command opens a second connection and provides an interactive root shell.

VulnCheck assigned **CVE-2026-66747** and reports that all roughly two dozen firmware images available from Zbtlink's download page contained the implant. There is no fixed firmware. Because Zbtlink offers OEM and ODM services, affected hardware can carry Zbtlink, ZBT, ZBTWiFi, Wiflyer, or an unrelated reseller brand; defenders should identify devices by model number rather than case branding.

## Tags
- ops
- operations
- ENDLESSDOORS
- CVE-2026-66747
- Zbtlink
- Shenzhen Zhibotong Electronics
- Wiflyer
- OpenWrt
- router compromise
- embedded Linux
- firmware backdoor
- supply-chain risk
- command and control
- unauthenticated RCE
- root shell
- outbound C2
- IoT
- VulnCheck

## Why this matters
- The implant is present in vendor-published firmware and starts at boot; exploitation does not require a separate vulnerability or inbound internet exposure.
- Its outbound connection traverses NAT and ordinary stateful firewalls. A router can therefore remain controllable from inside a branch, hotel, office, or vehicle network even when it has no public management interface.
- The protocol provides neither client nor server authentication and no transport encryption. Anyone able to control DNS resolution, the configured endpoint, or the network path can impersonate the server and execute commands as root.
- White-label distribution means logo- or manufacturer-name inventory can miss affected units.
- Disabling one startup item does not restore trust in firmware that shipped an undocumented root command channel. Replacement is the safest response.

## Implant and protocol
The implant is based on the public 2015 `rctl` (`remote control linux`) project. VulnCheck found customized `rctl` components in Zbtlink firmware and named the resulting implant ENDLESSDOORS.

### Host artifacts
- Two ordinary userland processes named `kworker`, running as root. Unlike genuine kernel workers, they appear without square brackets and have nonzero virtual memory sizes.
- `/usr/sbin/kworker`
- `/usr/lib/librctl.so`
- `/etc/kworker.cfg`
- `/etc/init.d/skworker`

### Command channel
1. The implant initiates an outbound connection to TCP port `7000`.
2. It registers with a fixed 39-byte message: a null-padded 33-byte class label followed by the LAN MAC address.
3. The server can send an arbitrary command, which the client passes to `popen()` as UID 0.
4. The reserved string `rctlbash` causes the client to connect to TCP port `7001`, allocate a pseudo-terminal, spawn `/bin/sh`, and bridge the shell over that connection.

VulnCheck reproduced takeover by answering a lab router's outbound connection and delivering a root-shell payload. This establishes exploitability of the analyzed firmware; the report does not claim observed malicious tasking of deployed routers.

## Affected models
VulnCheck confirmed ENDLESSDOORS in firmware for these model numbers:

- `CPE2801`
- `WE1026-5G-WD`
- `WE1326`
- `WE2007`
- `WE2008-DSIM`
- `WE2416`
- `WE3326`
- `WE5927`
- `WE5931`
- `WE5931AC`
- `WE826-T3-DSIM`
- `WG108`
- `WG1602`
- `WG1608-DSIM`
- `WG209`
- `WG2105`
- `WG2107`
- `WG259`
- `WG3526`
- `Z8102AX-2DSIM` / `Z8102AX`

The researchers examined 21 firmware images spanning these 20 models. They caution that OEM/ODM rebadging can expand the real affected population beyond the tested names and brands.

## Public network indicators
Treat these as detection and investigation pivots. IP ownership and DNS answers can change, and blocking alone does not make an affected router trustworthy.

| Role | Endpoint | Reported resolution / hosting |
|---|---|---|
| Primary | `zbtctl.epplink[.]net` | `47.100.190[.]96` — Alibaba Cloud, Shanghai |
| Primary | hard-coded address | `47.107.224[.]89` — Alibaba Cloud, Shenzhen |
| Secondary | `online-string[.]com` | `45.32.81[.]152` — Vultr |
| Secondary | `rbdg4nzqadui.wikaba[.]com` | `43.248.136[.]125` — Jiangsu Dongyun Cloud |

Also monitor outbound TCP `7000` and `7001` from router, cellular-CPE, and network-infrastructure segments.

## Defender guidance
1. **Inventory by model and hardware identity.** Search purchasing, contractor, branch, hotel, vehicle, and cellular-CPE inventories for the affected model numbers and for Zbtlink, ZBT, ZBTWiFi, Wiflyer, or unbranded devices.
2. **Alert on the published endpoints and ports.** Correlate DNS and egress connections with device identity; preserve connection timing and resolver logs. Alert rather than silently block so deployed devices can be found.
3. **Inspect reachable devices.** If shell access is available, capture `ps`, network connections, startup scripts, the four listed filesystem artifacts, firmware version, and hashes before changing state. Two unbracketed `kworker` processes with nonzero VSZ are the reported runtime signal.
4. **Isolate and replace.** Move suspected devices to a restricted network with deny-by-default egress. Replace them for any production or sensitive use; do not rely on deleting the startup script as a durable remediation.
5. **Scope exposure.** Review traffic and adjacent-system logs for unexpected connections sourced from the router. Rotate administrative, Wi-Fi, VPN, cellular-management, and other credentials that were stored on or traversed an affected device when exposure cannot be ruled out.
6. **Preserve evidence.** If active tasking is suspected, capture volatile process and network state plus a firmware/filesystem image before rebooting, when operationally safe.

## Assessment limits
- VulnCheck attributes the firmware and devices to Zbtlink / Shenzhen Zhibotong Electronics, but it does not identify the operator of the configured infrastructure or document malicious commands received by deployed devices.
- The researchers characterize the component as intentionally shipped rather than an accidental software defect and therefore did not notify Zbtlink before publication. That intent assessment is the researcher's conclusion; the public record cited here does not include a vendor response.
- Twenty models and 21 public firmware images were verified. The white-label population is unknown, and matching hardware appearance or a reseller brand alone is not confirmation.
- CVE-2026-66747 describes the unauthenticated command channel. At publication, the cited source reports no fixed firmware and recommends treating the issue as a device-trust problem.

## Source
- VulnCheck: [ENDLESSDOORS Is Phoning Home. Pick Up.](https://www.vulncheck.com/blog/zbt-endlessdoors) — August 5, 2026
- Follow-up: VulnCheck published two further implants in the same ZBT / MoreQuick firmware lineage on August 27, 2026 — see [SPEAKINGSTONE and DARKLANTERN: two more implants in ZBT / MoreQuick router firmware](speakingstone-darklantern-zbt-router-implants.md).
