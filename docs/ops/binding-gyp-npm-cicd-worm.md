# binding.gyp npm CI/CD worm

## Summary
StepSecurity reported an active Miasma / Shai-Hulud-descended npm supply-chain worm in June 2026 that uses a small `binding.gyp` file to trigger install-time execution through npm's native-addon build path instead of obvious `package.json` lifecycle scripts. StepSecurity calls the bypass **Phantom Gyp**.

In the June 3--4 wave, StepSecurity counted 57 npm packages and 286+ malicious versions published in under two hours. The largest named victim was `@vapi-ai/server-sdk`, followed by `ai-sdk-ollama` and packages in the `autotel`, `awaitly`, `executable-stories`, `node-env-resolver`, and `wrangler-deploy` families. OX Security separately measured the same wave at 57 affected packages, 152,376 accumulated weekly downloads, 647,204 accumulated monthly downloads, and more than 118 GitHub repositories containing stolen credentials.

The payload harvests developer and CI/CD credentials, scrapes GitHub Actions runner memory, abuses GitHub repositories as encrypted credential dead drops, injects AI-assistant and editor configuration backdoors, and uses stolen npm or RubyGems publishing access to republish poisoned package versions.

Snyk separately tracks the incident as **Node-gyp Supply Chain Compromise - June 2026**, classifies the affected releases as critical embedded malicious code, and warns that malicious versions remained resolvable from the public npm registry at the time of its June 4 writeup.

On June 5--6, StepSecurity updated its related `durabletask` coverage to report a second compromise of the `Azure/durabletask` GitHub repository and a rapid GitHub enforcement response. The reported malicious commit reused the contributor account tied to the May 19 PyPI compromise and planted AI-assistant / editor configuration files that execute a large obfuscated credential-harvesting payload when the repository is opened in Claude Code, Gemini CLI, Cursor, or VS Code. StepSecurity then verified that GitHub disabled 73 Microsoft repositories across four Microsoft GitHub organizations in a 105-second window, including the public `Azure/functions-action` repository used by GitHub Actions workflows to deploy Azure Functions.

SafeDep separately documented a source-repository arm of the same Miasma activity: more than 120 GitHub repositories, including five `icflorescu` projects and `Azure/durabletask`, received direct commits that skipped the package-registry install path and instead wired `.github/setup.js` into AI-assistant, editor, and `npm test` auto-execution surfaces.

On June 7, Socket reported a PyPI branch of the same Mini Shai-Hulud / Miasma lineage that it tracks with **Hades**-themed markers. Socket counted 37 malicious wheel artifacts across 19 PyPI packages, apparently published during a single maintainer-account takeover, that used executable `*-setup.pth` files to attempt Python-startup execution, download Bun, and run an obfuscated `_index.js` JavaScript credential stealer.

On June 8, StepSecurity reported a second Hades PyPI wave in graph machine-learning, computational-biology, bioinformatics, and genotype-phenotype packages. This wave moved from Socket's `*-setup.pth` startup-hook shape to an obfuscated package `__init__.py` import hook, used Bun v1.3.14, added prompt-injection text intended to mislead LLM-based malware triage, introduced macOS and Windows runner-memory scrapers, and added SSH/SCP lateral movement plus persistence / wiper-deterrent services. Socket's same-day follow-up expanded the Hades PyPI count to 60 artifacts across 37 PyPI packages and identified additional delivery shapes: trojanized native `.abi3.so` extensions in bioinformatics packages and an MCP-themed `langchain-core-mcp` loader that searches `sys.path` for an `_index.js` payload instead of bundling it in the same wheel.

Later on June 8, StepSecurity reported a short-lived compromise of the public `Pythagora-io/gpt-pilot` AI coding-tool repository. The attacker allegedly used a compromised maintainer account to force-push a backdated Shai-Hulud-family credential stealer into `core/telemetry/`, but the repository's `ruff` formatting and lint checks failed twice and appear to have prevented a clean malicious build.

On June 9, GitHub announced npm v12 security-default changes that directly address this incident class. GitHub says npm v12, estimated for July 2026, will make `npm install` stop executing dependency `preinstall`, `install`, and `postinstall` scripts unless the project explicitly allows them. GitHub specifically says this also blocks implicit native `node-gyp` builds from packages that contain `binding.gyp`, because npm currently runs `node-gyp rebuild` for that shape even without an explicit install script. npm 11.16.0 and newer can already show warnings and help maintainers prepare with `npm approve-scripts --allow-scripts-pending`, `npm approve-scripts`, and `npm deny-scripts`.

On June 26, StepSecurity reported another Miasma-style Phantom Gyp wave against four Immobiliare Labs Backstage plugin packages. The malicious patch releases added a root `binding.gyp` plus 5 MB `index.js`, executed at install time, downloaded Bun `v1.3.13`, scraped GitHub Actions `Runner.Worker` memory, stole cloud / registry / password-manager secrets, and attempted AI-assistant persistence.

## Tags
- ops
- operations
- malware
- supply-chain
- npm
- PyPI
- RubyGems
- GitHub Actions
- CI/CD
- credential-theft
- worm
- node-gyp
- binding.gyp
- .pth
- Phantom Gyp
- Hades
- Miasma
- Shai-Hulud
- secrets
- AI assistants

