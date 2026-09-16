# NightEagle (APT-Q-95) expands to Russian companies: GhostContainer on Exchange via VIEWSTATE injection, C2 hidden in `x-owa-urlpostdata` headers, Microsoft dev tunnels + rdp2tcp as the covert RDP channel, BlueKeep and DCSync for domain takeover (Kaspersky GERT, Sep 16, 2026)

## Tags
- ops
- operations
- NightEagle
- APT-Q-95
- GhostContainer
- Microsoft Exchange
- VIEWSTATE
- ASP.NET machine keys
- CVE-2020-0688
- GhostWebShell
- ysoserial
- Neo-reGeorg
- x-owa-urlpostdata
- AMSI bypass
- amsi.dll patching
- event log unhooking
- Microsoft dev tunnels
- devtunnels.ms
- rdp2tcp
- RDP tunneling
- portproxy
- atexec
- Impacket
- BlueKeep
- CVE-2019-0708
- Kerberos
- Forwardable tickets
- DCSync
- Active Directory
- GitHub tool hosting
- Cloudflare WARP
- compromised VPN credentials
- Kaspersky GERT
- MITRE ATT&CK

## Summary

Kaspersky GERT (Global Emergency Response Team) published on **September 16, 2026** a set of incident investigations of **NightEagle** (aka **APT-Q-95**), a group active since at least **2023** that historically focused on organizations in **Asia** and has now been observed attacking **businesses in Russia**. The durable value of the report is the toolkit and tradecraft, not the geography: an in-memory Exchange backdoor built by assembling **public GitHub components**, C2 smuggled inside a **legitimate-looking OWA header**, remote access maintained through **Microsoft's own dev-tunnel service** plus **rdp2tcp**, and domain takeover via **BlueKeep + DCSync**.

**Initial access:** in most incidents the attackers used **compromised valid credentials** against corporate VPNs. VPN connections originated from IP addresses in the **Russian segment associated with Cloudflare WARP tunnels** and from **European virtual infrastructure providers** — a privacy-relay-over-target-country pattern that keeps source lookups uninformative.

**GhostContainer on Microsoft Exchange.** During initial access and again as attacks progressed, the group deployed the **GhostContainer** backdoor on Exchange servers. The implant **incorporates components from several open-source projects, all public on GitHub**: the **Neo-reGeorg** tunnel, an exploit for **CVE-2020-0688** (the Exchange viewstate validation-key privilege escalation), and the **GhostWebShell** class from **ysoserial**. Kaspersky could not determine the exact delivery method but assesses **with high confidence** that the group used its previously documented technique: **extract the cryptographic keys used by Microsoft Exchange from the ASP.NET configuration, overwrite the VIEWSTATE framework parameter, and inject a payload into it** that launches GhostContainer in memory. Detection name: `Trojan.MSIL.GhostContainer.gen`; KTAE similarity ties new samples to earlier GhostContainer/NightEagle collections.

## GhostContainer internals

The backdoor is a **.NET assembly with three classes**:

| Class | Function |
|---|---|
| `Stub` | Processes C2 commands delivered to the infected system **through `x-owa-urlpostdata` headers**; evades **AMSI** and **Windows Event Log** mechanisms by **overwriting addresses in `amsi.dll` and `ntdll.dll`** |
| `App_Web_843e75cf5b63` | Accepts `fakePath` / `fakePageName` parameters and creates **virtual paths** that redirect requests to the proxying class |
| `App_Web_8c9b251fb5b3` | Implements **network traffic redirection (proxying) and socket forwarding** |

The C2 channel rides a header that OWA itself uses for legitimate postback data — a header-based channel embedded inside normal Outlook-on-the-web traffic, invisible to any inspection that treats `x-owa-urlpostdata` as trusted app noise.

## Traffic redirection: legitimate services as the covert channel

Once privileged, the group moves laterally over RDP using two tools **combined** — both "allowed" by design:

1. **Microsoft dev tunnels** — a legitimate Microsoft mechanism that publishes local web services to the internet on `*.*.devtunnels.ms` domains. The attackers used it to **expose port 3389 (RDP)** on compromised systems. Egress looks like Microsoft infrastructure traffic; no suspicious port is opened.
2. **rdp2tcp** — a public tool that **tunnels arbitrary TCP traffic over an established RDP connection** (server component on the target, client on the attacker side).

**The durable forensic tell is in the RDP event log:** opening/closing RDP virtual channels writes **events 132 (channel opened) and 148 (channel closed)** in `Microsoft-Windows-RemoteDesktopServices-RdpCoreTS/Operational`. Legitimate RemoteFX sessions name channels `XPSRD`, `cliprdr`, `Microsoft::Windows::RDS::DisplayControl`, etc. **A channel named `rdp2tcp` — or arbitrary random alphanumeric channel names — is the attacker.**

The group also used **Impacket's `atexec`** to create scheduled tasks running **`netsh interface portproxy add v4tov4`** port-forwarding (e.g. `listenport=443 connectaddress=10.0.12.101 connectport=445`) — standard Windows functionality abused for internal pivoting.

**Tool staging on GitHub:** archived tools were hosted in **GitHub repositories with legitimacy-mimicking names**, and the binaries inside were named after unrelated legitimate software:

- `https://github[.]com/mirror-js/mirror-js/refs/heads/main/js/js-webpack.zip`
- `https://github[.]com/mirror-js/mirror-js/refs/heads/main/js/jsonp-pack.zip`
- `https://github[.]com/browserthemes/resourcepack/releases/download/main/resource-pack.zip`
- Binary names: `adobe_32.exe`, `AdobeSync.exe`, `trueconf.exe`, `1cbroker.exe`, `1c-office-plugin.exe`, `trueconf-broker.exe` (Adobe and **TrueConf** video-conferencing masquerades; the 1C names target the Russian-market accounting stack, consistent with the new Russian victimology).

