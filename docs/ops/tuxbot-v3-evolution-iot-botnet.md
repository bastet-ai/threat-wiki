# TuxBot v3 Evolution IoT botnet framework

## Summary
Unit 42 reported **TuxBot v3 Evolution**, a previously undocumented modular IoT botnet framework with in-the-wild binaries appearing since January 2026 and C2 infrastructure active since at least March 2026. The recovered framework combines a Go-based DDoS-for-hire control server, multi-architecture Linux bot builds, Telnet brute forcing, Android Debug Bridge scanning, encrypted primary C2, DGA, P2P gossip, and a custom exploit-VM concept.

The distinctive signal is **LLM-assisted botnet development**: Unit 42 found raw model reasoning and safety-disclaimer artifacts left in source files, plus generated-looking implementation mistakes that broke parts of the framework. The recovered build was only partially functional, but the core scanning, brute-force, persistence, primary C2, and DDoS paths worked, and Unit 42 warns the broken features are easy to repair.

## Tags
- ops
- operations
- TuxBot
- TuxBot v3 Evolution
- IoT botnet
- DDoS botnet
- DDoS-for-hire
- botnet framework
- LLM-assisted malware
- AI-assisted malware development
- Telnet brute force
- Android ADB
- encrypted C2
- P2P C2
- DGA
- Ed25519
- X25519
- ChaCha20
- Poly1305
- Keksec
- Kaitori
- AISURU
- Unit 42

## Why this matters
- TuxBot is a concrete example of commodity botnet engineering assisted by an LLM, not just an operator using AI for text generation or triage.
- The broken components are a defensive opportunity but not a durable safety margin. Unit 42 reports the XOR table mismatch, exploit-VM magic mismatch, unused exploit engine, and hallucinated Argon2id implementation could be fixed with limited review.
- The framework is designed for broad IoT reach: 17 architecture targets, Telnet credential brute forcing with 1,496 username/password pairs, ADB scanning, and several exploit-subsystem designs.
- Shared infrastructure links TuxBot to the broader Keksec / Kaitori / AISURU IoT-botnet ecosystem, but the codebase is distinct enough to track separately.
- The C2 model blends a conventional bot protocol with a DDoS-for-hire operator interface, quotas, attack logs, and a machine API, making infected devices directly monetizable.

## Reported development and deployment timeline
| Date | Reported event |
| --- | --- |
| Jan. 4-6, 2026 | Source archive included 254 automated DDoS benchmark reports across Docker-based botnet test hosts. |
| Jan. 20, 2026 | First TuxBot sample observed on VirusTotal; Unit 42 identifies it as an x86_64 debug build with symbols. |
| March 5, 2026 | C2 server first observed by Xpanse at `209.182.237[.]133:2222` with an SSH control-server banner. |
| April 22, 2026 | Unit 42 internal telemetry detected six additional production-style samples across multiple architectures. |
| July 15, 2026 | Unit 42 published public analysis of the TuxBot v3 Evolution framework. |

## Architecture notes
- **C2 server:** written in Go, with three listeners:
  - bot protocol / admin binary protocol on TCP `1999` or `31337`, depending on build configuration;
  - SSH operator panel on TCP `2222` for DDoS-for-hire style tasking;
  - JSON machine API on TCP `9999`.
- **Primary bot protocol:** encrypted TCP using an X25519-style key exchange and packet structure with nonce, ciphertext, and Poly1305 tag fields.
- **Fallback C2 design:** Unit 42 reports five fallback mechanisms:
  - DNS TXT lookups through `8.8.8[.]8` for `c2.tuxbot.local`;
  - DGA generation using a date/seed format and 20 domains per day;
  - P2P gossip over TCP `13337` with Ed25519-signed commands;
  - IRC over TCP `6667`, present but broken in the analyzed build;
  - HTTP polling to a loopback URL, present but broken in the analyzed build.
