# LiteLLM compromise

## Tags
- ops
- operations
- supply-chain
- CI/CD
- PyPI
- malicious releases
- credential theft
- tooling

## Summary
Public reporting and community discussion indicate the LiteLLM compromise was part of a supply-chain abuse operation involving **stolen CI tokens**, **malicious PyPI releases**, and **credential exfiltration from runtime environments**. This page focuses on the operational chain rather than a single product failure.

## Timeline
- **Initial access:** CI/release credentials were obtained.
- **Release abuse:** those credentials were used to publish malicious packages.
- **Propagation:** the malicious packages were then used to exfiltrate credentials from downstream environments.

## Evidence
- Attackers obtained CI/release credentials
- Those credentials were used to publish malicious packages
- The malicious packages were then used to exfiltrate credentials from runtime environments
- The incident fits a broader pattern of package-manager compromise and release automation abuse

## Tooling
- CI/CD token abuse
- PyPI release publishing
- package install-time execution
- runtime credential harvesting
- secret exfiltration from build or runtime environments

## Why it matters
The LiteLLM compromise shows how a single release-system compromise can become a **credential theft and downstream distribution event**. Even when the initial access is limited to a build system, the blast radius can extend to every environment that trusts the published package.

## Defender takeaways
- Treat CI secrets as high-value and rotate after compromise
- Pin package versions where practical
- Verify provenance for newly published releases
- Hunt for unexpected publishing activity and unusual package metadata changes

## References
- Public community discussion and reporting on the LiteLLM supply-chain incident