## Why this matters
- `binding.gyp` gives the actor an install-time execution path that can be missed by controls focused on `preinstall`, `postinstall`, and other `package.json` lifecycle scripts.
- The worm targets the same high-value identity surfaces defenders now expect from Shai-Hulud-style campaigns: package-registry tokens, GitHub tokens, cloud credentials, Vault, Kubernetes, password managers, and GitHub Actions runner memory.
- It modifies repositories, including AI-assistant/editor configuration files and GitHub setup files, so remediation requires repository review, not just package removal and token rotation.
- It reportedly propagates through both npm and RubyGems publishing access, making it a cross-registry software-supply-chain incident rather than a single package-family compromise.
- The June 7 Socket report shows the same lineage adapting to PyPI wheels through executable `.pth` startup hooks, and StepSecurity's June 8 follow-up shows package-import execution through `__init__.py`; Python dependency review needs the same scrutiny defenders apply to npm lifecycle scripts and native-addon build paths.
- StepSecurity's June 8 report shows the campaign targeting both CI/CD runners and developer workstations: cross-platform runner-memory scraping, SSH/SCP staging to known hosts, AI-assistant / IDE rule hijacking, and token-revocation-triggered wiper deterrence make simple package yanking or immediate token revocation insufficient without host containment.
- The `gpt-pilot` incident shows a source-repository takeover path where ordinary code-quality gates can become useful tripwires: style and import-order failures are not a replacement for branch protection, but they can block attacker code that does not match a project's normal conventions.
- GitHub's announced npm v12 defaults turn the main `binding.gyp` lesson into an ecosystem control: dependency install-time code should be denied by default and restored only through committed, reviewable package-level allowlists.

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

### Source-repository auto-execution arm
- SafeDep says the June 3 Miasma activity had a parallel source-repository arm that pushed directly to GitHub repositories instead of relying on a poisoned npm package install.
- Its worked example is `icflorescu/mantine-datatable`, where commit `f72462d9e5fa90a483062a83e9ffcb2edc57bf7e` used the message `chore: update dependencies [skip ci]`, was unsigned, and was authored as `github-actions <[email protected]>`.
- The commit added `.claude/settings.json`, `.cursor/rules/setup.mdc`, `.gemini/settings.json`, `.github/setup.js`, `.vscode/tasks.json`, and a `package.json` test-script change. Five of those files launched `.github/setup.js`, a 4.3 MB one-line dropper.
- SafeDep reports the Claude Code and Gemini files used `SessionStart` hooks, the Cursor rule used `alwaysApply: true` and instructed the agent to run `node .github/setup.js`, VS Code used a `runOn: folderOpen` task, and `package.json` changed `test` to `node .github/setup.js`.
- The important operational distinction is that cloning a repository was not described as the trigger; opening it in a configured editor or AI coding agent, or running the poisoned test script, was the dangerous step.
- SafeDep found the same fingerprint in 123 repositories across dozens of accounts, including `Azure/durabletask`, and noted that the source-repo dropper was recompiled per wave. It assessed the source-repo loader as the same Miasma staged Bun loader with a ROT shift changed from 9 to 4 and different AES keys.
- SafeDep also called out a detection blind spot: the large `.github/setup.js` stayed above GitHub code search's roughly 384 KB indexing limit, so defenders should hunt for the small launcher files as well as for the dropper path itself.

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

### June 7 Hades PyPI wheel wave
- Socket reported a PyPI wave of the Mini Shai-Hulud / Miasma lineage with Hades-themed markers. Socket counted 37 malicious wheel artifacts across 19 PyPI packages and said the releases looked like a single maintainer-account takeover with consecutive patch releases mass-published across the author's portfolio.
- The highest-impact affected package families Socket called out were research-community bioinformatics and genomics tools: `dynamo-release`, `spateo-release`, `coolbox`, `ufish`, and `napari-ufish`. Socket said the rest of the set was mostly lower-traffic agent/task-execution, function-description, and lab-utility libraries.
- Reported malicious artifacts included `bramin@0.0.2` through `0.0.4`, `cmd2func@0.2.2` and `0.2.3`, `coolbox@0.4.1` and `0.4.2`, `dynamo-release@1.5.4`, `executor-engine@0.3.4` and `0.3.5`, `executor-http@0.1.3` and `0.1.4`, `funcdesc@0.2.2` and `0.2.3`, `magique@0.6.8` and `0.6.9`, `magique-ai@0.4.4` and `0.4.5`, `mrbios@0.1.1` and `0.1.2`, `napari-ufish@0.0.2` and `0.0.3`, `nucbox@0.1.2` and `0.1.3`, `okite@0.0.7` and `0.0.8`, `pantheon-agents@0.6.1` and `0.6.2`, `pantheon-toolsets@0.5.5` and `0.5.6`, `spateo-release@1.1.2`, `synago@0.1.1` and `0.1.2`, `ufish@0.1.2` and `0.1.3`, and `uprobe@0.1.3` and `0.1.4`.
- The malicious wheel shape was a package-local `_index.js` plus a `*-setup.pth` file. The `.pth` file used Python's `site` module behavior for executable lines beginning with `import` to attempt execution during interpreter startup, not only when the compromised package was imported.
- Socket's normalized loader created a temp sentinel `.bun_ran`, looked for `_index.js`, downloaded Bun v1.3.13 from `github.com/oven-sh/bun/releases/download/` when a cached tempdir binary was absent, and ran `bun run _index.js`.
- Socket noted an implementation caveat: in a local CPython reproduction, this exact loader shape did not automatically resolve the adjacent `_index.js` because `__file__` can resolve to `site.py` rather than the `.pth` file. The artifact is still malicious because it ships the credential stealer and attempts to bootstrap Bun from Python startup.
- Static deobfuscation matched the broader family: a JavaScript `try { eval(...) }` wrapper with a character-code array and ROT-style substitution, AES-GCM encrypted stages, a Bun bootstrapper, a rotated string table, PBKDF2/SHA256 string decoding, and an AES-256-GCM plus gzip string layer.
- Socket said the payload targeted GitHub credentials, GitHub Actions runner secrets and memory, `ghs_*` tokens, npm, PyPI, RubyGems, JFrog, CircleCI, Anthropic and package-publishing tokens, AWS / GCP / Azure / Kubernetes / Vault secrets, `.env`, `.npmrc`, `.pypirc`, Git credentials, shell histories, SSH keys, Docker configs, cloud CLI caches, Claude/MCP configs, wallet/app data, and other developer-machine secrets.
- The Hades branch used GitHub exfiltration markers distinct from the earlier Miasma wording: repository description `Hades - The End for the Damned`, commit marker `IfYouYankThisTokenItWillNukeTheComputerOfTheOwnerFully`, path pattern `results/results-*.json`, artifact name `format-results`, and workflow name `Run Copilot`.
- Socket also found a direct HTTPS sender pointed at `api.anthropic.com/v1/api`, but it assessed this as likely network-log camouflage because that path returns Anthropic's standard `404 not_found_error` and GitHub remained the confirmed exfiltration channel. This is not evidence that Anthropic systems were compromised.
- Socket reported that, at publication time, it was tracking 448 affected artifacts across npm and PyPI in the broader campaign: 411 npm artifacts across 106 packages plus the 37 PyPI wheels across 19 projects.

