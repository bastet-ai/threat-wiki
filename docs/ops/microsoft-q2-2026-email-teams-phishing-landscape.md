# Microsoft Q2 2026 email and Teams phishing landscape

## Summary
Microsoft Threat Intelligence's Q2 2026 review measures a sharp post-disruption decline in Tycoon2FA activity alongside continued migration into Microsoft Teams social engineering, especially voice phishing. Microsoft detected about 7.6 billion email-based phishing threats during the quarter. Credential phishing remained the objective in 94–96% of malicious-payload attacks, while weekly malicious Teams call attempts ended June at nearly ten times the mid-2025 baseline.

Two campaigns provide durable defender pivots: an automated business email compromise operation reached more than 67,000 users at more than 42,000 organizations in under three hours, and a nested-EML / calendar-invite campaign targeted more than 107,000 users at nearly 19,000 organizations before using a Microsoft authentication redirect to deliver a batch-file malware dropper.

## Tags
- ops
- Microsoft Threat Intelligence
- phishing
- Microsoft Teams
- vishing
- Tycoon2FA
- business email compromise
- credential theft
- calendar invitation
- OAuth redirect
- Amazon SES
- ClickUp
- Pixeldrain
- malware delivery

## Q2 landscape

### Tycoon2FA disruption effect
- Tycoon2FA-linked phishing volume fell to 1.5 million messages in May and 1.2 million in June, about 8% of its second-half 2025 monthly baseline and a reported 92% decline since Microsoft's March disruption began.
- Its share of CAPTCHA-gated phishing sites fell from 41% in March to 12% in June. Its share of QR-code campaigns fell from 20% to 14% over the same period.
- More than 40% of newly observed Tycoon2FA domains used the `.RU` top-level domain during Q2 after the platform was forced off Cloudflare.
- No replacement phishing service reached comparable scale during the quarter. This is evidence of sustained disruption impact, not evidence that phishing demand disappeared.

### Delivery and payload shifts
- Microsoft detected about 7.6 billion email phishing threats, declining from 2.7 billion in April to 2.4 billion in June.
- QR-code phishing fell from 17.4 million attacks in April to 8.3 million in June. PDF delivery remained dominant but fell to 58% of QR attacks, while DOC/DOCX rose to 40%.
- CAPTCHA-gated phishing fell from 8.2 million attacks in April to 2.2 million in June. SVG delivery rebounded from 5% in April to 26% in June, and embedded URLs returned to the largest share in June even though their raw volume remained historically low.
- Credential phishing accounted for 94–96% of malicious payloads; traditional malware delivery accounted for 4–6%.
- ICS calendar invitations remained a small share, about 4%, but increased 277% in June. Calendar objects deserve separate controls because they can place attacker content into a user's calendar without the normal attachment-open path.

### Teams and vishing migration
- Detected Teams phishing rose 19% from March to April, remained roughly flat in May, and increased another 10% in June.
- Technical-support and account-lockout themes remained dominant, but 52% of June attacks used generic display names rather than conspicuous IT/helpdesk branding.
- Sender naming shifted toward SaaS, scan/update, and infrastructure terminology, which Microsoft assesses may align with broader ClickFix-style update/fix lures.
- Average weekly malicious Teams calls rose 31% from April to May and 27% into June. Weekly attempts were about 80% higher than at the start of 2026 and nearly ten times the mid-2025 baseline.
- Calls concentrated between 14:00 and 20:00 UTC on weekdays, with near-zero weekend activity.

## Reported campaigns

### Automated aging-report and payroll-diversion BEC
On June 1, an actor sent messages to more than 67,000 users across more than 42,000 organizations between 14:08 and 16:52 UTC. The operation first impersonated sales executives to request aging reports and customer contacts, then impersonated CEOs or presidents to redirect payroll.

The actor:
- generated mail with Python's `email.mime`, leaving its default `===============[integer]==` MIME-boundary pattern;
- sent through Amazon SES, producing SES-style `Feedback-ID` and `Message-ID` values;
- used the DKIM-configured Slovak domain `ecajovna[.]sk`, allowing SPF and DKIM alignment;
- targeted role mailboxes such as `ar`, `accountsreceivable`, `hr`, and `payroll`;
- used per-message 1×1 SES engagement pixels to prioritize recipients who opened the lure; and
- directed replies to lookalike mail domains `ilyff[.]com`, `j-gmails[.]com`, and `x2mails[.]com`.

