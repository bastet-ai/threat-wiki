# RubyGems 24-gem crypto-utility fleet — the `45.138.12.177` C2 RETURNS under fresh names: 24 gems pushed in an 83-second scripted window (Oct 11 06:52:40–06:54:02Z), every one `0.9.1`, every `extconf.rb` a base64 double-fork `/bin/sh`-over-TCP reverse shell to **the SAME `45.138.12.177:8089`** the Wallet Guard wgkit fleet used — with the `bitcoin_rpc_lite_native` makefile name and the Oct-5 counter-forensics gates (CI / ephemeral-host / generated-user / analysis-path / uptime>30 min / dev-signals) baked in as shipped defaults — and for the FIRST TIME on this ledger a RubyGems malware fleet dual-advised 24/24 from day one (OSV `MAL-2026-17779`–`17802` + a 24-record same-second GHSA batch 15:31:13Z) while every gem stays LIVE and the C2 box itself has gone fully DARK

## Tags
- ops
- supply chain attack
- RubyGems
- malicious-package
- reverse-shell
- native-extension
- extconf-backdoor
- crypto-theft-costume
- wallet-costume
- sandbox-evasion
- anti-analysis-gates
- 45-138-12-177
- reqthrottle-lineage
- OSV malware stream
- GHSA-malware-lane
- registry-differential
- dead-C2-rearm-risk
- this-wiki-forensics

## What it is

One-hundred-and-forty-eighth-sweep stream move: OSV `+44 CONTIGUOUS MAL-2026-17759`–`17802` (the largest single-sweep move since the hundred-and-sixteenth's +31), of which **`MAL-2026-17779`–`17802` are TWENTY-FOUR RubyGems records**, every one an `amazon-inspector` source, published 13:45:11–14:01:05Z. The 24 names, all version `0.9.1`, all `version_created_at` inside **83 seconds (06:52:40–06:54:02.4Z, this wiki's registry-API pull)**:

`airdrop-eligibility-check`, `block-explorer-api`, `btc-fee-estimator`, `crypto-tax-export`, `defi-yield-calculator`, `dex-router-abis`, `erc20-approve-audit`, `eth-gas-oracle`, `evm-tx-decoder`, `gas-refuel-bridge`, `hd-wallet-generator`, `mev-sandwich-detect`, `multichain-rpc`, `nft-metadata-resolver`, `perp-funding-rates`, `seed-phrase-validator`, `sol-mint-utils`, `staking-apr-fetcher`, `ton-jetton-tools`, `tron-trc20-utils`, `wallet-balance-scanner`, `wallet-hd-derive`, `web3-signer-kit`, `xrp-ledger-utils`.

Every `authors` field follows the same template (`<prefix> maintainers` — `hd maintainers`, `web3 maintainers`, `wallet maintainers`, …) and every info line follows `Lightweight, dependency-free helpers for <prefix> …` = one scripted generator, one naming grammar: **pure crypto-utility neologisms — no typosquats, no lookalikes of real gems** (the Oct-4/5 fleet squatted `bitcoin-rpc-lite`/`keccak`-class names; this wave names nothing that exists, so `gem install` collisions come from search-ads and LLM autocomplete on plausible tooling names, not from typos).

## This wiki's artifact forensics (`hd-wallet-generator-0.9.1.gem`, sha256 `8fe9f4d0abaf37936e3653de0bdf4b487b5f9f9de1c794592332f31e930a80bd`, pulled and read WITHOUT execution)

The gem ships no native source. `ext/hd_wallet_generator/extconf.rb` is a five-gate anti-analysis wrapper around the spawn:

