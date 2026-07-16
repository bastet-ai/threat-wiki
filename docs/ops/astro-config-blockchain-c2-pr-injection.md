# Astro config blockchain C2 PR injection

## Summary

SafeDep reported a malicious pull request against `AsimRaza10/Understand-Anything` that hid an obfuscated loader inside `homepage/astro.config.mjs` while presenting the change as a benign dashboard path-filter fix. The pull request was not merged at the time of SafeDep's writeup, but it is a durable example of a source-repository supply-chain lane: a build-tool configuration file executes during `astro dev`, `astro build`, and `astro preview`, so any developer workstation, CI job, or preview builder that checked out and ran the branch should be treated as exposed.

SafeDep ties the payload fingerprints to the DPRK-attributed PolinRider campaign documented by OpenSourceMalware, while noting that this pull-request delivery path differs from earlier PolinRider developer-targeting lures such as poisoned npm packages, weaponized take-home tests, and malicious VS Code tasks.

## Tags
- ops
- operations
- supply-chain
- GitHub
- pull requests
- source-repository poisoning
- Astro
- JavaScript
- blockchain C2
- developer machines
- CI/CD
- DPRK
- PolinRider

## Why this matters
- Build-tool config is executable code. An `astro.config.mjs` edit can run before application code and outside dependency-manifest review.
- A plausible pull-request narrative can hide a build-pipeline payload even when no dependency is changed.
- The reported payload used horizontal whitespace to push obfuscated code out of GitHub's visible diff pane, making static PR review weaker if reviewers do not inspect full lines or raw files.
- Public blockchain infrastructure can act as a resilient second-stage relay: SafeDep reported Tron account data resolving to Binance Smart Chain transaction input that decrypted into JavaScript executed by `eval()`.

## Reported chain
1. A contributor pull request claimed to fix a dashboard path-finder dropdown and included fabricated-looking implementation and test-plan language.
2. The actual diff changed `.gitignore` and `homepage/astro.config.mjs`, not the React component areas implied by the PR text.
3. `.gitignore` suppressed Windows batch-script names such as `branch_structure.json`, `temp_auto_push.bat`, and `temp_interactive_push.bat`, which SafeDep interpreted as consistent with automated PR submission tooling.
4. `homepage/astro.config.mjs` recovered CommonJS `require` in an ES module context with `createRequire`, then appended an obfuscated IIFE after long horizontal whitespace on the same line as the existing config close.
5. The first-stage resolver contacted TronGrid, decoded a transaction-derived Binance Smart Chain transaction hash, fetched BSC transaction input from public RPC endpoints, split and XOR-decrypted the transaction data, and executed the resulting JavaScript.
6. SafeDep reported active next-stage BSC transaction hashes including `0x80a1148ee589125bc1e57d36abac9f08089b2990d9372be3a33a1f057ad1ef89` and `0xa896af4f2876df59af1e705fb75031630ebd37fa89659a9896be4d3da8c87f02`, plus related hash `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e`.

## Defender heuristics

### Pull-request review
- Treat edits to build configuration (`astro.config.mjs`, Vite/Next/Nuxt config, package-manager scripts, CI YAML, editor task files) as execution-capable even when the PR claims a UI or documentation change.
- Compare the PR description with the touched files. A change claiming to fix a React component but only modifying config and ignore files is a high-signal mismatch.
- Review raw files or use diff tooling that shows horizontally hidden content; do not rely only on GitHub's clipped visual diff for long lines.
- Flag unexpected `createRequire` in `.mjs` configuration files, especially when combined with network calls, obfuscation, `Buffer.from(..., 'hex')`, `eval()`, `Function()`, `child_process`, or dynamically decoded strings.

### Endpoint and CI triage
- If any environment ran `astro dev`, `astro build`, or `astro preview` from the reported branch, treat the host as compromised.
- Rotate credentials reachable from that environment after isolating and collecting evidence: GitHub tokens, registry tokens, cloud keys, CI secrets, SSH keys, and application secrets.
- Review outbound logs for SafeDep-reported IPs `166.88.54[.]158`, `198.105.127[.]210`, and `23.27.202[.]27`, plus public TronGrid / Binance Smart Chain RPC access from unexpected build contexts.
- Search repositories and PR branches for long-line whitespace padding in executable config files, `createRequire(import.meta.url)`, blockchain RPC endpoints, Tron address `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP`, and XOR-decryption / transaction-input decoding logic.

## Relationship to other coverage
- Socket's July 2026 [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md) reporting shows the same broader DPRK-linked activity moving beyond one pull request into npm, Packagist, Go modules, and a Chrome extension, with repeated use of hidden JavaScript loaders, Git history rewriting, and VS Code task execution.
- This is a source-repository / pull-request injection operation, not a package-registry worm like [Mini Shai-Hulud](mini-shai-hulud-npm-pypi-worm-campaign.md).
- The broader reusable pattern is [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md): repository-local config can execute when a developer or CI system opens, builds, previews, or tests a project.
- Keep attribution caveated to SafeDep's linkage to OpenSourceMalware's PolinRider reporting unless additional primary sources publish operator or infrastructure confirmation.

## Sources
- [SafeDep](https://safedep.io/astro-config-blockchain-c2-supply-chain)
