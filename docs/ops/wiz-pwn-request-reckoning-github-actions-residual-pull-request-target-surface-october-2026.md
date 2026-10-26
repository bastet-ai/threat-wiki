# Wiz "Pwn Request Reckoning": GitHub Actions' 2026 hardening closed the default pull_request_target case — the residual surface is explicit opt-ins, pre-backport SHA pins, non-checkout fetches, uncovered privileged triggers, and script injection

**Tags:** ops, supply-chain, ci-cd, github-actions, pwn-request, pull-request-target, detection-engineering
**First seen:** 2026-10-26 (Wiz Research publication)
**Source:** <https://www.wiz.io/blog/github-actions-security-pwn-request-reckoning> (Shay Berkovich, Oct 26, 2026 — full text captured by this wiki)
**Related:** [Gheist page](gheist-compromised-github-tokens-workflow-secret-dump-base32-ci-sync-branches-wiz-october-2026.md) (Part-1 threat model this updates), [GhostAction page](ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md), [LiteLLM 1.107.0 page](litellm-1-107-0-wheel-only-privcollect-startup-hook-credential-stealer-hourly-github-dead-drop-loader-jfrog-october-2026.md) (a prod-approval-gate bypass on the same trigger family), [Mini Shai-Hulud page](mini-shai-hulud-npm-pypi-worm-campaign.md) (the May TanStack wave chained a pull_request_target Pwn Request with cache poisoning + OIDC extraction)

## Summary

Wiz's Part-3 of its GitHub Actions research line updates the Pwn-request threat model for GitHub's 2026 platform changes. The default-case exploit (any fork PR triggering a `pull_request_target` workflow that checks out fork code) is now materially harder — and the residual risk has a specific, auditable shape: **the protections live inside `actions/checkout`, so anything that fetches code another way is unprotected; the protections apply to two triggers, so other privileged triggers are unprotected; and script injection was never a checkout bug at all.**

## The 2026 hardening timeline (as published)

| Date | Change |
|---|---|
| 2026-06-18 | `actions/checkout@v7.0.0` blocks fork-code checkouts by default on untrusted triggers (`pull_request_target`, `workflow_run`-on-PR) |
| 2026-06-26 | Read-only cache tokens at platform level for untrusted triggers (kills cache poisoning) |
| 2026-07-20 | Fork-checkout protection backported to all active majors: **v2.8.0, v3.7.0, v4.4.0, v5.1.0, v6.1.0** (v1 excluded); mutable tags (`@v4`) inherit automatically |
| 2026-09-10 | Fine-grained cache controls (`cache-mode`) GA |
| 2026-09-17 | Workflow Execution Protections GA (event policies, actor rules); default event policy in evaluate mode |
| 2026-12-02 | GitHub begins ENFORCING the default event policy that blocks `pull_request_target` in public repos without an explicit event policy (private/internal repos NOT affected) |

## The residual attack surface (durable findings)

1. **THE SHA-PINNING PARADOX.** Supply-chain best practice — pinning actions to exact commit SHAs — can silently opt a workflow OUT of the platform protection, because the guard is logic inside `checkout` itself: a SHA-pinned ref that resolves to a pre-Jul-20 release (e.g. `actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955` = `v4.3.0`) runs legacy code with NO fork-checkout protection, while `@v4` (→ v4.4.x) or `@v4.4.0` are protected. **Audit rule: every SHA-pinned `actions/checkout` ref must resolve to ≥ v2.8.0 / v3.7.0 / v4.4.0 / v5.1.0 / v6.1.0 / v7.0.0.** This is a NEW false-security inversion: the hardened-looking config is the vulnerable one.
2. **PROTECTIONS ARE ACTION-LOCAL.** Any fetch that isn't `actions/checkout` operates unrestricted under `pull_request_target`: direct `git clone` + `checkout $PR_SHA`, `gh pr checkout`, `gh repo clone`, and third-party checkout actions configured with a PR head ref.
3. **PROTECTIONS ARE TRIGGER-LOCAL (two triggers only).** `pull_request_target` and `workflow_run` are covered; **`issue_comment`** bot-command workflows (`/deploy`, `/test`, `/cherry-pick`) that check out `refs/pull/N/merge` are fully exploitable on checkout@v7 with no flag — note the inconsistency Wiz flags: GitHub's own cache controls classify `issue_comment` as low-trust while checkout protections ignore it. **`repository_dispatch`** runs with secrets and is exploitable when payload data influences the checkout ref. Authorization must hold from event-fire to code-run: check the commenter's CURRENT permission (`getCollaboratorPermissionLevel`, write+ — NOT `author_association`), pin the exact head SHA (the `/merge` ref is mutable — an attacker can push after the approving comment), and abort if the PR updated after the comment.
4. **SCRIPT INJECTION IS UNAFFECTED BY EVERY 2026 CHANGE.** `${{ }}` interpolation of attacker-controlled event fields (`pull_request.title`, comment body, dispatch payload) into `run:` blocks is code execution with the job's secrets and no checkout required. The fix is structural: pass untrusted context through environment variables (quoted), never into the script text.
5. **THE DECEMBER DEFAULT IS A DEFAULT, NOT A BAN.** Workflows that add an explicit permissive event policy — labelers, preview deploys, fork CI with secrets — are exactly the ones handling untrusted input with elevated privileges, and private/internal repos are outside the enforcement entirely.

## Hunt / audit checklist (as captured)

- Repo-wide grep: `pull_request_target` + any explicit event policy; audit WHY the opt-in exists.
- `actions/checkout@<40-hex>` refs → resolve the SHA → flag any ref older than the Jul-20 backports.
- `run:` steps that fetch code outside `actions/checkout` on untrusted triggers.
- `issue_comment` / `repository_dispatch` workflows with secrets + `refs/pull/.*/merge` or payload-derived refs.
- `run:` blocks interpolating `github.event.*` fields directly (quote-and-env is the fix).
- December-2 readiness: inventory public-repo workflows that will silently stop without an event policy — expect a wave of rushed permissive policies around the enforcement date; that wave is the new opt-in population to re-audit.

## Why it matters (durable reads)

- Pwn requests remain the credential-to-CI path that fed this year's biggest supply-chain stories (the Mini Shai-Hulud TanStack wave chained one with cache poisoning and OIDC extraction; LiteLLM's prod approval gate fell to a second-account approval, same trust-boundary family). Platform hardening moves the class underground; it does not delete it.
- The SHA-pinning paradox inverts a decade of Actions advice — detection should key on the PINNED-OLD case specifically, because that population believes itself hardened.
- The enforcement-date effect (Dec-2) creates a predictable, dated defender event: audit who writes permissive event policies in November.
