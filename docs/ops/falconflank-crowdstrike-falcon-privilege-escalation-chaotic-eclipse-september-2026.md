# FalconFlank: Chaotic Eclipse releases 0-day privilege-escalation PoC in CrowdStrike Falcon Sensor — abuses "Office malicious macros remediation" (THN, Sep 3, 2026)

## Tags
- ops
- operations
- CrowdStrike Falcon
- Falcon Sensor
- privilege escalation
- zero-day
- 0-day
- local exploit
- endpoint security
- EDR
- Office macros
- policy-setting abuse
- Chaotic Eclipse
- INFINITE NIGHTMARE
- MSNightmare
- Nightmare-Eclipse
- HardBreacher
- ShieldBreak
- RoguePlanet
- CVE-2026-69414
- CVE-2026-50656
- Windows
- Windows Server 2025
- Windows 11 25H2
- patch bypass
- security tool abuse

## Summary

On **September 3, 2026**, The Hacker News reported that the security researcher known as **Chaotic Eclipse** (a.k.a. **INFINITE NIGHTMARE, MSNightmare, and Nightmare-Eclipse**) released **FalconFlank**, a proof-of-concept for a **zero-day local privilege-escalation flaw in the CrowdStrike Falcon Sensor**. The PoC "abuses the **office malicious macros remediation**" feature of the Falcon Sensor and works on a **fully updated Windows 11 25H2 or Windows Server 2025** host running CrowdStrike Falcon. CrowdStrike confirmed it is **actively investigating** and is advising customers to **disable the "Microsoft Office File Suspicious Macro Removal" Windows policy setting**, while noting customers remain protected through the "Cloud Anti-malware for Microsoft Office Files" settings; a **FalconFlank Tech Alert** was posted in the CrowdStrike support portal. FalconFlank is the **third** in a rapid 2026 series of endpoint-security zero-days from the same researcher: **HardBreacher** (Kaspersky Endpoint Security for Windows 14.0.0.504, resolved via auto-update) and **ShieldBreak / CVE-2026-69414** (Microsoft Defender, a patch bypass for CVE-2026-50656 / RoguePlanet, still unfixed by Microsoft as of Sep 3). The durable pattern: **the security tool itself is the escalation primitive** — abusing an EDR/AV *remediation* feature (intended to clean malicious Office files) into a local LPE vector.

## Attribution and context
- **Chaotic Eclipse** — published researcher alias; a series of high-impact 2026 Windows/EDR zero-days all credit this handle: **FalconFlank** (CrowdStrike, Sep 3), **HardBreacher** (Kaspersky, days earlier), **ShieldBreak / CVE-2026-69414** (Microsoft Defender, "last month" per THN; a documented patch-bypass of CVE-2026-50656 / RoguePlanet). No independent attribution of the underlying group/individual is public.
- **CrowdStrike** — the vendor of the affected product. Responds with investigation + a targeted policy mitigation + a support-portal Tech Alert, not an immediate code fix.

