# COLDCARD predictable-RNG Bitcoin theft risk

## Summary
On July 30–31, 2026, Coinkite and Block published emergency warnings that affected COLDCARD firmware generated Bitcoin wallet seeds through a deterministic MicroPython pseudorandom-number-generator fallback instead of the intended STM32 hardware random-number generator. Block says active exploitation is underway and that its investigation began after reports of COLDCARD users losing funds. Coinkite says funded wallets created on affected firmware are at risk unless sufficient independent private dice entropy or a strong, unique BIP-39 passphrase protects them.

The vulnerability is historical seed compromise, not merely a firmware-version problem. Installing fixed firmware corrects future generation but does **not** repair an existing seed. Restoring affected seed words onto updated firmware or another wallet preserves the weakness; users must generate a new seed on fixed firmware and migrate funds.

Public reporting associates the disclosure with a July 30 sweep of 1,196 Bitcoin addresses that moved 1,082.65 BTC, worth about $70.2 million at the time, in 41 minutes. That linkage remains circumstantial: no public report has reconstructed a victim seed and matched it to a swept address, and no actor has been identified.

## Tags
- ops
- operations
- COLDCARD
- Coinkite
- Bitcoin
- hardware wallet
- cryptocurrency theft
- wallet theft
- weak entropy
- random number generator
- PRNG
- MicroPython
- Yasmarang
- seed recovery
- BIP-39
- active exploitation
- firmware
- supply chain
- incident response

## Affected seed-generation scope
Exposure follows the firmware used when the secret was generated, not the device's current firmware or manufacturing date.

| Device | Publicly reported affected seed-generation firmware | Fixed release |
| --- | --- | --- |
| Mk2 / Mk3 | Coinkite: 4.0.1–4.1.9; Block: 4.0.0–4.1.9 | 4.2.0 or later |
| Mk4 / Mk5 standard track | Before 5.6.0 | 5.6.0 or later |
| Mk4 / Mk5 Edge track | Before 6.6.0X | 6.6.0X or later |
| Q standard track | Before 1.5.0Q | 1.5.0Q or later |
| Q Edge track | Before 6.6.0QX | 6.6.0QX or later |

Coinkite says TAPSIGNER, OPENDIME, and SATSCARD are unaffected because they use different codebases. Block places Mk1 and Mk2/Mk3 releases through 3.2.2 outside this regression because those versions used the direct STM32 hardware-RNG path.

The Mk2/Mk3 lower-bound discrepancy is operationally important. Coinkite's advisory starts at 4.0.1, while Block traces the vulnerable path into released version 4.0.0. Until the vendor reconciles this, treat a seed generated on 4.0.0 as potentially affected.

## Root cause and attack path
The 2021 migration to `libngu` moved wallet generation from `ckcc.rng_bytes()` to `ngu.random.bytes()`. COLDCARD's production board configuration defined `MICROPY_HW_ENABLE_RNG` as zero because the firmware supplied a separate hardware-RNG wrapper. However, `libngu` used an `#ifndef` guard that checked only whether the macro existed, not whether it was enabled.

The build therefore linked `rng_get()` to MicroPython's deterministic Yasmarang fallback. The fallback initialized itself from the microcontroller UID and timer registers and collected no new entropy after initialization. The intended hardware-RNG implementation remained present in the firmware binary, which helped the integration error survive code review: reviewers did not verify end-to-end symbol resolution and runtime reachability.

For Mk2/Mk3 version 4, no cryptographic entropy was added to the affected stream. For Mk4, Q, and Mk5, boot-time secure-element material was hashed but only four bytes reached `reseed()`, replacing one 32-bit Yasmarang state word. Hashing the resulting output and applying a BIP-39 checksum could make it appear statistically uniform but could not expand the number of possible inputs.

An attacker who can determine or constrain the device UID, timer state, prior RNG-call history, and later-model reseed value can generate candidates offline. A wallet address, xpub, or public key provides a validation oracle; a matching seed or private key permits theft without physical access to the wallet.

## Entropy and exploitability caveats
- Coinkite's current estimate is about 40 bits of effective search space for affected Mk2/Mk3 generation and about 72 bits for Mk4/Q/Mk5 under its assumptions.
- Block gives a broad known-UID ceiling of about 2^40.7 candidates for Mk2/Mk3 when treating timer fields independently, but notes that a stable RTC can narrow a cold-boot model to roughly 2^16.3 SysTick states.
- For later models, Block establishes at most 2^32 securely distinguished streams once fallback state and call history are fixed. Its looser hidden-timer ceiling is below 2^73.3, which it explicitly says is not equivalent to 73-bit cryptographic security.
- Practical cost depends on UID knowledge, boot timing, RNG-call history, derivation cost, and device behavior. Block did not claim a complete brute-force benchmark and had not completed full empirical exploit validation when it published.
- The bug also reaches some paper-wallet keys, random seed splits, cloning and transport ECDH keys, USB encryption, Web2FA material, and password-generation paths. Impact varies by feature and requires protocol-specific evidence; it should not be assumed that every affected call directly reveals the main wallet seed.

## Reported theft cluster
Galaxy Research mapped a July 30 transaction sweep covering 1,196 Bitcoin addresses and 1,082.65 BTC in 41 minutes. The sweep reportedly used a distinctive 30 sat/vB, no-change pattern not seen in other Bitcoin transactions during the prior 30 days.

That pattern can cluster transactions but does not prove the source keys came from COLDCARD. A legitimate owner sweep can look structurally similar, and public evidence does not yet connect a reconstructed affected seed, device, firmware, or victim to the transactions. Preserve the $70.2 million figure as an associated loss hypothesis rather than a confirmed vulnerability-loss total.

