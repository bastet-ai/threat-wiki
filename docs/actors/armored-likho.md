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

## Tooling and infrastructure
- **[BusySnake Stealer](../tools/busysnake-stealer.md)** — Python / PyArmor Windows infostealer with browser credential theft, cookie theft, screenshot and clipboard collection, document exfiltration, task polling, and built-in reverse SSH tunneling.
- **AquilaRAT** — earlier / staple Armored Likho RAT tooling; Kaspersky notes architectural overlap with BusySnake's handler-based task execution and C2 status-update design.
- **Go2Tunnel** — prior standalone reverse SSH tunneling tool; BusySnake implements similar tunnel establishment directly inside the stealer.

## Defensive pivots
- Treat spear-phishing attachments that launch `rundll32.exe` and then PowerShell as high-risk initial access, especially when followed by Python runtime staging.
- Hunt for `%APPDATA%\\WindowsHelper`, `module.pyw`, `run.vbs`, `wh_selfdelete.vbs`, and scheduled tasks masquerading as Windows helper / update utilities.
- Correlate browser credential extraction, cookie database access, screenshot archives, reverse SSH processes, and outbound traffic to Armored Likho C2 domains.
- Because Kaspersky says first-stage code style strongly suggests LLM-generated loaders, do not rely only on stable loader syntax for clustering.

## Related pages
- [Armored Likho BusySnake campaign](../ops/armored-likho-busysnake-campaign.md)
- [BusySnake Stealer](../tools/busysnake-stealer.md)

## Sources
- [Kaspersky Securelist](https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/)
