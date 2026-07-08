# Git hash chain malleability

## Summary

July 2026 public research by Jacob Ginesin describes **Git hash chain malleability**: for signed Git commits, an attacker who does not have the signing key and does not break SHA-2 can construct a second commit object with the same tree, metadata, and a signature that still verifies, but with a different commit hash. The changed hash cascades to descendant commits because each child commit records its parent hash.

This is not a way to change source code while preserving a victim's signature. The malleated commit has the same tree content, so a pinned commit hash still protects dependency consumers: the malleated object has a different hash and will not satisfy the original pin. The durable defender issue is provenance and trust signaling. If a forge, automation system, or human reviewer treats a “Verified” badge as equivalent to “this exact commit hash is the original signed object,” attackers may be able to create confusing alternate histories that still display verified status.

## Tags

- patterns
- Git
- commit signing
- source repository poisoning
- supply chain
- provenance
- GitHub
- signed commits
- hash chain malleability
- signature malleability
- ECDSA
- OpenPGP
- S/MIME

## Technique

The paper identifies three practical malleation routes across signature formats that Git forges commonly verify:

1. **ECDSA algebraic inversion** — transform the signature value `s` to `n - s`; both forms remain valid for the same signed data.
2. **OpenPGP subpacket insertion** — add an unhashed OpenPGP subpacket for RSA / EdDSA signatures without changing the signed payload.
3. **S/MIME CMS re-encoding** — use non-canonical DER length re-encoding inside the CMS envelope.

Because a Git commit's object ID covers the raw bytes of the commit object, including the signature header, changing signature encoding bytes changes the commit hash even when the signed content and file tree are unchanged. Rewriting one signed commit also forces new hashes for descendants that point to it as a parent. A descendant's own signature does not automatically remain valid after its parent pointer changes, so the impact is strongest where a signed commit or a partially signed history is accepted based on forge verification signals rather than immutable hash provenance.

## Why defenders should care

This belongs in source-repository and CI/CD threat modeling even though it is not a code-substitution primitive:

- **Verified badge ambiguity:** a forge can truthfully show that the altered signature validates while the displayed hash is not the original signed hash a maintainer published.
- **Forensic confusion:** incident responders comparing histories across mirrors, forks, bundles, or caches may see different hashes for equivalent source trees and need to distinguish malleation from source-code tampering.
- **Allow-list drift:** controls that approve commits by “verified signer + repository + branch” rather than exact immutable hashes can be weaker than teams assume.
- **Release provenance gaps:** artifact attestations, SBOMs, release notes, and deployment records should bind to exact commit object IDs and artifact digests, not only to signer identity or a forge verification badge.
- **Supply-chain social proof:** malicious forks or mirrors can potentially display verified-looking commits for the same content under different hashes, making hash-based review conversations harder.

## Defensive guidance

- Pin dependencies, GitHub Actions, submodules, vendored source, and release inputs to exact commit hashes or cryptographic release artifacts; do not accept a “Verified” badge as a replacement for a known-good object ID.
- Record release provenance with commit hash, tree hash where useful, artifact digest, signer identity, build workflow identity, and timestamped attestation. Treat signer identity alone as insufficient.
- Alert on unexpected history rewriting, changed commit IDs for an otherwise identical tree, and branch/tag movement in release or CI repositories.
- Prefer protected tags and signed, immutable releases for distribution points; monitor tag retargeting separately from commit signature status.
- During incident response, compare both commit IDs and tree IDs. A matching tree with a different signed commit hash may indicate signature-object malleation rather than file-content tampering.
- Ask forge and tooling vendors how they canonicalize signature encodings, deduplicate malleated commit objects, and display verification status when multiple valid encodings exist for the same signed payload.

## Related pages

- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [GitHub Actions OIDC subject-claim collisions](github-actions-oidc-subject-claim-collisions.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Crypto supply-chain path to transaction authority](crypto-supply-chain-transaction-authority.md)

## Sources

- Jacob Ginesin, “Git Hash Chain Malleability”: https://arxiv.org/abs/2607.02820
- The Hacker News summary: https://thehackernews.com/2026/07/github-verified-commits-can-be.html
