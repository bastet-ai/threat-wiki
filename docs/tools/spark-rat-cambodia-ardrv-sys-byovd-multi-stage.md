# Spark RAT: Cambodia-focused cluster uses a multi-stage Inno/DLL side-load chain and the vulnerable OPSWAT ardrv.sys driver

## Summary
Acronis Threat Research Unit (Darrel Virtusio and Subhajeet Singha) documented a **Cambodia-focused phishing campaign** that delivers the open-source, Go-based cross-platform remote access trojan **Spark RAT** (upstream: [XZB-1248/Spark](https://github.com/XZB-1248/Spark)). The multi-stage chain is notable for a **bring your own vulnerable driver (BYOVD)** technique: it loads the legitimate-but-vulnerable **OPSWAT AppRemover driver `ardrv.sys`** (affected by **CVE-2026-36425**) to escalate privileges and terminate security software. Artifacts were observed between **late June and early August 2026**; Acronis does not know if the campaign remains ongoing. The chain has multiple **Silver Fox-style** indicators (DLL side-loading through a signed binary, Huorong targeting, service + scheduled-task persistence, Defender exclusions), but Acronis states there is **not enough evidence** to attribute the campaign to Silver Fox.

## Tags
- tools
- malware
- Spark RAT
- RAT
- Go
- remote access trojan
- BYOVD
- ardrv.sys
- CVE-2026-36425
- OPSWAT
- AppRemover
- DLL side-loading
- Inno Setup
- signed executable
- Tencent
- PNG shellcode
- vssvc.exe
- ctfmon.exe
- AMSI patch
- ETW
- persistence
- scheduled task
- Windows service
- Huorong
- Qihoo 360
- Cambodia
- phishing
- Silver Fox
- ValleyRAT
- Winos 4.0
- Acronis
- anti-sandbox
- timing check

## Attack chain
1. **Phishing:** targeted emails (Cambodian government notices, public-health announcements, dental examination records, real estate documents, promotional offers) carry compressed archives containing an **Inno Setup** executable.
2. **DLL side-loading:** the Inno Setup installer triggers a DLL side-loading chain using a **signed Tencent executable**, which delivers interim payloads that deploy the vulnerable **`ardrv.sys`** driver.
   - The loader runs a **timing-based anti-sandbox check** (fails if elapsed time falls outside the expected range, indicating a shortened/manipulated sleep environment).
   - It inspects running processes for **Huorong Internet Security** (`HipsTray.exe`) and, if present, attempts to weaken that product's privileges.
3. **Second stager:** shellcode concealed inside a **PNG file** in the archive is decrypted to run a second stager, which verifies it is running with **SYSTEM** privileges and then picks a mode:
   - **Inject mode** (already SYSTEM): skip persistence setup, parse/decrypt shellcode from a *second* PNG and inject into **`vssvc.exe`**; it monitors the `vssvc.exe` instance and re-injects on termination/restart (new PID).
   - **Setup mode** (not SYSTEM): check a hard-coded list of **Qihoo 360** processes; if none found, establish **Windows service-based persistence** (a service that re-sideloads the DLL to relaunch the cycle), then inject into `vssvc.exe` as above.
4. **Post-injection payload:** performs, in sequence:
   - Attempts to patch **AMSI** and **ETW**.
   - Sets up persistence using a **scheduled task**.
   - Installs the **`ardrv.sys`** driver (vulnerable to **CVE-2026-36425**) to terminate security-related processes such as **Microsoft Defender**, **Huorong Internet Security**, and **Tencent PC Manager**.
   - Reads/decrypts another embedded payload from a **third PNG** to perform user-mode termination of hard-coded security processes.
   - Simultaneously processes a **fourth PNG-based payload** to extract/decrypt shellcode injected into **`ctfmon.exe`**, leading to execution of **Spark RAT**.
5. **BYOVD driver roster:** the BYOVD routine references several other drivers, including those from **TrueSight** and the **Zemana Anti-Malware SDK** — both previously used by the **Silver Fox** threat actor before dropping **Winos 4.0 (aka ValleyRAT)**.

## Attribution posture
- **Silver Fox indicators (not conclusive):** targeting overlaps; DLL side-loading through a signed application; multi-stage payload delivery; persistence through Windows services and scheduled tasks; Microsoft Defender exclusions; repeated targeting of **Huorong** security processes (seen in past Silver Fox attacks).
- **Acronis caveat:** "there is not enough" evidence to attribute the campaign to Silver Fox. Treat it as **Silver Fox-style / similar tradecraft**, not confirmed Silver Fox.
- **Spark RAT itself** is open-source and cross-platform; its use here is a tool-choice signal, not an attribution.

## Durable detection pivots
- **Driver + CVE:** alert on **`ardrv.sys`** (OPSWAT AppRemover) being loaded or installed by a non-OPSWAT context, and on termination of Defender/Huorong/Tencent processes via a vulnerable driver (CVE-2026-36425). The BYOVD reference set (TrueSight, Zemana SDK drivers) is a secondary pivot.
- **PNG-hosted shellcode:** multiple PNG files in a dropped archive whose content is decrypted into shellcode; correlate with Inno Setup installers and a signed Tencent host process.
- **Injection targets:** shellcode injection into **`vssvc.exe`** (Volume Shadow Copy) and **`ctfmon.exe`** with AMSI/ETW patching immediately before.
- **Persistence pair:** a new **Windows service** that re-sideloads a DLL plus a **scheduled task** created in the same timeline.
- **Anti-analysis:** timing-based sleep checks that abort outside a real environment; Huorong `HipsTray.exe` process inspection.
- **Geography/lure:** Cambodia-localized lures (government, public health, dental, real estate, promotional) with Inno Setup delivery.

## Defender guidance
- Patch/validate **OPSWAT AppRemover** and other AppRemover-adjacent tooling to close **CVE-2026-36425**; inventory any host where `ardrv.sys` is present and confirm it was installed by legitimate OPSWAT use.
- Hunt for the PNG-shellcode + signed-Tencent-sideload + Inno Setup combination; it is a distinctive delivery signature.
- Treat `vssvc.exe` / `ctfmon.exe` injection with AMSI/ETW patching as high-confidence malicious on endpoints that do not legitimately inject into those processes.
- If Huorong or Qihoo 360 processes appear in a victim's process list during analysis, note the loader's explicit targeting as corroborating context (and check for privilege-weakening attempts against them).

## Confidence and caveats
- Observed artifacts span **late June–early August 2026**; campaign status after that window is **unknown**.
- Silver Fox similarity is **indicators-based, not attribution**; Acronis explicitly withholds a Silver Fox determination.
- Spark RAT is open-source; multiple unrelated actors can reuse it, so treat the tool alone as weak attribution.

## Related pages
- [TA4922 actor (ValleyRAT / Winos 4.0 lineage)](../actors/ta4922.md) (BYOVD driver roster overlap; Silver Fox-style tooling context)
- [BTR Reforged: weaponizing Defender's BTR.sys remediation driver](../ops/microsoft-defender-btr-sys-reforged-btr-cli.md) (signed-driver primitive context)

## Sources
- Acronis TRU: [Cambodia-focused cluster uses multi-stage infection chain with localized lures](https://www.acronis.com/en/tru/posts/cambodia-focused-cluster-uses-multi-stage-infection-chain-with-localized-lures/) — August 2026 (Darrel Virtusio, Subhajeet Singha)
- The Hacker News: [Spark RAT Targets Cambodia, Abuses Vulnerable OPSWAT Driver to Disable Security Tools](https://thehackernews.com/2026/08/spark-rat-targets-cambodia-abuses.html) — August 27, 2026
- Spark RAT upstream: [XZB-1248/Spark](https://github.com/XZB-1248/Spark)
