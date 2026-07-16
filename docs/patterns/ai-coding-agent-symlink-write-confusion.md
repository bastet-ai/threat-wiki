# AI coding-agent symlink write confusion

## Summary

Wiz disclosed **GhostApproval** on July 8, 2026: a class of AI coding-assistant trust-boundary failures where a malicious repository can place a symbolic link inside the workspace, induce the agent to write a seemingly harmless local file, and cause the operating system to write to a sensitive target outside the workspace instead. Wiz reported the pattern across Amazon Q Developer, Anthropic Claude Code, Augment, Cursor, Google Antigravity, and Windsurf.

The important defender lesson is not just “symlinks are dangerous.” AI coding tools often present a human-in-the-loop confirmation prompt as the safety boundary. In GhostApproval, that prompt can describe the workspace path the user approved while hiding the canonical target that actually receives the write. Wiz frames this as CWE-61 symlink following combined with CWE-451 UI misrepresentation of critical information.

Adversa AI's earlier SymJack research described the same operational hazard from another angle: an agent or shell command copies an innocent-looking file in a booby-trapped repository, the destination is a symlink to agent configuration, and the write plants executable MCP / agent configuration that runs on restart. Together, these reports make symlink resolution a first-class agent runtime control, especially on developer laptops and CI runners that hold source-control, package-registry, cloud, signing, SSH, browser, and LLM-provider credentials.

## Tags

- patterns
- AI agents
- AI coding assistants
- developer machines
- CI-CD
- symlink
- symbolic links
- arbitrary file write
- workspace sandbox
- prompt injection
- repository poisoning
- GhostApproval
- SymJack
- Amazon Q Developer
- Claude Code
- Cursor
- Google Antigravity
- Windsurf
- Augment
- Adversa AI
- Wiz
- CWE-61
- CWE-451

## Attack shape

1. An attacker publishes, submits, or sends a repository that appears to be a normal project or setup task.
2. The repository contains a symlink with a benign workspace name such as a project settings file, media file, documentation artifact, or generated config path.
3. The symlink points outside the workspace to a sensitive target such as `~/.ssh/authorized_keys`, an agent configuration file, an MCP server definition, shell startup file, IDE setting, credential store path, or CI workspace secret-bearing file.
4. Repository instructions, README text, agent memory, issue content, or a prompt ask the coding assistant to “set up,” “fix,” “copy,” or “update” the benign-looking file.
5. The agent follows the instruction and asks the user to approve the local-looking operation, or runs in a non-interactive / trusted mode where approval is implicit.
6. The kernel follows the symlink. The write lands on the sensitive outside-workspace file.
7. Impact depends on the target: persistent SSH access, agent/MCP command execution on restart, CI pipeline compromise, credential exfiltration, or arbitrary user-context code execution.

## GhostApproval case study

Wiz reported that six AI coding assistants followed symlinks in ways that crossed the workspace boundary and could lead to arbitrary file writes or remote code execution on the developer host:

| Product | Wiz status | Reported affected versions / fixed state |
| --- | --- | --- |
| Amazon Q Developer | Fixed | CVE-2026-12958; language server versions before 1.69.0 affected; 1.69.0 fixed |
| Cursor | Fixed | CVE-2026-50549; versions before 3.0 affected; 3.0 fixed |
| Google Antigravity | Fixed | Pending CVE at publication; fixed in 1.19.6 |
| Augment | In progress | Wiz tested 0.754.3 |
| Windsurf | In progress | Wiz tested V1.9566 |
| Anthropic Claude Code | Rejected by vendor | Wiz tested v2.1.42 and reported Anthropic considered the case outside its threat model |

Wiz's proof-of-concept shape used a workspace symlink disguised as `project_settings.json` pointing to `~/.ssh/authorized_keys`. The repository's instructions asked the assistant to update `project_settings.json` with an SSH public key. If the agent wrote through the symlink, the key landed in the user's authorized keys file rather than the repository file.

The key UI failure: a user or reviewer may see an approval dialog for a harmless-looking workspace path while the agent's resolved write target is a sensitive file outside the project. That makes the approval prompt insufficient unless it displays and enforces the canonical path.