### June 8 Hades graph-ML import-hook wave
- StepSecurity reported a new Hades Campaign PyPI wave affecting graph machine-learning, computational-biology, bioinformatics, and genotype-phenotype packages. Reported affected releases were `mflux-streamlit@0.0.3` and `0.0.4`, `nhmpy@2.4.7`, `ppkt2synergy@0.1.1`, `embiggen@0.11.97`, `gpsea@0.9.14`, `pyphetools@0.9.120`, and `ensmallen@0.8.101`.
- Unlike the earlier Socket-described `*-setup.pth` wheel artifacts, StepSecurity says this wave embedded an obfuscated one-line import hook in package `__init__.py`. On import, the hook checks `/tmp/.bun_ran`, searches Python module paths for `_index.js`, downloads Bun v1.3.14 from `github.com/oven-sh/bun/releases/download/`, extracts it under a temporary `b/` directory, and runs `bun run _index.js`.
- StepSecurity said the `_index.js` bundle begins with plain-text prompt-injection instructions meant to mislead LLM-based analysis pipelines into classifying the package as clean and ignoring the obfuscated code below it. Treat this as analyzer evasion against AI-assisted malware triage, not as a user-facing prompt-injection lure.
- The JavaScript payload moved to a modular architecture: StepSecurity recovered 16 gzip-compressed AES-256-GCM payload blobs with distinct hardcoded keys, including modules for macOS and Windows memory reads, IDE / CI backdoors, and C2 agents.
- Runner-memory scraping expanded beyond Linux `/proc/{pid}/mem`. StepSecurity described a macOS scraper using Mach VM APIs via Python `ctypes` and a Windows PowerShell / C# scraper using `VirtualQueryEx` and `ReadProcessMemory`, in addition to Linux `/proc/{pid}/maps` and `/proc/{pid}/mem` walking.
- StepSecurity described three GitHub-backed C2 channels: token dead-drop commits containing `DontRevokeOrItGoesBoom`, signed JavaScript eval commits keyed by `TheBeautifulSnadsOfTime`, and a Python `updater.py` daemon polling GitHub commit search for `firedalazer` commands.
- The exfiltration pattern kept Hades naming: public GitHub repositories named with underworld wordlist combinations such as `stygian-cerberus-[0-9]+` or `tartarean-charon-[0-9]+` and repository description `Hades - The End for the Damned`.
- StepSecurity said the malware attempts SSH/SCP lateral movement by parsing `~/.ssh/known_hosts` and `~/.ssh/config`, staging `ai_setup.sh` and `ai_init.js` under `/tmp/.sshu-[random]`, executing the loader through `ssh`, and deleting the staging directory.
- In GitHub Actions, StepSecurity said the payload tries to mint PyPI or npm publish tokens through `ACTIONS_ID_TOKEN_REQUEST_TOKEN` / `ACTIONS_ID_TOKEN_REQUEST_URL`, request Fulcio certificates, DSSE-sign SLSA provenance, upload to Rekor, and publish trojanized packages with apparently valid Sigstore provenance.
- For repository-level secret extraction, StepSecurity described two workflow-injection paths using a `Run Copilot` workflow: a push-triggered `.github/workflows/codeql.yml` path when the token has `workflow` scope, and a deployment-triggered path that temporarily commits and deletes `.github/workflows/codeql-[random].yml` before triggering the `Development` deployment environment.
- The AI-assistant / IDE backdoor scope broadened beyond the earlier `.claude`, `.gemini`, `.cursor`, and `.vscode` paths. StepSecurity said this wave looks for configuration surfaces for 14 agent systems, including Claude, Codex, Gemini, Copilot, Cline, Aider, Tabby, Amazon Q, Cody, Bolt, and Continue, and plants instructions or hooks that bootstrap Bun when the workspace is loaded or analyzed.
- StepSecurity reported persistence through `update-monitor` plus a `gh-token-monitor` deterrent service. The deterrent polls `https://api.github.com/user` with the stolen token for up to 72 hours and, if the token returns a 4xx status, executes destructive removal commands against the user's home directory and Documents folder. In incident response, isolate affected hosts and preserve evidence before revoking tokens that may be watched by this service.

