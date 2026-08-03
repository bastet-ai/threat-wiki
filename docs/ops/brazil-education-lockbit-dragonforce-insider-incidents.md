# Brazilian education LockBit, DragonForce, and insider incidents

## Summary
Kaspersky's Global Emergency Response Team (GERT) published an incident-response review of attacks against Brazilian educational institutions from January 2025 through June 2026. The dataset covers public and private organizations in São Paulo, Rio de Janeiro, and Pernambuco and shows a mix of ransomware, exposed-service and valid-account compromise, privilege escalation, and insider keylogging.

Three cases provide durable defender detail: a leaked-builder LockBit variant delivered through a compromised privileged account and moved manually with PsExec; DragonForce ransomware deployed after a compromised account installed AnyDesk; and a Portuguese-language Python keylogger run from a shared user's VS Code directory, with USB activity suggesting manual collection. The report does not attribute these incidents to a named operator.

## Tags
- ops
- operations
- Brazil
- education
- academic sector
- incident response
- ransomware
- LockBit
- LockBit 3.0
- DragonForce
- insider threat
- keylogger
- Python
- valid accounts
- exposed applications
- AnyDesk
- PsExec
- RDP
- AV killer
- Windows Defender impairment
- GodPotato
- SweetPotato
- BadPotato
- USB exfiltration
- shared accounts
- legacy systems
- digital forensics
- Amcache
- Prefetch
- UserAssist
- MFT
- USN Journal
- Program Compatibility Assistant
- Kaspersky GERT

## Dataset findings
- GERT reviewed cases opened from **January 2025 through June 2026**. Most were in São Paulo, with additional cases in Rio de Janeiro and Pernambuco.
- **60%** of organizations requesting response were private and **40%** were public. Kaspersky did not publish an absolute case count, so these percentages should not be treated as population-wide prevalence.
- **40%** of incidents were rated high severity and **60%** medium severity. High-severity cases were mainly ransomware-related.
- Private institutions were more frequently represented in the ransomware cases, while public-institution cases more often involved suspicious endpoint activity and privilege-escalation attempts.
- The most common initial-access paths were valid accounts, exploitation of public-facing applications, and insiders.
- Common post-access tools included Potato-family privilege-escalation exploits, AnyDesk for remote control, PsExec for lateral movement, and antivirus-killer malware in ransomware incidents.
- Active attacker activity was usually detected within minutes or hours, but technical response averaged **9.6 hours**, illustrating the longer triage and scoping burden after containment.
- Responders still found Windows 10 after its October 2025 end of support and unpatched Windows Server 2016 systems. Kaspersky did not tie a specific named vulnerability to the three detailed cases.

## Case 1: leaked-builder LockBit
A compromised privileged account gave the attacker access to internal systems containing student profiles and other data. The operator deployed a custom LockBit build created with the publicly leaked builder and encrypted file servers and databases. Kaspersky found no evidence of data exfiltration from the examined systems, which is narrower than proving no data left the wider environment.

The extracted ransomware configuration enabled local-disk and network-share encryption, process and service termination, Defender impairment, free-space wiping, wallpaper changes, and self-deletion. Built-in impersonation, PsExec spreading, and Group Policy spreading were disabled. The attacker instead moved manually with PsExec.

Useful reconstruction artifacts included:

- PsExec-associated `.KEY` files in the NTFS USN Journal, which helped identify previously compromised systems;
- Prefetch executions of `PsExecSvc.exe` and the ransomware filename `LBB.exe`;
- a batch script that enabled RDP and its firewall rule, changed multiple Microsoft Defender policy values, stopped `WinDefend`, and set it to disabled; and
- evidence that the script used administrative credentials to disable the deployed EDR.

The reconstructed activity window on the examined host ran from roughly 05:30 UTC until the final `LBB.exe` execution at 10:00 UTC on the same day.

## Case 2: DragonForce through AnyDesk
In a separate case, an attacker used a compromised user account to install AnyDesk, then ran a DragonForce ransomware sample named `1.EXE`. The operator cleared system logs after encryption.