The messages contained no malicious link or attachment. Detection therefore depends on sender/reply-to mismatch, role-mailbox targeting, impersonation, unusual SES automation patterns, and business-process verification rather than payload scanning alone.

### Nested EML, calendar invite, OAuth redirect, and BAT dropper
Between June 14 and 15, a campaign reached more than 107,000 users at nearly 19,000 organizations, almost exclusively in the United States. Messages impersonated an internal financial/staff-update function and included:
- a nested EML named `Re: Teams Archive Recording for {{DATE2}}.eml`, preserving an unfilled template token;
- an ICS invitation addressed to placeholder administrative accounts at the recipient domain; and
- a voicemail-style action inside the EML that linked to `login.microsoftonline[.]com`.

The link requested silent authentication to an attacker-registered multitenant Entra application. When no session could satisfy the request, Microsoft's authentication service redirected the browser to the application's registered destination on ClickUp's public attachment host. That destination served `Financial_report.bat`, which launched hidden PowerShell, downloaded `installer.exe` from Pixeldrain into the user's temporary directory, ran it silently, and removed the batch dropper. The Microsoft-hosted first link made the chain look safer to users and URL scanners; Microsoft reports malware delivery rather than credential theft as the final objective.

## Defender heuristics

### Email, calendar, and collaboration controls
- Inspect nested EML and ICS content rather than treating the outer message as the complete object. Flag literal template tokens such as `{{DATE2}}` and organization-branded “Teams archive” or staff-update lures.
- Monitor calendar invitations that target nonexistent, generic, or administrative local-part addresses and correlate them with matching inbound mail.
- Alert when external or newly observed tenants initiate support-themed Teams chats or calls, especially around account lockout, scanning, updates, or urgent remediation.
- Baseline and restrict external Teams communication where business needs permit. Include Teams messages and calls in phishing simulations and user reporting workflows.
- Require out-of-band verification for aging-report disclosure, payroll changes, and executive financial requests, even when mail passes SPF and DKIM.

### Identity and redirect controls
- Review multitenant Entra applications, redirect URIs, consent activity, and sign-in flows that begin at Microsoft authentication endpoints but terminate on public file-hosting services.
- Do not treat `login.microsoftonline.com` as a terminal allow-list decision. Resolve and inspect the full redirect chain and final downloaded object.
- Use phishing-resistant MFA for privileged and high-risk accounts, and investigate adversary-in-the-middle alerts and unusual silent-authentication requests.

### Endpoint and network hunting
- Hunt for `Financial_report.bat`, `installer.exe` launched from user temporary paths, hidden PowerShell spawned by batch files, and rapid dropper deletion.
- Review requests to `clickup-attachments.com` and `pixeldrain.com` that follow Microsoft authentication redirects or originate from email/calendar clients.
- Search mail telemetry for the Python `email.mime` boundary pattern, Amazon SES identifiers, mismatched reply-to domains, open-tracking pixels, and high-volume messages directed at finance/HR role accounts.
- Preserve the outer email, nested EML, ICS, redirect chain, downloaded files, Entra application identifiers, endpoint process tree, and proxy/DNS evidence during response.

## Public indicators

### June 14–15 malware-delivery campaign
- `9i6pokerdepot[.]com`
- `Customer.Service[@]9i6pokerdepot[.]com`
- `t90141296286.p.clickup-attachments[.]com`
- `hxxps://t90141296286.p.clickup-attachments[.]com/t90141296286/fb39c3a9-3161-40ad-847b-0683e0409d6f/Financial_report.bat`
- `hxxps://pixeldrain[.]com/api/file/3v92oJiL`
- `Re: Teams Archive Recording for {{DATE2}}.eml`
- `Financial_report.bat`

### June 1 BEC campaign
- `ecajovna[.]sk`
- `ilyff[.]com`
- `j-gmails[.]com`
- `x2mails[.]com`

Indicators are historical observations from Microsoft, not standalone attribution. Public hosting services should be scoped to exact paths and correlated behavior rather than blocked indiscriminately.

## Related pages
- [UNC6692 SNOW malware social-engineering campaign](unc6692-snow-malware-social-engineering.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [O-UNC-066 Entra passkey vishing](o-unc-066-entra-passkey-vishing.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)

## Sources
- Microsoft Security Blog: [https://www.microsoft.com/en-us/security/blog/2026/07/23/email-threat-landscape-q2-2026-trends-and-insights/](https://www.microsoft.com/en-us/security/blog/2026/07/23/email-threat-landscape-q2-2026-trends-and-insights/)
