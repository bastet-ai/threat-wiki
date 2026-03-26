# Cloudflare / Okta token theft incident

## Tags
- ops
- operations
- Cloudflare
- Okta
- HAR files
- session hijacking
- token theft
- Zero Trust

## Summary
In October 2023, attackers accessed files in Okta's support case management system, extracted session-bearing data from customer-uploaded HAR files, and used those artifacts to hijack administrator sessions at some affected customers. [Okta's October 20, 2023 advisory](https://sec.okta.com/articles/2023/10/tracking-unauthorized-access-oktas-support-system/), [Okta's November 3, 2023 root-cause update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/), and [Cloudflare's October 20 incident writeup](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) describe the same operational chain: compromise Okta support-side access, harvest sensitive support uploads, then reuse stolen session data to pivot into customer Okta tenants.

This page uses the descriptive title `Cloudflare / Okta token theft incident` because the incident is best understood as a support-system compromise and downstream session-token abuse event, not as a cleanly branded named campaign. Public reporting here does not provide a stable firsthand operator name, so no companion `Groups` or `People` page is published in this pass.

## Naming and companion-page assessment
- [Okta](https://sec.okta.com/articles/2023/10/tracking-unauthorized-access-oktas-support-system/) describes the event as unauthorized access to its support case management system.
- [Cloudflare](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) frames the customer-side incident as an attack that originated from an authentication token stolen from one of Okta's support systems.
- No companion `Groups` or `People` page is published in this pass. The compromise chain is well sourced; the actor identity is not.

## Timeline
- **2023-09-28 to 2023-10-17:** [Okta's November 3, 2023 root-cause update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) says the threat actor had unauthorized access to files inside Okta's customer support system during this period.
- **2023-10-13:** [Okta's November 3 update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) says BeyondTrust provided Okta Security an IOC associated with the event it had reported on October 2.
- **2023-10-17:** Okta says it revoked the Okta session tokens embedded in HAR files that had been downloaded by the threat actor.
- **2023-10-18:** [Cloudflare](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) says its Security Incident Response Team discovered attacks on its systems that traced back to an authentication token stolen from Okta's support systems.
- **2023-10-19:** [Okta's November 3 update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) says Okta identified Cloudflare as the fifth and final Okta customer whose session was hijacked and alerted affected customers.
- **2023-10-20:** [Okta](https://sec.okta.com/articles/2023/10/tracking-unauthorized-access-oktas-support-system/) published its public advisory and [Cloudflare](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) published its containment details.
- **2023-10-26:** [Cloudflare](https://blog.cloudflare.com/introducing-har-sanitizer-secure-har-sharing/) released `HAR Sanitizer` as a direct technical response to the incident pattern.
- **2023-11-03:** [Okta](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) said the attacker accessed files associated with 134 customers and used session tokens to hijack the legitimate Okta sessions of 5 customers.
- **2024-02-01:** [Cloudflare's Thanksgiving 2023 incident writeup](https://blog.cloudflare.com/thanksgiving-2023-security-incident/) said one access token and three service account credentials stolen during the October Okta compromise were not rotated and were later used in a November intrusion into Cloudflare's Atlassian environment.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### Okta
- [Okta's October 20 advisory](https://sec.okta.com/articles/2023/10/tracking-unauthorized-access-oktas-support-system/) says the attacker accessed files uploaded by certain customers in support cases and that HAR files may contain sensitive cookies and session tokens.
- [Okta's November 3 update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) says 134 customers had files accessed and 5 customers had sessions hijacked.
- The same November 3 writeup says the unauthorized access leveraged a service account credential stored in the support system itself.

### Cloudflare
- [Cloudflare's October 20 post](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) says the attacker compromised two separate Cloudflare employee accounts within Okta using session tokens taken from a Cloudflare support ticket.
- Cloudflare says its SIRT detected the activity internally more than 24 hours before Okta notified Cloudflare of the breach, and that no Cloudflare customer information or systems were impacted in the October activity.
- [Cloudflare's February 1, 2024 post](https://blog.cloudflare.com/thanksgiving-2023-security-incident/) says some credentials leaked in the October Okta compromise were not rotated and later enabled a separate November intrusion into Cloudflare's Atlassian environment.

## Operational chain
1. The attacker obtained access to Okta's support case management system using a compromised service account, according to [Okta's November 3, 2023 root-cause update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/).
2. Inside that system, the attacker accessed files uploaded by customers to support cases, including HAR files that could contain cookies and session tokens.
3. The attacker extracted session-bearing data from those HAR files and used it to hijack valid Okta administrator sessions at affected customers, bypassing the need for passwords or fresh MFA prompts.
4. [Okta's November 3 root-cause update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) shows that one affected customer had already alerted Okta earlier in October; [Cloudflare](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) shows the same path succeeding against two Cloudflare employee accounts on October 18.
5. After discovery, customers and vendors had to do more than revoke a single session: revoke embedded session tokens, sanitize support-upload practices, rotate leaked credentials, and verify whether any exposed downstream credentials remained active.

## Evidence and impact
- [Okta's November 3 update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) says the attacker accessed files tied to 134 customers and hijacked the sessions of 5 customers.
- [Cloudflare](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) says no customer data or systems were impacted in the October intrusion because rapid detection and its Zero Trust controls contained the attack.
- [Cloudflare's February 1, 2024 post](https://blog.cloudflare.com/thanksgiving-2023-security-incident/) shows the residual risk of incomplete remediation: one access token and three service-account credentials leaked in October were later used in November.
- [Okta's November 3 update](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/) shows the same attack pattern was detected by at least one affected customer before Okta's public disclosure, reinforcing the value of customer-side identity monitoring.

## Defender takeaways
- Treat support uploads as part of the identity attack surface. HAR files and similar artifacts can carry reusable session material.
- Sanitize cookies, tokens, and credentials out of troubleshooting artifacts before sharing them with vendors; [Cloudflare](https://blog.cloudflare.com/introducing-har-sanitizer-secure-har-sharing/) built `HAR Sanitizer` specifically because of this failure mode.
- When a support-side compromise is disclosed, assume downstream customer sessions and service credentials may need revocation or rotation even if the primary platform was not directly breached.
- Detect impossible or unusual session reuse, not just bad logins. In this incident the attacker often reused valid session material rather than failing authentication.
- Complete remediation matters. Cloudflare's later November incident shows that failing to rotate every exposed credential after an upstream compromise can preserve attacker access opportunities.

## Sources
- [Okta: Tracking Unauthorized Access to Okta's Support System](https://sec.okta.com/articles/2023/10/tracking-unauthorized-access-oktas-support-system/)
- [Okta: Unauthorized Access to Okta's Support Case Management System: Root Cause and Remediation](https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/)
- [Cloudflare: How Cloudflare mitigated yet another Okta compromise](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/)
- [Cloudflare: Introducing HAR Sanitizer: secure HAR sharing](https://blog.cloudflare.com/introducing-har-sanitizer-secure-har-sharing/)
- [Cloudflare: Thanksgiving 2023 security incident](https://blog.cloudflare.com/thanksgiving-2023-security-incident/)
