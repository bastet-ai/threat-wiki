# BREEZE COMET (GTIG): direct intrusions against Brazil's core payment systems — Rust/Nim/Go backdoor suite, rogue-hardware retail footholds, compromised municipal websites on three continents, and LLM-generated tradecraft

## Tags
- ops
- BREEZE COMET
- UNC5669
- GTIG
- Mandiant
- Brazil
- Latin America
- financial sector
- payment systems
- Pix
- STR
- Boleto
- COBALTSPIN
- LIGHTPAINT
- MILDFROST
- KICKPLATE
- BOATBEAM
- REALBREEZE
- XWORM
- rogue hardware
- mTLS credential theft
- CI/CD credential theft
- AI-augmented operations
- Plump Spider
- SHADOW-AETHER-064
- cybercrime

## Summary

Google Threat Intelligence Group published its first full write-up (September 1, 2026) of **BREEZE COMET** (formerly **UNC5669**), a financially motivated threat actor that since 2024 has compromised Brazilian financial-services, retail, and eCommerce organizations to execute **fraudulent transfers through Brazil's core payment rails — Pix, STR (Reserves Transfer System), and Boleto** — rather than the client-side retail fraud that has historically defined the region's cybercrime ecosystem. GTIG's durable read: a **shift from opportunistic banking fraud to direct intrusion into the financial switch itself**, supported by a custom multi-language backdoor suite and **LLM-generated operational scripts**. The activity overlaps with reporting publicly known as **Plump Spider** and Trend Micro's **SHADOW-AETHER-064** — the same Brazilian-financial cluster this wiki already tracks via Unit 42's CL-CRI-1163 reporting — making GTIG's tool taxonomy the missing naming layer on an on-wiki campaign.

The objective defines the access requirements, and they are unusually specific: BREEZE COMET needs **network access to Brazil's financial system network (RSFN) through an entity that holds it**, **mTLS credentials** that authenticate transactional payloads in the name of an org with funds, **persistent multi-account AD/cloud access**, and knowledge of the victim's transfer procedures and anti-fraud controls. Everything below serves those four requirements.

## Confirmed tradecraft (GTIG/Mandiant incident investigations since 2024)

- **Initial access, several ways in:**
  - Early: password spraying and **IT-support vishing** to talk users into installing RMM tools (AnyDesk observed). Axur corroborates the vishing and adds reported **insider recruitment** attempts at target organizations.
  - Mid-2025: **compromised Brazilian small-government (.gov) websites** used both as social-engineering staging (infostealers disguised as tax/receipt documents, e.g. `ComprovantePDF.exe`, and purchased/cracked **XWORM** backdoors persisting via startup shortcut edits) **and as C2 endpoints** — trusted-domain infrastructure that sails past reputation filters. GTIG observed the **same staging behavior replicated on municipal domains in Nigeria, Paraguay, Ghana, and Venezuela**, and the same staging infrastructure reused across operations targeting multiple organizations.
  - 2025: **physically plugging rogue hardware devices into retail store networks** to obtain a foothold, then moving laterally and pulling post-exploitation frameworks from external open directories with Netcat plus custom scripts. Trend Micro separately reported **JBoss AS exploitation** for initial access (the same entry point as SHADOW-AETHER-064).
