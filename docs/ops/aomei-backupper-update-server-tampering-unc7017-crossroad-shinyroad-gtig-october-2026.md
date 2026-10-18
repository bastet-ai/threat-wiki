# AOMEI Backupper / AnyViewer update-server tampering — UNC7017, CROSSROAD/SHINYROAD, the 5–10-minute ephemeral window (GTIG/Mandiant, Oct 2026)

## Summary

Google Threat Intelligence Group (GTIG) and Mandiant [published Oct 15, 2026](https://cloud.google.com/blog/topics/threat-intelligence/investigating-ephemeral-supply-chain-tampering) (first mainstream pickup The Hacker News Oct 16) an investigation of a software supply chain compromise of **AOMEI Technology's update infrastructure** (Backupper + AnyViewer) active **April–July 2026**, attributed to cluster **UNC7017**, credited with initial detection to ManageEngine Threat Analysis Lab (METAL, Zoho) EDR telemetry in late May.

The durable finding is the delivery TIMING, not the malware: the actor did not persist on the origin servers — it conducted **repeated configuration tampering windows of only 5–10 minutes**, reverting the files to authentic versions afterward. GTIG states this is the first software supply chain compromise they have encountered implemented in such short windows, **defeating point-in-time triage and automated file scanning** — a scanner or analyst polling the update endpoints between windows sees clean files.

The tampered artifacts are two INI files the AOMEI client polls over HTTPS:

- `down_html.ini` (`https://www2.aomeisoftware.com/download/abpopup/down_html.ini`) — carries the update version, the expected package MD5, and the download URL for `upgrade-now.zip`. Tampering flips the URL to attacker staging AND synchronizes the `Val=` MD5 so the client's own integrity check passes (July 16 example: `Url=` → `https://promotion.storage-data.com/download/abpopup/upgrade-now.zip`, `thrid=5→6`, MD5 `EE89C99F…` → `31323E7E…`).
- `Notifycfg.ini` — the notification/popup config. July 16 tampering injected **35,000+ repetitive `[dummy_XXXXXX]` sections** to override the client's version check and force immediate execution of the unpacked dropper regardless of installed version; July 20 tampering replaced a promotional banner with an **invisible 1×1-pixel popup at `Priority=9999`** pointing at `file://8.210.84.56/DavWWWRoot/campaign/24hour-flash-sale.html` — a silent **WebDAV/NTLM coercion** harvesting NetNTLMv2 hashes from every polling endpoint. Tampered Notifycfg.ini SHA256 `d2f9ef2429312667f0512504b6a19ba4a9cc5514f1b2933923dd42f75a1c5934`.

## Staging-infrastructure pivots (why infrastructure blocking fails)

Within the campaign the actor iterated its delivery lane three times:

1. **April–May:** Alibaba Cloud OSS Hong Kong (`serv.oss-cn-hongkong.aliyuncs.com`).
2. **July 1–7:** vendor-themed dedicated domains `storage-data.com` / `promotion.storage-data.com` / `aomei.storage-data.com`.
3. **July 20:** initial download moved to a **legitimate Google Cloud Storage bucket** `storage.googleapis.com/aomeiupdate/upgrade-now.zip` — passing enterprise newly-registered-domain (NRD) proxy blocks at fetch time, while the executed loader still phoned `storage-data.com` for stage-2/C2.

GTIG's point: the staging setup's evolution makes infrastructure-based blocking and network controls largely unestablishable — the fetch lane can be a trusted cloud provider's storage on any given day.

## Payload chain

- **CROSSROAD** (new family, stage-2 downloader): `upgrade-now.exe`, 64-bit C, SHA256 `9a58e8f49edf5644e5728f74cf36f560d3d486fa51db4db69d927963c7aca450`; environment validation, endpoint cleanup, stage-3 staging, scheduled-task persistence. Guardrails: **path check** — self-deletes if its own path lacks the substring `AOMEI` but CONTINUES its routines regardless; **geolocation** — resolves its own IP via `myip.opendns.com`, `o-o.myaddr.l.google.com`, `checkip.amazonaws.com`, `api.ipify.org`, `ifconfig.me/ip`, `icanhazip.com` with User-Agents `Anyviewer-loader/1.0` / `Anyviewer-ipcheck/1.0`, and aborts the primary payload path if the country code is `CN`; **mutex** `Global\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}`; anti-forensics reverts local host artifacts and timestomps PEs to fabricated 2024 compile dates.
- **SHINYROAD** backdoor (stage-3 suite), plus wave-dependent arms: May 28 wave silently installed a **modified commercial Radmin Server** (`rsetup64.exe /intsetup`) for persistent remote access; since early July the actor ran **Adaptix C2** across the `storage-data.com` infrastructure.

## Victimology and disposition

Impacted organizations spanned IT services, telecommunications, and higher education across Australia, Brazil, India, Pakistan, Portugal, Singapore, South Africa, Spain, Switzerland, Türkiye, and the United States — but victimology was **opportunistic**: every endpoint polling the update servers during a tampering window was targeted, so true scope likely exceeds the identified orgs. AOMEI took corrective action on the distribution servers after GTIG notification; **infected machines remain compromised** (THN, Oct 16) — server remediation does not clean clients, and the clients happily re-download from the now-authentic server while a loader persists.

## Defender heuristics (durable)

- **Ephemeral tampering is the new persistence-free compromise.** For any update/notification manifest endpoint you consume or serve, point-in-time file integrity is not evidence of integrity; detection needs per-fetch change history on the CONFIG (URL + hash fields), not periodic scans. Defenders on the consuming side can alert on `down_html.ini`-style files whose download-URL host differs from the vendor apex, regardless of the file's current state.
- **Synchronized MD5 = the vendor's own check is weaponized.** Client-side "expected hash" fields inside the same file being tampered authenticate the ATTACK, not the update. Trust belongs out-of-band (signed manifests), not in-band.
- **The config-bloat trick**: thousands of dummy sections overriding version checks is a schema-violation signal a config parser could catch cheaply if schemas were enforced client-side.
- **1×1 popup + `file://` UNC = NTLM coercion in config skin.** A notification-config renderer fetching `file://` paths is itself the vulnerability class; outbound SMB/WebDAV coercion can be blocked at the perimeter (block 445 outbound + NTLM-authenticated WebDAV egress).
- **Egress from update clients should be allow-listed by apex domain, cloud buckets included** — `storage.googleapis.com/<anything>` is not trust.
- **CN-geoguard + path-substring self-check + timestomp-to-2024** are pivot-worthy tradecraft markers for hunts.

## IoC quick table

| Type | Value | Role |
|---|---|---|
| Domain | `storage-data.com`, `promotion.storage-data.com`, `aomei.storage-data.com` | staging / C2 (July) |
| IP | `8.210.84.56` | WebDAV NTLM coercion |
| Bucket | `storage.googleapis.com/aomeiupdate/upgrade-now.zip` | NRD-evasion fetch lane (July 20) |
| Bucket | `serv.oss-cn-hongkong.aliyuncs.com` | early staging (Apr–May) |
| SHA256 | `9a58e8f49edf5644e5728f74cf36f560d3d486fa51db4db69d927963c7aca450` | CROSSROAD `upgrade-now.exe` |
| SHA256 | `d2f9ef2429312667f0512504b6a19ba4a9cc5514f1b2933923dd42f75a1c5934` | tampered Notifycfg.ini |
| MD5 | `31323E7E738230FA6A8DEEF2B7894666`, `BF73C4391B58CA95220CE3AE03F66DCF` | tampered down_html.ini `Val=` |
| Mutex | `Global\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}` | CROSSROAD single-instance |
| UA | `Anyviewer-loader/1.0`, `Anyviewer-ipcheck/1.0` | IP-reflection geolocation |
| Path rule | self-delete if path lacks `AOMEI` (continues anyway) | sandbox/path check |

## Timeline (public record)

- Apr–Jul 2026 — repeated 5–10-min tampering windows on `www2.aomeisoftware.com` config files.
- late May 2026 — METAL EDR detects activity across multiple customer environments.
- May 20 — CROSSROAD dropper submitted to VirusTotal (timestomped to 2024 dates).
- May 28 — modified Radmin Server wave.
- Jul 16 / Jul 20 — documented tamper instances (MD5-sync URL flip + dummy-section bloat; GCS bucket lane + 1×1 WebDAV coercion popup).
- Jul 2026 — campaign window closes; AOMEI secures servers after GTIG notification.
- Oct 15 — GTIG/Mandiant publication; Oct 16 — THN mainstream pickup ("servers fixed, infected machines remain compromised", organizations across 11 countries).

## Related pages

- [Brevo third-party widget supply chain](brevo-third-party-widget-supply-chain-wordpress-plugin-clickfix-sansec-september-2026.md) — the other 2026 shared-infrastructure compromise: Brevo's was one ~4 h poisoning window on served JavaScript, UNC7017's was REPEATED 5–10-min windows on update configs — same lesson class (trust boundary is the vendor's delivery lane), opposite persistence posture.

## Monitor

- AOMEI follow-up: client-side detection/removal tooling, signature of the modified Radmin install, SHINYROAD indicator publication.
- METAL (Zoho) companion blog for endpoint-level IoCs.
- Whether the 5–10-min-window pattern is copied by other actors against other update feeds (this is a playbook, now public).
- UNC7017 attribution refinements; any naming/law-enforcement action.
- Whether `storage-data.com` domains/bucket see re-registration or reuse.

Sweep context → [130th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-thirtieth-sweep).
