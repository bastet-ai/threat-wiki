# AWS root user password-spraying campaign across 150+ organizations — two fixed user agents, residential-proxy tunneling, no confirmed success (Datadog Security Labs, Aug 31, 2026)

## Tags
- ops
- operations
- AWS
- cloud
- identity
- root user
- root account
- password spraying
- credential attack
- brute force
- MFA
- CloudTrail
- detection
- threat research
- Datadog
- residential proxy
- console login
- ConsoleLogin
- AssumeRoot
- service control policies

## Summary

On **August 31, 2026**, Datadog Security Research (Martin McCloskey) reported a **password-spraying campaign against the AWS account root user** that ran from **July 24 to August 23, 2026**. Attackers made **repeated failed authentication attempts against the AWS root user account at more than 150 organizations**, with a **median of two attempts per organization** and up to **eight** in the campaign window. The campaign is fingerprinted by **two specific user agents** (an **Edg/Chrome 85** and a **Firefox 120** signature) and by **proxy-tunneled source traffic** — the source IPs span a wide range of countries and ASNs, and threat-intelligence sources flag all of them as **hosting infrastructure, residential proxies, or similar**. Targeted organizations show **no clear victimology** (they vary widely by country and industry), and **no successful authentication was observed**, so the attacker's intent could not be determined.

The notable tradecraft point: a **failed `ConsoleLogin` API call requires the email address associated with the root user account**. That means the attacker either **already held a list of root-user email addresses**, or **brute-forced a list of account emails until finding valid ones** — i.e., the spray presupposes valid root-account email enumeration, which is itself a meaningful indicator of pre-staged targeting data. Datadog published the report to share the activity with the community and invite defenders who observed similar traffic to collaborate at `securitylabs@datadoghq.com`.

## Attribution and context
- **No actor named.** Datadog does not attribute the campaign to a group or individual; victimology is "apparently random" (varies by country and industry) and no successful login was observed, so motive is not determinable. This is reported as observed malicious activity, not as confirmed intrusion.
- **Distinction from prior root-related reporting.** This is a **cross-organization root-user *console-login* spray**, not a specific CVE/exploit. It is a credential-attack signal, not a product flaw. It does **not** overlap with the AWS root-user *hardening* guidance in AWS IAM, which remains the underlying control to enforce.
- **Why the root user is a notable target:** the AWS root user has complete access to the account (resources, billing, settings) and some actions no other identity can perform. It is an unusual target because (a) AWS recommends monitoring all root user activity, so root actions draw scrutiny, and (b) since **June 2025 AWS IAM enforces MFA for root users across all account types** (a 35-day grace period separates the first console sign-in attempt from MFA registration). Targeting the root user takes more effort than easier paths such as stolen access keys — which is what makes a coordinated, multi-org spray notable.

## Technical detail
- **Target:** the **AWS account root user** (`arn:aws:iam::<account-id>:root`), via the **console sign-in** path (`ConsoleLogin` API, `eventSource: signin.amazonaws.com`).
- **Mechanism:** repeated **failed** `ConsoleLogin` attempts (password spraying — many accounts, few low-and-slow attempts per account, to stay under lockout thresholds). Median 2 attempts/organization, up to 8.
- **Enumerated data requirement:** generating a failed `ConsoleLogin` **requires the root user's email address** (the sign-in page requires the account email to select the root user). This implies the operator already had root-account emails for 150+ organizations — either a **pre-compiled list** or **brute-forced valid emails**.
- **Network fingerprints (two IOCs, both user-agent):**
  1. `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41` (an **Edge/Chrome 85** signature)
  2. `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0` (a **Firefox 120** signature)
- **Source traffic:** requests are **tunneled through proxies**; source IPs span a wide range of countries and ASNs, all flagged by threat-intel sources as hosting infrastructure, residential proxies, or similar. (Datadog did not publish a fixed IP block — the residential-proxy rotation is the tell, not static IPs.)
- **Campaign window:** **July 24 – August 23, 2026** (per-day targeting graph published by Datadog; activity distributed across the window rather than a single burst).
- **Outcome:** **no successful authentication observed**; intent undetermined.