- **Reconnaissance / AD operations:** Impacket, ADRecon, ADVipscan downloaded from GitHub and executed in-memory via PowerShell; a **custom LDAP brute-forcing utility, REALBREEZE**. Environments with low observability are explicitly profitable.
- **Credential hunting tuned to payments:** custom scripts search files and environment variables for mTLS credentials and admin certificates using grep-style terms **`boleto`, `cnab`, `remessa`, `webhook.*pix`, `instant.*payment`**; CI/CD environments are mined for hard-coded pipeline credentials, API keys, and privileged cloud tokens. Lateral movement via **hijacked service accounts initiating RDP**, SMB exec, and deliberate **SMB-path enumeration scans across internal subnets**.
- **Segmentation bypass — COBALTSPIN:** a **Rust** lightweight network tunneler that establishes a **reverse SOCKS5 proxy over WebSocket** back to C2, routing traffic between the operator and internal financial-API infrastructure **straight through boundary firewalls** with no host persistence mechanism to alert on.
- **Redundant persistence suite (2025–2026, four named backdoors):**
  - **LIGHTPAINT** (Java): installs a legitimate VPN (e.g. SoftEther) configured for automated persistence, then **programmatically adds Windows Defender Firewall inbound allow rules for the VPN manager** and **clears the Windows Networking Vpn Plugin Platform event log** to erase the connection's forensics.
  - **MILDFROST** (Java): passive JAR backdoor living inside the JVM process space; classes such as `DnsCommandBeacon.class` run **slow covert DNS tunnels**, and it serves as **fallback C2** — querying delegated subdomains for instructions and fresh copies of the C++ payloads.
  - **KICKPLATE** (Nim): payload-delivery and host-persistence workhorse impersonating **Windows Update Health Tools**; controls the SOCKS5 tunnelers, updates registry startup keys, silently modifies Windows services; supplemented by `schtasks.exe` as SYSTEM and `.lnk` edits in startup folders.
  - **BOATBEAM** (Go): stands up a **fake IIS HTTPS server on 443**, activating backdoor behavior **only when it receives a specific session cookie** — otherwise it is indistinguishable from a web server.
- **Defense impairment:** direct PowerShell `Set-MpPreference -DisableRealtimeMonitoring $true` across compromised hosts; post-theft **event-log clearing across hosts** and deletion of attacker-created directories.
- **Cloud/Kubernetes persistence (2025):** **malicious Kubernetes pods** deployed to maintain access and steal cloud secrets, exfiltrated to public paste/notepad sites (`dontpad[.]com`).
- **AI usage:** Mandiant recovered scripts showing **LLM-accelerated development** of recon, credential-validation, mass-deployment, victim-specific pivoting, and data-extraction tooling — highly functional code lacking human idiosyncrasies: unrolled structures, verbose explanatory comments, standardized execution headers (GTIG publishes an excerpt with Portuguese comments and per-step banners: `### STEP 1: ENUM ALL LINUX (SSH PORT 22) ###`).
- **Payoff:** within **24–48 hours** of reaching core financial applications via COBALTSPIN + privileged accounts, the actor executed **two waves of hundreds of fraudulent transactions** (per a client and third-party forensic analysis); at least one confirmed heist of tens of thousands of USD since 2024 — modest for the access achieved, which itself is a signal of an actor building capability faster than monetization.

## Why it matters (durable reads)

1. **The payment switch is a network target, not an app target.** The four access requirements (RSFN reach, mTLS transaction certs, persistent AD/cloud accounts, procedural knowledge) mean detections that work against bank fraud (card/endpoint telemetry) are blind here; the indicators to hunt are **mTLS keystore/certificate access with payment-vocabulary search terms**, service-account RDP, and SMB-enumeration scans.
2. **The tool names are now durable pivots.** COBALTSPIN (Rust reverse-SOCKS5-over-WebSocket), LIGHTPAINT (VPN + firewall-rule + VPN-event-log-clearing trio), MILDFROST (in-JVM DNS-tunnel fallback C2), KICKPLATE (Nim, Windows-Update-Health-Tools masquerade), BOATBEAM (cookie-gated fake-IIS), REALBREEZE (LDAP bruter). Any one of these appearing outside Brazilian finance would mark diffusion of this playbook.
3. **Compromised trusted websites as staging AND C2, replicated across continents.** Brazilian municipal `.gov` sites plus the **Nigeria / Paraguay / Ghana / Venezuela municipal replication** is the most transferable finding: local-government CMS compromise is becoming commodity crime infrastructure, and domain-reputation controls are exactly the defense it defeats — GTIG's own mitigation guidance says stop relying on `.gov` allowlists and do TLS decryption + DPI on egress.
4. **Rogue hardware on retail branch networks** is the low-tech foothold most organizations don't model; the fix GTIG prescribes (802.1X NAC on switch ports, port security, locked closets) is physical-network work, not endpoint work.
5. **Corroboration, not new attribution.** BREEZE COMET (GTIG) overlaps **Plump Spider** and **SHADOW-AETHER-064** (Trend Micro) and Unit 42's **CL-CRI-1163**; SockTz-era infrastructure (`167.148.195[.]53`) and JBoss entry previously tied on-wiki all sit in this same space. Treat the names as vendor labels over a likely-porous Brazilian financial-cybercrime ecosystem; no single operator identity is established by any of them.
6. **LLM-generated ops scripts with Portuguese comments are a hunting texture** (already our standing rule: AI-style tells only in combination with behavior — here: tunneling, credential search for payment terms, log clearing).

