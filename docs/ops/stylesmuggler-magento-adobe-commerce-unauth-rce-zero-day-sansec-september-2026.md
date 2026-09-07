# StyleSmuggler: Magento / Adobe Commerce unauthenticated RCE zero-day under active attack (Sansec, Sep 5, 2026)

## Tags
- ops
- operations
- web application
- Magento
- Adobe Commerce
- Magento Open Source
- RCE
- remote code execution
- unauthenticated
- zero-day
- GraphQL
- template injection
- Rust backdoor
- NTP C2 disguise
- Magecart
- e-commerce
- active exploitation
- Sansec
- Aikido

## Summary

On **September 5, 2026**, Sansec published **StyleSmuggler**, an unpatched **unauthenticated remote-code-execution zero-day** in **every current version of Magento Open Source and Adobe Commerce** (including 2.4.9, the latest release). Attacks began **September 4, 2026, 22:40 UTC** — a day before public disclosure. As of Aikido's September 7 follow-up, **Adobe had not published an advisory, CVE, or patch**, and Adobe Enterprise Support confirmed on September 7 that they were working on a patch with no ETA. The next scheduled Adobe security release is **September 8, 2026**, but coverage of this flaw is not confirmed.

The exploit is **two-stage**, both stages abusing Magento functionality that already exists:

1. **Stage 1 — inject:** An unauthenticated attacker sends a **GraphQL request** whose `styles` property carries an injected PHP payload. The payload does **not** execute immediately. It is written into a file that Magento generates itself (for example a **checkout failure report**).
2. **Stage 2 — execute:** The poisoned file is later rendered when Magento processes a **"Payment Transaction Failed Reminder" email**. The email does not need to be delivered — the code runs **server-side during template rendering**. The attack completes even if the message never reaches an inbox.

**Every version is vulnerable**: Sansec reproduced the full unauthenticated chain on clean installs of **2.4.7, 2.4.8, and 2.4.9**. One confirmed victim was running **2.4.6-p15** with the July and August 2026 security patches fully applied and `security:patch-status` clean — patch status did not save it. Moving sessions to Redis or the database does **not** stop the attack (an operator was observed failing once against session storage, then succeeding eight seconds later by routing the payload through a file uploaded via Magento custom options).

Confirmed intrusions have installed a **persistent Rust-based backdoor** disguised as a kernel thread. It survives a reboot and sits dormant for hours to days before activating. From there, the exposure is everything unauthenticated RCE on an e-commerce platform implies: **customer PII, payment transaction details, admin credentials, database contents, and a route to Magecart-style skimmer injections** against shoppers.

## Why this matters

- **Mass attack surface.** Magento and Adobe Commerce power a very large fraction of the world's e-commerce sites. An unauthenticated RCE with no known fixed version is a mass-compromise vector, not a single-site incident.
- **No vendor patch yet.** As of September 7, 2026 there is no CVE, no advisory, and no patch from Adobe. The interim mitigation is **disabling GraphQL** (which takes headless / PWA storefronts offline), or the Aikido Libraries drop-in patch for specific branches.
- **Two-stage delayed execution.** The inject-to-file and execute-at-email-rendering split means the compromise window is not the attack time but the **next failed-payment email render** — defenders hunting only at the moment of the GraphQL request will miss the RCE.
- **Rust backdoor disguised as kernel infrastructure.** The implant uses rotating process names (`[kworker/u:8:0]`, `fc-cache`, `chronyd`) to blend into legitimate system daemons, and C2 traffic is **NTP-shaped UDP on port 123** — a port and protocol that most egress filters pass unremarked.
- **Second, distinct actor.** Sansec identified a **separate actor** on the same victim stores on September 7, using a 485-byte PHP dropper that writes a web shell into the Magento product-image cache directory. The two actors share only their victims, not their tooling.

## Technical detail

### Exploit chain

| Stage | Mechanism |
|---|---|
| 1. Inject | Unauthenticated GraphQL request; `styles` property carries PHP payload; payload written into a Magento-generated file (e.g. checkout failure report) |
| 2. Execute | Magento renders a "Payment Transaction Failed Reminder" email; server-side template processing runs the embedded PHP; email need not be delivered |

### Affected versions

- **Magento Open Source**: 2.4.7, 2.4.8, 2.4.9 (confirmed vulnerable on clean installs)
- **Adobe Commerce**: all current versions (confirmed vulnerable)
- **Magento Cloud**: metapackage affected
- **2.4.6-p15** with July + August 2026 patches: confirmed vulnerable (one victim)
- No version is confirmed safe as of September 7, 2026

### Confirmed intrusions: Rust backdoor