## Detection / defensive heuristics
- **CloudTrail hunt query (published by Datadog)** — check whether this campaign hit you:
  ```
  source:cloudtrail
  @userIdentity.type:Root
  @eventName:ConsoleLogin
  @responseElements.ConsoleLogin:(Failure OR Success)
  @userAgent:("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
             OR "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")
  ```
- **Event shape:** `eventSource: signin.amazonaws.com`, `eventName: ConsoleLogin`, `userIdentity.type: Root` with an empty `accessKeyId`, a `responseElements.ConsoleLogin` of `Failure` (or `Success`), and a `userAgent` matching either signature. A failed sample from the report:
  ```json
  {
    "userIdentity": { "type": "Root", "principalId": "123456789012",
                      "arn": "arn:aws:iam::123456789012:root",
                      "accountId": "123456789012", "accessKeyId": "" },
    "eventTime": "2026-08-16T04:33:40Z",
    "eventSource": "signin.amazonaws.com",
    "eventName": "ConsoleLogin"
  }
  ```
- **Lower the specificity for broader coverage:** even without the exact user-agent string, any **`ConsoleLogin` against `userIdentity.type:Root`** (Failure or Success) is security-relevant and worth alerting on — AWS recommends monitoring *all* root user activity.
- **Reduce reliance on the root user (Datadog's mitigations):**
  - Use **AWS Organizations service control policies** to **prevent direct root activity in member accounts**.
  - Use **centralized root access** (short-lived, centrally authorized **`AssumeRoot`** sessions) to remove long-lived root credentials. Note: **neither control protects the organization's management account** — its root credentials need separate safeguards.
  - **Alert on all root activity** in CloudTrail: direct root sign-ins, root API activity, credential changes, and centrally-initiated privileged sessions.

## Why this matters
- **The root user is the crown jewel, and it is now being sprayed at scale.** A coordinated cross-organization root-user spray is a strong leading indicator that an attacker is building or testing root-access paths ahead of a more targeted or opportunistic follow-on attempt.
- **The email-enumeration requirement is the tell.** Because a failed `ConsoleLogin` needs the root email, this campaign presupposes valid root-account email data for 150+ orgs — meaning either a harvested/leaked email list or active enumeration. That data is a reusable asset, so the campaign is more plausibly *reconnaissance / credential-validation* than a one-off.
- **MFA alone is not sufficient.** Root MFA (enforced since June 2025) raises the bar but does not remove the value of the root account; the durable control is **removing the need for a persistent root identity** (SCPs + centralized `AssumeRoot`) plus **treating all root activity as a security event**.
- **Actionable, specific detection.** Datadog publishes the exact CloudTrail query and the two user-agent IOCs, so this is immediately triageable.

## Assessment limits
- **No confirmed success, no actor, no motive.** This is observed failed-authentication activity, not a confirmed intrusion. Datadog explicitly could not determine intent from the limited information and random-seeming victimology.
- **Residential-proxy source IPs are not a stable blocklist.** The report's network signature is proxy *type*, not fixed IPs; treat the two user agents + proxy-tunneled root `ConsoleLogin` as the durable indicators.
- **Management account is out of scope of the SCP/AssumeRoot mitigations.** Those controls protect member accounts; the management account's root still needs separate safeguards.

## Related pages
- [GitHub API enumeration / token abuse pattern](../patterns/github-api-enumeration-token-abuse.md)
- [HackerBot / Claw GitHub Actions exploitation campaign](hackerbot-claw-github-actions-exploitation-campaign.md)

## Sources
- Datadog Security Labs, August 31, 2026: [Password spraying campaign targets AWS root user accounts across 150+ organizations](https://securitylabs.datadoghq.com/articles/aws-root-user-bruteforce-campaign)
