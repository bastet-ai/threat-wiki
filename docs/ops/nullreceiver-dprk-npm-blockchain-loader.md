# NullReceiver DPRK-linked npm blockchain-loader wave

## Summary
On August 10, 2026, Sonatype Research Labs reported **six npm packages carrying the same JavaScript loader**. Three were legitimate packages with malicious versions appended to existing files; three were newly published packages that shipped with the loader from the outset. Sonatype tracks the groups as `sonatype-2026-005899` and `sonatype-2026-005901`.

The loader retrieves command-and-control addresses from an outbound Ethereum transaction, then downloads and executes additional JavaScript. Sonatype says the wallet and technique match recent **NullReceiver** activity that OpenSourceMalware attributed to the DPRK-linked **Contagious Interview** campaign. Treat that attribution as source-linked campaign evidence, not proof that every affected publisher or package maintainer was knowingly involved.

## Tags
- ops
- operations
- supply-chain
- npm
- JavaScript malware
- developer targeting
- package hijacking
- malicious packages
- Ethereum
- blockchain C2
- blockchain dead drop
- NullReceiver
- Contagious Interview
- Famous Chollima
- Lazarus
- DPRK
- North Korea
- credential theft
- detached execution
- Sonatype
- sonatype-2026-005899
- sonatype-2026-005901

## Affected packages and versions

### Hijacked legitimate packages — `sonatype-2026-005899`
- `@kolbo/mcp@1.57.1`
- `agentgui@1.0.1127`
- `godot-kit@1.0.1786316795`

### Malware-bearing new packages — `sonatype-2026-005901`
- `envpack-conf@1.0.1`
- `postcss-initial-provider@3.0.4`
- `tailwindcss-motion-advanced@1.0.1`

The distinction matters during response. The first group may enter environments through an established dependency or recognized publisher, while the second depends on new-package adoption, dependency confusion, typosquatting, or other discovery paths. Sonatype found substantial legitimate functionality in both groups, so a superficial package review can miss the appended loader.

## Loader and dead-drop behavior
1. The JavaScript loader queries multiple Ethereum JSON-RPC providers for an outbound transaction from an attacker-controlled wallet.
2. It reads bytes encoded in the transaction recipient address and decodes them into primary and secondary IPv4 C2 endpoints.
3. It races RPC requests, supports batched calls, and can fall back to the Blockscout API, making resolution resilient to loss of one provider.
4. It requests follow-on content from `/0x/cls` and `/0x/ls` on the resolved infrastructure.
5. A standard `GET` response can carry the payload. If that path fails, the loader sends a `HEAD` request and reads Base64 content from the `X-Payload-B64` response header.
6. It Base64- and XOR-decodes the retrieved JavaScript. The `/0x/cls` stage can run through `eval()` in the current Node.js process; downloaded stages can also execute as detached Node.js child processes.

Sonatype describes the implementation as broader than the previously reported NullReceiver behavior because of the redundant RPC, batch, Blockscout, dual-endpoint, and response-header fallback paths.

## Campaign relationship
Sonatype linked the six-package set to earlier `bianira-ui` and `fluid-type-ui` reporting through the shared Ethereum wallet and the NullReceiver resolution method. It also noted that appending malicious code to legitimate package files resembles the DPRK-linked PolinRider campaign.

These are useful lineage pivots, but defenders should preserve the evidence boundaries:

- wallet and loader reuse strongly support shared infrastructure or tooling;
- similar package-hijack placement supports a common tradecraft assessment;
- neither fact alone proves that every wave used the same operator, recruiter persona, initial-access method, or follow-on payload.

## Defender response
- Search manifests, lockfiles, SBOMs, package-manager caches, internal mirrors, CI artifacts, deployment images, and developer workstations for the six exact package-version pairs.
- If an affected version executed, do not stop at package removal. Preserve the package tarball, install/runtime process tree, Node.js command line, DNS and proxy records, Ethereum/Blockscout requests, and HTTP traffic to `/0x/cls` or `/0x/ls`.
- Hunt for `HEAD` requests followed by an `X-Payload-B64` response, Base64/XOR decode loops, `eval()` of network-derived JavaScript, and detached Node.js children whose parent is a package, build, test, IDE, or agent process.
- Assume secrets available to the affected Node.js process may be exposed. Rotate reachable source-control, npm, cloud, CI/CD, SSH, Kubernetes, wallet, browser-session, and developer-tool credentials from a known-clean system.
- Review package-publisher and source-control audit logs for account takeover, unexpected token use, unauthorized release creation, provenance changes, and synchronized modifications across other packages owned by the same identities.
- Block or tightly govern public blockchain RPC and explorer API access from build runners where it is not required. Alert on package lifecycle or application code using Ethereum RPC to resolve raw IP addresses.
- Rebuild affected artifacts from verified clean source and dependency snapshots; package removal on one workstation does not remediate copied build outputs or stolen credentials.

## Related pages
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)
- [StegaBin Pastebin steganography npm campaign](stegabin-pastebin-steganography-npm-campaign.md)
- [Contagious Interview SVG steganography campaign](contagious-interview-svg-steganography-ottercookie.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Direct-to-IP malware communications](../patterns/direct-to-ip-malware-communications.md)

## Sources
- Sonatype Research Labs: [https://www.sonatype.com/blog/six-npm-packages-use-ethereum-transactions-to-retrieve-malicious-payloads](https://www.sonatype.com/blog/six-npm-packages-use-ethereum-transactions-to-retrieve-malicious-payloads)
