# `ukraine69` (PyPI): a "Ukrainian locale helpers" costume whose import-time payload hunts Telegram `.vault` session files and DELETEs the victim's account via GoyGram, then self-cleans after 45 s — six releases in 80 min, TWO published after the queue filing that only covers the first four (queue `#1646`, finder ESTsecurity, this wiki static-verified Oct 17)

## Summary

On **October 17, 2026**, `ossf/malicious-packages` queue PR **[#1646](https://github.com/ossf/malicious-packages/pull/1646)** (`skb1209`, filed `14:45:19Z`) filed the PyPI package **`ukraine69`** — summary line `Ukrainian locale helpers, transliteration, date formatting and emoji flags`, owner PyPI user **`svinorezikk`**, no author/homepage/dependencies declared — as malicious across releases `1.2.0`–`1.2.3`, crediting **ESTsecurity** as finder. **This wiki independently pulled and statically read wheels `1.2.0` and `1.2.6` (hashes verified against the PyPI simple-index sha256 fragments, nothing executed) and confirmed the class.**

What the code does on **import**:

- **Vault hunt:** globs for `*.vault` files under the home directory (`**/*.vault`), `/run/hotaru*/**/*.vault`, and (from `1.2.2`+ layouts) the `session_dir/sanctuary/account-<uid>/user-<uid>.vault` shape plus env hints `HOTARU_ACCOUNT_ROOT` / `HOTARU_ACCOUNT_SESSION` and `~/.hotaru/**`, `~/.local/share/hotaru/**` — the file layout and naming of the **Hotaru** Telegram-client ecosystem.
- **Account destruction:** for each vault found, launches a **detached** Python child (`subprocess.Popen(..., start_new_session=True, close_fds=True)`, `sys.executable -I -c ...` in `1.2.5`+) that loads the vault via `goygram.security._read_vault`, opens a `goygram.mt.MTProto` session, and sends **`account.deleteAccount`** — then unlinks the `.vault` and its `.session` sibling. This is not exfiltration; **the payload's destructive primitive is deletion of the victim's Telegram account**.
- **Self-cleaning:** a delayed cleanup agent (`time.sleep(45.0)` in the `1.2.6` read) `shutil.rmtree`s the package directory, its `dist-info` metadata, and the `__pycache__` `.pyc` files after execution — an anti-forensics step timed to run before any human opens `site-packages`.
- **Version iteration:** per the filing, `1.2.2` expanded vault discovery and changed the GoyGram call path, and `1.2.3` swapped destruction for a **hidden reconnaissance child** that logs the first `200` bytes of up to three vaults plus environment details to local files (no network exfil evident in `1.2.3`). This wiki's `1.2.6` read shows the deletion path back, with a multi-strategy call ladder (dict-style, attribute-style, callable, raw `mt.send`) and a docstring written as **legitimate-maintenance changelog prose** ("Vault discovery: sanctuary layout", "Every vault found gets its own detached agent; first success wins") — the docstring itself is costume.

**The ledger-relevant state change is the publish clock, not the payload:** PyPI time records show `1.2.0` `14:09:58Z` → `1.2.3` `14:39:36Z` → **`1.2.5` `15:10:34Z`** → **`1.2.6` `15:29:25Z`** — six releases in ~80 minutes, with the last two published **after** `#1646` was filed at `14:45:19Z` while the filing (correctly, at filing time) scopes only `1.2.0`–`1.2.3`. As of this sweep's check: **zero OSV records (`v1/query` empty for `ukraine69`), zero GHSA, the queue PR still OPEN, and the package LIVE and installable with `latest 1.2.6`** — the advised-but-serving class again, and the advisory-chases-the-publisher loop on the fastest compressed clock yet recorded here (two post-filing iterations inside one hour while the PR sat open; the `pyyi` `2.4.2` precedent ran the same loop over ~17 h). Meaning is unasserted on intent — re-registration behavior after the merge is the tell to watch.

The target profile is the defensive story: victims are people running **non-official Telegram clients that store session vaults on disk** — the payload aims at the session-file estate, not credentials in env vars. Defenders: hunt `*.vault` reads + `account.deleteAccount` strings + detached `python -I -c` children in EDR telemetry; the cleanup path (`dist-info` removed but import history in shell/interpreter logs) means a vanished package is not an innocent one. IoC: PyPI name `ukraine69`, user `svinorezikk`; wheels `1.2.0` `c4f35d79…`, `1.2.6` `297dc4b9…` (leading sha256).

## Tags
- tools
- pypi
- telegram
- goygram
- hotaru
- wiper
- destructive-payload
- self-cleaning
- session-vault
- queue-1646
- estsecurity
- malicious-packages-queue

## Monitor

- `#1646` merge → OSV arrival; whether the import lands scoped `1.2.0`–`1.2.3` only (leaving `1.2.5`/`1.2.6` — and any future rung — out of advisory scope on arrival, the pyyi out-of-scope-rung class pre-baked) or gets updated to six.
- PyPI disposition: still live at check (`latest 1.2.6`); quarantine-lane clock vs the fast-kam193 precedent.
- `svinorezikk` re-registration / name churn; copycat of the vault-destruction primitive against other Telegram-session store layouts.
- Whether `1.2.3`-style recon logging (local files, no network) sees a follow-on release that adds exfil — destroy-after-recon is the natural ladder.