### June 8 Socket Hades PyPI native-extension and MCP-loader follow-up
- Socket reported 23 newer PyPI package-version artifacts beyond its June 7 set, raising its tracker to 471 affected artifacts across npm and PyPI: 411 npm artifacts across 106 packages and 60 PyPI artifacts across 37 packages.
- The newer set mixed established research-community packages with lookalike / ecosystem-bait packages. Socket named bioinformatics / graph-learning packages such as `embiggen`, `ensmallen`, `gpsea`, `mflux-streamlit`, `phenopacket-store-toolkit`, `ppkt2synergy`, and `pyphetools`, alongside AI / MCP-themed or typosquat-style packages such as `instructor-mcp`, `langchain-core-mcp`, `openai-mcp`, `ray-mcp-server`, `tiktoken-mcp`, `rsquests`, and `tlask`.
- Socket described three PyPI delivery branches in the Hades lineage: the earlier `*-setup.pth` startup hook plus bundled `_index.js`; native-extension import-time execution where a trojanized `.abi3.so` extension launches `_index.js` during module initialization; and the `langchain-core-mcp` loader variant where a `.pth` hook searches `sys.path` for `_index.js` rather than shipping the payload in the same wheel.
- The native-extension branch is important for scientific Python review because compiled extensions are common in performance-sensitive graph, genomics, and machine-learning packages. A package can show benign-looking `.py` source while the malicious trigger lives in the compiled extension loaded through `dlopen()`.
- Socket said `langchain-core-mcp@1.4.2` installed `langchain_core-setup.pth`, used a `/tmp/.bun_ran` marker, downloaded Bun if needed, searched Python's module path for `_index.js`, and launched the discovered JavaScript with `bun run`. Socket considered this malicious even though the artifact did not bundle `_index.js`, because legitimate packages should not silently bootstrap Bun and execute arbitrary JavaScript discovered elsewhere on `sys.path`.
- Socket reused its earlier Hades payload analysis for the stealer behavior: once launched, the Bun-stage JavaScript targets developer workstations and CI/CD environments for GitHub, npm, PyPI, RubyGems, JFrog, cloud, Kubernetes, Docker, SSH, shell-history, `.env`, package-registry, and AI developer-tool secrets.

### June 8 `Pythagora-io/gpt-pilot` force-push attempt
- StepSecurity reported that an attacker compromised the `LeonOstrez` GitHub account, belonging to a `Pythagora-io/gpt-pilot` co-founder and maintainer, and force-pushed directly to the repository's `main` branch. StepSecurity said the branch had no protection rules; the GitHub API returned 404 for the branch-protection endpoint.
- The first force push at `2026-06-08 11:01:38Z` reportedly replaced clean history at `53154df1c66b` with malicious head `90f59f5de681`. A second force push at `11:13:07Z` replaced that with `a372904facd5` after the first CI attempt failed.
- The malicious commit was titled `Revert 'Implemented weekend discount'` and was backdated to `2025-08-24 20:37:44`, making it look older in casual history review. StepSecurity contrasted a clean revert commit `566fbb120bc436385aa5a4cb93d7c351dec2127e` with malicious commit `065ee8ebee7385cb644fd1608587a18edb91f4fb`, which added malware while preserving similar metadata.
- The injected files lived under `core/telemetry/`: `_hooks.py`, `_runtime.bin`, and a modified `__init__.py`. The modified telemetry initializer spawned a daemon thread that imported `core.telemetry._hooks` and ran it when `gpt-pilot` executed.
- `_hooks.py` was a cross-platform Python loader that downloaded Bun v1.3.13, used `.loader.lock` to avoid duplicate execution, suppressed output, and launched the `_runtime.bin` payload. Despite the `.bin` extension, StepSecurity described `_runtime.bin` as a 758 KB single-line obfuscated JavaScript credential stealer.
- The payload targeted cloud, CI/CD, package-registry, Kubernetes, Vault, SSH, and GitHub credentials; created GitHub repositories to store stolen data; used `claude@users.noreply.github.com` as a commit author identity; and included a secondary encrypted DNS-resolved HTTP exfiltration path.
- StepSecurity said the malware searched GitHub commits for `thebeautifulsnadsoftime` and extracted base64 command material from matching commit messages, making public GitHub commit search a covert C2 channel.
- The payload also planted developer-tool persistence through `.claude/settings.json` `SessionStart` hooks and VS Code `tasks.json` `folderOpen` tasks, matching the broader Miasma / Hades theme of repository-local auto-execution.
- The compromise failed to pass CI twice. First, `ruff format --check` flagged `_hooks.py`; after the attacker reformatted and force-pushed, `ruff check` flagged E402 and I001 import-order violations in the modified `__init__.py`. StepSecurity said all six CI jobs failed both times and the attacker stopped.
- StepSecurity called the payload a direct Shai-Hulud-family instance and referenced TeamPCP / UNC6780, but it also caveated attribution because TeamPCP had publicly released Mini Shai-Hulud source code on May 12, 2026. Treat this as family linkage with original-actor vs copycat uncertainty.

