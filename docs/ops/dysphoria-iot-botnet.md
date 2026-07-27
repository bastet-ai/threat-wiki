# Dysphoria IoT botnet

## Summary
**Dysphoria** is a rapidly evolving Linux IoT botnet jointly documented by CNCERT and QiAnXin XLab. Public reporting traces it from post-disruption JackSkid and fbot-derived samples into a hybrid DDoS and relay network that resolves infrastructure through Ethereum Name Service (ENS) and Solana Name Service (SNS) records, then hides controllers behind victim-operated relays.

XLab reports more than 200,000 bots, 4,401 confirmed active devices in China from July 14–20, 2026, and a one-day peak of 239,000 active devices outside China. Treat those figures as source-reported estimates rather than a precise census: the report does not publish its counting or de-duplication methodology, and the overseas figure is partly complicated by infected hosts acting as C2 relays.

## Tags
- ops
- operations
- botnet
- IoT botnet
- DDoS
- DDoS-for-hire
- Linux malware
- router compromise
- weak passwords
- Telnet brute force
- SSH brute force
- blockchain dead drop
- Ethereum Name Service
- Solana Name Service
- victim-owned relay infrastructure
- UPnP
- JackSkid
- fbot
- Dysphoria
- CNCERT
- QiAnXin XLab

## Why this matters
- Dysphoria demonstrates operational recovery after infrastructure disruption: a March 19 law-enforcement action targeted JackSkid, but related samples used ENS within days and later added SNS and victim-hosted relays.
- Blockchain records make infrastructure changes harder to suppress through ordinary DNS action. Victim relays add another layer between bots and controllers, weakening static C2 blocklists and complicating seizure-based disruption.
- A dedicated relay build converts compromised NATed devices into externally reachable infrastructure by creating many UPnP port mappings and transparently forwarding traffic with Linux `epoll`.
- Weak Telnet and SSH credentials remain the most consistently reported propagation path even as the operators maintain a changing list of router, gateway, camera, and embedded-Linux RCE exploits.

## Evolution
- **March 25:** XLab captured a JackSkid variant that resolved `m3rnbvs5d[.]eth`, six days after coordinated law-enforcement action against JackSkid infrastructure.
- **April 1:** an fbot-derived build appeared.
- **April 29–30:** samples added customized RC4-like string protection and enabled `ukranianhorseriding[.]eth`.
- **Early May:** the botnet added SNS resolution through `24carnforth2merseyside[.]sol`.
- **June 10:** `burrberry[.]eth` appeared as an ENS infrastructure record.
- **June 25:** XLab observed a separate relay-only build with the DDoS modules removed.
- **June 27–28:** relay builds added automated UPnP mappings, while DDoS builds began retrieving dynamic victim-relay lists from distribution nodes.

## Architecture and behavior
### Blockchain-assisted infrastructure resolution
Dysphoria supports ENS and SNS record lookups. XLab reports these mappings:

| Name | Record key | Reported purpose |
|---|---|---|
| `burrberry[.]eth` | `node` | relay-distribution node addresses |
| `ukranianhorseriding[.]eth` | `network` | base network infrastructure |
| `24carnforth2merseyside[.]sol` | `deserialized` | base network infrastructure |

The records encode address material inside IPv6-looking text. The malware filters four selected bytes and applies a custom per-byte transformation to recover IPv4 addresses. A DDoS build then requests a current relay list from a decoded distribution node:

```text
http://<node_ip>:9000/nodes?key=meowmeowmeow
```

XLab says the returned endpoints were compromised hosts forwarding traffic toward the actual controllers, not the controllers themselves.

### DDoS build
- Masquerades its process name as `libdalvikengine.so`.
- Protects strings with a modified RC4 design that adds repeated LCG-based S-box shuffling and an LFSR step in the keystream process.
- Uses fixed 78-byte login and heartbeat messages.
- Login message type: `02 00`; reported 12-byte magic: `00 80 00 5a 00 57 00 c8 00 f0 00 1e`.
- Heartbeat message type: `00 00`; reported 12-byte magic: `22 ba 15 24 1a 6f 04 d4 1f 9c 0d 06`.
- Receives structured DDoS tasking with duration, attack type, target/netmask records, and variable option fields.

### Relay-only build
- Removes DDoS functionality and turns the infected system into a network relay.
- Uses UPnP to create **155** port mappings on a compatible local gateway.
- Listens on those mapped ports and opens a same-port outbound connection to a remote C2 service.
- Uses Linux `epoll` for bidirectional nonblocking forwarding.
- Reports JSON-formatted availability state to `login[.]trees4sale[.]net:9000` at intervals reported as at least four seconds.

## Propagation
XLab and CNCERT identify Telnet and SSH weak-password guessing as the botnet's main, stable infection method. Their reports also list known RCE flaws affecting routers, gateways, cameras, and other embedded Linux devices. The published lists are not identical; validate product applicability before turning any listed CVE into a detection or exposure assumption.

XLab's list includes:

