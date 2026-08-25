# Operation QUICSILVER: VHD-delivered Go backdoor targets Myanmar diplomats

## Summary
Seqrite Labs (coverage via The Hacker News, August 24, 2026; original analysis August 17, 2026) documented **Operation QUICSILVER**, an espionage campaign attributed with moderate confidence to a **China-nexus actor** targeting Myanmar government and IT interests — specifically entities tied to the **ITCSD (Information Technology Centre for Sustainable Development) under Myanmar's Ministry of Transport and Communications** — first observed around **April 2026**. The campaign delivers a new Go-based backdoor, **QUICAgent**, through double-extension LNK files that point at VHD containers, and communicates over **QUIC (UDP/443)** to infrastructure behind Cloudflare Workers discovery domains.

## Tags
- ops
- operations
- espionage
- QUICSILVER
- QUICAgent
- Seqrite
- Seqrite Labs
- China nexus
- Myanmar
- ITCSD
- Ministry of Transport and Communications
- VHD
- LNK
- Go backdoor
- QUIC
- Cloudflare Workers
- ftp.exe
- LOLBAS
- sandbox evasion
- LNK Startup persistence
- fake graduation invite
- holiday calendar lure

## Campaign chain
- **Lure:** early deliveries used `HolidayNotice.pdf.exe` alongside a fake Belgian–Myanmar holiday calendar; from June/July 2026 the actor shifted to **VHD files containing LNK decoys** — notably a Burmese-language fake graduation invitation attributed to the ITCSD.
- **Execution:** the LNK launches `ftp.exe -s` with a script file (**LOLBAS**). The script reconstructs the payload by binary-copying hidden OOXML parts — `_rels/header.doc` and `body.doc` — via `copy /b` into the final executable.
- **Payload:** the rebuilt implant is the Go-based **QUICAgent** backdoor.
- **Sandbox evasion:** the implant applies a randomized 100–600 ms delay at startup and burns CPU with ~1000× SHA-256 computations before beaconing.
- **C2:** discovery domains resolve to **Cloudflare Workers**; beaconing goes to `104.64.211[.]22` on **port 443 over QUIC/UDP**, with a ~5 second beacon interval and a unique `X-Agent-ID` per host. The observed command set comprises five commands.
- **Persistence:** an LNK placed in the Startup folder re-executes the chain at logon.

## Assessment limits
- Attribution to a China-nexus actor is **moderate confidence** per Seqrite; Myanmar government/IT targeting is based on lure content (ITCSD branding, Burmese-language materials), not victim confirmation beyond the reported set.
- No public KEV listing, vendor advisory, or law-enforcement confirmation exists as of the August 24, 2026 writeup.
- The campaign first observed April 2026; the published writeup describes activity through early August 2026, so earlier lures and infrastructure may differ.

## Defender heuristics
1. **Treat double-extension LNK files as hostile by default**, especially ones referencing `.vhd`, `.vhdx`, or Office document names; the `LNK → VHD` hop with `ftp.exe -s` script execution is the durable IOC shape for this campaign.
2. **Hunt the reassembly pattern**: `copy /b` of `_rels/header.doc` + `body.doc` inside an OOXML container producing an executable, and any `ftp.exe` spawning with `-s` script arguments (LOLBAS).
3. **Watch for QUIC/UDP C2**: outbound UDP 443 beacons with short intervals and a stable per-host header are not typical of normal client traffic; the `104.64.211[.]22` endpoint and Cloudflare-Workers-fronted discovery domains are the current infrastructure.
4. **Review LNK Startup persistence** on hosts that opened any Myanmar-government-themed document, and check for the startup delay + repeated SHA-256 burn pattern (sandbox-evasion artifact) in process telemetry.
5. **Sector relevance:** Myanmar diplomatic, government, and IT-adjacent organizations and their regional correspondents should treat Burmese-language invitation/graduation/holiday-themed attachments as presumed malicious.

## Related pages
- [Fake TradingView macOS stealer delivered by a paid YouTube ad](fake-tradingview-macos-stealer-malvertising.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)
- [DoFun Android head-unit malware: MoYu/BADBOX ad-fraud and proxy botnet](dofun-android-head-unit-jarservice-moyu-badbox.md)

## Sources
- Seqrite Labs: [Operation QUICSILVER: China-nexus actor targets Myanmar diplomats via VHD-delivered Go backdoor](https://www.seqrite.com/blog/operation-quicsilver-china-nexus-actor-targets-myanmar-diplomats-via-vhd-delivered-go-backdoor/)
- The Hacker News: [Operation QUICSILVER Targets Myanmar](https://thehackernews.com/2026/08/operation-quicsilver-targets-myanmar.html)
