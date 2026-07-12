# jscrambler npm preinstall stealer

## Summary
StepSecurity's July 11, 2026 report describes a malicious `jscrambler@8.14.0` npm release that added a `preinstall` hook to unpack and execute a platform-specific native binary on Linux, Windows, and macOS. The affected package is the official CLI client for the Jscrambler Code Integrity API; StepSecurity compared `8.14.0` with the last known-clean `8.13.0` release and found the tarball grew from 37.8 kB to 7.9 MB.

Socket's follow-up reporting and npm registry metadata expand the exposure window beyond the first release: the same payload appeared in additional `jscrambler` releases `8.16.0`, `8.17.0`, `8.18.0`, and `8.20.0` over roughly three hours. The delivery path changed mid-incident: `8.14.0`, `8.16.0`, and `8.17.0` used `preinstall`, while `8.18.0` and `8.20.0` removed the install hook and instead injected the dropper into package runtime files so it would execute when the package was imported or the CLI was run.

The malicious release hides a custom binary container in `dist/intro.js`, extracts the host-matching payload into a randomly named temp-directory dotfile, and launches it detached from the npm install process. Static analysis points to cross-platform browser credential and crypto-wallet theft, with additional Linux eBPF instrumentation capability and anti-analysis / network-enumeration imports in platform binaries.

## Tags
- ops
- supply chain
- npm
- JavaScript
- package registry
- preinstall
- install-time execution
- credential theft
- browser credential theft
- cryptocurrency wallet theft
- MetaMask
- eBPF
- kernel instrumentation
- Rust
- AI developer tooling
- MCP credentials
- cloud credentials
- anti-analysis
- Jscrambler
- StepSecurity
- Socket

## Why this matters
- This is a trusted commercial developer-tool CLI, not a throwaway typosquat. Consumers may have installed it in developer workstations or CI/CD build jobs with high-value browser, registry, cloud, and signing credentials nearby.
- The malicious code runs at npm install time, before application code executes, and detaches a native process from the package-manager process tree.
- The payload is not JavaScript. Hiding three gzip-compressed native executables inside a JavaScript-named file reduces visibility for source-only package review.
- StepSecurity's analysis found indicators of credential-store, browser-cookie, Chromium LevelDB / extension-wallet storage, and BIP39 seed-phrase parsing capability.
- Socket's follow-up analysis reports broader developer-machine targeting, including encrypted configuration strings for AI developer tooling / MCP credentials, cloud metadata and credential stores, Kubernetes, AWS Secrets Manager / SSM, and wallet vault material.
- The actor's switch from install-time hooks to import/CLI-time execution is a useful detection lesson: controls that only alert on `preinstall` / `postinstall` scripts will miss source-file dropper injection in later malicious releases.
- If installed in CI/CD, every secret available to that job should be treated as exposed.

## Socket follow-up: runtime trigger shift
Socket's July 11 follow-up is the key post-initial-publication change: defenders need to treat the incident as a multi-version compromise with both install-time and runtime execution paths, not only as a single `preinstall` event.

## Reported timeline
- **June 30, 2026:** `jscrambler@8.13.0` published; StepSecurity identifies it as the last known-clean release.
- **July 11, 2026:** `jscrambler@8.14.0` published with the malicious `preinstall` path. The tarball grows to 7.9 MB and includes `dist/intro.js` as a 7.8 MB binary container.
- **July 11, 2026:** StepSecurity's OSS AI Package Analyst scores the release at maximum suspicion and publishes analysis.
- **July 11, 2026:** Socket reports that the same threat actor subsequently published `8.16.0`, `8.17.0`, `8.18.0`, and `8.20.0`. The first three malicious releases use `preinstall`; later releases move the same dropper into runtime package files.
- **July 11-12, 2026:** npm registry metadata marks `8.14.0`, `8.16.0`, `8.17.0`, and `8.20.0` as compromised / deprecated. At scan time, `8.18.0` had the suspicious no-script profile Socket described and should be treated as compromised even if local registry metadata does not show the same deprecation string.

## Technical details
The `8.14.0` package adds a `preinstall` script that reads `dist/intro.js`. StepSecurity reports the file is not JavaScript: it is a custom binary container with magic bytes `1B 43 53 49 01`, followed by repeated platform entries containing a platform ID, size fields, and gzip-compressed native payload data.

During install, the loader selects the entry matching `process.platform`, decompresses it into the OS temp directory as a randomly named dotfile, and launches it fully detached. The resulting process can continue after `npm install` completes.

Socket's later analysis found the payload bytes were unchanged across the malicious releases, but the JavaScript trigger moved. In `8.14.0`, `8.16.0`, and `8.17.0`, `package.json` contains `"preinstall": "node dist/setup.js"`. In `8.18.0` and `8.20.0`, the hook disappears and the dropper is injected into `dist/index.js` and `dist/bin/jscrambler.js`, shifting execution from package installation to import or CLI invocation.

Static analysis of the native payloads surfaced:

