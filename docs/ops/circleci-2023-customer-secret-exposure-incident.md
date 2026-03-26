# CircleCI 2023 customer secret exposure incident

## Tags
- ops
- operations
- CircleCI
- CI/CD
- secrets
- GitHub OAuth
- Bitbucket
- AWS
- session theft

## Summary
In late 2022 and early January 2023, attackers used malware on a CircleCI engineer's laptop to steal a valid 2FA-backed SSO session, impersonate the employee, and gain access to a subset of CircleCI production systems. [CircleCI's January 4, 2023 security alert](https://circleci.com/blog/january-4-2023-security-alert/) and [January 12, 2023 incident report](https://circleci.com/blog/jan-4-2023-incident-report/) show why the incident belongs under `Ops`: the key value is the compromise chain from employee device malware to production token access to customer secret exposure across third-party systems.

This page uses the descriptive title `CircleCI 2023 customer secret exposure incident` because CircleCI itself framed the incident around customer secret exposure and mandatory rotation, not around a named threat group. Public reporting in the sources here does not provide a durable firsthand operator name or a clearly attributable public human identity, so no companion `Groups` or `People` page is added in this pass.

## Naming and companion-page assessment
- [CircleCI's January 4, 2023 alert](https://circleci.com/blog/january-4-2023-security-alert/) describes the event as a security incident requiring customers to rotate any secrets stored in CircleCI.
- [CircleCI's January 12, 2023 incident report](https://circleci.com/blog/jan-4-2023-incident-report/) describes an unauthorized third party that stole an employee's 2FA-backed SSO session and then exfiltrated customer environment variables, tokens, and keys.
- No companion `Groups` or `People` page is published in this pass. The operation is strongly sourced; the actor identity is not.

## Timeline
- **2022-12-16:** [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says the targeted employee laptop was compromised by malware on December 16, 2022.
- **2022-12-19:** The same report says the unauthorized third party conducted reconnaissance activity in CircleCI production systems on December 19, 2022.
- **2022-12-22:** CircleCI says data exfiltration from a subset of databases and stores occurred on December 22, 2022, and that this was the last recorded unauthorized production activity.
- **2022-12-29:** [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says a customer notified CircleCI about suspicious GitHub OAuth activity, triggering a deeper internal review with GitHub.
- **2022-12-31:** CircleCI says it proactively initiated rotation of all GitHub OAuth tokens on behalf of customers on December 31, 2022.
- **2023-01-04 16:35 UTC:** [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says it shut down access for the compromised employee account.
- **2023-01-04 18:30 UTC:** CircleCI shut down production access for nearly all employees, limiting access to a very small group for operational issues.
- **2023-01-04 22:30 UTC / 2023-01-05 02:30 UTC:** CircleCI rotated potentially exposed production hosts, then publicly disclosed the incident and told customers to rotate secrets immediately.
- **2023-01-05 03:26 UTC:** CircleCI revoked all Project API Tokens.
- **2023-01-06 05:00 UTC:** CircleCI revoked all Personal API Tokens created before January 5, 2023.
- **2023-01-06 06:40 UTC to 10:15 UTC:** CircleCI says it worked with Atlassian to rotate Bitbucket tokens on behalf of customers.
- **2023-01-07 07:30 UTC:** CircleCI completed rotation of GitHub OAuth tokens.
- **2023-01-07 18:30 UTC to 2023-01-12 00:00 UTC:** CircleCI says it worked with AWS to notify customers of potentially affected AWS tokens, and those notifications were complete by January 12, 2023.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### CircleCI
- [CircleCI's January 4 alert](https://circleci.com/blog/january-4-2023-security-alert/) told all customers to immediately rotate any secrets stored in project environment variables or contexts.
- The same alert recommended reviewing internal logs for unauthorized access starting from December 21, 2022 through January 4, 2023, or until secret rotation was complete.
- [CircleCI's January 12 incident report](https://circleci.com/blog/jan-4-2023-incident-report/) later clarified the deeper timeline and said the impacted employee had privileges to generate production access tokens as part of regular duties.

### GitHub, Atlassian, and AWS
- [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says GitHub helped investigate the suspicious OAuth activity first reported by a customer.
- The same report says CircleCI worked with Atlassian to rotate Bitbucket tokens on behalf of customers and with AWS to notify customers of potentially affected AWS tokens.
- The vendor-side recovery therefore had both an internal production-system component and a partner-coordination component across downstream secret ecosystems.

### Customer environments
- [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says the exfiltrated data included customer environment variables, tokens, and keys for third-party systems.
- CircleCI explicitly said it could not know whether those exposed secrets had been used against customer-owned third-party systems, which is why the operational scope extends beyond CircleCI itself.

## Operational chain
1. Malware on a CircleCI engineer's laptop stole a valid 2FA-backed SSO session, according to [CircleCI's incident report](https://circleci.com/blog/jan-4-2023-incident-report/).
2. The attacker used that session to impersonate the employee remotely and escalate access into a subset of CircleCI production systems.
3. Because the employee could generate production access tokens as part of regular duties, the attacker gained access to a subset of databases and stores containing customer environment variables, tokens, and keys.
4. The attacker exfiltrated data on December 22, 2022, including secrets for third-party systems. CircleCI says the data was encrypted at rest, but the attacker extracted encryption keys from a running process, potentially allowing access to the encrypted contents.
5. CircleCI then executed a large downstream containment effort: shutting down employee production access, rotating hosts, revoking internal and customer-facing tokens, and coordinating token rotation or notifications with GitHub, Atlassian, and AWS.

## Evidence and impact
- [CircleCI's January 12 incident report](https://circleci.com/blog/jan-4-2023-incident-report/) says the attacker accessed and exfiltrated customer environment variables, tokens, and keys from a subset of databases and stores.
- The same report says CircleCI had fewer than five customers inform it of unauthorized access to third-party systems at the time of publication, but also notes CircleCI could not directly determine all downstream misuse.
- [CircleCI's January 4 alert](https://circleci.com/blog/january-4-2023-security-alert/) treated every stored secret as potentially exposed, which is why the customer guidance was blanket rotation rather than a narrower revoke list.
- The operation matters because it was not a direct customer workload compromise through CircleCI pipelines alone; it was a CI/CD trust-boundary incident that exposed secrets for many outside systems.

## Defender takeaways
- Treat employee endpoint compromise in CI/CD vendors as a potential production-secret event, especially where engineers can mint or access privileged tokens.
- Prefer short-lived or federated credentials such as OIDC over long-lived stored secrets where possible; [CircleCI's January 4 alert](https://circleci.com/blog/january-4-2023-security-alert/) later recommended exactly that.
- When a CI platform tells you to rotate every stored secret, respond as if downstream environments may already be exposed; the blast radius is broader than the vendor's own infrastructure.
- Review customer-owned logs, not just vendor audit logs. CircleCI explicitly told customers to investigate their own downstream systems for suspicious use of stored secrets.
- Strong user auth is not enough by itself if a valid session can be stolen from an already-compromised endpoint. Session theft defeated the targeted employee's 2FA-backed login.

## Sources
- [CircleCI security alert: Rotate any secrets stored in CircleCI](https://circleci.com/blog/january-4-2023-security-alert/)
- [CircleCI incident report for January 4, 2023 security incident](https://circleci.com/blog/jan-4-2023-incident-report/)
