# Amazon Kiro "Power Leak": Kiro Powers prompt-injection data exfiltration

## Summary
Mindgard (Fergal Glynn) published **"Power Leak: Amazon Kiro IDE Prompt Injection Enables Data Exfiltration"** on **August 27, 2026**. An attacker-controlled repository or page context can steer the **Amazon Kiro** agentic IDE into **rewriting its own MCP server configuration** and transmitting sensitive local workspace data to an external endpoint — without the user explicitly asking Kiro to read or send anything. Mindgard assessed **exploitation difficulty as low** for the tested configuration (Kiro IDE 0.7.45 on Windows; latest public version at publication: 1.0.337). No CVE was assigned; Amazon fixed the flaw in **Kiro IDE 0.8.140**.

The durable value is twofold: (1) a concrete AI-IDE trust-boundary pattern — steering-file / MCP-configuration writes as an exfiltration and code-execution primitive — and (2) a public case study of **disclosure-process breakdown** against AI agent products: the related steering-file finding was classified a "duplicate" on HackerOne in December 2025 and sat unremediated until late January 2026, while the Kiro Powers exfiltration path took months to reach publication.

## Tags
- patterns
- Amazon Kiro
- Kiro Powers
- prompt injection
- indirect prompt injection
- MCP
- MCP configuration
- steering file
- POWER.md
- IDE trust boundary
- AI IDE
- agentic IDE
- data exfiltration
- credential theft
- workspace trust
- vulnerability disclosure
- HackerOne
- Mindgard
- developer tooling
- AI developer tooling

## The mechanism
- **Kiro Powers** bundle MCP server configurations, steering files (`POWER.md`), hooks, and contextual knowledge; the steering file acts as a persistent "onboarding manual" that tells the agent which MCP tools exist and when to use them.
- The flaw: attacker-controlled repository content can influence the Kiro agent enough that it **rewrites its own MCP server configuration file** and causes sensitive local information to be transmitted to an external endpoint — no approval prompt is shown to the user; the developer only asked Kiro to perform a legitimate action.
- Mindgard's write-up frames it as an extension of the earlier **steering-file directive** finding, where steering directives caused local information to be folded into a **Markdown image request** delivered to an attacker server (that path published January 15, 2026).
- Precedent in the same product: in **June 2026** Amazon fixed an insufficient access-control flaw (**CVE-2026-10591**, CVSS 8.8) that let a remote unauthenticated actor execute arbitrary commands via crafted instructions writing to execution-sensitive paths such as `.vscode/tasks.json` and `~/.kiro/settings/mcp.json`, with auto-execution on folder open.

## Disclosure timeline (Mindgard's account)
- **December 6, 2025** — initial Kiro steering-file data-exfiltration vulnerability discovered.
- **December 8, 2025** — disclosed to Amazon; classified a **duplicate** through HackerOne on December 10.
- **December 11, 2025** — the Kiro Powers prompt-injection exfiltration path discovered and submitted; HackerOne verified and forwarded to Amazon on December 13.
- **January 15, 2026** — initial steering-file disclosure published.
- **January 26, 2026** — Amazon verified the Kiro Powers disclosure; **remediation released** the same day.
- **August 27, 2026** — this write-up published.

## Durable defender guidance
- Treat **agent-config files as execution surfaces**: `~/.kiro/settings/mcp.json`, workspace `mcp.json`, steering/`POWER.md` files, and `tasks.json`-style auto-exec paths are writable state that an agent can change on an attacker's behalf. Inventory and alert on agent-modified MCP/steering configuration in developer environments.
- **Upgrade Kiro IDE to 0.8.140 or later**; verify any pinned or packaged Kiro builds in CI/developer images.
- Hunt for egress from IDE processes to unusual external endpoints (Markdown image URL patterns, `image-set` proxies, new HTTP origins) where the user did not request a fetch — the exfiltration rides on ordinary-looking agent network activity.
- For AI IDEs generally: restrict what the agent may write (allow-list config paths), disable auto-execution on folder open where the workflow allows, and treat any repository/page content steering an agent toward new network destinations as a malicious-input event, not a model quirk.
- Disclosure-process angle: for red-teamers, "duplicate" classifications on AI-agent findings deserve re-testing, because interaction-surface bugs (model interpretation × tool access × config writes) rarely fit traditional defect dedup.

## Confidence and caveats
- No CVE; fixed-version status is per Mindgard's reporting of Amazon's fix (0.8.140) — verify against Kiro's own release notes before treating 0.8.140 as the official first fixed build.
- Version scoping (0.7.45 tested, 1.0.337 latest at publication) is a Mindgard/HN detail; treat affected-version ranges as approximate.
- The "duplicate" HackerOne classification is Mindgard's account of their report handling; Amazon's internal disposition was not published.

## Related pages
- [Cursor Windows workspace-path binary hijack](cursor-windows-workspace-path-binary-hijack.md) (Mindgard's earlier Cursor finding — repo-root `git.exe` execution)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [AI coding-agent symlink write confusion](ai-coding-agent-symlink-write-confusion.md)

## Sources
- Mindgard: [Power Leak: Amazon Kiro IDE Prompt Injection Enables Data Exfiltration](https://mindgard.ai/blog/amazon-kiro-data-exfiltration) — August 27, 2026 (Fergal Glynn)
- The Hacker News: [Amazon Kiro Prompt Injection Can Exfiltrate Sensitive Data Through Kiro Powers](https://thehackernews.com/2026/08/amazon-kiro-prompt-injection-can.html) — August 27, 2026
