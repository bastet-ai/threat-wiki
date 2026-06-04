# binding.gyp npm CI/CD worm

## Summary
StepSecurity reported an active npm supply-chain worm on June 4, 2026 that uses a small `binding.gyp` file to trigger install-time execution through npm's native-addon build path instead of obvious `package.json` lifecycle scripts.

The payload harvests developer and CI/CD credentials, injects GitHub Actions workflow steps for persistence, and uses stolen npm or RubyGems publishing access to republish poisoned package versions. StepSecurity described the incident as developing and said the affected-package list was still expanding.

## Tags
- ops
- operations
- malware
- supply-chain
- npm
- RubyGems
- GitHub Actions
- CI/CD
- credential-theft
- worm
- node-gyp
- binding.gyp
- secrets

## Why this matters
- `binding.gyp` gives the actor an install-time execution path that can be missed by controls focused on `preinstall`, `postinstall`, and other `package.json` lifecycle scripts.
- The worm targets the same high-value identity surfaces defenders now expect from Shai-Hulud-style campaigns: package-registry tokens, GitHub tokens, cloud credentials, Vault, Kubernetes, password managers, and GitHub Actions runner memory.
- It modifies GitHub Actions workflows, so remediation requires repository and workflow review, not just package removal and token rotation.
- It reportedly propagates through both npm and RubyGems publishing access, making it a cross-registry software-supply-chain incident rather than a single package-family compromise.

## Reported chain

### Install-time trigger through `binding.gyp`
- StepSecurity says the malicious packages add a roughly 100-byte `binding.gyp` file.
- When npm sees `binding.gyp`, npm can invoke the native-addon build path during install even when the package has no suspicious `package.json` lifecycle hook.
- The small `binding.gyp` leads to malicious JavaScript that uses a ROT-N Caesar cipher to decode an inner script.
- The inner script decrypts two AES-128-GCM payloads with hardcoded keys.

### Runtime staging
- The first decrypted payload downloads Bun JavaScript runtime v1.3.13 from GitHub into a temporary directory.
- StepSecurity says the second decrypted payload is roughly 720 KB and runs through the downloaded Bun runtime.
- Using Bun gives the actor a standalone execution environment while keeping the initial package modification small.

### Credential collection
StepSecurity reports the worm searches for:

- npm tokens.
- GitHub tokens and personal access tokens.
- AWS access keys, including IMDSv2 and ECS task-role sources.
- GCP service-account credentials.
- Azure client secrets and Key Vault contents.
- HashiCorp Vault tokens from multiple local paths and the local Vault API.
- Kubernetes service-account tokens.
- RubyGems API keys.
- Passwords from 1Password CLI, `gopass`, and `pass`.
- Masked secrets extracted from GitHub Actions runner process memory.

### GitHub Actions workflow persistence
- With stolen GitHub tokens, the worm modifies workflow files in repositories the victim can push to.
- StepSecurity says the injected workflow content adds a setup step plus a payload-execution step so future CI jobs rerun the worm.
- This turns repository access into repeated credential-harvesting opportunities even after a single infected package install.

### Package-registry propagation
- With stolen npm or RubyGems tokens, the worm queries registry accounts for packages the victim maintains.
- It downloads maintained packages, injects the malicious payload, and publishes new poisoned versions.
- StepSecurity listed compromised versions published between June 3 and June 4, 2026 and noted that its list was still being updated.
- Early named package families in the StepSecurity table included `@vapi-ai/server-sdk`, `ai-sdk-ollama`, many `autotel-*` packages, `awaitly-*` packages, `executable-stories-*` packages, `node-env-resolver*`, and `wrangler-deploy`.

### Exfiltration
- StepSecurity says stolen credentials are encrypted with a hardcoded RSA public key.
- The worm exfiltrates the encrypted material into attacker-controlled GitHub repositories as dangling commits not reachable from normal branches, echoing dead-drop patterns seen in other recent package-registry worms.

## Defender heuristics

### Package review
- Treat unexpected `binding.gyp` additions as install-time code-execution signals, even when `package.json` scripts are absent or unchanged.
- Diff newly published package tarballs against prior known-good versions and flag tiny build-configuration files that launch larger staged scripts.
- Expand package-security checks beyond lifecycle hooks to include `node-gyp`, native-addon build files, generated project files, and build-tool configuration.
- Review exposure to the package names and versions StepSecurity lists; the list was still changing at publication time, so use the source as the live reference.

### CI/CD and repository response
- Search GitHub Actions workflows for unexpected setup steps, Bun downloads, temporary runtime execution, or newly added payload-runner commands.
- Review push events and workflow-file changes from accounts that also have npm or RubyGems publisher rights.
- Check for GitHub API activity that creates commits not referenced by branches or tags, especially in repositories not normally used for release automation.
- Preserve logs before rotating secrets if active workflow backdoors may still be present.

### Secret rotation and containment
- Rotate npm, RubyGems, GitHub, cloud, Vault, Kubernetes, and password-manager-derived credentials only after removing known workflow persistence and isolating infected developer or CI hosts.
- Revoke package-registry automation tokens and validate maintainers, 2FA posture, and trusted-publishing configuration for affected packages.
- Audit all packages maintained by any compromised publisher account; the worm's propagation model means sibling packages may be poisoned even if the originally installed package was cleaned.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [IronWorm npm Rust infostealer campaign](ironworm-npm-rust-infostealer.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [TeamPCP](../actors/teampcp.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm
