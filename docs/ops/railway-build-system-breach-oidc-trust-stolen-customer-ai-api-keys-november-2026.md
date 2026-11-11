# Railway build-system breach: escape, misplaced trust, and stolen AI keys

**Captured November 11, 2026 (243rd sweep) by this wiki from Railway's detailed incident report (published Nov 10, 2026; attack window Oct 20-21), the StepSecurity analysis (Nov 10), and press corroboration (BleepingComputer, The Hacker News). All figures are the company's own. No attacker artifact was touched.**

## Summary

Railway's full forensics of the October 20-21 breach turns a headline ("secrets leaked, ~$740k of fraud") into a **credential-chaining anatomy that never touches a crypto break**: a zero-day partial filesystem-isolation escape in the multi-tenant build fleet yielded a build-push credential; an internal Temporal cluster wrongly **accepted that build credential as a trusted client**, opening 353 stored build histories (with their secrets) and a copy of Railway's internal monorepo; the attacker scanned that source for the next door and found an **erroneously defined OIDC binding** in one cloud environment; the OIDC-issued short-lived cloud credential pulled two more internal credentials, one of them an SSH key onto a fleet-orchestration machine that held, on disk, the longer-lived credential able to authorize variable decryption. Database queries then **searched by name for AI provider keys** specifically, and the decrypted haul powered an estimated **$740,000 in fraudulent AI usage**, which Railway has said it will pay. The company's own framing is the most durable line: the attack ran **abliterated AI models in a harness similar to ARTEX** (per Wiz) against engineers hardening routes in parallel — "a contest of agent speed." Upper bound of exposure is `1.85%` of workspaces (~100,000) because Railway's logs identify affected ENVIRONMENTS, not individual variables; logs cannot say which secrets were read.

## The chain, as Railway documents it (UTC)

| Time | Event |
|---|---|
| Oct-20 `06:50` | Attacker begins probing build infrastructure (multi-tenant: many builds per VM, isolated) |
| Oct-20 `07:28` | **Unknown vulnerability**: partial filesystem-isolation escape, reads host-VM files, obtains the build-servers' internal credential (legit use: push images post-build) |
| Oct-20 ~13:58 | On-call paged by anomalous registry-API calls; trace leads back through the credential to the escaped build (`≈6.5 h` dwell to first alert) |
| Oct-20 `17:28` | Build credential revoked/replaced; reachable services restricted |
| (post-fix) | Attacker retries an escalation, fails; Railway's OWN hardening team reproduces a second exploit off the patched one within an hour = fix-then-retest as a race discipline |
| Oct-21 `03:26` | **Misconfigured OIDC binding** in one cloud environment yields a short-lived production cloud credential |
| Oct-21 `04:07-05:21` | Encrypted variables pulled from the production DB, queries name-matched to **AI provider keys**; two decryption windows (`04:42-05:14`, `06:36-07:15`) via the orchestration machine's credential + KMS |
| Oct-21 `07:14/07:22` | All cloud + static credentials disabled, key-decryption service shut, builds halted platform-wide |
| Oct-21 `09:24` | Attacker fully evicted |
| Oct-21 `20:19` | Every user session and token invalidated |
| Oct-22 `22:49` | Builds restored on hardened infra (dedicated ephemeral VM per build, credential scoped to ONE image push) |

What the Temporal step means: the build credential worked where it had **no business working** — an internal task system trusted a client by credential shape, not by role. That misplaced trust, not the escape, is what converted "read some host files" into "read 353 builds' secrets and the internal monorepo." The monorepo copy is what made the OIDC finding possible: the attacker had the map.

## Scale, as the company states it

