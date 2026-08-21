# RedC2 4.0 (RedShell Linux beacon) and the trojanized-npm delivery wave

## Summary
**RedC2** is a cross-platform, multi-OS command-and-control framework marketed on cybercrime forums and sold through a clearnet site branded **Red Offsec** ($99.99). Version **4.0** adds the **RedShell** Linux beacon and, per Trend Micro's enterprise unit TrendAI (report published the week of August 21, 2026), is being distributed in the wild through **14 trojanized npm packages** masquerading as working calendar/streak "math" utilities. What distinguishes this wave: no install hook is required — a single `import` anywhere in the dependency graph, including a transitive one, executes the payload, because the package entry file (`dist/index.mjs`) is itself a trojan loader that re-exports legitimate date helpers and launches the bundled implant as a detached background process at module load.

RedC2 4.0 also ships **Red Agent**, an LLM-backed command-execution layer that translates natural-language post-exploitation intent (network reconnaissance, credential dumping) into framework beacon commands, plus a **RedC2 EXT** command-line extension. The vendor markets Red Agent as an "AI-powered command execution system specialized for penetration testing."

## Tags
- tools
- malware
- C2
- RedC2
- RedC2 4.0
- RedShell
- Red Agent
- Red Offsec
- MarlboroMan
- npm
- trojanized npm
- supply chain
- Linux backdoor
- AI-assisted C2
- LLM command execution
- in-memory ELF execution
- SOCKS5 proxy
- BOF
- credential theft
- UAC bypass
- TrendAI
- import-time execution
- no-install-hook delivery

## The framework
- **Lineage.** RedC2 2.0 released August 2025; version 3.0 was sold in January 2026; version 4.0 was advertised by the actor "MarlboroMan" on Hack Forums in early June 2026 and is described as "built for evasion." Active development for at least a year; sold for $99.99 on Red Offsec, whose terms prohibit unauthorized access — i.e., a dual-use/red-team-branded C2 sold commercially.
- **Capabilities (Windows/macOS/Linux beacons).** Terminal access, file transfer, staged payload delivery, data collection, multi-beacon operation, network visualization, host-to-host tunneling, and in-memory execution of Beacon Object Files (BOFs), .NET assemblies, and shellcode.
- **RedShell (Linux, new in 4.0).** Provides an interactive `/bin/sh` shell and Linux-specific commands: system discovery, file operations, data collection (SSH keys, browser credentials), execution, persistence, in-memory ELF execution, SOCKS5 proxying, and network pivoting. It registers with the C2 server with a "check-in message" carrying basic system information, then enters a command-processing loop executing incoming instructions via `/bin/sh` and returning results.
- **Windows beacon extras.** UAC bypass, antivirus/EDR tampering, in-memory execution, and lateral movement (not in the macOS build).
- **Red Agent (AI layer).** An LLM-backed command-execution layer that turns natural-language intent into framework beacon commands. TrendAI flags this as a lowering-of-barrier trend: operators of varying skill levels can execute multi-stage intrusions through natural-language prompts against a model tuned for red-team operations.
- **C2 servers.** Remote Windows or Linux servers; the delivery framing in the npm wave wraps the implant as a "native math accelerator" binary (`math-core.bin`, `math-calc.bin`, `calc-math.dat`, `calc-cache.bin`, `calc.bin`, `calc-mapping.bin`) located in `dist/` or `dist/internal/`.

## The 14 trojanized npm packages
Identified by TrendAI (researcher Aliakbar Zahravi), all version `1.0.0`/`1.0.1`:

- `streak-metrics-math@1.0.0, 1.0.1`
- `kit-map-vim@1.0.0`
- `streak-map-cache@1.0.0`
- `streak-map-kit@1.0.0`
- `map-streak-kit@1.0.0`
- `streak-cache-map@1.0.0`
- `streak-calc-metrics@1.0.0`
- `streak-calc-math@1.0.0`
- `streak-math-abz@1.0.0`
- `streak-metricsaz@1.0.0`
- `streak-math-metrics@1.0.0`
- `streak-metricazbd@1.0.0`
- `streak-metricsazb@1.0.0`
- `streak-kit-map@1.0.0`

