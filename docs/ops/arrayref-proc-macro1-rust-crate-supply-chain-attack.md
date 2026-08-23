# Rust supply-chain attack: arrayref 0.3.10 and the proc-macro1 typosquat

## Summary
On **August 20, 2026**, a short but high-blast-radius **Rust crates.io supply-chain attack** compromised the foundational `arrayref` crate (v0.3.10, published **07:15 UTC**) and pulled in a **typosquatted `proc-macro1` crate** (v1.0.106 staging / v1.0.107 payload) impersonating the ubiquitous `proc-macro2`. The malicious code lives entirely in `proc-macro1`'s `build.rs`: any machine that **compiles** a project resolving the dependency — without ever calling the crate — downloads a platform-specific stage-2 binary from a Hostwinds VPS and executes it, detached from the Cargo build.

The operation was not limited to `arrayref`. Within 23 minutes the same compromised `droundy` account poisoned two more of its crates (`internment` 0.8.7, `append-only-vec` 0.1.9), and the registry sweep removed a second dropper crate (`proc-macro-en`) plus four additional attacker-owned crates. Per-crate exposure windows ran **86 / 90 / 107 minutes** (07:11–09:25 UTC overall). crates.io deleted `proc-macro1` at 08:03, removed `arrayref` 0.3.10 at 08:41, and purged the other two poisoned releases by 09:25. The legitimate `droundy` maintainer account (in good standing since 2009) is **presumed compromised** and locked; the attacker's `dtolney` persona (impersonating `proc-macro2` author David Tolnay) was fabricated the same morning with forged author metadata (`David Tolnay <rchaitm@gmail.com>`). All malicious yanks have been reversed. StepSecurity's August 20 technical write-up (including a live runtime reproduction) remains the most complete public record; stage-2 payload recovery is still pending, but third-party reports from infected hosts now describe persistence behavior.

## Tags
- ops
- operations
- Rust
- crates.io
- arrayref
- proc-macro1
- proc-macro2
- typosquat
- build.rs
- build-time execution
- supply chain
- cargo
- CI/CD
- Hostwinds
- incident response
- DPRK
- Sapphire Sleet
- UNC1069

