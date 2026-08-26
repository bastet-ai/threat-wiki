# SLEEPWALKER: passive raw-packet backdoor with its own bytecode command language

## Summary
**SLEEPWALKER** is a newly disclosed **passive backdoor** for Windows, covered by The Hacker News on **August 26, 2026** (report by Swati Khandelwal). The implant is an **unsigned 64-bit Windows DLL (59,904 bytes)** that is **side-loaded into `ERAAgent.exe`**, the ESET Management Agent, where it impersonates `dpapi.dll` — exposing the same 7 exports and carrying version-resource data copied from ESET. What makes it notable: **it contains no domains, IPs, or URLs and makes no outbound connections.** Instead it sits inert, waiting for a **single crafted packet** that carries commands encoded as **bytecode in a proprietary 23-instruction language**. The research blog that first published the analysis was not reachable at scan time (primary URL returning 404), so this page is based on The Hacker News's report.

## Tags
- tools
- backdoor
- passive backdoor
- SLEEPWALKER
- raw packet
- packet injection
- magic packet
- BPFDoor
- Red Menshen
- bytecode
- custom instruction set
- side-loading
- ERAAgent
- ESET
- dpapi.dll
- DLL side-loading
- VMCI
- NullSessionPipes
- EveryoneIncludesAnonymous
- Named Pipes
- YARA
- in-memory
- no C2
- sleep agent
- red team
- RCE

## How it works
- **Delivery/side-loading:** the DLL is dropped beside `ERAAgent.exe` and loaded as an impersonation of `dpapi.dll` (same 7 exports). Version resource data is copied from ESET to stay consistent with the host process.
- **Passive operation:** with no hard-coded C2 infrastructure, the backdoor has zero outbound traffic to hunt. Activation requires **one crafted inbound packet** — a "magic packet" trigger in the tradition of sleep-agent implants (compare **Red Menshen / BPFDoor**, the Linux raw-BPF sleep implant documented by Rapid7).
- **Command language:** commands arrive as **bytecode in a 23-instruction language** specific to the implant. The active opcode is a raw-packet listener; a second opcode enables an inert **DNS trigger**.
- **No-disk-write property:** no instruction in the language writes to disk, keeping the implant in-memory after activation.
- **VMCI gap:** packet traffic can pass through the **VMCI virtualization layer**, so host-to-guest packet captures may miss the trigger traffic entirely.

## Configuration and state manipulation (Windows)
- Sets the `EveryoneIncludesAnonymous` registry value to **1** and adds its pipe to **`NullSessionPipes`**, enabling anonymous named-pipe access as an auxiliary channel/state.
- **Cleanup bug:** the removal path records whether *its own* write succeeded rather than whether the value pre-existed, so cleanup can delete **legitimate** entries that were not created by the implant.

## IoCs
- Unexpected `dpapi.dll` **beside `ERAAgent.exe`**
- Unexpected `dpapisvc.dll` in the same directory
- SHA-256: `d347170752a28e2b8c4b8b9f3cab2e3a6541ba11682c94498d26eb9002779d60`
- MD5: `2318327b29bb1c0e2d2b5f0211fc7fac`
- `EveryoneIncludesAnonymous` = 1 with an unexpected `NullSessionPipes` entry
- ESET-managed endpoints running ERAAgent.exe with anomalous loaded-module lists

## Detection notes
- The disclosure ships a **YARA rule and a read-only PowerShell scanner**. The YARA rule keys partly on a **static AES key and compiled protocol code** — the authors note this is fragile against recompilation.
- Because there is no C2 beacon, classic network-detection (beaconing, known domains) will not find it; the hunting surface is **file/module placement** (fake `dpapi.dll` next to ESET agents) and the **registry state** above.
- VM-internal deployments are specifically harder: VMCI traffic between host and guest can evade host-side captures.

## Why this matters
- **Zero-infra sleep agents are maturing.** The magic-packet implant class (BPFDoor on Linux, SLEEPWALKER on Windows) removes the highest-value detection signal — outbound C2 — and shifts the detection burden to module-placement and memory/registry state checks.
- **Security-vendor agent binaries as side-load targets** is a recurring pattern: an ESET agent impersonating ESET's own DLL layout defeats naive "signed binary loaded a module" alerts.
- **No public toolkit release found as of August 26, 2026** — this is currently research-grade disclosure, not observed-in-the-wild.

## Related pages
- [CISA AA26-237A "A Tale of Two SOCs" (red-team tradecraft)](../ops/cisa-aa26-237a-tale-of-two-socs-red-team-critical-infrastructure.md)

## Caveats
- The primary research post (`https://r136a1.dev/2026-08-24/sleepwalker-a-passive-backdoor-with-its-own-command-language/`) returned 404 at scan time; all details above are from The Hacker News's coverage.
- Attributions in the source report refer to the researcher by first name only ("Reichel"); no group attribution is asserted here.

## Sources
- The Hacker News (Swati Kandelwal): [Newly discovered SLEEPWALKER backdoor waits for a single crafted packet](https://thehackernews.com/2026/08/newly-sleepwalker-backdoor-waits-for.html) (August 26, 2026)
- Primary research post (404 at scan time): `https://r136a1.dev/2026-08-24/sleepwalker-a-passive-backdoor-with-its-own-command-language/`
