# Spring Ring: Microsoft Teams vishing campaigns that escalated to an NTLM-relay domain takeover (Unit 42, Aug 31, 2026)

## Tags
- ops
- operations
- social engineering
- vishing
- voice phishing
- Microsoft Teams
- RMM
- PetitPotam
- NTLM relay
- authentication coercion
- PowerShell RAT
- AMSI bypass
- browser extension sideloading
- lateral movement
- identity attack
- Cloaked Ursa
- APT29
- Unit 42
- SaaS
- help desk impersonation

## Summary

On **August 31, 2026**, Unit 42 published "**Spring Ring: An Inside Look at Voice Phishing Campaigns in Microsoft Teams**" (Noam Sala), describing a coordinated social-engineering operation active **January–April 2026** that used **external Microsoft Teams accounts impersonating internal IT help desk** to conduct **vishing** calls against employees, then coerced victims into installing RMM tools or executing attacker payloads. The operation targeted **more than 150 employees across at least 10 companies** in various industries. Two campaigns (A and B) shared the Teams-vishing front but diverged sharply in execution: Campaign A installed an **obfuscated PowerShell RAT** (AMSI bypass, C2 at `san-sid[.]com`); Campaign B delivered a **tailored per-organization/per-user S3-hosted executable** that staged persistence, sideloaded an Edge extension, and attempted a **PetitPotam NTLM relay attack against the domain controller** for domain-level privilege — the DC coercion was blocked by Unit 42 MDR.

## Attribution and context

- **Unit 42 names the operation "Spring Ring."** No further actor identification is public as of publication; the post explicitly frames it against the broader trend toward trusted-collaboration-tool attacks and contrasts it with **Cloaked Ursa (aka APT29)**'s earlier Teams campaigns, which relied on credential harvesting and fake Entra ID tenants rather than live voice interaction.
- Unit 42 states there is **no evidence of a Microsoft product compromise or vulnerability** in this campaign — the abuse is of legitimate Teams external-chat / voice-call features.
- Context metrics cited: collaboration-tool phishing was **42% of all phishing alerts** in Cortex in the first four months of 2026 (up from 30% the prior period); KnowBe4 measured **Teams-based attacks up 41%** between October 2025 and March 2026, driven in part by Teams' default "Chat with Anyone" feature.

## Campaign anatomy

**Identity layer.** Attackers provisioned external `.onmicrosoft[.]com` tenants with authority-suggesting subdomains and role-named personas:
- `ithelp@InternalSystemsDaily[.]onmicrosoft[.]com`
- `HelpDesk@ITProtectionDepartment[.]onmicrosoft[.]com`
- `itadmin@MandatoryNetworkMonitoring[.]onmicrosoft[.]com`
- `Internal@InternalUSAHelpDeskIT[.]onmicrosoft[.]com`
- `ithelpdesk@CertifiedUpdateNetwork[.]onmicrosoft[.]com`
- plus individual-name personas (e.g., `patrick[..]@infrastructureopsdesk.onmicrosoft[.]com`, `robert[..]@systemdeploymentcenter.onmicrosoft[.]com`, `clara[..]@systemsupportoperations.onmicrosoft[.]com` — names partially redacted; the names are of legitimate industry personnel, not an account compromise).

**Interaction pattern.** Chat first, then an immediate unsolicited voice call. Attempts ranged from ~30-second dials/voicemails to **10–15 minute successful sessions**; one spoofed identity approached **5–6 targets within minutes**. Source IPs frequently originated from **commercial VPN services**. 26 distinct spoofed identities were observed across the campaigns.

## Campaign A: RMM → obfuscated PowerShell RAT

