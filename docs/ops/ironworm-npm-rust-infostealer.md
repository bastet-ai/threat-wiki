# IronWorm npm Rust infostealer campaign

## Summary
JFrog Security Research reported **IronWorm** on June 3, 2026: a self-replicating npm supply-chain campaign that starts from compromised developer/package-publisher access, ships a Linux Rust infostealer through npm `preinstall`, hides with an eBPF rootkit, communicates over Tor, and uses stolen GitHub / publishing access to plant itself into more repositories and npm packages.

JFrog's July 12, 2026 follow-up on the `jscrambler` npm compromise describes the new payload as an evolved IronWorm variant. The successor abandons the first campaign's Linux-only UPX-packed shape for a three-platform CSI container, adds automated npm self-propagation through raw registry `PUT` requests, broadens theft targets to VPN / network secrets and browser-extension wallets, and improves Tor transport management.

This page tracks IronWorm as an operation and malware campaign. It is adjacent to Shai-Hulud / Mini Shai-Hulud tradecraft, but JFrog did not identify it as the same actor. Treat the overlap as shared operational pattern until stronger attribution appears.

## Tags
- ops
- operations
- malware
- supply-chain
- npm
- GitHub
- Rust
- Linux
- eBPF
- rootkit
- Tor
- credential-theft
- infostealer
- worm
- cryptocurrency
- jscrambler
- Windows
- macOS
- VPN credentials

## Why this matters
- IronWorm moves beyond JavaScript install scripts: the reported sample drops a native Linux ELF under `tools/setup` and executes it from npm `preinstall`.
- The implant combines software-supply-chain propagation with endpoint stealth: Rust code, per-call-site string decryption, a modified UPX marker, Tor C2, and eBPF process / network hiding.
- The campaign specifically targets developer and crypto/Web3 environments, including cloud, package-registry, source-control, Kubernetes, AI-provider, and wallet material.
- JFrog observed 57 backdated malicious commits across nine organizations, showing that commit timestamps and bot-like author names are not reliable evidence of benign activity.
- The July 2026 `jscrambler` evolution shows IronWorm-style tradecraft can shift from Linux developer workstations to cross-platform commercial developer-tool packages and can propagate through npm API calls rather than visible `npm publish` process execution.

## Reported chain

### Initial npm finding
- JFrog investigated npm packages published by the `asteroiddao` account, tied to the `asteroid-dao` GitHub organization in the Arweave / WeaveDB ecosystem.
- JFrog used `weavedb-sdk@0.45.3` as its walkthrough sample.
- The malicious tarball copied legitimate package files and added a 976 KB Linux ELF at `tools/setup`.
- `package.json` executed the binary through `"preinstall": "./tools/setup"`, so installation ran the implant before normal dependency resolution.
- JFrog reported the malicious versions were deprecated within about a day and most malicious GitHub commits were removed, though some remained visible after cleanup.

### Repository poisoning and propagation
- Recovered strings showed GitHub API use, branch names, commit messages, package-ecosystem injection templates, and bot identities designed to blend into maintenance activity.
- JFrog found malicious commits with forged historical dates; the malware reportedly copied the timestamp of a repository's most recent legitimate commit so the added payload appeared old.
- Observed payload commits used the author identity `claude <claude@users.noreply.github.com>`, mimicking an AI coding assistant.
- JFrog reported 57 backdated malicious commits across nine organizations and tied the visible chain to a compromised `ocrybit` account with access to `asteroid-dao` and related repositories.
- For package repositories, IronWorm can drop a binary into paths such as `tools/setup` or `.github/scripts/precheck` and alter build/install hooks across ecosystems including npm, PyPI, Cargo, Conan, and vcpkg-style C/C++ projects.
- JFrog also found an unobserved but functional-looking workflow-replacement path: overwrite existing GitHub Actions workflows, serialize `${{ toJSON(secrets) }}` into a harmless-looking artifact, pin legitimate actions by SHA, and attribute the change to familiar automation names such as Dependabot, Renovate, or GitHub Actions.

### Trusted-publishing abuse
- When running in CI, JFrog says the malware can request an OIDC identity token using npm trusted-publishing audience expectations.
- It then exchanges that identity token through npm's `/-/npm/v1/oidc/token/exchange/package/<pkg>` endpoint for a short-lived package-scoped automation token.
- The token can publish a trojanized release to `registry.npmjs.org`, meaning provenance or trusted-publishing evidence would need to be correlated with clean workflow inputs, not treated as a standalone allow signal.

### Credential collection
- JFrog reported collection of 86 environment variables across cloud providers, object storage, databases, source control, package registries, CI/CD, messaging platforms, Vault, Kubernetes, and AI / ML providers.
- AI-related targets included credentials for Anthropic, OpenAI, Gemini, Cohere, Mistral, Groq, Perplexity, xAI, and related services.
- File targets included modern developer-tool paths such as `~/.claude/.credentials.json`, `~/.codex/auth.json`, `~/Cursor/auth.json`, and `~/.gemini/settings.json`, plus `~/.aws/credentials`, `~/.kube/config`, and `~/.docker/config.json`.
- JFrog also described wallet-focused theft: when wallet material is unlocked, a hook can collect the wallet password and recovery phrase and pass it to a local listener controlled by the malware.