- **Process names** (rotating per build):
  - Original: `[kworker/u:8:0]` (disguised as a kernel worker thread)
  - Sep 6 builds (arm64 + x86-64): `fc-cache` (copies to `~/.cache/fontconfig/fc-cache`, PID file `/tmp/.fc_<8hex>.lock`)
  - Sep 7 build: `chronyd` (re-drops to `/tmp/.chrony-<8hex>/chronyd`; the 8-hex agent ID carries over from the fc-cache drop — one implant renaming itself, not a second infection; reports version 2.1.5 vs 2.1.4)
- **Persistence**: cron entries written **directly into the cron spool file** (not via `crontab -e`), so syslog holds no `REPLACE` line. Observed schedules: `13,43 * * * *` (fc-cache variant), `57,27 * * * *` (chronyd variant). The chronyd build can also relaunch with **no cron entry at all** (parent PID 1), so an empty crontab is not evidence of a clean host.
- **C2 — NTP-shaped UDP**:
  - Primary: `ntp.timesync.to` and `ntp.timesysnc.net` (both resolving to **185.157.160.251** as of Sep 7)
  - Fallbacks: `ntp.synctime.to`, `ntp.syncstime.to`
  - Protocol: 48-byte UDP datagrams to port 123 every 60 seconds; only the first 4 bytes are real NTP; the rest carries a chunked MessagePack record (agent ID, hostname, username, OS version, memory/disk usage, uptime, root status, implant version)
  - Distinguishing from real NTP: the implant emits **nine 48-byte datagrams ~10 ms apart every 60 s** (real client sends one), and every datagram is marked **NTPv4 server mode** (a client has no reason to send server mode)
  - Before beaconing, the implant resolves its own public IP via plain HTTP from `api4.ipify.org`, `ipv4.icanhazip.com`, `ipv4.ident.me`, and `ipinfo.io`, using a User-Agent truncated after `AppleWebKit/537.36` (matches no real browser)
- **Sandbox evasion**: the implant reads `TracerPid` from `/proc/self/status`; if traced (sandbox / debugger), it still installs itself but **never beacons**.
- **Secondary C2** (original build): `99.84.67.186:443` (WebSocket over TLS)
- **Weaponization status**: as of publication, the backdoor had **not been weaponized** (no observed command-and-control traffic beyond the beacon), and no security vendor other than Sansec had detected it.

### Second actor: PHP web shell in product-image cache

On September 7, Sansec analyzed a **485-byte PHP dropper** that shares nothing with the Rust implant except its victims:

- **Download URL**: `https://www.incofar.it/js/jquery/plugins/ajaxfileupload/mag.txt`
- **Malware download hosts**: `247.cdnflare.xyz`, `209.141.43.95`
- **Behavior**: writes a web shell into the Magento product-image cache at `pub/media/catalog/product/cache/ss_<10hex>/sync_<10hex>.php` (hash-named directories make one extra file easy to overlook)
- **Shell behavior**: returns **404 to every request without the proper `X-Cache-Token` header**; with the header, it runs any PHP code from the `task` POST parameter
- **OAST callback before writing**: `457cfa2fb7p5.daf892t5qau4og8pi4cghbc6fhm1dim3u.oast.site`
- **Delivery path**: the dropper was recovered from a `Store:` request header, still JSON-escaped from the record Magento logged it into — confirming it entered through StyleSmuggler
- **Durable tell**: `find pub/media -name '*.php'` on any Magento host

### Free detection signal

On hosts where the web user cannot write a crontab, the implant still tries every minute, and every attempt is logged:

```
crontab[<pid>]: (www-data) AUTH (crontab command not allowed)
```

The first such line gives the infection time to the second. Grep auth logs for it.

### Aikido-specific intelligence

Aikido Intel rated StyleSmuggler **critical** before Adobe assigned a CVE, publishing three internal advisory IDs:

- `AIKIDO-2026-248927` — Magento Open Source
- `AIKIDO-2026-123768` — Adobe Commerce
- `AIKIDO-2026-724507` — Magento Cloud metapackage

Aikido Libraries provides a **drop-in patch** (no version upgrade required) for the following branches:

- `2.3.1-p12007002+aikido`
- `2.4.7-p1012007002+aikido`
- `2.4.8-p512007002+aikido`

The patch **sanitizes template styles** before Magento's engine processes them, closing the exact path StyleSmuggler uses to reach the directive and dependency-injection processing. It is applied at two points depending on version. Legitimate CSS passes through untouched.

For non-Aikido customers, the closest official interim mitigation is **disabling GraphQL** (which takes headless / PWA storefronts offline and only hardens against the current attack pattern; the underlying flaw remains open until Adobe ships a real fix).

