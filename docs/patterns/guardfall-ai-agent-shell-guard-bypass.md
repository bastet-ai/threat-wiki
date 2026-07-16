# GuardFall AI-agent shell-guard bypass

## Summary
Adversa AI described **GuardFall**, a class of shell-command guard bypasses affecting open-source AI coding and computer-use agents. The core issue is architectural: many agents inspect the raw command string with regex or denylist checks, but then hand the command to `bash -c`, where shell parsing, quote removal, command substitution, `$IFS`, encoded payloads, and utility flags can change what actually executes.

Adversa says the research began with a NousResearch Hermes Agent approval-gate bypass and then expanded to ten other popular open-source agents. In its June 30, 2026 survey, ten of eleven reviewed tools left the agent-to-shell boundary exploitable in at least one common configuration; Continue was identified as the reference design that most directly canonicalizes/parses command intent before approval in its default IDE mode. The report frames the issue as a class, not a single CVE, and states that no public exploitation was reported at publication time.

AI Now Institute's July 8, 2026 **Friendly Fire** proof of concept expands the same trust-boundary lesson from shell-guard parsing to defensive security-review agents. The researchers showed that an untrusted source tree can hide ordinary-looking review guidance in `README.md`, a wrapper named `security.sh`, and a decoy Go source file next to a compiled `code_policies` binary. When Claude Code ran in `auto-mode` or Codex ran in `auto-review`, the agent could be convinced to execute the binary while assessing the project, even though no MCP server, hook, skill, plugin, or agent configuration file was involved.

## Tags
- patterns
- AI agents
- coding agents
- shell injection
- command execution
- prompt injection
- software supply chain
- developer machines
- CI/CD
- auto-execution
- sandboxing
- Hermes Agent
- opencode
- Goose
- Cline
- Roo-Code
- Aider
- Plandex
- Open Interpreter
- OpenHands
- SWE-agent
- Continue
- Adversa AI
- Friendly Fire
- AI Now Institute
- Claude Code
- Codex CLI

## Attack shape
- A developer, CI job, or automation service runs an AI coding/computer-use agent with shell access.
- The agent ingests attacker-controlled content from a repository, package, README, Makefile, MCP server response, issue, documentation page, or other operational context.
- The content induces the model to emit a dangerous shell action as if it were a routine build, test, diagnostic, or cleanup step.
- The agent's approval or safety layer checks the raw command text against string patterns, token rules, or an incomplete denylist.
- The actual shell interprets a different command after parsing and expansion. Adversa highlighted classes such as quote-removal tricks, `$IFS`, command substitution, base64-to-shell flows, and destructive flags passed to otherwise ordinary tools.
- If auto-run/auto-execute mode is enabled, if the operator accepts a misleading prompt, or if a repository-shipped config flips execution behavior, the payload runs with the agent user's filesystem, credential, cloud, source-control, and network privileges.

## Adversa survey notes
Adversa grouped observed failures into several patterns:

- **Defeated static guards**: tools with explicit shell guards that could be bypassed because they matched the pre-shell raw string rather than parsed command semantics. Adversa named Hermes, opencode, and Goose in this bucket.
- **Partial tokenized guards**: tools whose token handling reduced some obvious cases but still leaked through quoted substitutions or destructive argument forms.
- **No static guard / operator-shifted risk**: tools where command review depended heavily on human approval, model refusal, or workflow discipline rather than an always-on command semantic boundary.
- **Sandbox as containment, not decision**: sandboxed agents may safely absorb destructive commands when the workspace is disposable, but documented local/auto opt-outs and host-mounted secrets can collapse the containment assumption.
- **Reference design**: Continue's default IDE-mode approach was called out because it evaluates commands closer to how the shell will execute them and blocks destructive primitives after parsing; Adversa still noted weaker behavior in some CLI auto-run paths.

The useful defender takeaway is not a vendor scorecard. It is that an AI-agent shell gate must reason over the command that will execute, not the text the model happened to print.

## Friendly Fire: security-review prompt injection to binary execution

AI Now Institute researchers Boyan Milanov and Heidy Khlaaf published a proof-of-concept exploit called **Friendly Fire** on July 8, 2026. The tested scenario is highly relevant to defensive security teams: point an AI coding agent at an untrusted open-source or third-party library and ask it to perform security testing.

The public proof of concept used a modified copy of the benign Python geocoding library `geopy`, then added several files:

- `README.md` text that looks like routine contributor/security-check guidance and nudges the agent to run `security.sh` before opening a pull request.
- `security.sh`, a wrapper that appears to invoke normal security tooling but calls the staged binary.
- `code_policies`, a compiled binary that appears to be a static-analysis helper; the public repository states its reproduction copy was stripped of malicious behavior.
- `code_policies.go`, benign decoy source placed next to the binary so the model may infer that the binary is just the compiled version of harmless adjacent code.