1. Victim (convinced they were talking to their own IT) launched built-in **Quick Assist** or downloaded third-party **RMM software**; attacker requested remote control.
2. Post-control enumeration: `whoami /groups`, `net group /dom`.
3. PowerShell downloader fetched an obfuscated PowerShell RAT from **`san-sid[.]com`**.
4. De-obfuscated payload: a **nine-line C2 stager** that disables AMSI via the **`amsiInitFailed`** flag, verifies the bypass with a test scan, then encrypts host data and beacons to `san-sid[.]com` for further payloads. Obfuscation used variable manipulation, arithmetic obfuscation, and anti-analysis bloat designed to time out de-obfuscation tools.
5. Endpoint detection blocked execution at the malware-execution phase (Cortex XDR agent).

## Campaign B: tailored S3 dropper → headless Edge → PetitPotam DC coercion

1. Victim was directed to a **per-company/per-user S3 endpoint**, e.g. `<company_name>-org-filters-update-<victim_name>.s3.us-west-2.amazonaws[.]com`, with the matching `.exe` filename — infrastructure and naming tailored to the target org and individual user.
2. Execution chain:
   - **Staging/persistence:** the executable moved itself to `\Temp\` and spawned persistence copies named **`vhlp-*.exe`** and **`scnr-*.exe`**.
   - **Browser hijacking:** launched a **hidden, headless Microsoft Edge** and wrote a **sideloaded Edge extension** to disk.
   - **Lateral movement / authentication coercion:** Python at **`C:\ProgramData\IntegrityData\python.exe`** ran SMB port-445 scanning against internal servers and generated NTLM traffic toward the DC, then attempted a **PetitPotam** exploit to coerce the DC into authenticating back to an attacker-controlled machine (NTLM relay → domain-level privileges).
3. The DC coercion was **blocked by Unit 42 MDR**; domain takeover did not complete in this case.

## Durable detection / defensive heuristics

- **Teams identity profiling:** external `.onmicrosoft[.]com` tenants whose subdomains contain authority keywords (`internal`, `certified`, `network`, `infrastructure`, `helpdesk`, `support`) plus generic or real-person "technician" display names; commercial-VPN source IPs; rapid chat→unsolicited-voice-call transition; high per-identity contact volume (5–6 targets within minutes); 30-second probe calls preceding 10–15-minute successful sessions.
- **Endpoint:** unsolicited RMM execution by users who do not need remote support; `amsiInitFailed`-flag AMSI bypass PowerShell; `vhlp-*.exe` / `scnr-*.exe` in `\Temp\`; headless Edge with a sideloaded extension; `C:\ProgramData\IntegrityData\python.exe`; SMB 445 scan + NTLM coercion patterns from a user-level host; `san-sid[.]com` and `<company>-org-filters-update-<user>` S3 URL shapes.
- **Domain:** PetitPotam / NTLM-relay alerts from a workstation context should be treated as high-confidence lateral movement; restrict machine-account relay and patch PetitPotam-prone KB3249402 / "Coerced" hardening (no ANonymous / restrict machine-account NTLM where feasible).
- **Platform hygiene:** audit who can chat with anyone externally in Teams (default "Chat with Anyone"), restrict external guest/external-tenant chat + voice, and alert on external-tenant chat creation followed by a call.

## Related pages

- [Impersonating IT support: Teams external-collaboration intrusion — MSI + portable Node.js + JavaScript implant, WinRM pivoting to DCs/CA (Microsoft, Sep 2, 2026)](microsoft-teams-it-support-impersonation-msi-nodejs-implant-winrm-september-2026.md)
- [Microsoft Teams external-chat phishing pattern](../patterns/microsoft-teams-external-chat-phishing.md)
- [Collaboration-channel identity-abuse pattern](../patterns/collaboration-channel-identity-abuse.md)
- [APT29 / Cozy Bear / Midnight Blizzard profile (Cloaked Ursa Teams campaigns)](../actors/apt29-cozy-bear-midnight-blizzard.md)

## Sources

- Unit 42 — "Spring Ring: An Inside Look at Voice Phishing Campaigns in Microsoft Teams" (Noam Sala; published 2026-08-31): [https://unit42.paloaltonetworks.com/spring-ring-voice-phishing-campaigns/](https://unit42.paloaltonetworks.com/spring-ring-voice-phishing-campaigns/)
