# Azure CLI LSHIY password-spray campaign

## Tags
- ops
- operations
- Azure CLI
- Microsoft Entra ID
- Microsoft 365
- password spraying
- credential stuffing
- identity attacks
- cloud identity abuse
- Conditional Access
- MFA bypass
- ROPC
- OAuth
- LSHIY
- AS32167
- IPv6
- Huntress
- The Hacker News

## Summary
Huntress reported an ongoing automated password-spray campaign against Microsoft's Azure command-line interface (CLI) that originated primarily from the `2a0a:d683::/32` IPv6 range associated with LSHIY LLC / AS32167. Between June 12 and June 26, 2026, Huntress observed more than 81 million login attempts against customer accounts, with at least 78 Microsoft accounts compromised across 64 organizations.

The campaign is durable for defenders because it shows how legacy or poorly covered authentication flows can turn "MFA enabled" into a false sense of safety. The actor validated known username/password combinations through the OAuth Resource Owner Password Credentials (ROPC) flow, which can mint user-delegated tokens without an interactive MFA prompt when Conditional Access policies are not scoped to cover all users, all cloud apps, and all client app types.

## Public reporting
- **2026-07-01:** Huntress published "No (Bad) CAP: Inside an Ongoing LSHIY Password Spray Attack," describing a massive, ongoing password-spray campaign against Azure CLI.
- Huntress said the observed June 12-26 window included more than 81 million login attempts, 78 compromised user accounts, and 64 affected organizations.
- The Hacker News amplified Huntress' findings the same day, highlighting that many affected organizations had Conditional Access policies but gaps in app, user, location, or enforcement coverage allowed the attack path to succeed.

## Tradecraft
1. The actor uses username/password combinations that appear to come from previously compromised credential lists.
2. Attempts are replayed at scale against Microsoft identity endpoints through Azure CLI authentication paths.
3. Valid credentials are used through the OAuth ROPC flow, where a direct username/password request to a tenant token endpoint can mint a delegated token.
4. ROPC does not support modern interactive MFA / SSO prompts in the way browser-based authorization flows do, so Conditional Access policy gaps can prevent MFA from firing.
5. Huntress observed a June 22 spike with 30 compromised identities across 23 businesses; in that spike, many organizations had MFA enforced but not in a way that covered the specific Azure CLI / ROPC path.

## Indicators and pivots
### Network / infrastructure
- `2a0a:d683::/32`
- `AS32167`
- LSHIY LLC

### Identity telemetry
- High-volume failed and successful sign-ins to Azure CLI or Microsoft first-party CLI application contexts.
- Sign-ins using ROPC / non-interactive token grant behavior rather than browser-based authorization.
- Successful sign-ins where Conditional Access expected MFA but the sign-in path did not trigger an MFA challenge.
- Source geolocation inconsistencies. Huntress noted that some telemetry geolocated activity to China while other third-party tooling placed some IPs in the United States, affecting trusted-location logic.
- Accounts with stale passwords that match previously breached credential combinations.

## Defender takeaways
- Treat "MFA enabled" as insufficient unless Conditional Access is enforced for **all users**, **all cloud apps**, and **all client app types** or an explicit block covers legacy/non-interactive flows.
- Review Entra ID / Microsoft 365 sign-in logs for Azure CLI, ROPC, non-interactive sign-ins, and user-delegated token issuance that bypassed expected MFA prompts.
- Where business workflows allow, restrict Azure CLI access for non-admin users and block ROPC-style authentication paths.
- Audit Conditional Access policies for common holes: policies scoped only to admin portals, only to privileged groups, only to non-trusted locations, or left in report-only mode.
- Prioritize response based on confirmed credential validity and successful sign-ins, not only spray volume; broad spray noise can hide the smaller set of compromised accounts.
- Rotate exposed passwords, revoke sessions and refresh tokens for confirmed-compromised accounts, and check downstream mailbox, OAuth app consent, forwarding, cloud resource, and SaaS activity.

## Related pages
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)
- [Klue Salesforce OAuth token abuse](klue-salesforce-oauth-token-abuse.md)
- [FortiBleed Fortinet credential exposure](fortibleed-fortinet-credential-exposure.md)

## Sources
- Huntress: [https://www.huntress.com/blog/lshiy-password-spray-attack](https://www.huntress.com/blog/lshiy-password-spray-attack)
- The Hacker News: [https://thehackernews.com/2026/07/azure-cli-password-spray-hits-at-least.html](https://thehackernews.com/2026/07/azure-cli-password-spray-hits-at-least.html)
