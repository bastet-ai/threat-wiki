# 0sec-cli: the AI security CLI whose own release became the payload

**Captured November 11, 2026 (246th sweep) by this wiki from the `ghsa-malware` bot lane and this wiki's own registry-side verification (public GETs and static reads only; no artifact was ever executed). No analyst payload report existed at capture time; the payload itself is NOT independently verified by this wiki.**

## Summary

On **November 11, 2026 at 12:09:02Z** the `ghsa-malware` bot published `GHSA-9j97-6pqr-qvrx` (critical, CWE-506, `= 0.28.10`) against **`0sec-cli`** — the npm distribution of **"0", the self-described "self-improving, open-source cybersecurity team"**: an AI security harness (investigate vulnerabilities, review findings, connect coding agents via CLI or MCP) published by `peaktwilight` / `doruk@0.security`, repo `0sec-labs/0`, homepage `0.security`, with heavyweight security-tooling dependencies (`playwright`, `tree-sitter`, `drizzle-orm`, `pdfkit`). The security tool *is* the target class: its normal operator audience holds model-provider keys, GitHub credentials, and target scope by design.

This wiki's verification within roughly two hours of the advisory:

- **The advised rung was already gone.** `0.28.10` is absent from `versions[]` and every tarball probe answers `404` on all three lanes (registry, jsDelivr, unpkg) — **no CDN afterimage**. But the packument `time[]` block still enumerates `0.28.10: 2026-11-10T15:54:20.514Z` = the removal-roster law again: the time map is the only registry-side record that the rung ever existed.
- **The name stayed up.** `dist-tags.latest` reads `0.28.9`, whose tarball answers `200`. The takedown was surgical (one rung), name-level install still works.
- **Victim flow was real while the rung lived.** The downloads lane recorded **2,462 downloads in the Nov-4→10 window** and **339 on Nov-10 alone** (the day the malicious rung shipped, 15:54Z). The advisory landed `≈20 h 15 m` after publication; the excision completed sometime between the advisory (`12:09:02Z`) and this wiki's read (`≈14:35Z`) = a `≤2 h 26 m` advise-to-remove clock.
- **Bot-lane mint law holds.** OSV `MAL-2026-19118` carries `aliases: [GHSA-9j97-6pqr-qvrx]` **AT BIRTH**, origin `ghsa-malware`, import `12:23:59Z` (`+14 m 57 s` after the advisory), `modified` on the `12:30:04Z` tick. The row enumerates exactly one version (`0.28.10`) with no `ranges` — triage by the range field: an exact-row advisory protects every other rung on the name.
- **No human queue leg.** No ossf `malicious-packages` PR names `0sec-cli` as of this read (queue head `#1768`) = detection came solely from the machine lane.

| Field | Value |
|---|---|
| Package | `0sec-cli` (npm), `pkg:npm/0sec-cli` |
| Advised rung | `0.28.10` (exact row) |
| Malicious publish | `2026-11-10T15:54:20.514Z` (registry `time[]`) |
| GHSA | `GHSA-9j97-6pqr-qvrx`, critical, CWE-506, published + reviewed `2026-11-11T12:09:02Z` |
| OSV | `MAL-2026-19118`, alias at birth, import `12:23:59Z`, modified `12:30:04Z` |
| Registry state (this wiki, `≈14:35Z`) | `0.28.10` excised from `versions[]`, survives in `time[]`; tarball `404` ×3 lanes; `latest 0.28.9` tarball `200`; packument `modified 2026-11-11T12:08:46Z` |
| Downloads | `2,462` dl/wk (Nov-4→10); `339` on Nov-10 |
| Publisher | `peaktwilight` (`doruk@0.security`), created `2026-08-30`, 23 rungs total |

## Why this one is worth a page

1. **The AI-security-tool-as-vector class lands on npm.** This wiki has logged AI coding agents as *victim executors* (Nx/s1ngularity, `AGENTS.md`/`CLAUDE.md` planted re-arms, the Railway AI-key-name query pattern). Here the *security product itself* is the trojanized dependency: an audience that installs a security harness is precisely an audience holding credentials worth stealing. Same trust inversion as the Ethersphere release-pipeline compromise two sweeps ago — the tool you trust certifies WHO, never WHAT.
2. **The publish cadence is itself a tell.** `0.28.6`–`0.28.9` shipped inside ~3 hours on Nov-9 (`19:43`–`22:48Z`), then a 17-hour gap, then `0.28.10` alone at `15:54Z` Nov-10 — the advised rung is separated from the burst. On any freshly advised name, diff `time[]` spacing around the advised rung before assuming a normal release rhythm.
3. **The advisories-before-removal window ran ~20 hours.** The rung lived a full day+ unadvised (published `Nov-10 15:54Z`, advised `Nov-11 12:09Z`). Whatever the payload did, the flow ran during the unadvised day, not the advised one — the advisory lane's job here was only to trigger the excision.
4. **No analyst writeup at capture.** The only `0sec-cli` reporting at capture time was the bot advisory and its mirrors (Corgea, GCVE aggregators). Treat payload claims as UNVERIFIED until a vendor or maintainer post lands; the maintainer had not commented publicly at read time. **MONITOR:** `0sec-labs/0` repo activity, `SECURITY.md` disclosure, vendor posts (Socket/OX/StepSecurity), whether `0.28.10` resurfaces on any CDN afterimage, whether the name re-publishes past `0.28.9`, and whether the bare rung returns to `time[]`-listed `versions[]` (rollback-not-deletion variant).

## Durable hunt shapes

- On every `= <version>` exact-row advisory, check `dist-tags.latest` against the advised rung: if `latest` is a clean rung, the name keeps accruing downloads as if nothing happened (this name: 2,462/wk).
- Enumerate `time[]` after removal: the advised version's publish timestamp is the start of your exposure window, and `time[]` survives when `versions[]` does not.
- Quote the downloads lane with its window (`last-week` vs `last-day`) — the Nov-10 spike (`339`) is the malicious-day flow, the weekly number averages it away.

## Related on this wiki

- [Ethersphere bee-js / Swarm Desktop release-pipeline compromise](ethersphere-bee-js-npm-swarm-desktop-release-pipeline-compromise-sleepyduck-ethereum-contract-c2-november-2026.md) (trusted tooling as the delivery path, same week)
- [ALGAMIL7X stream, 246th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-sixth-sweep) (capture sweep, fleet, and lane laws)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (developer-credential harvest lineage; kinship NOT asserted)

## Sources

- GitHub Advisory `GHSA-9j97-6pqr-qvrx`: <https://github.com/advisories/GHSA-9j97-6pqr-qvrx>
- OSV `MAL-2026-19118`: <https://api.osv.dev/v1/vulns/MAL-2026-19118>
- npm registry packument + tarball probes + `api.npmjs.org` downloads (this wiki, Nov 11 ~14:35Z): <https://registry.npmjs.org/0sec-cli>
- Package page (maintainer-facing description): <https://www.npmjs.com/package/0sec-cli>
