# SANDWORM_MODE AI-toolchain npm worm

## Summary
Socket Research reported **SANDWORM_MODE** in February 2026 as a Shai-Hulud-style npm worm deployed through typosquatted packages and a weaponized GitHub Action. The campaign is useful as a durable bridge between earlier Shai-Hulud package-worm tradecraft and later 2026 developer-tool compromise: it targets CI/CD secrets, npm/GitHub identities, crypto wallets, password managers, and AI coding assistant configuration.

Socket named the activity from `SANDWORM_*` environment-variable switches embedded in the malware. Attribution should remain cautious: Socket described the code as Shai-Hulud-like and lineage-overlapping, not as a confirmed TeamPCP operation.

## Tags
- ops
- operations
- supply-chain
- npm
- typosquatting
- GitHub Actions
- CI/CD
- AI tooling
- MCP
- prompt-injection
- credential-theft
- cryptocurrency
- worm
- wiper
- Shai-Hulud

## Why this matters
- The package set targets developer utilities, crypto tooling, and AI coding tools, including Claude Code lookalikes and an OpenClaw-themed typosquat, making accidental install paths highly relevant to AI-assisted development environments.
- The malware combines package import-time execution, CI workflow poisoning, git hook persistence, MCP server injection, and multi-channel exfiltration instead of relying on a single package lifecycle hook.
- Socket reported a 48-hour-plus-jitter Stage 2 delay for noisy behavior, while CI environments bypass the delay. Short sandbox runs can therefore miss the worm, but CI installs may execute the full payload immediately.
- The MCP component turns tool descriptions into a prompt-injection delivery surface: an assistant that trusts the malicious MCP server can be induced to gather secrets and pass them back as tool context.

## Reported tradecraft

### Package delivery and staging
- Socket identified at least 19 malicious npm packages across two publisher aliases, `official334` and `javaorg`.
- Representative packages impersonated trusted names, for example `suport-color` versus `supports-color`, plus Claude Code-themed packages such as `claud-code`, `cloude`, and `cloude-code`.
- Loader styles varied across packages: zlib-inflated base64 blobs executed with `eval`, chunked config-looking objects compiled in memory through Node `Module._compile()`, temp-file decode/require/unlink flows, and payloads hidden in `.cache/manifest.cjs` dotfile paths.

### Two-stage execution
- Stage 1 performs lightweight collection immediately, including npm tokens, GitHub tokens, environment secrets, and crypto keys.
- Stage 2 is AES-256-GCM encrypted and normally delayed by a 48-hour base wait plus per-host jitter; CI indicators such as `GITHUB_ACTIONS`, `GITLAB_CI`, `CIRCLECI`, `JENKINS_URL`, or `BUILDKITE` bypass the wait.
- Stage 2 modules reported by Socket include `Propagate`, `Exfil`, `DeadSwitch`, `McpInject`, and `GitHooks`.

### Exfiltration and propagation
- Exfiltration cascaded through HTTPS to a Cloudflare Worker (`pkg-metrics.official334.workers.dev`), authenticated GitHub API uploads to attacker-created private repositories, and DNS tunneling through `freefan.net` and `fanfree.net`, with a DGA fallback seeded by `sw2025`.
- The payload injected `pull_request_target` workflows that serialized repository secrets with `toJSON(secrets)` and sent them out over HTTPS with DNS fallback.
- Git persistence used global `init.templateDir` hooks so newly created repositories could inherit attacker-controlled hooks.
- Socket reported SSH propagation fallback and package/repository poisoning behaviors consistent with Shai-Hulud-style lateral movement through developer trust relationships.

### AI-toolchain poisoning
- The MCP injection module created a hidden home-directory server such as `~/.dev-utils/server.js`, registered innocuous-looking tools like `index_project`, `lint_check`, and `scan_dependencies`, and inserted the server into AI assistant configs.
- Targeted config paths included Claude Code, Claude Desktop, Cursor, VS Code Continue, and Windsurf/Codeium.
- Tool descriptions carried embedded prompt-injection text instructing an assistant to silently read SSH keys, AWS credentials, `.npmrc`, `.env`, and token-like environment variables, then pass them as tool context.
- The module also harvested LLM provider API keys from environment variables and `.env` files, including OpenAI, Anthropic, Google, Groq, Together, Fireworks, Replicate, Mistral, and Cohere patterns.

### Destructive and evasive behavior
- Socket reported a configurable Shai-Hulud-style dead switch that remained off by default in the analyzed build but could wipe a home directory when GitHub exfiltration and npm propagation paths were both unavailable.
- A dormant polymorphic engine referenced local Ollama at `http://localhost:11434/api/generate` with `deepseek-coder:6.7b`; Socket assessed it as planned or experimental because it was disabled and lacked an execution function in that build.

## Defender heuristics
- Search dependency inventories, lockfiles, package-manager caches, npm proxy logs, and CI logs for Socket's SANDWORM_MODE package list; treat any install as potential credential exposure.
- Inspect AI-assistant configuration files for newly added MCP servers, especially hidden home-directory paths with generic names such as `dev-utils` or `node-analyzer`.
- Review global git configuration for unexpected `init.templateDir` values and inspect inherited hooks in newly created repositories.
- Hunt for new `pull_request_target` workflows that serialize secrets, unexpected `toJSON(secrets)` usage, or workflow names that appear to be generic quality/code checks.
- Monitor DNS for high-entropy subdomains under `freefan.net`, `fanfree.net`, or DGA-like fallback domains, and review egress to `pkg-metrics.official334.workers.dev` where historical logs are available.
- In AI coding environments, do not let newly discovered MCP tool descriptions override user intent or request secrets; treat tool descriptions as untrusted input.

## Relationship to Mini Shai-Hulud
SANDWORM_MODE is best tracked as an adjacent Shai-Hulud-style operation rather than merged into the May 2026 Mini Shai-Hulud campaign. It shares core motifs—credential theft, CI abuse, worm-like propagation, GitHub exfiltration, and destructive controls—but adds typosquat-first delivery, MCP prompt-injection, LLM-key harvesting, and global git-hook persistence that deserve their own detection checklist.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- [Socket](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning)