## Indicators of Compromise

### Malware download
- `https://www.incofar.it/js/jquery/plugins/ajaxfileupload/mag.txt`
- `247.cdnflare.xyz` — malware download host
- `209.141.43.95` — malware download host

### C2 servers
- `99.84.67.186:443` — C2, WebSocket over TLS (original build)
- `windwsecurity.run:443` — remote shell, WebSocket over TLS (TCP)
- `ntp.timesysnc.net:123` — C2, custom NTP-shaped traffic
- `ntp.timesync.to:123` — C2, custom NTP-shaped traffic
- `ntp.synctime.to:123` — C2 fallback
- `ntp.syncstime.to:123` — C2 fallback
- `185.157.160.251:123` — NTP C2 IP (resolves for ntp.timesync.to and ntp.timesysnc.net as of Sep 7)

### OAST
- `457cfa2fb7p5.daf892t5qau4og8pi4cghbc6fhm1dim3u.oast.site`

### Process names (rotating)
- `[kworker/u:8:0]`
- `fc-cache`
- `chronyd`

### File paths
- `~/.local/share/.gvfsd/`
- `~/.cache/fontconfig/fc-cache`
- `/tmp/.kw_*`
- `/tmp/.cache_*`
- `/tmp/.gvfsd-*`
- `/tmp/.fc-*/fc-cache`
- `/tmp/fc-cache`
- `/tmp/.chrony-*/chronyd`
- `~/.local/share/.gvfsd/`
- `pub/media/catalog/product/cache/ss_<10hex>/sync_<10hex>.php`

### Cron entries
- `13,43 * * * *` (fc-cache variant)
- `57,27 * * * *` (chronyd variant)
- Entries written directly into cron spool file (no syslog `REPLACE` line)

### Auth log signal
- `crontab[<pid>]: (www-data) AUTH (crontab command not allowed)`

### Hunt commands
```bash
# Check for the Rust implant
crontab -l | grep -i gvfsd
ls -la ~/.local/share/.gvfsd/ ~/.cache/fontconfig/fc-cache /tmp/.kw_* /tmp/.cache_* /tmp/.gvfsd-* /tmp/.fc-*/fc-cache /tmp/fc-cache /tmp/.chrony-*/chronyd 2>/dev/null
ps -eo pid,comm,args | grep -iE 'kworker|fc-cache|chronyd'
grep -r 'crontab command not allowed' /var/log/
grep -ril 'x_trace_' var/report/

# Check for the PHP web shell
find pub/media -name '*.php'
```

## What merchants should do

1. **Check exposure**: if running Magento Open Source or Adobe Commerce, assume vulnerable. No fixed version exists as of September 7, 2026.
2. **Interim mitigation**: disable GraphQL if you cannot patch immediately (takes headless / PWA storefronts offline).
3. **Apply Aikido Libraries patch** if you are an Aikido customer (drop-in, no version upgrade).
4. **Do not wait for Adobe's September 8 release** — it is not confirmed to cover StyleSmuggler.
5. **Hunt for compromise**: run the hunt commands above; check for the Rust implant process names, cron entries, NTP C2 traffic on port 123, and PHP files under `pub/media/`.
6. **Rotate Magento credentials** if any evidence of compromise is found, since the backdoor has been observed sitting dormant before activating.
7. **Monitor for unexpected "Payment Transaction Failed Reminder" email bursts** — they may indicate the execution stage of an in-progress exploit.
8. **If you use Sansec Shield**: rules went live September 5; attacks before that date may have gotten through — run eComscan 1.9.7 to terminate `[kworker/u:8:0]` processes.

## Adobe status (as of Sep 7, 2026)

- No CVE assigned
- No advisory published
- No patch released
- Most recent Commerce security bulletin: August 11, 2026
- Next scheduled security release: **September 8, 2026** (coverage of StyleSmuggler not confirmed)
- Adobe Enterprise Support confirmed on September 7 that they are working on a patch; no ETA

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — same-day Aikido disclosure of the 111-day Shai-Hulud payload resurfacing, and e-commerce exploitation as a common post-exploitation objective across supply-chain waves

## Sources
- Sansec "StyleSmuggler: Magento and Adobe Commerce 0-day RCE under active attack" (Sep 5, 2026, updated Sep 7 13:29 UTC): [https://sansec.io/research/stylesmuggler](https://sansec.io/research/stylesmuggler)
- Aikido "StyleSmuggler fix: patch the Magento and Adobe Commerce RCE" (Sep 7, 2026): [https://www.aikido.dev/blog/stylesmuggler-fix](https://www.aikido.dev/blog/stylesmuggler-fix)
