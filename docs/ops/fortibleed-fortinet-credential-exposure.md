# FortiBleed Fortinet credential exposure

## Summary
CISA warned on June 18, 2026 that malicious cyber actors were targeting internet-accessible Fortinet devices using compromised credentials. The activity, publicly called `FortiBleed`, involves leaked credentials associated with roughly 74,000 Fortinet firewalls and VPN gateways in CISA's alert; The Hacker News later cited SOCRadar data reporting 86,644 affected FortiGate devices as of June 19.

Treat an exposed FortiGate or SSL VPN account hit by this activity as a credential-compromise and edge-access incident, not only as a password-hygiene issue. Terminate active sessions, rotate VPN and administrator credentials, enforce phishing-resistant MFA, remove public management exposure, and review firewall, VPN, authentication, domain-controller, and downstream network logs for lateral movement.

## Tags
- ops
- operations
- Fortinet
- FortiGate
- FortiOS
- SSL VPN
- edge device
- VPN gateway
- firewall
- credential exposure
- credential stuffing
- credential theft
- leaked credentials
- remote access
- active exploitation
- CISA
- incident response

## Why this matters
- FortiGate appliances often sit on the remote-access boundary; a valid VPN or administrator credential can become an initial-access path without exploiting a fresh software flaw.
- CISA says the leaked credentials are associated with approximately 74,000 Fortinet devices across government and private-sector organizations.
- Secondary reporting from The Hacker News, citing SOCRadar, raised the count to 86,644 compromised devices and described telecom, government, and education as top impacted sectors.
- The campaign blends old secrets, internet-exposed login endpoints, and weak credential lifecycle controls. Fortinet told The Hacker News the data is likely a resharing of data from previous incidents plus brute-forcing, and not related to a current Fortinet incident or advisory.
- Even after patching, upgraded FortiOS deployments can retain legacy password hashes until the relevant administrator logs in or credentials are reset; CISA specifically calls out PBKDF2 enforcement and removal of weaker legacy hashes.

## Reported activity
- CISA says malicious cyber actors targeted internet-accessible Fortinet devices across government and private-sector organizations using compromised credentials.
- Affected devices include Fortinet firewalls and VPN gateways, especially FortiGate appliances and associated SSL VPN gateways.
- The Hacker News summarizes SOCRadar reporting that generic `admin` accounts and built-in Fortinet system accounts made up a large share of exposed credentials, with organization-specific accounts also present.
- The Hacker News reports that the operators mass-scanned for Fortinet remote-login endpoints and used a bespoke credential-spraying tool against known username/password combinations.
- The same report describes a feedback loop: use leaked Fortinet credentials to access appliances, passively monitor traffic to collect more credentials, verify working logins, and add them to a confirmed-access database.
- Fortinet's statement to The Hacker News framed the exposed data as likely reshared from previous incidents plus brute-forcing, not a new vendor-side breach or current advisory.

## Defensive actions
### Immediate containment
- Terminate all active SSL VPN and administrative sessions on potentially affected Fortinet appliances.
- Reset all Fortinet VPN and administrator passwords, especially on internet-facing systems.
- Rotate any downstream credentials that may have traversed compromised VPN or firewall paths.
- Disable or remove unauthorized, stale, generic, and unnecessary accounts.
- If compromise is plausible, preserve configuration exports, logs, VPN session records, and authentication telemetry before rebuilding or factory-resetting appliances.

### Hardening
- Require phishing-resistant MFA for all remote-access and administrative accounts, and verify enforcement on all external gateways and management interfaces.
- Remove public internet exposure from firewall management interfaces; restrict administration to trusted internal networks or dedicated management paths.
- Confirm PBKDF2 is used for administrator credential storage in FortiOS and remove weaker legacy hashes following Fortinet guidance.
- Rename or disable generic/default administrator accounts where operationally possible; avoid reused credentials on edge devices.
- Monitor external attack surface for exposed Fortinet login panels and unexpected SSL VPN portals.

### Hunting and review
- Review firewall, VPN, authentication, and domain-controller logs for unusual access, impossible travel, new sessions from unfamiliar networks, unexpected administrator logins, account creation, policy changes, and configuration exports.
- Review routing, VPN, firewall-policy, address-object, local-user, admin-profile, and logging configuration changes after any suspicious login.
- Look for lateral movement from VPN-assigned address pools to identity infrastructure, backup systems, hypervisors, management networks, and file servers.
- Correlate Fortinet logins with password-spray, credential-stuffing, or successful authentication attempts against other remote-access systems.
- Treat any confirmed Fortinet edge access as a potential path to internal credential capture and session hijacking until downstream telemetry rules it out.

## Source caveats
- CISA confirms malicious use of compromised Fortinet credentials and provides the most durable public mitigation guidance.
- The larger 86,644-device count, sector/geography breakdown, and tooling details come from The Hacker News summarizing SOCRadar and other secondary reporting; keep those figures attributed.
- Do not redistribute leaked credential lists or victim-specific device data. Use vendor, CISA, and trusted exposure-management channels to determine whether a specific environment is affected.

## Related pages
- [PAN-OS GlobalProtect CVE-2026-0257 exploitation](pan-os-globalprotect-cve-2026-0257-exploitation.md)
- [Check Point VPN CVE-2026-50751 exploitation](check-point-vpn-cve-2026-50751-exploitation.md)
- [CitrixBleed session-hijack wave](citrixbleed-session-hijack-wave.md)

## Sources
- CISA: https://www.cisa.gov/news-events/alerts/2026/06/18/cisa-urges-hardening-fortinet-devices-after-reports-credential-exposure
- The Hacker News: https://thehackernews.com/2026/06/cisa-warns-fortinet-customers-as.html
