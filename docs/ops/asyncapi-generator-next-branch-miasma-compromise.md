# AsyncAPI generator / specs Miasma compromise

## Summary
StepSecurity reported that on July 14, 2026, a coordinated AsyncAPI supply-chain attack abused push access in **two repositories** and let legitimate GitHub Actions release workflows publish Miasma-family payloads with valid npm OIDC / SLSA provenance. The first attack pushed directly to `asyncapi/generator`'s `next` branch and published three poisoned generator packages at 07:10 UTC. The second attack pushed to `asyncapi/spec-json-schemas`'s `master` branch and published poisoned `@asyncapi/specs` releases through that repository's release workflow.

This is durable supply-chain intel because it shows the Miasma / Mini Shai-Hulud payload family moving from `binding.gyp` install-time hooks into **runtime `require()` execution** inside a high-blast-radius API tooling package. Provenance confirms the workflow and commit that built the package; it does not prove that the commit was reviewed or legitimate.

## Tags
- ops
- operations
- supply-chain
- npm
- GitHub Actions
- trusted publishing
- OIDC
- SLSA provenance
- Miasma
- Mini Shai-Hulud
- credential theft
- developer tooling
- AI tooling
- AsyncAPI

## Why this matters
- The affected packages are API generation, documentation, and AsyncAPI schema tooling that can run inside CI and developer workstations where GitHub, npm, cloud, Kubernetes, SSH, Docker, and AI-assistant credentials may be present.
- The malicious releases had legitimate npm provenance because the attacker used real release workflows from compromised branches. Defenders must validate release-triggering refs, branch protection, and code-review state in addition to checking provenance.
- The payload did **not** rely on `preinstall`, `postinstall`, or `install` lifecycle scripts. It executed when the poisoned module was loaded during normal generator use.
- The injected code used large leading whitespace to push the malicious line out of normal diff view, a useful source-review evasion pivot.
- The second stage identified itself as `Miasma v3` and exposed a professionally built multi-channel RAT / worm framework, not a one-off package stealer.

## Affected packages
StepSecurity lists these malicious package versions and last-known safe versions. As of 11:18 UTC on July 14, 2026, StepSecurity reported all five malicious versions had been unpublished and the latest dist-tags resolved to clean versions, but existing installations and lockfiles from the exposure window remain unsafe.

| Package | Malicious version | Last safe version |
| --- | --- | --- |
| `@asyncapi/generator` | `3.3.1` | `3.3.0` |
| `@asyncapi/generator-helpers` | `1.1.1` | `1.1.0` |
| `@asyncapi/generator-components` | `0.7.1` | `0.7.0` |
| `@asyncapi/specs` | `6.11.2-alpha.1`, `6.11.2` | `6.11.1` |

## Release-pipeline abuse
### `asyncapi/generator` `next` branch
The first malicious push used commit `3eab3ec9304aa26081358330491d3cfeb55cc245`, authored as the placeholder identity `Your Name <you@example.com>` and unsigned. StepSecurity reported the repository workflow `release-with-changesets.yml` ran on `refs/heads/next` as GitHub Actions run `29313420558`, publishing the three generator monorepo packages through npm's GitHub Actions trusted-publisher flow.

### `asyncapi/spec-json-schemas` `master` branch
StepSecurity's later coordinated-attack update added a second AsyncAPI repository. The same placeholder git identity (`Your Name <you@example.com>`, GitHub login `invalid-email-address`) pushed a series of commits to `asyncapi/spec-json-schemas` `master` between 07:51 and 08:28 UTC. That repository's `.github/workflows/if-nodejs-release.yml` release path fired on pushes to `master` whose commit messages started with `fix:` or `feat:`.

Key public pivots from the StepSecurity timeline:

| Commit | Time (UTC) | Message | Reported effect |
| --- | --- | --- | --- |
| `36269ce81837` | 07:56:11 | `fix: correct JSON schema` | Injected the padded obfuscated dropper into `index.js`. |
| `49cb17a9f920` | 07:56:14 | `6.13.5` | Version bump; did not follow the `fix:` / `feat:` publish path. |
| `61a930fca724` | 08:04:02 | `fix: correct JSON schema` | Second payload commit; published `@asyncapi/specs@6.11.2-alpha.1` at 08:06 UTC. |
| `689f5b96693a` | 08:28:02 | `fix: patch parser version` | Blank-line package metadata change; published `@asyncapi/specs@6.11.2` at 08:30 UTC. |

