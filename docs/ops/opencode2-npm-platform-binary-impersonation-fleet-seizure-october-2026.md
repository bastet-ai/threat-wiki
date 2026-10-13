# The `opencode2` nine-name platform-binary impersonation fleet: an 18-day, 67-version fake-project ladder on a real tool's binary name, ≈49k dl/wk, deleted with zero prior advisory and seized at the re-publish minute (this wiki forensics, Oct 13, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- typosquat
- brand-impersonation
- platform-binaries
- opencode
- opencode2
- osv
- ghsa
- seizure
- enforcement
- zombie-versions
- exposure-clock

## Summary

On Oct 13 `17:44:28–17:47:54Z` npm deleted-and-recreated **nine** registry docs in a ≈3.5-minute window — `opencode2` plus eight platform-suffixed siblings (`-windows-x64`, `-windows-arm64`, `-linux-x64`, `-linux-arm64`, `-linux-x64-musl`, `-linux-arm64-musl`, `-darwin-x64`, `-darwin-arm64`) — each re-created with the `0.0.0-stage` placeholder and `0.0.1-security` holder, while nine `critical` GHSAs minted inside **one second** at `17:47:30Z` and OSV mirrored all nine as the contiguous block `MAL-2026-17852`–`17860` (alias-at-birth, `database_specific` source `ghsa-malware`). Zero prior advisory existed for any of the names: like `@chatest/baileys` three sweeps ago, the GHSA/OSV pair was minted **at the seizure second**, not before it.

The costume is precise: `opencode2` is the **real binary name** of the OpenCode v2 CLI, which legitimately ships as `@opencode-ai/cli@beta` with platform-specific sibling packages (`@opencode-ai/cli-<platform>`); the attacker fleet squatting the bare `opencode2` + platform-grammar names sits exactly on the install path a user searching for the v2 preview would hit. Each doc carried a **67-version fake project ladder** (`2.0.16` → `2.7.53`) published continuously from **Sep 25 `19:21:41Z` to Oct 13 `12:49:58Z`** — 3–4 releases/day, minor/major bumps on a plausible cadence — the longest-running "live software project" tempo this ledger has seen on a seized name. Final rung `2.7.53` shipped `≈5 h` before the seizure. **Measured exposure print: Σ ≈49,021 downloads/week** across the nine names (npm downloads API, window Oct 5–11, captured at check while the names were already dead) — the largest single-wave exposure neutralized on this ledger since the Oct-12 Baileys 35-name wave (Σ ≈3,658 dl/wk), an order of magnitude larger.

## The seizure window (registry `time` blocks + advisory records, pulled 2026-10-13 ~19:2x UTC)

| Name | created/`0.0.0-stage` | `0.0.1-security` holder | holder vs GHSA `17:47:30Z` | last malicious rung |
|---|---|---|---|---|
| `opencode2` | 17:44:28.752 | 17:46:35.958 | −54 s | `2.7.53` 12:49:58 |
| `opencode2-darwin-arm64` | 17:44:34.722 | 17:46:41.636 | −49 s | `2.7.53` 12:45:51 |
| `opencode2-darwin-x64` | 17:44:41.936 | 17:47:51.465 | +21 s | `2.7.53` 12:48:20 |
| `opencode2-linux-arm64` | 17:44:47.884 | 17:46:56.753 | −34 s | `2.7.53` 12:47:16 |
| `opencode2-linux-arm64-musl` | 17:44:53.143 | 17:46:30.160 | −60 s | `2.7.53` 12:48:18 |
| `opencode2-linux-x64` | 17:44:58.367 | 17:45:55.056 | −95 s | `2.7.53` 12:48:26 |
| `opencode2-linux-x64-musl` | 17:45:04.622 | 17:47:12.823 | −18 s | `2.7.53` 12:48:26 |
| `opencode2-windows-arm64` | 17:45:11.145 | 17:46:07.309 | −83 s | `2.7.53` 12:49:43 |
| `opencode2-windows-x64` | 17:45:16.795 | 17:47:54.507 | +24 s | `2.7.53` 12:50:10 |

GHSA set (all `critical`, all published `17:47:30–31Z`, all `>= 0` whole-history scope): `GHSA-8w65-j2wh-mqv7` (`opencode2`), `GHSA-36mq-frp2-jc97`, `GHSA-pmv2-r2q9-rmg9`, `GHSA-xwcq-r6hw-mc5p`, `GHSA-cm8m-24p9-hh65`, `GHSA-3jr5-3qvm-r54h`, `GHSA-qx7m-vw4p-xv3j`, `GHSA-xr5m-85hf-27r5`, `GHSA-6x5j-r784-fx6j`. OSV mirror `MAL-2026-17852`–`17860`, every record alias-at-birth, published anchored to the GHSA second, every scope `introduced:0` with **no version list** — see "the `>= 0` scope shape" below.

