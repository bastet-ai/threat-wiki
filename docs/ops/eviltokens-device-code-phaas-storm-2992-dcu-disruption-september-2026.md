# EvilTokens device-code PhaaS and the Microsoft DCU disruption (Sep 22, 2026)

## Summary

**EvilTokens** is a device-code phishing-as-a-service platform that Microsoft Threat Intelligence documents in a September 22, 2026 teardown and that the Microsoft Digital Crimes Unit (DCU), with partners, disrupted the same day under court authorization. Launched in February 2026, within months it was linked to **more than 12,000 compromised email inboxes across over 10,000 organizations worldwide** — the highest concentrations in the United States, Canada, the United Kingdom, Australia, India, and France, across wholesale distribution, construction, financial services, real estate, higher education, and healthcare.

The service's operator/support actor is tracked by Microsoft as **Storm-2992**. The platform's center of gravity is not the phish page but an **AI chatbot that analyzes the victim's own compromised mailbox** — summarizing and translating mail, mapping organizational roles, surfacing wire-transfer discussions, identifying "money movers" and the best people to impersonate, and even drafting the follow-on BEC messages. Microsoft's framing: AI was not just writing the lure, it was choosing the targets and designing the fraud. DCU calls this **its first court-authorized action against an end-to-end AI-enabled cybercrime service** (its 40th disruption overall).

The disruption (full-text captured by this wiki from the DCU post): **50 websites seized and 150+ supporting domains disabled** under authorization from the U.S. District Court for the Eastern District of Virginia, with **Health-ISAC as co-plaintiff** and operational help from **Cloudflare, Coinbase, OpenAI, Railway, SpyCloud, The Shadowserver Foundation, and TRM Labs**. In the UK, the Metropolitan Police Service cybercrime unit **arrested two men (32 and 38) on September 11, 2026**, seized devices, and released both on conditional bail. Investigators found evidence large portions of the kit were **"vibe coded"** (AI-built by its own creators) and that the service drew on **multiple AI models**.

## Tags
- ops
- phishing
- phishing-as-a-service
- PhaaS
- EvilTokens
- Storm-2992
- device-code phishing
- OAuth device authorization grant
- token theft
- token replay
- business email compromise
- BEC
- AI-enabled cybercrime
- AI-assisted phishing
- inbox analysis
- Microsoft Digital Crimes Unit
- DCU
- disruption
- court order
- Metropolitan Police Service
- Health-ISAC
- Cloudflare
- Coinbase
- OpenAI
- Railway
- SpyCloud
- Shadowserver
- TRM Labs
- vibe coded
- Cloudflare Workers
- Vercel
- AWS Lambda
- serverless abuse
- Conditional Access
- PRT
- device registration
- inbox rules
- session revocation
- Microsoft 365
- Entra ID
- Huntress
- Forg365
- Kali365
- BlueKit

## Reported activity

### The kit (Microsoft Threat Intelligence, Sep 22)
- Emerged **February 2026**; sold through **Telegram** by Storm-2992 at a **$1,500 initiation fee + $500/month**, with paid add-ons (Antibot redirector, B2B Sender, Office 365 Capture Link, SMTP Sender) and crypto-referral rewards.
- Panel-driven campaigns: deployment choice (**Cloudflare Workers / Bunny or PHP hosting**), capture mode, layout/template, **44 email themes** (invoices, RFPs, shared files, document signing, voicemail/eFax, password-expiry), page language, CAPTCHA gate, "AI Mode."
- **Device code flow abuse end-to-end:** a background script on the lure page talks to the real Microsoft identity provider in real time to mint a live device code, displays it with a copy button, then redirects to the genuine `microsoft.com/devicelogin`. The script polls the operator's `/state` endpoint every 3–5 s (`checkStatus()`) waiting for the victim to paste the code; already-signed-in users authenticate the attacker's session with a single paste, **no password exposed, MFA never challenged**. Code auto-copies to the clipboard to minimize friction.
- **April 2026 infrastructure observation:** campaign automation spun up **thousands of unique, short-lived polling nodes on serverless/automation platforms** running Node.js backend logic, defeating signature/pattern detection end-to-end — from device-code generation through post-compromise. Observed heavy abuse of **Vercel (`.vercel.app`), Cloudflare Workers (`.workers.dev`), and AWS Lambda** for redirect logic so phishing traffic blends with legitimate enterprise cloud traffic; redirects also chained through compromised legitimate domains. Huntress' related Railway.com abuse write-up is cited by Microsoft ("Riding the Rails").
- Delivery evasion: image-links, multi-stage redirection, multi-stage attachments, fake CAPTCHA gates before any content renders.
- Post-compromise: within ~10 minutes of some breaches, **new device registrations to mint a PRT** (Primary Refresh Token) for long-term persistence; in others, delayed malicious **inbox rules** to conceal communications, and **Microsoft Graph reconnaissance** to map org structure and permissions. Stolen tokens support mailbox exfiltration, token auto-refresh, keyword alerting to the operator via Telegram, and admin detection inside the panel.
- **AI layer:** after compromise, the kit's AI reviewed mailbox pools to pick high-value targets (financial/executive/administrative roles), then for financial-authority profiles ran deep recon for wire-transfer details, pending invoices, and executive correspondence. Preset prompts: find wire-transfer discussions, identify "money movers," locate vendor invoices, pick impersonation candidates.

