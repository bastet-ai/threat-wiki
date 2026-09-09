# Microsoft: passkey-themed social engineering leads to identity and cloud compromise — Storm-3121 / Storm-3032 ecosystem

## Summary
On **September 9, 2026**, Microsoft Security Research published a research post documenting **active cloud-based intrusions observed since May 2026** across multiple accounts, in which the opening move is **identity-focused social engineering dressed up as passkey / MFA / SSO "helpdesk" activity**. The durable sequence, repeated across engagements, is: **phone-based social engineering → AiTM phishing or device-code flow → actor-registered MFA method (persistence) → Microsoft Graph reconnaissance → high-volume SharePoint / OneDrive / Exchange data collection and suspected exfiltration**, all through **proxy-associated infrastructure**.

Microsoft Threat Intelligence assesses that the initial-access activity is used by **a range of threat actors, including Storm-3121 (which conducts initial-access activity leading to ShinyHunters and Falcon extortion) and Storm-3032 (actors that splintered from the BlackFile group and now operate under the Helix extortion banner)**, as well as others. The post publishes a full KQL/Sentinel hunt kit and a Graph reconnaissance pattern matrix.

## Tags
- ops
- operations
- Microsoft
- Microsoft Security Research
- social engineering
- passkey
- MFA
- adversary-in-the-middle
- AiTM
- device code phishing
- MFA persistence
- Microsoft Graph
- identity compromise
- data exfiltration
- Storm-3121
- Storm-3032
- BlackFile
- ShinyHunters
- Helix
- extortion
- phishing infrastructure
- domain impersonation
- conditional access
- phishing-resistant MFA

## The attack chain
### Initial access: passkey and SSO lures
- The attack usually begins with a **call or SMS on the victim's personal phone** from someone claiming to be the organization's IT helpdesk, creating urgency that a **passkey, MFA, or SSO configuration must be updated immediately** to avoid disruption, with a link to a site that closely resembles the legitimate Microsoft sign-in experience.
- The passkey narrative is **pretext, not objective**: it exists to drive the victim into an **adversary-in-the-middle (AiTM) phishing** or **device-code authentication** flow. In AiTM the actor captures credentials and session tokens; in the device-code flow the victim approves a token for an attacker-controlled client, and the token can then be replayed — **bypassing MFA** without a stolen browser cookie.
- Lures are **personalized**: pre-attack research on employees and org structure (social/professional platforms), and — where an account is already compromised — passkey-themed messages **sent through Microsoft Teams from a trusted employee identity**, which significantly raises engagement.
- If the victim opens the link on a **personal, unmanaged device** (not onboarded to Defender for Endpoint), endpoint telemetry is absent; the employee's recollection of the call/text is often the only early evidence.

### Phishing infrastructure: reusable domains, victim-name subdomains
- Rapidly deployed phishing infrastructure around themes: **passkeys, SSO enrollment, account activation, identity verification**.
- Generic domains are registered and the **target organization's name is embedded as a subdomain** — `contoso[.]add-passkey[.]com` — so the URL looks familiar; multiple domains per target allow rotation. Domains are **operational within hours**, and are often registered with **Nicenic** (a registrar previously observed in extortion campaigns — Microsoft notes registration alone is not evidence of registrar involvement).
- Observed themes: passkey (`passkeyhelpdesk[.]com`, `secure-passkey[.]com`, `setupmypasskey[.]com`, `add-passkey[.]com`), SSO/IdP (`integratedsso[.]com`, `oktasession[.]com`), key setup/sync (`keysyncos[.]com`, `oskeysync[.]com`, `oskeysetup[.]com`, `oskeyregister[.]com`, `syncmykey[.]com`, `myconnectkey[.]com`, `oskeyconnect[.]com`), setup/verification (`validationsetupac[.]com`, `portalsetuphub[.]com`).

### Identity compromise, then MFA persistence
- Observed sequences: (a) anomalous `OfficeHome` sign-in from an unmanaged context → MFA (non-phishing-resistant) completed via AiTM → same session enumerates **My Apps**, **My Sign-Ins**, **Microsoft Approval Management**, **Account Controls**, then SharePoint/OneDrive via Graph; (b) device-code flow after the passkey lure, token replay; (c) sign-in with **compromised credentials where MFA was approved by a PhoneAppOTP method the actor had registered days earlier** — pre-seeded persistence, driven by an automated **Node.js + Microsoft Graph** system.
- **First objective after access: enroll an actor-controlled MFA method** — a new phone number, authenticator app, or **software-based OTP token**. Microsoft shows a real-world `Update user.` / `StrongAuthenticationPhoneAppDetail` record in which a second entry appears with `DeviceName: NO_DEVICE`, `DeviceTag: SoftwareTokenActivated`, `AuthenticationType: 2` — a durable, attacker-controlled factor that survives until explicitly removed.

