# Armored Likho

## Summary
**Armored Likho** is a Kaspersky-tracked APT cluster, also known as **Eagle Werewolf** based on circumstantial evidence. Kaspersky's July 2026 reporting describes the group as active against government agencies and the electric power sector in Russia, Kazakhstan, and Brazil, while also blending targeted espionage with financially motivated activity against private individuals.

## Tags
- actors
- APT
- cyber-espionage
- infostealer
- RAT
- spear phishing
- government targeting
- electric power sector
- Russia
- Kazakhstan
- Brazil
- Armored Likho
- Eagle Werewolf
- BusySnake Stealer
- AquilaRAT
- Go2Tunnel

## Public reporting snapshot
Kaspersky reports that Armored Likho uses spear-phishing archives with government, social-program, humanitarian-aid, debt-clearance, and psychological-test themes. The group has used EXE and LNK first stages, AI-looking loader code, Python-based stealers, modular RAT-style tasking, and reverse SSH tunneling.

Kaspersky assesses the July 2026 BusySnake activity as Armored Likho with **medium confidence**, based on tool and network overlaps rather than a single conclusive artifact.

In **May 2026**, Kaspersky GReAT documented a new espionage campaign against private individuals and organizations in Russia (major corporations, public sector, IT, and education). Initial access used a dropper app mimicking a donation service (built in Rust on the Tauri framework, with a fake login form and a catalog of "donatable items" pulled from `orderapiserver[.]info`); the dropper decrypts and launches the next stage in the background. The campaign introduced the **Still Toolkit**, a new Rust cyber-espionage suite:
- **Still Sync** — an asynchronous (Tokio-based) Rust stealer that steals **Telegram session data** (`tdata`), then uses the stolen session against the Telegram API to pull chat logs, media files, and other account data on demand. It speaks gRPC over FlatBuffers with HTTP or HTTPS to its C2 (default `https://tg4service[.]com:443`), with configuration read from `STILL_SYNC_ADDR`, `STILL_SEND_PATH`, and `STILL_TELEGRAM_PASSCODE` environment variables.
- **Still Audio** — a covert audio-surveillance implant that analyzes the incoming audio stream, detects speech automatically, records conversations, and uploads the recordings to C2.

Kaspersky detects the campaign components as `Trojan.Win64.Agent.*` and `HEUR:Backdoor.Win32.Generic`.

## Tooling and infrastructure
- **[BusySnake Stealer](../tools/busysnake-stealer.md)** — Python / PyArmor Windows infostealer with browser credential theft, cookie theft, screenshot and clipboard collection, document exfiltration, task polling, and built-in reverse SSH tunneling.
- **AquilaRAT** — earlier / staple Armored Likho RAT tooling; Kaspersky notes architectural overlap with BusySnake's handler-based task execution and C2 status-update design.
- **Go2Tunnel** — prior standalone reverse SSH tunneling tool; BusySnake implements similar tunnel establishment directly inside the stealer.
- **Still Toolkit (Still Sync / Still Audio)** — May 2026 Rust espionage suite: Telegram session stealer (Still Sync, gRPC/FlatBuffers, default C2 `tg4service[.]com`) and speech-detecting audio eavesdropper (Still Audio). See [Armored Likho Still Toolkit campaign](../ops/armored-likho-still-toolkit-russia-campaign.md).

## Defensive pivots
- Treat spear-phishing attachments that launch `rundll32.exe` and then PowerShell as high-risk initial access, especially when followed by Python runtime staging.
- Hunt for `%APPDATA%\\WindowsHelper`, `module.pyw`, `run.vbs`, `wh_selfdelete.vbs`, and scheduled tasks masquerading as Windows helper / update utilities.
- Correlate browser credential extraction, cookie database access, screenshot archives, reverse SSH processes, and outbound traffic to Armored Likho C2 domains.
- Because Kaspersky says first-stage code style strongly suggests LLM-generated loaders, do not rely only on stable loader syntax for clustering.
- Still Toolkit: look for Rust/Tauri donation-service lookalike apps, `orderapiserver[.]info` catalog traffic, Telegram `tdata` access, and `tg4service[.]com` (or the `STILL_SYNC_ADDR` override) C2 traffic; treat unexpected service installations of audio-capture components as a Still Audio indicator.

## Related pages
- [Armored Likho BusySnake campaign](../ops/armored-likho-busysnake-campaign.md)
- [Armored Likho Still Toolkit campaign](../ops/armored-likho-still-toolkit-russia-campaign.md)
- [BusySnake Stealer](../tools/busysnake-stealer.md)

## Sources
- Kaspersky Securelist: [https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/](https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/)
- Kaspersky GReAT: [Armored Likho expands its cyber-espionage toolkit](https://securelist.com/armored-likho-still-toolkit/121033/) — August 13, 2026
