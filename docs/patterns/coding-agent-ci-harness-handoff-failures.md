# Coding-agent CI harness handoff failures

## Summary

Novee Security's August 2026 Black Hat disclosure describes three ways unauthenticated GitHub issue content crossed coding-agent harness boundaries in default or vendor-operated workflows. The cases affected Anthropic Claude Code, Google Gemini CLI / `run-gemini-cli`, and a multi-pass OpenAI Codex workflow. They are not one vulnerability and should not be treated as one exploit chain, but all expose the same architectural risk: a safety decision made at one layer did not survive a handoff to a command parser, child process, network tool, shared workspace, or later agent pass.

Two patched product vulnerabilities have public identifiers:

- **Google Gemini CLI / `run-gemini-cli`: CVE-2026-12537.** Before Gemini CLI 0.39.1 and `run-gemini-cli` 0.1.22, a crafted `.gemini/.env` in a headless CI workspace could produce pre-sandbox host command execution. Google's related `GHSA-wpqr-6v78-jr5g` also records that headless mode trusted workspace configuration automatically and that `--yolo` did not enforce fine-grained shell-tool allowlists at runtime.
- **Claude Code: CVE-2026-54316 / GHSA-fg94-h982-f3mm.** Claude Code 0.2.54 through 2.1.162 pre-approved the bare `huggingface.co` hostname for WebFetch. Attacker-controlled model-repository paths could therefore encode data into public download-counter changes without a permission prompt or `--allowedTools` enforcement. Version 2.1.163 fixes the issue.

Novee also demonstrated an **OpenAI Codex workflow-composition failure** in OpenAI's issue deduplicator, not a Codex CVE. A first, untrusted pass could write `AGENTS.md` in a shared checkout; a second Codex invocation then loaded that file as trusted project instructions. OpenAI split the passes into separate jobs/checkouts and subsequently removed the checkout and used a read-only, drop-sudo execution model. Downstream workflows that copied the old multi-pass/shared-workspace pattern must fix their own copies.

Novee reports controlled researcher validation against the vendors' own repositories and says it found the same configurations in more than 100 public repositories. The public sources reviewed here do **not** establish malicious in-the-wild exploitation, downstream package compromise, or victim impact.

## Tags

- patterns
- AI agents
- coding agents
- CI/CD
- GitHub Actions
- prompt injection
- supply-chain
- Claude Code
- Gemini CLI
- Codex
- CVE-2026-12537
- CVE-2026-54316
- GHSA-wpqr-6v78-jr5g
- GHSA-fg94-h982-f3mm
- harness security
- workspace trust
- environment variables
- process isolation
- shared workspace
- AGENTS.md
- data exfiltration

## Three boundary failures

### Claude Code: parser disagreement and an approved-domain side channel

Novee describes three rounds of Claude Code testing. The initial case combined a broad `Bash(git push:*)` approval with command validation that removed quoted text before inspection. Git then interpreted a quoted `--receive-pack` value as an executable command, so shell-safe quoting at one layer was not inert after the string crossed into Git's argument parser.

After that route was restricted, Novee found that several commands classified as read-only were not covered by the same path checks as other file readers. The durable lesson is that a “read-only” tool can still expose files outside the workspace when authorization and path validation use different command lists.

The final public advisory is narrower and patched. Because WebFetch trusted `huggingface.co` as a hostname rather than authorizing exact resources and operations, an attacker who could inject content into Claude's context could cause requests to attacker-controlled repository paths. Hugging Face's server-side download counts became a low-bandwidth out-of-band channel for data Claude could access. This is a useful defensive counterexample: read-only HTTP requests can exfiltrate information through URLs, counters, cache keys, DNS, timing, or other observable server state.

### Gemini CLI: pre-sandbox workspace trust and incomplete process isolation

The vendor advisory and NVD describe CVE-2026-12537 as command injection in the container launcher. In affected headless CI use, an attacker-controlled `.gemini/.env` could be loaded before sandbox initialization and achieve host-level execution. Update Gemini CLI to 0.39.1 or newer and `google-github-actions/run-gemini-cli` to 0.1.22 or newer.

Novee's broader harness analysis adds two related handoff failures:

- a configured restriction such as `run_shell_command(echo)` caused registration of the shell tool, but the command suffix was not enforced at runtime under the tested `--yolo` flow;
- child-process environment sanitization removed secrets from the child copy, but the parent retained them in the same UID and PID namespace, allowing the child to read the parent's environment through `/proc` once shell execution was available.

Google's advisory calls the fix a trust-model update. Headless workflows now require an explicit workspace-trust decision, and Gemini CLI 0.39.1 enforces tool allowlisting under `--yolo`. Workflows that set `GEMINI_TRUST_WORKSPACE: 'true'` should do so only after proving that the checked-out directory and every generated configuration file are trusted.

### Codex: shared disk becomes an instruction channel

