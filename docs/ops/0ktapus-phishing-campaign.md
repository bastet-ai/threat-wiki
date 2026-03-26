# 0ktapus phishing campaign

## Tags
- ops
- operations
- identity
- smishing
- Okta
- Twilio
- MFA bypass
- Telegram

## Summary
The **0ktapus phishing campaign** was a 2022 SMS-phishing and voice-phishing operation against employees at organizations that used Okta or similar identity portals. [Group-IB](https://www.group-ib.com/blog/0ktapus/) coined the `0ktapus` name after tracking a large set of related phishing domains and a shared kit; [Okta](https://sec.okta.com/articles/scatterswine/) refers to related threat-actor activity as `Scatter Swine`; [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) later said researchers dubbed the malicious actors `0ktapus` or `Scatter Swine`. This page uses `0ktapus phishing campaign` as the primary title because it is the clearest cross-source shorthand for the operation, but the alias boundary should be treated as reporting-dependent rather than as a settled group identity.

Operationally, the campaign combined **employee-targeted smishing**, **lookalike Okta pages**, **real-time theft of passwords and OTP/TOTP codes**, and **follow-on abuse of admin consoles or customer-support tooling**. First-party reporting from [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/), [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack), [Okta](https://sec.okta.com/articles/scatterswine/), and [Signal](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know) shows the same broad pattern: steal phishable factors from employees, immediately reuse them for access, and then use provider-side visibility into SMS or identity workflows to expand victim impact.

## Naming and companion-page assessment
- [Group-IB](https://www.group-ib.com/blog/0ktapus/) named the campaign `0ktapus` based on the Okta-themed phishing infrastructure it tracked.
- [Okta](https://sec.okta.com/articles/scatterswine/) uses the actor label `Scatter Swine` for repeated phishing activity with similar tactics, infrastructure choices, and target sets.
- [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) says independent researchers dubbed the malicious actors `0ktapus` or `Scatter Swine`.
- No companion `Groups` or `People` page is published alongside this entry. The sources here strongly support the operation, but they do not cleanly resolve a durable crew boundary or a publicly confirmed human identity.

## Timeline
- **Since March 2022:** [Group-IB](https://www.group-ib.com/blog/0ktapus/) says it recovered data from `0ktapus` campaigns launched since March 2022.
- **2022-07-20:** [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) says attackers sent more than 100 SMS lures to employees and family members, using the newly registered domain `cloudflare-okta.com`; three employees entered credentials, but hardware-backed FIDO authentication blocked follow-on access.
- **2022-07-26:** [Group-IB](https://www.group-ib.com/blog/0ktapus/) says one client inquiry on July 26 kicked off the investigation that tied the infrastructure to a broader campaign.
- **2022-08-04:** [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) says it became aware of unauthorized access after employees were fooled by SMS messages and fake Okta login pages.
- **2022-08-15 to 2022-08-16:** [Signal](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know) says it notified about 1,900 potentially affected users and forced them to re-register their accounts.
- **2022-08-25:** [Okta](https://sec.okta.com/articles/scatterswine/) published detection guidance and said the actor had used previously stolen credentials plus Twilio-console access to search for OTP-related data tied to selected targets.
- **2022-10-27:** [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) published its investigation conclusion and linked the incident to the wider `0ktapus` / `Scatter Swine` wave.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### Group-IB
- [Group-IB](https://www.group-ib.com/blog/0ktapus/) says it identified **169 unique phishing domains** involved in the campaign.
- The same writeup says recovered campaign data included **9,931 compromised user credentials**, **5,441 compromised MFA codes**, and **136 unique email domains** belonging to compromised users.
- Group-IB says most targeted companies were in the United States and that IT, software, cloud, telecom, and financially relevant organizations were prominent in the victim data.

### Cloudflare
- [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) says the phish targeted employees with a fake Okta page hosted on DigitalOcean and registered through Porkbun less than an hour before the SMS wave began.
- Cloudflare says the phishing flow relayed credentials and TOTP material to the attacker in real time through Telegram-backed infrastructure, then attempted to log in from Windows systems over VPN.
- The same post says the kit also attempted to deliver AnyDesk remote-access software after credential collection, but Cloudflare's FIDO2 requirement prevented account takeover.

### Twilio and Authy
- [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) says attackers used stolen employee credentials to access internal Twilio administrative tools and customer information.
- Twilio's October 27, 2022 conclusion says **209 customers** and **93 Authy end users** were impacted, and that the last observed unauthorized activity was on **August 9, 2022**.
- Twilio also says there was **no evidence** that customer console passwords, authentication tokens, or API keys were accessed.

### Okta
- [Okta](https://sec.okta.com/articles/scatterswine/) says the actor searched for **38 unique phone numbers** in the Twilio console, nearly all linked to one targeted organization.
- Okta assesses that the actor used **previously stolen usernames and passwords** to trigger SMS MFA challenges, then used Twilio-console access to look up the resulting one-time passwords.
- Okta's writeup also documents recurring TTPs: bulk text lures, lookalike `-okta`, `-sso`, and `-vpn` domains, Windows-based sign-ins from new devices and IPs, and anonymization services such as Mullvad.

### Signal
- [Signal](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know) says Twilio-console exposure meant about **1,900 Signal users** could have had their phone number registration status revealed or their SMS verification code exposed.
- Signal says the attacker explicitly searched for **three** phone numbers and that one of those users reported an account re-registration.
- Signal forced re-registration for potentially affected users and emphasized that message history, contact lists, and other private data were not exposed through Twilio.

## Operational chain
1. Attackers assembled employee phone targets and sent SMS or voice lures that impersonated IT, password-reset, or schedule-change notices, according to [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack), [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/), and [Okta](https://sec.okta.com/articles/scatterswine/).
2. Those lures pushed targets to freshly registered lookalike domains such as `cloudflare-okta.com`, where fake login pages copied Okta-branded authentication flows.
3. The phishing kit captured usernames, passwords, and OTP/TOTP values and relayed them to the operators through Telegram-backed infrastructure in real time, allowing immediate reuse before codes expired, as described by [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) and [Group-IB](https://www.group-ib.com/blog/0ktapus/).
4. Where organizations still relied on phishable factors, the stolen credentials were used for account takeover and access to internal admin tooling; [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) resisted that step with FIDO2, while [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) says the actor succeeded in reaching internal systems.
5. [Okta](https://sec.okta.com/articles/scatterswine/) says Twilio-console access was then used to search for OTP-related data tied to additional targets, extending the campaign from employee credential theft into downstream account-recovery and session-expansion attempts.
6. [Signal](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know) shows the downstream effect: telecom-provider console access could be turned into attempted account re-registration against services that depended on SMS verification.

## Evidence and impact
- [Group-IB](https://www.group-ib.com/blog/0ktapus/) ties the campaign to a shared phishing kit, a common Okta-themed infrastructure pattern, and recovered compromise data spanning thousands of credentials and MFA codes.
- [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) shows why phishing-resistant MFA mattered: correct credentials were stolen, but hard-key origin binding blocked the attacker from using them.
- [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack) shows the opposite branch of the same chain: once a provider's internal admin tooling was reached, customer-impacting access followed even without theft of API keys or passwords.
- [Okta](https://sec.okta.com/articles/scatterswine/) shows that SMS-based MFA created a secondary exposure path when the actor could inspect provider-side OTP traffic.
- [Signal](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know) shows how that provider-side access affected downstream services that relied on SMS for account registration or recovery.

## Defender takeaways
- Prefer **phishing-resistant MFA** such as FIDO2/WebAuthn for workforce access; [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) shows this was the main control that broke the operation.
- Hunt for newly registered lookalike domains that combine company branding with terms such as `okta`, `sso`, `vpn`, or `helpdesk`, and block or isolate them quickly.
- Treat SMS- and voice-based IT lures as identity-compromise events, not just user-awareness issues; correlate mobile-targeting reports with identity logs and helpdesk activity.
- If an SMS or identity-support provider is compromised, audit for **phone-number searches**, **OTP visibility**, **unexpected device registrations**, and **forced reauthentication** needs across downstream services.
- Okta customers can adapt the [Okta](https://sec.okta.com/articles/scatterswine/) log-hunting guidance for new-device, new-IP, Windows-based sign-ins after SMS events or proxy-backed authentication attempts.

## Sources
- [Group-IB](https://www.group-ib.com/blog/0ktapus/)
- [Cloudflare](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/)
- [Twilio](https://www.twilio.com/en-us/blog/archive/2022/august-2022-social-engineering-attack)
- [Okta Security](https://sec.okta.com/articles/scatterswine/)
- [Signal Support](https://support.signal.org/hc/en-us/articles/4850133017242-Twilio-Incident-What-Signal-Users-Need-to-Know)
