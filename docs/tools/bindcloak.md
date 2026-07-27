# BINDCLOAK

## Summary
**BINDCLOAK** is a 64-bit C++ command-and-control implant documented by Zscaler ThreatLabz in July 2026. It was the final payload in a TELESHIM and MIXEDKEY intrusion chain targeting Middle Eastern government entities and beaconed to `cert.hypersnet[.]com`.

Public technical detail remains intentionally limited: Zscaler's Part 1 identifies BINDCLOAK, its delivery and victim-bound decryption path, one sample hash, and its C2 domain. ThreatLabz stated that a planned Part 2 will analyze the implant in depth.

## Tags
- tools
- malware
- implant
- backdoor
- BINDCLOAK
- Windows
- C++
- C2
- environmental keying
- reflective loading
- MIXEDKEY
- TELESHIM
- Middle East
- government targeting

## Delivery
- TELESHIM provides initial command execution and stages the next chain.
- MIXEDKEY is side-loaded through `pthreadVC2.dll`.
- The encrypted implant is stored as `C:\ProgramData\Crypto\DSS\C99F29AC08454855B3D538960BB2F34F.PCPKEY`.
- MIXEDKEY uses both file-contained XOR material and a key derived from the victim's volume serial number.
- The recovered PE has its `MZ` signature stripped and is reflectively loaded.

## Defender heuristics
- Hunt for the published `.PCPKEY` path and correlate access with the `Feedback` task, a GoPro service binary, `pthreadVC2.dll`, private executable memory, and traffic to the published C2.
- Preserve the encrypted file and original host volume metadata together.
- Treat DNS or connection attempts to `cert.hypersnet[.]com` from any process as a high-priority investigation pivot, while validating historical ownership and timing before broader attribution.
- Do not infer unsupported command capabilities until Part 2 or other primary analysis provides them.

## Public indicators
- Domain: `cert.hypersnet[.]com`.
- SHA-256: `3b0c658ebaa2bae80af97f390b9b2bb20a2f815eb584b2251255e84da4fa669d`.
- Encrypted staging file: `C:\ProgramData\Crypto\DSS\C99F29AC08454855B3D538960BB2F34F.PCPKEY`.

## Related pages
- [TELESHIM Middle East government espionage campaign](../ops/teleshim-middle-east-government-espionage.md)
- [TELESHIM](teleshim.md)
- [MIXEDKEY](mixedkey.md)

## Sources
- Zscaler ThreatLabz: [Targeted Attack on Government Entities in the Middle East — Part 1](https://www.zscaler.com/blogs/security-research/targeted-attack-government-entities-middle-east-part-1)
