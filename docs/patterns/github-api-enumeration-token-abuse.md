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

## Related pages
- [Git hash chain malleability](git-hash-chain-malleability.md)
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [Browser-based developer IDE OAuth token theft](browser-based-developer-ide-oauth-token-theft.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/coordinated-github-api-enumeration/)
- [The Hacker News](https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html)
