# GitLab's "private email address" is an unexpiring account-wide credential: the `glimt-` incoming-email token pushes code, runs CI/CD jobs as the victim, and bypasses project IP allowlists — sender identity is never verified, there is no setting to disable the feature, and GitLab closed the report as intended behavior (Aikido, Sep 23, 2026)

## Tags

- gitlab
- credential-design
- incoming-email
- glimt-token
- ip-allowlist-bypass
- ci-cd-abuse
- supply-chain
- insecure-defaults
- ai-generated-code-delivery
- defender-heuristic

## Summary

Aikido Security Research (Joe Leon), "Send GitLab an email, push to main," published Sep 23, 2026 (full text captured by this wiki). GitLab projects show a private per-project email address under "Email work item to this project": `incoming+project-id-glimt-XXXXXXXXXXXXXX-issue@incoming.gitlab.com`. The UI presents it as a project-scoped convenience ("yours alone", "adds items to this project", and until the report, "cannot be used to access any other data"). Aikido's tested findings, each confirmed against projects they control:

- **The `glimt-` string inside the address IS the credential** — a long-lived token tied to the user's account that **never expires**. The same token appears in the address of every project the account can see (five projects → five addresses, identical `glimt-` segment, private projects included). It is effectively a fine-grained personal access token with account-wide reach, delivered in the one format that exists to be handed out.
- **Sender is never authenticated.** Any mailbox on the internet can send to the address; GitLab processes the message as the token's owner. Holding the address = holding both authentication and authorization. (GitLab is "now considering" sender verification — not shipped.)
- **Issues → code in two steps.** Swap the `-issue` suffix for `-merge-request`; MR emails accept a **git `.patch` attachment**, which GitLab applies to the named source branch (creating the branch if it doesn't exist). A patch touching `.gitlab-ci.yml` gets **GitLab to run the attacker's CI job in the victim's project, as the victim**. Absent branch protection, a plain issue-email path also yields commits on `main` authored by the victim.
- **The mail path bypasses project IP restrictions.** A private project firewalled to a single non-attacker IP blocked Aikido's browser AND `git clone` — and still accepted the merge-request email.
- **Confirmed impacts from one leaked address:** push to a protected branch in a private IP-allowlisted repo; exfiltrate source from IP-allowlisted private projects; read CI/CD variables and secrets; read confidential issues (via the `/move` quick action); use the in-job `CI_JOB_TOKEN` to reach further into the account.
- **Constraints (bounds, not mitigations):** the token inherits the victim's role — a leaked Guest address is near-worthless, a Maintainer address reaches protected branches and CI/CD variables; and routing to a specific project needs that project's path slug + ID (public for public projects; private projects need an information leak, and the ID is guessable).
- **The addresses are already public.** Aikido surfaced ~a dozen live incoming-email addresses in one afternoon of searching READMEs, contributing guides, and support pages — nearly all published deliberately by maintainers telling users where to file bugs, several on very popular open-source projects.
- **No user-side kill switch.** There is no setting to disable issue-by-email or MR-by-email creation and no way to require sender match; the only control is the PAT-page reset, which invalidates every project address at once. Affected: every GitLab.com account and every self-managed instance with incoming email enabled (GitLab Dedicated appears unaffected, untested).
- **Vendor disposition:** reported via HackerOne May 2026 → closed **intended behavior**; a June confidential issue on the GitLab repo drew a fuller response. GitLab's shipped changes: removed "It cannot be used to access any other data" from the UI, added "and merge requests" where the UI said only work items, and documented that incoming email is not subject to IP restrictions. The mechanism is untouched. Aikido: "GitLab built a credential that reaches every project in the account and bypasses IP restrictions, then presented it as an email address."

## Durable reads

- **Format is not security.** The address "is called an email address, formatted like one, and has a copy button" — nothing about it looks like a credential, so it gets posted in public READMEs. This is the recurring secret-in-a-friendly-wrapper failure: the wrapper's stated semantics ("email address for filing bugs") train every tool and human in the path to treat a credential as public information. Detection/secret-scanning angle: Aikido added Betterleaks coverage for `glimt-`-prefixed tokens, custom-prefix tokens, and pre-`glimt-` legacy formats — scan for incoming-email addresses like any other secret, then rotate preemptively.
- **An allowlist that can be reached around through a different protocol is not a boundary.** Teams set GitLab IP restrictions believing a VPN-edge perimeter; the inbound mail path answers regardless. Same class as the on-wiki rule from `npmjs.it.com` and serverless-C2 coverage: the exposure unit is the attack SURFACE, not the protocol you thought you were blocking (compare: M365 device-code flow is phishable no matter the page you block).
- **The mail path is a code-delivery rail for AI-agent pipelines.** The attacker needed zero knowledge of the target repo beyond a leaked address + branch name; the patch + CI-job shape is supply-chain delivery with the victim's own identity stamped on the commit. This is a supply-chain variant of the product-instructed-command squat pattern on this wiki, inverted: not an unclaimed name, but an unclaimed inbox.
- **Intended-behavior closures do not close risk.** GitLab's factual framing ("a leaked token is a leaked token") sidesteps credential-presentation asymmetry: a token minted, formatted, and marketed as public-contact-info has a materially higher leak probability than one shown as `glpat-…`. Triage heuristic: when a vendor closes as by-design, the residual risk calculation includes the UI's own leak training.
- **Defender actions:** rotate the incoming-email token preemptively unless actively used (PAT page → reset, accept the all-addresses invalidation); grep org repos/docs/support macros for `incoming+project-.*@incoming.gitlab.com`; do not treat project IP allowlists as covering the mail path; review whether Maintainer/Owner roles need the feature at all — role reach is the blast radius.

## Sources

- Aikido Security Research (Joe Leon), "Send GitLab an email, push to main," Sep 23, 2026 — <https://www.aikido.dev/blog/gitlab-email-push-to-main> (full text captured by this wiki; RSS-listed 06:00 UTC Sep 23; tested claims verified by the authors against their own projects; HackerOne report May 2026 closed as intended behavior; Betterleaks scanner rules shipped alongside)
