# WordPress batch: WPMU DEV Dashboard, Avada, TranslatePress, Pods, GiveWP — five critical unauthenticated flaws

## Summary
On **August 29, 2026**, Wordfence and Patchstack (via The Hacker News) reported a batch of **five critical WordPress plugin/theme flaws** that all allow **unauthenticated attackers** to reach site takeover or arbitrary code execution: **WPMU DEV Dashboard** (authentication bypass, **CVE-2026-76581**, 9.8), **Avada** theme with **Fusion Builder** (arbitrary file write → RCE, **CVE-2026-18431**, 9.8), **TranslatePress** (administrator password-reset URL exposure, **CVE-2026-19632**, 9.8), **Pods** (authorization-bypass privilege escalation, **CVE-2026-19598**, 9.8), and **GiveWP** (PHP object injection → RCE, **CVE-2026-82222**, 10.0). NVD records confirm all five; fixed releases: WPMU DEV Dashboard `> 5.0.1`, Avada `> 7.16` (with Fusion Builder `> 3.16`), TranslatePress `> 3.3.1`, Pods `> 3.3.9`, GiveWP `> 4.16.7.1`. As of the August 29 reporting, no active in-the-wild exploitation of this batch was named.

## Tags
- ops
- operations
- WordPress
- WPMU DEV Dashboard
- Avada
- Fusion Builder
- TranslatePress
- Pods
- GiveWP
- CVE-2026-76581
- CVE-2026-18431
- CVE-2026-19632
- CVE-2026-19598
- CVE-2026-82222
- authentication bypass
- arbitrary file write
- privilege escalation
- PHP object injection
- unauthenticated RCE
- web application
- CMS

## Why this matters
- Five widely installed components (a dashboard/SSO plugin, a top-10 theme, a top multilingual plugin, a custom-fields plugin, and a top donation plugin) each have a **separate unauthenticated path to administrator takeover or RCE** — a single scanner pass can take over most of a typical WordPress stack.
- Three of the five flaws are **structural access-control mistakes** that recur across the ecosystem: an HMAC signed over an ambiguous concatenated field (WPMU DEV Dashboard), an error handler that logs instead of halting every access check (Pods), and a "safe unserialize" helper that does not strip objects (GiveWP). These are the same classes that make WordPress batch CVEs repeatedly exploitable.
- GiveWP's 10.0 object-injection chain is the highest-severity item: any site with **one published donation form and one active payment gateway** meets the prerequisites, which covers essentially all GiveWP installs.

## Operational characteristics
### CVE-2026-76581 — WPMU DEV Dashboard (≤ 5.0.1) — 9.8
- **Flaw:** inconsistent HMAC message construction between the unauthenticated `wdpsso_step1` and `wdpsso_step2` AJAX actions. Step 1 signs an **unseparated concatenation** of token, state, redirect, and domain; step 2 verifies a concatenation that **omits the domain field**.
- **Exploit:** an attacker obtains a valid HMAC from step 1 and replays it to step 2 by **moving the domain value into the redirect field** — yielding an authenticated administrator session.
- **Prerequisite:** the site is connected to WPMU DEV with **Hub SSO enabled and mapped to an administrator**.
- **Fix:** update WPMU DEV Dashboard above `5.0.1`; until patched, sites with Hub SSO mapped to admins should restrict WPMU DEV Dashboard access or disable Hub SSO.

### CVE-2026-18431 — Avada (≤ 7.16) + Fusion Builder (≤ 3.16) — 9.8
- **Flaw:** a chain of authorization and input-validation weaknesses **across the Avada theme and the Fusion Builder plugin** allows an unauthenticated attacker to write attacker-controlled files to the server.
- **Exploit:** write an arbitrary PHP file and execute it — full site compromise.
- **Prerequisite:** both Avada and Fusion Builder installed **and active**, plus certain administrator-authored content present.
- **Fix:** Avada above `7.16` and Fusion Builder above `3.16` (the NVD wording scopes the flaw to the ≤ 7.16 / ≤ 3.16 combination; update both).

### CVE-2026-19632 — TranslatePress (≤ 3.3.1) — 9.8
- **Flaw:** the unauthenticated `trp_get_translations_regular` AJAX action exposes the **raw administrator password-reset URL** — plaintext reset key and login parameters — when it is persisted in the translation dictionary table.
- **Prerequisite:** **automatic string saving enabled (the default)** **and** the target administrator's profile locale set to a **published secondary language** (the condition that causes the reset URL to be stored as a translatable string).
- **Fix:** TranslatePress above `3.3.1`; also audit any site where admin password-reset links may have been translated/cached.