## Lateral movement and domain compromise

- **Active Directory vulnerability exploitation** through the established tunnels to elevate and move.
- **CVE-2019-0708 (BlueKeep)** in one incident: the group used the vulnerable mechanism **to create a local account and add it to the Administrators and Remote Desktop Users groups** — a 2019 wormable RCE still serving as an account-creation primitive in 2026. KATA signature: `Exploit.CVE-2019-0708.TCP.C&C`; memory dumps retained exploit artifacts.
- **Non-standard Kerberos ticket requests** with the **`Forwardable`, `Proxiable`, `Renewable`** flag combination — long-lived delegable tickets for patient access.
- **DCSync**: attempted replication of the **Domain-Password object** from the AD database to impersonate the domain controller, harvest domain password hashes, and ultimately compromise domain controllers and the **entire Active Directory infrastructure**.

## Detection guidance (durable)

- **RdpCoreTS event log**: hunt virtual-channel **events 132/148 with non-canonical channel names** (`rdp2tcp`, random strings) — this single query catches the dev-tunnel + rdp2tcp combo regardless of payload.
- **OWA logs / traffic inspection**: `x-owa-urlpostdata` content that is not ASP.NET postback data; ASP.NET requests carrying injected VIEWSTATE payloads; unexpected changes to **ASP.NET machine-key** material on Exchange servers.
- **Endpoint**: `netsh interface portproxy` invocations, `atexec`-style scheduled-task creation (Impacket patterns), process trees spawning tunnel binaries named after Adobe/TrueConf/1C software, .NET assembly loading via PowerShell reflection.
- **Identity**: Kerberos TGT/TGS requests with Forwardable+Proxiable+Renewable outside normal admin workflows; **DCSync replication requests** (`potential_dcsync_via_startupparameters`-class detections).
- **Perimeter**: `*.devtunnels.ms` connections from non-development hosts — the service is legitimate, which is exactly why it is invisible to blocklist-based egress controls; alert on the *host-role mismatch*, not the domain.
- **Patch posture**: the published attack path assumes unpatched **CVE-2019-0708 (BlueKeep)** and **CVE-2020-0688** — this campaign is a reminder that seven-year-old Exchange/RDP holes remain an effective APT entry point where patch cycles stall.

## Kaspersky publish rules

Kaspersky published detection scenarios in its rules repository: `suspicious_assembly_loading_into_powershell_via_reflection`, `detection_of_access_to_tunnel_domains_dns`, `impacket_possible_activity`, `attempt_to_download_hacktool_or_risktool_by_non_browser`, `credentials_dumping_tools_file_artifacts_creation`, `potential_dcsync_via_startupparameters`, plus KATA network signatures for BlueKeep exploitation, tunneling variations, and AD attacks (DCSync, AD CS attempts).

## Indicators of compromise (MD5, as published)

| MD5 | Filename(s) |
|---|---|
| `1dcafb7f8448683281106b06dd22409a` | `AdobeSync.exe` |
| `1f3034b706c78b35d8e34044e68c693a` | `adobe_32.exe` |
| `3ecd1cd627d0340c92901a478a7caad8` | (tunneling tool) |
| `631fb131a56caf4ca0f287ed73e876ab` | `App_Web_Container_1.dll` (GhostContainer) |
| `4aa9fb1bf9223dfcdac920759bc7a3c7` | `1c-office-plugin.exe`, `1cbroker.exe`, `trueconf.exe` |

GitHub infrastructure: `https://github[.]com/mirror-js/mirror-js`, `https://github[.]com/browserthemes/resourcepack`

## MITRE ATT&CK (selected)

- T1190 — Exploit Public-Facing Application (Exchange VIEWSTATE injection / GhostContainer)
- T1078 — Valid Accounts (compromised VPN credentials)
- T1505.003 — Web Shell / in-memory web-application backdoor (GhostContainer)
- T1105 / T1090 — ingress tool transfer via GitHub; tunneling (Neo-reGeorg, dev tunnels, rdp2tcp, portproxy)
- T1562.001 / T1562.002 — Impair Defenses / disable Windows event logs (amsi.dll + ntdll.dll patching)
- T1021.001 — Remote Services: RDP (BlueKeep-created accounts, dev-tunnel-exposed 3389)
- T1558.003 / T1003.006 — Kerberos tickets (Forwardable/Proxiable/Renewable), DCSync
- T1053.005 — Scheduled Task/Job: `atexec`

## Monitoring

- Whether NightEagle's Russian-business victimology persists or re-centers on its historical Asian targets.
- Rotation of the GitHub repositories/binaries (both repos are live-public indicators — expect quick churn).
- Adoption of the **dev-tunnel + rdp2tcp** pattern by other groups (the technique is generic and cheap; this report is the first APT attribution Kaspersky publishes for it in this configuration).
- Whether the `x-owa-urlpostdata` C2 header appears in other campaigns' traffic.
- Additional GhostContainer variants beyond the three-class layout; Kaspersky notes KTAE similarity ties to earlier samples — watch for re-compilation with different class names.

## References

- Kaspersky Securelist / GERT (Sep 16, 2026): <https://securelist.com/tr/nighteagle-apt-ghostcontainer-and-tunneling/121323/>

## Related

- [Gamaredon 2025 tunnels and workers](gamaredon-2025-tunnels-workers-dead-drops.md) — another campaign where tunneling utilities are the durable pivot rather than the payload
- [Wiz "Artifactory Under Attack"](wiz-artifactory-in-the-wild-cve-2026-42016-42018-82329-september-2026.md) — same "legitimate platform feature as covert channel" pattern, different substrate
