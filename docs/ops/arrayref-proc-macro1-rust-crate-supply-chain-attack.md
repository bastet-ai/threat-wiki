# Rust supply-chain attack: arrayref 0.3.10 and the proc-macro1 typosquat

## Summary
On **August 20, 2026**, a short but high-blast-radius **Rust crates.io supply-chain attack** compromised the foundational `arrayref` crate (v0.3.10, published **07:15 UTC**) and pulled in a **typosquatted `proc-macro1` crate** (v1.0.106 staging / v1.0.107 payload) impersonating the ubiquitous `proc-macro2`. The malicious code lives entirely in `proc-macro1`'s `build.rs`: any machine that **compiles** a project resolving the dependency — without ever calling the crate — downloads a platform-specific stage-2 binary from a Hostwinds VPS and executes it, detached from the Cargo build.

The exposure window was roughly **86 minutes** (07:11 to ~08:41 UTC). crates.io deleted `proc-macro1` at 08:03 and removed `arrayref` 0.3.10 from the index at 08:41. The legitimate `droundy` maintainer account (in good standing since 2009) is **presumed compromised**; the attacker's `dtolney` persona (impersonating `proc-macro2` author David Tolnay) was fabricated the same morning with forged author metadata (`David Tolnay <rchaitm@gmail.com>`). StepSecurity published the first detailed analysis and flags it as a **developing story** — the stage-2 payload's full behavior is still under analysis.

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

## Why this matters
- **`arrayref` is a load-bearing crate with ~245 million all-time downloads.** Reverse-dependency reach documented by StepSecurity includes `tiny-skia` → `sctk-adwaita` → `winit` (i.e., under egui/eframe, iced, and most Rust GUI apps), plus `blake3`, `blake2b_simd`/`blake2s_simd`, `revm-precompile` (Ethereum), and `solana-runtime`/`spl-token` (Solana). Any CI job or developer build that resolved `arrayref ^0.3` fresh during the window ran the payload with that user's privileges.
- **Build-time execution is the primitive.** No import, no function call — `build.rs` runs at compile time. This mirrors the `npm postinstall` / `node-gyp binding.gyp` / PyPI `.pth` patterns already documented in the wiki, but in the Rust ecosystem, where `Cargo.lock` pinning is the primary defense.
- **The yank burst was deliberate social pressure.** Within the same minute as the malicious `arrayref` 0.3.10 publication, versions 0.3.5 through 0.3.9 were yanked in a scripted burst (~4 seconds apart) so that Cargo's "yanked version" warning nudges lockfile-holders toward upgrading into the trap.
- **Fresh-resolution window matters more than version numbers.** Because `Cargo.lock` pins exact versions, only projects that *re-resolved* dependencies (new lockfiles, `cargo update`, CI runners without lockfiles, `cargo add`) during ~07:11–08:41 UTC were exposed.
- **Attribution is not yet asserted.** This is a credential-theft / account-compromise + impersonation tradecraft event; StepSecurity does not link it to a named actor as of the initial post.

## Attack chain (timeline, UTC)
1. **01:17** — GitHub account `dtolney` created, impersonating David Tolnay (`proc-macro2` author).
2. **01:25** — matching crates.io account `dtolney` (id 438608) created.
3. **01:55** — `proc-macro1` **1.0.106** published: a clean verbatim copy of `proc-macro2` (staging; builds a plausible benign crate under the squatted name).
4. **07:11** — `proc-macro1` **1.0.107** published, adding build dependencies (`base64`, `rustls`, `ureq`) no genuine proc-macro library needs, plus the malicious `build.rs`.
5. **07:15** — `arrayref` **0.3.10** published from the legitimate owner account `droundy`, adding its first dependency in the crate's decade-long history: `proc-macro1 ^1.0.107`. In the same minute, `arrayref` 0.3.5–0.3.9 are yanked in a scripted burst.
6. **07:54** — incident reported to RustSec advisory-db and the Rust security team.
7. **08:03** — crates.io deletes `proc-macro1`.
8. **08:41** — crates.io removes `arrayref` 0.3.10 from the index. (~86-minute exposure window.)

## How the payload works
- `proc-macro1` 1.0.107's `build.rs` **reassembles infrastructure from base64 fragments**: payload host `https://23.254.165.112:9089/` and C2 endpoint `23.254.165.112:443`.
- It fetches a **stage-2 binary over TLS with certificate validation disabled** (accept-all verifier), choosing among `rust-crate_0.1.0` … `rust-crate_0.4.0` by target platform.
- Drops to `/tmp/rust-setup` (Unix) or `%TEMP%\rust-setup.ps1` via a hidden `wscript.exe` launcher (`rust-setup-launch.vbs`) on Windows, then **spawns it detached** with the C2 address as `argv[1]`, carefully escaping Cargo's job object so the build completes normally.
- The library code is genuine `proc-macro2`, so builds succeed and the infection is invisible in normal output.
- Payload host resolves to a **Hostwinds VPS** (`hwsrv-798836.hostwindsdns.com`) — the same provider class seen in Mastra / `easy-day-js` npm RAT infrastructure.

