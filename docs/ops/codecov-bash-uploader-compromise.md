# Codecov Bash Uploader compromise

## Tags
- ops
- operations
- Codecov
- CI/CD
- Bash Uploader
- secrets
- GCS
- supply-chain

## Summary
From January 31 to April 1, 2021, a malicious actor modified Codecov's `Bash Uploader` script so it could exfiltrate data from customer CI environments to attacker-controlled infrastructure. [Codecov's security update](https://about.codecov.io/security-update/) and [CISA's April 30, 2021 alert](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) describe a software-delivery compromise in which an error in Codecov's Docker image creation process exposed the credential needed to alter the uploader script.

This page uses the descriptive title `Codecov Bash Uploader compromise` because the official incident framing is the compromised uploader and its downstream secret exposure. Public reporting in the sources here does not provide a durable firsthand operator name, so this is an `Ops` page rather than a `Groups` or `People` profile.

## Naming and companion-page assessment
- [Codecov](https://about.codecov.io/security-update/) calls the event a `Bash Uploader Security Update` and centers the compromise on the Bash Uploader script and related uploaders.
- [CISA](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) describes it as a Codecov software supply-chain compromise.
- No companion `Groups` or `People` page is published in this pass. The compromise chain is well documented; the actor identity is not.

## Timeline
- **2021-01-31:** [Codecov](https://about.codecov.io/security-update/) and [CISA](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) say unauthorized alterations of the Bash Uploader began on January 31, 2021.
- **2021-04-01:** Codecov says a customer discovered a checksum discrepancy in the downloaded uploader, reported it that morning, and Codecov immediately remediated the affected script.
- **2021-04-15:** [Codecov](https://about.codecov.io/security-update/) says it notified affected users by email and in-product banner on April 15, 2021.
- **2021-04-29:** Codecov says it published additional information on what environment variables may have been obtained without authorization and how they may have been used.
- **2021-04-30:** [CISA](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) published its public alert urging users to review Codecov's update, re-roll potentially affected credentials, and reissue potentially affected certificates.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### Codecov
- [Codecov](https://about.codecov.io/security-update/) says the attacker gained access because an error in its Docker image creation process exposed the credential required to modify the Bash Uploader script.
- The same update says the Bash Uploader was also used by the `codecov-action` uploader for GitHub, the Codecov CircleCI Orb, and the Codecov Bitrise Step, so those related uploaders were also affected.
- Codecov also says self-hosted Codecov customers were very unlikely to be affected unless their CI pipelines fetched the Bash Uploader from Codecov's public infrastructure instead of from their self-hosted installation.

### Customer CI environments
- [Codecov](https://about.codecov.io/security-update/) says the modified uploader could expose any credentials, tokens, or keys available to the CI runner when the Bash Uploader executed.
- The same update says those stolen values could in turn expose services, datastores, and application code reachable with the compromised credentials.
- Codecov advised customers to inspect CI environment variables, re-roll sensitive credentials, and audit token use in downstream systems.

### CISA and downstream defenders
- [CISA](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) reinforced Codecov's guidance and specifically recommended re-rolling potentially affected credentials, tokens, and keys as well as revoking and reissuing potentially affected certificates.
- CISA's framing is important because it treats the event as a supply-chain compromise with downstream credential risk, not just a vendor-side script integrity problem.

## Operational chain
1. A credential exposed through Codecov's Docker image creation process gave the attacker access to alter the publicly fetched Bash Uploader script, according to [Codecov](https://about.codecov.io/security-update/).
2. Beginning on January 31, 2021, the attacker periodically modified the uploader so it could export data from customer CI environments to a third-party server.
3. When CI jobs executed the altered uploader, any environment variables, credentials, tokens, or keys available to that runner could potentially be exposed.
4. The same trust boundary extended to related uploaders that depended on the Bash Uploader, including GitHub Actions, CircleCI Orb, and Bitrise integrations.
5. Once a customer detected a checksum mismatch on April 1, 2021, Codecov remediated the script, rotated the credential used in the event, and began the broader customer notification and secret-rotation process.

## Evidence and impact
- [Codecov](https://about.codecov.io/security-update/) says there were 108 windows of time between January 31 and April 1 during which the Bash Uploader was affected.
- The same update says the attacker could potentially access any credentials, tokens, or keys exposed to the uploader during CI execution, which is why the downstream blast radius extended far beyond Codecov itself.
- [CISA](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise) treated the event seriously enough to publish a public supply-chain alert with re-rolling and certificate reissuance guidance.
- The operational importance of this incident is that a small modification to a ubiquitous helper script could quietly turn many unrelated CI pipelines into credential-exposure events.

## Defender takeaways
- Treat CI helper scripts and installer-style pipeline fetches as supply-chain surfaces. If the script comes from the internet at runtime, it can become an exfiltration path.
- Verify integrity before execution. In this case, the incident was discovered because a customer compared the expected checksum with the downloaded uploader.
- Prefer minimizing long-lived secrets in CI runners. Anything present in the environment when the altered uploader ran was potentially exposed.
- When a CI utility is compromised, rotate broadly. Credentials, tokens, keys, and even certificates may need replacement because the downstream access paths are hard to bound precisely.
- Separate the vendor compromise from its downstream impact. The durable lesson is not just that Codecov had a bad key path; it is that one compromised CI helper can fan out into many unrelated environments.

## Sources
- [Codecov: Bash Uploader Security Update](https://about.codecov.io/security-update/)
- [CISA: Codecov Releases New Detections for Supply Chain Compromise](https://www.cisa.gov/news-events/alerts/2021/04/30/codecov-releases-new-detections-supply-chain-compromise)
