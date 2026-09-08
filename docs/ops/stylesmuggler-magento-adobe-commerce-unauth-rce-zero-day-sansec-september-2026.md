# StyleSmuggler (CVE-2026-75650): Magento / Adobe Commerce unauthenticated RCE zero-day under active attack — Adobe emergency hotfix VULN-39341 (APSB26-146) (Sansec, Sep 5; Adobe, Sep 7, 2026)

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
- CVE-2026-75650
- APSB26-146
- patch
- credential rotation

## Summary

On **September 5, 2026**, Sansec published **StyleSmuggler**, an **unauthenticated remote-code-execution zero-day** in **every current version of Magento Open Source and Adobe Commerce** (including 2.4.9, the latest release). Attacks began **September 4, 2026, 22:40 UTC** — a day before public disclosure. **On September 7, 2026 at 20:20 UTC, Adobe published emergency advisory [APSB26-146](https://helpx.adobe.com/security/products/magento/apsb26-146.html)** (priority 1, its highest) assigning the flaw **CVE-2026-75650**, scored **CVSS 10.0** (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H), and shipped the fix as an **emergency composer hotfix, `VULN-39341`, not a full release**. Every version from **2.4.4 through 2.4.9** (Adobe Commerce, Magento Open Source) and **Adobe Commerce B2B 1.3.3–1.5.3** is affected; older versions in those branches are also affected but the hotfix is unverified on them. Because the backdoor sits on disk and may have been weaponized, **patching does not clean a compromised store — rotation and compromise-hunting are mandatory alongside the hotfix** (details in [Adobe patch / rotation checklist](#adobe-patch-apsb26-146-and-rotation-checklist)).

The exploit is **two-stage**, both stages abusing Magento functionality that already exists:

1. **Stage 1 — inject:** An unauthenticated attacker sends a **GraphQL request** whose `styles` property carries an injected PHP payload. The payload does **not** execute immediately. It is written into a file that Magento generates itself (for example a **checkout failure report**).
2. **Stage 2 — execute:** The poisoned file is later rendered when Magento processes a **"Payment Transaction Failed Reminder" email**. The email does not need to be delivered — the code runs **server-side during template rendering**. The attack completes even if the message never reaches an inbox.

**All in-range versions are vulnerable**: Adobe's advisory places the affected range at **2.4.4–2.4.9** (plus B2B 1.3.3–1.5.3). Sansec reproduced the full unauthenticated chain on clean installs of **2.4.7, 2.4.8, and 2.4.9**. One confirmed victim was running **2.4.6-p15** with the July and August 2026 security patches fully applied and `security:patch-status` clean — patch status did not save it. Moving sessions to Redis or the database does **not** stop the attack (an operator was observed failing once against session storage, then succeeding eight seconds later by routing the payload through a file uploaded via Magento custom options).

Confirmed intrusions have installed a **persistent Rust-based backdoor** disguised as a kernel thread. It survives a reboot and sits dormant for hours to days before activating. From there, the exposure is everything unauthenticated RCE on an e-commerce platform implies: **customer PII, payment transaction details, admin credentials, database contents, and a route to Magecart-style skimmer injections** against shoppers.

## Why this matters

- **Mass attack surface.** Magento and Adobe Commerce power a very large fraction of the world's e-commerce sites. An unauthenticated RCE with CVSS 10.0 is a mass-compromise vector, not a single-site incident.
- **Now patched, but the patch is a hotfix and the compromise window already passed.** Adobe shipped the fix as **`VULN-39341`** (emergency composer hotfix under [APSB26-146](https://helpx.adobe.com/security/products/magento/apsb26-146.html), Sep 7 20:20 UTC) covering **2.4.4–2.4.9** (Adobe Commerce + Magento Open Source) and **B2B 1.3.3–1.5.3** — no full release. Until the hotfix is applied, the interim mitigations remain **disabling GraphQL** (which takes headless / PWA storefronts offline) or the Aikido Libraries drop-in patch. **Patching closes the front door but does not remove a live backdoor** — Sansec observed operators rotating payloads several times a day, so assume any store exploited since Sep 4 is compromised until proven otherwise.
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

Per Adobe APSB26-146 (Sep 7, 2026), the hotfix `VULN-39341` was tested against the **2026-aug** releases of:

- **Adobe Commerce**: 2.4.4 → 2.4.9
- **Magento Open Source**: 2.4.4 → 2.4.9
- **Adobe Commerce B2B**: 1.3.3 → 1.5.3

Older versions within those branches are affected too, but the patch is **unverified** on them. Sansec independently reproduced the full unauthenticated chain on clean installs of **2.4.7, 2.4.8, and 2.4.9**; one confirmed victim ran **2.4.6-p15** with the July + August 2026 patches applied and `security:patch-status` clean — patch status did not save it. A Shield-blocked probe against a **2.4.7-p10** store on Sep 7 confirmed the current patch level is no defense.

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

1. **Apply the Adobe hotfix now**: download `VULN-39341-composer-patches.zip` from `repo.magento.com` and apply it as a composer patch. Confirm: `vendor/bin/magento-patches -n status | grep "39341\|Status"`.
2. **Rotate credentials per Adobe's checklist** — starting with the **encryption key**, then every credential that key protected: admin passwords, REST/SOAP/GraphQL integration tokens, OAuth client secrets, payment gateway API credentials, database credentials, SSH and deploy keys, and third-party extension API keys. **Rotate at the source, not only inside Magento** — rotating the encryption key alone does not invalidate anything an attacker already read.
3. **Scan for compromise before assuming you are in the clear**: stores were being exploited for **three days before the hotfix existed** (attacks began Sep 4 22:40 UTC; hotfix published Sep 7 20:20 UTC). Run the hunt commands above plus eComscan (Sansec Shield blocks every observed StyleSmuggler variant, but the patch should still be installed — the attack surface behind the bug is large).
4. **Interim mitigation if you cannot patch immediately**: disable GraphQL (takes headless / PWA storefronts offline) or apply the Aikido Libraries drop-in patch.
5. **Hunt for the backdoor**: check for the Rust implant process names (`[kworker/u:8:0]`, `fc-cache`, `chronyd`), direct cron-spool entries, NTP-shaped UDP/123 C2 to `185.157.160.251`, and PHP files under `pub/media/`.
6. **Monitor for unexpected "Payment Transaction Failed Reminder" email bursts** — they may indicate the execution stage of an in-progress exploit.
7. **If you use Sansec Shield**: rules went live September 5; attacks before that date may have gotten through.

## Adobe patch (APSB26-146) and rotation checklist

Published **September 7, 2026, 20:20 UTC** — priority 1 (Adobe's highest rating).

- **Advisory**: [APSB26-146](https://helpx.adobe.com/security/products/magento/apsb26-146.html)
- **CVE**: **CVE-2026-75650** — "Adobe Commerce is affected by an Improper Neutralization of Special Elements Used in a Template Engine vulnerability that could result in arbitrary code execution" (NVD, published 2026-09-07T21:17Z)
- **CVSS**: **10.0** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` (scope Changed — e-commerce scope impact: customer PII, payment data, admin credentials)
- **Fix form**: emergency **composer hotfix** `VULN-39341` (`VULN-39341-composer-patches.zip` from `repo.magento.com`), applied as a composer patch — **not** a full Commerce release; the scheduled Sep 8 release is moot for this flaw
- **Verified against** (2026-aug releases): Adobe Commerce 2.4.4–2.4.9, Magento Open Source 2.4.4–2.4.9, Adobe Commerce B2B 1.3.3–1.5.3; older in-branch versions unverified
- **Credential rotation checklist** (Adobe): encryption key → admin passwords → REST/SOAP/GraphQL integration tokens → OAuth client secrets → payment gateway API credentials → database credentials → SSH/deploy keys → third-party extension API keys; rotate each **at the source**

Sansec's position (Sep 7, 20:45 UTC): install the Adobe patch **and** deploy Sansec Shield; the operators changed payloads several times a day since September 4, and the backdoor is not recognized by any security vendor other than Sansec.

## Adobe status timeline

- **Sep 4, 22:40 UTC**: attacks begin (no public knowledge)
- **Sep 5**: Sansec publishes StyleSmuggler; no CVE, no advisory, no patch
- **Sep 7, (earlier)**: Aikido follow-up with drop-in Libraries patches; Adobe still silent
- **Sep 7, 20:20 UTC**: **Adobe publishes APSB26-146 / CVE-2026-75650 (CVSS 10.0) with hotfix VULN-39341**
- Most recent prior Commerce security bulletin: August 11, 2026

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — same-day Aikido disclosure of the 111-day Shai-Hulud payload resurfacing, and e-commerce exploitation as a common post-exploitation objective across supply-chain waves

## Sources
- Sansec "StyleSmuggler: Magento and Adobe Commerce 0-day RCE (CVE-2026-75650) under active attack" (Sep 5, 2026, last updated Sep 7 20:45 UTC, including the Adobe patch section): [https://sansec.io/research/stylesmuggler](https://sansec.io/research/stylesmuggler)
- Adobe Security Bulletin APSB26-146 (Sep 7, 2026, 20:20 UTC): [https://helpx.adobe.com/security/products/magento/apsb26-146.html](https://helpx.adobe.com/security/products/magento/apsb26-146.html)
- NVD CVE-2026-75650 (published 2026-09-07T21:17Z; CVSS 3.1 10.0, S:C)
- Aikido "StyleSmuggler fix: patch the Magento and Adobe Commerce RCE" (Sep 7, 2026): [https://www.aikido.dev/blog/stylesmuggler-fix](https://www.aikido.dev/blog/stylesmuggler-fix)
