# Xinference PyPI compromise

## Summary
JFrog Security Research reported an April 2026 compromise of the legitimate `xinference` PyPI package. Malicious versions `2.6.0`, `2.6.1`, and `2.6.2` were published to PyPI and later yanked by maintainers after users observed suspicious behavior.

The payload was not a typosquat: malicious code was injected into the legitimate release line. JFrog attributed the activity to the broader TeamPCP campaign based on actor markers, payload structure, and targeting overlap, while noting that TeamPCP publicly denied involvement and called it a copycat using TeamPCP's name and payload.

## Tags
- ops
- operations
- supply-chain
- PyPI
- Python
- credential-theft
- cloud
- TeamPCP
- AI

## Why this matters
- `xinference` is AI/inference infrastructure; compromise can expose model-serving hosts, cloud credentials, Kubernetes material, and developer secrets.
- The payload ran on import through `xinference/__init__.py`, so any service startup, CLI startup, or downstream dependency path that imported the package could trigger execution.
- The collector targeted not just local files but cloud metadata and secret-management APIs, making affected cloud VMs and CI runners high-priority incident-response targets.

## Affected versions
- `xinference==2.6.0`
- `xinference==2.6.1`
- `xinference==2.6.2`

JFrog says maintainers yanked these versions after users reported suspicious behavior. Treat any environment that installed or imported these versions as compromised.

## Payload chain
1. Malicious code was added to `xinference/__init__.py`.
2. Importing the package launched a detached Python subprocess with stdout/stderr suppressed.
3. The decoded first stage began with the marker `# hacked by teampcp` and unpacked a second embedded base64 collector.
4. The collector wrote host and secret data to stdout; the first stage captured it into a temporary file, compressed it as `love.tar.gz`, and uploaded it with `curl`.
5. Exfiltration targeted `hxxps://whereisitat[.]lucyatemysuperbox[.]space/` with custom header `X-QT-SR: 14`.

## Collection scope
JFrog's decoded payload collected broad developer, server, and CI/cloud material, including:

- host profile data: hostname, working directory, user, kernel, network interfaces/routes, and environment variables
- SSH private keys and host keys
- Git credentials and Git configuration
- AWS shared credentials/config, EC2 IMDS role credentials, and cloud secret inventory metadata
- Kubernetes kubeconfigs and service-account tokens
- Docker registry auth
- package-manager tokens such as `.npmrc`, `.pypirc`, and Cargo credentials
- `.env` files and recursive environment-file searches
- database, Redis, mail, VPN, Helm, Terraform, TLS key, and wallet material
- `/etc/passwd`, `/etc/shadow`, auth logs, Slack/Discord webhooks, and API-key patterns in JSON/env files

The AWS-aware logic attempted IMDSv2 token retrieval and SigV4-signed calls for `secretsmanager.ListSecrets` and `ssm.DescribeParameters`. JFrog noted a bug in one `GetSecretValue` loop, but the intent clearly covered cloud-hosted inference and server environments.

## Attribution and caveats
- JFrog tied the compromise to the TeamPCP campaign family through the actor marker, payload structure, and target profile.
- JFrog also recorded a same-day update that TeamPCP denied responsibility on Twitter and claimed the incident was a copycat using TeamPCP's name and malicious payload.
- Keep this page linked to TeamPCP as reported attribution / possible copycat activity, not as independently proven operator identity.

## Defender heuristics
- Search Python dependency manifests, lockfiles, package caches, images, and CI logs for `xinference` versions `2.6.0`, `2.6.1`, or `2.6.2`.
- Treat any host that imported an affected version as compromised; rotate reachable Git, PyPI, npm, cloud, Kubernetes, Docker, Vault, SSH, database, and application secrets after isolating the host.
- Hunt for network connections or logs involving `whereisitat[.]lucyatemysuperbox[.]space`, uploaded `love.tar.gz` archives, and HTTP header `X-QT-SR: 14`.
- Inspect Python environments for unexpected import-time subprocess launchers in package `__init__.py` files, especially detached interpreters executing decoded payloads.
- In cloud environments, review IMDS access, Secrets Manager `ListSecrets`, SSM `DescribeParameters`, and any unusual credential enumeration from inference hosts or CI runners.

## Related pages
- [TeamPCP](../actors/teampcp.md)
- [LiteLLM compromise](litellm-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Trivy → TeamPCP → CanisterWorm timeline](trivy-lite-llm-compromise-timeline.md)

## Sources
- JFrog Security Research: https://research.jfrog.com/post/xinference-compromise/