## SymJack / MCP configuration variant

Adversa AI's SymJack research showed a related chain against multiple coding-agent CLIs. Instead of asking the agent to directly edit a sensitive-looking file, the attack used an ordinary file-copy command and a symlinked destination. The visible action looked like copying a media or documentation file inside the repository. The real target was agent configuration, such as MCP server definitions or settings files. On restart, the planted configuration could launch attacker-controlled code as the user.

This variant matters because many agent products treat native file-write tools and shell commands differently. A command approval prompt that inspects `cp` arguments, file names, or the command text but does not resolve the destination path can miss the security-relevant effect.

## Defender guidance

### For agent users and platform teams

- Treat cloned repositories, issue text, README setup instructions, skill files, MCP definitions, and generated plans as untrusted input when an agent has filesystem-write or shell access.
- Disable or tightly review non-interactive / auto-approve coding-agent modes on developer workstations and CI runners that hold deploy keys, signing keys, cloud credentials, package-registry tokens, or production repository access.
- Before running an agent on an untrusted repository, inspect symlinks with `find -type l -ls` or equivalent tooling, and block symlinks that resolve outside the workspace unless explicitly required.
- Run coding agents in least-privilege containers, VMs, devboxes, or dedicated OS users with no ambient access to SSH keys, browser profiles, cloud CLIs, package tokens, or production repos.
- Do not let agent workspaces include symlinks to home-directory, dotfile, credential, agent-config, CI-config, shell startup, or SSH paths.
- Require human approval for writes to agent configuration, MCP server definitions, startup hooks, editor settings, shell profiles, SSH files, package-manager config, and CI workflow files even if the requested path appears local.

### For agent vendors and internal platform owners

- Resolve canonical paths before every read, write, copy, move, chmod, delete, archive extraction, and shell-file operation. Enforce workspace boundaries on the resolved path, not the displayed path.
- Show both requested and resolved paths in approval prompts. If they differ because of a symlink, junction, hard link, bind mount, or path alias, require a stronger explicit approval or block by default.
- Apply the same canonical-path policy to shell commands and built-in tools. Do not rely on text inspection of commands such as `cp`, `mv`, `tar`, `unzip`, `git checkout`, package-manager scripts, or generated setup scripts.
- Add a deny-by-default policy for writes to high-risk targets: SSH authorized keys and private keys, shell profiles, LaunchAgents / systemd / scheduled-task locations, agent/MCP config, IDE auto-execution config, package-manager config, Git hooks, browser profiles, and credential stores.
- Emit structured telemetry for symlink encounters, outside-workspace canonical paths, prompt displays, user approvals, auto-approval mode, and the process or tool that performed the write.
- Test agent releases with malicious-repository fixtures that combine symlinks, nested symlinks, relative path traversal, case-folding ambiguity, archive extraction, Git checkout behavior, and shell copy operations.

### Detection and response pivots

- Hunt for agent or shell processes writing outside a repository immediately after reading repository-local paths.
- Alert when coding-agent processes modify `~/.ssh/authorized_keys`, `~/.ssh/config`, shell startup files, `.git/hooks`, `.mcp.json`, `.claude*`, `.cursor`, `.vscode/tasks.json`, package-manager config, or CI workflow files.
- In CI, review pull requests for symlinks that point outside the workspace, especially when an agent job runs in trusted or auto-approve mode.
- If exploitation is suspected, preserve the repository tree including symlink metadata, agent prompt/approval logs, shell history, process telemetry, file modification times, and the sensitive target content before rotating exposed credentials.
- Treat confirmed outside-workspace writes by an agent as endpoint compromise until ruled out; rotate source-control, package-registry, cloud, SSH, signing, LLM-provider, and CI/CD credentials reachable from that user or runner.

## Related pages

- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)

## Sources

- Wiz: <https://www.wiz.io/blog/ghostapproval-a-trust-boundary-gap-in-ai-coding-assistants>
- The Hacker News: <https://thehackernews.com/2026/07/ghostapproval-symlink-flaws-could-let.html>
- Adversa AI: <https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/>
