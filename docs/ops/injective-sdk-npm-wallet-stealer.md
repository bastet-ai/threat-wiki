# Injective SDK npm wallet stealer

## Summary
Socket's and StepSecurity's July 9, 2026 reports describe a short-lived but high-impact compromise of the Injective Labs TypeScript SDK release path. A malicious `@injectivelabs/sdk-ts@1.20.21` release was published to npm with fake telemetry logic that captured wallet mnemonic phrases and private-key material during normal library use, then exfiltrated the data through an Injective-looking public infrastructure endpoint.

The same `1.20.21` version was also published across 17 additional `@injectivelabs` scoped packages that directly or transitively pinned the compromised SDK version. This made the incident relevant to transitive dependency consumers, not only applications that depended on `@injectivelabs/sdk-ts` directly.

## Tags
- ops
- supply chain
- npm
- JavaScript
- TypeScript
- cryptocurrency
- wallet theft
- credential theft
- mnemonic theft
- private key theft
- maintainer compromise
- source repository compromise
- package registry
- transitive dependency
- Injective Labs
- Socket Security

## Why this matters
- The compromised package has roughly 50,000 weekly downloads and is used in wallet workflows where mnemonic phrases and private keys are expected to pass through the library.
- Socket says the malicious functionality did **not** run at install time; it triggered when normal key-derivation methods were used. That reduces visibility for controls focused only on npm lifecycle hooks.
- The attacker amplified blast radius by publishing matching `1.20.21` releases in other `@injectivelabs` packages that pinned the malicious SDK version.
- Socket reported the compromised npm version was deprecated but still downloadable at publication time, with GitHub release artifacts also still present.
- Any mnemonic or private key passed through the affected version should be treated as compromised, even if the malicious release was installed only briefly.

## Reported timeline
- **June 8, 2026 20:06 GMT+2:** Suspicious activity began in the official Injective Labs GitHub repository through commits from a developer account with prior contribution history. Socket notes a `test-backdoor-check` branch that appears to have tested access and permissions.
- **June 8, 2026 22:59 GMT+2:** `@injectivelabs/sdk-ts@1.20.21` was published with malicious code.
- **June 8, 2026 23:18 GMT+2:** The legitimate account owner appears to have reverted the malicious change.
- **June 8, 2026 23:48 GMT+2:** A clean version was published.
- **July 9, 2026 Socket publication:** Socket reported the malicious npm version was deprecated but not removed, release artifacts were still present in GitHub releases, and npm showed 310 downloads for the compromised version.

## Compromised package set
Socket identifies `@injectivelabs/sdk-ts@1.20.21` as the package containing the infostealer functionality. It also lists the following `1.20.21` packages as direct or transitive dependents pinned to the compromised SDK version:

- `@injectivelabs/sdk-ts@1.20.21`
- `@injectivelabs/utils@1.20.21`
- `@injectivelabs/networks@1.20.21`
- `@injectivelabs/ts-types@1.20.21`
- `@injectivelabs/exceptions@1.20.21`
- `@injectivelabs/wallet-base@1.20.21`
- `@injectivelabs/wallet-core@1.20.21`
- `@injectivelabs/wallet-cosmos@1.20.21`
- `@injectivelabs/wallet-private-key@1.20.21`
- `@injectivelabs/wallet-evm@1.20.21`
- `@injectivelabs/wallet-trezor@1.20.21`
- `@injectivelabs/wallet-cosmostation@1.20.21`
- `@injectivelabs/wallet-ledger@1.20.21`
- `@injectivelabs/wallet-wallet-connect@1.20.21`
- `@injectivelabs/wallet-magic@1.20.21`
- `@injectivelabs/wallet-strategy@1.20.21`
- `@injectivelabs/wallet-turnkey@1.20.21`
- `@injectivelabs/wallet-cosmos-strategy@1.20.21`

## Technical details
Socket located the malicious code in:

- `/dist/esm/accounts-jQ1GSgaW.js`
- `/dist/cjs/accounts-Cy0p4lLW.cjs`

The malicious release hooked regular key-derivation paths, including `PrivateKey.fromMnemonic` and `PrivateKey.fromHex`, and passed method markers plus sensitive derivation material to a `trackKeyDerivation` function. In the mnemonic path, the full mnemonic phrase was recorded. In the hex path, private-key material or a representation of it was recorded.

Socket reports that the records were base64-encoded and silently sent with a POST request to a character-obfuscated endpoint:

- `https://testnet[.]archival[.]chain[.]grpc-web[.]injective[.]network`

Using an Injective-looking public infrastructure endpoint could blend exfiltration with normal SDK traffic. The stolen material is sufficient for an attacker to regenerate private keys and access affected cryptocurrency wallets.

## Defender heuristics
- Search dependency manifests, lockfiles, SBOMs, private registries, build caches, container layers, developer workstations, CI runners, and deployed bundles for any `@injectivelabs/*@1.20.21` package.
- Do not limit review to direct dependencies. Audit transitive resolution paths because the companion `@injectivelabs` packages pinned `@injectivelabs/sdk-ts@1.20.21`.
- Move funds and rotate any mnemonic phrase, wallet seed, private key, or derived wallet material that may have passed through the affected package version.
- Upgrade affected packages to a known-clean release; Socket specifically points to clean `1.20.23` as the replacement available at publication time.
- Hunt package-install and runtime telemetry for use of `/dist/esm/accounts-jQ1GSgaW.js`, `/dist/cjs/accounts-Cy0p4lLW.cjs`, and POST traffic to `testnet[.]archival[.]chain[.]grpc-web[.]injective[.]network` from developer tools, CI, wallets, test suites, or application runtimes.
- Review GitHub, npm, SSO, and maintainer-account audit logs for suspicious branch creation, commits, release creation, npm publication, token use, MFA reset, and session activity around the June 8, 2026 compromise window.
- Treat this as source-repository and package-registry compromise until ruled out: clean rebuilds should evict npm caches, private registry mirrors, GitHub release artifacts, and generated bundles that could preserve the compromised files.

## Related pages
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)
- [Mastra easy-day-js npm scope compromise](mastra-easy-day-js-npm-scope-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- Socket: https://socket.dev/blog/compromised-injective-sdk-npm-package
- StepSecurity: https://www.stepsecurity.io/blog/injective-npm-supply-chain-attack-18-packages-backdoored-to-steal-crypto-wallet-keys
