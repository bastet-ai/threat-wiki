# `minecraftaccfinder` (PyPI) — a `SKULL`-bannered Minecraft-account stealer + full Windows RAT with Discord exfil, published as a six-version ladder in 23 minutes, and at check the machine advisory lane has seen NONE of it

**Captured by this wiki October 12, 2026 (~09:2x–09:5x UTC, one-hundred-and-seventh sweep).** Live subject page: curated-lane PR [`ossf/malicious-packages` #1625](https://github.com/ossf/malicious-packages/pull/1625) (reporter `eskim86`, opened 08:02:31Z) is the ONLY public record — **ZERO OSV, ZERO GHSA ≈8.7 h after the first publish** while every version remains installable from PyPI.

## What it is

`minecraftaccfinder` is a PyPI package whose importable module is an 86,870-byte, single-file, fully standalone Windows infostealer + interactive RAT — and its declared surface is a Minecraft account finder. Six versions (`0.1.2`, `2.0.0`, `0.3.0`, `0.3.1`, `0.4.0`, `3.0.0`) were published between **01:05:17Z and 01:28:04Z on Oct 12 in one 23-minute window**, interleaved version numbers and all (2.0.0 landed between 0.1.2 and 0.3.0) — the scripted-ladder grammar the ledger has been reading on npm for weeks, reproduced on PyPI. `latest = 3.0.0`, zero yanks, zero quarantine markers at check.

Artifact record (pulled and read by this wiki, NOT executed):

- sdist `minecraftaccfinder-3.0.0.tar.gz` sha256 `2a57158af872064d9440f0d21121adb449152dd28873c9b2d244b52c34820617`
- module `minecraftaccfinder/__init__.py` sha256 `89f4148533676173ddeac9dac0bf0fa1656cd855adbfbc5b0665ae0c50e7fc49` (86,870 B)
- `pyproject.toml` carries NO dependencies; no `setup.py` build hooks; execution rides the `console_scripts` entry point `minecraftaccfinder = minecraftaccfinder:main` — the module body itself ALSO runs on plain `import` (the file begins `print("error❌")` and everything else executes at import time).

## The costume, and the tell

The module opens by printing `error❌`, then carries a giant ASCII-art **SKULL** banner immediately followed by a fake supply-chain skin:

> `OneDrive Sync Helper v2.6.1 [Protected Build] — SECURITY BOT — PROTECTED BUILD / AUTHORIZED DEPLOYMENT ... digitally signed by the Microsoft release team ... Scan Safe: verified 2026-01-12 | SHA-256: AB12CD34...`

The "signed by the Microsoft release team" claim with a truncated placeholder hash (`AB12CD34...`) is the tell: the banner is decoy text inside a package named after Minecraft account lookup, and the code below it does neither job. The skull is the more honest label.

## Capability map (read from source, no execution)

Targets, all Windows-pathed (`winreg`/`ctypes`, `%APPDATA%`):

- **Browsers × 3 engines:** Chrome/Chromium-family DPAPI + `Local State` AES-key extraction + `Login Data` + cookie decryption (incl. v10/v20 ABE path with `/_abe_policy_disable/`), Firefox `key4.db`/`logins.json`/plaintext cookies, plus a **CDP debug-browser launch** (`_launch_debug_browser`, `--json/new`, websocket `Runtime` calls) to dump cookies/logins from a live profile.
- **Scope of the harvest is account-theft-shaped, not just credential-shaped:** `%roblox.com` cookies, **Gmail cookies** (account-recovery email access), **Discord leveldb** (token), **Minecraft `launcher_accounts.json`** (`grab_minecraft` — the literal product the package name advertises), browser saved passwords via DPAPI/ABE and Firefox.
- **RAT layer:** a `c2_client`/`c2_listen` thread pair (interactive listener), a **60-second screenshot loop**, a **keylogger with a "typed keys texter" thread**, a password-manager spy loop — and the operator status line quoted verbatim in source: `STATUS ONLINE: auto-screen every 60s | PW-MGR spy 1s | keylog spy + TYPED KEYS texter`.
- **Standalone crypto:** ships a pure-Python AES-256-GCM/CBC implementation so it works with zero installed dependencies — the same no-deps portability design the ledger sees in phishing kits, not libraries.

**Exfil channel is Discord:** hardcoded bot-channel post to channel id `1361722007997124650` (`https://discord.com/api/v10/channels/{CHANNEL_ID}/messages`) with a webhook fallback `https://discord.com/api/webhooks/15wun9sW...` (token truncated in source; the code checks the bot token against a `MTE4xxxx...` placeholder before using it, so a real token may or may not be committed). Exfil blocks are zlib-compressed, and the module also fetches `api.ipify.org` for victim geo-IP. A local "delivery receipt" is written next to the payload logging what was sent.

## Why this is the headline, not the malware itself

This class of package — gaming-account stealer + commodity RAT — is the most common thing on PyPI. The ledger-relevant fact is the **advisory differential**:

- Amazon Inspector / OpenSSF package-analysis has been this ledger's most reliable PyPI/npm feeder for six weeks, publishing hundreds of `MAL-2026-*` records, often <1 h after publish.
- `minecraftaccfinder` shipped six live versions 01:05–01:28Z, was reported into the curated lane at 08:02Z, and at this check (~09:5xZ) has **no OSV record at all** — name-keyed `v1/query` returns empty — and **no GHSA** (`affects=` lookup empty). Every consumer keyed to the machine lane is blind to a full-RAT package whose skull banner is the first thing in the file.
- Contrast the same-week clock: `agentaix`/`media-manager5` were quarantined ≤1.5 h of OSV arrival; `lore-cs` was advised same day; this name has outlasted the machine lane for ~8.7 h and counting while `latest` is installable.
- Curated-lane dependence has its own clock risk: the ledger's own precedent says curated PRs can sit for days-to-weeks (`#1590` ≈9 d, `#1618` ≈86 h), and until one merges, OSV/GHSA-keyed consumers see nothing. #1625 is the entire public record.

**DURABLE:** zero-OSV + zero-GHSA is now demonstrated as a STEADY STATE for a live full-RAT PyPI package with a self-advertising name — the "curated-subject zero-machine-record is a steady state" read from `util-foriepft`/`orderly-plugin` reproduces on PyPI, at higher severity. Detection here cannot depend on advisories: the static tells (skull banner, `winreg` + `discord.com/api/webhooks` + `launcher_accounts.json` + keylogger threads in a package whose name promises an account "finder") are all YARA/grep-able from the sdist alone.

## Defender hunts

- Any PyPI/npm package whose module contains `discord.com/api/v10/channels/` or `discord.com/api/webhooks/` outside a genuine Discord-bot library.
- `launcher_accounts.json`, `leveldb` + `Local State` + `logins.json` references in the same module.
- `STATUS ONLINE` / `keylog` / `_screenshot_loop` string set.
- Channel id `1361722007997124650` and webhook fragment `15wun9sW` in egress/proxy logs (Discord API calls from non-client processes; resolver logs won't help — `discord.com` is the destination, so hunt the process+URL pair, not the domain).
- Interim disposition for users of anything named `*accfinder*` on Windows: treat browser passwords, cookies (Google/Roblox), Discord tokens, and Minecraft accounts on that host as exposed; rotate from a clean device, and check for the module file + its local `oa_debug.log`-style drop.

## Monitor

- OSV/GHSA arrival for `minecraftaccfinder` (does the machine lane ever catch up, and how many hours late?) and `#1625` merge or rot.
- Publisher identity (PyPI project page renders no uploader to this wiki's fetcher; the PR reporter `eskim86` is the curator, not necessarily the publisher) — check PyPI JSON API for maintainer next sweep.
- Sibling names: `*accfinder*`/`*account*finder*` grammar on PyPI/npm, and any Discord-channel-id reuse in other packages (the channel id is a durable cluster key, the ledger's `chat_id 1064260758` precedent).
- Whether `3.0.0` stays the top version or the ladder iterates while unadvised (the advisory-as-build-trigger question only starts once an advisory exists — today the trigger risk is the curated PR itself: `#1625` is public while the package is live).

## Follow-up — October 12 one-hundred-and-eighth sweep (~11:3x–11:4x UTC): the machine lane arrived, the registry followed, GHSA has not

- **OSV `MAL-2026-17809` MINTED `published 2026-10-12T09:29:22Z`** (source `kam193`, eight versions `0.1.0`–`3.0.0` in scope — the full ladder). First publish `01:05:17Z` → OSV = **≈8 h 24 m machine-lane lag**, the ledger's first measured arrival clock on a non-self-reporting PyPI stealer. The `modified` stamp flipped `10:30:03Z` ≈1 h post-mint (queue-event rule).
- **GHSA STILL ABSENT ≈2 h later** (`aliases: None`, `pip`-ecosystem `affects=` lookup empty) = OSV-keyed consumers are covered, **Dependabot-class consumers remain blind to a quarantined full-RAT package** — the two-lane split on this page's own subject, live.
- **PyPI REGISTRY ACTION ≈2 h behind OSV:** `simple` index now meta-tagged `pypi:project-status quarantined` with a ZERO-file listing; JSON API `404`. Ordering publish → OSV → registry mirrors the RubyGems 24-gem advisory-led pattern; whether the name soft-holds (RubyGems name-hold taxonomy) or hard-deletes decides the resquat watch — **any version under `minecraftaccfinder` under ANY publisher is a comeback.**
- **Correction to this page's original framing (self-capture):** the ~09:5xZ name-keyed `v1/query` read returned empty although the mint's own `published` stamp predates it by ~30 min — the 150th's stale-edge rule applies to `v1/query` too (shared edge cache). The honest zero-advisory window is ≈8.4 h, and "zero OSV + zero GHSA as STEADY STATE" now rests on `util-foriepft`/`orderly-plugin`, not this name. What this page still proves: **machine-lane absence carries a lag distribution measured in attack-days, not minutes — it is never a benign signal at check time.**
- Curated PR #1625 remains open unmerged (post-mint it is bookkeeping); the Discord channel-id `1361722007997124650` and string hunts above stay armed — quarantine removed the supply, not the infrastructure.