## Owner actions
1. **Do not generate another seed until the correct fixed release is installed.** Standard and Edge are separate release tracks; a numerically higher old Edge version is not necessarily fixed.
2. **Determine how the funded seed was created.** Record the model, firmware at generation time, whether at least 50 fair independent private dice rolls were mixed in, and whether funds require a strong unique BIP-39 passphrase. The COLDCARD PIN is not a BIP-39 passphrase.
3. **Treat uncertain history as exposure.** If the generation firmware, dice count, dice privacy, or passphrase strength cannot be established, migrate.
4. **Generate a completely new seed on fixed firmware.** Updating or restoring the old seed does not repair it. Do not derive the replacement from the affected seed.
5. **Verify before moving funds.** Back up and verify the new seed, wallet fingerprint, and receive address on the trusted device display. Send and confirm a small test transaction before moving the remainder.
6. **Move the remaining balance promptly but carefully.** Keep the old backup until the complete balance arrives and is confirmed. Avoid web-based seed tools, screenshots, digital dice-roll records, and untrusted recovery services.
7. **Review multisig composition.** Multisig mitigates this issue only when the signing quorum does not consist entirely of affected keys. Replace affected cosigner seeds and review quorum safety before relying on the arrangement.
8. **Protect possible evidence.** Preserve the model, serial and firmware history, wallet fingerprints, xpubs, transaction IDs, timestamps, support correspondence, and original backups without exposing seed words. Coordinate with Coinkite, wallet providers, exchanges, and appropriate authorities if theft is suspected.

Coinkite says a seed made with at least 50 fair, independent, private dice rolls is not at risk from this bug alone. A strong, unique, secret BIP-39 passphrase adds a separate barrier, but Coinkite still recommends migration because neither control repairs the affected seed. Short, reused, patterned, quoted, exposed, or uncertain passphrases do not qualify.

## Engineering lessons
- Verify entropy call graphs and linked symbols in production binaries; source presence and matching function signatures do not prove the intended implementation is reached.
- Fail builds when a hardware entropy provider is disabled, shadowed, or replaced. Test macro values rather than macro existence.
- Add known-answer, fault-injection, restart-diversity, and hardware-in-the-loop tests that distinguish a true entropy source from a deterministic generator that merely passes repetition checks.
- Preserve full entropy when mixing independent sources. Truncating a secure digest to 32 bits caps the number of securely distinguished states.
- Fail closed on entropy-source initialization and health failures. A PRNG producing nonrepeating adjacent values is not evidence of unpredictability.
- Incident response for key-generation flaws must address every historical secret, not only deploy patched software.

## Timeline
- **2021-03-01:** Block traces the wallet-generation migration to the vulnerable `libngu` path to commit `b18723dd`.
- **2021-03-17:** Block says Mk2/Mk3 firmware 4.0.0 first released the affected path; Coinkite's current affected table begins at 4.0.1.
- **2022-03:** Mk4 added secure-element reseeding, but only 32 bits reached the PRNG reseed state.
- **2026-07-30:** Block and other researchers began investigating reports of COLDCARD fund loss, root-caused the RNG issue, notified Coinkite, and published early because it assessed active exploitation.
- **2026-07-30:** Coinkite issued its preliminary warning.
- **2026-07-30:** The associated 1,196-address Bitcoin sweep occurred; public evidence has not proven causal linkage.
- **2026-07-31 to 2026-08-01:** Coinkite released and documented fixed standard and Edge firmware across affected models and expanded its technical and migration guidance.

## Evidence and attribution limits
The root cause and affected generation paths are supported by independent Block analysis and Coinkite's first-party advisory. Exact attack cost remains model-dependent, and Block's publication was an early analysis without complete empirical validation. Coinkite says its formal review is still in progress.

No public source has identified the operator, established an initial victim list, measured how many affected seeds remain funded, or cryptographically linked the July 30 sweep to a recovered COLDCARD seed. Coinkite's speculation that an attacker may have used AI to review historical firmware is not supported by published forensic evidence and should not be treated as actor tradecraft or attribution.

## Related pages
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [Silent Swap Google Notes crypto clipper](silent-swap-google-notes-crypto-clipper.md)
- [Injective SDK npm wallet stealer](injective-sdk-npm-wallet-stealer.md)
- [Adform Trackpoint JavaScript supply-chain crypto clipper](adform-trackpoint-javascript-supply-chain-crypto-clipper.md)

## Sources
- Coinkite, “COLDCARD Security Advisory,” updated 2026-08-01: [https://blog.coinkite.com/coldcard-mk3-seed-generation-warning/](https://blog.coinkite.com/coldcard-mk3-seed-generation-warning/)
- Coinkite, “Technical Deep Dive into the Entropy Issue,” updated 2026-08-01: [https://blog.coinkite.com/entropy-technical-backgrounder/](https://blog.coinkite.com/entropy-technical-backgrounder/)
- Block Bitcoin Engineering and Security, “Predictable RNG Fallback and 32-Bit Reseed in COLDCARD Firmware,” 2026-07-30: [https://engineering.block.xyz/blog/predictable-rng-fallback-and-32-bit-reseed-in-coldcard-firmware](https://engineering.block.xyz/blog/predictable-rng-fallback-and-32-bit-reseed-in-coldcard-firmware)
- The Hacker News, “Coldcard Hardware Wallet Flaw Linked to $70 Million Bitcoin Theft in 41 Minutes,” 2026-08-01 (secondary reporting for Galaxy Research sweep context): [https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html](https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html)