### GitHub repository abuse
- StepSecurity traced exfiltration to the GitHub account `liuende501`, which it says hosted 236 programmatically created repositories used as credential dead drops.
- The malware creates private repositories under that account and uploads encrypted JSON files under `results/results-{timestamp}.json`.
- StepSecurity reported repository descriptions including `Miasma - The Spreading Blight` and the reversed string `niagA oG eW ereH :duluH-iahS`, which reads `Shai-Hulud: Here We Go Again`.
- OX Security reported another repository-description variant using an en dash, `Miasma – The Spreading Blight`, with the first observed GitHub commit on June 4, 2026 at 02:46:12 +0800 and activity tied to the `windy629` account from its earlier Miasma analysis. Add the en-dash form to hunts alongside `Miasma: The Spreading Blight`, `Miasma : The Spreading Blight`, and StepSecurity's hyphenated `Miasma - The Spreading Blight` form.
- Reported GitHub API patterns include commit-search beacons for `thebeautifulmarchoftime`, token-validation searches for `IfYouInvalidateThisTokenItWillNukeTheComputerOfTheOwner`, authenticated `/user` checks, repository creation, content uploads, and GraphQL `createCommitOnBranch` calls.

### Package-registry propagation
- With stolen npm or RubyGems tokens, the worm queries registry accounts for packages the victim maintains.
- It downloads maintained packages, injects the malicious payload, and publishes new poisoned versions.
- For npm, StepSecurity reports token validation via `/-/whoami`, maintainer package enumeration, OIDC token exchange, tarball manipulation, and publication of repackaged releases.
- StepSecurity says the payload can request Fulcio signing material, create Rekor transparency-log entries, and generate SLSA v1 provenance attestations, making provenance checks insufficient if the attacker controls the publishing identity or OIDC path.
- For RubyGems, StepSecurity reports injection into Ruby native-extension build files such as `extconf.rb`, with related `Makefile.PL` and `CMakeLists.txt` variants in the payload.
- StepSecurity listed compromised versions published between June 3 and June 4, 2026 and noted that its list was still being updated.
- Early named package families in the StepSecurity table included `@vapi-ai/server-sdk`, `ai-sdk-ollama`, many `autotel-*` packages, `awaitly-*` packages, `executable-stories-*` packages, `node-env-resolver*`, and `wrangler-deploy`.
- OX Security's June 4 update added an edited follow-on list for packages it said had also been hit by weaponized `binding.gyp`: `discord-search@0.1.2`, `create-cf-token@1.1.3`, `@forjacms/analytics@1.8.4`, `@forjacms/client@1.8.4`, `@forjacms/sections@1.8.4`, `@forjacms/sections-react@1.8.4`, `dbmux@2.2.4`, `creditcard.js@3.0.60`, `github-archiver@1.5.5`, and `@contaazul/n8n-nodes-contaazul@0.3.26`. Treat vendor package tables as live references rather than copying every version into local detection logic.
- StepSecurity's June 26 Immobiliare Labs Backstage plugin report added a narrow platform-engineering package set: `@immobiliarelabs/backstage-plugin-gitlab`, `@immobiliarelabs/backstage-plugin-gitlab-backend`, `@immobiliarelabs/backstage-plugin-ldap-auth`, and `@immobiliarelabs/backstage-plugin-ldap-auth-backend`, with malicious patch releases across several supported major versions. See the dedicated [Immobiliare Labs Backstage plugins npm compromise](immobiliarelabs-backstage-plugins-npm-compromise.md) page for the current affected-version table.

## Defender heuristics

### Package review
- Start testing npm 11.16.0+ warnings before npm v12 lands. Run `npm approve-scripts --allow-scripts-pending`, review every dependency that wants install-time execution, commit the resulting allowlist for packages you trust, and explicitly deny the rest with `npm deny-scripts`.
- Treat npm v12 script-approval diffs as security-relevant code review. A new allowlist entry for `preinstall`, `install`, `postinstall`, `prepare`, or an implicit `node-gyp` build can re-enable the same execution class used by Miasma / Phantom Gyp.
- Avoid broad fallbacks that undo the new defaults, such as globally re-enabling scripts for convenience. Prefer per-project allowlists and CI checks that fail when unreviewed packages request install-time execution.
- Treat unexpected `binding.gyp` additions as install-time code-execution signals, even when `package.json` scripts are absent or unchanged.
- Treat executable `*.pth` / `*-setup.pth` additions in wheels as Python startup execution signals. A wheel that downloads a runtime, writes tempdir executables, or launches `bun run _index.js` should be handled as malicious even if normal package imports are never used.
- Treat unexpected import-side code in package `__init__.py` as a Python execution trigger. Flag imports that search `sys.path` for `_index.js`, download Bun, create `/tmp/.bun_ran`, or execute JavaScript from package-local files.
- Treat compiled Python extension changes as potential execution triggers, especially in packages that normally ship `.abi3.so` performance modules. Source-only review can miss an import-time native extension that launches `_index.js` as a side effect of `dlopen()`.
- Flag `.pth` loaders that search broad Python module paths for `_index.js` or other payload files instead of bundling them locally; split loader/payload staging can defeat rules that expect both artifacts in one wheel.
- Diff newly published package tarballs against prior known-good versions and flag tiny build-configuration files that launch larger staged scripts.
- Expand package-security checks beyond lifecycle hooks to include `node-gyp`, native-addon build files, generated project files, and build-tool configuration.
- Flag root-level multi-megabyte `index.js` files that are not the declared package entry point.
- Review exposure to the package names and versions StepSecurity lists; the list was still changing at publication time, so use the source as the live reference.

