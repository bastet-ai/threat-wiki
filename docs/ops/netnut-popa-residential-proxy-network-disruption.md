# NetNut / Popa residential proxy network disruption

Google Threat Intelligence Group (GTIG) reported a July 2026 disruption of the **NetNut** residential proxy network, also known as **Popa**, coordinated with the FBI, Lumen, and other partners.

## Why it matters
- GTIG estimates NetNut at **at least 2 million devices** worldwide, including home-device classes such as smart TVs and streaming boxes.
- Google observed **316 distinct threat clusters** using suspected NetNut exit nodes during a single week in June 2026, including cybercriminal and espionage groups.
- Residential proxy exit nodes let attackers make credential attacks, infrastructure access, fraud, scanning, and intrusion traffic appear to originate from ordinary consumer ISP addresses.
- When a home device becomes an exit node, unauthorized traffic can pass through the local network, creating risk for the owner and adjacent private devices as well as reputational blocking of the home IP.

## Reported disruption actions
GTIG said Google and partners took ecosystem-level action rather than publishing a simple indicator blocklist:

- disabled Google accounts and associated Google services used by NetNut for malware command and control;
- shared technical intelligence on NetNut SDKs and backend C2 infrastructure with platform providers, law enforcement, and research firms;
- used Google Play Protect to warn users and disable applications known to include NetNut SDKs, with continued protection against future install attempts;
- framed the action as a continuation of the January 2026 IPIDEA disruption and broader work against malicious residential proxy networks.

Google describes the result as **degradation**, not permanent eradication. The company warned that proxy operators can recover by buying capacity from peer networks, reselling each other, or shifting traffic under reseller brands.

## Network composition and tradecraft
- GTIG and public reporting connect NetNut / Popa enrollment to SDKs distributed in applications for home devices, including smart TVs and streaming boxes.
- Google says some devices may arrive with proxy components preinstalled, while others are enrolled after users install applications that hide proxy code.
- GTIG identified NetNut botnet plugin components for larger botnet ecosystems such as **Badbox 2.0**.
- Third-party reporting cited by Google tied the network to Mirai-family DDoS botnet activity and other proxy-abuse patterns.
- The network's reseller model means many apparently separate proxy brands may ultimately rely on the same device pool.

## Defender guidance
### For enterprises and identity teams
- Treat residential-ISP source addresses as insufficient proof of legitimacy for authentication, VPN, SaaS, and admin activity.
- Correlate password-spray and credential-stuffing attempts by behavior: impossible travel, user-agent reuse, ASN/ISP churn, request timing, target lists, and failed-to-successful login sequences.
- Watch for rapid source-IP rotation across consumer ISPs combined with stable session fingerprints or infrastructure-touch patterns.
- Review fraud, abuse, and bot controls that over-trust consumer ISP geolocation or reputation.

### For platform and network defenders
- Monitor for traffic that appears to come from ordinary residential IPs but repeatedly touches admin portals, login endpoints, cloud APIs, exposed management surfaces, or known attacker infrastructure.
- Track proxy-reseller brand overlap and treat sudden disappearance or reappearance of traffic under adjacent brands as a sign of capacity migration, not necessarily remediation.
- Use device-owner notifications carefully: many exit nodes are likely consumer devices whose owners are victims or unaware participants.

### For home and small-business device owners
- Avoid applications that pay for "unused bandwidth" or "sharing your internet" unless the business model and consent boundaries are explicit and trusted.
- Remove unknown TV/streaming-box apps, keep firmware current, and reset or replace devices that cannot receive updates.
- Segment smart TVs, streaming boxes, and other IoT devices away from laptops, phones, NAS, and work systems.
- Review router DNS, egress, and bandwidth anomalies when a home IP is unexpectedly blocked or flagged.

## Source caveats
- Google and cited researchers describe NetNut / Popa as a malicious residential proxy/botnet network. Alarum Technologies, NetNut's owner, has publicly disputed the "botnet" characterization and described its software as consented bandwidth sharing.
- Consent and enrollment quality can vary by app, SDK, region, and device supply chain; defenders should avoid assuming every enrolled device owner knowingly participated.
- The 2-million-device and 316-threat-cluster figures are GTIG estimates/observations, not a full global census of all residential-proxy abuse.

## Sources
- [Google Cloud / GTIG](https://cloud.google.com/blog/topics/threat-intelligence/google-continued-disruption-residential-proxy-networks)
- [The Hacker News](https://thehackernews.com/2026/07/google-disrupts-netnut-residential.html)

## Tags
- NetNut
- Popa
- residential proxy
- botnet
- proxy network
- Google Threat Intelligence Group
- GTIG
- FBI
- Lumen
- Google Play Protect
- Android
- smart TVs
- streaming boxes
- Badbox 2.0
- Mirai
- password spray
- credential attacks
- infrastructure disruption
- consumer IoT
