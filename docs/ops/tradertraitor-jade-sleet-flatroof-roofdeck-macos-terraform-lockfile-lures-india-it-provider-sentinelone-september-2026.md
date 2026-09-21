# TraderTraitor / Jade Sleet: the KelpDAO–LayerZero macOS backdoors (FLATROOF = our on-wiki macOS.Gaslight, + ROOFDECK with Nostr-resolved C2 and signed commands) resurface on an Indian IT-services victim with no crypto ties — weaponized `.terraform.lock.hcl` lures, a dormant-until-Cursor-opened foothold, and a day-after-disclosure stealth rebuild (SentinelOne Labs, Sep 18, 2026)

## Summary

SentinelOne Labs published **"Don't Call Us, We'll Call Your APIs: TraderTraitor Backdoors Resurface on Victim With No Crypto Ties"** on September 18, 2026 (published alongside the authors' LABScon 2026 talk; The Hacker News picked it up September 21). It documents a second victim of the exact macOS backdoor pair used in the April 2026 **KelpDAO/LayerZero $292M** theft: an **India-based IT services provider, unaffiliated with cryptocurrency**, infected via the same DPRK fake-job-interview pipeline. The attribution sentence is now explicit: **TraderTraitor aka UNC4899, PUKCHONG, Jade Sleet** (the financially motivated Lazarus subgroup that hit Bybit via the Safe{Wallet} supply-chain compromise in early 2025 per GitHub's 2023 framing quote).

Three things make this durable intel rather than one more DPRK recruiting-scam writeup:

1. **FLATROOF = macOS.Gaslight.** SentinelOne states the June 2026 Gaslight analysis (our [macOS.Gaslight page](macos-gaslight-rust-backdoor.md)) IS the FLATROOF backdoor under LayerZero/Mandiant's name — the first public alias join between the SentinelLABS tool family and the incident-named tooling.
2. **ROOFDECK's C2 bootstrap is a decentralized dead-drop**: the implant needs a config file containing a **Nostr public key** of an attacker profile; on first run it pulls live relays from `api.nostr[.]watch/v1/online`, merges them with a hardcoded list of legitimate Nostr relays, finds the operator's profile, and **uses the profile's `website` field as the C2 URL**. All operator commands are **signed with an attacker private key and signature-verified by an embedded public key before execution** — C2 authenticity without infrastructure ownership, and command injection impossible for a defender who seizes the relay or C2 host.
3. **The disclosure-response behavior**: on **April 20 — one day after LayerZero's public announcement** — the attackers deployed a rebuilt ROOFDECK (stripped symbols/debug, new path, new pinned cert chain) that then **deleted the old FLATROOF and ROOFDECK binaries**. Vendor publication is an adversary trigger; assume your IR notes become attacker OPSEC input the moment they go public.

## Tags
- ops
- DPRK
- North Korea
- Lazarus
- TraderTraitor
- Jade Sleet
- PUKCHONG
- UNC4899
- Slow Pisces
- macOS
- malware
- backdoor
- Rust
- ARM64
- FLATROOF
- Gaslight
- ROOFDECK
- Nostr
- dead-drop
- C2
- Terraform
- supply-chain
- infrastructure-as-code
- fake-job-interview
- Contagious Interview
- social-engineering
- developer-targeting
- DevOps
- job-lure
- crypto
- LayerZero
- KelpDAO
- Bybit
- keychain-theft
- persistence
- LaunchAgent
- Gatekeeper-bypass
- mkcert
- OPSEC
- certificate-pivot

## Why this matters
- **The developer endpoint is the access product.** The victim was chosen the same way as LayerZero's "Developer1": an Apple Silicon MacBook whose owner ran Terraform/Ansible against AWS, OVH, and OpenStack, holding cloud credentials + source-control access. SentinelOne's formulation: *individuals whose social media advertises infrastructure/DevOps work are candidates; the value of the target is whatever their laptop can reach.*
- **Infrastructure-as-code files are now first-class phishing attachments.** A `terraform init` on a repo from your "interviewer" treats `.terraform.lock.hcl` custom providers as the source of truth and downloads+executes attacker modules. The lockfile is trusted-by-design tooling nobody code-reviews.
- **Not every intrusion pays, and that changes triage.** The attacker's own activity suggests the India victim "yielded insufficient value to sustain the intrusion" — beaconing went intermittent after a C2 migration and the binary went to Trash by June 17. Low-and-slow doesn't mean abandoned-by-accident; it can mean downgraded-by-accounting, and can be resumed.
- **Signed commands + decentralized C2 discovery is the hardened-resilience pattern** to design detections against, because takedown-centric defenses (sinkhole the C2, seize the domain) don't revoke the trust model.

