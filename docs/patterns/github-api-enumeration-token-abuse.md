# GitHub API enumeration and access-token abuse

## Summary
Datadog Security Labs' July 8, 2026 research describes overlapping campaigns that systematically enumerate corporate GitHub organizations, repositories, and users through GitHub's API. The activity blends public-data scraping, old or dormant "ghost" GitHub accounts, custom automation with plausible user agents, and compromised OAuth / personal access tokens.

Treat this as a source-control exposure pattern. Most requests can look benign because they hit public API surfaces and return successful responses, but Datadog observed cases where activity escalated from mapping to apparent private-repository cloning.

## Tags
- patterns
- GitHub
- source control
- source-repository reconnaissance
- API enumeration
- access token abuse
- OAuth tokens
- personal access tokens
- PAT theft
- ghost accounts
- dormant accounts
- repository exfiltration
- supply chain
- developer identity
- Datadog Security Labs

## Why this matters
- GitHub organization mapping is useful pre-compromise work for package-registry attacks, CI/CD compromise, social engineering, dependency confusion, and source-repository poisoning.
- Public GitHub API calls may not create obvious failed-authentication or permission-denied signals. Defenders need aggregate behavior, not just error events.
- Dormant accounts with old creation dates can make automated enumeration look less like fresh burner-account activity.
- Compromised OAuth tokens and PATs can turn reconnaissance into private repository access, cloning, and secret-hunting.
- The pattern overlaps with recent developer-ecosystem incidents where attackers first map maintainers, repositories, workflows, and package ownership before publishing malware or modifying release automation.

## Observed tradecraft
- Systematic enumeration of corporate GitHub organizations, public repositories, users, followers/following relationships, gists, starred repositories, organization membership, and GraphQL-visible public objects.
- Coordinated movement by multiple accounts across multiple organizations over time, with versioned automation and custom or legitimate-sounding user agents.
- Use of "ghost" accounts: GitHub accounts that are often years old, dormant, or otherwise less obviously disposable than newly created burners.
- Use of compromised OAuth tokens and personal access tokens from legitimate users.
- Activity that usually appears as successful HTTP 200 API traffic rather than blocked or failed authentication.
- Escalation in some cases from public enumeration to behavior consistent with private repository cloning.

## Defender heuristics
- Monitor GitHub audit logs, API logs, enterprise events, and identity-provider telemetry together. A token that looks valid at GitHub may still be anomalous for the user, device, ASN, country, or time window.
- Baseline API volume by actor, token type, user agent, route family, organization, and source network. Alert on coordinated enumeration across many repositories, users, or organizations.
- Treat unusual reads and clones as security events, not just developer activity: private repository clone spikes, broad `repo` scope use, token access from new ASNs, and rapid listing of repositories followed by clone/download actions deserve triage.
- Inventory OAuth apps, GitHub Apps, fine-grained PATs, classic PATs, deploy keys, and machine users. Remove unused tokens and revoke grants for users who no longer need source access.
- Prefer SSO enforcement, fine-grained / short-lived credentials, mandatory token expiration, least-privilege scopes, and organization policies that restrict third-party OAuth app authorization.
- Review dormant internal GitHub users and external collaborators. Disable stale accounts, remove stale organization memberships, and require re-verification before privileged repository access is restored.
- Correlate GitHub API enumeration with later package-registry, CI/CD, and cloud events: npm / PyPI publication, GitHub Actions workflow edits, secret-scanning alerts, repository archive downloads, and unusual CI token use.

## Detection pivots
- High-rate or scripted calls to GitHub organization, repository, user, member, follower/following, gist, stars, and GraphQL endpoints.
- API traffic from accounts with little normal development history but old creation dates.
- User-agent strings that are new to the organization, unusually versioned, or shared across multiple accounts.
- Valid OAuth or PAT use from unexpected ASNs, hosting providers, VPNs, or countries compared with the user's normal pattern.
- Repository clone or archive-download activity shortly after broad enumeration.
- Multiple users or tokens touching similar route families from related networks within the same time window.

## Concrete case: Wiz CIRT multi-organization PAT campaign (May–June 2026)
Wiz CIRT's August 13, 2026 writeup documents a coordinated campaign in which compromised GitHub PATs were used across multiple organizations over roughly three weeks. The reconstruction adds three durable specifics to this pattern:

- **Staged escalation with distinct infrastructure per phase.** Reconnaissance on May 15 hit the `/repositories/{id}/readme` endpoint from a single us-east-1 EC2 IP (`13.221.167[.]217`) using a standard Chrome 125 user agent. Validation clones on May 29–31 came from `107.174.201[.]183` with the `git/2.25.1` user agent. Mass cloning on June 1 (09:14–14:55 UTC) came from 102 ca-central-1 AWS IPs with the `git/2.43.0` user agent, cloning up to thousands of repositories per organization.
- **Valid employee PATs, unknown origin.** The clones used valid PATs belonging to employees of the affected organizations. Wiz found no code or cloud-resource source for the tokens, leaving endpoint compromise as an unconfirmed hypothesis — so the initial access vector is still open.
- **Retention trap.** GitHub Enterprise Cloud retains `git.clone`, `git.fetch`, and `git.push` events only seven days. Without external streaming, the full exfiltration scope may be unrecoverable.

Investigation order from Wiz's playbook: contain (revoke the token), expand the timeline from audit logs, identify the leak source, enumerate every cloned repository, treat every valid secret inside those repositories as compromised, rotate, then hunt for unauthorized use of the rotated credentials in cloud and SaaS control planes.

## Related pages
- [Git hash chain malleability](git-hash-chain-malleability.md)
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [Browser-based developer IDE OAuth token theft](browser-based-developer-ide-oauth-token-theft.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- Datadog Security Labs: [https://securitylabs.datadoghq.com/articles/coordinated-github-api-enumeration/](https://securitylabs.datadoghq.com/articles/coordinated-github-api-enumeration/)
- The Hacker News: [https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html](https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html)
- Wiz CIRT GitHub PAT compromise campaign investigation: [https://www.wiz.io/blog/investigating-github-pat-compromise](https://www.wiz.io/blog/investigating-github-pat-compromise)
