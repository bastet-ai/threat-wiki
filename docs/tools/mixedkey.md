# MIXEDKEY

## Summary
**MIXEDKEY** is a 64-bit Windows reflective loader documented by Zscaler ThreatLabz in July 2026. It was deployed after TELESHIM in an East Asia-linked campaign against Middle Eastern government entities. The loader is side-loaded as `pthreadVC2.dll` by a legitimate GoPro service binary and decrypts a victim-bound BINDCLOAK implant from a `.PCPKEY` file.

## Tags
- tools
- malware
- loader
- MIXEDKEY
- Windows
- DLL side-loading
- reflective loading
- environmental keying
- volume serial number
- XOR
- control flow flattening
- mixed boolean arithmetic
- opaque predicates
- BINDCLOAK
- TELESHIM

## Reported execution chain
- The operator stages a legitimate GoPro binary, `MSVCP120.dll`, `MSVCR120.dll`, and malicious `pthreadVC2.dll` in a plausible `C:\ProgramData` vendor directory.
- A scheduled task named `Feedback` runs the legitimate binary every ten minutes.
- The binary side-loads `pthreadVC2.dll`.
- MIXEDKEY reads `C:\ProgramData\Crypto\DSS\C99F29AC08454855B3D538960BB2F34F.PCPKEY` and loads its decrypted payload from memory.

## Victim-bound decryption
1. Retrieve the host's four-byte volume serial number with `GetVolumeInformationA`.
2. Repeat it five times to form a 20-byte rolling XOR key.
3. Use the first 311 bytes of the `.PCPKEY` file as another rolling XOR key for the remainder.
4. Apply the volume-derived key to the first-stage plaintext.
5. Recover a PE with a stripped `MZ` signature and a prefixed four-byte payload size.
6. Reflectively load the PE and invoke its export.

MIXEDKEY also uses large numbers of mixed-boolean-arithmetic operations and opaque predicates. ThreatLabz reported roughly 1,000 instructions to compute a single runtime string byte.

## Defender heuristics
- Detect GoPro service binaries loading `pthreadVC2.dll` from `C:\ProgramData` rather than an expected product path.
- Hunt for the `Feedback` scheduled task, `.PCPKEY` extension, `C:\ProgramData\Crypto\DSS`, and the fixed published filename.
- Preserve the original volume serial number with the encrypted payload; off-host analysis without it may fail by design.
- Look for a signed or legitimate process reading the `.PCPKEY` file and then allocating or executing private memory.

## Public indicator
- SHA-256 `3b3eaea783fd6dab90f0408274bf8a9c49adbdc70c0efd70658d65b0e1684a3f` — `pthreadVC2.dll`.

## Related pages
- [TELESHIM Middle East government espionage campaign](../ops/teleshim-middle-east-government-espionage.md)
- [TELESHIM](teleshim.md)
- [BINDCLOAK](bindcloak.md)

## Sources
- Zscaler ThreatLabz: [Targeted Attack on Government Entities in the Middle East — Part 1](https://www.zscaler.com/blogs/security-research/targeted-attack-government-entities-middle-east-part-1)