## Reported behavior

### Delivery: fake interviews with per-victim backdoored repos
- Classic **Contagious Interview** social engineering: the attacker contacts **job seekers at the company that ends up compromised** (not random candidates), each targeted profile being DevOps or crypto/FinTech engineering.
- Lure repos are themed as **infrastructure-engineering projects of the company the actor is impersonating**; pivoting from LayerZero's published `gtn-candidate-repo`, SentinelOne found further lures referencing the companies **Northwind** and **Novacart** (fabricated or real-but-impersonated, unresolved).
- Each repo ships a **weaponized `.terraform.lock.hcl`** with a custom provider pointing at attacker domains (three identified; SentinelOne's IoC list carries them). Running `terraform init` fetches and executes the malicious provider module.
- Developer-awareness wrinkle: in one repo the **candidate removed a typosquatted provider** from the lockfile and noted it — possibly reading the infection as a security-awareness test. Lures now live inside a "would you run this?" teaching moment, which cuts both ways.

### FLATROOF (aka macOS.Gaslight) — initial-collector implant
- Dropped as `SystemUpdate` in `~/Library/com.apple.iTunesCloud/SystemUpdate`; ARM64 Rust.
- On start it **removes `com.apple.quarantine` from ROOFDECK and sets its executable bit** — Gatekeeper is bypassed by the first-stage implant, so the second implant runs with no signature check and no prompt.
- Detailed capability set + the analyst-targeting prompt-injection block are on our [macOS.Gaslight page](macos-gaslight-rust-backdoor.md).
- Ships with a Python collection module exfiltrating over **Telegram using a built-in bot token**.

### ROOFDECK — the follow-on implant
- Dropped as `iSync` in `~/Library/com.apple.internal.ck/iSync`.
- **Requires a pre-existing config containing at minimum a Nostr public key** → designed to be deployed only after foothold/control exists (`~/.config/.repl_history` stores C2 URLs, keys, beaconing settings — the filename itself is tradecraft: a fake REPL history).
- C2 bootstrap: pull live relays from `api.nostr[.]watch/v1/online` + hardcoded legitimate Nostr relay list → locate the operator's Nostr profile by pubkey → **read its `website` field = C2 URL**. C2 endpoint path `/app_version`, HTTPS with an **embedded pinned certificate**.
- **Every C2 command is signed server-side; the implant verifies against an embedded public key before executing.** Handlers are separated per command in source; the implant **re-implements common shell commands** for directory/file operations (SentinelOne ties this habit to sophisticated DPRK tooling incl. Lazarus' LightlessCan).
- Persistence: `~/Library/LaunchAgents/loginwindow.plist` with a dynamic app-identifier and a hardcoded `--type=renderer` argument to make the process look like a browser helper.
- **OPSEC leak:** the pinned cert was made with **mkcert default metadata**, exposing a Linux QEMU VM running as username **`ub`** — SentinelOne found multiple attacker domains reusing that certificate CN = a certificate-name pivot that survives domain rotation.

### Timeline on the India victim (telemetry-derived)
- Backdoors on disk since **March 18, 2026** (delivery vector unproven); **dormant until March 29**, when beaconing began — first launch **by Cursor, seconds after the `~/DevOps-Automation/cloudshield` workspace was opened**. An IDE opening a workspace is the detonator; EDR that ignores `cursor` as "development noise" misses the parent-child signal.
- **April 20, 2026** (day after LayerZero's public KelpDAO disclosure): rebuilt ROOFDECK deployed as `loginwindow` at `~/Library/com.apple.appleaccountd/loginwindow` (SHA-1 `5728b11d30586bbfc1d8bd12df1c722a06e767a2`), functionally identical but **stripped of symbols/debug info**, then used to **delete both older binaries**.
- Intermittent beaconing to new C2 `grenight[.]com` until **June 1**; binary moved to Trash **June 17** — SentinelOne assesses the intrusion yielded insufficient value to sustain.

## Indicators and hunt pivots
- Paths: `~/Library/com.apple.iTunesCloud/SystemUpdate`, `~/Library/com.apple.internal.ck/iSync`, `~/Library/com.apple.appleaccountd/loginwindow`, `~/Library/LaunchAgents/loginwindow.plist`, config `~/.config/.repl_history`.
- Process tells: implant launched by Cursor/editor processes seconds after workspace open; LaunchAgent plists named `loginwindow.plist` with `--type=renderer` from outside a browser bundle; a binary stripping `com.apple.quarantine` off another file.
- Network: HTTPS to `/app_version` with a pinned non-CA cert; DNS to `api.nostr[.]watch` (rare on corporate laptops unless the user is actually on Nostr); `grenight[.]com`; the three malicious Terraform provider domains in SentinelOne's IoC list (canonical page).
- Certificate pivot: TLS certs issued by **mkcert with default metadata / CN exposing username `ub` on a QEMU VM** — hunt your TLS-inspection logs for that issuer string.
- Hash: ROOFDECK rebuild SHA-1 `5728b11d30586bbfc1d8bd12df1c722a06e767a2`.
- Supply-chain audit: any repo received out-of-band (interview projects, "take-home" repos) with a `.terraform.lock.hcl` naming a provider source that is not `registry.terraform.io` — treat `terraform init` on such a repo as executing attacker code.

## Defender heuristics
- Gate `terraform init` (and OpenTofu/Ansible Galaxy fetches) in CI and on managed endpoints to approved registry mirrors/provider domains; pin provider checksums and verify against the public registry.
- Treat IDE-spawned first-execution of a previously-dormant binary as a Tier-1 detection, not development noise (parent = editor, child = unsigned binary in `~/Library/com.apple.*`).
- Alert on quarantine-attribute removal (`xattr -d com.apple.quarantine`) by non-installer binaries.
- On any confirmed DPRK macOS implant: treat every cloud credential the laptop could reach as exposed (this actor's LayerZero objective was API keys → AWS/GCP privilege escalation), rotate at the identity layer, and audit for the follow-on implant rebuild — the attacker may already have replaced what your IR report described.
- Search for attacker infrastructure by **certificate identity** (mkcert defaults, `ub` QEMU CN) rather than domains — this actor rotates domains within weeks.

## Attribution notes
SentinelOne names the cluster **TraderTraitor (aka UNC4899, PUKCHONG, Jade Sleet)**, the financially motivated DPRK Lazarus subgroup, and states cooperation with Google and Mandiant on the technical details. The June Gaslight assessment ("DPRK-aligned macOS activity cluster, high confidence") and this campaign-level naming are now the same lineage. SentinelOne's own caveat stands on the India victim: delivery mechanism unproven (implants on disk before observation began).

## Related pages
- [macOS.Gaslight Rust backdoor](macos-gaslight-rust-backdoor.md) — the FLATROOF implant's June 2026 analysis incl. the prompt-injection anti-analysis block
- [CrashStealer macOS notarized dropper](crashstealer-macos-notarized-dropper.md) — adjacent macOS developer-targeting ecosystem
- [Kimsuky / Emerald Sleet / TA427](../actors/kimsuky-emerald-sleet-ta427.md) — another DPRK-nexus named cluster on-wiki

## Sources
- SentinelOne Labs (canonical, verified live by this wiki): [https://www.sentinelone.com/labs/dont-call-us-well-call-your-apis-tradertraitor-backdoors-resurface-on-victim-with-no-crypto-ties/](https://www.sentinelone.com/labs/dont-call-us-well-call-your-apis-tradertraitor-backdoors-resurface-on-victim-with-no-crypto-ties/) (published Sep 18, 2026 17:00 UTC, alongside the authors' LABScon 2026 talk)
- The Hacker News: [https://thehackernews.com/2026/09/jade-sleet-linked-to-indian-it-provider.html](https://thehackernews.com/2026/09/jade-sleet-linked-to-indian-it-provider.html) (Sep 21, 2026)
