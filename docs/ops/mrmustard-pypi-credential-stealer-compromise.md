# MrMustard PyPI credential-stealer compromise

## Summary
On July 24, 2026, StepSecurity reported that `mrmustard==0.7.4`, a release of XanaduAI's legitimate quantum-photonics Python package, contained an import-time credential stealer. The malicious artifact existed on PyPI without a matching GitHub tag or release and injected 258 lines into `mrmustard/__init__.py`; the default-branch source did not contain the payload.

StepSecurity and the public project issue attribute the publication path to a compromised maintainer GitHub account. Two July 23 commits on subsequently deleted branches first probed a self-hosted runner and then exposed the repository's PyPI and Codecov secrets to a `webhook.site` endpoint. The stolen PyPI token reportedly enabled direct publication of the source-artifact-only `0.7.4` release.

The PyPI project API returned `404` when threat.wiki checked it on July 24, consistent with package removal. The upstream GitHub issue remained open; no maintainer postmortem was public at that check. Treat the account-takeover sequence as incident-reporter attribution pending maintainer confirmation.

## Tags
- ops
- operations
- supply-chain
- PyPI
- Python
- maintainer compromise
- GitHub Actions
- CI/CD
- self-hosted runner
- token theft
- credential theft
- import-time execution
- persistence
- SSH keys
- AWS
- Kubernetes
- HPC
- research sector
- quantum computing
- StepSecurity

## Why this matters
- The malicious code was inserted only into the published artifact. Reviewing the default GitHub branch or relying on source-repository scanners would not have exposed the package drift.
- A single `import mrmustard` was sufficient to collect credentials and install three independent persistence paths.
- The collection profile was aligned to developer and research systems: SSH, AWS, Kubernetes, GPU, Conda, and HPC scheduler material can enable movement from a workstation or cluster login node into source, cloud, and compute infrastructure.
- Deleting the package is insufficient after import because the payload survives through cron, Python startup, and shell startup hooks.

## Affected release and status
- Malicious: `mrmustard==0.7.4`
- Reported safe by StepSecurity: `0.7.3` and earlier, and the `1.0.0a*` prerelease line
- No corresponding `v0.7.4` GitHub release or tag
- Latest public GitHub releases observed: `v0.7.3` from March 2024 and `v1.0.0a1` from July 2025
- PyPI JSON endpoint status at the July 24 check: `404 Not Found`

The absence of a current PyPI page prevents threat.wiki from independently validating the removed artifact's hashes. Search internal package caches, artifact repositories, software inventories, and lockfiles rather than relying only on current registry metadata.

## Reported compromise sequence
1. Commit `2ebfe28ab549492e74b98ce323fa881725cbfcf2` deleted seven normal workflow files on a throwaway branch and added a self-hosted-runner job that executed `whoami`.
2. Commit `80aba721b2a902bc6efb04e3c77c3bdd28d1e716` added a GitHub Actions workflow that placed `PIPY_TOKEN` and `CODECOV_TOKEN` into a base64-encoded JSON object and sent it to `webhook.site`.
3. The branches were deleted, but the commits remain publicly retrievable.
4. The actor reportedly used the exposed PyPI token to publish `mrmustard==0.7.4` directly, bypassing the normal tagged-release workflow.
5. The published archive matched `0.7.3` except for an added 258-line block at the top of `mrmustard/__init__.py`.

The malicious commits are unsigned. Their author metadata identifies the affected maintainer identity, but Git commit author fields alone are not proof that the named person performed the actions.

## Import-time payload
The injected `_check_tf_compatibility()` function ran from top-level package initialization, launched a background daemon thread, and deleted its own module attribute after execution. It stopped when common CI environment variables, container marker files, or Docker, Kubernetes, or LXC strings in `/proc/1/cgroup` were present.

StepSecurity reported collection of:

- files under `~/.ssh` containing private-key material
- `~/.aws/credentials` and `~/.aws/config`
- `~/.kube/config`
- environment variables with AWS, Kubernetes, SLURM, PBS, SGE, CUDA, NVIDIA, and Conda-related prefixes
- hostname, username, operating system, Python version, current directory, and `id` output
- public IP from `ifconfig.me`
- installed Python packages from `pip freeze`
- GPU detail from `nvidia-smi` and SLURM queue detail from `squeue`

The payload XOR-obfuscated its collection URL with key `tf_compat_v2`, encoded collected JSON, and sent it to `https://metrics.femboy.energy/v1/collect`. A per-host marker and timestamp under `~/.cache/.tf_cache` limited collection attempts to roughly once per hour.

## Persistence
The import compiled a second-stage copy to `~/.cache/.tf_cache/hw_probe.pyc` and reportedly installed:

- a cron entry running the file every 15 minutes
- `mmcompat.pth` in a writable Python `site-packages` directory, causing execution on Python startup
- a background launch line in `~/.bashrc` or `~/.zshrc`, labeled `# tensorflow hardware compatibility check`

StepSecurity reproduced all three paths during controlled detonation. Removing the Python package does not remove these artifacts.

