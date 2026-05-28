# Operation DangerousPassword axios npm compromise

## Summary
ESET's May 28, 2026 APT activity report says Lazarus continued **Operation DangerousPassword** during Q4 2025–Q1 2026 and that the activity led to compromise of the widely used `axios` JavaScript library.

According to ESET, attackers used compromised lead-maintainer credentials to publish malicious `axios` versions to npm. The trojanized releases injected malicious code into affected systems before detection and removal. Because `axios` has more than 100 million weekly npm downloads and is embedded across web, mobile, and server-side JavaScript applications, the incident represents a high-blast-radius maintainer-account compromise even with limited public technical detail.

## Tags
- ops
- operations
- Lazarus
- North Korea
- Operation DangerousPassword
- npm
- axios
- JavaScript
- supply-chain
- maintainer compromise
- compromised credentials
- package registry
- developer-targeting
- CI/CD
- credential-theft

## Why this matters
- A single maintainer credential compromise against a core JavaScript dependency can expose far more downstream organizations than direct intrusion against one target.
- The public reporting ties the compromise to Lazarus activity that also targets developers and cryptocurrency organizations, so defenders should treat package-registry credentials, developer workstations, and CI/CD secrets as likely objectives.
- Even after malicious releases are removed, lockfiles, private mirrors, build caches, container layers, vendored dependencies, and generated artifacts can preserve exposure.
- The incident reinforces that high-download dependencies need publisher-account hardening, provenance checks, and rapid dependency-inventory response paths, not only source-code review.

## Reported chain
ESET's public summary gives the following high-level chain:

1. Lazarus activity under Operation DangerousPassword compromised credentials belonging to a lead maintainer of `axios`.
2. The attackers used the maintainer access to publish malicious `axios` versions to npm.
3. The malicious versions injected trojanized code into systems that installed or built with the affected releases.
4. The packages were later detected and removed.

ESET does not publish detailed package-version, payload, or indicator tables in the public blog summary. Treat the report as strategic public attribution and impact framing until additional maintainer, registry, or vendor postmortems supply precise version and IOC data.

## Defender heuristics
- Inventory all `axios` versions installed from npm across source repositories, lockfiles, build systems, private registries, package caches, container images, and deployed artifacts around the Q4 2025–Q1 2026 window.
- Prefer registry provenance, signed publish metadata, package-integrity hashes, and reproducible-build comparisons where available; do not rely only on current npm package state after removal.
- Review npm, GitHub, SSO, cloud, and CI/CD audit logs for unusual maintainer-token use, package-publish events, release automation changes, unexpected two-factor resets, and new automation tokens.
- Rebuild affected applications from known-good dependency sets after cache eviction; stale lockfiles or private mirrors can continue serving removed malicious versions.
- Rotate package-registry, GitHub, CI/CD, cloud, API, and signing credentials that were present on systems that built with suspect releases.
- Apply least-privilege and phishing-resistant MFA to maintainer and release accounts, and separate human maintainer credentials from automated package-publish tokens.

## Attribution notes
ESET reports the compromise in the context of Lazarus and Operation DangerousPassword. The public summary does not provide enough detail to independently connect the `axios` package event to a specific Lazarus subgroup or toolchain, so this page tracks the incident as ESET-attributed North Korea-aligned supply-chain activity.

## Related pages
- [RemotePE](../tools/remotepe.md)
- [3CX desktop app compromise](3cx-desktop-app-compromise.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- ESET: https://www.welivesecurity.com/en/eset-research/eset-apt-activity-report-q4-2025-q1-2026/
- ESET PDF: https://web-assets.esetstatic.com/wls/en/papers/threat-reports/eset-apt-activity-report-q4-2025-q1-2026.pdf
