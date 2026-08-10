# Gunra ransomware-as-a-service activity

## Summary
**Gunra** is a financially motivated double-extortion ransomware operation first observed by the FBI in April 2025. A joint CISA, FBI, DC3, NSA, U.S. Secret Service, and Republic of Korea National Police Agency advisory published on August 10, 2026 says Gunra formalized a ransomware-as-a-service affiliate program in January 2026 and has also used the **Golden Community** name. Its leak-site claims span government, critical infrastructure, healthcare, finance, manufacturing, transportation, utilities, academia, media, retail, and professional services across multiple regions.

Gunra appears based on or strongly influenced by the leaked Conti source code. The operation began with Windows targeting and later added Linux and broader cross-platform locker support. The public advisory documents exploitation of internet-facing FortiOS and FortiProxy devices, compromised VPN and VDI authentication paths, credential theft, Impacket-driven movement, OneDrive and SharePoint exfiltration, deletion of primary and disaster-recovery backups, and ChaCha20 plus RSA-4096 encryption.

## Tags
- ops
- campaign
- Gunra
- ransomware
- RaaS
- double extortion
- data theft
- FortiGate
- FortiOS
- VPN
- Impacket
- MFA bypass
- CISA
- FBI

## Why this matters
- The joint advisory is based on observed intrusions rather than leak-site claims alone and supplies downloadable STIX indicators.
- Gunra affiliates have exploited `CVE-2024-55591` and `CVE-2025-24472` against FortiOS and FortiProxy, while another documented path abused exposed VPN gateways, default credentials, and missing account lockout.
- One victim chain progressed from an internet-connected administrator workstation into the SSL-VPN console, an unused dual-homed account, VDI session hijacking, Active Directory, IT virtual desktops, and authentication-server tampering.
- The actors modified VDI authentication processing so an attacker-chosen one-time password always succeeded, creating a persistent MFA bypass.
- Exfiltration reached tens of terabytes in at least one case, and actors deleted backup data at both primary and disaster-recovery sites before and after ransomware deployment.
- The encryptor has no required DNS or HTTP behavior during encryption, so defenders should not depend on a last-stage network indicator.

## Observed intrusion chain

### Initial access
The FBI observed exploitation of public-facing firewall and VPN appliances, including:

- `CVE-2024-55591` — FortiOS and FortiProxy authentication bypass;
- `CVE-2025-24472` — FortiOS and FortiProxy authentication bypass;
- creation of the privileged `forticloud-sync` account through vulnerable Fortinet scheduled-task functionality;
- credential-exposure and SSH access-control weaknesses in internet-facing VPN gateways;
- default credentials on an SSL-VPN administrator account where account lockout was absent.

These are observed routes, not an exhaustive list of every affiliate's access method. Gunra has advertised for penetration testers and ethical hackers to supply enterprise access in exchange for a share of ransom proceeds.

### Persistence, credential access, and lateral movement
Observed post-access behavior includes:

- downloading OpenSSH from attacker-controlled infrastructure to establish tunnels;
- modifying an unused account to bypass a mandatory password change and preserve access across external and internal networks;
- reusing stolen VDI sessions and moving through RDP to authentication servers, Active Directory, and IT workstations;
- using Impacket `psexec.py` and `smbclient.py` over SMB;
- using `secretsdump.py` against domain controllers to extract NTDS password hashes, enabling pass-the-hash or pass-the-ticket movement;
- manipulating SSL-VPN traffic controls to collect VDI credentials and session material;
- stealing session cookies and modifying VDI portal authentication files so a Gunra-selected OTP bypassed MFA;
- stealing a Hiware access-control server's symmetric key, then decrypting stored enterprise server passwords.

Gunra actors commonly cleared system and network access logs and command history. KNPA observed activity concentrated between 10:00 p.m. and 6:00 a.m. local victim time. That timing is a hunt pivot, not a verdict by itself.

### Collection and exfiltration
The actors collected business documents, databases, personally identifiable information, internal email, and network configuration records before encryption. The advisory identifies:

- `main.exe` tooling that exfiltrated from Microsoft OneDrive and SharePoint;
- compressed staging archives;
- Mega as an exfiltration destination in at least one case;
- publicly available tools including Rclone, FileZilla, 7-Zip, WinRAR, DBeaver, Mimikatz, Sliver, AnyDesk, Google Remote Desktop, and Impacket.

The presence of any dual-use tool is not independently evidence of Gunra. Correlate it with account, process, transfer, appliance, and endpoint behavior.

