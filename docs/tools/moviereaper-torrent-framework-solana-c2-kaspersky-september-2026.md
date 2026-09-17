# MovieReaper: a modular Windows trojan framework distributed through a compromised torrent-file repository, with Solana-blockchain C2 rendezvous (Kaspersky GReAT, Sep 17, 2026)

## Summary

Kaspersky GReAT published (September 17, 2026) a previously unknown modular, multi-stage crimeware framework dubbed **MovieReaper**, distributed by trojanizing movie torrents — including the currently popular "The Odyssey" (2026) — through the compromise of **itorrents[.]org**, a widely used **public repository of torrent files**, rather than the torrent trackers themselves. Trackers that draw their torrent archives from itorrents[.]org began inadvertently serving malicious `.torrent` files to all of their users: when a user resolves a magnet link, the compromised archive substitutes a different torrent that delivers the MovieReaper loader. Kaspersky has identified **several hundred victims** — individuals and organizations — across **Russia, Türkiye, Japan, Kenya, Uganda, Colombia, Spain, the Netherlands, Belgium, Germany, Finland, Tanzania, Ghana, Nepal** and other countries, spanning enterprise, government, IT, consulting, retail, transportation, and agriculture sectors. Activity by the same actor dates back to **October 2025**.

The framework's durable design features: a **blockchain-resilient C2 rendezvous** (stage 2 fetches the next-stage C2 address from a data field of a **Solana mainnet account** via the public `api.mainnet.solana.com` RPC, making the second stage resistant to IP/domain takedown), a **four-stage in-memory chain** with only the initial loader touching disk, heavy sandbox-evasion in stage 1 (deliberately **no `LoadLibrary`/`GetProcAddress` calls** — PEB `Ldr` linked-list traversal and manual DLL parsing to resolve functions), a **vectored-exception-handler + debug-break trick** to reach a raw `NtProtectVirtualMemory` syscall, `EtwpCreateEtwThread` for shellcode execution, UAC bypass + persistence masquerading as `C:\ProgramData\Microsoft\Windows\Telemetry\msedge.exe`, and a **final "file manager" implant with 21 operator commands** giving full remote filesystem control (download, upload, list, create, copy, rename, move, delete, chmod, symlink, plus image-preview exfiltration). Stage 2 beacons over **HTTPS with a TLS-pinned certificate**, using **nanopb protobuf** as the message container, and can load arbitrary new **COFF modules** into memory and run their `module_init` — an on-demand extension interface, so the published 21-command implant is a floor, not a ceiling. Strings are encrypted with a custom stream cipher; shellcode parts are fetched over plain HTTP from image-like URL paths (`/cloud/v192.4/ui/sync-status-icons.png` etc.). Kaspersky detects the family as `HEUR:Trojan.Win64.Agent.gen`.

Kaspersky's own disruption read: **stage 1 is the choke point** — first-stage C2 is a single domain (`deadhub[.]org`) and a single fallback IP (`193.23.118[.]155`), so taking that server down stops the chain — while stage 2's Solana-resolved C2 is deliberately built to survive conventional infrastructure takedowns. As of publication **the itorrents[.]org archive remains compromised**. And because the framework is self-contained, modular, and largely in-memory, it can be **reused in later campaigns with minimal rework**.

## Tags
- tools
- malware
- trojan-framework
- modular-malware
- torrent-compromise
- software-supply-chain
- distribution-compromise
- solana
- blockchain-c2
- decentralized-c2
- rpc-rendezvous
- windows
- uac-bypass
- in-memory-execution
- shellcode
- etwthread
- peb-walking
- tls-pinning
- protobuf
- coff-loading
- sandbox-evasion
- kaspersky
- great
- crimeware
- file-manager-backdoor

## Distribution: poisoning the torrent archive, not the trackers

