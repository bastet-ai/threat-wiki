# binding.gyp npm CI/CD worm

## Summary
StepSecurity reported an active Miasma / Shai-Hulud-descended npm supply-chain worm in June 2026 that uses a small `binding.gyp` file to trigger install-time execution through npm's native-addon build path instead of obvious `package.json` lifecycle scripts. StepSecurity calls the bypass **Phantom Gyp**.

In the June 3--4 wave, StepSecurity counted 57 npm packages and 286+ malicious versions published in under two hours. The largest named victim was `@vapi-ai/server-sdk`, followed by `ai-sdk-ollama` and packages in the `autotel`, `awaitly`, `executable-stories`, `node-env-resolver`, and `wrangler-deploy` families.

The payload harvests developer and CI/CD credentials, scrapes GitHub Actions runner memory, abuses GitHub repositories as encrypted credential dead drops, injects AI-assistant and editor configuration backdoors, and uses stolen npm or RubyGems publishing access to republish poisoned package versions.

Snyk separately tracks the incident as **Node-gyp Supply Chain Compromise - June 2026**, classifies the affected releases as critical embedded malicious code, and warns that malicious versions remained resolvable from the public npm registry at the time of its June 4 writeup.

On June 5--6, StepSecurity updated its related `durabletask` coverage to report a second compromise of the `Azure/durabletask` GitHub repository and a rapid GitHub enforcement response. The reported malicious commit reused the contributor account tied to the May 19 PyPI compromise and planted AI-assistant / editor configuration files that execute a large obfuscated credential-harvesting payload when the repository is opened in Claude Code, Gemini CLI, Cursor, or VS Code. StepSecurity then verified that GitHub disabled 73 Microsoft repositories across four Microsoft GitHub organizations in a 105-second window, including the public `Azure/functions-action` repository used by GitHub Actions workflows to deploy Azure Functions.

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
- Phantom Gyp
- Miasma
- Shai-Hulud
- secrets
- AI assistants

## Why this matters
- `binding.gyp` gives the actor an install-time execution path that can be missed by controls focused on `preinstall`, `postinstall`, and other `package.json` lifecycle scripts.
- The worm targets the same high-value identity surfaces defenders now expect from Shai-Hulud-style campaigns: package-registry tokens, GitHub tokens, cloud credentials, Vault, Kubernetes, password managers, and GitHub Actions runner memory.
- It modifies repositories, including AI-assistant/editor configuration files and GitHub setup files, so remediation requires repository review, not just package removal and token rotation.
- It reportedly propagates through both npm and RubyGems publishing access, making it a cross-registry software-supply-chain incident rather than a single package-family compromise.

## Reported chain

### Install-time trigger through `binding.gyp`
- StepSecurity says the malicious packages add a 157-byte `binding.gyp` file.
- When npm sees `binding.gyp`, npm can invoke `node-gyp rebuild` during install even when the package has no suspicious `package.json` lifecycle hook.
- The malicious `binding.gyp` uses gyp command substitution to run `node index.js > /dev/null 2>&1 && echo stub.c`, returning a fake source file so the build path does not immediately fail.
- The small `binding.gyp` leads to a multi-megabyte root `index.js`; in StepSecurity's `executable-stories-demo@0.1.11` example, the legitimate package entry point remained `dist/index.js`, while the root `index.js` existed only for the install trigger.
- The JavaScript uses a ROT-N Caesar cipher and `eval()` to decode an inner script; StepSecurity observed different ROT shifts across packages as an evasion technique.
- The inner script decrypts two AES-128-GCM payloads with hardcoded keys.

### Runtime staging
- The first decrypted payload downloads Bun JavaScript runtime v1.3.13 from GitHub into a temporary directory such as `/tmp/b-*`.
- StepSecurity says the second decrypted payload is a 668 KB obfuscated main payload that runs through the downloaded Bun runtime.
- Using Bun gives the actor a standalone execution environment while keeping the initial package modification small and bypassing monitoring that keys only on Node.js child processes.
- In StepSecurity's controlled GitHub Actions run, `npm install @vapi-ai/server-sdk@1.2.2` invoked `node-gyp rebuild`, ran `node index.js`, downloaded Bun, launched `/tmp/.../bun run /tmp/...js`, called `gh auth token`, used `sudo python3` to read the GitHub Actions `Runner.Worker` process memory, and began exfiltration to `api.github.com` within seconds.

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

StepSecurity specifically observed a runner-memory scraping pipeline using `tr -d '\0'` and `grep` for GitHub Actions secret structures, a technique intended to bypass log masking by reading secret values where the runner process stores them unmasked.

