# TeamPCP: AFP/WAPF/FBI charge two Western Australian men over the Trivy, KICS, and LiteLLM supply-chain attacks

## Summary
On **August 27, 2026**, the Australian Federal Police (AFP) and the Western Australia Police Force (WAPF) **charged two Western Australian men** with a combined **14 offences** over their alleged role as principal participants in **TeamPCP**, the cybercrime syndicate behind the **March 2026** compromise of the open-source security scanners **Trivy** and **Checkmarx KICS** and the AI-gateway project **LiteLLM**. **Louis Michael Gaebler, 23**, and **Ruben Ian Thomson, 21**, appeared at **Perth Magistrates Court** on August 27, the day after the AFP and WAPF executed search warrants at properties in **Cottesloe, Hamilton Hill, and Mandurah** and seized electronic devices for forensic analysis. The **FBI** participated in the investigation and issued a joint media release; FBI Cyber Division Assistant Director **Brett E. Leatherman** said the two men are allegedly members of TeamPCP, whose malicious code "potentially compromised more than a thousand organizations worldwide."

This is the first named-person charging in the TeamPCP matter. It is an **allegation, not a conviction**: no charge names a specific compromised project, and the men are presumed innocent until the matter is determined by the court. The durable value for defenders is the **exposure-window hygiene guidance** the FBI reaffirmed: treat exfiltrated credentials and CI/CD secrets as a persistent risk and rotate them across the full March exposure window, regardless of the charging outcome.

## Tags
- ops
- operations
- supply-chain
- TeamPCP
- law enforcement
- arrest
- charging
- Australia
- AFP
- WAPF
- FBI
- Trivy
- Checkmarx KICS
- LiteLLM
- GitHub Actions
- Docker Hub
- npm
- PyPI
- OpenVSX
- credential theft
- CI/CD
- publishing credentials
- cross-ecosystem
- exposure window

## The charging
- **Agencies:** AFP (lead), WAPF, and FBI (joint media release). FBI Cyber Division Assistant Director **Brett E. Leatherman** spoke at the announcement.
- **Named individuals (alleged):** Louis Michael Gaebler, 23 (Mandurah); Ruben Ian Thomson, 21 (Cottesloe). Police allege both were **principal participants** in the syndicate and **received payments in cryptocurrency**, the value of which is under investigation.
- **Warrants / seizure:** Search warrants executed at properties in **Cottesloe, Hamilton Hill, and Mandurah** on August 26, 2026; electronic devices seized for forensic analysis.
- **Court appearance:** Perth Magistrates Court, **August 27, 2026**.
- **Total offences:** 14 across the two men.
  - **Cottesloe man, 21 (Thomson):** one count of possessing data with intent to commit a computer offence; four counts of unauthorized modification of data with intent to commit a serious offence; one count of supplying data with intent to commit a computer offence; one count of failing to comply with a **section 3LA order** (Crimes Act 1914 (Cth)); and one count of **dealing with proceeds of crime worth $100,000 or more**.
  - **Mandurah man, 23 (Gaebler):** one count of possessing data with intent; four counts of unauthorized modification of data with intent to commit a serious offence; and one count of supplying data with intent to commit a computer offence.
- **Maximum penalties:** the section 3LA count carries up to **10 years' imprisonment**; the proceeds-of-crime count carries up to **20 years**.
- **Scope caveat:** none of the 14 charges names a specific compromised project. The charging alleges roles in the syndicate, not each individual compromise.

## Campaign mechanics (as described by the AFP)
The syndicate "worked by stealing publishing credentials from trusted open-source projects and pushing poisoned versions out through the projects' own release channels." The campaign spanned **five distribution ecosystems: GitHub Actions, Docker Hub, npm, PyPI, and OpenVSX**, with the compromise of one project supplying the credentials used against the next.
- **Trivy → KICS:** credentials taken during the Trivy scanner compromise were turned on the **Checkmarx KICS** GitHub actions days later.
- **Trivy → LiteLLM:** **LiteLLM's own build pipeline installed Trivy without pinning it to a verified version.** The poisoned scanner then captured the project's publishing token, which the actor used to push the backdoored **LiteLLM** releases in late March. LiteLLM routes requests across LLM providers and is the point where an organization's provider keys are consolidated, making it a high-value credential target.

