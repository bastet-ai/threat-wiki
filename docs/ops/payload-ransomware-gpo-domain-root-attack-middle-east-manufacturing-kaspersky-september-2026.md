# PAYLOAD ransomware delivered domain-wide impact entirely through Active Directory: a Kaspersky GERT incident where the "ransomware" was two malicious GPOs linked at the domain root — ransom wallpaper, logon banner, firewall-off, and local-admin disablement across every endpoint with NO encryptor, NO resident binary, and NO endpoint persistence (September 21, 2026)

## Summary

Kaspersky's Global Emergency Response Team (GERT) published a full incident report on **September 21, 2026** ("Group Policy hijacked: PAYLOAD ransomware weaponizes Active Directory GPO," Securelist, canonical URL verified live by this wiki at capture) covering an **April 2026 intrusion at a Middle East manufacturing organization** in which the entire Windows-side attack was implemented **inside Active Directory itself**: the actor obtained domain-admin-equivalent control and authored a malicious Group Policy Object **named literally `PAYLOAD`** (`{C897F2C7-C2AC-4E6F-BF48-58036FF29E79}`), linked at the domain root.

Forensic triage (Apr 15–16) confirmed the headline finding: **no files encrypted on any Windows machine, no malicious binaries resident on disk, no endpoint persistence, no active malicious processes.** Through legitimate GPO mechanisms the single object dropped the ransom note (`SYSVOL\hello.txt` → `README-payload.txt` on every desktop, `C:\`, `D:\` via the Group Policy Files CSE), set the ransom legal-notice caption ("Welcome to Payload!") and text via registry policy, forced the ransom image (`SYSVOL\payload.jpg`) as **lock-screen and wallpaper**, and **disabled the local Administrator account** across the domain via `GptTmpl.inf`. A second domain-root GPO, **`win Firewall Off`** (`{22099AD2-E062-4F56-B574-5099BBA4E7A6}`), disabled Windows Firewall on domain/private/public profiles everywhere (T1562.004). The only actual cryptomalware found was a **PAYLOAD ESXi sample targeting the Linux servers**; data exfiltrated from file servers during the quiet window was later published on the dark web.

Two 2026 ransomware trends converge here, and Kaspersky names them: **living-off-the-land abuse of a channel EDR is designed not to inspect** (GPO is signed, allowlisted, SYSTEM-privileged distribution — the file- and process-based detection stack never sees the payload because there is no file and no process), and **encryptionless extortion** (leverage = operational disruption + data publication, not cryptographic denial).

## Timeline (per Kaspersky GERT)

| Date (Apr 2026) | Event |
|---|---|
| 11 Apr | Initial access: valid **compromised domain credential** authenticates to the org's **FortiGate SSL VPN** (T1078 + T1133). Insufficient FortiGate logging prevented reconstructing how the credential fell; spraying/stuffing, phishing, and IAB purchase all kept as plausible hypotheses. |
| 13 Apr | **`PAYLOAD` GPO** authored and linked at domain root; `payload.jpg` + `hello.txt` staged in SYSVOL; second GPO **`win Firewall Off`** linked; endpoints cache the policy. |
| 13 Apr | Data exfiltration observed from file servers and several additional systems. |
| 14 Apr | **Detonation**: routine endpoint reboots apply the computer-configuration policies en masse — ransom wallpaper/lock screen/banner appear, local admins disabled. The attack had sat dormant in the GPO cache for a day because computer policy application waits for reboot/refresh. |
| 15–16 Apr | GERT engaged; confirms no encryption, no resident malware, no persistence. |

## What makes this durable intel

1. **The GPO cache is a timed detonator.** The MFT + Group Policy History/Shadow registry analysis shows weaponization (13 Apr) and impact (14 Apr) separated only by the reboot cycle. Kaspersky draws both defender readings: the gap gives the actor a **quiet exfil window** between weaponization and impact, and it **severs the temporal link** between the cause (a GPO-creation event in directory logs) and the effect (mass user-visible disruption) — timeline reconstruction collapses without DS-change auditing.
2. **Detection has to move to the directory and SYSVOL, not the endpoint.** Because no binary exists, the highest-value telemetry is: **Event ID 5137** (new `groupPolicyContainer` created by a non-GPO-admin account), **5136** (changes to `gPLink` at the domain root or sensitive OUs; `gPCMachineExtensionNames` / `gPCUserExtensionNames` / `gPCFileSysPath` / `versionNumber` edits on any GPO), **5141** (GPO deletion), plus **SYSVOL file-integrity monitoring** (unexpected images, text files, `ScheduledTasks.xml`, modified `registry.pol` / `GptTmpl.inf`). A subtle inversion Kaspersky calls out: **SYSVOL content changes WITHOUT a matching 5136** indicate direct template editing via PowerView/SharpGPOAbuse-class tooling that bypasses the GPMC path — missing audit events are themselves the signal.
3. **The endpoint artifacts are the GPO keys themselves.** Loopback processing is provable from the `HKCU\…\Group Policy\State\<SID>\Loopback-GPO-List` entry (user settings applied machine-wide — how the wallpaper hit every user); the History/Shadow keys dated the application to 13 Apr.
4. **Remediation order is DC-first.** Kaspersky's four phases: (1) domain-controller actions before touching endpoints — unlink/remove the malicious GPOs and clean SYSVOL, because endpoint cleanup cannot remove a policy distribution channel; (2) AD/GPO hardening (constrain who can create and link GPOs — Group Policy Creator Owners + domain link rights was the actor's likely route per GERT); (3) credential and access hardening; (4) detection and monitoring per above. An org that reimaged endpoints but left the GPO linked would be re-ransomed at the next policy refresh.
5. **PAYLOAD family capabilities, scoped honestly.** Kaspersky separates what happened in THIS incident from family-level capabilities derived from public reverse engineering of PAYLOAD Windows samples: optional **event-log clearing** (dynamic `wevtapi.dll` load → `EvtOpenChannelEnum`/`EvtNextChannelPath`/`EvtClearLog` across Security/System/Application/PowerShell channels), **security-process and service termination**, and **VSS deletion** (confirmed in an encrypting PAYLOAD sample, not in this incident). ETW patching, BYOVD, and ESXi security-policy weakening are explicitly labeled **ecosystem-relevant, not confirmed PAYLOAD features**. The report's own discipline is the template: family capability ≠ incident attribution.
6. **Lineage.** GPO abuse as a ransomware distribution channel has a long public record Kaspersky recites — Ryuk (GPO + SYSVOL startup items + PsExec), LockBit affiliates editing `ScheduledTasks.xml` in SYSVOL, BlackCat/ALPHV scheduled tasks via GPO — what PAYLOAD adds is using policy settings **for pure impact** (notes, wallpaper, banner, account disablement, firewall-off) rather than as an encryptor launcher.

## Hunt guidance (from the report, condensed)

- Enable **Advanced Audit Policy → DS Access → Audit Directory Service Changes** on every DC; alert on 5137/5136/5141 involving `groupPolicyContainer`/`gPLink`, especially at domain root and by non-standard accounts.
- FIM on `\\<domain>\sysvol\<domain>\Policies\` for non-replication-origin files (images, txt, scripts) and modified `registry.pol`/`GptTmpl.inf`.
- Endpoint post-detonation tell: sudden domain-wide change in the applied policy set (Microsoft-Windows-GroupPolicy/Operational) + `Loopback-GPO-List` state entries.
- Treat SYSVOL-modified-without-5136 as direct-edit tooling (PowerView/SharpGPOAbuse class).
- FortiGate (and any SSL VPN) auth logs need retention long enough to survive an IR engagement — GERT could not reconstruct initial access because the appliance under-logged.

## Caveats

- Vendor incident report (Kaspersky GERT) — single-source; victim unnamed (Middle East manufacturing); no actor attribution is offered for the intrusion, and the PAYLOAD family linkage is by tooling/GPO naming, not operator identity.
- The `T1685.x` technique numbering used in the report differs from the widely known `T1070.001`/`T1562.x` IDs (Kaspersky notes the former numbering); map to whichever ATT&CK matrix version your SIEM content uses.

## Tags
- ops
- ransomware
- PAYLOAD
- Active Directory
- Group Policy
- GPO
- SYSVOL
- domain controller
- encryptionless
- extortion
- FortiGate
- SSL VPN
- living-off-the-land
- anti-forensics
- ESXi
- Kaspersky
- GERT
- detection-engineering
- incident-response
- Middle East

## Sources

- Kaspersky Securelist (Sep 21, 2026, canonical URL verified live by this wiki): [Group Policy hijacked: PAYLOAD ransomware weaponizes Active Directory GPO](https://securelist.com/tr/payload-ransomware-via-group-policy/121335/) — Ahmad Zaidi Said, Elsayed Elrefaei, Kaspersky Security Services.

## Related pages

- [DeadLock ransomware](../tools/deadlock-ransomware.md) — Polygon-configured recovery app; the on-chain recovery side of 2026 ransomware tooling
- [The Gentlemen / GigaWiper](../tools/the-gentlemen-ransomware.md) — destructive-tooling counterpart: recovery inhibition as the objective
- [Blackpoint ChainScript RAT](../tools/chainscript-rat-polygon-websocket-c2-blackpoint-september-2026.md) — same-week Blackpoint/Kaspersky reminder that impact delivery keeps moving into channels EDR doesn't inspect
