# Plugin4Shell: zero-click RCE in Claude Code, Codex, GitHub Copilot, and Gemini CLI via a plugin SHA-pinning bypass — the pinned-commit checkout never verifies where it landed (AIR, Sep 17, 2026)

## Summary
AIR Security (researchers Or Nevo, Dor Granat, Niv Hoffman; published **September 17, 2026**, found May 2026 with working PoCs against all four agents, disclosed to vendors June 2026) disclosed **Plugin4Shell**, a **plugin SHA-pinning bypass** that yields **zero-click remote code execution** in all four major AI coding agents: **Claude Code, OpenAI Codex, GitHub Copilot, and Google's Gemini CLI**. The bug is not in a marketplace but in every agent's install path: the agent checks out the exact commit the marketplace pinned but **never verifies the checkout actually landed on that commit**. An attacker who controls the plugin's repository makes `git checkout <pinned-sha>` resolve to **attacker code while the pin still looks honored** — and because installed plugins **auto-update in the background** (default in Claude Code and Codex), the swap reaches already-installed, already-reviewed, already-pinned plugins with **no user action at all**. AIR calls it "the first supply chain vulnerability of the AI agent ecosystem." Vendor responses diverged sharply: **Anthropic patched Claude Code in 2.1.179** (confirmed Jun 17), **OpenAI patched Codex in 0.146.0** (verified Aug 12), **Microsoft shipped no fix for Copilot**, and **Google declined to patch, instead deprecating Gemini CLI entirely** (confirmed Aug 4) and telling users to migrate to Antigravity — meaning every existing Gemini CLI install stays exposed indefinitely. GitHub's public position is that the attack "cannot be exploited on GitHub" because GitHub rejects 40-hex branch names; AIR counters that marketplaces on other hosts — **Bitbucket and any self-hosted git server** — accept SHA-shaped branch names, and Anthropic's own documentation lists Bitbucket and self-hosted git as valid marketplace backends, so Copilot and Claude Code remain exposed through supported configurations. Doing everything right — reviewing a plugin, pinning its commit, trusting a marketplace — does not protect you.

## Tags
- patterns
- AI agents
- AI coding assistant
- supply-chain
- plugin pinning
- SHA pinning
- git ref ambiguity
- zero-click
- RCE
- auto-update
- Claude Code
- Codex
- GitHub Copilot
- Gemini CLI
- marketplace abuse
- AIR
- prompt injection adjacent
- plugin4shell

## Why this matters
- **The pin is the trust anchor, and it silently dissolved.** SHA pinning is the industry's explicit answer to plugin rug-pulls: review at one commit, pin it, run that hash forever. Plugin4Shell nullifies it without touching the pin — review passes, the pin is written, and *different code installs*. Every downstream vetting process built on pinning inherits the failure.
- **Zero-click via the defender's own convenience feature.** Auto-update is what makes this zero-click: the same vulnerable `git checkout` re-runs in the background, so when the marketplace re-pins to a new commit, the attacker's branch swap lands on every agent that already trusts and already runs the plugin. The attacker needs no install step, no prompt, no click — only that the benign plugin is already there.
- **The vulnerable users are the careful ones.** AIR's framing: "the victim only has to have a plugin installed, from a marketplace they trust, that was reviewed and pinned exactly as the security model intends." Organizations that run internal review-and-pin programs are precisely the ones relying on the guarantee that broke.
- **One design error, four labs.** The same missing assertion — verify the resolved HEAD equals the pinned SHA — sits in every major agent. This is an ecosystem-level mistake repeated independently, which is why "one flaw, and every major lab made it" is the durable lesson, and why no marketplace-side control can restore the guarantee: the pin is resolved inside the agent.
- **The vendor-response asymmetry is the actionable part.** As of disclosure: patched (Claude Code 2.1.179, Codex 0.146.0), **unpatched with no fix shipped** (Copilot), and **permanently unpatched because the product is deprecated** (Gemini CLI). Deprecation without patch leaves every install exposed; the only guidance is migrate to Antigravity, which has no SHA pinning to bypass. Unpatched-agent users must disable plugin auto-update or remove marketplace plugins.
- **The attack chain is already proven end to end.** AIR's earlier work demonstrated both prerequisite steps at scale: **The Story of Skills** (a benign-passing malicious skill reached ~26,000 agents before removal — plant then rug-pull is easy) and **SkillJacking** (**925 hijacked skills, 134,000 agents affected** — takeover of legitimate plugin repos happens in the wild). Plugin4Shell is the delivery mechanism that defeats the containment built for exactly those scenarios.
- **Converges with the week's agent-trust-intelligence.** Mandiant's Sep 16 AI Risk and Resilience case study showed a hijacked *live coding-assistant session* used to spread Shai-Hulud across ~100 internal repositories; Anthropic's Sep 17 report showed eval sandboxes and LiteLLM tiers extorted for production API keys. Plugin4Shell completes the picture: the agent's *plugin supply chain* is now a mass-delivery vector. Anything that ingests untrusted content while holding developer credentials is the perimeter — and now so does its plugin loader, on a schedule, without asking.

## Mechanism (as published)

### Variant A — Claude Code, OpenAI Codex, GitHub Copilot (git ref/commit ambiguity)
Agents clone the plugin repository and check out the pinned SHA:

