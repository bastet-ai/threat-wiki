# Armored Likho Still Toolkit: Telegram session theft and audio eavesdropping in Russia

## Summary
Kaspersky GReAT reported on **August 13, 2026** a **May 2026 cyber-espionage campaign by the Armored Likho group** (also known as **Eagle Werewolf**) against private individuals and organizations across Russian industries — major corporations, the public sector, IT, and education. The initial access used a fake donation-service app as bait; the headline finding is a new Rust-based espionage suite, the **Still Toolkit**, made up of **Still Sync** (Telegram session-data theft plus on-demand API-based data pull) and **Still Audio** (speech-detecting covert audio surveillance).

## Tags
- ops
- operations
- Armored Likho
- Eagle Werewolf
- Still Toolkit
- Still Sync
- Still Audio
- Telegram session theft
- tdata
- Rust malware
- Tauri
- gRPC
- FlatBuffers
- audio surveillance
- Russia
- cyber-espionage
- Kaspersky

## Initial infection
The chain starts with an app that mimics a donation service (distribution method unknown as of the report; Kaspersky obtained samples posing as apps from different Russian foundations). The app is a dropper written in **Rust on the Tauri framework** with a graphical interface:
- It shows a login form asking for a password supplied by the attackers.
- After a valid password, it displays a catalog of "donatable items" and categories, pulled from `orderapiserver[.]info` through the `public/categories` and `public/products` endpoints — enough of a facade to look legitimate.
- While the user browses, the dropper quietly decrypts and launches the next-stage payload in the background.

Kaspersky says the decrypt-and-launch mechanism has not changed since the February 2026 campaign, and the campaign broadly overlaps the November 2024 and February 2026 Armored Likho campaigns (Starlink-activation and fundraising-themed lures), but with a significantly expanded implant arsenal.

## Still Sync — Telegram session stealer
- Asynchronous Rust application on the **Tokio** runtime.
- Steals **Telegram session data** (`tdata`); with the stolen data it can log into the victim's account and automatically pull **chat logs, media files, and other account data through the Telegram API** — ongoing access beyond a one-shot theft.
- Talks to the server over **gRPC** with **FlatBuffers**-serialized messages; supports both HTTP and HTTPS, with the C2 URL determining the transport.
- Configuration comes from environment variables: `STILL_SYNC_ADDR` (C2 address, default `https://tg4service[.]com:443`), `STILL_SEND_PATH` (path to the `tdata`), and `STILL_TELEGRAM_PASSCODE` (passcode handling).

## Still Audio — covert audio surveillance
- Analyzes the incoming audio stream, **automatically detects speech**, records conversations only when speech is present, and sends recordings to a command-and-control server.
- Deployed as part of the same toolkit; Kaspersky's detection names cover the components as `Trojan.Win64.Agent.*` and `HEUR:Backdoor.Win32.Generic`.

## Victimology and attribution
- Targets: individuals and organizations in Russia across major corporations, public sector, IT, and education.
- Kaspersky assesses the campaign as **Armored Likho** with strong tooling and infrastructure continuity to the group's November 2024 and February 2026 campaigns; the Still Toolkit components are new to the public record.
- The fundraising/donation lure matches the group's documented pattern of impersonating charitable or program-related services.

## Defender priorities
1. **Hunt for Telegram session theft**: `tdata` access on Windows endpoints, unexpected `tdata` exfiltration, and outbound gRPC/HTTPS traffic to `tg4service[.]com:443` or the `STILL_SYNC_ADDR` override.
2. **Treat any Armored Likho compromise as a conversation-harvesting event**: stolen Telegram sessions give attackers ongoing, account-level access to chat history and media — assume exfiltration of any message content from the account, and rotate or log out all Telegram sessions on affected devices.
3. **Hunt for the donation-service dropper**: Rust/Tauri apps with a password-gated login form that then fetch a product catalog over HTTP(S) are the observed facade; correlate `orderapiserver[.]info` `public/categories` / `public/products` requests with local execution of unknown Rust binaries.
4. **Audio-surveillance indicator**: unexpected Windows services or processes capturing audio with speech-activity gating, especially in environments where Armored Likho initial access is plausible.
5. **Persistence**: a Base64-encoded PowerShell command installs `SysExcSvc.dll`-style service pairs in this actor's other campaigns (see [Head Mare / PhantomGraph](head-mare-trueconf-phantomcore-campaign.md) for the same two-component service-split tradecraft); review service creation logs for split installer commands.

## Assessment limits
- Reporting is Kaspersky GReAT (August 13, 2026); no independent vendor corroboration is published as of this scan.
- The Still Toolkit has not been publicly linked to other actors or campaigns.
- Victim scope is described at the sector level; Kaspersky did not name organizations.

## Related pages
- [Armored Likho](../actors/armored-likho.md)
- [Armored Likho BusySnake campaign](armored-likho-busysnake-campaign.md)
- [Head Mare: TrueConf server exploitation delivers PhantomCore and PhantomGraph](head-mare-trueconf-phantomcore-campaign.md)

## Sources
- Kaspersky GReAT: [Armored Likho expands its cyber-espionage toolkit](https://securelist.com/armored-likho-still-toolkit/121033/) — August 13, 2026