- The actors did **not** compromise torrent trackers. They compromised **itorrents[.]org**, a popular public repository of torrent `.torrent` files that many trackers consume as their archive.
- Consequence: one upstream compromise lets the actor reach users of **multiple trackers without touching any of them**, and each tracker's own reputation launders the malicious torrents.
- Substitution happens at magnet-resolution time: the legitimate archive returns a **different torrent file**, whose payload is an executable disguised as the movie — Kaspersky's example filename is `odyssey (2026) [1080p] [webrip] [5.1].exe`, with the `.exe` extension hidden by filename length. Multiple decoy filenames, **one shared MD5 (`A0B13781EDD7CFDAB13D79AFFF3C83C1`)** across all downloads.
- As of the report's publication date, the archive **remains compromised**.

## Infection chain

### Stage 1 — loader
- Global single-instance mutex with a random-looking string (observed: `Global\fnulSktzSqvVLXHU`, `Global\E4AyDKzvEhe2hgAr`).
- Anti-sandbox battery, with API resolution done by **walking the PEB `Ldr` double-linked list and manually parsing loaded DLL exports** to avoid `LoadLibrary`/`GetProcAddress` telemetry.
- Decodes `deadhub[.]org`; on connection failure falls back to plain HTTP against `193.23.118[.]155`. Fetches shellcode fragments from randomized image-like paths, e.g. `/cloud/v192.4/ui/sync-status-icons.png`, `/cloud/v192.4/onboarding/welcome-bg.jpg`, `/cloud/v192.4/ui/file-preview-placeholder.png`, `/cloud/v192.4/shared/link-banner.jpg`.
- Maps the shellcode RWX via a **vectored exception handler that rewrites its own handler address and trips a debug break**, redirecting control flow into a function issuing a raw `NtProtectVirtualMemory` syscall (locating the `0F 05` sequence inside ntdll), then executes via the undocumented `EtwpCreateEtwThread`.

### Stage 2 — Solana rendezvous + implant core
- Performs an HTTPS RPC `getAccountInfo` call for Solana account **`6pnDGAiHgyPdmckM5Qt1YbanGzrX43WLEU159nRaNLDm`**; the account's data field holds the base64-encoded second-stage C2 address, decrypted with a static XOR key embedded in the shellcode. Attackers write the value through a simple purpose-built Solana program at **`CSiY8bQLBYPdfPWkwipBzH6sijTVQVVsA279JQdvwHtL`**.
- Second-stage C2 observed at **`208.64.33[.]90`** and **`208.94.246[.]53`**; communication is HTTPS with a **TLS-pinned certificate**, messages containerized with **nanopb protobuf**.
- Core command: parse a COFF file, load it in memory, execute its `module_init` — a generic plugin interface the operator can extend server-side.

### Stage 3 — UAC bypass + persistence
- Downloads a UAC-bypass/persistence module, masquerades as **`C:\ProgramData\Microsoft\Windows\Telemetry\msedge.exe`**, and restarts itself with a command-line flag. The beacon carries a flag telling the C2 whether the process is first-run or respawned from the Telemetry folder, so the server serves the persistence module once and the real implant thereafter.

### Stage 4 — final "file manager" implant
- **21 commands**: remote directory listing/enumeration, file download/upload/read, create/copy/rename/move/delete/chmod/symlink, and **preview/thumbnail commands that exfiltrate image previews before full extraction**. Kaspersky suspects additional modules are loaded on demand.
- Recovered modules were compiled **with symbols** (which sped up the reverse engineering) — itself a tell of a low-opsec crimeware operation.

## Victimology
- Several hundred victims; individuals **and organizations** in Russia, Spain, Germany, Finland, Türkiye, Japan, Nepal, Kenya, Tanzania, Uganda, Ghana, Colombia and other European, Asian, and African countries.
- Sectors: enterprise, government, IT, consulting, retail, transportation, agriculture.
- Same actor's activity observed back to **October 2025**; the campaign has iterated (expanded arsenal, harder-to-detect loader) on the same design pattern: stream-cipher strings, HTTP shellcode fragments, multi-technique sandbox evasion.