The npm provenance attestation for `@asyncapi/specs@6.11.2` records `.github/workflows/if-nodejs-release.yml`, `refs/heads/master`, and commit `689f5b96693ab1f82a825b6d7c4ee566b0afc4c6`, confirming the package came from the compromised workflow rather than a stolen npm token.

## Injection points
The generator monorepo attack injected the same obfuscator.io-style payload into one file per package:

| Package | Injected source path |
| --- | --- |
| `@asyncapi/generator@3.3.1` | `apps/generator/lib/templates/config/validator.js` |
| `@asyncapi/generator-helpers@1.1.1` | `packages/helpers/src/utils.js` |
| `@asyncapi/generator-components@0.7.1` | `packages/components/src/utils/ErrorHandling.js` |

The malicious line was approximately 7.7 KB and padded with roughly a thousand leading spaces. There were no package lifecycle install scripts; the code fired when the package was `require()`d by normal use of the generator or supporting libraries.

The `@asyncapi/specs` attack used a related but not byte-identical ESM / TypeScript-compiled `index.js` dropper from a different obfuscator build. It used the same drop behavior and final Miasma RAT infrastructure, but a different IPFS source CID: `Qmet4fhsAaWMBUxNDfREHwgiyDeSWy4YSYs9wiKUW5jGyf`.

## Payload chain
1. **Runtime trigger:** `require()` spawns a detached hidden Node process with ignored stdio and `windowsHide: true`, then unreferences it.
2. **Downloader:** the child process creates a NodeJS-looking directory and downloads `sync.js` from IPFS. The generator packages used `https://ipfs.io/ipfs/QmQobZSp1wRPrpSEQ56qnyq7ecZh5Bg5k1fnjt4SUwwHb9`; the specs package used `https://ipfs.io/ipfs/Qmet4fhsAaWMBUxNDfREHwgiyDeSWy4YSYs9wiKUW5jGyf`.
3. **Drop paths:** Linux `~/.local/share/NodeJS/sync.js`; macOS `~/Library/Application Support/NodeJS/sync.js`; Windows `%LOCALAPPDATA%\NodeJS\sync.js`.
4. **Decoded payload:** StepSecurity statically reconstructed an AES-256-GCM / HKDF-SHA256 and ROT-decoded 3.08 MB Node.js application self-identified as `Miasma v3`.
5. **C2 configuration:** the baked config included HTTP C2 and exfiltration on `85.137.53.71` ports `8080`, `8081`, and `8091`, plus Nostr relays, BitTorrent DHT bootstrap nodes, libp2p / GossipSub, and an Ethereum contract dead drop `0x12c37A86a0Ed0beBe5d1d6a43E42f07860eAc710`. StepSecurity later confirmed runtime egress attempts to `85.137.53.71`, `router.bittorrent.com`, and `dht.transmissionbt.com` in an isolated Harden-Runner analysis.

## Reported capabilities
StepSecurity's static analysis identified a modular RAT / worm framework with:

- Six C2 channels: HTTP REST, Nostr, IPFS, BitTorrent DHT, libp2p GossipSub, and Ethereum blockchain dead-drop control.
- Credential harvesting for browser Login Data / Cookies / Local State, SSH keys, `~/.npmrc`, `~/.gitconfig`, GitHub CLI config, AWS credentials, Kubernetes config, Docker credentials, and macOS Keychain.
- Token-specific handling for `GITHUB_TOKEN`, `NPM_TOKEN`, and `PYPI_TOKEN`.
- AI tool poisoning capability through an `ai-tool-poisoner` module, relevant to Claude Code, GitHub Copilot, Cursor, and similar developer assistants.
- LAN discovery and lateral movement modules for subnet scanning, mDNS discovery, and local propagation attempts.
- A metamorphic mutation engine; StepSecurity reported the decrypted header `// mutated v3 profile=low runtime=1`.
- Persistence through systemd, crontab, macOS launchd, and Windows Registry autostart keys.
- Self-destruct / evidence wiping capability and arbitrary shell execution from C2.