## Technical detail
- **Target component:** the **Falcon Sensor**'s **Office malicious-macro remediation** subsystem — the part of the agent that inspects and "remediates" Office files flagged for suspicious macros.
- **Abuse class:** the PoC turns that *remediation* path into a **local privilege escalation** — i.e., the code path that is supposed to *clean* untrusted Office content is instead leveraged to gain elevated execution. (THN's writeup does not disclose the full sink; the mechanism is framed as "abuses the office malicious macros remediation.")
- **Reproduction conditions:** **fully updated Windows 11 25H2** or **Windows Server 2025** with the Falcon Sensor installed. The researcher notes CrowdStrike "may already have detections for the flaw by now," so testing requires **adding the PoC to exclusions or obfuscating it and changing the DLL-load technique**.
- **Artifacts / artifacts to hunt:**
  - FalconFlank PoC DLL-load activity around the Office-macro remediation path.
  - Any newly written/loaded DLL in `C:\Windows\System32` (the common sink in this researcher's prior work — e.g., ShieldBreak's `phoneinfo.dll`, HardBreacher's `MY_SNAKE_IS_SOLID.dll`).
  - Process lineage where a Falcon/Office-remediation context spawns an elevated (SYSTEM-equivalent) child.
- **Mitigation (vendor):** **Disable the "Microsoft Office File Suspicious Macro Removal" Windows policy setting**; remain protected via the **Cloud Anti-malware for Microsoft Office Files** settings; follow the **FalconFlank Tech Alert** in the CrowdStrike support portal.

## Why this matters
- **The defender becomes the exploit.** A privilege escalation that rides *inside* an EDR's own Office-macro-remediation feature means the control meant to stop macro attacks can instead *deliver* elevation — a "trusted-binary-abuse" class that is hard to block by allowlisting because the parent is the security agent itself.
- **Fully-patched hosts are affected.** Works on **fully updated Win11 25H2 / Server 2025** — no missing patch; this is a 0-day in the security tool, not the OS.
- **Series, not an outlier.** FalconFlank is the **third** endpoint zero-day from Chaotic Eclipse within ~5 weeks (Kaspersky → Microsoft Defender → CrowdStrike). The recurring theme is *abusing an AV/EDR remediation/clean path* for LPE — a consistent tradecraft signature defenders should treat as a standing threat class.
- **Actionable, specific mitigation.** CrowdStrike names the exact policy setting to disable and the exact protective setting that remains — a concrete, testable response.

## Detection / defensive heuristics
- **Immediate (per vendor):** disable the **Microsoft Office File Suspicious Macro Removal** Windows policy setting; confirm the **Cloud Anti-malware for Microsoft Office Files** settings are active; apply the **FalconFlank Tech Alert** guidance.
- **Host-based hunting** (no network IOCs; this is local):
  - New/unexpected DLLs written to `C:\Windows\System32` by a Falcon/Office-remediation process.
  - Elevated (SYSTEM / high-integrity) child processes spawned from the Falcon Sensor's Office-macro-remediation context.
  - Unusual DLL-load activity around Office files under Falcon inspection, especially after an "exclusion" or obfuscated-load pattern.
- **Series-aware monitoring:** track Chaotic Eclipse's published PoCs (FalconFlank, HardBreacher, ShieldBreak) as a *standing tradecraft pattern* — any AV/EDR "remediation" or "clean" code path that writes into system directories and then spawns elevated execution should be treated as a potential LPE.

## Assessment limits
- **Mechanism depth.** THN reports the abuse class ("office malicious macros remediation") but does not publish the full code-level sink; the exact flaw (race, write-what-where, token duplication, etc.) is not detailed in this report. Re-check CrowdStrike's Tech Alert and any subsequent vendor blog for the precise mechanism and the shipped fix.
- **No confirmed in-the-wild exploitation.** This is a **researcher PoC**, not a reported compromise. The researcher notes CrowdStrike may already have detections.
- **Fix status.** As of Sep 3, CrowdStrike was "actively investigating"; mitigation is a **policy-setting toggle**, not a confirmed sensor update. Re-check the sensor release notes for a code fix.
- **Alias attribution.** "Chaotic Eclipse" and its aliases are a published researcher handle; the underlying identity/group is not independently attributed.

## Related pages
- [Microsoft Defender CVE-2026-50656 RoguePlanet / ShieldBreak patch bypass](microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md)
- [Pegasus iMessage zero-click in Serbia (Citizen Lab / SHARE, Sep 3, 2026)](pegasus-imessage-zero-click-serbia-student-movement-citizen-lab-share-september-2026.md)
- [MECCHA CHAMELEON second delayed RCE via custom map (Aikido, Sep 3, 2026)](meccha-chameleon-delayed-rce-custom-map-arbitrary-file-write-aikido-september-2026.md)

## Sources
- The Hacker News — "Researcher Releases FalconFlank PoC Showing Privilege Escalation in CrowdStrike Falcon" (Ravie Lakshmanan; published 2026-09-03): [https://thehackernews.com/2026/09/researcher-releases-falconflank-poc.html](https://thehackernews.com/2026/09/researcher-releases-falconflank-poc.html)