### CVE-2026-19598 — Pods (≤ 3.3.9) — 9.8
- **Flaw:** the `pods_admin` AJAX router funnels **every access check** (method allowlist, nonce verification, login enforcement, capability gate) through `pods_error()`, which under the JSON meta-box-loader compatibility path **only writes failures to the PHP error log and returns false instead of terminating the request** — making all guards ineffective.
- **Exploit:** unauthenticated privilege escalation to Administrator, or overwrite of any user's password (including the site owner's), complete site takeover, or any other administrator action.
- **Fix:** Pods above `3.3.9`.

### CVE-2026-82222 — GiveWP (≤ 4.16.7.1) — 10.0
- **Flaw (Patchstack):** the chain combines a **broken "safe unserialize" helper**, a donation flow that feeds that helper attacker-controlled data, and a **gadget chain in code GiveWP ships** — PHP object injection to remote code execution: "a place to store an attacker-controlled serialized object, code that later unserializes it, and a gadget chain in loaded classes."
- **Prerequisite:** one published donation form and one active payment gateway (i.e., a normal configured GiveWP site).
- **Root-cause pattern (Patchstack):** trusting a serialization sanitizer that does not strip objects, unserializing data read back from the database as if trusted, and shipping development-only libraries into production that provide ready-made gadget chains.
- **Fix:** GiveWP above `4.16.7.1`.

## Defender heuristics
- **Patch order by blast radius:** GiveWP (10.0, near-universal prerequisites) → WPMU DEV Dashboard (admin SSO mapping) → Avada/Fusion Builder → Pods → TranslatePress.
- Hunt for exploitation **before** patching: unauthenticated requests to `wdpsso_step1` / `wdpsso_step2`, `trp_get_translations_regular`, `pods_admin` JSON meta-box-loader paths, unexpected administrator logins, new admin accounts created out-of-band, unexpected PHP files in theme/plugin directories (Avada write), and object-injection marker patterns in donation-form submissions (GiveWP).
- For GiveWP specifically, inspect the serialized storage of donation-form data for attacker-controlled serialized objects and treat any recent admin action on a site with GiveWP ≤ 4.16.7.1 as potentially attacker-driven.
- Rotate WordPress admin passwords, application passwords, and hosting-panel credentials after any confirmed exploitation; preserve web logs, filesystem mtimes, and the WordPress user/option tables before cleanup.
- WAF / virtual patching can buy time for the AJAX-action endpoints (by name and parameter shape), but do not treat it as a substitute for the plugin/theme updates.
- Generalize the three recurring anti-patterns when reviewing other plugins: (a) HMAC/nonce messages over unseparated field concatenations, (b) central error handlers that swallow security failures, (c) "safe" unserialize helpers that still accept objects.

## Related pages
- [Elementor Pro CVE-2026-32475 unauthenticated RCE and WordPress 7.0.4](elementor-pro-cve-2026-32475-unauthenticated-rce-wordpress-704.md)
- [WP Maps Pro CVE-2026-8732 exploitation](wp-maps-pro-cve-2026-8732-exploitation.md)
- [WordPress wp2shell CVE-2026-63030 / CVE-2026-60137 exploitation](wordpress-wp2shell-cve-2026-63030-60137-exploitation.md)

## Sources
- The Hacker News, "Five Critical WordPress Plugin and Theme Flaws Enable Site Takeover or RCE," 2026-08-29 (Wordfence / Patchstack reporting): [https://thehackernews.com/2026/08/five-critical-wordpress-plugin-and.html](https://thehackernews.com/2026/08/five-critical-wordpress-plugin-and.html)
- NVD records: [CVE-2026-76581](https://nvd.nist.gov/vuln/detail/CVE-2026-76581), [CVE-2026-18431](https://nvd.nist.gov/vuln/detail/CVE-2026-18431), [CVE-2026-19632](https://nvd.nist.gov/vuln/detail/CVE-2026-19632), [CVE-2026-19598](https://nvd.nist.gov/vuln/detail/CVE-2026-19598), [CVE-2026-82222](https://nvd.nist.gov/vuln/detail/CVE-2026-82222)
- Wordfence threat-intel records: [WPMU DEV Dashboard](https://www.wordfence.com/threat-intel/vulnerabilities/id/3d4321c8-15a4-46f5-9b0e-2098a7fcfb5b?source=cve), [Avada](https://www.wordfence.com/threat-intel/vulnerabilities/id/5bef5bd3-8ec9-4a5b-bcdd-98952c7ef390?source=cve), [TranslatePress](https://www.wordfence.com/threat-intel/vulnerabilities/id/4f4ebf09-b089-4118-a0ee-399243253f9c?source=cve), [Pods](https://www.wordfence.com/threat-intel/vulnerabilities/id/3628032a-3121-45a7-8a78-cfcd8ba6af2f?source=cve)
- Patchstack, "Unauthenticated PHP Object Injection to Remote Code Execution on GiveWP" (CVE-2026-82222): [https://patchstack.com/articles/unauthenticated-php-object-injection-to-remote-code-execution-on-givewp](https://patchstack.com/articles/unauthenticated-php-object-injection-to-remote-code-execution-on-givewp)
