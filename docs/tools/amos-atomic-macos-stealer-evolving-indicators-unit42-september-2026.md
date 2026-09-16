# AMOS (Atomic macOS Stealer): the indicators always rotate — Unit 42's early-August 2026 lab snapshot pins the durable pattern (fake "macOS toolkit" quick-setup page → clipboard-paste Zsh → `/tmp/helper` → masquerade dirs `.com.apple.accountsd` / `.com.apple.metadata.mds` → Terminal-app TCC permission prompts → staged `stage=` C2 URLs)

## Tags
- tool
- tools
- AMOS
- Atomic Stealer
- Atomic macOS Stealer
- macOS malware
- infostealer
- ClickFix
- clipboard paste
- Zsh script
- Mach-O
- universal binary
- Gatekeeper
- TCC permissions
- Terminal permissions
- Apple masquerade
- accountsd masquerade
- mdworker masquerade
- crypto wallet theft
- browser credential theft
- Telegram data
- Apple Notes
- staged C2 URLs
- Hetzner C2
- cracked software lure
- malicious ads
- Unit 42
- active development

## Summary

**AMOS (Atomic macOS Stealer)** is a macOS information stealer, advertised on Telegram since at least **April 2024**, that exfiltrates system information, login credentials, browser data, keychain material, SSH keys, authentication stores, and **cryptocurrency wallet data**. It is distributed via **ClickFix-style clipboard-paste campaigns**, **malicious advertisements**, and **cracked-software / "toolkit" instruction pages**. Unit 42's **September 16, 2026** analysis of a lab infection from **early August 2026** is less valuable for its indicators than for its core conclusion, stated explicitly: **AMOS indicators change constantly** — domains, URLs, IPs, filenames, hashes, and directory paths all rotated between the July 31, 2026 and August 5, 2026 infections Unit 42 compared. The malware is **in active development**; anything blocklisted from a report is stale. The durable defense is the behavioral chain below.

## Infection chain (Unit 42 lab reproduction, Aug 5, 2026)

