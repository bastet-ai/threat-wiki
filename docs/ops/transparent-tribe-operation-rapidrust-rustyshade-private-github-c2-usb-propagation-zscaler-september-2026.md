# Transparent Tribe "Operation RapidRust": RUSTYSHADE Rust backdoor with private-GitHub-repository C2, RUSTYMOVE USB propagation, and PSNATCH/BASHNATCH file stealers against Indian/Afghan government and defense (Zscaler ThreatLabz, Sep 2026)

## Summary

Zscaler ThreatLabz (Sudeep Singh, report published the week of September 14–18, 2026; The Hacker News coverage September 18) attributes a fresh campaign — **Operation RapidRust** — to the Pakistan-aligned espionage group **Transparent Tribe (APT36, Earth Karkaddan)** targeting **government and defense entities in India and Afghanistan**. Four previously undocumented tools: **RUSTYSHADE** (Rust backdoor), **RUSTYMOVE** (USB propagation), **PSNATCH** (PowerShell file stealer), **BASHNATCH** (its bash twin). The durable tradecraft items: the backdoor's encrypted C2 rides on **attacker-controlled PRIVATE GitHub repositories** via the GitHub REST API (bidirectional file-based tasking — the same "legitimate-platform-as-C2" lane as GITSHELLPAD, observed in APT36-adjacent Gopher Strike in September 2025); delivery infrastructure includes **typosquatted Indian news sites** (`theprints[.]org` mimicking The Print, `indiatodays[.]org` mimicking India Today); and post-compromise operations are **time-boxed to 4 a.m.–11 a.m. UTC on weekdays** — a scheduling signature in its own right. The report lands a little over a month after Acronis TRU tied the same group to the PATCHCORD/SHEETCORD campaign against Afghan telecom and South Asian critical infrastructure (already on-wiki).

## Tags
- ops
- apt36
- transparent-tribe
- cyber-espionage
- pakistan
- india
- afghanistan
- rust
- github-c2
- private-repository-c2
- usb-propagation
- file-stealer
- powershell
- bash
- typosquatting
- news-impersonation
- zscaler
- operation-rapidrust
- rustyshade
- rustymove
- psnatch
- bashnatch

## The toolkit

**RUSTYSHADE** — 64-bit Rust backdoor. C2 channel is an **encrypted exchange of named files inside a private GitHub repository**, driven through the GitHub REST API — no bespoke server, traffic looks like normal GitHub API use, and takedown requires GitHub-side action against an account, not a sinkhole-able IP. Fixed filenames structure the protocol:

| File | Purpose |
|---|---|
| `command.txt` | encrypted C2 commands |
| `results.txt` | encrypted command output |
| `info.txt` | system reconnaissance data |
| `heartbeat.txt` | keepalive beacon confirming active infection |
| `screenshot.png` | encrypted desktop screenshot |
| `webcam_photo.jpg` | encrypted webcam capture |
| `download.bin` | encrypted exfiltrated file contents |

Commands cover screenshots, webcam capture, file operations, and background command execution. Functionally overlaps **GITSHELLPAD** (Golang implant, Gopher Strike campaign, September 2025) — the private-repo file-tasking design is becoming an APT36 house style.

**PSNATCH / BASHNATCH** — file stealers fetched from an attacker-controlled **GitHub gist** post-compromise, one variant per platform (PowerShell for Windows, bash for Linux). Recursive scan of preconfigured directories for Office documents, images, archives, media, executables, scripts, and databases **modified within the last three months**, exfiltrated **to a private repository named after the infected machine** (one repo per victim = victim sorting via repo naming, echoing the campaign-ID patterns this wiki has seen in npm stealers). Caps: 1 GB per file, 5 GB per execution.

**RUSTYMOVE** — lightweight 64-bit Rust USB propagation tool: a PowerShell watcher continuously monitors for removable media and copies two pre-staged files to each detected drive root: `DriverInstaller.zip` (containing RUSTYSHADE) and `DocScanner-11-Aug-2026-5-37pm.pdf.LNK` (suspected LNK command to execute RUSTYSHADE after extraction). A deliberate **air-gap-adjacent bridge** — the classic APT36/SideCopy USB propagation tradition rebuilt in Rust.

