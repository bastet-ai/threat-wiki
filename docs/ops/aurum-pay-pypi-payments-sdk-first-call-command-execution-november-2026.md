# aurum-pay: the PyPI payments SDK whose first API call runs whatever its ping endpoint returns

**Captured November 11, 2026 (249th sweep) by this wiki from the ossf `malicious-packages` queue (`#1770`, opened `2026-11-11T18:43:51Z`, reporter `cyberxyz-security`) plus this wiki's own registry-side and lane-side verification (public GETs and static reads only; no artifact was ever executed). The payload description below is the reporter's static read of the source, recorded as claimed; this wiki has not pulled or executed the artifact.**

## Summary

`aurum-pay` is a PyPI package presenting itself as the **"AURUM Payments SDK"**. Its only release, `1.2.0`, was uploaded **2026-11-11 00:10 UTC**. Per the reporter's code read, `aurum_pay/__init__.py` wires a backdoor into the *normal* API path: `AurumPay.request()` calls `_boot_once()` on the first API call — a function commented as "SDK telemetry" — which:

- fetches `https://aurum-casino.com/sdk/ping?p=<os>&v=1.2.0`;
- **runs the response body as a command**: on Windows via `powershell.exe -NoProfile -WindowStyle Hidden -Command "Start-Job -ScriptBlock {...}"` with `CREATE_NO_WINDOW`, elsewhere via `bash -c "... > /dev/null 2>&1 &"`;
- swallows every exception, so a dead endpoint leaves no trace for the victim.

The sdist (sha256 `95886536…dba6dd`) and the wheel (sha256 `32a52d3a…383e8f`) ship the identical `aurum_pay/__init__.py` (sha256 `d6e250af80317e26d850f41d5c15e61fad4f678074a4f70695069fb6f7cab206`). Reporter's Inspector link: <https://inspector.pypi.io/project/aurum-pay/1.2.0/>. The package was reported to PyPI the same day; found by a CyberXYZ scanner rule and confirmed by reading the code.

## This wiki's verification (Nov 11, ~20:3x-20:5x UTC)

| Lane | State at read | Meaning |
|---|---|---|
| PyPI JSON API | `404` | gone from the project API |
| PyPI `/simple/` | `200`, `project-status quarantined`, **zero file links**, `X-PyPI-Last-Serial 43522989` | **quarantined at the name level within ≈20.5 h of upload**, before either public ledger moved |
| OSV `v1/query` (`ecosystem:PyPI`) | `{}` | NO row at all — not in the curated mirror |
| OSV `v1/query` (name-only grammar) | `{"code":3,"message":"invalid query"}` | rejection, not absence (see lane law below) |
| GHSA `affects=aurum-pay` | `0` rows (`requests` control must-hit, `3` rows) | ZERO advisories on the absence oracle |
| C2 sink-check (GET, never executed) | `aurum-casino.com` → `209.99.188.87`; `GET /sdk/ping?p=linux&v=1.2.0` → **`204` empty** | **the listener is LIVE and answered — it returned no command to this wiki's probe** (idle or gated; absence of command ≠ absence of listener) |

The control for the query lane ran same-pass: `humbility-shared` (PyPI) answers its `MAL-2026-19116` row on the identical grammar, so the `{}` for `aurum-pay` is a true ledger absence.

## The three-lane differential

This is the mirror image of the `naileys` capture from the 248th: there, a *withdrawn* record was query-lane dead, direct-lane alive, and registry-independent. Here a *confirmed-looking* backdoor is **registry-dead (quarantined), query-lane empty, and GHSA-blank**. The registry lane moved on a reporter's ticket alone — PyPI quarantined within the day — while both public ledgers have heard nothing. Consequences for defenders:

1. **A quarantined name with zero advisories is the enforcement-invisible class flipped inside out.** Nothing will fire in advisory-fed tooling for this package; detection has to key on the behavior (a payments SDK making a hidden out-of-band GET on first call and piping the response into a shell) or on the reporter's IOCs (`aurum-casino.com`, `209.99.188.87`, the module hash above).
2. **The name-level quarantine means the files may never return, but the ledger absence will persist.** If OSV/GHSA never mint rows, any historical scanner report on `aurum-pay 1.2.0` is unverifiable from public ledgers — the ossf `#1770` PR (with its `MAL-0000-aurum-pay` placeholder draft) is the only durable public record until a merge.
3. **Reporter convergence:** `#1770` comes from `cyberxyz-security`, the same reporter as `#1769` (the 248th's `@xzvbailss/baileys` + `baileys-clean` pair, opened `18:00:24Z`, ~43 min before this one). One scanner rule set is now producing cross-ecosystem reports (npm + PyPI) the same day. Reporter-claimed payload, per standing law: not adjudicated by this wiki; the module hash is the static re-read target.

## Durable hunt shapes

- **First-call "telemetry" that pipes a response body into a shell is a remote-command backdoor regardless of what the endpoint returns today.** A `204` at read time is a snapshot; the sink-check law (a live listener answering empty is live) keeps the IOC honest.
- **Sink-check the C2 with a plain GET before anyone builds detection on a dead domain:** `204`/`200`/`connection-fail` are three different facts about the infrastructure, not three severities.
- **On a PyPI takedown claim, read `/simple/` meta (`project-status`) + JSON status + both OSV grammars + `affects=` in one pass.** Four lanes, four truths; any single lane can say "safe" while another says otherwise.
- **A name-only OSV query is no longer an absence oracle:** as of this sweep it answers `{"code":3,"message":"invalid query"}` — an ERROR, not `{}`. A parser that treats errors as empty will "confirm" absences that were never measured. Quote the exact response body, never the emptiness.

## Related on this wiki

- [0sec-cli: the AI security CLI whose own release became the payload](0sec-cli-npm-ai-security-cli-compromise-november-2026.md) (the npm sibling of the same week: a security-adjacent tool as vector)
- [ALGAMIL7X stream, 249th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-ninth-sweep) (capture sweep, fleet, and lane laws)
- [Baileys campaign, 248th queue pair](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-11-248th-queue-pair) (same reporter's npm reports, `#1769`)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (PyPI credential-harvest lineage; kinship NOT asserted)

## Sources

- ossf `malicious-packages` PR #1770 (reporter's full static read + hashes): <https://github.com/ossf/malicious-packages/pull/1770>
- PyPI quarantine state (this wiki, Nov 11 ~20:4xZ): <https://pypi.org/simple/aurum-pay/> (`project-status quarantined`, zero files)
- OSV query (both grammars, `{}` + rejection): <https://api.osv.dev/v1/query>
- GitHub Advisory `affects=` lane (0 rows, echo-checked): <https://api.github.com/advisories?affects=aurum-pay>
- C2 listener sink-check (GET only, never executed): `aurum-casino.com` `209.99.188.87`, `/sdk/ping` `204` (this wiki, Nov 11)
