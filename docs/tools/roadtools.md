# ROADtools

## Summary
**ROADtools** is an open-source Python framework for Microsoft Entra ID / Azure AD research and red-team work. Unit 42's May 2026 reporting emphasizes that multiple nation-state actors have operationalized ROADtools-style capabilities for cloud intrusions because the framework works through legitimate Microsoft APIs, can tune request attributes such as user-agent strings, and directly supports identity discovery, token exchange, and device registration.

The durable risk is not that ROADtools exists as a public tool; it is that Entra ID token workflows, device-registration trust, and Microsoft Graph enumeration can become attacker persistence and discovery paths after phishing, password spray, token theft, or endpoint compromise.

## Tags
- tools
- cloud
- Azure
- Entra ID
- Microsoft Graph
- ROADtools
- ROADrecon
- roadtx
- identity
- token theft
- token replay
- device registration
- persistence
- MFA bypass
- discovery
- defense evasion
- espionage
- nation-state
- APT29
- Midnight Blizzard
- Curious Serpens
- UTA0355

## Why this matters
- ROADtools gives operators a repeatable way to map Entra ID tenants, users, groups, devices, applications, service principals, roles, and directory relationships after obtaining access.
- The `roadtx` module can acquire, exchange, and reuse tokens, including flows that help attackers bypass repeated interactive MFA prompts.
- Device registration can turn a compromised account into a more durable cloud foothold by adding attacker-controlled devices to Entra ID.
- Legitimate Microsoft API use and configurable client traits make simple network allow/deny logic less reliable than behavior and identity-control monitoring.

## Operational characteristics
- **ROADrecon discovery:** enumerates users, groups, devices, service principals, applications, roles, and directory configuration into a local SQLite database with a web UI for relationship review.
- **Microsoft Graph transition:** Unit 42 notes that Azure AD Graph retirement has fragmented ROADrecon support; an official `msgraph` branch exists, while community forks continue partial Microsoft Graph enumeration support.
- **roadtx token workflows:** supports device code, refresh-token reuse, on-behalf-of-style exchanges, Primary Refresh Token workflows, and other OAuth/OIDC paths that can convert stolen material into fresh access tokens.
- **Device registration persistence:** `roadtx` can obtain an access token for Azure device registration and create Entra ID device entries, writing device certificates and keys locally for later use.
- **Default device artifacts:** Unit 42 calls out defaults such as Windows OS, OS version `10.0.19041.928`, and device names beginning with `DESKTOP-`; these are useful but weak indicators because operators can change them.
- **API blending:** ROADtools traffic uses legitimate Microsoft endpoints and can vary request attributes such as user-agent strings, pushing defenders toward identity telemetry correlation rather than single-string matching.

## Public actor usage
- **APT29 / Midnight Blizzard / Cloaked Ursa:** Microsoft reported ROADtools usage in 2021-era activity after targeted spear-phishing and delegated administrative privilege abuse.
- **Curious Serpens / Peach Sandstorm / APT33:** Microsoft reported ROADtools usage after password-spray initial access in 2023 operations.
- **UTA0355:** Volexity's 2025 reporting described targeted Microsoft 365 OAuth phishing where the operator registered a rogue device and acquired Microsoft Graph access; Unit 42 notes the tooling matched `roadtx` token-management capabilities.

## Defender heuristics
- Monitor Entra ID audit logs for unexpected device registration, device join events, and new device objects created shortly after risky sign-ins, password-spray activity, phishing reports, or impossible-travel anomalies.
- Hunt for suspicious defaults such as registered devices with OS version `10.0.19041.928`, generic `DESKTOP-` names, or device metadata inconsistent with the user's normal hardware fleet.
- Correlate token-refresh activity, Microsoft Graph enumeration bursts, and directory-read API calls against user role, device compliance, sign-in risk, and historical behavior.
- Watch for unusual OAuth flows, device-code authentication, refresh-token reuse from new infrastructure, or token use that bypasses expected interactive sign-in patterns.
- Restrict who can register or join devices, enforce strong Conditional Access and token protection where possible, and review service-principal / app permissions that allow broad directory reads.
- Treat ROADtools-like findings as cloud-intrusion evidence: preserve Entra ID audit/sign-in logs, Microsoft Graph activity, endpoint artifacts, and tenant configuration snapshots before making broad remediation changes.

## Related pages
- [APT29](../actors/apt29-cozy-bear-midnight-blizzard.md)
- [Microsoft Midnight Blizzard mailbox theft from Microsoft](../ops/microsoft-midnight-blizzard-mailbox-theft-from-microsoft.md)
- [Okta support-system compromise](../ops/cloudflare-okta-token-theft-incident.md)

## Sources
- Unit 42: https://unit42.paloaltonetworks.com/roadtools-cloud-attacks/
- ROADtools project: https://github.com/dirkjanm/ROADtools
- Volexity targeted OAuth phishing report: https://www.volexity.com/blog/2025/04/22/phishing-for-codes-russian-threat-actors-target-microsoft-365-oauth-workflows/
- Microsoft on NOBELIUM delegated administrative privilege abuse: https://www.microsoft.com/en-us/security/blog/2021/10/25/nobelium-targeting-delegated-administrative-privileges-to-facilitate-broader-attacks/
- Microsoft on Peach Sandstorm password spray operations: https://www.microsoft.com/en-us/security/blog/2023/09/14/peach-sandstorm-password-spray-campaigns-enable-intelligence-collection-at-high-value-targets/