## Public indicators
### Package and files
- `mrmustard==0.7.4`
- `mrmustard/__init__.py`
- `_check_tf_compatibility`
- `~/.cache/.tf_cache/`
- `~/.cache/.tf_cache/hw_probe.pyc`
- `mmcompat.pth`
- `# tensorflow hardware compatibility check`

### Network
- `metrics.femboy[.]energy`
- `femboy[.]energy`
- `hxxps://metrics.femboy[.]energy/v1/collect`
- `hxxps://webhook[.]site/710babde-6ace-47fe-83f4-9688e6548df9`
- `ifconfig[.]me`

### Repository commits
- `2ebfe28ab549492e74b98ce323fa881725cbfcf2`
- `80aba721b2a902bc6efb04e3c77c3bdd28d1e716`

Treat network indicators as historical and potentially mutable. Do not probe them from production systems.

## Detection and response guidance
### Scope exposure
- Search requirements files, `pyproject.toml`, lockfiles, SBOMs, build logs, package caches, internal mirrors, virtual environments, containers, and research-cluster software modules for `mrmustard==0.7.4`.
- Distinguish installation from execution where logs permit, but do not assume “installed only” is safe if imports, tests, notebooks, shells, Python startup, or package validation may have occurred.
- Hunt DNS, proxy, and endpoint telemetry for the reported C2, webhook UUID, and `ifconfig.me` access correlated with Python or MrMustard activity.
- Inspect user crontabs, shell startup files, all writable system and virtual-environment `site-packages` directories, and `~/.cache/.tf_cache` for persistence.
- On shared HPC systems, scope login nodes, notebook services, job environments, shared homes, scheduler-submitted jobs, and credentials exposed through scheduler environment variables.

### Contain and recover
- Isolate affected hosts while preserving the malicious artifact, Python environment, process and network evidence, shell histories, crontabs, startup files, package caches, and GitHub Actions audit data.
- From known-clean systems, revoke and rotate reachable SSH keys, AWS credentials and sessions, Kubernetes client certificates and tokens, repository and package-registry tokens, Codecov tokens, CI secrets, and other environment-resident credentials.
- Remove all three persistence paths and the cache directory only after evidence collection. Rebuild when execution is confirmed or complete payload and credential scope cannot be established.
- Review AWS CloudTrail, Kubernetes audit logs, SSH authentication, source-control, registry, Codecov, CI/CD, and scheduler logs for follow-on use. Rotation without reviewing use can miss established access.
- For maintainers, revoke the affected account's sessions and tokens, rotate repository secrets, review organization and repository audit logs, validate self-hosted runners, and compare every published artifact with a trusted source commit and build record.

## Durable defender lessons
- Require PyPI trusted publishing with narrowly scoped GitHub OIDC claims instead of long-lived upload tokens where the release architecture permits it.
- Restrict who can create or modify workflows, require review for `.github/workflows/**`, and alert on deleted workflow branches, self-hosted runner label changes, and secrets sent to first-seen destinations.
- Compare registry artifacts against tagged source and reproducible builds. A clean repository does not establish that a registry tarball or wheel is clean.
- Treat `.pth` files, package `__init__.py` changes, shell startup edits, and user crontab creation by dependency code as high-signal behavior on developer and research endpoints.
- Do not let CI/container evasion create false reassurance: package detonation should include realistic developer-host conditions with controlled network egress.

## Attribution and scope caveats
StepSecurity credits Aikido researcher Ilyas Makari for the initial report. No named threat actor, victim count, confirmed downstream credential use, or relationship to Shai-Hulud, Mini Shai-Hulud, Miasma, or TeamPCP was reported. Keep this incident separate unless later public evidence establishes shared infrastructure, code, access, or operator behavior.

## Related pages
- [Xinference PyPI compromise](xinference-pypi-compromise.md)
- [SleeperGem RubyGems maintainer-account compromise](sleepergem-rubygems-maintainer-account-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- StepSecurity: [https://www.stepsecurity.io/blog/compromised-pypi-mrmustard-0-7-4-credential-stealer](https://www.stepsecurity.io/blog/compromised-pypi-mrmustard-0-7-4-credential-stealer)
- Public upstream issue: [https://github.com/XanaduAI/MrMustard/issues/656](https://github.com/XanaduAI/MrMustard/issues/656)
- Public credential-exfiltration commit: [https://github.com/XanaduAI/MrMustard/commit/80aba721b2a902bc6efb04e3c77c3bdd28d1e716](https://github.com/XanaduAI/MrMustard/commit/80aba721b2a902bc6efb04e3c77c3bdd28d1e716)
- Public self-hosted-runner reconnaissance commit: [https://github.com/XanaduAI/MrMustard/commit/2ebfe28ab549492e74b98ce323fa881725cbfcf2](https://github.com/XanaduAI/MrMustard/commit/2ebfe28ab549492e74b98ce323fa881725cbfcf2)
- Upstream releases: [https://github.com/XanaduAI/MrMustard/releases](https://github.com/XanaduAI/MrMustard/releases)
