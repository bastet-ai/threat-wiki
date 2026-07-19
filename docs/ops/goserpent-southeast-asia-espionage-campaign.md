# GoSerpent Southeast Asia espionage campaign

## Summary
Kaspersky GReAT reported a long-running espionage operation against government and diplomatic organizations in Southeast Asia centered on **GoSerpent**, a Go remote-access and proxy backdoor used since at least 2021. Activity observed from late 2025 through May 2026 combined persistent access, credential dumping, delayed document collection, chained proxying, and a purpose-built network-share exfiltration path.

The actor returned after several weeks with an evolved toolset built around Stowaway and the TmcLoader/TmcPayload pair. Kaspersky found a possible relationship with **TetrisPhantom** based on targeting and operational similarities, but says attribution remains uncertain.

## Tags
- ops
- operations
- GoSerpent
- McMx
- ThumbcacheService
- Stowaway
- TmcLoader
- TmcPayload
- Go malware
- remote access trojan
- SOCKS5
- proxy
- reverse tunneling
- credential dumping
- Mimikatz
- document collection
- network-share exfiltration
- data theft
- espionage
- Southeast Asia
- government targeting
- diplomatic targeting
- TetrisPhantom
- low-confidence attribution
- Kaspersky GReAT

## Toolchain and sequencing
### Initial phase
- **GoSerpent** receives encrypted, Base64-encoded C2 arguments, decrypts them with AES-CBC, and protects C2 traffic with ChaCha20. It provides a shell, file upload/download, listening and outbound connections, port forwarding, and SOCKS5 proxying.
- **McMx** is a simpler related Go RAT/proxy that receives plaintext C2 parameters from configuration files but retains the same core proxy, forwarding, shell, and transfer functions.
- **ThumbcacheService** runs as a Windows service and collects `.doc`, `.docx`, `.pdf`, `.xls`, and `.xlsx` files, including matching files in `$Recycle.Bin`. It archives them with 7-Zip under a 20 MB limit and stores the staged collection as `C:\Users\Public\thumbcache_605a.db`.
- Mimikatz and QuarksDumpLocalHash collect credentials and local password hashes that can later authorize access to network shares.

### Delayed exfiltration phase
In May 2026, after allowing collection to continue for weeks, the actor deployed a customized **Stowaway** agent for SOCKS5, port forwarding, reverse and SSH tunneling, shell access, and file transfer over TCP, HTTP, or WebSocket.

Stowaway delivered **TmcLoader**, an obfuscated Windows-service loader that decrypts **TmcPayload** into `svchost.exe`, plus `{BBF061R2-BE25-4F6D-8B2D-1A6A39C3FSA2}.db`. That configuration contains network-share credentials and destination paths. TmcPayload reads it and transfers the exact `thumbcache_605a.db` archive created by ThumbcacheService. This collection-to-credential-to-share sequence is the campaign's most durable behavioral signature.

## Detection pivots
- `C:\Users\Public\thumbcache_605a.db` or repeated collection of office documents and recycled files followed by password-protected 7-Zip archive creation.
- `{BBF061R2-BE25-4F6D-8B2D-1A6A39C3FSA2}.db` under `C:\Users\Public\Libraries`, especially when read by a service-hosted in-memory payload.
- Go binaries masquerading as `lass.exe` or `updates.exe` and combining shell, file-transfer, SOCKS5, and port-forwarding behavior.
- Mimikatz or SAM-hash dumping followed days or weeks later by access to network shares and transfer of `thumbcache_605a.db`.
- New Windows services that inject or map decrypted code into `svchost.exe`; Stowaway-like TCP, HTTP, WebSocket, or SSH tunnel chains across multiple internal hosts.
- Public C2 pivots: `152.32.160[.]239`, `8.220.194[.]108`, `8.220.214[.]132`, `8.220.209[.]155`, `8.220.193[.]189`, `101.36.104[.]87`, `144.48.6[.]46`, `103.138.13[.]30`, `47.80.22[.]58`, `152.32.222[.]113`, and `43.106.30[.]226`.

Kaspersky published file hashes for GoSerpent, McMx, ThumbcacheService, Stowaway, and TmcLoader in the primary report. Infrastructure hosted at Alibaba Cloud or UCLOUD HK should be evaluated with host and protocol evidence rather than blocked by provider range.

## Defender guidance
- Hunt retrospectively to late 2025. The operation deliberately separates collection and exfiltration by weeks, so a short telemetry window can hide the full chain.
- Correlate service creation, Go RAT/proxy execution, LSASS/SAM access, 7-Zip document staging, and later network-share authentication. Preserve staged databases and configuration files because they establish intended collection and destination paths.
- Isolate affected systems and invalidate compromised domain/local credentials before reconnecting network shares. Review the same credentials across VPN, remote administration, and adjacent diplomatic or government environments.
- Detect chained proxy behavior and internal tunnel creation, not just public C2 IPs. Restrict service accounts and endpoints from arbitrary SMB destinations and unnecessary outbound SSH/WebSocket access.
- Treat the TetrisPhantom link as an analytic lead only; do not merge actor identities without stronger public evidence.

## Related pages
- [CL-STA-1062 Southeast Asia government and energy intrusions](cl-sta-1062-southeast-asia-tinyrct.md)
- [Operation GriefLure Southeast Asia LNK dropper](operation-grieflure-southeast-asia-lnk-dropper.md)
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)

## Sources
- Kaspersky Securelist: <https://securelist.com/goserpent-backdoor-in-southeast-asia/120687/>
