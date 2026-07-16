# Evilginx and device-code phishing open-directory cluster

## Summary
Lexfo's July 2026 investigation started from an exposed Python `http.server` directory listing on **185.163.204[.]7:8080** and unfolded into three Microsoft 365 phishing operations using custom Evilginx forks and Microsoft OAuth device-code abuse.

The cluster is useful defensively because it places two different identity-phishing paths side by side: transparent adversary-in-the-middle proxying that steals Microsoft 365 session cookies, and device-code flow abuse where the victim authenticates on the legitimate Microsoft device-login page and authorizes the attacker's session.

## Tags
- ops
- phishing
- Microsoft 365
- Microsoft Entra ID
- Evilginx
- adversary-in-the-middle
- device-code phishing
- OAuth device authorization grant
- MFA bypass
- session cookie theft
- token theft
- token replay
- phishing-as-a-service
- The Quarry
- MaDoO Blaster
- codemado
- mail-argenta
- saroula01
- Lexfo
- The Hacker News
- SOCRadar
- AI-assisted malware
- AI-assisted development
- SimpleHelp
- RMM abuse
- Cloudflare Tunnel

## Reported activity
- Lexfo found a live attack server at **185.163.204[.]7** in Budapest exposing phishing configurations, credential-harvesting logs, backup archives, RMM installers, combolists, Telegram session files, and shell history.
- The shell history pointed to public GitHub repositories and Evilginx forks tied to the operator Lexfo tracks as **codemado**, who used **picis[.]net** for Microsoft 365 AiTM phishing.
- The codemado operation used Microsoft 365-themed lure paths for Office, OneDrive, Authenticator, Adobe, DocuSign, and SharePoint pretexts, plus Cloudflare Tunnel fronting and a multi-tool RMM arsenal.
- Lexfo pivoted from the exposed server to two additional custom Evilginx forks: **red-queen**, attributed by Lexfo to **mail-argenta**, and **black-queen**, associated with **saroula01**.
- The **red-queen** fork modified Evilginx behavior to rename `crossorigin` and `integrity` attributes, add URL rewriting in `http_proxy.go`, pre-fill victim email addresses, and set long-lived Microsoft session-cookie TTLs.
- The **black-queen** fork used the Microsoft OAuth device-code flow rather than password capture: victims were driven to the legitimate Microsoft device-login page while the backend polled for the resulting token.
- Lexfo reported **218 distinct captured accounts** across 12 countries in black-queen Telegram logs from June 2025 to July 2026, with roughly 94% corporate mailboxes; token files in repository history showed auto-refresh behavior.
- Lexfo and The Hacker News link codemado's **MaDoO Blaster** bulk-mailer promotion to SOCRadar's **The Quarry** PhaaS ecosystem as a supplier relationship, not proof that all three operators belonged to that ecosystem.
- Lexfo found signs of AI-assisted development in surrounding glue code, phishlets, and commits across the operations, while noting that the Evilginx core changes themselves were comparatively small.

## Why this matters
- **Passkeys and FIDO2 help against Evilginx-style proxy phishing but not device-code authorization abuse.** In device-code phishing, the user authenticates on the real Microsoft origin and satisfies real MFA while authorizing an attacker-controlled session.
- **Long-lived refresh tokens matter more than one-time credential theft.** Lexfo observed token auto-refresh and repeated captures consistent with maintaining access after initial authentication.
- **Public Evilginx forks lower the bar.** The operators mostly wrapped and lightly customized open-source tooling, then added lure, automation, RMM, and campaign-management code.
- **Misconfigured attacker infrastructure remains a defender intelligence source.** Exposed directories, repository history, and shell history linked tooling, operators, infrastructure, and campaign telemetry.

## Defender guidance
1. Block or tightly scope the Microsoft OAuth device-code flow with Conditional Access wherever it is not required. Test in report-only mode before enforcement for legitimate Teams room devices, command-line tools, or constrained-device workflows.
2. Hunt Entra sign-in logs for device-code flow usage and token refreshes from unfamiliar IPs, geographies, devices, or user agents, especially for users who do not normally use device-login workflows.
3. Monitor refresh-token grants involving the Microsoft Office client ID **d3590ed6-52b3-4102-aeff-aad2292ab01c** where that client and device-code flow are abnormal for the tenant.
4. Pair phishing-resistant MFA with Continuous Access Evaluation and location/device-based Conditional Access so stolen cookies or refresh tokens are re-evaluated when source network, device, or risk changes.
5. Treat user reports of Authenticator-themed device-code prompts, QR-code login prompts, or requests to visit `microsoft.com/devicelogin` as identity incidents, not only user-awareness failures.
6. Review for downstream persistence after suspected compromise: mailbox rules, OAuth grants, application consents, SharePoint/OneDrive access, Teams activity, RMM deployment, and password/MFA method changes.
7. Block or inspect access to known phishing infrastructure and patterns, including recently registered Microsoft-themed subdomains, Cloudflare Tunnel fronting, and lure paths imitating Office, OneDrive, Authenticator, DocuSign, Adobe, and SharePoint.

## Related pages
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [O-UNC-066 Entra passkey vishing](o-unc-066-entra-passkey-vishing.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)

## Sources
- Lexfo: <https://blog.lexfo.fr/opendir-to-phishing-operator.html>
- The Hacker News: <https://thehackernews.com/2026/07/misconfigured-server-reveals-three.html>
- Microsoft device-code Conditional Access guidance: <https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-teams-devices-device-code-flow>
- Microsoft Storm-2372 device-code phishing report: <https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/>
- Microsoft AI-enabled device-code phishing report: <https://www.microsoft.com/en-us/security/blog/2026/04/06/ai-enabled-device-code-phishing-campaign-april-2026/>
- SOCRadar The Quarry PhaaS report: <https://socradar.io/blog/the-quarry-phaas-irs-ssa-phishing/>