### Stealth and command channel
- The Linux sample was a Rust release binary packed with a lightly modified UPX stub; the `UPX!` marker was overwritten to break default `upx -d` detection until restored.
- JFrog reported per-call-site string encryption, increasing reverse-engineering cost because no single key decrypts all embedded strings.
- The eBPF component hides processes from `/proc` listings and hides TCP connections from `/proc/net/tcp` and netlink views used by tools such as `ss`.
- Kernel lockdown weakens the strongest hiding behavior because the memory rewrite helpers fail, making hidden processes and sockets visible again on hardened systems.
- For C2, IronWorm downloads the Tor expert bundle, writes its own `torrc`, starts Tor, beacons to `/api/agent`, and receives commands over plain HTTP inside the Tor tunnel.
- Reported command support includes secret upload, file download from operator-controlled infrastructure, and remote shell execution; JFrog also saw code suggesting a possible `temp.sh` fallback upload path, though it did not confirm use in the wild.

### July 2026 `jscrambler` evolution
- The `jscrambler` payload is delivered from `package/dist/intro.js` as a custom CSI container with magic bytes `1B 43 53 49 01 03 00`, holding gzip-compressed Linux x86-64, Windows x86-64, and macOS arm64 payloads.
- JFrog says the evolved Linux payload scans npm environment variables and config files, validates tokens through `registry.npmjs.org/-/whoami`, enumerates orgs and packages, ranks targets by `api.npmjs.org/downloads/point/last-month`, injects `setup.mjs` / `scripts.preinstall`, and publishes by sending raw HTTPS `PUT` requests to `registry.npmjs.org` with the stolen bearer token.
- Theft scope expands beyond the first report's developer/cloud/wallet focus into VPN and network credentials, including WireGuard configs, OpenVPN configs, IPsec / strongSwan secrets, and PPP CHAP/PAP credentials.
- Browser-extension wallet targeting includes MetaMask extension ID `nkbihfbeogaeaoehlefnkodbefgpgknn` and Trust Wallet extension ID `egjidjbpglichdcondbcbdnbeeppgdph`.
- The Tor workflow now probes for a local SOCKS port, downloads Tor Expert Bundle archives from `archive.torproject.org` if needed, writes a local `.torrc`, waits for `Bootstrapped 100%`, and performs SOCKS5 CONNECT negotiation directly.
- JFrog's IOC set for this wave includes CSI container SHA-256 `a41a523ef9517aab37ed6eea0ec881821bdcb7aefcb5c5f603adc7907f868c86`, Linux payload `fbbcf4d8f98168f78f5c0c47a9ae56d59ec8ac84a7c9ca6b797fedfb8d62d2bd`, Windows payload `b7ca95d1b23c8e67416a25cedf741de0917c2096bbc9d24649eea7853d054903`, and macOS payload `c8fd47d36bdf7c825378593ab82ed8c24d1dc52e26b507812393e24e1d5201fd`.

## Defender heuristics

### Repository and package review
- Audit every repository reachable by a compromised developer or publisher account, including private repositories if audit visibility allows it.
- Search for backdated commits, suspicious branches, unexpected binary additions, and build/install hook changes attributed to `claude`, `dependabot[bot]`, `renovate[bot]`, `github-actions[bot]`, or other automation identities outside their normal behavior.
- Do not trust commit age alone; compare GitHub Actions execution time, push events, and audit logs against commit author/committer timestamps.
- For npm packages, diff new releases against prior known-good tarballs and flag native binaries added to paths such as `tools/setup` or `.github/scripts/precheck`.
- For the `jscrambler`-era variant, also flag large JavaScript-named binary containers such as `dist/intro.js`, added `setup.mjs` files, and `scripts.preinstall` rewrites created by registry-side package infection.
- Review PyPI `setup.py`, Cargo `build.rs`, Conan, vcpkg, and other build-system hooks for new subprocess execution or binary staging.

### CI/CD and identity hunting
- Hunt for workflows that write `${{ toJSON(secrets) }}` or bulk secret material into files/artifacts, especially names resembling formatting, lint, metrics, or report output.
- Treat pinned action SHAs as necessary but not sufficient; a malicious workflow can pin legitimate actions while exfiltrating secrets through allowed artifact channels.
- Correlate npm trusted-publishing exchanges with expected branches, protected environments, release commits, and workflow definitions.
- Correlate npm registry publication events with both CI/workstation process telemetry and registry API logs. The `jscrambler` evolution can publish through direct HTTPS registry `PUT` requests and may not leave an `npm publish` process trail.
- Rotate credentials only after preserving enough evidence to determine which repositories, packages, CI jobs, and cloud resources were reachable.

### Endpoint and Linux controls
- On developer and CI Linux hosts, investigate unexpected Tor downloads, `torrc` creation, `tools/setup` execution, and unknown Rust/ELF processes spawned by package installation.
- For the cross-platform evolution, investigate Tor Expert Bundle downloads, unknown systemd/user-systemd units such as `pgmon.service`, cron additions, unrecognized macOS LaunchAgent / LaunchDaemon plists, and Windows Startup-folder executables or shortcuts.
- Use kernel-lockdown and eBPF restrictions where operationally possible; JFrog's analysis indicates lockdown can break IronWorm's strongest process and socket hiding.
- Prefer endpoint telemetry that does not rely only on `/proc` or netlink views that eBPF rootkits can filter.
- Isolate suspected developer hosts before broad token rotation if active malware may still be collecting refreshed secrets.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)
- [Agent skill marketplace poisoning](../patterns/agent-skill-marketplace-poisoning.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- JFrog Security Research: [https://research.jfrog.com/post/iron-worm-shai-hulud-rustier-cousin/](https://research.jfrog.com/post/iron-worm-shai-hulud-rustier-cousin/)
- JFrog Security Research: [https://research.jfrog.com/post/ironworm-returns-rustier-than-ever/](https://research.jfrog.com/post/ironworm-returns-rustier-than-ever/)
- jscrambler incident page: jscrambler-npm-preinstall-stealer.md