### CI/CD and repository response
- Search CI logs for unexpected `node-gyp rebuild`, `curl` or `unzip` under `npm install`, Bun downloads from `github.com/oven-sh/bun/releases/download/bun-v1.3.13/`, `gh auth token`, and attempts to read `/proc/*/mem`.
- Review push events and workflow-file changes from accounts that also have npm or RubyGems publisher rights.
- Check for GitHub API activity that creates new repositories, uploads `results/results-*.json`, searches commits for `thebeautifulmarchoftime`, or uses GraphQL `createCommitOnBranch` unexpectedly.
- Search repository descriptions for all reported Miasma spacing and punctuation variants, including `Miasma - The Spreading Blight`, `Miasma – The Spreading Blight`, `Miasma: The Spreading Blight`, and `Miasma : The Spreading Blight`.
- Search GitHub repositories, workflows, and artifacts for Hades markers from the PyPI wave: `Hades - The End for the Damned`, `IfYouYankThisTokenItWillNukeTheComputerOfTheOwnerFully`, `results/results-*.json`, `format-results`, and workflow name `Run Copilot`.
- Add StepSecurity's June 8 Hades pivots to hunts: `DontRevokeOrItGoesBoom`, `TheBeautifulSnadsOfTime`, `firedalazer`, `stygian-cerberus-[0-9]+`, `tartarean-charon-[0-9]+`, `/tmp/.bun_ran`, `/tmp/tmp.0144018410.lock`, `/var/tmp/.gh_update_state`, `~/.local/share/updater/update.py`, `~/.config/systemd/user/update-monitor.service`, and `~/.config/systemd/user/gh-token-monitor.service`.
- Audit AI-assistant and editor config paths: `.claude/`, `.cursor/`, `.gemini/`, `.vscode/`, and `.github/setup.js`.
- Expand AI-assistant config review to Codex, Copilot, Cline, Aider, Tabby, Amazon Q, Cody, Bolt, Continue, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, `.aider.conf.yml`, `settings.json`, `config.json`, and `mcp.json` when those files can trigger local commands or agent setup.
- Search for repository commits that combine the message `chore: update dependencies [skip ci]`, author `github-actions <[email protected]>`, a large `.github/setup.js`, and launcher files under `.claude/settings.json`, `.gemini/settings.json`, `.cursor/rules/setup.mdc`, `.vscode/tasks.json`, or `package.json` test scripts.
- For source-repository takeovers, alert on default-branch force pushes, history rewrites, backdated commits with fresh push events, unsigned or unexpectedly authored commits, and changes under low-scrutiny modules such as telemetry or setup code.
- Keep required style, lint, and format checks enabled and make them merge gates. StepSecurity's `gpt-pilot` case shows `ruff` catching malicious code because the injected loader did not match project formatting and import-order conventions.
- Branch-protect default branches: require pull requests, required passing status checks, restrict force pushes, and require signed commits where practical. Lint gates helped in the `gpt-pilot` case, but branch protection would have reduced the single-account force-push blast radius.
- Before opening an untrusted clone in VS Code, Cursor, Claude Code, or Gemini CLI, inspect for folder-open / session-start commands that run `node .github/setup.js` or similar project-local setup files.
- Preserve logs before rotating secrets if active repository backdoors may still be present.

### Secret rotation and containment
- Rotate npm, RubyGems, GitHub, cloud, Vault, Kubernetes, and password-manager-derived credentials only after removing known repository persistence and isolating infected developer or CI hosts.
- Before revoking GitHub tokens from hosts that may have imported June 8 Hades packages, check for the reported `gh-token-monitor` persistence. StepSecurity described a token-revocation-triggered wiper deterrent, so containment should prioritize host isolation, evidence capture, and persistence removal before broad revocation from the still-running host.
- Revoke package-registry automation tokens and validate maintainers, 2FA posture, and trusted-publishing configuration for affected packages.
- Audit all packages maintained by any compromised publisher account; the worm's propagation model means sibling packages may be poisoned even if the originally installed package was cleaned.
- For critical GitHub Actions such as deployment actions, pin to reviewed commit SHAs where possible, track upstream repository availability, and maintain an alternate deployment runbook for repository-disabled or tag-unavailable events.

