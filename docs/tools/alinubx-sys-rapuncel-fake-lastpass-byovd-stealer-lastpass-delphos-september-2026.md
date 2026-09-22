# Alinubx.sys / Rapuncel: fake LastPass Authenticator installer, Microsoft-signed BYOVD driver that kills 145 security processes (LastPass + Delphos Labs, Sep 17/21, 2026)

## Summary

LastPass (the brand's own security team) and Delphos Labs disclosed on **September 17, 2026** (relayed by The Hacker News September 21) a Windows credential-theft campaign in which a **fake LastPass Authenticator installer** installs a **kernel driver signed through Microsoft's own Windows Hardware Compatibility Publisher (WHCP) attestation chain** — a driver whose only executed function is to **terminate 145 named antivirus/EDR/security processes from kernel level**, below the layer where those products can see or block anything. With security software down, the companion stealer (which LastPass calls **Rapuncel**) harvests saved passwords from more than two dozen browsers, cryptocurrency wallet files, Discord/Steam/Telegram sessions, Windows Credential Manager contents, and files named like "password"/"seed"/"recovery," then ZIPs and exfiltrates them.

The campaign is a textbook assembly of three durable failure modes:

1. **Attestation ≠ safety.** The driver was renamed `Alinubx.sys` from **`CcProtect.sys`, a driver from the Chinese disk-encryption product CnCrypt already cataloged on LOLDrivers as a process killer with public PoC code**. Same product name, version, and submitter — only the file name and description changed. That rename dropped detections from ~7/70 engines to **zero on VirusTotal**. Microsoft's signing dates the attestation to **March 2023**, years before the campaign. Researchers' framing: *"Microsoft attestation proves a driver passed through a trust pipeline. It does not prove the driver is safe."*
2. **The vulnerable-driver blocklist is a hash list, and this driver — renamed OR original — was never on it.** Delphos checked Microsoft's blocklist (on by default since the Windows 11 2022 update) on **August 20** and found neither file listed; it is still not listed as of the September 17 report. The blocklist matches known hashes — a renamed or recompiled driver produces a new hash the list does not carry, so the blocklist is structurally behind BYOVD reuse.
3. **App-bound encryption defeated by asking the browser to decrypt.** For Chrome/Edge's app-bound encryption (designed to stop exactly this theft), the stealer **injects code into the browser and asks the browser's own decryption service to release the passwords** — the trust boundary is walked through, not broken.

## Delivery chain

- **Lure:** a fake GitHub organization page `github.com/LastPass-Authenticator` that **ranks in search results** for terms like "LastPass Authenticator download" and mimics a real product page. The download button chains through several GitHub pages to an **attacker server serving impersonation pages for at least 40 brands** (LastPass statement). A near-identical second fake page for a "macOS LastPass" product was taken down before researchers could examine it. The real LastPass Authenticator ships only from lastpass.com and official app stores — **not GitHub**.
- **Dropper:** ZIP archives of **148 MB and 127.9 MB, padded with junk files so scanners with size limits skip them**. Inside: a renamed copy of Microsoft's genuine debug tool **`vsdbg.exe`** beside a malicious **`vsdbg.dll`** — classic DLL side-loading.
- **Escalation:** the loader tries three privilege-escalation paths, reaches **SYSTEM**, and installs the kernel driver as a service.
- **Driver:** `Alinubx.sys` carries the 145-name kill list and executes it at load. Its code ALSO contains file-hiding, process-injection, and web-traffic-rerouting routines gated on a configuration file the attackers did not ship — dormant capabilities. **The driver re-kills security tools and re-runs the stealer on every reboot**, defeating cleanup attempts that don't remove the service.
- **Lineage:** Delphos assesses with **high confidence** the loader was built with the **Cruciferra crypter** — a paid tool whose default kill list also holds 145 names and whose driver is interchangeable — and with **moderate confidence** that Rapuncel is a **relative (not identical build) of BoryptGrab**, the fake-repository stealer Trend Micro documented in March. Arctic Wolf separately reported a wave of **nearly 300 fake GitHub repositories** delivering this family in July. No victim count is public.

## Tags
- tool
- tools
- BYOVD
- bring your own vulnerable driver
- LOLDrivers
- kernel driver
- WHCP
- attestation
- Microsoft blocklist
- process killer
- EDR-killing
- DLL side-loading
- vsdbg
- stealer
- credential theft
- app-bound encryption
- browser injection
- password managers targeted
- fake installer
- fake GitHub organization
- search-ranking lure
- padding archive
- Cruciferra
- BoryptGrab
- LastPass
- Delphos Labs
- Windows
- brand impersonation

## Durable pivots (hunt these — lineage/behavior, not one file name)

| Artifact | Value |
| --- | --- |
| Driver service name | `NvFsFilter` |
| Driver path | `C:\Windows\System32\drivers\nvfsflt64.sys` |
| Driver file name | `Alinubx.sys` (operators already renamed once — expect renames) |
| Device path | `\\.\Alinubx` |
| Signer metadata | `Henan Dafeng Software` / contains `CnCrypt` |
| Behavior | driver load immediately followed by security-process terminations |
| Side-load pair | `vsdbg.exe` + same-directory `vsdbg.dll` (genuine Microsoft tool is single-file) |
| Archive tell | 100+ MB ZIP download for a consumer authenticator |

Community detection for this exact driver is published on LOLDrivers — but it is hash-matched and shares the same rename weakness.

## Defender guidance

- **Treat a machine that ran this as kernel-compromised.** Every browser-saved password on it is stolen, plus wallet files, Discord/Steam/Telegram sessions, and Credential Manager contents — the stealer copies these BEFORE the driver work begins. Rotate from a separate clean device. Rebuild (or at minimum kernel-level forensic inspect) rather than clean-and-hope: the driver re-kills protections and re-runs the stealer on every boot.
- **Blocklist your own drivers.** Microsoft's blocklist does not cover the CnCrypt lineage — push LOLDrivers entries into your own Windows Driver Control / SOC policy (deny-by-signer for `Henan Dafeng Software`/`CnCrypt` product metadata), and alert on driver-service creation (`System` event log 7045) naming non-Microsoft INF-signed kernel drivers on workstations.
- **App-bound encryption is not a safe default on shared/managed hosts** — its defense is the browser service itself, which injectable-process malware co-opts. Password managers whose vaults require a second factor outside the OS remain the compensating control.
- **Detection of the kill pattern beats detection of the file:** a burst of security-process exits shortly after a new driver-service load is behaviorally unmissable at the EDR-controller level, even when the endpoint agent is already dead — the controller sees the agent stop reporting.
- **For maintainers/orgs:** this family's distribution is **GitHub organizations that rank in search**. Treat top-search-result "product downloads" hosted on GitHub as hostile-by-default; pin vendor domains.

## Systemic read

Microsoft's response to Delphos (reported Aug 19): the behavior **does not meet Microsoft's definition of a security vulnerability** because the driver is not a Microsoft component; researchers were pointed to the separate blocklist-intake channel, which had not listed the driver as of disclosure. That is the durable governance gap: the attestation pipeline and the blocklist pipeline are separate systems with different definitions of harm, and BYOVD abuse falls between them. Compare the on-wiki **GodDamn/GentleKiller** BYOVD record and the **ShieldBreak/RoguePlanet** Defender-driver case: 2026's recurring endpoint-killer pattern is signed-driver reuse, and hash blocklists lose the race by design. The capability-vs-incident discipline in this report is also worth copying: the driver's un-configured routines (hiding, injection, rerouting) are documented as dormant, not claimed as executed.

## Monitoring

- Whether Microsoft adds the CnCrypt/`CcProtect` lineage to the vulnerable-driver blocklist (the blocklist gap is the story — track the intake outcome, not the file).
- Backfill of the joint LastPass/Delphos report's full IOC list (contract server IPs/domains, the 40 impersonated brands) and any named-victim or infection-count disclosure.
- Whether the `vsdbg` side-load + padded-ZIP + fake-GitHub-org pattern is reused for other brands (the same family is already documented in ~300 repos per Arctic Wolf).
- Cruciferra crypter takedown/rotation (the 145-name kill list is the crypter's, so crypter-side changes move the whole family's behavior).
- Whether the dormant driver routines (file hiding / injection / traffic rerouting) ever ship with a config file — that would upgrade the family from stealer-enabler to full interceptor.

## Sources

- The Hacker News (Swati Khandelwal), "Fake LastPass Authenticator Installer Abuses Microsoft-Signed Driver to Kill Antivirus and EDR," Sep 21, 2026: <https://thehackernews.com/2026/09/fake-lastpass-authenticator-installer.html> (full text captured by this wiki Sep 22, 2026; attributes LastPass + Delphos Labs, disclosure Sep 17, 2026).
- Delphos Labs site live at capture (canonical joint report URL not yet retrievable — SPA front-end; backfill pending).
- LOLDrivers entry for the `CcProtect.sys` / CnCrypt lineage (referenced by researchers; community detection is hash-matched).

## Related pages

- [GodDamn ransomware PoisonX signed-driver BYOVD](../ops/goddamn-ransomware-poisonx-byovd.md) — same signed-driver-reuse failure mode, ransomware context
- [Spark RAT Cambodia ardrv.sys BYOVD](spark-rat-cambodia-ardrv-sys-byovd-multi-stage.md) — BYOVD to terminate security products, same kill-from-below design
- [RatHat Android ADB self-pairing spyware](rathat-android-adb-self-pairing-genai-driven-spyware-zimperium-september-2026.md) — the mobile mirror: walking through a platform's own trust service instead of breaking it