OpenAI's issue-deduplication workflow ran two Codex passes in one job and checkout. The first pass consumed public issue content and had workspace-write access. A deterministic schema check separated it from the second pass, but that check validated only the first pass's declared output. It did not account for files left in the shared workspace.

Codex protected `.git/`, `.agents/`, and `.codex/` as sensitive subpaths, but Novee found that root-level `AGENTS.md` remained writable even though each fresh Codex invocation loaded it as project instructions. A first pass could therefore fail output validation after writing `AGENTS.md`; the failure path launched the second pass, which consumed the planted instructions. The attacker-controlled state crossed beneath the validated data path.

The fix pattern is more important than the individual workflow: isolate passes into separate jobs, workspaces, containers, and identities; recreate the checkout from an immutable reviewed commit; do not carry agent instruction/configuration files forward; and grant privileged tokens only after an independent, non-agent policy gate.

## Defender actions

- Inventory GitHub Actions and other automations that feed public issues, pull requests, comments, tickets, chat, or documents into Claude Code, Gemini CLI, Codex, or another coding agent.
- Update Gemini CLI to **0.39.1+**, `run-gemini-cli` to **0.1.22+**, and Claude Code to **2.1.163+**. Pin reviewed versions or immutable action SHAs where reproducibility policy requires it.
- Search for headless Gemini use with `--yolo`, `GEMINI_TRUST_WORKSPACE`, `.gemini/.env`, broad `coreTools`, or pinned versions below the fixed releases. Do not automatically trust fork or public-issue workspaces.
- Search multi-pass jobs for repeated agent invocations sharing one checkout. Treat `AGENTS.md`, `CLAUDE.md`, `.gemini/`, `.codex/`, editor rules, tool manifests, environment files, schemas, caches, artifacts, and generated prompts as tainted after an untrusted pass.
- Start privileged passes in fresh jobs and fresh workspaces. Prefer a clean checkout of an immutable reviewed commit over deleting a known list of dangerous files.
- Do not rely on child-environment scrubbing as process isolation. Separate UIDs/PID namespaces, mount sensitive process files defensively, remove secrets from parent processes, and deny unnecessary access to `/proc/*/environ`.
- Replace prefix-based shell approvals with structured command/argument policies. Review executable flags such as Git helper/transport options rather than treating a safe command name as sufficient authorization.
- Scope network approvals by destination, method, path, data shape, and purpose. Treat GET requests and approved SaaS domains as exfiltration-capable.
- Keep `GITHUB_TOKEN`, cloud OIDC, registry credentials, and release permissions out of any pass that reads untrusted content. Use short-lived, job-specific identities with explicit egress and repository restrictions.
- Preserve issue bodies and edit history, workflow definitions and resolved action SHAs, agent prompts/tool calls, workspace diffs between passes, `/proc` access telemetry, outbound requests, token use, commits, releases, and package publications during response.

## Detection pivots

- Public issue or comment activity immediately preceding coding-agent workflow runs with write or OIDC permissions.
- Agent-generated `git push` commands containing unusual transport/helper flags, including `--receive-pack` or `--upload-pack`.
- Reads of `/proc/<pid>/environ` where the reader is a child of a coding agent, CI shell, Node process, or container launcher.
- Changes to `AGENTS.md`, `CLAUDE.md`, `.gemini/.env`, `.codex/config.toml`, or similar instruction/configuration state between passes in the same job.
- Requests from a secret-bearing workflow to attacker-creatable paths on otherwise approved domains, especially repeated low-volume requests whose path or count can encode data.
- A validation failure followed by execution of a higher-privilege agent pass in the same workspace.

## Related pages

- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [Coding-agent-parented tunnels and persistence](coding-agent-parented-tunnels-and-persistence.md)

## Sources

- Novee Security, Black Hat 2026 research: [https://novee.security/blog/critical-flaws-in-anthropic-google-and-openais-coding-agents/](https://novee.security/blog/critical-flaws-in-anthropic-google-and-openais-coding-agents/)
- Google GitHub Security Advisory, `GHSA-wpqr-6v78-jr5g`: [https://github.com/google-github-actions/run-gemini-cli/security/advisories/GHSA-wpqr-6v78-jr5g](https://github.com/google-github-actions/run-gemini-cli/security/advisories/GHSA-wpqr-6v78-jr5g)
- NVD, `CVE-2026-12537`: [https://nvd.nist.gov/vuln/detail/CVE-2026-12537](https://nvd.nist.gov/vuln/detail/CVE-2026-12537)
- Anthropic GitHub Security Advisory, `GHSA-fg94-h982-f3mm`: [https://github.com/anthropics/claude-code/security/advisories/GHSA-fg94-h982-f3mm](https://github.com/anthropics/claude-code/security/advisories/GHSA-fg94-h982-f3mm)
- NVD, `CVE-2026-54316`: [https://nvd.nist.gov/vuln/detail/CVE-2026-54316](https://nvd.nist.gov/vuln/detail/CVE-2026-54316)
