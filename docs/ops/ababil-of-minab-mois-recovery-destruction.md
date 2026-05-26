# Ababil of Minab MOIS-linked recovery-destruction campaign

## Summary
**Ababil of Minab** is a pro-Iranian persona that publicly claimed destructive intrusions in late March and early April 2026, including the Los Angeles County Metropolitan Transportation Authority incident. Gambit Security reports that forensic evidence ties the campaign to infrastructure and activity associated with Iran's Ministry of Intelligence and Security (MOIS), rather than a cleanly independent hacktivist crew.

The campaign targeted organizations in the United States, Israel, Saudi Arabia, and Turkey. Gambit describes exfiltration across the victim set and destructive operations at a subset of victims, with attackers deliberately striking virtualization, storage, applications, and backup infrastructure to deny recovery.

## Tags
- ops
- operations
- Iran
- MOIS
- Ababil of Minab
- destructive operations
- data exfiltration
- recovery denial
- backups
- virtualization
- storage deletion
- LA Metro
- hacktivist persona
- FileFiend
- wiper-adjacent
- operational resilience

## Why this matters
- The case shows a state-linked cluster using a public persona to claim or launder destructive activity.
- The destructive playbook is recovery-focused: delete virtual machines, storage volumes, databases, and backup infrastructure so normal restore paths fail in parallel.
- Gambit recovered custom exfiltration tooling and identified additional victims beyond those the persona chose to expose.
- The operation reinforces that backup and virtualization administration are Tier-0 security surfaces, not merely IT availability systems.

## Operational characteristics
- **Persona and timing:** Ababil of Minab surfaced publicly in late March and early April 2026 and claimed the LA Metro intrusion, data theft, and system destruction.
- **Attribution evidence:** Gambit says forensic evidence links the campaign to infrastructure and activity associated with a prior Iran-linked cluster publicly known as Black Shadow, which Israel's National Cyber Directorate attributed to MOIS.
- **Victim geography:** public and nonpublic victims span the United States, Israel, Saudi Arabia, and Turkey.
- **Exfiltration:** data theft occurred across the victim set. The Hacker News summary notes a bespoke C++ collection and exfiltration tool internally named **FileFiend**, able to enumerate local drives and SMB shares, walk file systems, and send files to hard-coded C2.
- **Alternate exfil path:** in some cases, data was compressed into RAR archives on an internal host, uploaded to the victim organization's public web root, then retrieved with Axel through proxychains.
- **Destruction:** where destructive actions occurred, the attackers targeted IT, application, virtualization, storage, and backup layers through both scripts and hands-on-keyboard activity.

## Defender heuristics
- Treat virtualization managers, backup consoles, storage arrays, and disaster-recovery tooling as privileged identity systems: require phishing-resistant MFA, least privilege, alerting, and separate break-glass controls.
- Continuously test immutable/offline backups against adversarial scenarios: domain compromise, backup-admin compromise, storage-volume deletion, VM deletion, and corrupted restore catalogs.
- Hunt for bulk VM deletion, datastore deletion, snapshot removal, backup-job disabling, backup repository tampering, database drops, and unusual administrative logins clustered near data staging or exfiltration.
- Monitor for internal hosts staging large RAR archives in public web roots, unexpected Axel downloads, proxychains use, and file walkers touching broad SMB shares.
- Preserve hypervisor, storage, backup, web-server, proxy, and identity logs immediately; recovery-denial campaigns can destroy the telemetry needed for root-cause analysis.

## Related pages
- [Handala](../actors/handala.md)
- [Seedworm / MuddyWater](../actors/seedworm-muddywater.md)
- [Langflow CVE-2025-34291 exploitation](langflow-cve-2025-34291-exploitation.md)

## Sources
- Gambit Security: https://gambit.security/blog-posts/babil-of-minab-iran-mois-destruction-campaign
- The Hacker News summary: https://thehackernews.com/2026/05/muddywater-uses-dll-side-loading-in.html