### Graph reconnaissance
- A deliberate, multi-stage inventory of the tenant: `/organization`, `/subscribedSkus`, `/licenseDetails` (tenant profile); `/users`, `/groups`, `/members`, `/transitiveMembers` (directory); `/directoryRoles`, `/roleManagement`, `/authentication/methods` (privilege + MFA discovery); `/applications`, `/servicePrincipals`, `/oauth2PermissionGrants`, `/appRoleAssignments` (application + consent discovery); `/sites`, `/lists`, `/drives`, `/drive/items`, `/root/children`, `/search` (SharePoint/OneDrive discovery); `/messages`, `/mailFolders`, `/attachments` (mailbox discovery); with **automation/pagination** (`$top`, `$skip`, `$skiptoken`, `/delta`, `/search`).
- **No single Graph call looks suspicious** — `/users` or `/groups` is routine. The tell is **one identity/application/token systematically traversing multiple recon categories, then content endpoints, from the same source context** — assessed holistically, not call-by-call. Infrastructure rotates across the lifecycle (different IPs for auth, recon, and exfil), so correlation across stages, not per-IP blocklists, is the detection.

### Collection and suspected exfiltration
- High-volume **SharePoint Online and OneDrive** `FileAccessed` / `FileDownloaded` activity, plus **Exchange Online access via REST APIs** (mailbox and attachment retrieval).
- The pace is **deliberately throttled** — **fewer than 1,000 files or emails per hour** — spanning **hours to days**, blending into normal enterprise usage while steadily extracting large volumes.
- A **`python-httpx` user agent** was associated with high-volume SharePoint/OneDrive access in several cases; Microsoft is explicit that the user agent alone is not malicious — evaluate volume, identities, source infrastructure, and prior identity-compromise evidence together.
- Exfiltration paths in the hunt kit: anonymous-proxy CloudAppEvents, `One Outlook Web` REST event bursts (≥500/hour per account/IP), and `python-httpx` download windows (≥100 files/2h).

## Attribution
Microsoft Threat Intelligence assesses the initial-access activity is used by **a range of threat actors**, and names **Storm-3121** (initial access leading to **ShinyHunters** and **Falcon** extortion) and **Storm-3032** (a splinter of **BlackFile**, now operating under the **Helix** extortion banner). Activity observed **since May 2026**. No named malware family, C2 infrastructure, or victim list is published; domains/IPs/hosting providers "can change quickly."

## Defender guidance (from the post)
1. **Investigate as a connected sequence:** unusual sign-in → authentication-method enrollment → Graph reconnaissance → token issuance → abnormal SaaS download / mailbox activity. Prioritize unusual sign-ins followed by new auth-method registration.
2. **Hunt the Graph recon matrix:** identities/applications touching **≥3 recon categories from the same IP within 30 minutes** (the published query thresholds: ≥10 requests, ≥3 categories, ≥6 distinct paths); control-plane recon on `/directoryRoles`, `/authentication/methods`, `/oauth2PermissionGrants`; repository discovery via `/search`, `/delta`, `$skiptoken`/`$top` paging; mailbox/attachment enumeration (≥3 attachment requests in a window).
3. **Hunt exfil:** `One Outlook Web` REST bursts, `python-httpx` + uncommon-for-user ISP/user-agent on download events, anonymous-proxy CloudAppEvents.
4. **Contain confirmed compromises:** revoke sessions and refresh tokens, reset credentials, **remove attacker-registered authentication methods and mailbox rules**, require secure re-registration.
5. **Reduce future risk:** do not treat an IP/domain match as conclusive — validate behavior, persistence events, and data-access volume; **enforce phishing-resistant MFA (FIDO2/passkeys, Windows Hello for Business) via Conditional Access**; require **managed, compliant devices** for Exchange, SharePoint, and Graph-privileged apps; keep the passkey/MFA-update pretext on the phishing blocklist and train helpdesk-aware verification (call back through known numbers before acting on "MFA update" requests).

## Durable read
The passkey is a **smokescreen, not the target**: the campaign's value is in **converting a human into a token issuer** (AiTM or device-code) and then **installing an attacker-owned MFA factor** so the compromise outlives every password and session reset that doesn't specifically remove the registered method. Defenders should treat **"new authentication method added after an unusual sign-in"** as a near-always-investigate event, and hunt **behavioral progression** (recon → collection → exfil) instead of single-call anomalies.

## Related pages
- [Impersonating IT support: human-operated Teams external-collaboration intrusion impersonating IT/helpdesk](microsoft-teams-it-support-impersonation-msi-nodejs-implant-winrm-september-2026.md)
- [CISA KEV September 9, 2026 additions: four exploited flaws — Citrix NetScaler, Fortinet, Cisco FMC, Chrome V8](cisa-kev-citrix-fortinet-cisco-chromium-september-9-2026.md)
- [Unit 42 Pass-ta-key: synced-passkey theft research](../notes/source-index.md) (source watch)

## Sources
- Microsoft Security Blog: [Passkey-themed social engineering leads to identity and cloud compromise](https://www.microsoft.com/en-us/security/blog/2026/09/09/passkey-themed-social-engineering-leads-identity-cloud-compromise/) (Sep 9, 2026; Microsoft Security Research + Defender Experts)
- BOD 26-04 (context for federal patch deadlines on same-day KEV items): [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