## Reported scale
- **AFP:** the malicious code **potentially compromised more than 1,000 organizations** globally, enabled the theft of **more than 500,000 credentials**, and led to the exfiltration of **at least 300 GB** of data.
- **Unit 42** published the same two figures in March, hedged as what the actor "may have exfiltrated."
- **CloudSEK** (August): reconstructed exposure of **more than 2,500 organizations** and roughly **434,000 CI/CD pipelines**; noted that credential theft is not proof of successful compromise, and that the **confirmed** victim count is the **16 organizations** TeamPCP published on its leak site as of late March.
- **Hudson Rock** (August): attributed **118,829 CI runner dumps to 2,488 corporate domains** from a **153 GB archive** of the attackers' own exfiltrated data.
- **StepSecurity:** analysis of the CloudSEK dataset found **GitLab** led the affected platforms (**1,064 organizations**), ahead of **GitHub Actions (618)**, **Azure DevOps (233)**, **Jenkins (105)**, **Bitbucket Pipelines (94)**, and **CircleCI (15)**.
- **PyPI status (The Hacker News, August 27):** the two malicious **LiteLLM** builds no longer appear in the package's release history, but both still return **HTTP 200** from PyPI's CDN at their direct package URLs five months after removal from the index.
- **TeamPCP-linked infrastructure** has been disrupted; treat surviving tokens, leaked credentials, and re-published packages as still live until rotated.

## Durable defender guidance
- **Treat the March 2026 exposure window as open until you prove otherwise.** Rotate **all CI/CD secrets, publishing tokens, and cloud credentials** accessible during the window for any project that used or depended on **Trivy**, **Checkmarx KICS**, or **LiteLLM**, or that ingested artifacts from a poisoned build. The FBI explicitly advises treating exfiltrated data and credentials as a persistent risk because "affiliated threat actors are likely to weaponize them long after the initial compromise."
- **Pin verified versions.** The LiteLLM compromise exploited an **unpinned Trivy install** in a build pipeline. Pin scanner and tool versions to a verified digest or version and verify supply provenance (Trusted Publishing / OIDC where available) to prevent a re-used poisoned binary from re-stealing publishing tokens.
- **Hunt the five ecosystems.** Search **GitHub Actions** (workflow audit logs, `id-token` / OIDC claims, unexpected publish jobs), **Docker Hub** (unexpected image tags / re-pushes), **npm** (postinstall scripts, unexpected versions), **PyPI** (suspended / re-listed builds), and **OpenVSX** (unexpected extension releases) for the actor's publishing footprint.
- **Assume cross-project credential reuse.** Because credentials from one compromised project funded the next, a hit on any of the three named projects is a signal to review the organization's entire dependency graph, not just the named package.
- **Preserve evidence.** Retain workflow logs, package-index responses, registry audit logs, and exfiltration indicators across the window for correlation with the ongoing law-enforcement matter.

## Confidence and caveats
- The charging is **allegation-based**; the individuals are presumed innocent, and no charge names a specific compromised project.
- Scale figures (1,000+ organizations, 500,000+ credentials, 300+ GB; 2,500+ orgs / 434,000 pipelines; 118,829 dumps / 2,488 domains) come from the AFP, Unit 42, CloudSEK, Hudson Rock, and StepSecurity respectively and use **different collection and classification windows** — use their union for scoping, and do not treat any single count as final.
- "Credential theft ≠ compromise": the confirmed victim count is the 16 leak-site organizations; reconstructed exposure figures are lower-bound scoping aids, not confirmed intrusions.
- The PyPI "still returns 200 at the direct URL" detail reflects a CDN caching / content-retention artifact, not an active malicious release; verify against the index, not the bare object URL.

## Related pages
- [TeamPCP actor page](../actors/teampcp.md)
- [LiteLLM compromise](litellm-compromise.md)
- [LiteLLM CVE-2026-42271 MCP/stdio command injection](litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [Telnyx PyPI TeamPCP compromise](telnyx-pypi-teampcp-compromise.md)
- [Bitwarden CLI / Checkmarx Shai-Hulud third coming](bitwarden-checkmarx-shai-hulud-third-coming.md)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md)
- [StepSecurity state of open source supply chain attacks 2026](stepsecurity-state-of-open-source-supply-chain-attacks-2026.md)

## Sources
- The Hacker News: [Alleged TeamPCP Hackers Charged in Australia Over Major Supply Chain Attacks](https://thehackernews.com/2026/08/alleged-teampcp-hackers-charged-in.html) — August 27, 2026 (summarizing the AFP / WAPF / FBI joint release)
- Australian Federal Police media release (joint with WAPF / FBI) — August 27, 2026
- FBI Cyber Division joint media release (Assistant Director Brett E. Leatherman) — August 27, 2026
- The Hacker News confirmation via PyPI (August 27, 2026): two malicious LiteLLM builds absent from release history but still serving HTTP 200 at direct CDN URLs
