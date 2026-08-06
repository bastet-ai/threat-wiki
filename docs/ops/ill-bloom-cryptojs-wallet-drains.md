# Ill Bloom CryptoJS wallet-drain campaign

## Summary
On August 5–6, 2026, Coinspect publicly identified the weak generator behind its **Ill Bloom** investigation as `CryptoJS.lib.WordArray.random()` and named five wallet applications that used the function to create recovery phrases. The affected code reduced nominal 128- and 256-bit entropy to effective search spaces of about **2^39** and **2^47**, making candidate recovery phrases enumerable on commodity hardware.

Coinspect measured two exploitation waves beginning May 27. Across the monitored address set, attackers drained about **$5.69 million** from 431 accounts in the first wave and addresses associated with 522 seeds in the second, spanning Bitcoin, Ethereum, Tron, Rootstock, and Polygon. The figure is a measured lower bound, not a complete loss estimate.

This is a historical-secret compromise. Updating CryptoJS or a wallet application does not make an already generated phrase safe. Affected users must create a new seed through a confirmed cryptographically secure path and move all assets; importing the old phrase into patched software or a hardware wallet preserves the weakness.

## Tags
- ops
- operations
- Ill Bloom
- CryptoJS
- crypto-js
- GHSA-rg76-677x-56q9
- weak entropy
- weak RNG
- pseudorandom number generator
- Multiply-With-Carry
- BIP-39
- recovery phrase
- cryptocurrency theft
- wallet theft
- Bitcoin
- Ethereum
- Tron
- Rootstock
- Polygon
- RRWallet
- Bexo Wallet
- NanChat
- Bitcoin Libre
- Milo Wallet
- active exploitation
- incident response

## Why this matters
- The weak generator existed in widely used CryptoJS 3.x releases for years, and a temporary correction in 3.2.0 and 3.2.1 was reverted in 3.3.0. An ordinary dependency upgrade within 3.x could therefore reintroduce the unsafe implementation.
- Dependency presence alone is not evidence of exploitable wallet generation. Defenders and maintainers must trace whether `WordArray.random()` supplied security-sensitive entropy on the actual generation path.
- Hashing, PBKDF2, or another KDF cannot restore entropy that was absent at generation time.
- Discontinued applications and unavailable historical builds make affected-user discovery and notification incomplete.
- Public blockchain history gives attackers a validation oracle: generated candidates can be converted to addresses and checked for activity and funds.

## Root cause and affected library versions
The vulnerable implementation was introduced in CryptoJS `3.1.2-4` in June 2014. It used a custom variation of George Marsaglia's Multiply-With-Carry generator seeded from `Math.random()`, rather than a cryptographically secure random source.

CryptoJS 3.2.0 and 3.2.1 temporarily switched to native cryptographic randomness. Version 3.3.0 restored the weak generator because the earlier change was treated as breaking. Version 4.0.0 permanently moved to the platform's native cryptographic API in February 2020.

GitHub advisory `GHSA-rg76-677x-56q9` lists npm package versions below 4.0.0 as affected and 4.0.0 or later as patched, while its technical description records the 3.2.0 and 3.2.1 exceptions. The broad package range should not be used as a standalone exposure verdict: an application is vulnerable only where the unsafe function generated a secret, key, nonce, recovery phrase, or other security-sensitive value.

Coinspect identified the React Native-oriented `ferrumnet/bip39` fork as one route into wallet applications. The fork replaced upstream `bip39` native randomness with CryptoJS, but it is not necessarily the only downstream path.

## Confirmed wallet applications
This list is confirmed but explicitly incomplete.

| Application | Public status | Confirmed remediation |
| --- | --- | --- |
| RRWallet / RenrenBit | Discontinued | No fix available |
| Bexo Wallet | Active | Coinspect reports a fix in 20.1.0; public reporting on August 6 could not confirm that updated store builds were available |
| NanChat | Active | 1.3.0; wallets created before 1.3.0 should migrate through the built-in tool |
| Bitcoin Libre | Active | Version 4, released July 2024 |
| Milo Wallet | Discontinued | No fix available |

The public disclosure does not provide complete vulnerable-version ranges for RRWallet, Bexo Wallet, Bitcoin Libre, or Milo Wallet. Application version and dependency evidence must be combined with the time and code path used to create the phrase.

## Exploitation and loss scope
Coinspect reproduced the attack chain by enumerating outputs from the affected generator, converting them to BIP-39 recovery phrases, deriving addresses, and comparing those addresses with public blockchain data.

- **May 27:** the first observed sweep took about $3.14 million from 431 accounts.
- **May 30–July 13:** a second wave drained addresses associated with 522 seeds for about $2.55 million, including roughly $2.18 million USDT from one Tron account on July 4.
- **Measured total through July 13:** $5,690,922 across the two waves.
- **Monitored set:** 2,114 seeds with on-chain activity across Bitcoin, Ethereum, Tron, Rootstock, and Polygon.

These measurements cover Coinspect's known address set. They do not prove that every weak seed, affected wallet product, network, or theft has been identified. Coinspect estimates that the exposed population reaches into the thousands across Bitcoin and EVM-compatible networks but has not published a wallet-by-wallet victim count.