Registry-state facts at check: every doc's `versions` map contains ONLY `0.0.0-stage` + `0.0.1-security` (maintainer `npm`); the survivor `time` block preserves all 67 phantom ladder entries (second-plus ledger instance of the survivor-block grammar after `@chatest`/`@yudzxml`); sampled tarballs `2.7.53`, `2.7.50`, `2.0.16` all `404` = zombie list reconfirmed as the only installability oracle; the stage/holder tarballs `200` (the npm machinery itself).

## Why this costume was chosen (durable read)

- **Binary-name squatting is the next namespace after scope/clone squatting.** The legit tool ships as `@opencode-ai/cli` (scope, defended) whose *command* is `opencode2` and whose platform executables follow the `-linux-x64` / `-darwin-arm64` / `-musl` suffix grammar. The fleet reproduced the command name + the platform grammar at the **bare-name** level, which no scope defense covers. Hunt: any install of a bare name matching a known tool's *binary* or *platform-suffixed* distribution name that is not the vendor's scoped package.
- **The 67-version ladder is fake-project theater, and it paid.** A `>= 0`-flagged, single-version typosquat trains analysts and feeds to skip it; a name with 18 days of plausible minor-version churn, daily publish cadence, and thousands of weekly downloads looks like software. The download counter (`opencode2` alone 5,622/wk) shows installs flowed as if it were.
- **Zero-advisory lifetime + advisory-at-seizure is now a three-instance class** (`@yudzxml`, `@chatest`, this fleet ×9): npm's abuse lane deletes/recreates first and the GHSA/OSV pair is minted in the same breath, so **advisory-keyed consumers never see the exposure window at all** — only the survivor `time` block and the downloads counter hold it. Exposure archaeology = `time` block + `api.npmjs.org/downloads`, captured before the recreation reset erases the counter window.
- **The `>= 0` scope shape is the right answer for wholesale squats.** Where `npp-ml` showed version-enumerated scope as a liability against an iterating package, the whole-history scope on an impersonation-squat (the name was malicious from version zero) is the scope-proof form — every consumer resolves affected on any version. Expect this shape to spread to future impersonation sweeps; it cannot be walked past by publishing `2.7.54`.
- **Holder-vs-advisory ordering is now measured per-name at fleet scale:** holders landed from −95 s to +24 s around the shared `:30`-batch GHSA second — consistent with the publish/re-publish-minute wall (holders fire during the recreate `17:44–17:47`), with the advisory batch minted at the next batch second. Fleet seizure = one recreate pipeline pass, ≈2 m 07 s stage→holder max.

## Defender hunts

- Any `require`/`install` of bare `opencode2` or `opencode2-<platform>` — treat every historical version as compromised (advisory scope is whole-history). Rotate secrets on any host that installed.
- Generic rule: for any bare npm name that mirrors a vendor CLI's *command* name or its platform-binary suffix grammar, check the vendor's scoped package is what actually resolves; assert install provenance (`_npmUser`, doc `created` age) in CI.
- Registry-fleet signature for future sweeps: N docs deleted-and-recreated inside minutes + N GHSAs inside one second + contiguous MAL block = coordinated abuse-lane sweep; the individual names tell you the costume, the window tells you it was one investigation, not N.

## Related pages
- [@chatest/baileys seizure](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#october-13-chatest-seizure) — the two-instant publish-minute seizure grammar this fleet reproduces at ×9 scale on one investigation
- [@accenturecodefoundry scope squat](accenturecodefoundry-npm-fake-scope-hex-hostname-username-exfil-azurewebsites-october-2026.md) — same-day fresh-name squatting with the opposite enforcement outcome (zero-record, still live)
- [Baileys 35-name enforcement wave](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#october-12-enforcement-wave-35) — the previous biggest fleet seizure on this ledger; same holder-at-birth + zombie-list mechanics
- [npp-ml scope liability](../tools/npp-ml-pypi-notepadpp-costume-adexplorer-bundle-payload-swap-kam193-october-2026.md) — the version-enumerated-scope failure mode that the `>= 0` whole-history scope shape solves
- [122nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-second-sweep)
