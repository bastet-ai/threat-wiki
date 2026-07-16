# Showboat

## Summary
Lumen Black Lotus Labs' May 2026 reporting describes **Showboat** as a previously unreported Linux post-exploitation framework used against telecommunications organizations since at least mid-2022. The tool can spawn a remote shell, transfer files, hide its process, maintain service persistence, swap command-and-control nodes, and expose SOCKS5 / port-mapping functionality for access to internal network systems.

Lumen assesses that Showboat was used by at least one, and likely several, PRC-aligned activity clusters. The publicly described activity includes a Middle East telecommunications victim, telecom-impersonation infrastructure in Southeast / Central Asia, and possible additional victim telemetry in the United States and Ukraine. Attribution is intentionally cautious because the same post-exploitation frameworks and infrastructure patterns may be shared across multiple China-aligned clusters.

## Tags
- tools
- malware
- Linux
- backdoor
- post-exploitation
- SOCKS5
- proxy
- portmap
- persistence
- C2
- telecom
- critical-infrastructure
- espionage
- PRC-aligned
- China
- Middle East
- Southeast Asia
- Ukraine

## Why this matters
- Showboat is built for foothold maintenance and internal pivoting on Linux systems that often have weaker EDR coverage than endpoints.
- The SOCKS5 and port-mapping functions let operators reach systems that are not internet-exposed but are accessible from the compromised host.
- Telecom targeting makes the tool strategically important: compromised carriers can become collection points, stepping stones, or supply-chain exposure for downstream customers.
- The infrastructure picture reinforces a recurring PRC-aligned pattern: shared or pooled post-exploitation frameworks complicate actor attribution and require defenders to track tool/infrastructure clusters separately from named groups.

## Operational characteristics
- Initial configuration retrieval from an embedded C2, with the public sample using `telecom.webredirect[.]org` and port `80`.
- Host survey collection including hostname, OS information, running processes, the agent process, and desktop screenshot data.
- Host metadata sent in a `PNG` field as encrypted / base64-encoded content.
- Built-in functions for file upload/download, process hiding, service persistence, C2 replacement, SOCKS5 proxying, and port mapping.
- The `hide` capability retrieves code from external dead-drop locations such as Pastebin or forums; Lumen noted one referenced Pastebin snippet from January 2022.
- SOCKS5 and port-map routines append different path markers (`SKS` and `MAP`) and support post-compromise movement into LAN-only systems.
- Configuration JSON is encrypted using the last five digits of the victim UUID as the key.

## Infrastructure notes
Lumen's public report identifies a primary cluster around `telecom[.]webredirect[.]org` resolving to `139.84.227[.]139`, with X.509 certificate metadata (`My Organization`) used as a clustering pivot. The same investigation linked additional C2 nodes and telecom-themed impersonation domains, including:

- `139.84.227[.]139` — original C2 associated with `telecom.webredirect[.]org`.
- `194.135.25[.]132` — second C2 reached through a matching certificate pivot and observed with an Afghanistan ISP Outlook server victim from December 2025 into February 2026.
- `23.27.201[.]160` / `singtelcom[.]site` — telecom-themed impersonation infrastructure.
- `101.36.105[.]222` / `kaztelecom[.]shop` — telecom-themed impersonation infrastructure.
- `116.169.244[.]208:2096` — China Unicom / Chengdu-adjacent node that Lumen treats as possible upstream or developer-test infrastructure.
- `192.9.141[.]111` — secondary-cluster C2 associated with two possible U.S. compromises over port `9999`.
- `64.176.43[.]209` — secondary-cluster C2 associated with possible Ukrainian-region victim traffic.

Certificate pivots called out by Lumen include SHA-256 prefixes / fingerprints such as `27df475626aafce2ea1548a9f35efb9ad951298c8b11a6adb3ccdfcd5170c677`, `A72427af3c046fd90999a6505b2372dc4ffde122227f30ed21621ecd4f2d3e8b`, `E28a96f983b8605decd2ac1db16ebad5fa741a6aa4e585a38ade0e5ad7d6cec0`, and a secondary-cluster fingerprint `2229e7f3cabbce4d67cd79c89fd5a100b20e8a99f4a2bf9aac77a978f49eb520`.

## Defender heuristics
- Monitor Linux servers, routers, and telecom-adjacent infrastructure for unexpected outbound HTTP/SOCKS5 traffic, especially to low-reputation VPS hosts or telecom-themed dynamic DNS / lookalike domains.
- Treat Linux hosts that begin proxying traffic on high ports such as `9999` as potential pivot points, not just infected endpoints.
- Hunt for service persistence added by unusual ELF binaries and for process-hiding behavior that requires cross-checking `/proc`, process lists, service units, network sockets, and file-system artifacts.
- Pivot from self-signed certificates with reused subject/issuer metadata, not just exact certificate hashes; Lumen's cluster analysis found related nodes with differing fingerprints but repeated metadata patterns.
- Give higher priority to east-west traffic from mail servers, routers, Linux jump hosts, and telecom edge systems where business processes do not require proxy behavior.

## Related pages
- [Webworm](../actors/webworm.md)

## Sources
- Lumen Black Lotus Labs: <https://www.lumen.com/blog/en-us/introducing-showboat-a-new-malware-family-taunts-defenses-and-targets-international-telecom-firms>
- The Hacker News summary: <https://thehackernews.com/2026/05/showboat-linux-malware-hits-middle-east.html>