## Owner response
1. Determine **where and when the recovery phrase was generated**. Current application version, current CryptoJS version, or later import into a hardware wallet does not answer that question.
2. If the phrase came from a confirmed affected version or its origin is uncertain, treat it as compromised.
3. Obtain migration instructions only from the wallet project's verified official channels. Confirm that the replacement version and secure generation path are actually available before creating a new phrase.
4. Generate a completely new seed through a confirmed cryptographically secure source. Do not transform, hash, extend, or re-import the old phrase.
5. Verify the new receive address on a trusted display, test with a small transfer, then move all assets and tokens on every supported chain.
6. Update counterparties, recurring payment instructions, application logins, and allowlists that depend on the old address. Never send new funds to the old phrase.
7. Preserve transaction IDs, wallet and application versions, installation history, addresses, timestamps, and vendor correspondence without exposing recovery phrases or private keys.
8. Never enter a phrase or private key into an online “checker.” Coinspect's public exposure checker accepts addresses only; a negative result means only that the submitted address is absent from the published dataset.

NanChat's first-party advisory says users who created a wallet before 1.3.0 should consider it compromised and migrate. Imported phrases generated securely elsewhere and Ledger-backed wallets are outside NanChat's affected generation path, but their original generation source must still be trustworthy.

## Developer and defender actions
- Search source, lockfiles, historical releases, minified bundles, mobile packages, and software bills of materials for `crypto-js`, `WordArray.random()`, and downstream forks such as `ferrumnet/bip39`.
- Prove data flow from entropy generation to secrets; do not classify every application carrying CryptoJS below 4.0.0 as exploitable.
- Review historical builds, not only the current release. Retain signed packages and reproducible-build evidence so discontinued generation paths can be reconstructed.
- Identify users by generation version and time where privacy-preserving telemetry permits it, then issue explicit seed-migration guidance. A generic “update the app” notice is insufficient.
- Replace insecure generation with the platform CSPRNG and add deterministic tests that fail if entropy calls resolve to `Math.random()`, noncryptographic PRNGs, or fallback implementations.
- Treat cryptographic-key and recovery-phrase flaws as incident-response events requiring secret replacement, not ordinary patch-only vulnerabilities.

## Evidence and attribution limits
Coinspect links the measured drains to recovery phrases produced by the weak generation process through reproduced generation, address derivation, and on-chain analysis. Public reporting does not identify the theft operator, establish initial access to wallet applications, or show that CryptoJS itself was maliciously modified. This is insecure historical design propagated into downstream wallet generation, followed by exploitation of predictable secrets.

The five named applications are confirmed examples, not an exhaustive product inventory. A vulnerable CryptoJS dependency is a discovery lead; exploitability requires evidence that the function generated the relevant secret.

## Related pages
- [COLDCARD predictable-RNG Bitcoin theft risk](coldcard-predictable-rng-bitcoin-theft.md)
- [OkoBot cryptocurrency-wallet malware framework](okobot-cryptocurrency-wallet-framework.md)
- [Injective SDK npm wallet stealer](injective-sdk-npm-wallet-stealer.md)
- [Silent Swap Google Notes crypto clipper](silent-swap-google-notes-crypto-clipper.md)

## Sources
- Coinspect / Ill Bloom, “Technical Disclosure: The CryptoJS Randomness Vulnerability,” August 2026: [https://illbloom.org/articles/cryptojs-vulnerability/](https://illbloom.org/articles/cryptojs-vulnerability/)
- Coinspect / Ill Bloom, “Identifying the Wallets Behind Vulnerable Recovery Phrases,” August 2026: [https://illbloom.org/articles/identifying-wallets-vulnerable-recovery-phrases/](https://illbloom.org/articles/identifying-wallets-vulnerable-recovery-phrases/)
- Coinspect / Ill Bloom, “Second Wave of Wallet Drains Analysis,” updated July 2026: [https://illbloom.org/articles/chain-analysis-2/](https://illbloom.org/articles/chain-analysis-2/)
- Coinspect, “Ill Bloom: Investigating a Wallet Generation Vulnerability During Active Exploitation,” August 5, 2026: [https://www.coinspect.com/blog/ill-bloom-investigation/](https://www.coinspect.com/blog/ill-bloom-investigation/)
- CryptoJS maintainer advisory `GHSA-rg76-677x-56q9`, August 5, 2026: [https://github.com/brix/crypto-js/security/advisories/GHSA-rg76-677x-56q9](https://github.com/brix/crypto-js/security/advisories/GHSA-rg76-677x-56q9)
- NanChat, “Security Advisory: Wallet Migration”: [https://nanchat.com/security/](https://nanchat.com/security/)
- The Hacker News, “CryptoJS Weak RNG Behind $5.7 Million in Drains Affects Five Crypto Wallet Apps,” August 6, 2026: [https://thehackernews.com/2026/08/cryptojs-weak-rng-behind-57-million-in.html](https://thehackernews.com/2026/08/cryptojs-weak-rng-behind-57-million-in.html)