## Hunt guidance

- Firewalls/VPN: alert on **inbound firewall rule additions by non-admin/service contexts**, VPN service installs (SoftEther especially) outside IT-managed hosts, and **clearing of `Microsoft-Windows-Networking/VpnPlugin-Platform`** event logs (log-clear on one host is rare; this specific channel is the tell).
- JVM estates: passive JARs loaded into long-running Java processes with DNS-querying behavior (`DnsCommandBeacon` pattern); Java processes making DNS TXT/subdomain lookups they've never made.
- HTTPS listeners: web servers on 443 not in inventory, or IIS-looking services whose responses **differ only when a specific cookie is present** (compare cookie/no-cookie fetches from your own scanning).
- Egress: reverse-SOCKS5/WebSocket tunneling from hosts that have no business tunneling; outbound to paste/notepad services (`dontpad[.]com` and equivalents) from Kubernetes workloads.
- Credential stores: file/env searches combining `boleto|cnab|remessa|webhook.*pix|instant.*payment` — this vocabulary in PowerShell/bash history is close to a one-signature detection for this actor class.
- Physical: 802.1X enforcement reports and switch-port security logs on retail/branch VLANs; unknown MACs obtaining DHCP.
- Municipal-site compromise (if you run a local-government CMS anywhere): unexpected file writes, and the fact that your domain appearing in someone else's TLS certificates is a compromise indicator.

## Monitoring

- GTIG follow-ups naming additional victims or the mTLS-credential theft outcomes; any disruption/takedown touching the Nigerian/Paraguayan/Ghanaian/Venezuelan municipal staging set.
- Whether COBALTSPIN/LIGHTPAINT/MILDFROST/KICKPLATE/BOATBEAM names appear in other clusters (playbook diffusion beyond Brazil).
- Convergence or divergence with Trend Micro SHADOW-AETHER-064 and Unit 42 CL-CRI-1163 follow-on reporting (`167.148.195[.]53` rotation, SockTz versions) — does anyone tie the three labels to one operator?
- XWORM sales/leak-tracking for the cracked versions this actor used, and Axur's insider-recruitment claims maturing into named cases.
- Expansion GTIG flags as possible: **Africa and other Latin American countries** — watch Pix-style instant-payment rails elsewhere (Mexico's DiMo SPEI, Colombia's Bre-B) for the same playbook.

## Sources

- Google Threat Intelligence Group / Mandiant: [Financially Motivated Threat Actor BREEZE COMET Targets Brazil](https://cloud.google.com/blog/topics/threat-intelligence/financially-motivated-threat-actor-breeze-comet-targets-brazil) (September 1, 2026; captured by this wiki September 20, 2026 sweep).
- Corroborating labels referenced by the primary and our prior pages: Trend Micro SHADOW-AETHER ("Vibe Hacking" report); Unit 42 CL-CRI-1131/CL-CRI-1163; Axur (vishing + insider recruitment); Trend Micro JBoss exploitation reporting.

## Related pages

- [SHADOW-AETHER AI-augmented Latin America intrusions](shadow-aether-ai-augmented-latam-intrusions.md) — Trend Micro's SHADOW-AETHER-064 overlaps this cluster per GTIG
- [Unit 42 CL-CRI-1131/1163 LLM-orchestrated LATAM campaigns](unit42-clcri-1131-1163-llm-orchestrated-latam-campaigns-september-2026.md) — the Brazilian-financial campaign side of the same picture
- [Unit 42 Spring Ring Teams vishing campaigns](spring-ring-teams-vishing-rmm-petitpotam-campaigns-unit42-august-2026.md) — IT-support vishing into RMM, same first-stage shape
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