### AI assistant and editor backdoors
- StepSecurity says the payload can commit backdoor configuration files into repositories reachable with stolen GitHub tokens.
- Named targets include Claude Code (`.claude/setup.mjs`, `.claude/settings.json`), Cursor (`.cursor/rules/setup.mdc`), Gemini (`.gemini/settings.json`), VS Code (`.vscode/tasks.json`, `.vscode/setup.mjs`), and GitHub setup code (`.github/setup.js`).
- The social-engineering text reported by StepSecurity frames the files as required for IDE integration and dependency setup.
- This is durable because the poisoned repository can trigger later when a developer opens the project in an AI-assisted IDE, even if the original package install is no longer happening.

### June 5 `Azure/durabletask` repository reinfection
- StepSecurity says Microsoft's official `durabletask` Python SDK was first compromised on PyPI on May 19, 2026, with malicious `durabletask` versions `1.4.1`, `1.4.2`, and `1.4.3` uploaded directly to PyPI; PyPI currently lists `1.4.0` as the latest available version and the three reported malicious versions have no files available through the public PyPI JSON API.
- StepSecurity reported that the June 5 repository reinfection used commit `5f456b8` with the decoy message `Switched DataConverter to OrchestrationContext [skip ci]`.
- The commit reportedly planted `.claude/settings.json`, `.gemini/settings.json`, `.cursor/rules/setup.mdc`, `.vscode/tasks.json`, and `.github/setup.js` rather than changing legitimate application code.
- StepSecurity says `.github/setup.js` was the actual malware, a 4.6 MB triple-obfuscated credential-harvesting payload using ROT transformation, AES-128-GCM, and JavaScript string-table mangling.
- The important defender distinction is that cloning alone was not described as the trigger; StepSecurity warned that opening the repository in VS Code or AI coding tools that auto-execute the planted configuration files should be treated as compromise and followed by credential rotation.
- The recurrence shows why Shai-Hulud / Miasma response has to include publisher-account recovery, contributor-token rotation, and repository config review. Cleaning or yanking package versions is not enough if the same identity can later commit editor or AI-agent persistence into source repositories.

### June 5--6 Microsoft repository disablement and `Azure/functions-action` blast radius
- StepSecurity's June 6 follow-up says GitHub disabled 73 Microsoft repositories across four Microsoft GitHub organizations after the `Azure/durabletask` malicious commit, with block timestamps from `2026-06-05T16:00:50Z` to `2026-06-05T16:02:35Z`.
- StepSecurity says every disabled repository returned HTTP 403 with GitHub API reason `tos`, and it cross-checked similar Azure Functions repositories plus `microsoft/durabletask-python` that were not disabled to conclude the enforcement was targeted rather than a broad outage.
- The most visible operational impact was `Azure/functions-action`, the official GitHub Action many workflows reference as `Azure/functions-action@v1` for Azure Functions deployment. While the repository was disabled, workflows relying on that mutable tag stopped resolving.
- Microsoft Learn responses quoted by StepSecurity recommended alternate deployment paths while the repository was unavailable, including Azure CLI, Azure DevOps Pipelines, VS Code deployment, Zip Deploy, or Azure Pipelines.
- This adds a second defender lesson beyond editor/AI-agent auto-execution: high-dependence GitHub Actions are availability dependencies. Pinning actions to commit SHAs can make failures more explicit and tamper-resistant, but it does not remove the need for contingency deployment paths when an upstream action repository is disabled.
- StepSecurity linked the `Azure/durabletask` commit and the May 19 PyPI compromise through the same contributor account, and framed two plausible explanations: the original credentials were never fully rotated, or the account was re-compromised through the worm's own AI-tool / folder-open propagation loop.

### GitHub repository abuse
- StepSecurity traced exfiltration to the GitHub account `liuende501`, which it says hosted 236 programmatically created repositories used as credential dead drops.
- The malware creates private repositories under that account and uploads encrypted JSON files under `results/results-{timestamp}.json`.
- StepSecurity reported repository descriptions including `Miasma - The Spreading Blight` and the reversed string `niagA oG eW ereH :duluH-iahS`, which reads `Shai-Hulud: Here We Go Again`.
- Reported GitHub API patterns include commit-search beacons for `thebeautifulmarchoftime`, token-validation searches for `IfYouInvalidateThisTokenItWillNukeTheComputerOfTheOwner`, authenticated `/user` checks, repository creation, content uploads, and GraphQL `createCommitOnBranch` calls.

