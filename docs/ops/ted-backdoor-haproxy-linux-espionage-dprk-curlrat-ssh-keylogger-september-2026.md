# "ted backdoor": DPRK-linked Linux espionage toolkit — HAProxy 2.8.12 trojan plus CurlRAT and SSH keylogger targeting South Korean media and automotive sectors

## Tags
- ops
- HAProxy
- ted backdoor
- CurlRAT
- SSH keylogger
- Linux
- South Korea
- media sector
- automotive sector
- DPRK APT
- APT37
- trojanized daemons
- crond
- agetty
- atd
- sshd
- polkitd
- filter API
- browser session hijacking
- credential harvesting
- long-term surveillance
- Rapid7
- MITRE ATT&CK

## Summary
On **September 4, 2026**, Rapid7 Labs disclosed a **previously undocumented Linux espionage toolkit** — built around a backdoor it names the **"ted backdoor"** — that has been used to **target organizations across South Korea's automotive and media industries** with minimal detection. Rapid7 attributes the campaign **with medium confidence to DPRK APTs**, citing the target sectors (long-term espionage), simple XOR-based encryption and a custom substitution cipher, and the fact that the hardcoded C2 list is **associated to APT37 (Lazarus) on ThreatFox**.

The toolkit's defining feature is the depth of its integration with the victim environment. The **ted backdoor is compiled into the victim's existing HAProxy 2.8.12** build (a trojanized **HAProxy 2.8.12-0fdb194**, released November 22, 2024 — the earliest possible compilation date; the earliest VirusTotal uploads of its components date to **mid-2025**). It uses HAProxy's **native filter API, internal memory pools, event scheduler, and process-management infrastructure** to intercept web traffic and hide from monitoring while genuine load-balancing traffic continues normally. Operating alongside it are an **SSH keylogger**, a **curl-based RAT (CurlRAT)**, and a **stager**, plus **trojanized system daemons: crond, agetty, atd, sshd, and polkitd**.

The framework enables **remote command execution on compromised servers, injection of malicious scripts into web traffic, credential harvesting, and long-term surveillance** — an espionage posture, not a monetizing one.

## Components and capabilities
- **ted backdoor (HAProxy-embedded):** compiled as part of HAProxy 2.8.12, using the filter API, memory pools, event scheduler, and process management to intercept traffic, hide from monitoring, and keep real load-balancing operational. It tunnels its C2 **as HTTP through the load balancer** and blacklists known scanner IPs.
- **CurlRAT:** a curl-based remote access trojan. It maintains a **watchdog thread that polls `/proc/haproxy.pid` hourly** and tracks started/stopped/restarted/reloaded states, reporting them to the operator's infrastructure over a `writeservice_info` endpoint. It performs **sandbox evasion** (checks `/usr/lib/libvirtlog.so.0` before activating and aborts in a virtualized environment), sends a **10 KB system-info structure**, and validates a victim token before dispatching commands. All C2 payloads are **Base64-encoded after feedback XOR**; it polls C2 over HTTPS with a **libcurl fallback to HTTP**, sending payloads as `application/x-www-form-urlencoded` POST. On config-validation failure it **falls back to secondary C2 `img.monderhouse.space`**; `img.darklights.store` is used as a **backup config host**. The victim ID is derived from **hostname + IP + hardware UUID + cron version string, MD5'd and uppercased**, and sent as a `User-token` header on every C2 request.
- **SSH keylogger:** a **PAM (pluggable authentication modules) module** that intercepts plaintext passwords. Captured credentials are saved to an **encrypted log at `/var/lib/sshd/c8c68e629bba773a10ac80012d10bf19`**, encrypted with a **substitution cipher** before writing.
- **Passive web-session capture engine (ted):** intercepts HTTP sessions and harvests **source IP, host, URL, referer, user-agent, and Accept-Language** via regex-gated filters; it can **replace or append a decrypted payload script to response bodies**, rewriting `Content-Type`, `Content-Length`, and `Content-Disposition`, forcing a 200 OK, and stripping `Accept-Ranges`. Timestamped records are written per matched request, with expanded records when the Accept-Language key is present.
- **Interactive shell tunnel:** tunnelled **through the HAProxy HTTP pipeline via named FIFOs**, with response exfiltrated via a raw `send()` on the TCP socket to **bypass HAProxy logging**.
- **Trojanized daemons (crond, agetty, atd, sshd, polkitd):** the same stager/RAT pattern as HAProxy, but without the HAProxy monitor. The agetty and polkitd variants spawn a thread to run **CurlRAT reaching `img.worksongo.store` and `img.socialteams.store`** respectively.

## C2 infrastructure
The hardcoded C2 set (ThreatFox-associated to **APT37**) follows a consistent **`img.<name>.<tld>`** naming convention that Rapid7 reads as a **shared registration workflow rather than ad-hoc infrastructure**. `img.responsive.pstatic.autos` **mimics Naver's** `pstatic.net` asset domain. Observed hosts:
- `img.monderhouse.space` (primary / secondary C2)
- `img.smartnords.site`
- `img.darklights.store` (backup config host; `api_token/ecd427ea8...` on network failures)
- `img.responsive.pstatic.autos` (Naver-mimicking)
- `img.socialteams.store`
- `img.worksongo.store`

## MITRE ATT&CK techniques
Rapid7 mapped the toolkit across a wide technique surface, including:
- **T1497.001** Virtualisation/sandbox evasion (CurlRAT `libvirtlog.so.0` watchdog)
- **T1480** Execution guardrails (stager deploys only if HAProxy or cron are detected; CurlRAT validates victim token; ted blacklists scanner IPs)
- **T1556.003** Modify authentication process: PAM (SSH keylogger plaintext capture)
- **T1539** Steal web session cookie (passive capture engine)
- **T1082** System information discovery (stager profiling + CurlRAT 10 KB beacon)
- **T1185** Browser session hijacking (response-body script injection)
- **T1071.001** Application layer protocol: web protocols (ted C2 over HTTP; CurlRAT over HTTPS/HTTP)
- **T1132.001** Data encoding: standard encoding (Base64 + feedback XOR; ted raw bytes with rolling XOR session key)
- **T1572** Protocol tunnelling (interactive shell via HAProxy named FIFOs, raw `send()` exfil)
- **T1568** Dynamic resolution (MD5-derived victim ID as `User-token`)
- **T1041** Exfiltration over C2 channel
- **T1560** Archive collected data (substitution-cipher SSH log; feedback XOR + Base64 outbound)

## Indicators of compromise (IOCs)
Rapid7 published SHA-256 hashes for the components (C2 configuration / payload artifacts):
```
5db1b6d52faf60b4f32d6fd0c7c938e4d05d29a14c32ded4a9668357c08b6a91
09739441ed4599bac2f8159028f772f71e4b25c8badfff95574e56d7384f3dbe
fea1bc36632c71e5a839803469ef60ac47595d36b2c50934ac109ade6df06e61
83f7d565b0465546027052b597af46eae3a199e7a91fcc2ab936341147349130
7007a78d50a993cb174c685eba96eb442c9507e38fd9d8e5dffc712f613ec110
6cf1b5e92a9c0756f597a5ddefb38eba32961c52efac7ab2a0aa52c639a8fc53
ed72f4cd8d467b5c5d95ae6aeca4aaeea14d79565d379c1ca5871a714727be16
feeea9d0bf6ae7396d28271baa51ae50df5169ce5d32a516865856f91abc50b3
d53c760c23b4405eb04ad0f20ead375440344b3bdf1fb7854ed12e40d155eabe  (cronie)
2f02b09d61d432134e994ad671258f523bbf289ae6091fd4eae192c60bd51b6f  (agetty)
8f30b57928934ae67478d0e690c91d046e35a638da098d02922a4a88a0fdb66c  (atd)
a1d8af3a6acb731f07f72040eccb3450c1c83d40e29f736c2a63d35388660be4  (polkitd)
12810854c8b2c391b23e2e18b013e873d0369b0637aa3cf993136c07188ba3b8
009a1e2d7a582a24e50cf2ffc2a005482c8e38f22bf5ed416053855f8d054e1e
4bb923eb040aa13ca8fd409c31ee4729c60ddff32e350efe1c5a4a9168a065f5
```
C2 domains (defanged): `img.monderhouse[.]space`, `img.smartnords[.]site`, `img.darklights[.]store`, `img.responsive[.]pstatic[.]autos`, `img.socialteams[.]store`, `img.worksongo[.]store`.

