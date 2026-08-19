# SilkParasite

## Summary
**SilkParasite** is a previously unreported cyber-espionage operation observed targeting government bodies in **Central Asia**. Bitdefender Labs assessed the intrusion set to be a **China-nexus threat cluster with medium confidence**. It was first discovered in late 2025. The operation deploys **seven remote-access-tool (RAT) families**, five of which had not been documented before this report: **DriveSilkRAT, CookiETagRAT, NomadRAT, GoginRAT, and NodeEdgeRAT**. The remaining two families build on established Chinese-nexus tooling.

## Tags
- groups
- SilkParasite
- China-nexus
- Central Asia
- espionage
- government targeting
- RAT
- DriveSilkRAT
- CookiETagRAT
- NomadRAT
- GoginRAT
- NodeEdgeRAT
- BLOODALCHEMY
- Deed
- ShadowPad
- PlugX
- SpiceRAT
- DLL sideloading
- plugin architecture
- AI-assisted development
- spear phishing
- macro
- Kaspersky detection bypass
- .NET
- C++
- Go
- JavaScript

## Why this matters
- SilkParasite is the **third prominent threat actor to strike Central Asia in recent years**, after UAC-0063 and FamousSparrow — a useful frame for regional defenders who are hunting the same geography with a different toolchain.
- The clearest China-nexus signal is **BLOODALCHEMY**, an updated version of **Deed RAT** (itself a successor to **ShadowPad**, an evolution of **PlugX**). BLOODALCHEMY was first documented by Elastic Security Labs in October 2023 in REF5961 attacks against Southern and Southeast Asian government organizations; its reuse here links the campaign to the same tool lineage widely used by Chinese-speaking actors.
- A second China-nexus indicator is an **updated version of SpiceRAT** (attributed to another Chinese-speaking actor, "SneakyChef") that can download and run executable binaries and arbitrary commands.
- Bitdefender describes the arsenal as **expert, human-developed espionage tooling with traces of AI-assisted development** — "different from AI-generated malware." The clearest AI signature is a phishing lure that is indubitably AI-generated; it is also the only place the adversary appears sloppy, which raises the possibility that the sloppiness was deliberate to confuse attribution.
- Nearly every implant uses a **plugin-oriented architecture** and spans four languages (**.NET, C++, Go, JavaScript**), delivered predominantly through **DLL sideloading** of attacker-supplied signed binaries.

## Public activity profile
- **Initial access:** password-protected RAR archives containing malicious Microsoft Office documents, likely delivered by spear-phishing email; the archive password is supplied in the email body. Opening the document launches a macro that triggers a DLL-sideloading sequence to drop the first-stage payload.
- **Lure tailoring:** recovered documents are crafted to look relevant to government entities in **Uzbekistan, Turkmenistan, Kyrgyzstan, Tajikistan, and Kazakhstan**, several impersonating specific ministries. One additional document, recovered from a public malware-sharing platform, was addressed to a **Georgian** government entity.
- **Detection-evasion tell:** the macro checks whether **Kaspersky antivirus** is installed and running before execution, consistent with the region's prevalence of that product.
- **Malware families (seven total):** five newly documented — DriveSilkRAT (roughly 65 observed instances, mostly in the Asia region), CookiETagRAT, NomadRAT, GoginRAT, NodeEdgeRAT — plus updated BLOODALCHEMY and SpiceRAT.
- **AI-assistance artifacts:** GoginRAT ships Go test functions and a hard-coded AES key set to `0123456789abcdef`; NodeEdgeRAT carries a configuration field for an encryption key set to the literal `change_this_key`; NomadRAT and GoginRAT share a similar architecture that suggests one high-level design implemented in two languages (a pattern consistent with AI-assisted scaling).
- **Tooling characteristics:** the C-based BLOODALCHEMY backdoor is launched by a DLL loader sideloaded via a legitimate binary and supports host-info collection, overwriting the malware binary/loader/trusted binary, and terminate/uninstall commands.

## Defensive priorities
- Treat **DLL sideloading** as the most consistent detection surface: the reliable signal is the *pairing*, not the DLL name alone — a legitimately signed application loading a library placed beside it while running from an unusual location.
- Low-footprint, plugin-based implants operating through legitimate cloud services are poorly served by volume-based detection; prefer **behavioral baselines** that flag unusual process-to-network-service relationships over signatures for any single artifact.
- Hunt for password-protected RAR lures with an in-email password and Office macros that check for a specific AV product (Kaspersky) before running — a strong regional tell for this cluster.
- Baseline and alert on the newly documented RAT family names (DriveSilkRAT, CookiETagRAT, NomadRAT, GoginRAT, NodeEdgeRAT) and the BLOODALCHEMY / Deed / ShadowPad / PlugX lineage artifacts.

## Assessment limits
- China-nexus is a **medium-confidence** assessment by Bitdefender, not a confirmed attribution; the shared tool lineage (BLOODALCHEMY, SpiceRAT) is the primary driver.
- The AI-assisted-development characterization is an analytical observation, not a verified operational fact; Bitdefender explicitly distinguishes AI-assisted expert tooling from fully AI-generated malware.
- No confirmed victims are named; the geographic and ministry-tailored lures define the target set.

## Related pages
- [OctLurk and SilkLurk Central Asia espionage campaign](../ops/octlurk-silklurk-central-asia-espionage.md)
- [PTC Windchill / FlexPLM CVE-2026-12569 exploitation](../ops/ptc-windchill-flexplm-cve-2026-12569-exploitation.md)
- [Clop-linked Windchill JSP web shell (CVE-2026-12569 follow-up)](../ops/ptc-windchill-flexplm-cve-2026-12569-exploitation.md#clop-linked-jsp-web-shell-follow-up)

## Sources
- The Hacker News: [SilkParasite Espionage Campaign Targets Central Asian Governments with Five New RATs](https://thehackernews.com/2026/08/silkparasite-espionage-campaign-targets.html) — August 19, 2026, citing Bitdefender Labs technical report
- Bitdefender Labs (technical report, August 2026)
- Elastic Security Labs, October 2023: first documentation of BLOODALCHEMY in REF5961 activity
