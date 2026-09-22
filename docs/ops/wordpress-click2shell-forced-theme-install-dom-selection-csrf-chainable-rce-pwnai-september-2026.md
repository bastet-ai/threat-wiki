# WordPress "Click2Shell": one link opened by a logged-in admin force-installs an attacker-chosen wp.org theme with no clicks — session-privilege CSRF through the software's own install button, chainable to RCE via a second theme flaw (pwn.ai, patched in 7.1.1, Sep 17, 2026)

## Summary

WordPress shipped a security release **7.1.1 on September 17, 2026** fixing a flaw pwn.ai calls **Click2Shell**: a crafted link, opened by a **logged-in administrator**, causes WordPress's **own JavaScript to press the Install button** for a theme the attacker picks from the official WordPress.org directory — no clicks, no CSRF token theft (the admin's own session supplies the nonce). The installed theme stays deactivated, so nothing visibly changes on the site. The core bug alone does not accept an arbitrary theme ZIP; **code execution requires chaining a second, separate weakness in the installed theme** — the same "one primitive installs the stage, another runs it" shape as the on-wiki wp2shell chain. No in-the-wild exploitation reported. The durable read is the mechanism: **two components read the same URL differently** — the wp.org API treats a parameter as a plain theme slug and returns a legitimate theme, while the admin page reuses the raw attacker text, punctuation included, inside DOM-selection code, so injected characters redirect the script's own click target. The privileged action executes with the platform's blessing because the platform is the one performing it.

## Tags
- ops
- vulnerability
- wordpress
- click2shell
- csrf
- session-privilege-abuse
- DOM-selection-injection
- theme-install
- rce-chain
- pwn-ai
- client-side
- confused-deputy

## Mechanism (from pwn.ai via The Hacker News)

1. Attacker crafts a link whose parameter carries a legitimate wp.org theme slug **plus punctuation/characters**.
2. The WordPress.org directory endpoint treats the value as an ordinary theme name and **returns a real theme** — from the server's perspective this is a valid request.
3. The admin page **reuses the original text verbatim inside code meant to select a page element** to pick the install target; attacker-added characters steer that selection onto the **Install button**, and WordPress's own script clicks it.
4. The admin is already authenticated, so **their session supplies the permission and the security token** — the attacker needs neither.
5. Result: an attacker-chosen official-directory theme is installed and left deactivated (site appearance unchanged; nothing looks wrong).
6. To reach code execution the attacker needs a **second flaw in the installed theme** (e.g., reached when WordPress builds a preview). pwn.ai demonstrated the full chain against a theme weakness; core alone is install-only.

## Why it matters (durable reads)

1. **Session-privilege CSRF is the modern shape of "the CSRF token protected us":** the classic defense assumes the attacker can't supply a valid nonce — here the victim's own session provides it because the site's own script performs the privileged action. Any admin UI where **URL-controlled text reaches DOM element selection for a privileged button** is the same bug class, in any CMS or admin console.
2. **Two parsers, one string** — an API path that sanitizes-as-slug and a front end that re-embeds the raw value is the recurring split-brain pattern (compare the Netty five-bytes-short guard and GitPython config re-serialization both on-wiki from OX Security: same component family reading the same data with different assumptions).
3. **Install-then-chain is the supply-chain-adjacent web-CMS playbook:** installing an attacker-CHOSEN but legitimate directory artifact keeps the "malicious file" detectors blind; the second-stage theme weakness (or an attacker-uploaded theme update) does the damage. Defender check: theme inventory ≠ just activated themes; **installed-but-inactive themes are an attack surface** — diff the `wp-content/themes` directory against an approved list, not the dashboard.
4. This lands in the same WordPress security lane as **wp2shell** (Wiz, July 2026, CVE-2026-63030 / CVE-2026-60137, in KEV and on-wiki): the pattern of WordPress-core bugs as RCE prefixes continues; patch cadence for core security releases stays a standing priority.

## Defender actions

- **Update to WordPress 7.1.1 now** — security release, vendor advises immediate update.
- Hunt unexpected **installed-but-inactive themes**, especially on dates preceding admin clicks of unusual links; correlate `wp-content/themes` additions against the approved set.
- For custom admin UIs: audit anywhere a URL/parameter value is interpolated into DOM queries or jQuery selectors that gate privileged actions.
- No ITW exploitation reported; treat KEV addition as a monitor item, not current state.