### Package-registry propagation
- With stolen npm or RubyGems tokens, the worm queries registry accounts for packages the victim maintains.
- It downloads maintained packages, injects the malicious payload, and publishes new poisoned versions.
- For npm, StepSecurity reports token validation via `/-/whoami`, maintainer package enumeration, OIDC token exchange, tarball manipulation, and publication of repackaged releases.
- StepSecurity says the payload can request Fulcio signing material, create Rekor transparency-log entries, and generate SLSA v1 provenance attestations, making provenance checks insufficient if the attacker controls the publishing identity or OIDC path.
- For RubyGems, StepSecurity reports injection into Ruby native-extension build files such as `extconf.rb`, with related `Makefile.PL` and `CMakeLists.txt` variants in the payload.
- StepSecurity listed compromised versions published between June 3 and June 4, 2026 and noted that its list was still being updated.
- Early named package families in the StepSecurity table included `@vapi-ai/server-sdk`, `ai-sdk-ollama`, many `autotel-*` packages, `awaitly-*` packages, `executable-stories-*` packages, `node-env-resolver*`, and `wrangler-deploy`.

## Defender heuristics

### Package review
- Treat unexpected `binding.gyp` additions as install-time code-execution signals, even when `package.json` scripts are absent or unchanged.
- Diff newly published package tarballs against prior known-good versions and flag tiny build-configuration files that launch larger staged scripts.
- Expand package-security checks beyond lifecycle hooks to include `node-gyp`, native-addon build files, generated project files, and build-tool configuration.
- Flag root-level multi-megabyte `index.js` files that are not the declared package entry point.
- Review exposure to the package names and versions StepSecurity lists; the list was still changing at publication time, so use the source as the live reference.

### CI/CD and repository response
- Search CI logs for unexpected `node-gyp rebuild`, `curl` or `unzip` under `npm install`, Bun downloads from `github.com/oven-sh/bun/releases/download/bun-v1.3.13/`, `gh auth token`, and attempts to read `/proc/*/mem`.
- Review push events and workflow-file changes from accounts that also have npm or RubyGems publisher rights.
- Check for GitHub API activity that creates new repositories, uploads `results/results-*.json`, searches commits for `thebeautifulmarchoftime`, or uses GraphQL `createCommitOnBranch` unexpectedly.
- Audit AI-assistant and editor config paths: `.claude/`, `.cursor/`, `.gemini/`, `.vscode/`, and `.github/setup.js`.
- Preserve logs before rotating secrets if active repository backdoors may still be present.

### Secret rotation and containment
- Rotate npm, RubyGems, GitHub, cloud, Vault, Kubernetes, and password-manager-derived credentials only after removing known repository persistence and isolating infected developer or CI hosts.
- Revoke package-registry automation tokens and validate maintainers, 2FA posture, and trusted-publishing configuration for affected packages.
- Audit all packages maintained by any compromised publisher account; the worm's propagation model means sibling packages may be poisoned even if the originally installed package was cleaned.
- For critical GitHub Actions such as deployment actions, pin to reviewed commit SHAs where possible, track upstream repository availability, and maintain an alternate deployment runbook for repository-disabled or tag-unavailable events.

## Reported indicators
- `binding.gyp` SHA-256: `ef641e956f91d501b748085996303c96a64d67f63bfeef0dda175e5aa19cca90`
- Example `executable-stories-demo@0.1.11` package tarball SHA-256: `288f26c2eadcb1a7923fe376d16f5404216cce15d9fc162a4a78574dc7df399a`
- Decrypted Bun loader SHA-256: `ceff7c51d70832c3ec8dd2744b606a23b3c924ef664ae23439b9b742ea154108`
- Decrypted main payload SHA-256: `da39146ef451d1b174a24d00b1e2a45cd38d54e849737f8f35333dcb22175707`
- GitHub exfil account: `github.com/liuende501`
- GitHub commit-search C2 keyword: `thebeautifulmarchoftime`
- GitHub token-validation keyword: `IfYouInvalidateThisTokenItWillNukeTheComputerOfTheOwner`
- Bun download path: `github.com/oven-sh/bun/releases/download/bun-v1.3.13/`
- Suspicious gyp command marker: `<!(node index.js > /dev/null 2>&1 && echo stub.c)`
- `durabletask` malicious PyPI versions reported by StepSecurity: `1.4.1`, `1.4.2`, `1.4.3`
- `Azure/durabletask` malicious repository commit reported by StepSecurity: `5f456b8`
- `durabletask` reported C2 / payload host: `check.git-service[.]com`
- `durabletask` reported secondary C2: `t.m-kosche[.]com`
- `durabletask` reported C2 IP: `160.119.64.3`
- `Azure/functions-action` disabled-repository impact reported by StepSecurity: workflows referencing `Azure/functions-action@v1` stopped resolving while the repository was unavailable

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [IronWorm npm Rust infostealer campaign](ironworm-npm-rust-infostealer.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [TeamPCP](../actors/teampcp.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm
- Snyk: https://snyk.io/blog/node-gyp-supply-chain-compromise-self-propagating-npm-worm-binding-gyp/
- StepSecurity: https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack
- StepSecurity Microsoft repository disablement follow-up: https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents
- PyPI: https://pypi.org/pypi/durabletask/json
