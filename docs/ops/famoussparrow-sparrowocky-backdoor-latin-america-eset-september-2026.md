# FamousSparrow swaps SparrowDoor for SparroWocky — modular C++ backdoor with embedded open-source tradecraft (Mbed TLS / MinHook / COFF loader / SilentMoonwalk), 90% Latin America targeting (ESET, Sep 2026)

## Summary

ESET Research (report shared with The Hacker News ahead of publication, September 17, 2026) documented **SparroWocky**, a previously unreported modular **C++ backdoor** deployed by the China-aligned espionage group **FamousSparrow** (active since at least 2019, assessed to overlap with **Earth Estries** and **Salt Typhoon**) against governmental entities in **Argentina, Ecuador, Guatemala, Honduras, Panama, Peru, Puerto Rico, and Venezuela** since at least **August 2025**. SparroWocky has **replaced SparrowDoor as the group's primary implant**, yet the delivery tradecraft is unchanged: a **DLL sideloading chain** (legitimate executable launches a loader DLL that decrypts and launches the payload). The name comes from early builds containing the **first stanza of Lewis Carroll's "Jabberwocky."** ESET's durable finding is architectural: where FamousSparrow previously ran open-source offensive tools *beside* its backdoor, with SparroWocky it **integrates open-source code directly into the custom implant** — Mbed TLS for the C2 channel, MinHook to hide new-thread start addresses, a COFF loader for in-memory plugins, and a SilentMoonwalk (StackMoonwalk) variant to spoof call stacks originating from its own MinHook routines. **90% of the group's targets in ESET's telemetry are in Latin America** since July 2025; whether that reflects a formal geographic mandate or temporary geopolitical posture is explicitly unclear. Initial-access vector: unknown.

## Tags
- ops
- actor
- nation-state
- China-nexus
- FamousSparrow
- Salt-Typhoon
- Earth-Estries
- SparroWocky
- SparrowDoor
- backdoor
- C++
- DLL-sideloading
- Mbed-TLS
- MinHook
- COFF-loader
- SilentMoonwalk
- Latin-America
- espionage
- ESET

## Why this matters
- **An implant lineage pivot is detection inventory, not just a name change.** Clusters that hunt FamousSparrow via SparrowDoor artifacts must add SparroWocky while keeping the sideloading-chain detection, which the group did **not** change. ESET: "Despite switching to a distant malware family, the underlying techniques remain the same."
- **Bespoke integration of public tooling raises the bar on "open-source tool = attribution signal."** Mbed TLS, MinHook, COFF Loader, and SilentMoonwalk are individually commodity; the finding is that the group now **compiles them into its own codebase** rather than shipping them as separate DLLs — stripping, hook-placement analysis, and call-stack-integrity telemetry do the distinguishing, not file hashes.
- **The Latin America concentration is the geopolitical read.** FamousSparrow was historically tracked on telecom/ISP intrusion paths (Salt Typhoon overlap); 90%-LATAM governmental targeting since July 2025 matches the same regional squeeze Unit 42's CL-CRI clusters and ESET's earlier Earth Estries work describe — multiple China-aligned operators converging on Western-hemisphere government networks.

## Technical detail (as published)
- **Capabilities:** execute arbitrary files; act as a TCP proxy; run commands; collect system info and network-interface IPs; exfiltrate files; periodic screenshots; file operations; self-deletion.
- **Embedded open-source components:**
  - **Mbed TLS** — TLS channel to C2 (`216.238.110[.]120`).
  - **MinHook** — hides the start address of newly created threads from security products.
  - **COFF Loader** — dynamic loading/execution of in-memory plugins as COFF objects.
  - **SilentMoonwalk (or StackMoonwalk) variant** — spoofs call stacks originating from the MinHook routines (the pairing is deliberate: the stack-spoof exists to cover the hook).
- **Execution chain:** legitimate signed-looking executable → loader DLL (sideload) → decrypts and launches main payload. Same as SparrowDoor.
- **Naming artifact:** early iterations embed the first stanza of "Jabberwocky" (Lewis Carroll, c. 1855).
- **Victimology:** governmental entities in Argentina, Ecuador, Guatemala, Honduras, Panama, Peru, Puerto Rico, Venezuela; high-profile entities across the region since July 2025; 90% of group targets in ESET telemetry located in Latin America.
- **Group lineage:** active since at least 2019; "shares some level of overlap" with Earth Estries and Salt Typhoon (ESET's phrasing — correlation framing, not same-operator proof).

## Defender actions
- Inventory the **DLL sideloading shape** on government/enterprise endpoints: unexpected DLL loads adjacent to legitimate vendor binaries, then outbound TLS to low-reputation hosting (`216.238.110[.]120` as of publication; expect rotation).
- Because the implant's stack traces are deliberately sanitized, **hook-detection telemetry matters more than stack-based attribution**: scan for MinHook-style detours in ntdll/kernel32 paths in-process, and treat thread-start-address gaps as suspicious on their own.
- For LATAM government defenders: treat this as a standing-operations update, not a campaign with an end date — the group has held regional focus for 14+ months.

## Caveats
- Initial access vector is **not disclosed**; ESET does not name the delivery mechanism.
- The C2 IP is from ESET's analysis at publication; expect rotation.
- "Overlap" with Salt Typhoon / Earth Estries is ESET's assessed relationship, not a multi-agency attribution; keep the three names separable.
- C2 command set detail beyond the published capability list is not public.

## Related pages
- [Unit 42 CL-CRI-1131 / CL-CRI-1163 LLM-orchestrated LATAM campaigns](unit42-clcri-1131-1163-llm-orchestrated-latam-campaigns-september-2026.md) — the financially motivated LATAM squeeze on the same geography, different operator class
- [SilkParasite page](../actors/silkparasite.md) — cited UAC-0063 / FamousSparrow regional-targeting framing
- [Transparent Tribe Operation RapidRust](transparent-tribe-operation-rapidrust-rustyshade-private-github-c2-usb-propagation-zscaler-september-2026.md) — same month, another state cluster changing implant families while keeping delivery tradecraft

## Sources
- The Hacker News (Serious Business), "China-Aligned FamousSparrow Deploys SparroWocky Backdoor Across Latin America," September 17, 2026 (relay of ESET's technical report by Alexandre Côté Cyr and Romain Dumont): <https://thehackernews.com/2026/09/china-aligned-famoussparrow-deploys.html>
- ESET Research (primary report; linked from THN ahead of/at publication): <https://www.welivesecurity.com/en/eset-research/>