- `≤1.85%` of workspaces (~`100,000`) COULD have had variables decrypted — logs identify environments, not variables, so this is an **upper bound**, and Railway emailed the high-risk subset.
- `353` build histories read, including variables/secrets passed to those builds.
- `1,852` users' linked-account tokens exposed (BYOK agent keys, GitHub OAuth tokens); all reset, all notified; no logins found using them.
- `~$740,000` estimated fraudulent AI spend on stolen customer AI-provider keys; Railway commits to paying non-refundable charges.
- Data copied but not decrypted is now permanently undecryptable — the decryption credential was disabled mid-incident.
- Preliminary report (Oct-22) and final report (Nov-10) DISAGREE on the attack clock (preliminary started at the `13:58` page; final starts at the `07:28` exploit) = a preliminary incident report is a snapshot under fog, diff it against the final before citing timelines.

## Durable hunt shapes

1. **Audit credential RECIPIENTS, not just issuers.** Enumerate every internal service that accepts a build/CI credential as a client; a credential that "reaches" a task system it was never issued for is the lateral hop in this story.
2. **OIDC binding review is a named control.** One wrong trust definition in one cloud environment was the pivot to production. Diff every OIDC federator's `aud`/`sub`/subject-mapping against the workload that actually needs it (the wiki's OIDC subject-claim pattern page is the sibling class).
3. **On-disk long-lived credentials next to KMS access are a decryption pair.** The orchestration machine held BOTH the network position and the authorize-decryption credential. Neither alone was enough; the machine made them one capability. Hunt hosts that combine them.
4. **Name-pattern DB queries are a forensic tell.** The attacker queried the variables DB matching AI-provider key names; a DB audit log showing `SELECT`s filtered on secret-name patterns is this campaign's fingerprint.
5. **Logs that identify environments but not variables cannot bound a leak.** Encrypt-and-log-every-decrypt (Railway's post-incident control) is the answer; adopt it BEFORE the incident.
6. **Agent-speed defense needs agent-speed offense in rehearsal.** Railway's hardening team re-exploiting its own patch within an hour, and the attacker running an ARTEX-similar harness (per Wiz), make red-team cadence a tempo question, not a quarterly one. Railway's own fix-then-retest step is the template.

## Related on this wiki

- [Qubole cross-account role abuse](qubole-aws-cross-account-integration-role-abuse-trufflehog-validation-self-destruct-iso-november-2026.md) (same reporting week, same class: your trusted third party's credential is your blast radius)
- [Ethersphere bee-js / Swarm Desktop release-pipeline compromise](ethersphere-bee-js-npm-swarm-desktop-release-pipeline-compromise-sleepyduck-ethereum-contract-c2-november-2026.md) (trusted release infrastructure as attack surface)
- [Gheist compromised GitHub tokens workflow secret dump](gheist-compromised-github-tokens-workflow-secret-dump-base32-ci-sync-branches-wiz-october-2026.md) (the CI-credential economy both stories spend in)
- [ARTEX section on the ConnectWise page](connectwise-saas-application-identities-compromise-m365-tenant-access-october-2026.md#october-24-wiz-artex-in-the-wild) (the harness family the attacker is said to have resembled)

## Sources

- Railway, "Incident Report: October 21st Security Attack" (Nov 10, 2026): [https://blog.railway.com/p/incident-report-october-security-incident](https://blog.railway.com/p/incident-report-october-security-incident)
- StepSecurity, "Railway's Security Incident: Why CI/CD Needs Runtime Security" (Nov 10, 2026): [https://www.stepsecurity.io/blog/railway-security-incident-cicd-runtime-security](https://www.stepsecurity.io/blog/railway-security-incident-cicd-runtime-security)
- BleepingComputer, "Railway breach leads to $740,000 in fraudulent AI charges" (Nov 11, 2026): [https://www.bleepingcomputer.com/news/security/railway-warns-devs-to-rotate-secrets-after-potential-breach/](https://www.bleepingcomputer.com/news/security/railway-warns-devs-to-rotate-secrets-after-potential-breach/)
- The Hacker News, "Railway Says Stolen Customer AI Keys Led to $740,000 in Estimated Unauthorized Usage Charges" (Nov 11, 2026): [https://thehackernews.com/2026/11/railway-says-stolen-customer-ai-keys.html](https://thehackernews.com/2026/11/railway-says-stolen-customer-ai-keys.html)