### Scale and disruption (DCU, Sep 22)
- **>12,000 inboxes / >10,000 organizations** worldwide linked to the service since February.
- Civil action + coordinated ops: **50 websites seized, 150+ domains disabled**; partners Cloudflare, Coinbase, OpenAI, Railway, SpyCloud, Shadowserver, TRM Labs; Health-ISAC co-plaintiff (healthcare among the targeted verticals).
- **Met Police arrests Sep 11, 2026** (two men, 32 and 38, on conditional bail, devices seized).
- Microsoft notified affected customers and helped remediate; DCU characterizes the model, not just the infrastructure, as the durable threat: assume an attacker with AI inside an inbox "understands it in minutes, not days."

## Durable defender reads

1. **The device-code flow itself is the phishable surface.** The victim interacts only with genuine Microsoft surfaces; there is no fake login page to spot. Microsoft's standing recommendation: **block device code flow wherever possible**; where Teams devices need it, scope the exception to Teams device resource accounts and exclude the Device Registration Service resource from the Conditional Access policy.
2. **Revoking sessions is not containment.** Microsoft's observation: standard revocation often invalidates only refresh tokens, **leaving access tokens live up to an hour** — hands-on operators work inside that window. Their guidance is to **temporarily DISABLE the compromised account**, not just revoke, plus `revokeSignInSessions`, plus audit for attacker-registered devices/PRTs and attacker-created inbox rules (the same IR-audit-beyond-rotation posture this wiki recorded for BlueKit's auto-enrolled TOTP persistence).
3. **Serverless platforms are the redirect rail, not the payload.** Domain-blocklisting is structurally outgunned when redirect logic lives on `.vercel.app` / `.workers.dev` / AWS Lambda / Railway. Correlate device-code authentications with recent URL-click telemetry on the recipient's endpoint (Microsoft publishes the `AlertInfo`→`EmailEvents`→`IdentityInfo`→`DeviceEvents BrowserLaunchedToOpenUrl` join as an Advanced-hunting query) instead of scoring the destination domain.
4. **Detection grammar shipped with the report:** Defender detections span anomalous OAuth device-code authentication, anomalous token exchange, device join/registration after device-code sign-in, anomalous Graph API volume/POST activity after the flow, and suspicious inbox-rule creation; Sentinel queries cover phishing-link clicks and delivered-threat triage. Threat-analytics technique profile: Device code phishing.
5. **AI-in-the-loop PhaaS is now a product category with pricing.** $1,500 + $500/mo buys identity attack, mailbox intelligence, target selection, and fraud drafting in one panel; "vibe coded" and multi-model are tells of the next builder cohort. Independent verification of a compromise should not depend on the victim's own AI-tooling telemetry (the self-compromise-for-bounty failure mode this wiki recorded on PhantomRaven sits adjacent to this design).
6. **Disruption is not remediation** — the standing rule from Kratos and FakeCap-class takedowns: sessions, PRTs, inbox rules, and copied kits survive the domain seizures.

## Related pages
- [Forg365 Microsoft 365 PhaaS](forg365-microsoft-365-phaas.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [Evilginx and device-code phishing open-directory cluster](evilginx-device-code-phishing-open-directory.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [BlueKit Browser-in-the-Middle PhaaS and TOTP-enrollment persistence](bluekit-browser-in-the-middle-phaas-totp-enrollment-persistence-spycloud-september-2026.md)
- [Kratos Microsoft 365 PhaaS and infrastructure disruption](kratos-microsoft-365-phaas-disruption.md)
- [Collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)
- [PhantomRaven LLM-generated npm infostealer (self-manufactured compromise)](../tools/phantomraven-llm-generated-npm-infostealer-bug-bounty-hunter-crowdstrike-september-2026.md)

## Sources
- Microsoft Security Blog (Threat Intelligence, Sep 22, 2026, full text captured via RSS by this wiki): [https://www.microsoft.com/en-us/security/blog/2026-09-22/unmasking-eviltokens-getting-to-the-root-of-device-code-phishing/](https://www.microsoft.com/en-us/security/blog/2026-09-22/unmasking-eviltokens-getting-to-the-root-of-device-code-phishing/)
- Microsoft On the Issues / DCU (Steven Masada, Sep 22, 2026, full text captured): [https://blogs.microsoft.com/on-the-issues/2026-09-22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/](https://blogs.microsoft.com/on-the-issues/2026-09-22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/) (shortlink `https://aka.ms/ETDisruption`)
- Huntress, "Riding the Rails: Threat Actors Abuse Railway.com PaaS as Microsoft 365 Token Attack Infrastructure": [https://www.huntress.com/blog/railway-paas-m365-token-replay-campaign](https://www.huntress.com/blog/railway-paas-m365-token-replay-campaign)
- Microsoft device-code Conditional Access guidance: [https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-teams-devices-device-code-flow](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-teams-devices-device-code-flow)
