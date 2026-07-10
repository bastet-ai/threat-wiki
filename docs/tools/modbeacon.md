# MODBEACON

## Summary
**MODBEACON** is a Windows x64 memory-resident stage / implant reported by Qianxin Threat Intelligence Center's Red Raindrop Team in July 2026. Qianxin observed the malware in **Operation Phnom Penh**, where a Silver Fox / UTG-Q-1000 Ghost distributor delivered a custom Trojan to selected victims instead of only commodity fake-software payloads.

The durable defender signal is the transport and plugin architecture: Qianxin reports a loader / beacon separation, injectable configuration, agent-token authentication, host fingerprinting, heartbeat and result reporting, in-memory plugin loading, and **gRPC over HTTP/2** C2 built on transport concepts from Xray/V2Ray-style anti-censorship proxy frameworks.

## Tags
- tools
- malware
- backdoor
- Windows malware
- Rust malware
- MODBEACON
- Silver Fox
- UTG-Q-1000
- Ghost
- ValleyRAT
- WinOS
- gRPC C2
- HTTP/2
- Xray
- V2Ray
- plugin architecture
- in-memory plugins
- Qianxin Threat Intelligence Center
- Red Raindrop Team

## Why this matters
- MODBEACON upgrades a noisy fake-software distribution ecosystem into a selective access-delivery mechanism: commodity SEO lures can become a route for higher-grade implants.
- gRPC bidirectional streaming over HTTP/2 can blend with legitimate service traffic and evade simplistic blocklists that key only on executable names or raw TCP beacons.
- The use of agent tokens, host fingerprinting, and in-memory native plugins gives defenders several telemetry points beyond static file hashes.
- Qianxin assesses the distributor as a hybrid threat actor: a traffic broker / cybercrime access supplier that can deliver advanced custom Trojans on demand.

## Reported behavior
- Delivered through Ghost infrastructure associated with counterfeit-software SEO campaigns.
- Ghost creates persistence for the MODBEACON stage using services, scheduled tasks, and a WMI permanent event subscription named `CBPUserTimer`.
- MODBEACON runs as a Windows x64 memory-resident stage / implant and appears Rust-based or statically linked with the Rust runtime.
- Communicates over TLS using gRPC over HTTP/2.
- Uses host fingerprinting, agent-token authentication, heartbeat, status reporting, and command-result reporting.
- Supports in-memory plugin loading and native-v3 plugin session capabilities with entry / init / fini style callbacks.
- Qianxin named the Trojan from the string `MODBEACON_AGENT_TOKEN_PATCH_V1`.

## Indicators
### MODBEACON C2
- `skystackservice[.]com`
- `fast-cloud-node[.]com`

### Ghost C2 / delivery infrastructure
- `www.nd9c887r[.]com`
- `www.damaix9k[.]com`
- `vaeth[.]cn`
- `182.16.88[.]242:22`
- `kkuu8899[.]org`

### MD5 hashes reported by Qianxin
- `13aff4f82171d42e7f0a72dc96346c45`
- `f6c69d8026d2114e5322f06f69471a6c`
- `9913b09fddbe47d4459c1ae0aa8c4953`
- `e32797efc17c8a9a663f6f0e64fcfa08`

### Counterfeit-domain / staging example
- `cn-mumu[.]com[.]cn`
- `https://asd268668.oss-ap-southeast-1.aliyuncs[.]com/MeiqiWintsetup_x64.zip`

## Defender heuristics
- Hunt for WMI permanent event subscriptions and timer consumers with unexpected names such as `CBPUserTimer`, especially on systems recently exposed to fake-software installers.
- Inspect endpoint telemetry for newly installed services or scheduled tasks that launch binaries from user-writable paths after software-download lures.
- Baseline gRPC / HTTP/2 outbound traffic from workstations; investigate unusual TLS destinations, especially to domains with CDN fronting plus no business owner.
- Search memory and EDR string telemetry for `MODBEACON_AGENT_TOKEN_PATCH_V1` and plugin-loading behavior from unsigned or recently downloaded binaries.
- Treat Ghost / ValleyRAT / WinOS infections as possible access-broker footholds, not just nuisance adware or fraud tooling.

## Related pages
- [MODBEACON Operation Phnom Penh](../ops/modbeacon-operation-phnom-penh.md)
- [WhatsApp VBScript ManageEngine RMM campaign](../ops/whatsapp-vbscript-manageengine-rmm-campaign.md)

## Sources
- Qianxin Threat Intelligence Center: https://ti.qianxin.com/blog/articles/operation-phnom-penh-silverfox-ghost-distributor-targets-specific-victims-with-modbeacon-en/
- The Hacker News: https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html