- `CNVD-2021-79445`
- `CVE-2013-3307`
- `CVE-2016-20016`
- `CVE-2017-17215`
- `CVE-2017-5259`
- `CVE-2018-14558`
- `CVE-2020-25499`
- `CVE-2020-8515`
- `CVE-2022-35733`
- `CVE-2025-9528`
- `CVE-2025-28137`
- `CVE-2025-34152`
- `CVE-2025-55182`

The Hacker News notes that the role of `CVE-2025-9528` is unclear: NVD scores the Linksys E1700 command-injection flaw as requiring high privileges, while the public botnet reports do not explain how it enters the propagation chain.

## Public indicators
Treat IP addresses as time-bounded infrastructure and domains as hunt pivots rather than permanent blocks. Victim-operated relays may appear in telemetry without being operator-owned infrastructure.

### Download and C2 servers
- `217.60.195[.]160`
- `76.164.203[.]171`
- `92.42.100[.]131`
- `78.153.155[.]152`
- FTP banner: `220 cool ftp server hosted on brian krebs' giant ass 4head`

### Domains
- `i[.]peer4you[.]net`
- `o[.]peer4you[.]net`
- `login[.]trees4sale[.]net`
- `www[.]trees4sale[.]net`
- `c2[.]saintpetersburgresident[.]ru`
- `peer[.]saintpetersburgresident[.]ru`
- `kieron[.]androiddebugbridge[.]su`
- `dysphoria[.]androiddebugbridge[.]su`
- `telaviv[.]androiddebugbridge[.]su`
- `jerusalem[.]androiddebugbridge[.]su`
- `node[.]androiddebugbridge[.]su`
- `wow[.]androiddebugbridge[.]su`

### Blockchain names
- `m3rnbvs5d[.]eth`
- `burrberry[.]eth`
- `ukranianhorseriding[.]eth`
- `24carnforth2merseyside[.]sol`

### SHA-1
- `c1bedea261f325441fb9a75c50b11d0c8fb01ac6`
- `a3b9575897c16cbf6afe3af1aa8b55171ea6edf9`
- `8db6c78533c176f13b61405cdc3f8fad703325f1`
- `9c1716d770ea69e8e1418d96d52222396ecb4362`
- `73651c02b29f1c07e3177e86c967fc45e9f30f0f`
- `955ff909972958098f0d4a06bcc4d6b9eea90449`
- `25081bdec05f64eb4f313420c82d8de957e30026`
- `dcea71b9ab9de8efca301de9e2f7bf11c7132364`
- `df510f6f69a5c149c216c7b3accc4f460d8cf363`
- `b0782a9d6eef2ce02f734a6e5e1d8e0f9a2b65be`
- `e7e1694162639ed587625432a79cfaa49f560d11`
- `b7faa44ab0772047a8581bbfdd9c561e28fc66de`

## Defender guidance
- Inventory internet-exposed routers, gateways, cameras, and embedded Linux systems; remove unnecessary exposure and remote management.
- Replace default and weak credentials with unique passwords; disable Telnet and require SSH keys where the platform supports them.
- Patch supported devices against applicable known-exploited IoT flaws. Replace end-of-life devices that cannot receive security updates.
- Disable UPnP where it is not required. Audit gateways for unexplained bursts of port mappings or unusually large mapping sets, especially around 155 ports.
- Hunt for the `libdalvikengine.so` process-name masquerade on non-Android embedded Linux systems, the reported FTP banner, port `9000` `/nodes?key=meowmeowmeow` requests, and repeated JSON health reports to `login[.]trees4sale[.]net`.
- Monitor blockchain-name-resolution services and application telemetry for the published ENS/SNS names; do not assume conventional DNS controls cover this path.
- Correlate connections to suspected relays with process, authentication, UPnP, NAT, and egress telemetry before classifying the remote host as attacker-owned.
- If compromise is suspected, preserve volatile process and network state, gateway mapping tables, firmware and filesystem images where feasible, and authentication logs before rebooting. Rebuild or replace the device and rotate any credentials exposed to it or reused elsewhere.

## Attribution and measurement caveats
- CNCERT and XLab connect Dysphoria's evolution to JackSkid and fbot code and infrastructure. Shared code and strings across IoT botnet families can indicate reuse or a common supplier; they do not by themselves establish a single operator.
- No public source reviewed here names an operator.
- XLab says the service advertises roughly 4 Tbps of attack capacity and describes near-daily attacks against internet-service and gaming targets. Those capacity and storefront claims are not independently measured, and the report does not name victims.
- The 200,000-plus scale and 239,000-device overseas daily peak remain source-reported estimates without a published counting methodology.

## Sources
- CNCERT and QiAnXin XLab: [Dysphoria evolution and deep technical analysis](https://blog.xlab.qianxin.com/dysphoria/)
- Nokia Deepfield: [JackSkid post-disruption analysis](https://github.com/deepfield/public-research/blob/main/jackskid/report.md)
- NICTER Blog: [JackSkid ENS/SNS transition analysis](https://blog.nicter.jp/2026/05/jackskid_2026_may/)
- The Hacker News: [Dysphoria adds blockchain C2 and victim relays](https://thehackernews.com/2026/07/dysphoria-iot-botnet-adds-blockchain-c2.html)
- NVD: [CVE-2025-9528](https://nvd.nist.gov/vuln/detail/CVE-2025-9528)
