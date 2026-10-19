# The `@pkgship` frp binary-mirror scope: one advised arm64 build purged 18 s before its own advisory while ten siblings ride unadvised and byte-identical to upstream (OSV MAL-2026-17922 + GHSA-753f-gx8g-q88w, Oct 18, 2026)

## Tags
- tools
- npm
- supply-chain
- malicious-package
- frp
- tunneling
- binary-mirror
- GitHub-Advisories
- OSV
- pkgship
- bytemover

## Summary

On **October 18, 2026 at 21:10:43 UTC** GitHub published `GHSA-753f-gx8g-q88w` (critical, CWE-506 "Embedded Malicious Code", CVE-less, boilerplate-only text) against npm **`@pkgship/frpc-linux-arm64` version `0.71.0`**. OSV imported it as **`MAL-2026-17922`** at `21:22:01Z` (`modified 21:30:38Z`, alias present AT BIRTH). At this wiki's live check the same evening:

- **npm had already deleted `0.71.0` `≈18 s` BEFORE the advisory published.** The package doc's `time.modified` is `2026-10-18T21:10:25Z`; the `0.71.0` arm64 tarball answers `404`. The flagged artifact is **purged-and-unknowable** — the GHSA boilerplate ("consider fully compromised… rotate all secrets") is the ENTIRE public claim about what it did.
- **The `time` block preserves the lifetime:** `0.71.0` published `2026-09-10T07:26:01Z`, purged `Oct 18 ≈21:10Z` = **`≈38.5 days` installable exposure**; last-week downloads `3` (npm downloads API).
- **`latest 0.71.1` (published today `15:38:59Z`) still serves and is OUTSIDE the advisory range** (`= 0.71.0`, first-patched `None`).
- **Static verification by this wiki (pull + hash, zero execution):** the served `0.71.1` arm64 `frpc` binary is sha256 `651de3428bdc7f37b4bad76ed3236b221939a989c433cd7daee79d2817519f8b` — **byte-identical (`cmp` clean, `15,007,906 B`) to `fatedier/frp` v0.71.1's official `frp_0.71.1_linux_arm64` release binary**. The **UNADVISED** sibling `@pkgship/frpc-linux-amd64 0.71.0` binary is likewise byte-identical to the official v0.71.0 amd64 release.

## The scope (live census at check)

Eleven `@pkgship` names, all live, all maintainer **`bytemover`**, binary/platform packages published today `15:36–16:06Z` (plus doc `created 2026-09-10`), every one `0.71.0` + `0.71.1`:

| Name | Shape | Advised? | State at check |
|---|---|---|---|
| `@pkgship/frpc` | wrapper (`bin/frpc.js` spawnSync resolver, ZERO install scripts) | NO | live `latest 0.71.1` |
| `@pkgship/frps` | wrapper (same grammar) | NO | live `latest 0.71.1` |
| `@pkgship/frpc-linux-arm64` | binary package | **YES (`= 0.71.0`)** | `0.71.0` PURGED, `0.71.1` served |
| `@pkgship/frpc-linux-amd64` | binary package | NO | live, `0.71.0` still served (verified upstream-identical) |
| `@pkgship/frpc-linux-arm` / `-arm-hf` / `-riscv64` / `-loong64` | binary packages | NO | live `latest 0.71.1` |
| `@pkgship/frpc-darwin-amd64` / `-darwin-arm64` | binary packages | NO | live `latest 0.71.1` |
| `@pkgship/frpc-windows-amd64` / `-arm64` | binary packages | NO | live `latest 0.71.1` |

`homepage` fields point at the real upstream `github.com/fatedier/frp`; `repository` claims `github.com/pkgship/frp` (unverified). Wrappers carry no lifecycle scripts; platform packages are manifest + binary only. npm search `text=scope:pkgship` returns `total 0` — **scoped packages are not search-indexed; enumerate scopes by direct doc fetch + name probes, never by search** (self-capture).

## Why it matters (durable reads)