1. `in_ci?` — refuses if any of `CI GITHUB_ACTIONS TRAVIS JENKINS_URL GITLAB_CI CODESPACES` is set.
2. `ephemeral_host?` — refuses on empty/`instance`/`localhost` hostnames or hostnames matching `uvm|firecracker|sandbox|vagrant|fc[_-]?vm`.
3. `generated_user?` — refuses `uA\d+` users and `sandbox|tester|analys|scanner` substrings.
4. `analysis_path?` — refuses cwd under `/opt/rubygems`, `/var/tmp`, `/tmp/`, `/private/var/tmp`, `/workspace/`.
5. `machine_age_ok?` — requires `/proc/uptime` > 1800 s, AND `dev_signals?` — requires the HOME dir to contain at least one of `.ssh`, `.gitconfig`, `.npmrc`, `.gem/credentials`, `.bundle` = **only real developer workstations pass**.

If every gate passes: base64 payload → `fork` → `Process.setsid` → second `fork` (full daemonize, stdio to NULL) → `sleep 1200 + rand(1200)` (**20–40 min randomized**, matching every OSV detail's wording) → `eval` of a plain-text TCPSocket reverse shell: `HOST, PORT = '45.138.12.177', 8089`, `/bin/sh` with bidirectional `IO.copy_stream` threads, 30 s reconnect loop. Then the file continues with a NORMAL `require 'mkmf'; create_makefile('bitcoin_rpc_lite_native')`.

**That makefile name is the smoking gun.** `bitcoin_rpc_lite_native` is the extension build-name the Oct-4/5 **Wallet Guard / wgkit fleet (account `reqthrottle_3474`, C2 `45.138.12.177:8089/:8090` + `:8092` stage)** used on its reverse-shell-family gems — recorded verbatim on [the Wallet Guard page](rubygems-wallet-guard-mitm-wgkit-crypto-theft-fleet-reqthrottle-october-2026.md). Same IP, same port, same `:8089`, same build-name, and the payload's evasion gates are EXACTLY the counter-forensics that page measured on Oct 5 (the four OSV-advised gems re-shipped `1.0.1` nine minutes after their advisories with sandbox/CI/uptime/dev-signals gates). The Oct-5 read — **this operator treats advisories as a patch-feed, not a stop signal** — is now measured one campaign later: the gates that were a same-day hot-fix response are the shipped defaults from version one of all 24 new names, plus two NEW gates this wiki had not seen on the old fleet (`generated_user?`, `analysis_path?`).

Recorded as strong same-operator/lineage evidence on five independent overlaps (C2 IP + port, makefile build-name, gate grammar, payload shape, randomized 20–40 min delay). Operator identity remains unproven in the formal sense; the `reqthrottle_3474` account itself is erased — this wave's publisher account is not yet extracted (RubyGems owners API does not expose it for these names; the templated `authors` field is not a username).

## The lanes: 24/24 dual-advised from day one — the exact inverse of the Oct-5 fleet

- **OSV:** 24/24 records, published 13:45–14:01Z = **~7 h publish-to-OSV** (Oct-5 fleet: 4/48 at capture, 42/48 posthumous after registry death).
- **GHSA:** a **24-record same-second batch at 15:31:12–14Z** (`GHSA-p4hf-p5fc-85p7`, `GHSA-9grv-7vv7-5ppj`, `GHSA-5wxm-jv9m-mw2r`, `GHSA-g92c-g6pm-wf38`, `GHSA-m6qx-67h3-wwrh`, `GHSA-94vm-385v-mjfj`, `GHSA-xqg7-h4h5-x6pf`, …, this wiki's listing-walk read) = full mirror **~8.5 h after publish**, no posthumous catch-up needed. The Oct-6 durable that "the malware-lane mirror thaws in catch-up bursts, not live-mirror cadence" now has its first same-day, complete, forward mirror at 24-name scale.
- **Registry action: NONE.** All 24 gems LIVE and installable at check (~8.6 h post-publish, dual-advised) = the advisory/action differential again, now with the belt-and-braces irony: the same grammar the advisory lanes could finally see end-to-end is the grammar whose registry state never moves. Compare the Oct-5 fleet: fully dead within hours of capture.
- `aliases` still `None` on sampled records (~1.5 h post-GHSA) = standing OSV-native join rule holds.

## The C2 has gone dark — armed-body, dead-rail

This wiki's same-check probes of the whole `45.138.12.177` rail: **`:8089` CLOSED, `:8090` CLOSED, `:8080/w` connection-fails (was `200 ARMED` at the Oct-6 ninetieth sweep), `:8092` connection-refused (eighth-plus).** The box that hosted the wgkit stage kit went silent sometime between Oct 6 and now. Every one of the 24 live gems contains a payload that, on any un-gated host after its 20–40 min randomized sleep, reconnect-loops to a **dead listener**. This is the GhostAction pattern re-crossed from the other direction: **beacons deployed on a dead C2 = the operator either lost the box or moved on — and the re-arm risk is that a re-deployed listener at the same IP:port silently resurrects 24 live packages' payloads with no package-side change.** Monitor list accordingly: any `45.138.12.177:8089` liveness return, any payload mutation on the 24 names (`0.9.1` is every version — a `0.9.2` or `1.0.0` is the re-arm vector), and whether `:8080/w`'s exfil endpoint re-appears on a new IP (the wgkit kit's collection rails were IP-pinned, so a new IP requires new packages — the grammar grep remains the durable hunt).

## Durable reads

1. **A C2 is a campaign asset, not a campaign artifact.** The operator lost/abandoned `45.138.12.177` and re-launched a fresh 24-name fleet ON THE SAME IP. Advisory consumers keying package names saw a brand-new campaign; infrastructure-keyed consumers see the same actor with 100% continuity. Hunt keys: the IP set (union across all observed campaigns), the makefile build-names (`bitcoin_rpc_lite_native`), the gate grammar (`machine_age_ok?` + `dev_signals?` + `analysis_path?`), the `20–40 min randomized sleep` shape, and the templated RubyGems metadata (`<prefix> maintainers` / `Lightweight, dependency-free helpers for <prefix>`).
2. **The Oct-5 "counter-forensics as shipped feature" read is confirmed one campaign later**: adversary patch velocity against public advisories is not episodic; assume every published evasion finding re-appears in the next wave's baseline.
3. **Mirror completeness ≠ enforcement.** 24/24 OSV + 24/24 GHSA within ~9 h — the best advisory-lane outcome this ledger has on a RubyGems fleet — and zero registry action at check. Advisory-keyed blocklists can now SEE this fleet completely; they still cannot stop it.
4. Anti-analysis gating inverted: the gates filter out scanners, sandboxes, CI and cloud builders, so **the measured install base understates real risk** (legit CI traffic installs harmlessly, real dev boxes pay). A `gem install` telemetry spike will NOT show the exposure; hostname-forensics (a `~/.python2`-class artifact does not exist here — the payload is in-memory + socket, hunt by process tree `sh`-over-TCP + outbound `:8089`) is the detection path.

## State at check (one-hundred-and-forty-eighth sweep, ~15:2x–15:5x UTC Oct 11)

24/24 gems LIVE `0.9.1` (this wiki's `/api/v1/gems/<name>.json` pulls, `version_created_at` 06:52:40–06:54:02Z); OSV 24/24; GHSA 24/24 (15:31:12–14Z); `aliases` None sampled; C2 all ports dead; `hd-wallet-generator-0.9.1.gem` sha256 `8fe9f4d0…` preserved by this wiki (the OSV detail text + this capture = the durable public record of the payload while the gems stay live).

**Monitor:** C2 return on `:8089`/`:8080` (resurrection risk on 24 live packages); any version beyond `0.9.1` on any of the 24 names (re-arm vector); registry enforcement arrival (first action on any name = differential clock start); `reqthrottle`-account re-registration attempts; a THIRD wave adopting these gates; whether RubyGems takes fleet-wide action retroactively like the Oct-5 death-ladder; `aliases` joins onto 17779–17802; the 24 publisher identities if owners-API detail ever surfaces.

## <a id="oct-11-purge-followup"></a>October 11 one-hundred-and-forty-ninth sweep follow-up (~17:2x–17:4x UTC): REGISTRY ACTION ARRIVED — ALL 24 GEMS PURGED ≈10–10.5 h AFTER PUBLISH, the soft-200 shell state again

Same-day follow-up check: every one of the 24 names now reads `404` at `/api/v1/gems/<name>.json` and at `/api/v1/versions/<name>.json`, and `gem fetch` routes (`/downloads/<name>-0.9.1.gem`) answer `403` — while the HTML page `/gems/<name>` still serves `200` with **"This gem is not currently hosted on RubyGems.org. Yanked versions of this gem may already exist."** The distinction is load-tested with a guaranteed-nonexistent control name, which instead draws Rails `Page not found`: these 24 are NAME-HOLDS with zero live versions, not erased names. This is the **bare-vs-soft-200 split** the predecessor page recorded on the Oct-5 death-ladder — RubyGems retroactively took fleet-wide action exactly as this page's monitor list predicted, ≈10 h post-publish and ≈1.5–2 h after this page's "all 24 LIVE" capture.

Durable updates to this page's reads:
1. **"Mirror completeness ≠ enforcement" gains its counter-time**: the mirror (OSV 13:45–14:01Z, GHSA 15:31Z) ran ~8.5 h; the purge landed ~10.3 h. On a RubyGems fleet the advisory lanes now PREDICT the enforcement window rather than replacing it — blocklists keyed to either feed get their lead time, and the registry does eventually move. The Oct-5 fleet died within hours of capture; this one lived through a full advisory cycle first. Watch whether the NEXT wave (if any) dies faster or slower — that delta is the enforcement-learning curve.
2. **The public artifact record now runs through the advisories + this wiki's capture**: with zero live versions, `hd-wallet-generator-0.9.1.gem` sha256 `8fe9f4d0…` (preserved here, no execution) + the 24 OSV detail texts are the durable public payload record — the same end-state the `test-react-app-in/out/way` trio reached in September (GHSA tarball-origin hashes as the only surviving artifact evidence).
3. **The resurrection risk mutates**: beacons are no longer installable, but already-infected real dev boxes still hold the 20–40 min reconnect loop against a dead `45.138.12.177:8089` (re-verified CLOSED this check, `:8090` closed, `:8080/w` dead). A re-deployed listener at that socket still resurrects every compromised host — the C2-return monitor matters MORE now, not less.
4. **Name-hold = re-registration surface**: the soft-200 shells mean the names are held, not released — per the ledger's holder-wave precedent, held hollow names are the classic resquat/comeback costume. Monitor any version appearing under these 24 names under a NEW publisher as strongly as a `>0.9.1` under the old.

Queue/state this check: OSV high-water HOLDS `17802` (`17803/04/05/10/20` `404`, controls `17779`/`17802` live); `aliases` still `None` on `17779` ≈2 h post-GHSA; KEV JSON-verified unchanged 2026.10.08/1,739; ossf queue `#1590`/`#1613`/`#1618–1621` all still open — zero merges since `#1611`.

## Related pages

- [RubyGems Wallet Guard / wgkit crypto-theft fleet (reqthrottle_3474)](rubygems-wallet-guard-mitm-wgkit-crypto-theft-fleet-reqthrottle-october-2026.md) — the same-C2 predecessor campaign, live stage-kit capture, and the counter-forensics observation this fleet ships as defaults
- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — the standing OSV-stream ledger; the +44 move of this sweep is recorded at the hundred-and-forty-eighth section
- [GhostAction workflow-injection mining campaign](ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md) — the same beacons-on-dead-infrastructure re-arm pattern from the GitHub Actions side
