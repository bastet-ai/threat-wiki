# CISA AA26-237A "A Tale of Two SOCs": red team fully compromises two critical-infrastructure orgs; one detects nothing

## Summary
On **August 25, 2026**, CISA published advisory **AA26-237A** ("A Tale of Two SOCs"), disclosing the results of **two simultaneous red team assessments** against two critical-infrastructure organizations using similar tradecraft, with sharply different defensive outcomes. Both organizations were **fully compromised at the domain level**, and in both the red team also reached **sensitive business systems (SBSs)** and **cloud resources**:

- **Organization A** — a **Government Services and Facilities Sector** organization. The red team gained initial access via a web application with **default credentials** on several built-in accounts, phished from an internal address to land on four workstations, escalated via the **default Machine Account Quota** plus a **misconfigured AD CS certificate template** (the same abuse class as the recently disclosed domain-takeover exploit **Certighost**), then accessed three SBSs using **cleartext-stored credentials** (including decrypted database configuration files and **static AWS access keys set never to expire**). In the cloud it stole a **Primary Refresh Token** and abused **Entra ID applications with elevated permissions** to read the security team's email and check whether defenders were aware of the activity. **Organization A did not detect any of it.**
- **Organization B** — a **Water and Wastewater Systems Sector** organization. Its SOC detected the initial phishing payloads **as they executed** and isolated the affected workstations within **2 to 20 minutes**, cutting off C2 before the intrusion could spread. CISA's trusted agents then executed a red team payload on a designated non-privileged host in an **assume-breach** model. The team still found the same underlying problems — cleartext credentials for a **domain service account in an SCCM configuration file** that carried rights over a domain controller, which it used to run a **DCSync attack** and retrieve the **krbtgt secret** — and reached a **bastion host in the OT demilitarized zone**, which blocked outbound internet access, so no C2 channel was established and the team did not enter the OT systems themselves.

CISA attributes the gap between the two outcomes to **the people and processes operating the tools, rather than the tools themselves**: "Detection tools are only as effective as the people, processes, and procedures supporting them."

## Tags
- ops
- CISA
- AA26-237A
- red team
- APT simulation
- critical infrastructure
- SOC
- security operations
- detection failure
- alert fatigue
- false positives
- Machine Account Quota
- AD CS
- certificate template
- ESC1
- Escalate with Certify
- Certighost
- DCSync
- krbtgt
- SCCM
- Primary Refresh Token
- Entra ID
- cleartext credentials
- static AWS keys
- token revocation
- assume-breach
- OT
- water and wastewater
- government services and facilities
- people and process
- incident response

## What the advisory establishes
1. **Similar tradecraft, divergent outcomes.** Both engagements used the same general approach; the difference is detection and response. Organization A's failure was not a tooling gap on paper — it "ran multiple security operations centers (SOCs) and endpoint tools" — but **no shared visibility between them**, **no escalation procedures**, and **limited analyst authority to act**.
2. **The enablers (Organization A), per CISA:**
   - **Machine Account Quota at the default**, letting any domain user add machine accounts;
   - **Misconfigured AD CS certificate templates** allowing certificate requests for any user (**ESC1** — the same class as Certighost);
   - **Cleartext credentials** for service and database accounts stored on reachable systems;
   - **Static cloud access keys set never to expire**, with no token revocation in place;
   - **Over-permissioned Entra ID applications** able to read mail across all users.
3. **Organization A's detection failure is a concrete case study in alert fatigue:** thousands of false-positive alerts from normal business operations, many rated at **higher severity** than the red team's alerts, obscured the real ones. A genuine alert tied to red team activity on an SCCM server was **dismissed as a false positive** after defenders could not identify the system's owner.
4. **Organization B proves the same attack is stoppable with functioning detection:** payload execution was observed in real time, hosts were isolated in 2–20 minutes, and C2 was severed before spread. The assume-breach phase then mapped the *latent* blast radius (krbtgt via DCSync, OT DMZ bastion reach) that would have materialized without that early detection.
5. **The OT boundary held at the network layer, not the identity layer:** the OT DMZ bastion blocked outbound internet, which is why no C2 channel was established — the team had already obtained the krbtgt secret and could, in a real attack, have moved laterally inside the OT network without any outbound channel.

## Defender priorities
1. **Machine Account Quota:** lower the default `ms-DS-MachineAccountQuota` (default 10) to a controlled value on every domain; alert on new computer-account creations.
2. **AD CS:** run `EscalateWithCertify` (and successor tooling) against certificate templates; hunt ESC1/ESC8/ESC10 exposures and patch template misconfigurations — the advisory explicitly ties the escalation to the Certighost class.
3. **Kerberos hygiene:** monitor `4662` privilege use and `4769` TGT requests with the `DCSync` (0x10000) option; the Organization B result shows DCSync is achievable from a single SCCM-config-file credential.
4. **Credentials in configuration:** sweep SCCM/SCCM-adjacent configuration files, database config dumps, and service accounts for cleartext secrets; rotate and add revocation.
5. **Static cloud keys:** enforce rotating/short-lived credentials, disable static keys set to "never expire," and add token-revocation runbooks; a stolen PRT plus an over-permissioned Entra app was enough to read the security team's own mail.
6. **Alert hygiene is the root cause:** the Organization A pattern (high-severity false positives drowning real alerts, multi-SOC silos, no escalation path, analysts without authority) is the durable lesson. Re-tune severities, build cross-SOC visibility, and define who can isolate a host.
7. **OT DMZ:** outbound-block on OT DMZ bastions is a valid control, but pair it with identity monitoring — the krbtgt was already taken by the time the bastion was reached.

## Caveats
- CISA identifies the organizations only by sector (Government Services and Facilities; Water and Wastewater Systems) — no names, no dates of engagement beyond the August 25, 2026 publication.
- The advisory is CISA's own assessment; no independent third-party validation of the two engagements is available.
- "Default Machine Account Quota" and "misconfigured AD CS template" are described as the *class* of finding; the advisory does not publish the specific template names or quota values.

## Timeline
- **August 25, 2026** — CISA publishes AA26-237A "A Tale of Two SOCs."
- **August 26, 2026** — The Hacker News reports on the advisory.

## Related pages
- [CISA KEV: Microsoft Entra / Zimbra August 21 batch](cisa-kev-microsoft-entra-zimbra-august-21-2026.md)
- [CISA water-sector PLC activity alert (July 30, 2026)](../notes/source-index.md)
- [AA26-231A: AI-generated exploit scripts target Siemens S7 PLCs](aa26-231a-siemens-s7-ai-generated-exploit-scripts-us-critical-infrastructure.md)

## Sources
- CISA: [AA26-237A "A Tale of Two SOCs" — advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-237a) (published August 25, 2026; page returned 403 to automated clients, content sourced via the August 26 The Hacker News report)
- The Hacker News: [CISA Red Team Compromised Two Critical Infrastructure Orgs, One Detected Nothing](https://thehackernews.com/2026/08/cisa-red-team-compromised-two-critical.html) (August 26, 2026)
