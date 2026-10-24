# Aokigahara: a Windows infostealer whose distinctive handler steals AI-app and AI-agent sessions (Check Point Research, October 23, 2026)

**First seen:** October 23, 2026 (Check Point Research publication; sample set analyzed earlier)
**Type:** Windows infostealer with a dedicated AI-application/developer-tool session collector (`aisessions`), clipper component, and a structured X25519 + AES-GCM upload gate
**Source:** [Check Point Research — "Infostealer riding the AI Train"](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/) (Oct 23, 2026; analysis by @Tera0017/CPR)

## Summary

**Aokigahara** is a newly observed Windows infostealer that Check Point Research detailed on October 23, 2026. It carries the expected consumer-theft baseline — Chromium/Firefox profiles, ~21 desktop wallet families plus six wallet extensions, Discord/Telegram tokens, Steam, FTP/SFTP clients, password managers, VPN configs, screenshots, clipboard — but its distinctive module is `aisessions`: a purpose-built collector for AI application and AI-agent credentials, session data, and configuration files. An earlier version may have circulated under the names **Kamidere** or **Stygian** (CPR's own uncertainty, recorded as-published).

This is the credential-stealer wing of the AI-toolchain attack class this wiki tracks alongside the supply-chain wing (`abstract-claude` transcript-exfil hooks, the `sitecard` no-auth SSH default, the `obsidian-tc` vault-token GHSAs): the same artifacts an agentic dev box writes to disk — `~/.claude/credentials.json`, `~/.codex/auth.json`, `~/.aws/sso/cache`, VS Code-family `state.vscdb` stores — are this module's enumerated target list.

## Capabilities (handler table, per CPR)

| Handler | Targets |
|---|---|
| `sysinfo` | Computer/user names, IP, Windows version, CPU/RAM, screen, language, uptime, processes, env vars, installed software, AV detected |
| `screenshot` / `clipboard` | `Screenshot.jpg`, `Clipboard.txt` |
| `browsers` | 30+ Chromium-family profiles (Chrome/Edge/Brave/Opera/Vivaldi/Yandex/360Chrome/CocCoc/Torch/URBrowser/QQBrowser/Whale/Avast/CCleaner Browser …) — logins + cookies |
| `firefox` | `logins.json` (NSS-decrypted), key database, cookies |
| `wallets` | Exodus, Atomic, Electrum(+LTC), Ethereum keystore, Zcash, Armory, Bytecoin, Jaxx, Guarda, Coinomi, Wasabi, Dogecoin, DashCore, Litecoin, Bitcoin, Monero, Daedalus, Binance, Ledger Live, TokenPocket; MetaMask/Phantom/TronLink/Coinbase/Binance/Trust extension data |
| `discord` / `telegram` / `discordforks` | LevelDB token scraping, `tdata`, modded-client config files |
| `steam` / `gaming` | `loginusers.vdf`, `config.vdf`, `ssfn*`; Roblox/Battle.net/Epic/Riot/Minecraft/GOG/Origin/Ubisoft |
| `outlook` / `thunderbird` | Mail profiles: addresses, IMAP/POP3/SMTP details, passwords; Thunderbird profile files |
| `vpn` | `*.ovpn`, NordVPN, ProtonVPN, PIA, Surfshark, Windscribe configs |
| `ftp` | FileZilla, WinSCP, CoreFTP, FlashFXP, SmartFTP saved sessions (host/user/pass) |
| `passman` | KeePass, Bitwarden (+CLI), 1Password, Dashlane, RoboForm, NordPass, Sticky Password |
| `filegraber` | Desktop/Documents/Downloads picks under `Files/Documents` + `Files/Crypto` |
| `websessions` | Chromium local/session storage (web-app session data) |
| **`aisessions`** | **AI/dev-tool credentials — see below** |
| `ide` | VS Code/Cursor/Windsurf/JetBrains local data; **Git credential files, `.ssh` private keys, AWS/Azure/GCP credential + config files**, GitHub Copilot storage |
| `clipper` / `clipper_drop` | Drops a separate clipboard-manipulation component under `C:\Microsoft\Vault` from embedded data |

### The `aisessions` target list (the hunt-relevant part)

CPR's path inventory names, per app (`%s` = user profile):

- **Claude Code / Claude Desktop:** `%s\.claude\credentials.json`, `%s\.claude.json`, `%s\Claude`, UWP `Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude`
- **Codex:** `%s\.codex\auth.json`, `%s\.codex\config.toml`, `%s\.codex\.env`
- **ChatGPT Desktop:** UWP `Packages\OpenAI.ChatGPT-Desktop_2p2nqsd0c76g0\LocalCache\Roaming\ChatGPT`
- **Cursor / Cursor Insiders:** `User\globalStorage\state.vscdb`, `storage.json`
- **Windsurf / Windsurf-Next:** `state.vscdb` × 2 channels; **Codeium:** `%s\.codeium\config.json`
- **VS Code / Insiders:** `globalStorage\state.vscdb`
- **GitHub Copilot:** `%s\.copilot\config.json`, `%s\.copilot\hosts.json`
- **AWS CLI / SSO / Amazon Q / Kiro:** `%s\.aws\credentials`, `config`, `sso\cache`, `sso\cache\kiro-auth-token.json`, `%s\amazon-q\data.sqlite3`, `Kiro\...\kiro.kiroagent\profile.json`
- **Gemini CLI:** `gemini-cli-workspace-token.json`, `.gemini-cli-workspace-master-key`, `%s\.gemini\.env`, `config.json`
- **JetBrains AI Assistant:** `JetBrains\*\options\AIAssistantQuotaManager2.xml`
- Windows Credential Manager queries

## Anti-analysis

All gates are config-flag-gated. When the language flag is on, execution stops if keyboard layout or UI language matches the bitmask `0x6C0400C8601` — **RU, UA, BY, TJ, AM, AZ, GE, KZ, KG, TM, UZ** (classic CIS-exclusion). Analysis-environment checks: PEB debug flags, debug-port/object queries, debug-output string, hardware breakpoints `DR0–DR3`; hypervisor CPUID IDs; VM guest-tools registry/process checks; firmware/SMBIOS fingerprints; low process count; cursor movement; username/computer-name strings `sandbox, malware, virus, sample, test, user, admin, CurrentUser, John, Peter, JOHN, John Doe, WDAGUtilityAccount`. API resolution is hash-based; control-flow flattening around config decryption.

## Configuration

Encrypted blob in the `.stgcfg` PE section: magic `STGC`, ciphertext length, 16-byte IV, ciphertext. AES-256-CBC; the 32-byte key is derived from an embedded seed by an FNV-1a-style expansion (CPR published the derivation pseudocode). Decrypted config carries: C&C `base_url`, server **X25519 public key**, `build_id`, `gate_token`, **module bitmask** (dispatch table AND — every module stays embedded even when disabled), language/analysis check flags, optional TLS SHA-256 certificate pin, up to three fallback URLs.

## Network (the `/gate` protocol)

All requests `POST`, `Content-Type: application/octet-stream`, `User-Agent: Microsoft-CryptoAPI/10.0` (observed changing across versions = active development):

- `POST /gate/handshake` — registers an upload session, body = victim's raw 32-byte X25519 public key; headers `X-Build-ID`, `X-Gate-Token`, `X-Session`, `X-HWID`, `X-KEX: x25519`. Requires HTTP 200 before uploads.
- `POST /gate/chunk` — one ZIP per executed module, AES-256-GCM sealed: body = 12-byte nonce (4-byte LE chunk index ‖ 8 random bytes) ‖ ciphertext ‖ 16-byte tag. Headers add `X-Chunk` (module label — `sysinfo`, `browsers`, `firefox`, **`aisessions`**, …), `X-Chunk-Index`, `X-Total`.
- `POST /gate/complete` — body = the 8-byte literal `COMPLETE`, then local session cleanup (does not itself prove every upload landed).

The upload key is `SHA-256(X25519-shared-secret ‖ "aokigahara")` — the fixed string is the malware's own self-name and a durable byte-level hunt marker.

## Detection opportunities (defender-facing)

- **Endpoint (highest fidelity):** read-access to `~/.claude/credentials.json`, `~/.claude.json`, `~/.codex/auth.json`, `~/.aws/sso/cache/*`, VS Code-family `state.vscdb`, `~/.copilot/*`, `~/.gemini/*` **by an unfamiliar non-app process** — these paths have a tiny legitimate-reader set on dev boxes and are enumerated verbatim above. EDR file-access rules on exactly these paths are cheap and specific.
- **Host artifacts:** file creation under `C:\Microsoft\Vault\` (non-standard for anything legitimate); a PE image containing a `.stgcfg` section with `STGC` magic.
- **Network:** outbound POSTs to `/gate/handshake`, `/gate/chunk`, `/gate/complete` with the `Microsoft-CryptoAPI/10.0` User-Agent on **non**-CryptoAPI traffic (real CryptoAPI clients do not POST octet-streams to arbitrary hosts); header set `X-Build-ID`/`X-Gate-Token`/`X-Session`/`X-HWID`/`X-KEX`; body prefix `COMPLETE` on `/gate/complete`. Certificate-pinning absence means TLS inspection sees hostnames but not the header set if the path is proxied opaque — log the header names.
- **Memory/service:** none documented by CPR; no persistence mechanism described in the write-up — this is a one-pass collector, not an implant. Absence of persistence is itself a triage signal (stolen-sessions alert with no persistence artifact = stealer sweep, not C2 residency).

## Assessment and watch

- CPR does not attribute, does not name victims, and does not quantify distribution. Monetization is inferred (service resale, unauthorized consumption, conversation-history extortion), explicitly not confirmed.
- The **"Stygian" earlier-version alias is CPR's own hedge**; it is *not* linkable to the Hades/Mini Shai-Hulud dead-drop repo naming wordlist (which contains "stygian" as a Greek-underworld vocabulary item — coincidence, recorded-not-accused). No supply-chain delivery vector has been published; do not conflate this stealer with the AI-toolchain supply-chain incidents above; the overlap is the TARGET SET, not evidence of shared actors.
- The significance for the agentic-developer population: every session-resume token an AI CLI or agent caches to disk is now a listed, toolized target. Rotation practice for `~/.claude/credentials.json`-class artifacts has never existed for most teams because nobody stole them before; the CIS-language gate suggests the initial customer base skews non-CIS.

**Monitor:** delivery vectors when/if CPR or others publish them; alias confirmation for Kamidere/Stygian lineage; whether the `/gate` grammar or the `.stgcfg`/`STGC` config format appears in other builders (stealer-as-a-service adoption); KEV addition (none — no exploitation determination, unattributed commodity tool); whether the target list grows to new AI CLIs as they ship.
