# UTA0533 SonicWall SMA1000 zero-day compromise

## Summary
Volexity attributed a June-July 2026 SonicWall SMA1000 appliance intrusion to a previously undocumented cluster it calls **UTA0533**. The actor chained **CVE-2026-15409** and **CVE-2026-15410** as zero-days to reach localhost-only services, execute code, escalate to root, install memory-injected Java implants, capture unencrypted LDAP traffic, and attempt internal pivots.

The earliest observed compromise was June 22, 2026. SonicWall disclosed and patched the vulnerabilities in July; CISA added both to KEV. This page adds the post-disclosure forensic chain and compromise indicators to the earlier KEV record.

## Tags
- ops
- operations
- UTA0533
- SonicWall
- SMA1000
- CVE-2026-15409
- CVE-2026-15410
- zero-day
- active exploitation
- edge appliance
- VPN
- SSRF
- WebSocket
- privilege escalation
- root access
- credential theft
- KNUCKLEBALL
- ROOTRUN
- ORANGETAIL
- Suo5
- Behinder
- web shell

## Affected scope
Rapid7 lists SMA1000 Series models 6210, 7210, and 8200v on vulnerable builds `12.4.3-03245`, `12.4.3-03387`, `12.4.3-03434`, `12.5.0-02283`, `12.5.0-02624`, and `12.5.0-02800`. The flaws do not affect the SMA 100 Series or SSL VPN functionality on SonicWall firewalls. Consult SonicWall's live advisory for current fixed hotfixes rather than treating this summary as a version authority.

## Exploit and persistence chain
1. **CVE-2026-15409:** an unauthenticated `/wsproxy` request using `User-Agent: SMA Connect Agent` and a `bmID` beginning `-3389` opens a WebSocket tunnel to localhost-only services. Volexity observed ports 1050 and 8188; Rapid7 demonstrated non-root execution through the CouchDB Erlang service.
2. The actor used the appliance's CouchDB context to write and execute files and obtain access needed for the next stage.
3. **CVE-2026-15410:** path traversal in the `remove_hotfix` workflow causes a staged script to execute as root.
4. **ROOTRUN**, written as `/usr/bin/xzfind`, is a setuid ELF utility that runs supplied shell commands as root.
5. **KNUCKLEBALL**, `/usr/lib/python3.11/site-packages/deploy_new.py`, uses the Java Attach API to inject two JAR agents into the legitimate SonicWall WorkPlace JVM.
6. One JAR contains a user-agent-gated **Suo5** HTTP proxy. The other contains **ORANGETAIL**, a Behinder-like custom Java web shell.
7. Persistence was added to `/etc/init.d/workplace`, and `/var/lib/unit/conf.json` was modified to proxy attacker-created external routes to the injected implants.
8. On a second appliance, UTA0533 staged `tcpdump` scripts under `/var/tmp` to capture cleartext LDAP traffic and extract usernames and passwords.

## High-value detection pivots
### Web and application logs
- In `/var/log/aventail/extraweb_access.log`, requests to `/wsproxy` with `bmID=-3389...`, `serviceType=SSH`, localhost-like host values, destination ports 1050/1051/8188, and HTTP `101` upgrades.
- Successful POST requests to unexpected routes such as `/__api__/login` and `/__api__/logout`.
- `/var/log/aventail/ctrl-service.log` entries containing `running hotfix removal for:` followed by `../` traversal into `/tmp` or `/var/tmp`.
- The impossible-looking implant gate:
  `Mozilla/6.0 (Windows NT 11.0; Win64; x64) AppleWebKit/1537.136 (KHTML, like Gecko) Chrome/149.0.0.1 Safari/1537.136`

