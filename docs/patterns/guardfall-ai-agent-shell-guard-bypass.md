# GuardFall AI-agent shell-guard bypass

## Summary
Adversa AI described **GuardFall**, a class of shell-command guard bypasses affecting open-source AI coding and computer-use agents. The core issue is architectural: many agents inspect the raw command string with regex or denylist checks, but then hand the command to `bash -c`, where shell parsing, quote removal, command substitution, `$IFS`, encoded payloads, and utility flags can change what actually executes.

Adversa says the research began with a NousResearch Hermes Agent approval-gate bypass and then expanded to ten other popular open-source agents. In its June 30, 2026 survey, ten of eleven reviewed tools left the agent-to-shell boundary exploitable in at least one common configuration; Continue was identified as the reference design that most directly canonicalizes/parses command intent before approval in its default IDE mode. The report frames the issue as a class, not a single CVE, and states that no public exploitation was reported at publication time.

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
- Adversa AI: https://adversa.ai/blog/opensource-ai-coding-agents-shell-injection-vulnerability/
- The Hacker News summary: https://thehackernews.com/2026/06/guardfall-exposes-open-source-ai-coding.html
- Hermes Agent issue referenced by Adversa/THN: https://github.com/NousResearch/hermes-agent/issues/36846