Prefetch and `Amcache.hve` preserved the ransomware execution despite log deletion. Amcache also supplied the sample's SHA-1 value, allowing responders to identify it as DragonForce. The report does not publish that hash or claim a specific DragonForce affiliate.

## Case 3: shared-account insider keylogger
A shared Windows account allowed a suspected insider to run `Windows Host Widgets.exe` and `Windows Host Widgets_.exe` from:

```text
C:\Users\<user>\.vscode\dlo
```

Program Compatibility Assistant, Amcache, Prefetch, and UserAssist artifacts showed repeated interactive execution. Both executables contained the same decompilable Python keylogger. It used Portuguese identifiers, tracked Caps Lock state, and wrote hidden `cacheX.txt` logs, incrementing `X` on each run.

The malware had no persistence or automated exfiltration. USB connections near execution times suggest that someone manually retrieved the logs with removable media, but Kaspersky could not conclusively identify an individual without additional evidence or physical-security footage. The organization reset affected-account passwords.

## Defender actions
1. **Eliminate shared accounts.** Assign individual identities, enforce least privilege, and retain authentication and endpoint telemetry sufficient to connect activity to a person and device.
2. **Require phishing-resistant MFA on exposed access paths.** Prioritize VPN, remote administration, webmail, and other public-facing services; review privileged accounts and invalidate leaked or reused credentials.
3. **Control remote-access software.** Allow-list approved RMM tools and alert on first-seen AnyDesk, TeamViewer, service creation, unexpected installers, and remote-control use from unusual identities or hosts.
4. **Hunt manual ransomware staging.** Correlate PsExec or `PsExecSvc.exe`, `.KEY` artifacts, RDP enablement, port 3389 firewall changes, Defender policy edits, EDR administrative-disable events, log clearing, and rapid fan-out to file servers or databases.
5. **Retain diverse forensic artifacts.** Central logs are not enough. Preserve Amcache, Prefetch, PCA, UserAssist, MFT, USN Journal, service, registry, EDR, authentication, RMM, and USB-device records.
6. **Detect user-space keylogging paths.** Investigate unexpected executables and hidden incrementing text files under `.vscode` or other user-writable developer directories, especially on shared or lab machines.
7. **Constrain removable media.** Apply device control where appropriate and correlate USB insertion with suspicious process execution, file creation, and account access.
8. **Remove unsupported systems and patch exposed applications.** Isolate systems that cannot be upgraded and reduce their credentials, network reachability, and administrative trust.
9. **Protect recovery paths.** Keep isolated, immutable, tested backups and ensure compromised domain or endpoint administrators cannot erase every recovery copy.
10. **Preserve before rebuilding.** Collect volatile state and high-value filesystem artifacts from representative hosts before remediation; attacker log clearing does not remove all reconstructable evidence.

## Evidence and attribution caveats
The source is a retrospective summary of Kaspersky GERT engagements, not a census of Brazilian education-sector incidents. It omits the absolute number of cases, affected organization names, sample hashes, source infrastructure, exploited-application details, and named operator attribution. The percentages therefore describe the reviewed response dataset only.

`LockBit` and `DragonForce` identify ransomware families or ecosystems, not necessarily the human operators behind each intrusion. In particular, public availability of the LockBit builder makes family-level code identification insufficient for actor attribution. The insider case supports local execution and likely USB collection but not a conclusive individual attribution.

## Related pages
- [Toy Ghouls GenieLocker ransomware activity](toy-ghouls-genielocker-ransomware.md)
- [Anubis ransomware CitrixBleed 2 / RMM / cloudflared intrusions](anubis-ransomware-citrixbleed2-rmm-cloudflared.md)
- [The Gentlemen ransomware](../tools/the-gentlemen-ransomware.md)

## Sources
- Kaspersky Global Emergency Response Team, “An analysis of incidents at Brazilian educational institutions,” 2026-08-03: [https://securelist.com/incidents-at-brazilian-educational-institutions/120803/](https://securelist.com/incidents-at-brazilian-educational-institutions/120803/)