## <a id="september-22-sibling-flaw-comment2shell"></a>September 22 follow-up: the SIBLING flaw in the same 7.1.1 release — "Comment2Shell" (CVE-2026-93485), anonymous-comment XSS that becomes RCE when an admin merely views the page (Patchstack, 7.1, fixed 7.1.1)

The Hacker News's Sep 22 write-up (full text captured by this wiki) surfaced the **other** comment vector fixed in the same September 17 WordPress 7.1.1 release: **CVE-2026-93485 "Comment2Shell"** (Patchstack-assigned, **CVSS 7.1**, affected **4.7 → 7.1**, branch fixes 7.1.1 / 7.0.5 / 6.9.8 / back to 4.7.36).

- **Mechanism:** WordPress sanitizes a comment **at save time**, then **reformats it at render time** — the flaw lived in the gap between the two passes. A **line break inside an attribute of an allowed HTML tag** survives the save-time check; during display reformatting one step splits the tag and relocates attacker text into position where the browser parses it as a **live event handler**, which fires **on page load with no click**, executing with **whatever privileges the viewing browser holds**.
- **The RCE condition is the same privileged-session reuse as Click2Shell:** the script only needs a **logged-in administrator to open the page carrying the comment** — then it uses the admin's own session to upload a plugin containing a web shell (the known browser-to-server path). Theme install here, plugin upload there: the 7.1.1 release fixed **two** primitives that both end at "the platform performs a privileged action with the viewer's own credentials."
- **Preconditions and their real strength:** works on **block themes** (or classic themes that format comments the same way), not all themes. WordPress described exploitation as "subject to comment approval" — but **comment moderation is off by default** and the hold-first-time-commenter setting is workable-around, so the comment can reach the page unapproved; Patchstack's formulation is the durable one: **"moderation isn't a security control."**
- **State:** no in-the-wild exploitation, **not KEV-listed** at this wiki's Sep 22 check (KEV 2026.09.21 / 1,717). Reported by Rafie Muhammad, full write-up Sep 21. 7.1.1 fixed 11 security issues total; Comment2Shell was the **only anonymous-attacker-reachable** one. The same release carried Click2Shell (this page's subject).
- **Durable read:** *sanitize-then-reformat* is a class, not a WordPress bug — a security check that runs on one representation of untrusted data while the renderer emits another representation reopens the exact hole the check was supposed to close. This is the same "two components read the same value differently" family as this page's Click2Shell DOM-selection mechanism and the OX Security four-CVE trust-failure page.
- **Defender delta to this page's actions:** the Click2Shell hunt (unexpected installed themes) now needs a sibling: on unpatched 4.7–7.1 sites, hunt **unexpected plugin uploads / new files under `wp-content/plugins`** correlated with admin page views of comment-bearing posts, and treat "comments closed" as the interim mitigation Patchstack/WordPress name (close comments site-wide or per-post if you cannot update immediately).

## Caveats

- pwn.ai's naming and chain details are relayed via The Hacker News (Sep 18, 2026); the specific chained theme weakness was described without naming the theme in the coverage checked at scan time.
- CVSS/CVE assignments for the core issue were not in the relayed coverage; the WordPress 7.1.1 security release is the authoritative fix reference.

## Related pages

- [Wiz wp2shell active exploitation](wordpress-wp2shell-cve-2026-63030-60137-exploitation.md) — prior WordPress-core-as-RCE-prefix campaign
- [Four critical trust-failure CVEs (OX Security)](../tools/four-critical-trust-failure-cves-netty-sni-fallback-gitpython-hookspath-ox-september-2026.md) — same "two readers, one value" family

## Sources

- The Hacker News, "New WordPress Click2Shell Flaw Forces Theme Installs, Can Chain to Code Execution," September 18, 2026: <https://thehackernews.com/2026/09/new-wordpress-click2shell-flaw-forces.html>
- pwn.ai research (via THN); WordPress 7.1.1 security release, September 17, 2026.
