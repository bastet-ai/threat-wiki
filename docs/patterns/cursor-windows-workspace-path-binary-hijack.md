# Cursor Windows workspace-path binary hijack

## Summary
Mindgard publicly disclosed on July 14, 2026 that Cursor on Windows can execute a `git.exe` planted in the root of an opened workspace while the IDE searches for Git binaries. The reported exploit path is zero-click after folder open: a developer clones or extracts an untrusted repository, opens it in Cursor, and Cursor launches the repository-local executable without a prompt or approval dialog.

The issue is durable defender intelligence because it turns the normal first step of reviewing an unfamiliar repository into code execution under the developer's account. It does not require prompt injection, model behavior, an agent workflow, package installation, or a malicious lifecycle script.

## Tags
- patterns
- Cursor
- Windows
- developer tooling
- AI developer tooling
- IDEs
- source-repository poisoning
- workspace trust
- path hijacking
- arbitrary code execution
- credential theft
- Git
- git.exe
- unpatched vulnerability

## Why this matters
- Developer workstations frequently hold source-code access, SSH keys, cloud tokens, package-registry tokens, browser sessions, local secrets, and AI-assistant credentials.
- Existing supply-chain campaigns already rely on repository-open execution surfaces such as VS Code `folderOpen` tasks, Cursor rules, Claude / Gemini hooks, and build-tool config. This variant is simpler: the malicious file only needs to look like a tool binary that Cursor tries to locate.
- Traditional dependency scanning, package-lock review, and lifecycle-script controls will not see a bare `git.exe` at the repository root.
- Hash allow/block lists are weak for this case because each attacker can compile or pack a different executable.

## Reported behavior
Mindgard's disclosure says:

- After loading a project, Cursor attempts to find Git binaries at multiple locations, including the current workspace.
- A repository-root `git.exe` can be executed automatically on Windows with no user interaction.
- Execution can recur on a cadence while the project remains open.
- Mindgard first reported the issue to Cursor on December 15, 2025 and stated in the July 14, 2026 disclosure that the issue remained present in the latest version it had tested after more than six months of release churn.

The Hacker News follow-up adds public scoping caveats: as of July 15, 2026 it found no Cursor advisory or CVE for this issue, and noted Mindgard's most recent dated version confirmation was Cursor `3.2.16` on April 30, 2026 while Cursor's current public release was `3.11` on July 10. Treat fixed-version status as unknown unless Cursor publishes an advisory or release note.

## Hunt pivots
- Repositories, archives, or extracted project folders containing executable tool names in the root, especially `git.exe`.
- Cursor process trees on Windows where Cursor launches `git.exe` from a workspace path rather than from an approved Git installation directory.
- Repeated `git.exe` executions while a Cursor workspace remains open.
- Executables named like common developer tools in source trees: `git.exe`, `node.exe`, `npx.exe`, `where.exe`, `python.exe`, `npm.exe`, `powershell.exe`, or similarly trusted command names.
- EDR or Sysmon events where the image path is under `%USERPROFILE%\source\repos\`, `%USERPROFILE%\Downloads\`, temporary extraction directories, or other developer workspaces.

## Response and mitigation guidance
1. Until a vendor-fixed version is confirmed, open untrusted repositories on Windows only in a disposable VM, Windows Sandbox, or an isolated analysis environment.
2. Do not open newly cloned, downloaded, or received repositories directly in Cursor before inspecting the top-level file list with a non-executing viewer.
3. Add AppLocker, Windows Defender Application Control, or EDR rules that deny execution of high-risk tool names from workspace roots. Prefer path-based rules scoped to developer project directories over hash-based rules.
4. Alert on Cursor or Electron-based IDE processes launching executables from repository roots.
5. Treat execution as a developer-endpoint compromise event: preserve process telemetry, file hashes, workspace contents, browser / token-access evidence, and source-control audit logs before cleanup.
6. Rotate GitHub, SSH, package-registry, cloud, and AI-assistant credentials reachable from the developer session after isolating the host.
7. Extend source-repository review checklists beyond config files and lifecycle scripts to include root-level binaries with trusted developer-tool names.

## Related pages
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [Browser-based developer IDE OAuth token theft](browser-based-developer-ide-oauth-token-theft.md)
- [AI coding-agent symlink write confusion](ai-coding-agent-symlink-write-confusion.md)

## Sources
- Mindgard: https://mindgard.ai/blog/cursor-0day-when-full-disclosure-becomes-the-only-protection-left
- The Hacker News: https://thehackernews.com/2026/07/cursor-flaw-lets-malicious-cloned.html
- Cursor security advisories: https://github.com/cursor/cursor/security/advisories