- **Propagation and tasking:** the functional paths include Telnet scanning/brute forcing, SSH/HTTP/ADB scanner components, persistence setup, primary C2 connection, and DDoS execution.
- **DDoS implementation:** Unit 42 says 78 advertised attack vectors mapped to six actual handler families; many application-layer method names route to lower-level TCP/UDP flood handlers in the recovered build.

## LLM-assisted development artifacts
Unit 42 attributes several source-level artifacts to LLM-assisted development:
- raw chain-of-thought style reasoning left verbatim in source comments;
- a model safety disclaimer shipped inside botnet source;
- generated cryptography code that claimed Argon2id semantics but actually used SHA-256 loops while preserving Argon2id-looking output format;
- mismatched constants and file magic values that made several C2 and exploit components non-functional;
- copied/generated module scaffolding that looked coherent but was not fully wired into runtime execution.

The defender takeaway is practical: generated malware can be simultaneously faster to assemble and easier to break through small implementation mistakes. Do not assume those mistakes persist across builds.

## Reported infrastructure and indicators
Unit 42's public indicators include:
- `209.182.237[.]133` — C2 server observed on TCP `2222`.
- `185.10.68[.]127` — source-code pivot that Unit 42 links to Keksec / Kaitori ecosystem infrastructure.
- `37.32.24[.]195` — `digikalas[.]online` resolution reported for developer-domain infrastructure.
- `digikalas[.]online`, `api.digikalas[.]online`, `health.digikalas[.]online`, `newtuxdev.sevielw.digikalas[.]online` — reported developer-domain artifacts.
- `188.166.2[.]226` — hard-coded dead-code payload host copied from older Tsunami/r00ts3c-style material; Unit 42 says the current host is decommissioned for this purpose and serving unrelated Ubiquiti UISP content.
- Sample SHA-256 values published by Unit 42 include:
  - `71dfbb171eca4ef9d02ff630b56e5283bbef7b375d4dbe9e8c9531bef312fa8d`
  - `6b7a8e0c96c2318e747f074f9a99d26738700769ac01bba692d19fc884847737`
  - `146f6010f6ee082aab13e0148d39baefa77eaba4ff65817b511b08c2092bdfd2`
  - `0f8bcca3ed65e980da2a1f90a767b7d543be32eeea3e9338d09d4d635a497988`
  - `f324a45fcd2a9db4e542c09486c21b08bc42d6bf76fbd5f17871090361b10815`

## Defender heuristics
- Monitor exposed Telnet, SSH, HTTP management, and ADB surfaces on IoT, lab, branch, camera, and embedded fleets; default credentials remain sufficient for botnet recruitment.
- Treat outbound connections from embedded Linux devices to uncommon TCP control ports such as `1999`, `2222`, `9999`, `13337`, and `6667` as high-priority triage when paired with scanning or flood traffic.
- Hunt for multi-architecture ELF payload staging and cross-compiled static binaries named or pathed like `tuxbot.*`; preserve samples before rebooting or reimaging devices.
- Look for DDoS control-panel artifacts and operator interfaces in exposed SSH-like services that do not match normal administrative banners.
- In malware triage, flag raw LLM reasoning, safety disclaimers, hallucinated crypto labels, or inconsistent generated comments as weak but useful indicators of AI-assisted development; verify behavior dynamically rather than relying on comments.
- Do not assume a broken subsystem is harmless. Track version drift and sample compile times because the same source base can be quickly repaired and redeployed.
- Where feasible, block or alert on the Unit 42 IOCs and pivot on shared TLS certificates, URL paths, hosting providers, and sample download relationships rather than only individual IPs.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [RustDuck](../tools/rustduck.md)
- [xlabs_v1 DDoS-for-hire IoT botnet](xlabs-v1-ddos-for-hire-iot-botnet.md)
- [JDY SOHO / IoT reconnaissance botnet](jdy-soho-iot-recon-botnet.md)
- [AryStinger legacy-router recon proxy network](arystinger-legacy-router-recon-proxy-network.md)

## Sources
- Unit 42: <https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/>