- embedded SQLite strings associated with Chrome and Firefox credential stores such as `Login Data`, `Cookies`, `Web Data`, and Firefox `key4.db`;
- embedded LevelDB strings matching Chromium Local Storage / IndexedDB storage used by browser-extension wallets such as MetaMask;
- an embedded BIP39 English wordlist for seed-phrase parsing or validation;
- Linux imports from `libbpf.so.1`, including `bpf_object__open_mem`, `bpf_object__load`, `bpf_program__attach`, and `bpf_map__fd`, indicating in-memory eBPF loading / kernel instrumentation capability;
- Windows anti-analysis and network-enumeration imports including `IsDebuggerPresent` and `GetExtendedTcpTable`.
- Socket identifies the embedded executables as Rust-built cross-platform infostealers and reports ChaCha20-Poly1305-encrypted configuration strings for browser / wallet data, AI developer tooling, cloud credentials, Kubernetes APIs, AWS Secrets Manager / SSM, GCP metadata, and multipart `/upload` exfiltration over TLS.

StepSecurity noted that recovery of full C2 details and deeper disassembly were still ongoing at publication time.

## Indicators
| Type | Value | Notes |
| --- | --- | --- |
| Malicious package | `jscrambler@8.14.0` | Presence in lockfiles, caches, or `node_modules` confirms exposure to the compromised version. |
| Malicious package | `jscrambler@8.16.0` | Same payload; `preinstall` delivery according to Socket and npm metadata. |
| Malicious package | `jscrambler@8.17.0` | Same payload; `preinstall` delivery according to Socket and npm metadata. |
| Malicious package | `jscrambler@8.18.0` | Same payload; runtime-file injection path according to Socket. Treat as compromised even where registry deprecation metadata is inconsistent. |
| Malicious package | `jscrambler@8.20.0` | Same payload; runtime-file injection path according to Socket and npm metadata. |
| Last known-clean package | `jscrambler@8.13.0` | StepSecurity's recommended downgrade target at publication time. |
| Suspicious file | `node_modules/jscrambler/dist/intro.js` | 7.8 MB custom binary container disguised as JavaScript; magic bytes `1B 43 53 49 01`. |
| Suspicious file | `node_modules/jscrambler/dist/setup.js` | Hook loader used by `8.14.0`, `8.16.0`, and `8.17.0`. |
| Suspicious file | `node_modules/jscrambler/dist/index.js` | Runtime-file injection path reported for `8.18.0` / `8.20.0`; diff against a clean release. |
| Suspicious file | `node_modules/jscrambler/dist/bin/jscrambler.js` | CLI runtime-file injection path reported for `8.18.0` / `8.20.0`; diff against a clean release. |
| Dropped file pattern | `<tmpdir>/.[a-z0-9]{6,}(.exe)` | Randomly named temp-directory dotfile written by the preinstall loader. |
| Linux payload SHA-256 | `fbbcf4d8f98168f78f5c0c47a9ae56d59ec8ac84a7c9ca6b797fedfb8d62d2bd` | Extracted ELF x86-64 payload. |
| Windows payload SHA-256 | `b7ca95d1b23c8e67416a25cedf741de0917c2096bbc9d24649eea7853d054903` | Extracted PE32+ payload. |
| macOS payload SHA-256 | `c8fd47d36bdf7c825378593ab82ed8c24d1dc52e26b507812393e24e1d5201fd` | Extracted Mach-O arm64 payload. |
| Outbound domain | `check.torproject.org` | Observed by StepSecurity Harden-Runner monitoring. |
| Outbound domain | `archive.torproject.org` | Observed by StepSecurity Harden-Runner monitoring. |
| Outbound IP | `37.27.122.124` | Observed by StepSecurity Harden-Runner monitoring. |
| Outbound IP | `57.128.246.79` | Observed by StepSecurity Harden-Runner monitoring. |

## Defender heuristics
- Search dependency manifests, lockfiles, SBOMs, npm caches, private registry mirrors, container layers, CI workspaces, and developer machines for `jscrambler@8.14.0`, `8.16.0`, `8.17.0`, `8.18.0`, and `8.20.0`.
- Hunt for `node_modules/jscrambler/dist/intro.js` near 7.8 MB and with magic bytes `1B 43 53 49 01`.
- Diff `dist/setup.js`, `dist/index.js`, and `dist/bin/jscrambler.js` against a verified clean `8.13.0` package. Do not rely only on package-manager lifecycle-script telemetry.
- Hunt temp directories (`/tmp`, `%TEMP%`, `$TMPDIR`) for recently created randomly named dotfiles matching the install window, and inspect orphaned or detached child processes spawned from `npm`, `node`, or package-manager jobs.
- If `8.14.0` was installed on a workstation, treat the host as compromised: rotate browser-saved credentials, SSO sessions, npm/GitHub tokens, cloud credentials, and any cryptocurrency wallet secrets that may have been accessible through browser-extension storage.
- If installed in CI/CD, rotate all secrets exposed to the job, including npm tokens, cloud credentials, repository tokens, deployment keys, and signing material.
- Prefer install-script controls and cooldown policies for newly published package versions; combine them with egress allow-listing so detached install-time binaries cannot freely reach unapproved destinations.

## Related pages
- [Injective SDK npm wallet stealer](injective-sdk-npm-wallet-stealer.md)
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)
- [IronWorm npm Rust infostealer campaign](ironworm-npm-rust-infostealer.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/jscrambler-npm-package-publishes-malicious-preinstall-binary
- Socket: https://socket.dev/blog/jscrambler-supply-chain-attack
- npm registry metadata: https://registry.npmjs.org/jscrambler
- Jscrambler GitHub issue #322: https://github.com/jscrambler/jscrambler/issues/322