1. **A binary-mirror scope is a low-friction costume because frp is legitimate dual-use.** `frp` is the standard open-source reverse-proxy/tunnel client — attackers run `frpc` for pivoting constantly, so a "just republishing frp binaries for npm" scope draws no social suspicion and a flagged build reads plausibly as a false positive either way. The advisory-vs-upstream byte-identity test this wiki ran is the discriminator: **hash any binary-mirror package against the upstream project's official release table before trusting OR fearing it.**
2. **The flagged artifact is unknowable.** Purged before its own advisory, no CVE, boilerplate-only text, no reporter attribution, no surviving tarball: the entire factual content is "one arm64 `0.71.0` build between `Sep 10` and `Oct 18` was called malicious." Recorded-not-asserted: this wiki cannot distinguish a single poisoned build from a mis-scoped advisory — ten siblings unadvised while one platform rung is flagged is consistent with either.
3. **The alias model holds from both ends.** `MAL-2026-17922` read `aliases [GHSA-753f-gx8g-q88w]` at FIRST TOUCH (GHSA-first arrival → join at birth), while `MAL-2026-17921` (leakdeep, OSV-first, kam193-curated) the same evening still reads `aliases None` with `modified` re-frozen `16:45:03Z`. Model v3 (the join rides the GHSA-mint event, OSV-first records never join) survives unchanged.
4. **Publish→OSV-import on a GHSA-first record measured `11 min 18 s`** (`21:10:43Z` → `21:22:01Z`), versus the `:31`/`:22` hourly batcher lag for OSV-first records and the `≈6 min` merged-PR clock. The pipeline is FAST when the GHSA is the origin.
5. **The queue was bypassed again.** `ossf/malicious-packages` has no filing for any `@pkgship` name at check (issues search `total 0`) — the GHSA-led machine lane advised end-to-end with no curated PR, joining leakdeep's machine-lane precedent.

## Hunt guidance

- Any `@pkgship/*` install in lockfiles/CI (all eleven names; the scope is young — `Sep 10` doc creation).
- `0.71.0`-range `@pkgship/frpc*` installs dated `Sep 10 – Oct 18` for the advised arm64 window.
- Generic binary-mirror rule: any npm package shipping a Go static binary whose hash does NOT match the upstream project's official release artifact for the claimed version.

## October 18 one-hundred-and-thirty-seventh sweep: FIRST READ (this wiki forensics ~21:1x–21:5x UTC)

Recorded at first touch: GHSA `21:10:43Z`, OSV `21:22:01Z`, npm purge `21:10:25Z` (`18 s` pre-advisory), `0.71.1` arm64 + `0.71.0` amd64 binaries `cmp`-identical to official releases, eleven-name scope census (above), download counts `2–4/wk`, wrappers script-free. **ROUTE SELF-CAPTURE (durable): GHSA `affects=<pkg>` returns `[]` for malware advisories unless the call also passes `type=malware`** — `affects=leakdeep`, `affects=ukraine69`, `affects=@pkgship/frpc-linux-arm64` ALL read false-`[]` bare and ALL return their GHSA with `&type=malware`; bare-`affects=` zero-reads on other pages from earlier sweeps re-score as UNKNOWN unless corroborated (the ledger's queue-name zero-reads were re-verified genuinely zero under the corrected route this sweep: `bbmarker`, `imgdecode`, `@apexscore/cli`). Monitor: a second advisory on any sibling (= scope-asymmetry resolves toward targeted poisoning); any new `@pkgship` version (re-hash vs upstream); queue filing ever appearing; `0.71.0` amd64 disposition (still served, advised scope excludes it). Sweep context → [137th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-thirty-seventh-sweep).

## <a id="october-19-second-read"></a>October 19 one-hundred-and-thirty-eighth sweep: SECOND READ (~01:3x UTC) — scope-asymmetry test still unresolved

Second advisory check `≈4.5 h` after `GHSA-753f`: the `@pkgship` scope carries exactly ONE malware advisory (arm64 `= 0.71.0`); `affects=@pkgship/frpc-linux-amd64&type=malware` (corrected route) `[]`; no new OSV record names any `@pkgship` package. `0.71.0` amd64 still served, `0.71.1` still latest. Targeted-vs-mis-scoped stays undecidable at two reads. Forward: same test at `≈24 h`; any newly published `@pkgship` version gets an immediate upstream-hash check. Sweep context → [138th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-19-one-hundred-and-thirty-eighth-sweep).

## <a id="october-19-third-read"></a>October 19 one-hundred-and-thirty-ninth sweep: SCOPE-ASYMMETRY THIRD READ — still ONE advised name `≈11 h` in (`@pkgship/frpc-linux-amd64` OSV `{}`, `@pkgship/frpc` `{}`, arm64 alone `MAL-2026-17922`; no second advisory, no queue filing on any `@pkgship` name). Targeted-vs-mis-scoped stays undecidable; no new version published = no re-hash trigger on `0.71.1`. Sweep context → [139th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-19-one-hundred-and-thirty-ninth-sweep).

## <a id="october-19-fourth-read"></a>October 19 one-hundred-and-fortieth sweep: SCOPE-ASYMMETRY FOURTH READ — still ONE advised name `≈14 h` in (`@pkgship/frpc` `{}`, `@pkgship/frpc-linux-amd64` `{}`, arm64 alone `MAL-2026-17922`, its `GHSA-753f` alias intact); no second advisory, no queue filing, no new version = no re-hash trigger. Sweep context → [140th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-19-one-hundred-and-fortieth-sweep).