```
git clone <plugin repo> ./
git checkout aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

The attacker, controlling the upstream repo, **creates a branch whose name is the exact 40-hex pinned SHA and sets it as the repository's default branch**. The plain clone brings it down as a local branch of that name; `git checkout` **prefers the ref over the object id** when a name is both (printing only a "refname is ambiguous" warning), so the pinned commit's presence is irrelevant — the branch is what lands in the working tree. Two conditions: the host must allow hash-shaped branch names (git's own `check-ref-format` accepts 40-hex; GitHub rejects them; Bitbucket and self-hosted git accept), and the branch must be the repo default (a non-default branch is fetched only as a remote-tracking ref, and checkout would fall back to the real commit). The agent reports a successful install *at the pinned commit*.

The zero-click layer: a routine version bump makes the marketplace re-pin to a new benign commit `bbb...`; the attacker then names a branch `bbb...` pointing at malicious code and makes it default; every agent's **background auto-update** re-runs the checkout and receives it.

### Variant B — Gemini CLI (FETCH_HEAD shadowing)
Gemini pins via `--ref`:

```
git clone --depth 1 <plugin repo> ./
git fetch origin 41d0bc0a4aeb2fbf797dacea39e876d98c95024b
git checkout FETCH_HEAD
```

The fetch records the correct commit in `.git/FETCH_HEAD` — but `git checkout FETCH_HEAD` resolves **refs before reading that file**: if the repository's default branch is itself named `FETCH_HEAD`, the checkout takes the branch and the fetched commit is silently discarded.

### The fix AIR prescribes
One assertion, inside the agent, after checkout:

```
test "$(git rev-parse HEAD)" = "<pinned-sha>" || abort
```

It must check the **resolved HEAD**, not the requested ref — that distinction is exactly what the Gemini variant slips through — and it cannot be enforced marketplace-side because the pin is resolved on the client.

## Vendor response timeline (per AIR; independently covered by The Register, Sep 17)
| Date | Event |
|---|---|
| May 2026 | Found by AIR with working PoC against all four agents |
| June 2026 | Coordinated disclosure to all four vendors |
| 2026-06-17 | Anthropic confirms fix in **Claude Code 2.1.179** |
| 2026-08-04 | Google confirms **no fix** — Gemini CLI deprecated; users advised to migrate to Antigravity |
| 2026-08-12 | **Codex 0.146.0** verified fixed |
| Sep 17, 2026 | Public disclosure. **Microsoft/Copilot: no fix shipped.** GitHub states SHA-shaped branch/tag names are rejected on GitHub so the flaw "cannot be exploited on GitHub"; AIR notes marketplaces on Bitbucket/self-hosted git are supported configurations, keeping Copilot exposed |

## Caveats
- Scale ("millions of agents") and the "first-of-its-kind AI supply-chain attack" framing are **vendor-reported by AIR**, a startup that emerged from stealth on Sep 1, 2026 and sells agent-marketplace controls (it states its own Air Marketplace/Air Filter customers were unaffected) — treat product claims as marketing-adjacent; the mechanism itself is concrete and verifiable git behavior.
- SkillJacking's 925 skills / 134,000 agents figures are AIR's own prior research, not independently audited.
- No in-the-wild exploitation of Plugin4Shell has been reported as of disclosure; this is a demonstrated capability, not an observed campaign.
- Whether Copilot's marketplace support actually reaches non-GitHub hosts in default enterprise configurations is contested between GitHub and AIR; the safe assumption for defenders is exposed.

## Defender actions
- **Patch or remove**: update Claude Code to ≥ 2.1.179 and Codex to ≥ 0.146.0. For Copilot, no vendor patch exists — disable agent plugin auto-update or restrict plugin sources until Microsoft ships a fix. For Gemini CLI, treat every install as permanently vulnerable; migrate to Antigravity or decommission.
- **Inventory installed agent plugins/skills** with their pinned SHAs and marketplace hosts; any plugin whose marketplace backend is Bitbucket or self-hosted git should be treated as exposed regardless of pin state.
- **Verify pins yourself**: script `git rev-parse HEAD`-against-pin checks for locally cached plugin clones; alert on mismatch.
- **Treat plugin materialization as a detection surface**: new files appearing in agent plugin directories without an install event, background `git clone`/`git checkout` processes spawned by agent runtimes, and any branch name matching `^[0-9a-f]{40}$` or named `FETCH_HEAD` in a plugin repo.
- **Extend the privileged-session rule** (Mandiant): the coding agent and everything its plugin loader auto-installs run with the developer's reach — the same containment (isolated credentials, egress via internal registries, allowlisted dependency verification hooks) applies to plugins as to AI-recommended packages.

## Related pages
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [Mandiant IR case study: AI coding-assistant session hijack spreads Shai-Hulud](../ops/mandiant-ai-coding-assistant-session-hijack-shai-hulud-saas-september-2026.md)
- [Anthropic Threat Intelligence report, September 2026](../ops/anthropic-threat-intelligence-report-september-2026-ai-augmented-operations.md)
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [Actions /cool GitHub Actions tag compromise](../ops/actions-cool-github-actions-tag-compromise.md) (ref/tag-vs-commit ambiguity against CI, the pre-agent ancestor of this failure)

## Sources
- AIR Security (primary): [https://www.air.security/blog-posts/plugin4shell](https://www.air.security/blog-posts/plugin4shell)
- The Register coverage (Sep 17, 2026): [https://www.theregister.com/security/2026-09-17/ai-coding-agents-0-click-rce-flaw-could-hand-attackers-keys-to-the-kingdom/](https://www.theregister.com/security/2026-09-17/ai-coding-agents-0-click-rce-flaw-could-hand-attackers-keys-to-the-kingdom/)
- Help Net Security coverage (Sep 18, 2026): [https://www.helpnetsecurity.com/2026-09-18/plugin4shell-ai-coding-agents-vulnerability/](https://www.helpnetsecurity.com/2026-09-18/plugin4shell-ai-coding-agents-vulnerability/)
- AIR SkillJacking (prior work, 925 skills / 134,000 agents) and The Story of Skills (~26,000 agents): linked from the primary post
