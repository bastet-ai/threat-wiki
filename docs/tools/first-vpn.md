# First VPN

## Summary
**First VPN** was a criminal VPN / proxy service advertised on Russian-speaking cybercrime forums and disrupted in a May 2026 international law-enforcement action. Eurojust says the service targeted cybercriminal customers by promising anonymity, no cooperation with judicial authorities, no useful logs, and jurisdictional insulation. Europol characterized it as appearing in almost every major Europol-supported cybercrime investigation, and public reporting links it to ransomware, large-scale fraud, data theft, scanning, and denial-of-service activity.

The durable intelligence value is infrastructure tradecraft: crimeware and ransomware operators continue to rely on purpose-built VPN and proxy services that blend commodity VPN protocols, anonymous payments, forum-based promotion, and cross-border hosting. When those services are seized, domain, exit-node, payment, and support-channel artifacts become useful retrohunt pivots.

## Tags
- tools
- infrastructure
- proxy
- VPN
- criminal infrastructure
- ransomware
- cybercrime
- Russian-speaking forums
- Exploit.in
- XSS.is
- takedown
- Europol
- Eurojust
- FBI
- OpenConnect
- WireGuard
- VLESS
- Reality
- OpenVPN
- L2TP/IPSec
- PPtP

## Why this matters
- First VPN shows the repeated role of dedicated privacy infrastructure in ransomware reconnaissance, intrusion staging, fraud, and data-theft operations.
- The service allegedly marketed non-cooperation and no-log claims directly to criminal users, making it closer to a crimeware enabler than a neutral VPN provider.
- Seizures of criminal VPNs can generate retroactive investigative value: Eurojust says authorities accessed the service before it went offline and obtained insights and traffic data from users who believed they were protected.
- Infrastructure indicators from takedowns are time-sensitive but useful for historical log review, attribution support, and clustering across intrusion attempts.

## Operational characteristics
- **Forum promotion:** Europol/Eurojust and secondary reporting describe promotion on Russian-speaking cybercrime forums including Exploit[.]in and XSS[.]is.
- **Long-running service:** the FBI flash alert summarized by The Hacker News says First VPN had operated since about 2014.
- **Global exit footprint:** public reporting describes 32 exit-node servers across 27 countries, including U.S. exit nodes `2.223.66[.]103`, `5.181.234[.]59`, and `92.38.148[.]58`.
- **Protocol mix:** public FBI-sourced reporting lists OpenConnect, WireGuard, Outline, VLess TCP Reality, OpenVPN ECC, L2TP/IPSec, and PPtP options; VLESS/Reality can disguise VPN traffic as HTTPS-like traffic on common web ports.
- **Payments and support:** public reporting lists Bitcoin, Perfect Money, WebMoney, EgoPay, and InterKass payments, plus self-hosted Jabber and Telegram support channels.
- **Law-enforcement action:** coordinated activity on 2026-05-19 and 2026-05-20 dismantled more than 33 servers, seized `1vpns.com`, `1vpns.net`, `1vpns.org`, and associated onion domains, and included a search/interview of a suspect in Ukraine.

## Defender heuristics
- Search historical VPN, proxy, firewall, identity-provider, and EDR telemetry for connections to seized First VPN domains and known exit nodes, especially around ransomware precursor activity, external scanning, suspicious admin logins, and data staging.
- Treat First VPN artifacts as infrastructure pivots rather than attribution by themselves; VPN exit nodes are shared infrastructure and require correlation with identity, endpoint, timing, and tradecraft.
- For remote-access and admin panels, correlate successful logins from commodity VPN/proxy networks with impossible travel, new device fingerprints, MFA resets, password-spray precursors, or unusual post-authentication enumeration.
- Preserve raw logs before broad blocklist cleanups when a criminal VPN takedown appears relevant to an incident; seized-service telemetry may later enable law-enforcement or partner correlation.
- Monitor for replacement infrastructure and protocol shifts after takedowns, especially VLESS/Reality-like traffic masquerading as normal HTTPS and new forum-advertised VPN brands.

## Related pages
- [CitrixBleed session-hijack wave](../ops/citrixbleed-session-hijack-wave.md)
- [ConnectWise ScreenConnect exploitation wave](../ops/connectwise-screenconnect-exploitation-wave.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Eurojust: https://www.eurojust.europa.eu/news/eurojust-coordinated-investigation-shuts-down-criminal-vpn-network
- Europol: https://www.europol.europa.eu/media-press/newsroom/news/cybercriminal-vpn-used-ransomware-actors-dismantled-in-global-crackdown
- The Hacker News summary with FBI flash-alert details: https://thehackernews.com/2026/05/first-vpn-dismantled-in-global-takedown.html
- FBI IC3 flash alert PDF: https://www.ic3.gov/CSA/2026/260521.pdf