## Defender notes
- **Distribution integrity extends to torrent archives.** A compromised shared `.torrent` repository is a supply-chain single point of failure for every tracker that mirrors it. Block/monitor magnet-resolved downloads from itorrents[.]org-sourced archives; any torrent whose extracted payload is an executable is the campaign.
- **Filename-with-double-extension + movie name = the user-facing tell**; the shared-hash MD5 set below is the detection-grade tell across decoy names.
- **Executables running from `C:\ProgramData\Microsoft\Windows\Telemetry\` masquerading as `msedge.exe`** is the persistence tell.
- **Network hunt:** Solana mainnet RPC `getAccountInfo` calls from non-crypto desktop processes, especially paired with image-path HTTP GETs on non-standard hosts; first-stage `deadhub[.]org` / `193.23.118[.]155`; second-stage `208.64.33[.]90` / `208.94.246[.]53`.
- **Blockchain-C2 visibility:** the C2 address can be rotated by the attacker with a Solana transaction, but the **account and program addresses are durable identifiers** — monitor `6pnDGAiHgyPdmckM5Qt1YbanGzrX43WLEU159nRaNLDm` and `CSiY8bQLBYPdfPWkwipBzH6sijTVQVVsA279JQdvwHtL` on-chain for rotation events; blocking RPC egress breaks the rendezvous but also flags the egress pattern.
- **Disruption priority (Kaspersky's):** stage 1's single-domain/single-IP dependence is the takedown target; stage 2 is built to outlive IP blocklisting.

## Indicators of compromise
- File hashes (MD5, per Kaspersky): `4334BBAEA8DE33BF9D45E9B4E4E3BC2`, `4843F9FAFCAE492F11E2D4D33DBB4CDD`, `5310CABAE3FBE6DB8742849B588093F9`, `A0B13781EDD7CFDAB13D79AFFF3C83C1`, `70060341CAF3338697A7DDFE0FB62875`, `AD4643EEA15AC286FA47D1131F9EF756`, `D0B967571AC8A3863C7F324BF5BDE99C`, `D88D550D0FB8E60CFFFF3EA61FF7A067`
- File path: `%ProgramData%\Microsoft\Windows\Telemetry\msedge.exe`
- Mutexes: `Global\E4AyDKzvEhe2hgAr`, `Global\fnulSktzSqvVLXHU`
- Domains/IPs: `itorrents[.]org` (compromised distribution archive), first-stage C2 `deadhub[.]org` + `193.23.118[.]155`, second-stage C2 `208.64.33[.]90`, `208.94.246[.]53`
- Solana identifiers: account `6pnDGAiHgyPdmckM5Qt1YbanGzrX43WLEU159nRaNLDm`, program `CSiY8bQLBYPdfPWkwipBzH6sijTVQVVsA279JQdvwHtL`
- Detection name: `HEUR:Trojan.Win64.Agent.gen`

## Related pages
- [KREMLIN / REF9334 — Ethereum smart-contract dead-drop C2 (Elastic)](../ops/kremlin-ref9334-chrome-integrity-forgery-ethereum-c2-brazilian-banking-malware-elastic-september-2026.md) — same blockchain-as-C2-rendezvous pattern on a different chain and crime class
- [GoCaracal — Ethereum smart-contract C2 fallback](gocaracal-dark-caracal-ethereum-smart-contract-c2-fallback.md) — espionage-side precedent for RPC-resolved C2 adoption
- [Unit 42 Aeternum — blockchain C2 contract analysis](aeternum.md) — Polygon-based contract-resolved C2 precedent

## Sources
- Kaspersky GReAT, "The Odyssey and trojans again: MovieReaper attacks users in multiple countries via compromised torrents" (Sep 17, 2026): [https://securelist.com/moviereaper-malware-torrent-odyssey-solana/121344/](https://securelist.com/moviereaper-malware-torrent-odyssey-solana/121344/)