### Encryption and recovery denial
The Windows encryptor enumerates accessible drives from `A:` through `Z:`, excludes common system directories and extensions, and queues user data for multithreaded ChaCha20 plus RSA-4096 encryption. Confirmed artifacts include:

- `.ENCRT` as the current encrypted-file extension and `.CRYPT` in a July 2025 sample;
- `R3ADM3.txt` as the ransom note;
- WMI and `WMIC.exe` deletion of volume shadow copies;
- deletion of backup and archive data at primary and disaster-recovery sites;
- Tor and qTox negotiation with a five-to-seven-day deadline.

The actors have demanded amounts above tens of millions of U.S. dollars, but opening demands do not establish payment or realized loss.

## High-confidence indicators

### Files
- `2dc70a12d158d437e45a55b1d52f3d61c6082a1e1667573302ba3b62813e2751` — SHA-256, `main.exe`, OneDrive and SharePoint exfiltration
- `834efe9b392c6c000877ea5613a079445affc16fe8af5997d68c55cafc95e5d1` — SHA-256, `main.exe`, OneDrive and SharePoint exfiltration
- `91f8fc7a3290611e28a35a403fd815554d9d856006cc2ee91ccdb64057ae53b0` — SHA-256, `cryptor.exe`
- `a82e496b7b5279cb6b93393ec167dd3f50aff1557366784b25f9e51cb23689d9` — SHA-256, `msmp.exe`
- `R3ADM3.txt` — ransom note
- `.ENCRT`, `.CRYPT` — encrypted-file suffixes

### Infrastructure and account artifacts
- `datapub[.]news` — historical clearnet leak-site mirror, observed June–July 2025
- `23.239.119[.]2` through `23.239.119[.]6` — historical infrastructure, observed July–November 2025
- `91.201.66[.]146` — historical infrastructure, observed November–December 2025
- `forticloud-sync` — malicious privileged Fortinet account associated with exploitation of the two listed CVEs

CISA's advisory and STIX bundles contain the complete historical IP, onion-service, email, qTox, and file-indicator set. Vet historical infrastructure before blocking and avoid treating an isolated dual-use tool as malicious.

## Defender guidance
- Patch exposed FortiOS, FortiProxy, VPN, RDP, and VDI infrastructure, prioritizing known-exploited flaws. Inventory appliances that cannot provide trustworthy endpoint telemetry.
- Search Fortinet configuration and task history for `forticloud-sync`, unexpected super-user creation, configuration changes, and unusual administrator logins.
- Reset default credentials, enforce lockout or rate limits, require phishing-resistant MFA, and review dormant or unused accounts that bridge internet-facing and internal networks.
- Hunt for VPN traffic-control changes, anomalous session-cookie reuse, VDI authentication-file modifications, a fixed OTP that succeeds across users, OpenSSH tunneling, and after-hours administrative activity.
- Detect `secretsdump.py`, `psexec.py`, `smbclient.py`, NTDS access, pass-the-hash or pass-the-ticket behavior, and unusual RDP or SMB movement from VDI and administrator workstations.
- Audit OneDrive, SharePoint, Mega, Rclone, FileZilla, and archive creation for abnormal volume and first-seen account or host combinations. Treat cloud audit retention as part of incident readiness.
- Maintain offline, immutable, separately credentialed backups and test restoration from a location not reachable by production or backup-administration identities. Gunra has targeted both primary and disaster-recovery copies.
- If compromise is suspected, preserve volatile appliance and VDI evidence, isolate affected systems, revoke sessions, rotate domain and appliance credentials, inspect authentication servers for backdoors, and investigate exfiltration before restoration.

## Related pages
- [DeadLock ransomware](../tools/deadlock-ransomware.md)
- [Anubis ransomware CitrixBleed 2 / RMM / cloudflared intrusions](anubis-ransomware-citrixbleed2-rmm-cloudflared.md)
- [FortiOS CVE-2025-68686 symlink-persistence bypass](fortios-cve-2025-68686-symlink-persistence-bypass.md)
- [FortiBleed Fortinet credential exposure](fortibleed-fortinet-credential-exposure.md)

## Sources
- CISA, FBI, DC3, NSA, U.S. Secret Service, and KNPA: [https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-222a](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-222a)
- CISA STIX JSON: [https://www.cisa.gov/sites/default/files/2026-08/AA26-222A-stix.json](https://www.cisa.gov/sites/default/files/2026-08/AA26-222A-stix.json)
- CISA STIX XML: [https://www.cisa.gov/sites/default/files/2026-08/AA26-222A-stix.xml](https://www.cisa.gov/sites/default/files/2026-08/AA26-222A-stix.xml)