## Why this matters
- **`arrayref` is a load-bearing crate with ~245 million all-time downloads.** Reverse-dependency reach documented by StepSecurity includes `tiny-skia` → `sctk-adwaita` → `winit` (i.e., under egui/eframe, iced, and most Rust GUI apps), plus `blake3`, `blake2b_simd`/`blake2s_simd`, `revm-precompile` (Ethereum), and `solana-runtime`/`spl-token` (Solana). Any CI job or developer build that resolved `arrayref ^0.3` fresh during the window ran the payload with that user's privileges.
- **Build-time execution is the primitive.** No import, no function call — `build.rs` runs at compile time. This mirrors the `npm postinstall` / `node-gyp binding.gyp` / PyPI `.pth` patterns already documented in the wiki, but in the Rust ecosystem, where `Cargo.lock` pinning is the primary defense.
- **The yank burst was deliberate social pressure.** Within the same minute as the malicious `arrayref` 0.3.10 publication, versions 0.3.5 through 0.3.9 were yanked in a scripted burst (~4 seconds apart) so that Cargo's "yanked version" warning nudges lockfile-holders toward upgrading into the trap.
- **Fresh-resolution window matters more than version numbers.** Because `Cargo.lock` pins exact versions, only projects that *re-resolved* dependencies (new lockfiles, `cargo update`, CI runners without lockfiles, `cargo add`) during ~07:11–08:41 UTC were exposed.
- **Attribution is not yet asserted.** This is a credential-theft / account-compromise + impersonation tradecraft event; StepSecurity does not link it to a named actor as of the initial post. On the same day, however, Wiz published infrastructure overlap evidence with DPRK-attributed supply-chain campaigns (shared beacon path and Hostwinds range with the Microsoft-attributed Mastra/Sapphire Sleet campaign, and a victim-reported C2 IP that appears in Mandiant's UNC1069 axios analysis) — correlation, not operator confirmation; see the [Wiz section](#wiz-stage-2-implant-analysis-and-dprk-infrastructure-overlap).

## Attack chain (timeline, UTC)
1. **2026-08-18** — `arone` (7 versions) and `aronenao` (11 versions) reach their final publishes; both carry malicious build scripts and are owned by the same account as `tinymember`. The campaign's infrastructure predates the arrayref push by two days.
2. **01:17** — GitHub account `dtolney` created, impersonating David Tolnay (`proc-macro2` author).
3. **01:25** — matching crates.io account `dtolney` (id 438608) created.
4. **01:55** — `proc-macro1` **1.0.106** published: a clean verbatim copy of `proc-macro2` (staging; builds a plausible benign crate under the squatted name).
5. **07:11** — `proc-macro1` **1.0.107** published, adding build dependencies (`base64`, `rustls`, `ureq`) no genuine proc-macro library needs, plus the malicious `build.rs`.
6. **07:15** — `arrayref` **0.3.10** published from the legitimate owner account `droundy`, adding its first dependency in the crate's decade-long history: `proc-macro1 ^1.0.107`. In the same minute, `arrayref` 0.3.5–0.3.9 are yanked in a scripted burst.
7. **07:34** — `internment` **0.8.7** published from the same compromised account, with the same build-time dropper dependency injected.
8. **07:37** — `append-only-vec` **0.1.9** published from the same account, completing three poisoned releases in 23 minutes.
9. **07:54** — incident reported to RustSec advisory-db (report #3161 by researcher jhobern) and the Rust security team.
10. **08:03** — crates.io deletes `proc-macro1`.
11. **08:41** — crates.io removes `arrayref` 0.3.10 from the index (~86-minute exposure window).
12. **09:04** — `internment` 0.8.7 deleted (~90-minute window). The `droundy` GitHub account and the canonical `droundy/arrayref` repository return 404 (cause unknown at the time).
13. **09:25** — `append-only-vec` 0.1.9 deleted after being flagged malicious in the RustSec thread at 09:14 (~107-minute window, the longest of the three).
14. **Same day** — `proc-macro-en`, `aovine`, `arone`, `aronenao`, and `tinymember` deleted; all publishing accounts and the `droundy` account locked; the maliciously yanked `arrayref`, `internment`, and `append-only-vec` releases un-yanked, restoring the clean versions.

## How the payload works
- `proc-macro1` 1.0.107's `build.rs` **reassembles infrastructure from base64 fragments**: payload host `https://23.254.165.112:9089/` and C2 endpoint `23.254.165.112:443`.
- It fetches a **stage-2 binary over TLS with certificate validation disabled** (accept-all verifier), choosing among `rust-crate_0.1.0` … `rust-crate_0.4.0` by target platform.
- Drops to `/tmp/rust-setup` (Unix) or `%TEMP%\rust-setup.ps1` via a hidden `wscript.exe` launcher (`rust-setup-launch.vbs`) on Windows, then **spawns it detached** with the C2 address as `argv[1]`, carefully escaping Cargo's job object so the build completes normally.
- The library code is genuine `proc-macro2`, so builds succeed and the infection is invisible in normal output.
- Payload host resolves to a **Hostwinds VPS** (`hwsrv-798836.hostwindsdns.com`) — the same provider class seen in Mastra / `easy-day-js` npm RAT infrastructure.

## Indicators of compromise
- **Network:** `23.254.165.112:9089` (payload host), `23.254.165.112:443` (C2), `hwsrv-798836.hostwindsdns.com`
- **Network (stage-2 C2, third-party reports):** `23.254.167.107` and `23.254.167.216` (reported by infected developers in the RustSec thread; both in the same Hostwinds range as the build-time C2 — treat the `23.254.165.0/24` and `23.254.167.0/24` ranges, not just the individual addresses, as the indicator)
- **Files:** `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`
- **Binaries:** `rust-crate_0.1.0` / `_0.2.0` / `_0.3.0` / `_0.4.0`
- **Crates (compromised legitimate, deleted):** `arrayref` 0.3.10, `internment` 0.8.7, `append-only-vec` 0.1.9 (all under the same `droundy` owner)
- **Crates (attacker-owned, all versions deleted):** `proc-macro1` (1.0.106 decoy and 1.0.107 payload), `proc-macro-en` (spare dropper, same build script as `proc-macro1`), `aovine`, `arone`, `aronenao`, `tinymember` (deleted by association; no malicious code found in it, but shared the owner account)
- **Accounts:** `dtolney` (crates.io id 438608, impersonator); `droundy` (legitimate owner of the three compromised crates, presumed compromised and locked as a precaution; associated GitHub account returning 404 at time of writing)
- **Email:** `rchaitm@gmail.com` (forged author metadata)
- **SHA-256 (registry-verified via crates.io index git history):**
  - `25ad700976873c76af785cb99b33c48db7df8b81f21d1e9e06b3676b9a9373ae` — `arrayref-0.3.10.crate`
  - `61198155da51b838772eecf5bfaac6cbc4dcc388dccc56658fc28a8e831b34d4` — `proc-macro1-1.0.107.crate`
  - `b5c1b5b0763a8809a644a8f92224653f0aca623a98eecc714d27f74b80fbe436` — `proc-macro1-1.0.106.crate`
  - Checksums for `internment` 0.8.7, `append-only-vec` 0.1.9, and the `proc-macro-en` release are not recoverable: those versions were hard-deleted from crates.io, the sparse index, and docs.rs before they could be archived.

## JFrog follow-up: two more crates in the same `droundy` account

On **August 20, 2026**, JFrog Security Research independently confirmed the `arrayref` / `proc-macro1` incident and **expanded the compromised-crate list to three parent crates** — all published from the same crates.io owner account (`droundy`) and all silently pulling in the `proc-macro1` typosquat as a transitive dependency:

| Crate | Compromised version | ~Downloads | Last clean pin | JFrog Xray ID |
| --- | --- | --- | --- | --- |
| `arrayref` | 0.3.10 | 245M | `arrayref = "=0.3.9"` | `XRAY-1058267` |
| `internment` | 0.8.7 | 14.4M | `internment = "=0.8.6"` | `XRAY-1058269` |
| `append-only-vec` | 0.1.9 | 4.5M | `append-only-vec = "=0.1.8"` | `XRAY-1058268` |
| `proc-macro1` (carrier) | 1.0.107 | — | remove entirely | `XRAY-1058266` |

- **The carrier is still `proc-macro1` 1.0.107.** JFrog's mechanics match StepSecurity's: the parent crates only *add a dependency* on the typosquat; all malicious runtime lives in `proc-macro1`'s `build.rs` (split-base64 C2 fragments, accept-all TLS, `ureq` / `rustls` / `base64` build-deps, detached stage-2 spawn).
- **The stage-2 endpoints were down at JFrog's time of writing** (`23.254.165.112:9089` and `:443` did not respond), so the remote payload had not been recovered as of the JFrog post. JFrog's explicit caveat: inactive URLs do **not** mean the attack failed — with `arrayref` at ~245M lifetime downloads, any `cargo build` against a freshly resolved lockfile inside the window was enough to execute whatever the operator served.
- **Remediation (JFrog):** validate `Cargo.lock` / vendored trees for the three compromised versions or any `proc-macro1` entry; remove them and pin to the clean versions above; regenerate lockfiles from trusted crates.io metadata after the malicious versions were deleted; hunt for `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`; block `23.254.165.112` on ports 9089 and 443; and rotate credentials from any host/CI that ran Cargo against an affected lockfile (treat confirmed execution as full host compromise).
- **JFrog Curation** customers with an immaturity policy in place were fully protected: all hijacked packages were flagged the same day.
- The `proc-macro1` author field is spoofed as `David Tolnay <rchaitm@gmail.com>` with repository `https://github.com/dtolnay/proc-macro1` — corroborating StepSecurity's `dtolney` impersonation persona.

## StepSecurity August 20 technical write-up: runtime reproduction and stage-2 persistence

On **August 20, 2026**, StepSecurity published the full technical write-up (with a live runtime reproduction using Harden-Runner) and flagged it as a developing story. It confirmed the JFrog scope (the same three `droundy` crates plus the `proc-macro1` carrier) and extended the record in three ways.

**Runtime reproduction.** StepSecurity ran a GitHub Actions workflow that checks out a project carrying `arrayref` 0.3.10 and runs a build step. In audit mode the only anomalous event was the build step's outbound connection to `23.254.165.112:9089` (flagged `Anomalous`, first-seen, never observed in prior runs) while every legitimate Rust build destination (`github.com`, `index.crates.io`, `static.crates.io`, `docs.rs`, `static.rust-lang.org`) was allowed. The step and job both concluded **success** — from the Actions UI alone, nothing looks wrong. The process tree showed the fetched binary continuing to run after the build script exited, matching the dropper's detached `spawn` + `std::mem::forget(child)`. After the payload host was added to the global block list, a second identical run was denied at the egress layer (`AttackBlocked`, reason `COMPROMISED_ARRAYREF_C2_IP`) with no workflow changes — demonstrating that destination-based egress control catches this attack class even for a release that was only malicious for 86 minutes. Both public runs are inspectable (Harden-Runner runs 32352102796 and 32352856981).

**Blast-radius figures.** Per the write-up: combined all-time downloads of the three compromised crates are **~264M**; `arrayref` alone has **406 dependent crate versions** directly; the decoy was staged **~5 hours** before weaponization; and the exposure windows were **86 / 90 / 107 minutes** per crate (07:11–09:25 UTC overall). `internment` itself depends on `append-only-vec`, so a single `internment` resolve during the window could pull two poisoned crates into one tree.

**Stage-2 persistence (third-party reports, not independently reproduced).** A developer infected on Linux reported the post-execution behavior: the payload created `$HOME/.config/AzureKits` and `$HOME/.config/ServiceKit`, dropped executables named **`MonoService`** and **`MonoXpc`**, registered a **systemd service** to restart itself, and connected to `23.254.167.216`. A separate researcher in the same thread reported `23.254.167.107` in use for C2. These are third-party reports StepSecurity has not independently reproduced, but they are consistent with the dropper's design and worth hunting for now. The stage-2 binaries (`rust-crate_0.1.0` … `_0.4.0`) were not recoverable from public sources at the time of writing.

**Provenance red flags (corroborated).** `arrayref` is a zero-dependency utility with no use for a proc-macro library; `proc-macro1` is imported nowhere — a same-day typosquat dependency in a zero-dependency crate's manifest is a high-confidence indicator of a compromised release by itself. No commit, tag, or release for `arrayref` 0.3.10 exists in the owner's GitHub history, and the `droundy` account and the canonical `droundy/arrayref` repo returned 404 — the publish came from the owner's crates.io credentials (a long-lived API token or stolen session), not the project's normal workflow. The Rust Security Response Team assesses the owner's machine or credentials as compromised, not that the owner acted maliciously.

**Detection and defense deltas from the write-up.**
- **Lockfile is the decisive check, not the registry.** Because the malicious versions were *deleted* (not merely yanked) and the RustSec advisories were still pending, `cargo audit` reports clean for a project that pinned a poisoned version. A warm `~/.cargo/registry` cache or a committed `vendor/` directory keeps building the payload offline even though the version no longer exists in the registry.
- **The `yank` burst was the delivery channel.** Yanking `arrayref` 0.3.5–0.3.9 makes Cargo print a "yanked in registry" warning on every subsequent build; the "responsible" fix — `cargo update -p arrayref` — resolves to the single non-yanked modern release, `0.3.10`. The attacker turned the registry's own safety feature into the delivery mechanism. (crates.io has since reversed all of these yanks.)
- **Cooldown / release-age policies** (only admit crate versions older than N days) would have neutralized this attack, mirroring the `axios@1.14.1` lesson.
- **Publishing hygiene:** one stolen long-lived crates.io token was enough to poison three crates in 23 minutes; scoped, short-lived tokens and OIDC trusted-publishing flows remove that surface.

## Wiz stage-2 implant analysis and DPRK infrastructure overlap

On **August 20, 2026**, Wiz Research published a stage-2 analysis and a DPRK-overlap assessment (Rami McCarthy / Benjamin Read). Wiz recovered and analyzed the implant from Google Threat Intelligence, filling the gap StepSecurity flagged (stage-2 binaries not publicly recoverable at that time). Treat this as vendor analysis of the same campaign; the DPRK overlap is infrastructure correlation, not operator attribution.

**Stage-2 implant capabilities (Wiz).**
- Beacons to C2 via **HTTPS POST to `/49890878`**, exfiltrating host info and stolen credential data as Base64-encoded JSON.
- **Browser credential-store reads:** enumerates saved logins and extension settings in Chrome, Brave, and Edge profiles by querying their SQLite stores directly. Wiz's edit clarifies that the queries **enumerate** saved logins — they do not retrieve the encrypted credential material. (Wiz's earlier wording that "browser credentials were stolen" was corrected.)
- **Persistence:** Windows Registry Run key, macOS LaunchAgent, or Linux systemd user service.
- **Commands:** `kill` (terminate), `minicfg` (reconfigure C2 and beacon interval), `startup` (install persistence), `runscript` (download and execute PowerShell or shell scripts, synchronously or in background).
- **DGA fallback:** if the primary C2 is unreachable, the implant generates 10 algorithmic `.com` domains every 5 days; the relevant domains did not appear registered at Wiz's time of writing.
- **Crypto:** configuration encrypted with AES-128-GCM under the hardcoded key `i am botking`; commands authenticated via an embedded RSA-2048 private key.
- **Prevalence (Wiz):** `arrayref` is present in over 35% of all Wiz environments and ~75% of Rust-present environments (any version), which raises the blast-radius estimate beyond the dependency-tree figures.
- **Wiz hashes:** SHA1 `f4767ad92cb61401fd69139cade563501c39b991` (Linux stage-2, `rust-crate_0.1.0`), `fc0fdb978eac72f4484b48db058e4473f1bc516e` (Windows stage-2, `rust-crate_0.2.0`), `ff7e20cf642346bf893f1eca808df82035bb53d0` (macOS arm64 stage-2, `rust-crate_0.4.0`); SHA256 values for the three `.crate` files match the StepSecurity/JFrog record.

**DPRK infrastructure overlap (Wiz's assessment, with its corroboration chain stated).**
- **Shared C2 endpoint pattern:** the arrayref payloads beacon to `/49890878`, the same request path used in the **Mastra** npm campaign that **Microsoft attributes to DPRK / Sapphire Sleet**. The arrayref beacon IP also shares an SSL issuer (`WIN-A6QF8AHPQH1\Administrator@WIN-A6QF8AHPQH1`) with `23.254.167[.]13`, another Mastra-campaign IP.
- **Victim-reported infrastructure:** a victim's reported C2 traffic to `23.254.167[.]216` (one of the two RustSec-thread third-party reports above) also appears in **Google Cloud Threat Intelligence's analysis of UNC1069's axios npm attack**, which **Mandiant links to North Korea**.
- **Preferred host:** both campaigns generally use the same `23.254.164.0/23` Hostwinds LLC range.
- **Interpretation:** infrastructure overlap of this shape (shared beacon path, shared SSL issuer, shared /23, victim-reported IP appearing in a named DPRK campaign) is strong correlation evidence but does not by itself establish that the arrayref operator is a DPRK group. The wiki's `easy-day-js` / Mastra infrastructure record already notes the same Hostwinds provider class. Until a named-actor assessment or takedown links the two operations, track this as "substantial DPRK-campaign infrastructure overlap per Wiz."

**Wiz remediation additions.** Check `Cargo.lock` across all repositories and the local `~/.cargo/registry/cache` for the malicious versions or any of the six attacker-controlled crate names; treat any host that built an affected project as compromised (rotate all reachable credentials, tokens, CI secrets, and signing keys; rebuild artifacts produced after exposure from clean sources); reset passwords stored in the affected host's Chrome/Brave/Edge profiles and revoke associated sessions (enumeration exposure, even without encrypted-material retrieval); remove `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`, and any unrecognized systemd user services / `HKCU` Run entries / LaunchAgents; and review build-time dependency additions — a new networking build-dependency (`ureq` / `reqwest` / `rustls`) in a crate that has no reason to make network calls is a high-confidence tripwire.

## RustSec advisories published and the Rust security team's official account

On **August 21, 2026** the RustSec advisory-db published **seven `malicious`-category advisories** for this incident (first batch committed 2026-08-20 15:46 UTC; a follow-up commit on 2026-08-21 06:28 UTC incorporated updated `arrayref`-usage information), resolving the "pending RustSec advisories" watch item that had kept `cargo audit` blind to the poisoned versions:

| Advisory | Crate | Category note | Unaffected / state |
| --- | --- | --- | --- |
| `RUSTSEC-2026-0260` | `arrayref` 0.3.10 | malicious dependency on `proc-macro1` | `<= 0.3.9` |
| `RUSTSEC-2026-0266` | `internment` 0.8.7 | malicious dependency on `proc-macro1` | `<= 0.8.6` |
| `RUSTSEC-2026-0262` | `append-only-vec` 0.1.9 | malicious dependency on `proc-macro1` | `<= 0.1.8` |
| `RUSTSEC-2026-0265` | `proc-macro1` (all versions) | build script downloading a malicious payload; crate removed, accounts locked | `expect-deleted` |
| `RUSTSEC-2026-0264` | `proc-macro-en` (single version) | same build script as `proc-macro1`; same supply-chain attack | `expect-deleted` |
| `RUSTSEC-2026-0259` | `arone` (7 versions, last published 2026-08-18) | malicious build script; removed 2026-08-20, account locked | `expect-deleted` |
| `RUSTSEC-2026-0261` | `aronenao` (11 versions, last published 2026-08-18) | malicious build script; account locked | `expect-deleted` |

- `RUSTSEC-2026-0263` covers `tinymember` (2 versions, 27 total downloads, no dependents on crates.io) as **removed for affiliation only** — it "did not directly contain malicious code" but shared the owner account with `arone` / `aronenao`. `aovine` (deleted with the other attacker crates) has **no advisory** as of this update.
- The Rust Security Response Team's post on the Rust blog (2026-08-20, Manish Goregaokar on behalf of security-response) is the official account. It confirms the registry mechanics (report received 2026-08-20 07:15 UTC; `proc-macro1` and the associated crates `proc-macro-en`, `aovine`, `arone`, `aronenao`, `tinymember` deleted; the maliciously republished `arrayref`, `internment`, and `append-only-vec` versions removed and the maliciously-yanked clean versions un-yanked; publishing accounts locked), and makes three points the vendor write-ups had left open:
  - **The `droundy` owner is not believed to be malicious** — "their computer or credentials are likely compromised," and the team was attempting to contact them. The owner's machine or credentials are the compromise vector, consistent with the stolen-token / long-lived-credential assessment in the StepSecurity write-up.
  - **Exposure figure:** `arrayref` 0.3.10 was downloaded **2,285 times** during its 86-minute window, "less than 10% of `arrayref` download traffic across all versions, as most users had older versions in their lockfiles" — a concrete lower bound for build-execution corroboration.
  - **Official cache-hunt command:** the blog publishes the canonical `find ~/.cargo/registry/cache` sweep for all seven poisoned/attacker crate names, matching the Defender-priorities item 4 above.
- With the advisories published, **`cargo audit` can now flag lockfiles pinned to the poisoned versions** (and vendor checkouts still carrying them); the lockfile `grep` and cache-purge steps remain the primary controls because deleted versions still build from warm caches.
- No CVE has been assigned to any of the seven advisories; this remains a registry/attack campaign, not a product vulnerability. No CISA KEV entry observed.

## Defender priorities
1. **Check lockfiles everywhere:** `grep -A2 'name = "arrayref"' Cargo.lock`. Version `0.3.10` (or `internment` 0.8.7 / `append-only-vec` 0.1.9), or any entry named `proc-macro1`, `proc-macro-en`, `aovine`, `arone`, `aronenao`, or `tinymember` at any version, means the payload ran on that machine — CI runners included. One command: `grep -rEn 'proc-macro1|proc-macro-en|aovine|arone|aronenao|tinymember|arrayref.*0\.3\.10|internment.*0\.8\.7|append-only-vec.*0\.1\.9' --include=Cargo.lock --include=Cargo.toml .`
2. **Artifact hunt:** look for `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`, and stage-2 binaries `rust-crate_0.x.0` in build directories; alert on egress to `23.254.165.112` (ports 9089 and 443), the reported stage-2 C2s `23.254.167.107` and `23.254.167.216` (ideally the whole `23.254.165.0/24` and `23.254.167.0/24` Hostwinds ranges), and on `hwsrv-798836.hostwindsdns.com`.
3. **Stage-2 persistence hunt (Linux):** `$HOME/.config/AzureKits` and `$HOME/.config/ServiceKit` directories, executables named `MonoService` or `MonoXpc`, and any unexpected systemd service that restarts them (third-party reports — verify before alerting, but hunt while the indicators are fresh).
4. **Purge caches and vendored copies:** `find ~/.cargo/registry/cache -type f \( -name 'arrayref-0.3.10.crate' -o -name 'internment-0.8.7.crate' -o -name 'append-only-vec-0.1.9.crate' -o -name 'proc-macro1-*.crate' -o -name 'proc-macro-en-*.crate' -o -name 'aovine-*.crate' -o -name 'arone-*.crate' -o -name 'aronenao-*.crate' -o -name 'tinymember-*.crate' \)` — plus CI caches and container images baked with a warm registry. A deleted version still builds from a warm cache; with the RustSec advisories now published, `cargo audit` flags lockfiles pinned to a poisoned version, but not caches or vendored trees that outlive it.
5. **If evidence is found:** treat the host as compromised — rotate every credential, token, and signing key reachable from it (SSH keys, cloud tokens, crates.io/API tokens, GPG/supply-chain signing keys, CI secrets), and **rebuild artifacts produced during the 07:11–09:25 UTC window from clean sources** (tainted binaries may be shipping to users). Audit build logs from that window for jobs that created or updated lockfiles, and review what each affected ephemeral runner could access.
6. **If clean:** pin `arrayref = "=0.3.9"`, `internment = "=0.8.6"`, and `append-only-vec = "=0.1.8"` in lockfiles (the malicious yanks have been reversed, so these are the normal, warning-free choices again — but verify the resolved version in the lockfile rather than trusting the absence of a warning), and never resolve yank warnings by blind upgrades.
7. **CI hardening:** enforce committed `Cargo.lock` in pipelines (`cargo build --locked`; never `cargo update` or fresh resolution on ephemeral runners), consider registry-provenance / attestation checks on dependency resolution for Rust builds, and mirror npm `min-release-age` / cooldown controls — a release-age policy would have made this a non-event.
8. **Watch the crates.io/RustSec follow-through:** RustSec advisories RUSTSEC-2026-0259 through -0266 are now published (see [the RustSec section](#rustsec-advisories-published-and-the-rust-security-teams-official-account)); remaining open items are `droundy` account recovery or handover, any new `arrayref` release, follow-on publications under the `dtolney` persona (including `aovine`, which still has no advisory), a CVE assignment, and stage-2 payload recovery from public sources.

## Assessment limits
- As of this update the record rests on StepSecurity's August 20 technical write-up (with live runtime reproduction), JFrog Security Research's independent confirmation, Wiz Research's stage-2 analysis and DPRK-overlap assessment, the RustSec advisory-db's seven published advisories, the Rust security team's official blog account, and crates.io audit/index forensics. No named-actor attribution is asserted by any vendor; the DPRK overlap is infrastructure correlation (shared beacon path `/49890878`, shared SSL issuer, shared `23.254.164.0/23` Hostwinds range, and a victim-reported C2 IP in Mandiant's UNC1069 axios analysis). Treat the `dtolney` persona and `rchaitm@gmail.com` metadata as attacker-fabricated, not as operator identity. The Rust security team's "owner not acting maliciously; computer or credentials likely compromised" assessment is the strongest public statement of the compromise vector.
- The stage-2 binaries were not recoverable from public registry sources; Wiz obtained and analyzed them from Google Threat Intelligence. Wiz's browser-credential finding is an **enumeration** of saved logins and extension settings (Chrome/Brave/Edge SQLite stores), not retrieval of encrypted credential material — the article was corrected on that point after publication.
- Stage-2 persistence artifacts (`AzureKits` / `ServiceKit` directories, `MonoService` / `MonoXpc` executables, systemd service, and the `23.254.167.107` / `23.254.167.216` C2s) come from **third-party reports in the RustSec thread**, not from independently reproduced samples. Hunt them, but do not treat them as confirmed vendor findings.
- The `internment` 0.8.7, `append-only-vec` 0.1.9, and `proc-macro-en` `.crate` files were hard-deleted before they could be archived, so their checksums are unrecoverable; stage-2 SHA1 hashes are per Wiz.
- crates.io deletion/lock state (all malicious versions deleted; attacker accounts and `droundy` locked; malicious yanks reversed) is as reported at publication time and may change.
- Blast-radius figures (~264M combined all-time downloads; 406 dependent crate versions; 86 / 90 / 107-minute windows) are per StepSecurity's investigation; Wiz's environment-prevalence figures (`arrayref` in >35% of all environments, ~75% of Rust-present environments) are a separate, coarser estimate.
- No CISA KEV entry or CVE assignment observed for this incident as of this scan; it is a registry incident, not a product vulnerability.

## Related pages
- [Mastra / easy-day-js npm scope compromise](mastra-easy-day-js-npm-scope-compromise.md) — the Microsoft-attributed DPRK/Sapphire Sleet npm campaign whose C2 path and Hostwinds range overlap this incident per Wiz
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md) — the axios maintainer-account compromise campaign whose GCTI/Mandiant UNC1069 analysis (per Wiz) includes `23.254.167.216`
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md) — cooldown / registry-drift controls with a direct analog here (pin `arrayref`, don't follow yank-bursts)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md) — npm preinstall + IDE-hook supply-chain tradecraft; same "build-time execution" primitive, different registry
- [SleeperGem RubyGems maintainer-account compromise](sleepergem-rubygems-maintainer-account-compromise.md) — dormant-maintainer account takeover across the RubyGems ecosystem
- [Miasma – The Spreading Blight (Mini Shai-Hulud cross-ecosystem wave)](mini-shai-hulud-npm-pypi-worm-campaign.md) — cross-ecosystem package compromise patterns, including Go modules

## Sources
- StepSecurity: [Rust Supply-Chain Attack: arrayref 0.3.10 and the proc-macro1 Typosquat Execute a Remote Payload at Build Time](https://www.stepsecurity.io/blog/arrayref-rust-crate-supply-chain-attack) — August 20, 2026 (timeline, IOCs, hashes, runtime reproduction; developing story)
- JFrog Security Research: [Compromised Rust crates on crates.io silently execute malware at build time](https://research.jfrog.com/post/arrayref-proc-macro1-crates-io/) — August 20, 2026 (independent confirmation; `internment` / `append-only-vec` scope, Xray IDs, clean-version pins)
- Wiz Research: [Rust Supply Chain Attack on arrayref: Significant Overlap with DPRK Campaigns](https://www.wiz.io/blog/rust-supply-chain-attack-on-arrayref-significant-overlap-with-dprk-campaigns) — August 20, 2026 (stage-2 implant analysis from Google Threat Intelligence samples; DPRK infrastructure overlap: `/49890878` beacon path and Hostwinds range with the Mastra/Sapphire Sleet campaign, and `23.254.167[.]216` in GCTI's UNC1069 axios analysis; environment-prevalence figures)
- RustSec advisory-db: report filed 2026-08-20 07:54 UTC (referenced by StepSecurity); advisories `RUSTSEC-2026-0259` (arone), `RUSTSEC-2026-0260` (arrayref), `RUSTSEC-2026-0261` (aronenao), `RUSTSEC-2026-0262` (append-only-vec), `RUSTSEC-2026-0263` (tinymember, affiliation), `RUSTSEC-2026-0264` (proc-macro-en), `RUSTSEC-2026-0265` (proc-macro1), `RUSTSEC-2026-0266` (internment) — published 2026-08-20/21, all `malicious`
- Rust blog (Security Response): [Supply chain attack on arrayref](https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref) — August 20, 2026 (official registry account; owner-compromise assessment; 2,285-download exposure figure; canonical `~/.cargo/registry/cache` hunt command)
