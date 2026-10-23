# Sitecard (PyPI) — "SSH access cards" with no-auth default and a hardcoded ntfy rendezvous: the first kam193 MAL-class mint still FULLY SERVED a full hour AFTER its critical GHSA (OSV `MAL-2026-18242`, `GHSA-9wjg-8fcv-pxj2`, 13 rungs, artifacts live throughout)

 kam193 campaign `2026-10-sitecard` · OSV `MAL-2026-18242` (published 2026-10-23T16:30:56Z) · `GHSA-9wjg-8fcv-pxj2` (critical, published 2026-10-23T18:31:16Z) · 13 rungs `0.1.0`–`0.1.14` · 1,283 downloads last week at capture

## What it is

`sitecard` is a PyPI package branded as a developer utility — *"Issue temporary SSH access cards for development workspaces"* — that opens tunneled SSH sessions to a victim's machine. The kam193 tracker (source of the OSV record) classifies it `MALICIOUS`/`backdoor` with the operative finding:

> The package provides code to create an SSH session exposed via tunnels. By default, created session is accessible without any auth and reported to a hardcoded location, exposing any user to be accessed by attacker.

This wiki read the `0.1.14` sdist (public GET, sha256 `a6e497421f1438d7d9e89ea2e18ddec1fa67a2881d7728c7f788241481acb810` = the PyPI-declared digest, verified this sweep). The layout is ordinary, unobfuscated Python (`src/sitecard/`, ~17 modules, no install-time hooks, no binaries):

- **No-auth SSH is the DEFAULT, documented as a feature.** README: *"Fresh Sitecard sessions allow public access by default because they are disposable"*; `--accept` *"permits SSH without credentials… Anyone with the relay URL can then open a shell."* The `--no-public-access` authenticated path exists but is the opt-in, not the default.
- **Hardcoded rendezvous.** `session.py` carries `RENDEZVOUS_DEFAULT_URL = "https://ntfy.sh/02f9fe8a5cd9627395798443a235896b"` — every session self-publishes to a fixed public ntfy.sh topic, which is the "reported to a hardcoded location" in kam193's description. `wsroute.py` defaults the tunnel provider to `wss://uptermd.upterm.dev` (public tunnel-of-the-day infrastructure).
- **A model-relay companion that proxies inference THROUGH the tunnel.** `model_relay.py` hosts a Responses-API-shaped endpoint with `DEFAULT_UPSTREAM = "https://chatgpt.com:18080/backend-api/codex"` and a `--accept`-style anonymous mode (`-a`) — the README's own text: *"Anonymous URLs expose workspace/model access to anyone."*
- **Microsoft Dev Tunnel integration with `--anonymous` access commands copy-pasteable from the README** (`devtunnel access create … --anonymous`), i.e. the documentation walks users into placing an unauthenticated shell behind a public HTTPS URL.

**Classification note (recorded, not asserted):** the disclosure of the dangerous behavior is IN the README, the code is clean Python, and no fetch-and-exec loader or credential-stealer was found at read depth. kam193's `MALICIOUS` call rests on the no-auth-exposed-and-reported-to-attacker-known-location architecture, and GitHub's importer agreed at `critical` with all 13 rungs in range. It is simultaneously plausible this is an attacker-operated access tool AND that it is a reckless dev-tool the tracker escalated — the durable fact for defenders is narrower and stronger: **a PyPI package whose default operation exposes an unauthenticated shell and announces sessions to a fixed public topic, carrying a malware-class GHSA and an OSV entry, still installable at ~1,283 downloads/week.** Block/remove the name; treat any host running it as having an open inbound path.

## Why this record is a lane first

Prior kam193 MAL-class mints on this lane were either quarantined within `≈1–2 h` of the OSV mint (voice-synth wave three `21`-for-`21`, `qowa`, `onsokets`) or leaked installable but were pulled within the same day (wave one `19`-of-`21`). `sitecard` is different in shape and duration: `MALICIOUS`-class with a critical GHSA published at `18:31:16Z`, and **every artifact still served `≈1.5 h` AFTER the GHSA** — PyPI JSON `200`, `/simple/` `200` with all 26 files, tarball `200` re-downloaded and re-hashed post-advisory — the full artifact readable in the open while both ledgers scream, which is what made the forensics above possible in one sweep. Its OSV also carries a REAL version history (`13` rungs across Sep-22 → Oct-18 with a burst of `9` rungs inside `≈2 h` on Oct-18) instead of the campaign boilerplate single `0.1.0`.

Consequences:
- **The artifact-starvation wall has an exception class**: names with pre-existing release history and download traffic survive enforcement longer — either because takedown is a judgment call on an established project, or because the publisher is not co-operating with the campaign's own hygiene. Either way, **read-live-first triage pays**: a live MAL-class mint is a forensics opportunity the quarantined cohort never gives.
- **The clock story continues**: OSV `16:30:56Z` while live → GHSA `18:31:16Z` (`≈2 h 05 m`, inside the same importer tick that finally mirrored voice-synth wave three) → OSV `aliases` STILL `None` at `≈2.5 h` after the GHSA existed. The never-join law now covers a LIVE name with a critical GHSA — alias-diff reconcilers stay blind even here.

## Hunt spec

- `pip download sitecard` / any venv containing `sitecard` (13 rungs, all advised; `latest 0.1.14`, `1,283` dl/wk at capture — expect real installs in the wild, not attacker-only).
- Egress/connections to: `ntfy.sh/02f9fe8a5cd9627395798443a235896b` (fixed topic string = the single best indicator), `*.upterm.dev` / `uptermd.upterm.dev`, `*.devtunnels.ms` with anonymous access created (query the devtunnel audit path where available).
- Listening loopback SSH gateway on `127.0.0.1:4822` (`DEFAULT_PORT`), plus hosted relay ports `8080/8081` under devtunnels.
- Inbound SSH sessions arriving through public tunnels on developer workstations with no corresponding ticket — the README literally calls it "remote debugging and compatibility testing," expect that as the social cover.

## State at capture (Oct 23, ~19:2x–19:5x UTC)

Registry FULLY LIVE (JSON `200`, simple `200`, files `200`); OSV `18242` live, `aliases None`; GHSA `9wjg` live `critical`, ranges `= 0.1.0` … `= 0.1.14` — both ledgers enumerate all 13 rungs, identical version sets, `diff(advisory, OSV)` clean (the 186th's subset-completeness check passes on this record). ossf queue filing unknown. The publisher name/email fields are empty in the PyPI doc (no author, no project URLs) — costume-class anonymity on an `≈1 month` old account footprint (`0.1.0` Sep-22, first release).

**Monitor:** whether PyPI quarantines it (the advisory is live and critical — inaction is now conspicuous), whether the ntfy topic is alive to subscriber reads (do NOT publish to it), whether `0.1.15` appears, `aliases` join status, whether any victim telemetry surfaces. Sweep context → [188th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-23-one-hundred-and-twenty-eighth-sweep).
