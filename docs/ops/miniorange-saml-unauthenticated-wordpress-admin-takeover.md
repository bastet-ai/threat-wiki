# miniOrange SAML 2.0 SSO plugin: unauthenticated flaws grant WordPress admin access (active exploitation)

## Summary
Per The Hacker News (August 25, 2026), attackers are **actively exploiting two severe unauthenticated authentication-bypass flaws** in the **Xecurify miniOrange SAML 2.0 Single Sign On WordPress plugin** (disclosed by Patchstack, reported by the DigitalOcean security team):
- **CVE-2026-61979** (CVSS 8.1) — unauthenticated privilege escalation via **signature-algorithm confusion**; fixed in **17.0.5** (Standard edition).
- **CVE-2026-15981** (CVSS 9.8) — authentication bypass via **accepting malformed SAML signatures as valid**: `mo_saml_validate_signature()` performs a loose boolean check on PHP `openssl_verify()`'s tri-state integer return, so an error return of **-1 is evaluated as truthy** and treated as successful verification. A crafted `SAMLResponse` with an attacker-controlled `NameID` and a deliberately malformed signature makes the plugin call `wp_set_auth_cookie()` for the targeted account — **any existing WordPress user, including administrators**.

**Exploitation is confirmed in the wild:** Patchstack observed anomalous WordPress administrator session attempts originating from DigitalOcean's trusted network after an attacker used the bypass to obtain a WordPress admin session cookie (the attack stalled at the admin panel, which was restricted behind the trusted network). Scan activity came from `207.211.214.41`, `79.127.224.14`, `102.91.71.83`, `162.243.116.148`, `84.201.6.54`, `64.225.25.188`; Patchstack assesses the spread as **opportunistic scanning** rather than a targeted campaign. A **public PoC that chains the two flaws to gain admin privileges is available**.

## Tags
- ops
- operations
- WordPress
- miniOrange
- Xecurify
- SAML
- SSO
- Patchstack
- DigitalOcean
- CVE-2026-15981
- CVE-2026-61979
- openssl_verify
- loose boolean check
- malformed signature
- authentication bypass
- privilege escalation
- admin takeover
- active exploitation
- opportunistic scanning
- PoC available

## Exploitation mechanics
- **CVE-2026-15981 (primary):** submit a crafted SAML response to the plugin with a malformed signature; `openssl_verify()` returns -1 (error), the plugin's tri-state-ignoring boolean check treats it as valid, and `wp_set_auth_cookie()` logs in the attacker as the targeted user's `NameID` — no credential needed.
- **CVE-2026-61979 (companion):** signature-algorithm confusion allows unauthenticated privilege escalation (e.g., to administrator), enabling the PoC chain from the bypass to full admin control.

## Indicators
- **Scanner source IPs (Patchstack):** `207.211.214.41`, `79.127.224.14`, `102.91.71.83`, `162.243.116.148`, `84.201.6.54`, `64.225.25.188`.
- **Behavior:** SAML `SAMLResponse` POSTs carrying attacker-controlled `NameID` values and malformed/invalid signature fields targeting WordPress sites with the miniOrange SAML SSO plugin; subsequent admin session activity from unexpected source IPs.

## Defender heuristics
1. **Patch now:** update the Xecurify miniOrange SAML 2.0 SSO plugin to ≥ 17.0.5 (CVE-2026-61979) and ≥ 17.0.6 (CVE-2026-15981, Standard edition) — both are unauthenticated and a public chainable PoC exists.
2. **Hunt the signature-error primitive:** alert on any SAML `SAMLResponse` accepted where the signature verification library returned an error status; for WordPress + miniOrange specifically, alert on `wp_set_auth_cookie()` calls where the preceding SAML validation logged an `openssl_verify` error.
3. **Assume admin access was achieved on any hit site:** review post-auth activity (user/role changes, plugin installs, theme edits, webhook/backup creation, cron jobs, outbound exfiltration) from the first anomalous SAML POST.
4. **Correlate scanner IPs** across the WordPress estate; the listed IPs are opportunistic — expect recurrence and additional source addresses.
5. **Broader lesson for PHP integrations:** tri-state / int-returning verification functions compared with loose booleans are a recurring auth-bypass class — audit `openssl_verify`, `hash_hmac`/`sodium` result handling, and `xmlsec`-style checks in any in-house SAML/OIDC bridge.

## Assessment limits
- Patchstack's "opportunistic scanning" assessment reflects the observed spread; the single stalled DigitalOcean incident is the only confirmed victim-side exploitation datapoint as of August 25, 2026.
- Affected-version ranges beyond the "fixed in 17.0.5 / 17.0.6 (Standard edition)" statement are not fully published at capture; verify against the plugin changelog before scoping.

## Related pages
- [Keycloak CVE-2026-18963 unauthenticated password-reset account takeover](../tools/keycloak-cve-2026-18963-unauthenticated-account-takeover.md)
- [Elementor Pro CVE-2026-32475 unauthenticated RCE](../ops/elementor-pro-cve-2026-32475-unauthenticated-rce-wordpress-704.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)

## Sources
- The Hacker News: [Attackers Target miniOrange SAML Flaws That Can Grant WordPress Admin Access](https://thehackernews.com/2026/08/attackers-target-miniorange-saml-flaws.html)
- Patchstack advisory (CVE-2026-61979, CVE-2026-15981)