### Files and configuration
- `/usr/bin/xzfind` or any unexpected setuid binary.
- `/usr/lib/python3.11/site-packages/deploy_new.py`
- `/tmp/hypdate.b64`, `/tmp/1234.sh`, `/tmp/agent_wp8.jar`, `/tmp/agent_wp9.jar`, `.attach_pid*`, or `.java_pid*` artifacts.
- Unexpected files or packet captures under `/var/tmp`, especially `lib.sh` launching `tcpdump` against TCP/389.
- `/etc/init.d/workplace` launching `deploy_new.py`.
- `/var/lib/unit/conf.json` routes that map `/__api__/login` or `/__api__/logout` to `http://127.0.0.1:8085`, `/workplace/error.jsp`, or `/workplace/dialogs/errorDialog.jsp`.

### Selected SHA-256 indicators
- ROOTRUN / `xzfind`: `81a9af3846bad3a1107164ff7cf0a08e020b31a3b32fd17866e17d4c1565f7f2`
- KNUCKLEBALL / `deploy_new.py`: `8c470301dcb7278f73e622f1950073567b34011c64b60cdfbb0f89803923a5a3`
- Suo5 agent / `agent_wp8.jar`: `1e1e68bbb899450a57274a8b12082ed4e2040a2aae77014f20431689d2b4edee`
- ORANGETAIL / `agent_wp9.jar`: `ea9154e374e4f77bc2cf54282e23543573980342a85bc888cb23f20b8bbba081`

Volexity observed more than 200 source IPs, including commercial VPN infrastructure. Use its public IP list only with time and request-path context; IP-only blocking is low confidence and short lived.

## Defender guidance
- Patch to SonicWall's fixed platform hotfix immediately. Because exploitation predates disclosure, patching alone does not establish device integrity.
- Before rebooting or rebuilding, preserve RAM, disk, `/var/log/aventail/*`, `/var/lib/unit/conf.json`, `/etc/init.d/workplace`, `/tmp`, and `/var/tmp`. Volexity found that a reboot removed memory-resident evidence on one appliance.
- Compare appliance files and configuration to a trusted baseline; enumerate unexpected setuid files and review all NGINX Unit routes.
- Hunt internal telemetry for authentication attempts originating from the SMA appliance, LDAP credential exposure, traffic captures, and outbound or lateral proxy traffic. Treat credentials processed or cached by a compromised appliance as exposed.
- Rotate credentials only after isolation and persistence removal. Rebuild a confirmed-compromised appliance from trusted media/configuration, then investigate downstream VPN and identity systems.
- Deploy Volexity's public YARA rules and retain behavioral detections because filenames and routes can be changed.

## Attribution caveat
Volexity's **UTA0533** label identifies a previously undocumented activity cluster, not a publicly attributed government or criminal group. The use of Suo5, Behinder-like techniques, VPN exit nodes, and appliance zero-days does not by itself support a stronger attribution.

## Related pages
- [CISA KEV: Microsoft SharePoint / ADFS, FortiSandbox, and SonicWall SMA1000 July 2026 additions](cisa-kev-microsoft-sharepoint-adfs-sonicwall-sma1000-july-2026.md)
- [VerdantBamboo appliance BRICKSTORM operation](verdantbamboo-appliance-brickstorm-operation.md)
- [Check Point VPN CVE-2026-50751 exploitation](check-point-vpn-cve-2026-50751-exploitation.md)

## Sources
- Volexity: [Proxying to Compromise: SonicWall Secure Mobile Access 0-Day Exploitation](https://www.volexity.com/blog/2026/07/17/proxying-to-compromise-sonicwall-secure-mobile-access-0-day-exploitation/)
- Rapid7: [SonicWall SMA1000 zero-days actively exploited: CVE-2026-15409 and CVE-2026-15410](https://www.rapid7.com/blog/post/etr-rapid7-mdr-team-discovers-new-sonicwall-sma1000-zero-days-being-actively-exploited-cve-2026-15409-cve-2026-15410/)
- SonicWall PSIRT: [SNWLID-2026-0008](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0008)
- CISA Known Exploited Vulnerabilities catalog: <https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>