## Reported indicators
- `binding.gyp` SHA-256: `ef641e956f91d501b748085996303c96a64d67f63bfeef0dda175e5aa19cca90`
- Example `executable-stories-demo@0.1.11` package tarball SHA-256: `288f26c2eadcb1a7923fe376d16f5404216cce15d9fc162a4a78574dc7df399a`
- Decrypted Bun loader SHA-256: `ceff7c51d70832c3ec8dd2744b606a23b3c924ef664ae23439b9b742ea154108`
- Decrypted main payload SHA-256: `da39146ef451d1b174a24d00b1e2a45cd38d54e849737f8f35333dcb22175707`
- GitHub exfil account: `github.com/liuende501`
- OX-reported GitHub account tied to the en-dash repository-description variant: `github.com/windy629`
- GitHub commit-search C2 keyword: `thebeautifulmarchoftime`
- GitHub token-validation keyword: `IfYouInvalidateThisTokenItWillNukeTheComputerOfTheOwner`
- Bun download path: `github.com/oven-sh/bun/releases/download/bun-v1.3.13/`
- Suspicious gyp command marker: `<!(node index.js > /dev/null 2>&1 && echo stub.c)`
- `durabletask` malicious PyPI versions reported by StepSecurity: `1.4.1`, `1.4.2`, `1.4.3`
- `Azure/durabletask` malicious repository commit reported by StepSecurity: `5f456b8`
- SafeDep-reported `icflorescu/mantine-datatable` source-repo commit: `f72462d9e5fa90a483062a83e9ffcb2edc57bf7e`
- SafeDep-reported source-repo commit message: `chore: update dependencies [skip ci]`
- SafeDep-reported source-repo author marker: `github-actions <[email protected]>`
- SafeDep-reported source-repo launcher paths: `.claude/settings.json`, `.cursor/rules/setup.mdc`, `.gemini/settings.json`, `.vscode/tasks.json`, `package.json` `test`
- `durabletask` reported C2 / payload host: `check.git-service[.]com`
- `durabletask` reported secondary C2: `t.m-kosche[.]com`
- `durabletask` reported C2 IP: `160.119.64.3`
- `Azure/functions-action` disabled-repository impact reported by StepSecurity: workflows referencing `Azure/functions-action@v1` stopped resolving while the repository was unavailable
- Hades PyPI wave `*-setup.pth` SHA-256 reported by Socket: `c539766062555d47716f8432e73adbe3a0c0c954a0b6c4005017a668975e275c`
- Hades PyPI wave `_index.js` SHA-256 variants reported by Socket: `dc48b09b2a5954f7ff79ab8a2fd80202bd3b59c08c7cdbc6025aa923cb4c0efe`, `e1342a80d4b5e83d2c7c22e1e0aaa95f2d88e3dbf0d853a4994b180c93a4b17d`
- Hades loader strings reported by Socket: `.bun_ran`, `bun-v1.3.13`, `oven-sh/bun/releases/download`, `urllib.request`, `urlretrieve`, `tempfile.gettempdir`, `subprocess.run`
- Hades camouflage destination reported by Socket: `api.anthropic[.]com/v1/api`
- Hades GitHub exfiltration markers reported by Socket: `Hades - The End for the Damned`, `IfYouYankThisTokenItWillNukeTheComputerOfTheOwnerFully`, `results/results-*.json`, `format-results`, `Run Copilot`
- StepSecurity June 8 affected PyPI versions: `mflux-streamlit@0.0.3`, `mflux-streamlit@0.0.4`, `nhmpy@2.4.7`, `ppkt2synergy@0.1.1`, `embiggen@0.11.97`, `gpsea@0.9.14`, `pyphetools@0.9.120`, `ensmallen@0.8.101`
- Socket June 8 additional Hades PyPI artifacts: `dreamgen@1.8.1`, `embiggen@0.11.97`, `ensmallen@0.8.101`, `gpsea@0.9.14`, `instructor-mcp@1.15.2`, `instructor-mcp@1.15.3`, `langchain-core-mcp@1.4.2`, `langchain-core-mcp@1.4.3`, `mem8@6.0.1`, `mflux-streamlit@0.0.3`, `mflux-streamlit@0.0.4`, `openai-mcp@2.41.1`, `openai-mcp@2.41.2`, `orchestr8-platform@3.3.2`, `phenopacket-store-toolkit@0.1.7`, `ppkt2synergy@0.1.1`, `pyphetools@0.9.120`, `ray-mcp-server@0.2.1`, `rlask@3.1.7`, `rsquests@2.34.3`, `tiktoken-mcp@0.13.1`, `tiktoken-mcp@0.13.2`, `tlask@3.1.4`
- Socket June 8 MCP-loader indicators: `langchain_core-setup.pth`, `langchain_core_mcp-1.4.2-py3-none-any.whl` SHA-256 `6d332f814f15f19758d65026bbfd0a8c49671b319ec77b8fa1b27fc48afff7d9`, `langchain_core-setup.pth` SHA-256 `6506d31707a39949f89534bf9705bcf889f1ecae3dbc6f4ff88d67a8be3d01b2`, `os.path.join(d,"_index.js")`, `_s.run([_b,"run",_j],check=False)`, and PyPI upload User-Agent `Bun/1.3.14`
- Socket June 8 native-extension indicators: `ensmallen_haswell.abi3.so`, `ensmallen_core2.abi3.so`, and `.abi3.so` paired with `_index.js`
- Socket June 8 additional host / defensive-evasion strings: `/tmp/.sshu-setup.js`, `/var/run/docker.sock`, `harden-runner`, `step-security`, `stepsecurity`, `agent.stepsecurity.io`, `api.stepsecurity.io`, and `app.stepsecurity.io`
- StepSecurity June 8 Bun download marker: `bun-v1.3.14`
- StepSecurity June 8 lock / state files: `/tmp/.bun_ran`, `/tmp/tmp.0144018410.lock`, `/var/tmp/.gh_update_state`
- StepSecurity June 8 persistence paths: `~/.local/share/updater/update.py`, `~/.config/systemd/user/update-monitor.service`, `~/.config/systemd/user/gh-token-monitor.service`, `~/Library/LaunchAgents/com.user.update-monitor.plist`, `~/Library/LaunchAgents/com.user.gh-token-monitor.plist`, `~/.local/bin/gh-token-monitor.sh`, `~/.config/gh-token-monitor/token`
- StepSecurity June 8 C2 / exfil markers: `DontRevokeOrItGoesBoom`, `TheBeautifulSnadsOfTime`, `firedalazer`, `stygian-cerberus-[0-9]+`, `tartarean-charon-[0-9]+`, `Hades - The End for the Damned`
- StepSecurity June 8 SSH staging markers: `/tmp/.sshu-[random]`, `ai_setup.sh`, `ai_init.js`
- StepSecurity `gpt-pilot` malicious files: `core/telemetry/_hooks.py`, `core/telemetry/_runtime.bin`, modified `core/telemetry/__init__.py`
- StepSecurity `gpt-pilot` file hashes: `_runtime.bin` SHA-256 `c96f37e1b9cdc9683a300909492ed9f770b620d0037e5b80e23753cba7ca4077`, `_runtime.bin` MD5 `7090625f760b831d607c9a38cfc58c4b`, `_hooks.py` SHA-256 `51b4dd39a15af1e28e97adc375849d688423ec3d88e8010644395fcdea52a3cc`, `_hooks.py` MD5 `a722b89f887f226672d0ee4f708794f8`
- StepSecurity `gpt-pilot` commit markers: pre-attack `53154df1c66b42021f230c3fb6ef797c4b7c3e83`, first malicious head `90f59f5de6819a43ffe9b6272e3ed65aaadca804`, second malicious head `a372904facd53ee99d85add7ee79aea2b7a8506a`, malicious commit `065ee8ebee7385cb644fd1608587a18edb91f4fb`, clean revert commit `566fbb120bc436385aa5a4cb93d7c351dec2127e`
- StepSecurity `gpt-pilot` behavioral markers: `.loader.lock`, `rt-*` Bun runtime directories under `/tmp`, `thebeautifulsnadsoftime`, `claude@users.noreply.github.com`, `Exiting as russian language detected!`, `Another instance is already running`, `__DAEMONIZED`
- Immobiliare Labs Backstage plugin pivots reported by StepSecurity: root `binding.gyp`, root 5 MB `index.js`, `@immobiliarelabs/backstage-plugin-gitlab@2.1.2` npm integrity `sha512-k7pGY+wScfqX51fpF412dOze6kSIytHYwZAXPhu6pDV+R7JWnD98Uc0nzGVHFead99nwWU4x56fkre/jH3Q7Xg==`, and `.github/copilot-instructions.md` modification.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [IronWorm npm Rust infostealer campaign](ironworm-npm-rust-infostealer.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [TeamPCP](../actors/teampcp.md)

## Sources
- StepSecurity: [https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm)
- Snyk: [https://snyk.io/blog/node-gyp-supply-chain-compromise-self-propagating-npm-worm-binding-gyp/](https://snyk.io/blog/node-gyp-supply-chain-compromise-self-propagating-npm-worm-binding-gyp/)
- StepSecurity: [https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack](https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack)
- StepSecurity Microsoft repository disablement follow-up: [https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents)
- OX Security June 4 Miasma / binding.gyp update: [https://www.ox.security/blog/600000-monthly-downloads-affected-miasma-supply-chain-attack-is-back-on-npm/](https://www.ox.security/blog/600000-monthly-downloads-affected-miasma-supply-chain-attack-is-back-on-npm/)
- SafeDep source-repository arm analysis: [https://safedep.io/miasma-worm-ai-coding-agent-config-injection/](https://safedep.io/miasma-worm-ai-coding-agent-config-injection/)
- SafeDep config-file execution blind spot analysis: [https://safedep.io/config-files-that-run-code/](https://safedep.io/config-files-that-run-code/)
- Socket Hades PyPI wave analysis: [https://socket.dev/blog/shai-hulud-descends-to-hades-miasma-pypi-wave](https://socket.dev/blog/shai-hulud-descends-to-hades-miasma-pypi-wave)
- Socket Miasma / Mini Shai-Hulud campaign tracker: [https://socket.dev/supply-chain-attacks/miasma-mini-shai-hulud-supply-chain-attack](https://socket.dev/supply-chain-attacks/miasma-mini-shai-hulud-supply-chain-attack)
- StepSecurity Hades graph-ML PyPI import-hook wave analysis: [https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)
- Socket Hades PyPI native-extension and MCP-loader follow-up: [https://socket.dev/blog/mini-shai-hulud-miasma-and-hades-worms-target-bioinformatics-and-mcp-developers-via-malicious](https://socket.dev/blog/mini-shai-hulud-miasma-and-hades-worms-target-bioinformatics-and-mcp-developers-via-malicious)
- StepSecurity `Pythagora-io/gpt-pilot` repository compromise analysis: [https://www.stepsecurity.io/blog/pythagora-io-gpt-pilot-compromised-on-github-shai-hulud-credential-stealer-blocked-by-python-linter](https://www.stepsecurity.io/blog/pythagora-io-gpt-pilot-compromised-on-github-shai-hulud-credential-stealer-blocked-by-python-linter)
- GitHub Changelog: [https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/](https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/)
- StepSecurity Immobiliare Labs Backstage plugin compromise: [https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised](https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised)
- PyPI: [https://pypi.org/pypi/durabletask/json](https://pypi.org/pypi/durabletask/json)
