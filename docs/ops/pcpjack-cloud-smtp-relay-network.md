# PCPJack cloud SMTP relay network

## Summary
Hunt.io's June 2026 infrastructure recovery shows a later-stage **PCPJack** operation converting compromised Linux cloud servers into a hidden SMTP relay network. The recovered open directories on `213.136.80[.]73` exposed Chisel tunneling binaries, Python deployers, JSON state files, active scanners, exploitation tooling, and a Sliver C2 configuration.

The durable defender lesson: PCPJack is not just a credential-stealing cloud worm. Public reporting now shows the operator can turn cloud footholds into reusable proxy infrastructure for spam, phishing, or other email-delivery abuse after initial compromise.

## Tags
- cloud
- Linux
- SMTP
- proxy
- Sliver
- Chisel
- credential theft
- worm
- TeamPCP-adjacent
- cloud infrastructure

## Reported chain
- **Initial PCPJack behavior:** SentinelOne reported PCPJack as a cloud credential-theft framework that worms through exposed Docker, Kubernetes, Redis, MongoDB, RayML, and vulnerable web applications, harvests cloud, container, developer, productivity, and financial credentials, and removes artifacts associated with TeamPCP / PCPcat-style infections.
- **Observed exposed infrastructure:** Hunt.io found two unauthenticated directories on `213.136.80[.]73`, a server already tied to PCPJack C2 infrastructure.
  - Port `8444` exposed a 12-file SMTP proxy deployment toolkit: source, compiled binaries, and state artifacts.
  - Port `9443` exposed the operator's live working directory, scanners, exploitation tooling, and a Sliver C2 configuration.
- **Proxy deployment:** The toolkit used stock `jpillora/chisel` builds for multiple Linux CPU architectures and deployed victim-side binaries as hidden dot-prefixed files, including persistence at `/var/tmp/.xs`.
- **Beacon-driven automation:** Recovered deployers connected to the local Sliver client API, selected Linux beacons that had recently checked in, and mapped each beacon UUID deterministically into SOCKS5 proxy ports.
- **Relay purpose:** Hunt.io reported an SMTP quality gate and a standalone verification daemon, indicating the converted hosts were intended for email relay rather than generic proxy resale alone.
- **Scale:** A version-3 state file reportedly confirmed **230 successful uploads and executions** in one March 2026 deployment run across AWS, Google Cloud, and Azure-hosted systems.
- **Downstream synchronization:** Verified proxy lists were synchronized every five minutes by SCP to `38.242.204[.]245`, which Hunt.io could not access during analysis.

## TeamPCP relationship caveat
SentinelOne framed PCPJack as evicting or removing TeamPCP-associated artifacts rather than as a confirmed TeamPCP operation. Hunt.io also treats the recovered relay deployment as connected to PCPJack infrastructure, not as proof that TeamPCP controlled the SMTP relay network. Track it as **TeamPCP-adjacent / anti-TeamPCP cloud crimeware activity** until public reporting establishes a stronger actor relationship.

## Defender takeaways
- Treat exposed cloud services and internet-reachable workload APIs as potential **relay infrastructure**, not only cryptomining or credential-theft risks.
- Hunt for Sliver and Chisel activity on Linux cloud workloads, especially hidden or system-looking binaries under `/var/tmp/`, `/tmp/`, or service-manager paths.
- Investigate unusual SOCKS5 listeners, deterministic high-port allocations, and host egress patterns that test or relay SMTP.
- Watch for credential theft plus immediate infrastructure repurposing: PCPJack's public tradecraft spans credential harvesting, lateral propagation, Sliver beacons, and proxy conversion.
- Cloud providers and defenders should correlate abuse complaints for outbound email with preceding exposed-service compromise, because compromised hosts may be used as mail relays after the original intrusion.
- Do not rely on hash-only Chisel detections; Hunt.io reported unmodified stock Chisel builds, which can match legitimate upstream binaries.

## Indicators from public reporting
| Indicator | Role |
| --- | --- |
| `213.136.80[.]73` | PCPJack infrastructure exposing deployment and working directories |
| `38.242.204[.]245` | Downstream SCP synchronization target for verified proxy lists |
| `/var/tmp/.xs` | Victim-side Chisel persistence path reported by Hunt.io |
| `/root/.sliver-client/configs/root_localhost.cfg` | Sliver client configuration path in recovered deployer logic |
| `10000`-`14999` | Reported deterministic SOCKS5 port range derived from Sliver beacon UUIDs |
| `9000`, `8080`, `2053` | Excluded / infrastructure-related ports in recovered deployer logic |

## Sources
- Hunt.io: PCPJack hijacked 230 AWS, GCP, and Azure servers to run a hidden SMTP relay network: [https://hunt.io/blog/pcpjack-230-cloud-servers-smtp-proxy-network-sliver-chisel](https://hunt.io/blog/pcpjack-230-cloud-servers-smtp-proxy-network-sliver-chisel)
- SentinelOne: PCPJack cloud worm evicts TeamPCP and steals credentials at scale: [https://www.sentinelone.com/labs/cloud-worm-evicts-teampcp-and-steals-credentials-at-scale/](https://www.sentinelone.com/labs/cloud-worm-evicts-teampcp-and-steals-credentials-at-scale/)
- The Hacker News: PCPJack hijacks 230 AWS, Google Cloud, and Azure servers for covert SMTP relay network: [https://thehackernews.com/2026/06/pcpjack-hijacks-230-aws-google-cloud.html](https://thehackernews.com/2026/06/pcpjack-hijacks-230-aws-google-cloud.html)