The naming pattern (rearranged fragments of "streak", "map", "math", "metrics", plus random suffixes) is consistent with generated typosquat/squatted names targeting streak-tracking and date-math helper packages.

## Delivery mechanics (the high-signal part)
- **No install hook required.** The malicious execution rides on module load, not `preinstall`/`postinstall`. Any project that imports one of these packages — directly or transitively — executes the payload on import.
- **Entry file is the trojan loader.** `dist/index.mjs` re-exports the (genuine) date helpers and, on load, locates the bundled binary, marks it executable, and launches it as a detached background process.
- **Implant disguise.** The Linux backdoor is presented as a native math-accelerator binary; the filename varies per package but the content is the RedShell beacon.
- This is a repeat pattern for npm supply-chain delivery (see the keyv preinstall/IDE-hook compromise and the arrayref / proc-macro1 Rust build-time attack) with a variant: **open-time/import-time execution instead of install-time**.

## Defender priorities
1. **Block or audit these 14 packages by exact name@version** in registry proxies, lockfiles, and CI. Hunt for the binary filenames (`math-core.bin`, `math-calc.bin`, `calc-math.dat`, `calc-cache.bin`, `calc.bin`, `calc-mapping.bin`) in `dist/` and `dist/internal/` of installed dependencies.
2. **Alert on import-time execution.** The threat model is any `import`/`require` of the squatted module, not only install scripts. File-system watches for new native binaries appearing under `node_modules/*/dist/` on developer machines and build agents are the primary control.
3. **Hunt for RedShell beacon behavior on Linux:** `/bin/sh`-backed interactive command loops from unexpected processes, SSH-key and browser-credential collection, in-memory ELF execution, SOCKS5 proxying, and host-to-host tunneling from build/dev hosts.
4. **Treat AI-assisted C2 as a tradecraft shift, not a capability shift.** Red Agent lowers operator skill requirements; the underlying beacon capabilities (BOFs, shellcode, UAC bypass, AV tampering, lateral movement) are the same primitives detection should already cover. Expect more low-skill, high-volume use of AI-orchestrated post-exploitation.
5. **Track the vendor.** Red Offsec ($99.99, ToS-gated) and the "MarlboroMan" forum persona are the durable public identifiers; version numbering (2.0 Aug 2025 → 3.0 Jan 2026 → 4.0 Jun 2026) provides a versioning timeline for future beacon changes.

## Assessment limits
- TrendAI/Trend Micro analysis of the 14 npm packages and RedC2 4.0 mechanics; secondary coverage via The Hacker News (August 21, 2026). No confirmed victim count is published; the 14 packages are the identified set, not necessarily the full set.
- No victim attribution, actor attribution, or KEV linkage is asserted for this wave.
- Red Agent behavior in the wild (beyond framework documentation and vendor marketing) is not documented; treat the AI layer as product capability, not observed use.

## Related pages
- [Rust supply-chain attack: arrayref 0.3.10 and the proc-macro1 typosquat](../ops/arrayref-proc-macro1-rust-crate-supply-chain-attack.md)
- [Microsoft Defender CVE-2026-50656 RoguePlanet / ShieldBreak patch bypass](../ops/microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md)
- [CISA KEV August 21: Zimbra SNMP and Microsoft Entra ID](../ops/cisa-kev-microsoft-entra-zimbra-august-21-2026.md)

## Sources
- TrendAI (Trend Micro): [RedC2 AI-Powered Linux Implant](https://www.trendaisecurity.com/en-us/resources-insights/trendai-security-blog/redc2-ai-powered-linux-implant) — report published the week of August 21, 2026
- The Hacker News: [14 Trojanized npm Packages Drop RedC2 4.0 Linux Backdoor With AI-Assisted C2](https://thehackernews.com/2026/08/14-trojanized-npm-packages-drop-redc2.html) — August 21, 2026