1. **Lure**: `getmacouscloud[.]com` hosts an instruction page for a fake "macOS toolkit" "quick setup." Unit 42 notes this copy/paste pattern is *called* ClickFix but is technically a variant — no fake CAPTCHA, just instructions to copy a command and paste it into Terminal.
2. **Paste → execute**: the copied text fetches a **Zsh script** from `hxxps[:]//ferncore13[.]com/curl/<64-hex>` — the same `/curl/<id>` URL shape Microsoft documented in its fingerprinting-gated MacSync/AMOS campaign.
3. The Zsh script embeds **Base64-encoded GZIP-compressed** data; decompressing yields a follow-up Zsh script that retrieves and runs a Mach-O installer saved as **`/tmp/helper`**, alongside a plist named **`/tmp/starter`**.
4. **Persistence (two masquerade directories under the user's `~/Library/Application Support/`)**:
   - `.com.apple.accountsd/` — shell script `.service` executing Mach-O **`AccountsHelper`** (masquerading as the accountsd daemon's support directory)
   - `.com.apple.metadata.mds/` — shell script `.mdworker` executing Mach-O **`mdworker_shared`** (masquerading as Spotlight metadata worker paths)
5. **Social/permission engineering**: infection requires the **user's admin password** (prompted mid-chain), after which the **Terminal process itself** requests TCC permissions — **control of Finder, Desktop files, Documents files, control of Notes** — each prompt appearing "legitimate" because Terminal is the requesting app.
6. **Collection**: data gathered to `/tmp`, compressed to **`out.zip`**, with an internal structure that doubles as a target list:
   - `deskwallets/Binance/`, `deskwallets/TonKeeper/` (desktop wallets)
   - `FileGrabber/aws/`, `FileGrabber/docker/`, `FileGrabber/filezilla/`, `FileGrabber/gcloud/`, `FileGrabber/zsh_history`
   - `Telegram Data/`, `info`, `username`

## C2 pattern (durable)

Post-infection traffic is **HTTP POSTs to a C2 whose URLs end in staged markers** — collection categories visible in the URL itself:

`stage=boot`, `stage=init_session`, `stage=messengers`, `stage=credentials`, `stage=browsers`, `stage=wallets`, `stage=resolve_auth`, `stage=local_data`

This exact `stage=` URL grammar appeared in both Unit 42 infections (July 31 and August 5, 2026) **while everything around it rotated** — C2 moved from `188.166.78[.]138` to `161.35.146[.]120` (both Hetzner ranges in the observed set). Hunt the URL shape, not the IP.

## Why blocklists fail against AMOS

Unit 42's explicit guidance: treat any published AMOS indicator set (including theirs) as a **time-limited snapshot**. Stable behavioral pivots instead:

- Zsh executed by `Terminal.app` fetching a `/curl/<sha256-ish hex>` path (shared with Microsoft's documented ClickFix front-end campaign)
- Creation of `~/Library/Application Support/.com.apple.*` directories — **Apple-namespaced dot-directories under a user's Application Support are not legitimate macOS layout**
- A Terminal process requesting Finder/Notes/Desktop/Documents TCC control outside a developer's known workflow
- `out.zip` written under `/tmp` containing `deskwallets/` or `FileGrabber/` paths
- HTTP POST URLs ending `stage=wallets` / `stage=credentials` / etc.

## Relations

AMOS sits at the end of several documented macOS delivery lines: the **Microsoft-documented fingerprinting-gated ClickFix campaign** (250+ dictionary-word `file` front-ends delivering MacSync or AMOS), the **Huntress Google-Doc-sidebar campaign** (Sep 15, 2026 — Apps Script sidebar profiling wallet extensions, then AMOS on the macOS branch), **GTIG UNC7005/Storm-2945** (commodity infostealer stage of Russian-interest targeting), and cracked-software/malvertising distribution.

## Indicators (as published by Unit 42, Sep 16, 2026 — snapshot, expected stale)

| Item | Value |
|---|---|
| Initial Zsh script SHA-256 | `71781ad8adefb499aee9bcbe1a166e69ccc37a47066682f617d65c76d8cde88c` (1,991 B) |
| Extracted payload Zsh SHA-256 | `7ea6ff8b12c59aaae1ab6f4f5a57045dad5a8127954f3ffd3d1c154d40d7ca3a` (1,213 B) |
| Installer (`/tmp/helper`) SHA-256 | `a598fcdcd49247312861ff90c16cb4a5d49fede6072e30e7416dd276668fa2a9` (330,768 B, universal Mach-O) |
| Persistent (`AccountsHelper`) SHA-256 | `6bfcdb4920383375b7e519918df7eb4db751b974b5571a15ce66b82478012620` (438,576 B) |
| Persistent (`mdworker_shared`) SHA-256 | `4504006d1911057be42435d4625f03d83c4d0b7b6898d14beb9cdeba6cf667b9` (568,368 B) |
| Lure site | `getmacouscloud[.]com` |
| Initial download | `hxxps[:]//ferncore13[.]com/curl/608e70d1338612686917ee5cd300ff7ed8e318dfd787a50257f92142e99bd688` |
| Payload URLs | `hxxps[:]//grove-89[.]com/api/metrics/run?event=pasted`, `hxxps[:]//ferncore13[.]com/2kqYRM0DCrnyJgoS4gVLl_FHJRRdTUhGCbjyuYwpZ6c/m1/update` |
| C2 (Aug 5 infection) | `161.35.146[.]120` |
| C2 (Jul 31 infection) | `188.166.78[.]138` |

## References

- Unit 42 (Sep 16, 2026): <https://unit42.paloaltonetworks.com/atomic-macos-amos-stealer-activity/>
- Malware-Traffic-Analysis.net AMOS infection writeup (Jun 9, 2026); Malpedia AMOS family page (via Unit 42)

## Related

- [macOS ClickFix fingerprinting-gate campaign](../ops/macos-clickfix-fingerprinting-gate-campaign.md) — the Microsoft-documented 250-domain front-end line that ends in MacSync/AMOS
- [Google Doc sidebar / rogue-CA campaign](../ops/google-docs-apps-script-sidebar-clickfix-rogue-ca-ledger-implant-huntress-september-2026.md) — Sep 2026 delivery line whose macOS branch serves AMOS
- [UNC7005 Russian-interest targeting clusters](../ops/russian-oauth-whatsapp-device-link-account-hijacking-gtig.md) — AMOS/Vidar as the commodity-stealer stage