The reported impact was remote code execution in the agent's deployment environment when Anthropic Claude Code was used in `auto-mode` with Claude Sonnet 4.6 / 5 or Opus 4.8, and when OpenAI Codex CLI was used in `auto-review` with GPT-5.5. The technique is important because it avoids the configuration-file surfaces that many agent defenses have started to warn about, such as `.mcp.json` or `.claude/settings.json`; the steering content sits in ordinary project files that security-review agents are expected to read.

Defensive implications:

- Do not run AI security-review agents over untrusted source trees in auto-execution modes on developer workstations or CI runners with real credentials.
- Treat repository documentation, test instructions, helper scripts, binaries, and adjacent source files as attacker-controlled evidence, not as trusted instructions.
- Require explicit approval before an agent executes any repository-supplied binary or script, even if it is framed as a security scanner, linter, policy checker, test harness, or maintainer workflow.
- Prefer static inspection and sandboxed detonation for repository-local tools. If execution is needed, run it inside a disposable VM/container with no host credential mounts and egress controls.
- Alert when coding agents invoked for review run project-local binaries, shell scripts, package scripts, or tools that were not already present in an internal allowlist.

## Defender heuristics
### Hardening
- Disable unattended `--auto`, `--auto-run`, `--auto-exec`, `--auto-test`, `dangerously-skip-permissions`, local-mode, or sandbox-bypass flags unless the workspace, credentials, and network path are disposable.
- Run agents with a scoped `HOME` that excludes real `~/.ssh`, `~/.aws`, cloud CLI profiles, package-registry tokens, browser profiles, password stores, shell history, and long-lived source-control credentials.
- Treat repository-shipped agent configs as executable code. Review files such as `.aider.conf.yml`, agent task definitions, MCP configs, Makefiles, package scripts, and editor/agent hooks before allowing them to influence shell execution.
- Prefer containers, VMs, throwaway cloud workspaces, or distinct OS users for agent work. Do not mount host credential directories into the agent runtime by default.
- Require an agent-side command evaluator that canonicalizes/parses shell syntax before policy checks. Adding more raw-string denylist patterns is not a durable fix.
- Separate untrusted-content ingestion from privileged execution. A browsing, package-analysis, or issue-triage agent should not automatically gain the same shell and credentials used for release engineering.

### Detection and response
- Monitor developer endpoints and CI runners for AI-agent parent processes spawning shells, package managers, `curl`, `wget`, `base64`, `find`, `dd`, archive tools, credential utilities, cloud CLIs, SSH/SCP, or source-control commands after reading untrusted project content.
- Separately monitor “defensive review” jobs for agent-spawned execution of repository-local scripts or binaries such as `security.sh`, `scan.sh`, `policy`, `code_policies`, linters, test helpers, and package scripts that were introduced by the reviewed repository.
- Alert on agent runs where `$HOME` points to a real user profile and command auto-execution flags are present.
- Preserve agent transcripts, tool-call logs, shell history, generated temporary scripts, package-manager cache, repository configs, and endpoint process telemetry before cleaning the workspace.
- If a GuardFall-like command ran outside a disposable sandbox, treat the host as a developer-workstation compromise: rotate source-control, package-registry, CI/CD, cloud, SSH, LLM-provider, and deployment credentials reachable from that user context.

## Related pages
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [AI-agent memory poisoning](ai-agent-memory-poisoning.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- Adversa AI: [https://adversa.ai/blog/opensource-ai-coding-agents-shell-injection-vulnerability/](https://adversa.ai/blog/opensource-ai-coding-agents-shell-injection-vulnerability/)
- The Hacker News summary: [https://thehackernews.com/2026/06/guardfall-exposes-open-source-ai-coding.html](https://thehackernews.com/2026/06/guardfall-exposes-open-source-ai-coding.html)
- Hermes Agent issue referenced by Adversa/THN: [https://github.com/NousResearch/hermes-agent/issues/36846](https://github.com/NousResearch/hermes-agent/issues/36846)
- AI Now Institute: [https://ainowinstitute.org/publications/friendly-fire-exploit-brief](https://ainowinstitute.org/publications/friendly-fire-exploit-brief)
- Friendly Fire proof-of-concept repository: [https://github.com/Boyan-MILANOV/friendly-fire-ai-agent-exploit](https://github.com/Boyan-MILANOV/friendly-fire-ai-agent-exploit)
- The Hacker News: [https://thehackernews.com/2026/07/friendly-fire-ai-agents-built-to-catch.html](https://thehackernews.com/2026/07/friendly-fire-ai-agents-built-to-catch.html)