## Activity window and signature

- Significant operations observed **August 20 – September 1, 2026**.
- **C2 commands issued only between 04:00–11:00 UTC and only on weekdays** — operator-hours signature usable for hunting (GitHub API activity to victim-named repos outside that window from unusual ASNs is anomalous in either direction) and for attribution correlation.
- Post-compromise sequence: system/user/network reconnaissance → next-stage payload deployment.
- Delivery: typosquatted news-brand domains hosting malicious PowerShell scripts and payloads (`theprints[.]org`, `indiatodays[.]org`).

## Why it matters (durable reads)

1. **Private-GitHub-repository C2 is espionage-grade infrastructure laundering.** The C2 "server" is a platform account: no IPs to blocklist, no certificates to track, traffic indistinguishable from developer activity, and per-victim private repos give the operator clean segmentation. Defenders on GitHub Enterprise/enterprise networks should baseline **REST API file-read/write patterns against private repos unknown to the org**, especially the named-file set above; generic "is the process signed/legit" logic misses it entirely.
2. **The weekday 04:00–11:00 UTC scheduling is a behavioral IOC that survives tool rotation.** Tools change; human working hours don't.
3. **USB propagation is not dead.** RUSTYMOVE shows a nation-state actor still investing in removable-media bridging for targets where network egress is monitored — expect the `DriverInstaller.zip` + `.pdf.LNK` pair shape to recur.
4. **Operational-tempo corroboration:** Acronis's PATCHCORD/SHEETCORD report (~August, Afghan telecom) and RapidRust (India/Afghanistan government + defense) within five weeks of each other support Zscaler's "high operational tempo" framing rather than a one-off tool drop.

## Hunt guidance

- GitHub/network egress: REST API calls to private repositories from non-corporate processes; fixed filename patterns `command.txt`/`results.txt`/`info.txt`/`heartbeat.txt`/`screenshot.png`/`webcam_photo.jpg`/`download.bin` in the same repo; repos whose names encode machine identifiers.
- DNS/proxy: `theprints[.]org`, `indiatodays[.]org` (and expect variants — the pattern is `<brand>s[.]org` against Indian news properties).
- Endpoint: unsigned Rust binaries; PowerShell removable-drive watchers; USB root writes of `DriverInstaller.zip` or `*.pdf.LNK` files; gist-fetching post-compromise scripts; 1 GB/5 GB exfil caps as a volume signature.
- Time-box hunting: C2-like GitHub API sessions concentrated at 04:00–11:00 UTC weekdays.

## Caveats

- Single-vendor report (Zscaler) so far; THN coverage relays it. No named victims beyond sector-level (government/defense, India/Afghanistan).
- "Suspected to contain a command" wording on the `.LNK` file is Zscaler's inference.
- Attribution to Transparent Tribe/APT36 is Zscaler's; consistent with Acronis's independent PATCHCORD attribution the prior month but not multi-agency confirmed.

## Related pages

- [PATCHCORD / SHEETCORD APT36 Afghan-telecom campaign](patchcord-sheetcord-apt36-afghan-telecom-south-asia.md) — same group, prior month, Acronis attribution.
- [Mirage Kitten NodeRabbit/PollCat coding-challenge campaign](mirage-kitten-noderabbit-pollcat-coding-challenge-september-2026.md) — platform-legitimate C2 lane comparison.
- [NightEagle GhostContainer](nighteagle-ghostcontainer-exchange-dev-tunnel-rdp2tcp-dcsync-russia-kaspersky-september-2026.md) — another actor abusing legitimate Microsoft platform services as covert C2/tunneling.

## Sources

- The Hacker News, "Transparent Tribe Deploys New Rust Backdoor Using Private GitHub Repositories for C2," September 18, 2026: <https://thehackernews.com/2026/09/transparent-tribe-deploys-new-rust.html>
- Zscaler ThreatLabz technical report (Operation RapidRust, September 2026, via THN).
- Acronis TRU PATCHCORD context: [on-wiki page](patchcord-sheetcord-apt36-afghan-telecom-south-asia.md).
