# Operation Dragon Weave Azure Blob C2 campaign

## Summary
Seqrite describes **Operation Dragon Weave** as a targeted espionage campaign against Czech Republic and Taiwan-linked victims that uses ZIP-delivered lures, DLL sideloading, a Rust loader, and an Adaptix C2-derived payload that abuses Microsoft Azure Blob Storage as dead-drop command and control.

Seqrite assesses the activity with **moderate confidence** as China-linked based on targeting, TTPs, and tooling, but does not map it to a specific named group. Keep that attribution caveated unless a later primary source provides stronger linkage.

## Tags
- ops
- operations
- espionage
- China-linked
- Czech Republic
- Taiwan
- Azure
- cloud C2
- DLL sideloading
- Rust
- Adaptix C2

## Why this matters
- The campaign blends C2 traffic into `blob.core.windows.net`, forcing defenders to distinguish normal Azure Blob Storage use from malware dead-drop patterns.
- The chain offers two execution paths from the same archive: an LNK / VBScript / PowerShell route and a self-contained Rust dropper route.
- RUSTCLOAK and AZUREVEIL combine commodity-adjacent tradecraft with careful evasion: sandbox computer-name checks, multi-layer payload decryption, in-memory PE loading, Windows fiber execution, and runtime API hashing.

## Reported chain
- Initial delivery: a ZIP archive submitted from Taiwan on March 26, 2026, containing a `data` folder, a Chinese-named `.pdf.lnk` shortcut, and a Rust executable masquerading as a document.
- Lure content:
  - a Chinese WPS Cloud documentation artifact that Seqrite suspects may have been a leftover from a different campaign;
  - a Czech Social Security Administration-themed appointment / reservation PDF shown to the victim during execution.
- Path A: the `.pdf.lnk` launches `wscript.exe` with `data\empty.vbs`, which starts `Profile.ps1` with execution-policy bypass and a hidden window.
- Path B: the user runs `_計畫申請審查結果通知單.exe`, a Rust dropper that creates `%LOCALAPPDATA%\WebViewFixUtility`, extracts required components, and launches the same later-stage loader path.
- The PowerShell path decrypts `1.dat` with XOR key `P@ssw0rd_am_2026`, producing `RuntimeBroker_update.exe`; it also moves `UnityPlayer.dll` and `Com.dat` into `%TEMP%`.
- `RuntimeBroker_update.exe` sideloads the malicious `UnityPlayer.dll`, which Seqrite names **RUSTCLOAK**.

## RUSTCLOAK loader details
- RUSTCLOAK is a Rust-based DLL loader.
- Seqrite observed a plaintext Rust build path in the binary: `C:\Users\dell2\.cargo\registry\src\index.crates.io-1949cf8c6b5b557f\src\decrypt_SM4.rs`, exposing the developer username `dell2` and Rust crate details including `libsm-0.5.1` and `base64-0.21.7`.
- Before payload execution, it checks the host computer name against more than 100 hardcoded sandbox / analyst names and exits on a match.
- It reads encrypted `Com.dat` and unwraps it through:
  - a custom RC4 layer using key `F8 83 40 17 1D 66 AA C2 B0 25 A8 6C A0 DD C4 5A`;
  - Base64 decoding;
  - SM4-CBC decryption using key `CD CE 4F DB 3E 6A F2 44 AC 62 8C F4 96 1F 6B FB` and IV `FA 70 B1 81 A0 BA 5D 46 7A 5D 40 DD 99 B6 9B 42`.
- The loader allocates memory, writes the decrypted PE payload, changes permissions with `VirtualProtect`, and transfers execution through Windows fibers (`CreateFiberEx` / `SwitchToFiber`) rather than a normal new-thread pattern.

## AZUREVEIL payload details
- Seqrite names the final payload **AZUREVEIL** and describes it as a 64-bit MinGW C++ DLL / Adaptix C2 agent.
- AZUREVEIL resolves roughly 87 Windows APIs at runtime using djb2-style hashing across libraries such as `wininet.dll`, `Ws2_32.dll`, `Advapi32.dll`, `Iphlpapi.dll`, and `msvcrt.dll`.
- Its reported Azure Blob Storage endpoint is `note1ggbbhggdwa1[.]blob[.]core[.]windows[.]net`.
- The agent uses Azure Blob Storage as a dead-drop channel:
  - the implant uploads small encrypted beacons;
  - the operator places encrypted commands in the same container;
  - the implant retrieves commands, executes them, and uploads encrypted results.
- Seqrite reported blob object naming in the form `{agent_id}/{timestamp1}_{timestamp2}.bin`.
- A hardcoded SAS token was valid from March 19, 2026 to March 19, 2027 and included broad blob permissions, suggesting the operator planned long-lived infrastructure use.
- Seqrite identified 36 supported commands, including directory and logical-drive listing, network-adapter enumeration, and execution of Beacon Object Files (BOFs) with output captured through a named pipe and returned through Azure Blob Storage.

## Defender notes
- Hunt endpoints for the reported file names and paths: `empty.vbs`, `Profile.ps1`, `1.dat`, `Com.dat`, `RuntimeBroker_update.exe`, `UnityPlayer.dll`, `%LOCALAPPDATA%\WebViewFixUtility`, and `%TEMP%` staging of these components.
- Treat unexpected Azure Blob Storage access to `note1ggbbhggdwa1[.]blob[.]core[.]windows[.]net` as high priority; where possible, profile blob traffic by container/object naming and SAS-token use, not only by domain.
- Review Windows telemetry for DLL sideloading around `RuntimeBroker_update.exe` and local `UnityPlayer.dll` placement.
- Look for hidden PowerShell launched by `wscript.exe` after `.lnk` execution, especially execution-policy bypass paired with archive-extracted script paths.
- Add detections for RUSTCLOAK traits: sandbox-name comparison, SM4 / RC4 / Base64 chained decryption, `VirtualAlloc` / `VirtualProtect`, and fiber-based execution.
- Because the public attribution is moderate-confidence and not tied to a named group, prioritize behavior and infrastructure hunting over cluster-label matching.

## Related pages
- [Cloud Atlas](../actors/cloud-atlas.md)
- [Ghostwriter / FrostyNeighbor JavaScript PicassoLoader chain](../actors/ghostwriter.md#2026-ukrtelecom-themed-frostyneighbor-campaign)

## Sources
- Seqrite: [https://www.seqrite.com/blog/operation-dragon-weave-uncovering-a-china-linked-campaign-targeting-czech-republic-and-taiwan-using-azure-cloud-c2/](https://www.seqrite.com/blog/operation-dragon-weave-uncovering-a-china-linked-campaign-targeting-czech-republic-and-taiwan-using-azure-cloud-c2/)
- The Hacker News summary: [https://thehackernews.com/2026/06/china-aligned-groups-ramp-up-attacks.html](https://thehackernews.com/2026/06/china-aligned-groups-ramp-up-attacks.html)
