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
Public reporting and community discussion indicate the LiteLLM compromise was part of a supply-chain abuse operation involving **stolen CI tokens**, **malicious PyPI releases**, and **credential exfiltration from runtime environments**. Boost Security Labs attributes the March 2026 incident to **TeamPCP** and frames it as a follow-on opportunity from the earlier Trivy compromise, while caveating the exact initial-access path. This page focuses on the operational chain rather than a single product failure.

## Timeline
- **Initial access:** CI/release credentials were obtained. Boost reported that investigators considered poisoned Trivy distribution channels as a likely path, but did not treat it as proven without BerriAI internal forensics.
- **Release abuse:** attackers published malicious `litellm` PyPI versions `1.82.7` and `1.82.8` outside the normal GitHub/CircleCI release path.
- **Payload escalation:** version `1.82.7` placed payload code in `litellm/proxy/proxy_server.py`, while `1.82.8` used a `.pth` file (`litellm_init.pth`) so the payload could execute on Python startup without importing LiteLLM.
- **GitHub account abuse:** Boost reported that a compromised GitHub account closed the public disclosure, defaced 15 organization repositories, wiped 182 personal repositories, and exposed 70 private BerriAI repositories.
- **Propagation:** the malicious packages exfiltrated credentials from downstream environments.

## Evidence
- Attackers obtained CI/release credentials
- Those credentials were used to publish malicious packages
- The malicious packages were then used to exfiltrate credentials from runtime environments
- The incident fits a broader pattern of package-manager compromise and release automation abuse

## Tooling
- CI/CD token abuse
- PyPI release publishing
- package install-time execution
- Python `.pth` startup execution
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
- Boost Security Labs: https://labs.boostsecurity.io/articles/teampcp-litellm-supply-chain-compromise/
- Public community discussion and reporting on the LiteLLM supply-chain incident