## Indicators and hunt pivots
- Lockfiles, caches, SBOMs, or artifact manifests containing the affected package/version pairs above, including `@asyncapi/specs@6.11.2-alpha.1`.
- GitHub provenance attestations for the generator packages referencing `repo:asyncapi/generator:ref:refs/heads/next`, `release-with-changesets.yml`, commit `3eab3ec9304aa26081358330491d3cfeb55cc245`, or Actions run `29313420558`.
- GitHub provenance attestations for `@asyncapi/specs` referencing `repo:asyncapi/spec-json-schemas:ref:refs/heads/master`, `.github/workflows/if-nodejs-release.yml`, commit `689f5b96693ab1f82a825b6d7c4ee566b0afc4c6`, or the attacker commit sequence above.
- Unexpected process trees where `node` spawns detached hidden `node -e` children from AsyncAPI generator execution.
- IPFS fetches for `QmQobZSp1wRPrpSEQ56qnyq7ecZh5Bg5k1fnjt4SUwwHb9` or `Qmet4fhsAaWMBUxNDfREHwgiyDeSWy4YSYs9wiKUW5jGyf`.
- Files at `~/.local/share/NodeJS/sync.js`, `~/Library/Application Support/NodeJS/sync.js`, or `%LOCALAPPDATA%\NodeJS\sync.js` created after AsyncAPI generator use.
- Outbound connections to `85.137.53.71:8080`, `85.137.53.71:8081`, or `85.137.53.71:8091`.
- Nostr relay, BitTorrent DHT, libp2p, or Ethereum mainnet traffic from CI runners or developer workstations that normally only run documentation / code-generation jobs.
- Diff hunks with very long leading-whitespace padding or single-line obfuscated JavaScript added to generator, helper, or component utility files.

## Response guidance
1. Treat hosts and CI runners that installed and executed the malicious versions as compromised. Runtime use matters; installation alone may not have triggered this variant, but cached artifacts can still be dangerous.
2. Preserve package tarballs, npm caches, lockfiles, provenance attestations, GitHub audit logs, Actions logs, runner process telemetry, and EDR evidence before cleanup. Include AsyncAPI transitive dependency paths that may have pulled `@asyncapi/specs` through parsers or generators.
3. Isolate affected runners / workstations before rotating tokens if live malware may still observe the revocation process.
4. Rotate GitHub, npm, PyPI, cloud, Kubernetes, Docker, SSH, browser-session, and AI-assistant credentials reachable from affected environments.
5. Rebuild CI runners and developer environments from known-clean images; remove the NodeJS-looking `sync.js` paths and persistence entries only after evidence capture.
6. Add egress policy for package-build jobs so documentation/code-generation steps cannot reach IPFS gateways, DHT bootstrap nodes, Nostr relays, blockchain RPC, or arbitrary HTTP C2.
7. Harden npm trusted-publishing by binding release workflows to protected, reviewed refs; require branch protection, signed commits or vigilant mode, CODEOWNERS review, and environment approvals for publish jobs.
8. Audit release workflows that trigger from `next`, prerelease, snapshot, maintenance, or `master` branches based only on commit-message prefixes. Provenance should be considered necessary but not sufficient.

## Attribution notes
The payload self-identifies as Miasma and overlaps Mini Shai-Hulud / Miasma supply-chain tradecraft, but StepSecurity framed the public evidence as compromised repository push access and legitimate release-pipeline abuse rather than a named actor claim. Keep this as **Miasma-family / Mini Shai-Hulud-style activity** unless later public reporting ties it to TeamPCP or another operator with higher confidence.

## Related pages
- [Leo Platform npm Miasma-style compromise](leo-platform-npm-miasma-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/compromised-next-branch-pushes-malicious-asyncapi-generator-generator-helpers-and-generator-components-to-npm