## Why this matters
- **The load balancer is the backdoor.** Embedding the implant inside the HAProxy filter API and process lifecycle means the C2 traffic, the credential capture, and the session hijacking all ride on a process the operator trusts to be doing legitimate work — genuine load balancing continues while the toolkit surveils. The durable tell is a **HAProxy that is intercepting and rewriting responses it should only be routing**, not a new process on the box.
- **It is an espionage kit, not a ransomware drop.** Remote command execution, web-traffic script injection, PAM-level SSH credential capture, browser-session hijacking, and hourly HAProxy health reporting are the signatures of **long-term surveillance**, and the medium-confidence DPRK / APT37 association (South Korean media + automotive) puts it in the state-sponsored espionage lane.
- **Trojanized system daemons widen the surface.** Compromised `crond`, `agetty`, `atd`, `sshd`, and `polkitd` mean persistence and credential capture are not confined to HAProxy — a clean HAProxy rebuild alone does not remove the backdoor.

## Detection / defensive heuristics
- **Hunt for the `img.<name>.<tld>` C2 naming pattern** and the specific domains above; the consistent `img.` prefix across `.space`/`.site`/`.store`/`.autos` is the registration-workflow tell.
- **Alert on HAProxy processes rewriting response bodies** (Content-Type/Content-Length/Content-Disposition changes, forced 200, stripped Accept-Ranges) for traffic that should be pure routing.
- **PAM integrity:** monitor for unexpected PAM modules in `sshd`'s auth chain and the **encrypted credential log at `/var/lib/sshd/c8c68e629bba773a10ac80012d10bf19`**.
- **Watchdog behavior:** a non-HAProxy process **polling `/proc/haproxy.pid` hourly** and reporting to `writeservice_info` is a high-signal CurlRAT indicator.
- **Daemons:** verify `crond`, `agetty`, `atd`, `sshd`, and `polkitd` binary hashes against known-good — trojanized variants here are the persistence, not just the entry.
- **Sandbox-evasion correlation:** a process that checks `libvirtlog.so.0` and aborts in a VM, then MD5s `hostname+IP+hardware UUID+cron version` into a `User-token` header, is the CurlRAT fingerprint.

## Assessment limits
- **Attribution is medium confidence.** Rapid7 ties it to DPRK APTs on sector targeting, primitive encryption (XOR + substitution cipher), and ThreatFox APT37 C2 association — a reasonable but not conclusive inference.
- **Earliest-compilation bound is structural** (the HAProxy 2.8.12-0fdb194 release date of November 22, 2024 and mid-2025 VirusFirst uploads), not a confirmed first-seen.
- **No named victims, payment, or exfiltration scope** is disclosed; the campaign is described as long-term surveillance of South Korean media and automotive organizations.
- **IOC set is Rapid7-published only**; independent confirmation of the hashes and C2 across other vendors has not been recorded in this page.

## Related pages
- [ulid-xyz transitive delivery chain / MicrosoftSystem64 RAT (DPRK-linked cross-platform implant, same "persistence name is the durable tell" logic)](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md)
- [RMM phishing campaign spanning 46 countries (ANY.RUN, Sep 4 — same scan window)](rmm-phishing-campaign-46-countries-verbatim-disposable-infra-anyrun-september-2026.md)
- [Kimsuky / Emerald Sleet / TA427 (DPRK APT actor profile — context for the DPRK espionage lane)](../actors/kimsuky-emerald-sleet-ta427.md)

## Sources
- Rapid7 Labs — "Inside the 'ted' backdoor: HAProxy-based Linux espionage toolkit targets South Korean media and automotive sectors" (published 2026-09-04): [https://www.rapid7.com/blog/post/tr-dprk-apts-ted-backdoor-curlrat-target-south-korean-media-automotive-sectors/](https://www.rapid7.com/blog/post/tr-dprk-apts-ted-backdoor-curlrat-target-south-korean-media-automotive-sectors/)
- The Hacker News — "New 'Ted' Backdoor Hides Inside Victims' HAProxy Builds" (2026-09-04): [https://thehackernews.com/2026/09/new-ted-backdoor-hides-inside-victims.html](https://thehackernews.com/2026/09/new-ted-backdoor-hides-inside-victims.html)