## Indicators of compromise
- **Network:** `23.254.165.112:9089` (payload host), `23.254.165.112:443` (C2), `hwsrv-798836.hostwindsdns.com`
- **Files:** `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`
- **Binaries:** `rust-crate_0.1.0` / `_0.2.0` / `_0.3.0` / `_0.4.0`
- **Crates:** `arrayref` 0.3.10, `proc-macro1` 1.0.106 and 1.0.107
- **Accounts:** `dtolney` (crates.io id 438608, impersonator); `droundy` (legitimate `arrayref` owner, presumed compromised; associated GitHub account returning 404 at time of writing)
- **Email:** `rchaitm@gmail.com` (forged author metadata)
- **SHA-256:**
  - `25ad700976873c76af785cb99b33c48db7df8b81f21d1e9e06b3676b9a9373ae` — `arrayref-0.3.10.crate`
  - `61198155da51b838772eecf5bfaac6cbc4dcc388dccc56658fc28a8e831b34d4` — `proc-macro1-1.0.107.crate`
  - `b5c1b5b0763a8809a644a8f92224653f0aca623a98eecc714d27f74b80fbe436` — `proc-macro1-1.0.106.crate`

## Defender priorities
1. **Check lockfiles everywhere:** `grep -A2 'name = "arrayref"' Cargo.lock`. Version `0.3.10`, or any entry named `proc-macro1`, means the payload ran on that machine — CI runners included.
2. **Artifact hunt:** look for `/tmp/rust-setup`, `%TEMP%\rust-setup.ps1`, `%TEMP%\rust-setup-launch.vbs`, and stage-2 binaries `rust-crate_0.x.0` in build directories; alert on egress to `23.254.165.112` ports 9089 or 443 and on `hwsrv-798836.hostwindsdns.com`.
3. **If evidence is found:** treat the host as compromised — rotate every credential, token, and signing key reachable from it (CI secrets, GPG/supply-chain signing keys, cloud credentials in env), and **rebuild artifacts produced after exposure from clean sources** (tainted binaries may be shipping to users).
4. **If clean:** pin `arrayref = "=0.3.9"` in lockfiles and never resolve yank warnings by blind upgrades. Note that Cargo currently resolves `arrayref ^0.3` to the 2017-era 0.3.4 until the maintainer situation is resolved — audit any build that unexpectedly downgrades.
5. **CI hardening:** enforce committed `Cargo.lock` in pipelines (never `cargo update` or fresh resolution on ephemeral runners), and consider registry-provenance / attestation checks on dependency resolution for Rust builds, mirroring npm `min-release-age` / cooldown controls.
6. **Watch the crates.io/RustSec follow-through:** `arrayref` is back under compromised-maintainer question; expect a version-bump, maintainer handover, or re-publish decision, and re-scan after any new `arrayref` release.

## Assessment limits
- Single-source analysis as of the initial scan: StepSecurity blog post (August 20, 2026), explicitly marked a **developing story, actively investigated** with the stage-2 payload behavior still being analyzed. No named-actor attribution is asserted; treat the `dtolney` persona and `rchaitm@gmail.com` metadata as attacker-fabricated, not as operator identity.
- crates.io deletion state (`proc-macro1` fully removed; `arrayref` 0.3.10 removed from index; 0.3.5–0.3.9 yanked) is as reported at publication time and may change.
- Blast-radius figures (~245M all-time downloads, 86-minute window) are per StepSecurity's investigation; independent reverse-dependency validation has not yet been published.
- No CISA KEV entry or CVE assignment observed for this incident as of this scan; it is a registry incident, not a product vulnerability.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md) — cooldown / registry-drift controls with a direct analog here (pin `arrayref`, don't follow yank-bursts)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md) — npm preinstall + IDE-hook supply-chain tradecraft; same "build-time execution" primitive, different registry
- [SleeperGem RubyGems maintainer-account compromise](sleepergem-rubygems-maintainer-account-compromise.md) — dormant-maintainer account takeover across the RubyGems ecosystem
- [Miasma – The Spreading Blight (Mini Shai-Hulud cross-ecosystem wave)](mini-shai-hulud-npm-pypi-worm-campaign.md) — cross-ecosystem package compromise patterns, including Go modules

## Sources
- StepSecurity: [Rust Supply-Chain Attack: arrayref 0.3.10 and the proc-macro1 Typosquat Execute a Remote Payload at Build Time](https://www.stepsecurity.io/blog/arrayref-rust-crate-supply-chain-attack) — August 20, 2026 (timeline, IOCs, hashes, remediation; developing story)
- RustSec advisory-db: report filed 2026-08-20 07:54 UTC (referenced by StepSecurity)
