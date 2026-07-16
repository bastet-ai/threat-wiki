# RustDuck

## Summary
RustDuck is a two-stage DDoS botnet family tracked by QiAnXin XLab from activity beginning in February 2026. XLab describes a **Loader + Core** architecture with multiple variants, cross-platform targeting, and a rapid transition from C implementations toward Rust. The name comes from early core payloads that encrypted three `duckdns` C2 domains.

The durable defender signal is the propagation mix: weak Telnet/SSH passwords, IoT and network-device vulnerabilities, Android ADB exposure, and web/application RCEs across Jenkins, YARN, ThinkPHP, and other components. That combination lets a DDoS crew reuse the same payload ecosystem across routers, cameras, Android terminals, servers, and enterprise edge infrastructure.

## Tags
- tools
- malware
- botnet
- DDoS
- Rust
- IoT botnet
- weak passwords
- Telnet brute force
- SSH brute force
- Android ADB
- web RCE
- loader
- AES-GCM C2
- duckdns
- QiAnXin XLab

## Why this matters
- XLab says RustDuck is not yet comparable to the largest mainstream DDoS botnets, but its engineering pace is notable: loader formats, packing, encryption, decompression, and C2 handling changed across observed variants.
- The spread chain blends opportunistic internet scanning with a broad exploit set. XLab names Android ADB, TVT API, Ruijie, TP-Link, ZTE, ThinkPHP, Jenkins, YARN, and historical CVEs including CVE-2025-29635, CVE-2017-17215, CVE-2018-8007, and CVE-2024-1781.
- The C2 protocol attempts to blend with encrypted web traffic by using an SSL-like header pattern, then protects command traffic with AES-GCM and separate uplink/downlink key material.
- Commands include DDoS attack launch, emergency stop, host status reporting, remote hot update, and dynamic C2 update, so infected devices can be retasked or moved to new infrastructure without reinstalling.

## Reported propagation and infrastructure
- XLab observed more than 20 IPs participating in RustDuck propagation; the most active implant source reported was `176.65.139[.]204`.
- Propagation paths include weak-password brute forcing over Telnet/SSH plus exploitation of IoT, device, and web/component RCE paths.
- Early naming pivots came from C2 domains under `duckdns.org`; XLab also published additional domains such as `gayporn.twilightparadox[.]com`, `bigniggadick.ignorelist[.]com`, `ilovefemboy.mooo[.]com`, `disciplinenahidwin[.]st`, and `criminalcloudflare[.]online`.

## Loader and C2 notes
XLab clustered loader evolution into four stages:

| Stage | SHA1 prefix | Config/decode traits |
| --- | --- | --- |
| Variant 1 | `8315f650` | 16-byte config, LCG + XOR decryption, LZ4 decompression, dynamic magic verification |
| Variant 2 | `6aa791c7` | 33-byte config, Xoshiro128 + XOR, BLZ decompression, dynamic constants |
| Variant 3 | `4d11bd49` | 48-byte config, standard XOR, LZ4, fixed `ASHPCK` plaintext marker |
| Variant 4 | `d39a3ee9` | 32-byte config, ChaCha20, LZ4, fixed `iEMPK` plaintext marker |

The command loop uses a TLS-looking `0x17 0x03 0x03` prefix, a nonce, ciphertext, and authentication tag. XLab reports AES-GCM transport encryption with separate client and server key/nonce material derived after the handshake.

## Defender heuristics
- Treat exposed Telnet, SSH, ADB, Jenkins, YARN, ThinkPHP, and management-plane services as botnet recruitment surfaces, not only as commodity scanner noise.
- Block or monitor known RustDuck propagation infrastructure and C2 domains from XLab's report; use passive DNS and proxy telemetry to pivot on dynamic-DNS hostnames that resolve near known implant-source IPs.
- Hunt edge and IoT fleets for ELF payloads with appended overlay configuration data, LZ4/BLZ decompression routines, ChaCha20 or AES-GCM code paths, and TLS-looking traffic that does not complete normal TLS negotiation.
- Watch for processes on routers, cameras, Android terminals, and Linux servers that initiate outbound dynamic-DNS lookups followed by sustained encrypted-looking sessions and sudden UDP/TCP flood traffic.
- For response, preserve the sample and overlay data before cleaning; the loader configuration may contain the current C2 list, decompression settings, and variant markers needed to scope related infections.

## Related pages
- [xlabs_v1 DDoS-for-hire IoT botnet](../ops/xlabs-v1-ddos-for-hire-iot-botnet.md)
- [JDY SOHO / IoT reconnaissance botnet](../ops/jdy-soho-iot-recon-botnet.md)
- [AryStinger legacy-router recon proxy network](../ops/arystinger-legacy-router-recon-proxy-network.md)

## Sources
- QiAnXin XLab: [https://blog.xlab.qianxin.com/rustduck-en/](https://blog.xlab.qianxin.com/rustduck-en/)
- The Hacker News summary: [https://thehackernews.com/2026/06/rustduck-botnet-rebuilds-in-rust-to.html](https://thehackernews.com/2026/06/rustduck-botnet-rebuilds-in-rust-to.html)
