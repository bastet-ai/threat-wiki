# Dutch Police / NCSC 17-million-device botnet disruption

## Summary
Dutch Police and the Netherlands National Cyber Security Centre (NCSC-NL) announced a 2026-05-28 disruption of a large unnamed botnet after a security-researcher report to NCSC. The investigation found at least **17 million infected devices** and **200 command-and-control / hosting servers** located in the Netherlands. The Hague cybercrime police seized several servers from a hosting provider for investigation, and the provider took the botnet infrastructure offline because it was being used for criminal activity.

The public release does not name the malware family, operators, victim geography, or specific infection vector. The durable value is scale and infrastructure pattern: consumer computers, tablets, smartphones, routers, cameras, and other IoT / edge devices can be centrally coordinated through hosting-provider infrastructure and later repurposed for DDoS, spam, phishing, fraud, proxying, and other cybercrime activity.

## Tags
- ops
- operations
- botnet
- takedown
- law enforcement
- Netherlands
- NCSC-NL
- Dutch Police
- hosting provider
- IoT
- edge devices
- residential proxies
- DDoS
- spam
- phishing
- cybercrime
- consumer devices
- mobile devices

## Why this matters
- A 17-million-device estimate puts this in the class of large criminal botnets even though the public advisories omit malware-family details.
- The 200-server footprint in one country shows how botnet control planes can concentrate in hosting-provider infrastructure while infected devices remain globally distributed.
- NCSC explicitly links weakly secured consumer routers, mobile devices, IoT devices, and other edge equipment to residential-proxy abuse, reinforcing that botnets are not only DDoS platforms but also anonymity and fraud infrastructure.
- The disruption does not prove endpoint remediation. Devices may remain infected, recover from alternate C2, or be absorbed by successor infrastructure if owners do not patch, reset, and harden them.

## Reported facts
- **Announcement date:** 2026-05-28; Dutch Police page updated 2026-05-29.
- **Discovery path:** a security researcher reported the network to NCSC-NL; NCSC informed Dutch Police.
- **Scale:** at least 17 million infected devices.
- **Infrastructure:** 200 servers used to host botnet infrastructure were located in the Netherlands.
- **Action:** The Hague police cybercrime team seized several servers from a hosting provider for investigation; the hosting provider took the botnet offline.
- **Device classes:** public advisories mention computers, tablets, smartphones, routers, security cameras, smart devices, and other IoT / edge devices.
- **Abuse categories:** Dutch authorities describe botnet use for cyberattacks, spam, phishing, online fraud, and traffic-flood disruption of websites.

## Defender heuristics
- Treat botnet takedown news as a prompt for historical log review, not just blocklisting. Look for prior outbound connections from edge, mobile, workstation, and IoT networks to hosting-provider IP ranges later associated with the disruption if indicators become available.
- Prioritize visibility and patching for internet-reachable edge devices: routers, NAS, cameras, VPN appliances, SOHO firewalls, mobile devices, and unmanaged smart devices.
- Replace default passwords, enforce unique credentials and MFA where available, and review router / IoT admin exposure from the internet.
- Segment consumer / IoT / guest networks away from administrative systems and sensitive workloads so commodity botnet infection does not become a pivot path.
- For enterprise networks, monitor unexpected egress from non-user devices, unusual proxy behavior, high-rate outbound traffic, SMTP abuse, and connections from devices that should not communicate with arbitrary hosting-provider infrastructure.
- If a device is suspected to be enrolled in a botnet, preserve useful logs where possible, then rebuild or factory-reset, patch firmware, rotate local/admin passwords, and rejoin it only after configuration hardening.
- Track follow-up publications from NCSC-NL, Dutch Police, hosting providers, Shadowserver, CERTs, or security vendors for malware-family names, sinkhole data, indicators, or victim-notification paths.

## Related pages
- [First VPN](../tools/first-vpn.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [Ollama P2P cryptominer RAT campaign](ollama-p2p-cryptominer-rat.md)
- [ConnectWise ScreenConnect exploitation wave](connectwise-screenconnect-exploitation-wave.md)

## Sources
- NCSC-NL: [https://www.ncsc.nl/nieuws/gezamenlijke-actie-politie-en-ncsc-legt-groot-botnetwerk-plat](https://www.ncsc.nl/nieuws/gezamenlijke-actie-politie-en-ncsc-legt-groot-botnetwerk-plat)
- Dutch Police: [https://www.politie.nl/nieuws/2026/mei/28/06-politie-en-ncsc-halen-groot-botnetwerk-offline.html](https://www.politie.nl/nieuws/2026/mei/28/06-politie-en-ncsc-halen-groot-botnetwerk-offline.html)
