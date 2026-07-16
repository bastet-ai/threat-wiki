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

## 2026-05-22 Boost Labs update
Boost Security Labs' detailed LiteLLM writeup adds three durable defender pivots to the existing TeamPCP record: the precise `1.82.7`/`1.82.8` PyPI payload split, `.pth`-based Python startup execution with no import requirement, and a caveated initial-access analysis that narrows but does not prove a Trivy bridge.

## Timeline
- **March 19, 2026:** TeamPCP's earlier Trivy compromise created a plausible credential-theft bridge into later victims, but Boost treats the exact LiteLLM initial-access path as a working hypothesis rather than proven BerriAI internal forensics.
- **March 24, 2026:** public warning and community investigation started after TeamPCP Telegram chatter about another large supply-chain attack and a `+35k stars` GitHub repository.
- **Release abuse:** attackers published malicious `litellm` PyPI versions `1.82.7` and `1.82.8` outside the normal GitHub/CircleCI release path.
- **Payload escalation:** version `1.82.7` placed payload code in `litellm/proxy/proxy_server.py`, requiring a proxy-module import. Version `1.82.8` moved to `litellm_init.pth`, so Python's automatic `site` initialization could execute the payload on every Python startup after installation, even with no LiteLLM import.
- **GitHub account abuse:** Boost reported that a compromised GitHub account closed the public disclosure, defaced 15 organization repositories, wiped 182 personal repositories, and exposed 70 private BerriAI repositories.
- **Propagation:** the malicious packages exfiltrated credentials from downstream environments to `models.litellm.cloud`, a typosquat chosen to blend with normal LiteLLM network activity.

## Evidence
- Attackers obtained CI/release or maintainer credentials and used them to publish PyPI artifacts that did not correspond to normal GitHub release tags.
- Boost's CI/CD forensics ruled out several easy Trivy paths for the inspected BerriAI CircleCI job: sampled logs installed clean `trivy` `0.69.3` from APT, BerriAI did not use `aquasecurity/trivy-action`, and the Homebrew Trivy vector was not valid because Homebrew built clean source.
- Boost's remaining Trivy hypothesis is narrower: if Trivy was the bridge, it was more likely a poisoned GitHub Release binary, Docker image, or force-pushed action tag used somewhere outside the sampled clean paths.
- The malicious PyPI packages used two delivery styles: `proxy_server.py` import-time execution in `1.82.7`, then `.pth` startup execution in `1.82.8`.
- The payload exfiltrated to `https://models.litellm.cloud/`.
- Boost enumerated more than 230 CircleCI secret names that would have been in scope if the payload executed where those variables were loaded, spanning PyPI publishing, GitHub, cloud providers, Vault/Infisical, databases, DockerHub, Redis, Slack, Sentry/PagerDuty/Datadog, and LLM-provider API keys.
- The incident fits TeamPCP's broader pattern of turning one supply-chain foothold into package publication, credential theft, public taunting, repository exposure/destruction, and second-order victim hunting.

## Tooling
- CI/CD token abuse
- PyPI release publishing
- package install-time and interpreter-startup execution
- Python `.pth` startup execution via automatic `site` module processing
- double base64 payload wrapping for simple static-evasion
- runtime credential harvesting from build, developer, or service environments
- typosquat exfiltration endpoint (`models.litellm.cloud`)

## Why it matters
The LiteLLM compromise shows how a single release-system compromise can become a **credential theft and downstream distribution event**. Even when the initial access is limited to a build system, the blast radius can extend to every environment that trusts the published package.

## Defender takeaways
- Treat CI secrets as high-value and rotate after compromise, but only after affected runners and developer endpoints are contained.
- Pin package versions where practical and watch for malicious patch bumps that appear without corresponding GitHub tags or release automation records.
- Hunt Python environments for unexpected `.pth` files, especially package-branded startup files that execute encoded code.
- Review PyPI upload logs, GitHub account actions, disclosure-issue closures, repository visibility changes, and destructive repository operations as one incident chain.
- Verify provenance for newly published releases, but do not treat provenance alone as sufficient when upstream CI or trusted-publishing workflows may be compromised.
- Search network telemetry for `models.litellm.cloud` and adjacent LiteLLM-looking domains used outside expected application paths.

## References
- [Boost Security Labs](https://labs.boostsecurity.io/articles/teampcp-litellm-supply-chain-compromise/)
- Public community discussion and reporting on the LiteLLM supply-chain incident
