# Claude Code GitHub Action prompt-injection boundary

## Summary
GMO Flatt Security researcher RyotaK documented a Claude Code GitHub Actions trust-boundary flaw where untrusted GitHub issue or comment content could be routed into workflows that held repository and workflow privileges. Anthropic fixed the reported bypasses and related hardening issues in `anthropics/claude-code-action` v1.0.94, according to the researcher's June 2026 writeup.

Microsoft Threat Intelligence separately reported a Claude Code Action case on June 5, 2026 where prompt-injected, attacker-controlled GitHub content could drive the agent's file-read tooling toward sensitive runner process files. Microsoft says Anthropic mitigated that issue in Claude Code version 2.1.128 by blocking access to sensitive `/proc` files.

This is best tracked as a reusable pattern rather than a single intrusion: AI-assisted CI jobs convert repository text into agent instructions, then run with GitHub App, `GITHUB_TOKEN`, OIDC, issue, pull-request, content, discussion, or workflow permissions. If the permission boundary treats GitHub Apps, edited issues, or issue-triage flows as trusted when they are attacker-influenced, a public issue can become a repository takeover path.

## Tags
- patterns
- AI assistants
- Claude Code
- GitHub Actions
- prompt injection
- CI/CD
- supply-chain
- repository poisoning
- GitHub App
- OIDC
- secrets

## Why this matters
- Claude Code GitHub Actions can run in CI/CD with permissions that are powerful enough to read and write code, issues, pull requests, discussions, and workflows.
- The reported flaw shows that “only trusted users can trigger the agent” controls can fail when GitHub App behavior, public-repository issue creation, issue editing, or companion triage workflows are part of the chain.
- The blast radius is supply-chain shaped: compromising the action's own repository or a popular downstream repository could poison code consumed by many other projects.
- This class of issue is not unique to Claude Code. Any AI agent that ingests issue/PR text and receives repository write privileges needs a hard trust boundary between untrusted content and privileged actions.

## Reported boundary failures

### GitHub App trust bypass
- The action's permission check allowed actors ending in `[bot]`, treating GitHub Apps as trusted.
- RyotaK notes that GitHub Apps can have implicit public-repository read behavior and can create public issues or pull requests without explicit repository-specific write permission, similar to normal users.
- In a vulnerable flow, a malicious GitHub App could create attacker-controlled issue content that passed the action's GitHub-App actor check and reached Claude Code as trusted context.

### Untrusted issue triage
- Anthropic's example issue-triage workflow used `allowed_non_write_users: "*"` so external users could open issues and invoke Claude for labeling or triage.
- The example also passed `secrets.ANTHROPIC_API_KEY` and `secrets.GITHUB_TOKEN` into the action with `issues: write`.
- The researcher says workflow-run summaries were public by default and could become an exfiltration channel when prompt injection caused Claude to include sensitive output in the summary.
- Even after disabling that summary behavior, command execution paths such as `gh issue view` needed argument validation because attacker-influenced URLs could embed secrets into outbound requests.

### Chained workflow escalation
- A lower-privilege issue-triage workflow with `issues: write` can let an attacker edit issues or comments.
- If a separate “tag mode” Claude workflow later trusts a write-user-created issue or comment containing `@claude`, the attacker can race-edit that trusted object after creation and before Claude fetches it.
- That chain can move from untrusted public issue creation to Claude processing attacker-controlled instructions inside a workflow with broader repository and OIDC permissions.

### Runner environment exposure through file-read tools
- Microsoft Threat Intelligence says it observed prompt-injection attempts in public repositories using AI-assisted GitHub workflows across multiple vendors, including payloads hidden in HTML comments that were invisible in the rendered issue but visible to an agent reading raw Markdown.
- In Microsoft's Claude Code Action case, Bash subprocess execution paths had environment-scrubbing controls, but the agent's Read tool was not subject to the same sandboxing model.
- Microsoft reports the Read tool was eventually authorized to access `/proc/self/environ`, exposing the workflow's `ANTHROPIC_API_KEY` and potentially other runner credentials available in the process environment.
- The durable lesson is that secret scrubbing for shell commands is not enough when an AI workflow has independent file-read, network, artifact, summary, or repository-write tools. Every tool exposed to untrusted model input needs its own allow/deny boundary.

## Defender heuristics
- Inventory workflows using `anthropics/claude-code-action`; update to v1.0.94 or newer and avoid floating major tags where policy requires reproducibility.
- Treat `allowed_non_write_users` as high risk. If it must be used, grant only the minimum permissions needed for a narrow task and do not expose unrelated secrets.
- Split untrusted triage workflows from privileged repository-modifying workflows. Do not let output, edited issues, generated comments, or summaries from untrusted workflows become trusted agent input.
- Restrict `permissions:` in every Claude/AI workflow. Avoid broad `contents: write`, `actions: write`, `pull-requests: write`, `id-token: write`, or workflow write permissions unless the specific job needs them.
- Block agent access to sensitive runner paths such as `/proc/self/environ`, `/proc/*/environ`, token files, cloud credential files, and CI metadata endpoints unless the workflow has a tightly scoped, reviewed need.
- Treat raw issue, pull-request, and comment text as hostile even when dangerous instructions are hidden from browser rendering with HTML comments or other markup tricks.
- Require human review for AI-generated commits, workflow-file edits, release/tag changes, and dependency updates.
- Review workflow logs and summaries for unusual secret-like output, unexpected `gh` or `git` commands, issue edits by automation, and AI-agent commits after public issue activity.
- Prefer pinned action SHAs for privileged workflows and monitor upstream action repositories for security releases.

## Related pages
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)

## Sources
- GMO Flatt Security: https://flatt.tech/research/posts/poisoning-claude-code-one-github-issue-to-break-the-supply-chain/
- Anthropic fix commit linked by public reporting: https://github.com/anthropics/claude-code-action/commit/1bbc9e7ff7d48e1299f7fa9698273d248e0cafea
- The Hacker News summary: https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/
