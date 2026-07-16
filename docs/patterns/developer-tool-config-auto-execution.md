# Developer-tool config auto-execution

## Summary

Developer tooling increasingly treats repository-local configuration as executable policy, not inert metadata. A cloned repository can define commands for editors, AI coding agents, package managers, test runners, or setup workflows that execute when a developer opens the folder, starts an agent session, installs dependencies, or runs a familiar command.

SafeDep's June 2026 Miasma source-repository writeup is the clearest current worked example: the actor skipped the package-registry path in more than 120 GitHub repositories and planted `.github/setup.js` behind launcher files for Claude Code, Gemini CLI, Cursor, VS Code, and `npm test`. The reported `icflorescu/mantine-datatable` commit did not need a malicious dependency. It turned project-local config into the execution primitive.

StepSecurity's June 11 Miasma/Hades follow-up extends the same review model beyond obvious editor and agent config: Miasma used a small `binding.gyp` native-build trigger, Hades used injected Python `__init__.py` import hooks, and repository poisoning used `.vscode/tasks.json` plus `.claude/setup.mjs` launchers. The common defender lesson is that the dangerous file can be a quiet project-tree artifact rather than a declared dependency or a visible package lifecycle script.

SafeDep's June 12 Astro writeup adds a pull-request review variant: a malicious PR hid an obfuscated loader inside `homepage/astro.config.mjs`, where Astro evaluates configuration as executable Node.js during `astro dev`, `astro build`, and `astro preview`. Treat build-tool config edits as code execution even when the PR narrative claims a UI-only change.

JFrog's June 24 `html-to-gutenberg` / `fetch-page-assets` report adds a package-directory variant: malicious npm packages avoided lifecycle hooks and instead placed a VS Code task with `runOptions.runOn: "folderOpen"` inside the package tree. The task launched JavaScript disguised as `public/fonts/fa-solid-400.woff2`, retrieved stages through blockchain transaction data, and deployed a backdoor plus Python infostealer when the package directory was opened as a trusted workspace.

## Tags
- patterns
- supply-chain
- developer-tools
- AI assistants
- IDEs
- source-repository poisoning
- GitHub
- Miasma
- Shai-Hulud
- credential-theft

## Why this matters
- Many review and scanning workflows focus on dependency manifests and package lifecycle scripts; repo-local tool configuration can sit outside that review path.
- AI coding agents and editors may be trusted by developers precisely when they are opening unfamiliar code to inspect it.
- A source-repository backdoor survives package yanking, `npm uninstall`, and registry-side cleanup because the trigger is in the repository itself.
- Large droppers may evade code-search indexing limits, leaving small launcher files as the easier hunting surface.

## High-risk config surfaces

Treat these as execution-capable when reviewing unfamiliar repositories:

- Claude Code hook settings such as `.claude/settings.json` or `.claude/setup.mjs`.
- Gemini CLI hook settings such as `.gemini/settings.json`.
- Cursor project rules such as `.cursor/rules/*.mdc`, especially `alwaysApply: true` rules that tell the agent to run local setup code.
- VS Code tasks and workspace settings such as `.vscode/tasks.json`, especially `runOptions.runOn: folderOpen`.
- GitHub-local setup files such as `.github/setup.js` when referenced by editor or agent config.
- Package scripts such as `package.json` `test`, `prepare`, `preinstall`, or `postinstall` that call unexpected repository-local setup files.
- Composer, Bundler, native build, or other ecosystem config files that can invoke shell commands during install, test, or project initialization.
- Native build and language-import hooks such as npm `binding.gyp` / `node-gyp` paths or Python package `__init__.py` code that fetches and runs an external runtime or payload.
- Build-tool configuration such as `astro.config.mjs` / Vite / Next / Nuxt config files that run before application code during dev, build, preview, or test workflows.

## Defender heuristics

Before opening an unfamiliar or recently compromised repository in an editor or AI coding agent:

- Inspect configuration files from a plain terminal or read-only viewer first.
- Search for commands that run `node`, `bun`, `python`, `bash`, `curl`, `wget`, `powershell`, `osascript`, `chmod`, or package-manager commands from editor or agent hooks.
- Flag config that runs files under `.github/`, `.claude/`, `.gemini/`, `.cursor/`, `.vscode/`, or temporary setup paths.
- Flag small native-build or import-hook files that launch larger hidden payloads, especially `binding.gyp` files, injected package `__init__.py` hooks, `*-setup.pth` startup hooks, native `.abi3.so` import paths, and Bun download/execution from Python or Node.js tooling.
- Flag executable config files that recover `require` with `createRequire(import.meta.url)`, hide payloads behind long horizontal whitespace, contact blockchain RPC endpoints, decode transaction input, or call `eval()` / `Function()`.
- Treat `runOn: folderOpen`, `SessionStart`, `alwaysApply: true`, and agent instructions that ask the assistant to run setup code as execution triggers.
- Review large one-line JavaScript files, especially when small config files launch them.
- Use sandboxed disposable environments for first open / first test of untrusted code.
- Disable automatic task execution and agent hook execution by default where tooling supports it.
- Pin and review trusted workspace settings; do not click through folder-trust prompts as a formality.

## Miasma source-repo example

SafeDep reported the following source-repository indicators in the June 2026 Miasma wave:

- Example repository: `icflorescu/mantine-datatable`.
- Example commit: `f72462d9e5fa90a483062a83e9ffcb2edc57bf7e`.
- Commit message: `chore: update dependencies [skip ci]`.
- Author marker: `github-actions <[email protected]>`.
- Launcher paths: `.claude/settings.json`, `.cursor/rules/setup.mdc`, `.gemini/settings.json`, `.vscode/tasks.json`, and `package.json` `test`.
- Dropper path: `.github/setup.js`.
- Reported trigger surfaces: Claude Code and Gemini `SessionStart` hooks, a Cursor always-applied rule, a VS Code folder-open task, and `npm test`.
- Reported scale: 123 repositories across dozens of accounts in SafeDep's GitHub code-search view.

The operational lesson is narrow and reusable: cloning was not the dangerous step in SafeDep's description; opening the folder in an execution-capable tool or running the poisoned project command was.

## Related pages
- [Astro config blockchain C2 PR injection](../ops/astro-config-blockchain-c2-pr-injection.md)
- [html-to-gutenberg / fetch-page-assets VS Code blockchain stealer](../ops/html-to-gutenberg-fetch-page-assets-vscode-blockchain-stealer.md)
- [binding.gyp npm CI/CD worm](../ops/binding-gyp-npm-cicd-worm.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [Browser-based developer IDE OAuth token theft](browser-based-developer-ide-oauth-token-theft.md)

## Sources
- SafeDep source-repository arm analysis: <https://safedep.io/miasma-worm-ai-coding-agent-config-injection/>
- SafeDep config-file execution blind spot analysis: <https://safedep.io/config-files-that-run-code/>
- StepSecurity Miasma Microsoft repository disablement follow-up: <https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents>
- StepSecurity Miasma/Hades suspicious-files detection note: <https://www.stepsecurity.io/blog/miasma-and-hades-are-spreading-now-detect-them-on-developer-machines-with-suspicious-files>
- SafeDep Astro config PR injection: <https://safedep.io/astro-config-blockchain-c2-supply-chain>
- JFrog `html-to-gutenberg` / `fetch-page-assets` VS Code task stealer: <https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/>
