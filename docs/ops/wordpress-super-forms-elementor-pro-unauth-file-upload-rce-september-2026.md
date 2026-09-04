# WordPress Super Forms / Elementor Pro unauthenticated file-upload RCE

## Summary
On **September 4, 2026**, The Hacker News reported (from **Wordfence**) that threat actors are actively exploiting **two critical unauthenticated arbitrary-file-upload flaws** in popular WordPress plugins, **Super Forms – Drag & Drop Form Builder** and **Elementor Pro**:

- **CVE-2026-14894** (CVSS 9.8) — missing file-type validation in **Super Forms** that lets an unauthenticated attacker upload files of any type, including executable PHP, leading to remote code execution. **Fixed in 6.3.314.**
- **CVE-2026-32475** (CVSS 9.0/9.8) — the same unauthenticated arbitrary-file-upload-to-RCE class in **Elementor Pro**. **Fixed in 4.2.2.** Details were disclosed by Patchstack in August 2026. Exploitation requires at least one published Elementor page containing a Form widget with a File Upload field.

Wordfence had already blocked **over 440,000 exploit attempts** — more than 250,000 against CVE-2026-14894 and 190,000 against CVE-2026-32475 — indicating coordinated, high-volume in-the-wild scanning and exploitation. The durable pattern is the well-known WordPress **arbitrary file upload → PHP web shell → full site compromise** chain, where a single published upload endpoint becomes an unauthenticated remote-code-execution primitive.

## Tags
- ops
- operations
- WordPress
- Super Forms
- Elementor Pro
- CVE-2026-14894
- CVE-2026-32475
- active exploitation
- unauthenticated
- arbitrary file upload
- PHP web shell
- remote code execution
- patch management

## Why this matters
- WordPress powers a large share of the public internet; unauthenticated RCE in widely installed plugins is an immediate, high-blast-radius target.
- Both flaws are **unauthenticated** — no credentials, no account required. Any exposed instance running an unpatched plugin version is in scope.
- Arbitrary file upload of a PHP payload yields a web shell from which an attacker can create administrator accounts, exfiltrate data, and seize control of the entire site.
- The volume of blocked attempts (440,000+) shows this is not opportunistic but **coordinated active exploitation**, consistent with the WP-SHELLSTORM / webshell-access-brokerage theme in the ecosystem.

## Operational characteristics
- **Affected plugins:** Super Forms – Drag & Drop Form Builder (CVE-2026-14894); Elementor Pro (CVE-2026-32475).
- **Vulnerability class:** missing/insufficient file-type validation on an upload endpoint → unauthenticated attacker uploads a PHP file of any type → remote code execution.
- **CVSS:** CVE-2026-14894 = 9.8; CVE-2026-32475 = 9.0/9.8.
- **Exploit status:** active, high-volume in-the-wild exploitation per Wordfence.
- **Attack mechanics (Super Forms, CVE-2026-14894):** attacker issues an HTTP POST to `/wp-admin/admin-ajax.php` using the `super_submit_form` action, submitting a file field with a Base64-encoded PHP payload and an attacker-controlled filename. The Base64 blob observed in the wild decodes to PHP that moves the uploaded file to an attacker-chosen target name and echoes a confirmation string (e.g. "Upload: <a href='$target'>$target</a>"), confirming the web shell landed.
- **Precondition (Elementor Pro, CVE-2026-32475):** target must have at least one published Elementor page with a Form widget containing a File Upload field.
- **Fixed versions:** Super Forms **6.3.314**; Elementor Pro **4.2.2**.
- **Public attribution:** no actor named in the reviewed public sources; preserve the "coordinated active exploitation" read without asserting operator identity.

## Defender heuristics
- Immediately update Super Forms to 6.3.314 and Elementor Pro to 4.2.2 on every WordPress instance; these are the only reliable controls.
- Inventory instances that run either plugin and confirm the fixed version is actually loaded (not just the latest available) — check the active plugin version, not the changelog.
- Hunt for PHP files that were newly written to writable web-root or upload directories by non-administrative / anonymous sessions, and for `admin-ajax.php` `super_submit_form` / Elementor Form-widget upload POSTs with Base64 payloads or unusual MIME types.
- Look for web-shell indicators: `move_uploaded_file`-style handlers, `@unlink` self-deletion patterns, obfuscated/Base64-eval PHP, new `.php` files with unexpected names, and the "Upload: <a href=..." confirmation strings in response bodies.
- For unpatched instances, temporarily disable the vulnerable upload endpoints (remove File Upload fields, restrict the form action, or apply a WAF rule that blocks executable-MIME / PHP-payload uploads on `admin-ajax.php`) until the fix is deployed.
- If compromise is suspected, treat it as full-site takeover: review admin users, cron jobs, plugins/themes for backdoors, and correlate with the exploit-attempt window.

## Related pages
- [Elementor Pro CVE-2026-32475 disclosure + WordPress 7.0.4 CVE-2026-65640 (root-cause detail, Aug 18–20, 2026)](elementor-pro-cve-2026-32475-unauthenticated-rce-wordpress-704.md)
- [WordPress five-flaw critical batch (WPMU DEV / Avada / TranslatePress / Pods / GiveWP)](wordpress-wpmu-dev-avada-translatepress-pods-givewp-critical-batch-august-29-2026.md)
- [WordPress wp2shell CVE-2026-63030 / CVE-2026-60137 exploitation](wordpress-wp2shell-cve-2026-63030-60137-exploitation.md)
- [Wordfence vulnerability intelligence source entry](../notes/source-index.md)

## Sources
- The Hacker News summary: [https://thehackernews.com/2026/09/over-440000-exploit-attempts-target.html](https://thehackernews.com/2026/09/over-440000-exploit-attempts-target.html)
- NVD: [https://nvd.nist.gov/vuln/detail/CVE-2026-14894](https://nvd.nist.gov/vuln/detail/CVE-2026-14894)
- NVD: [https://nvd.nist.gov/vuln/detail/CVE-2026-32475](https://nvd.nist.gov/vuln/detail/CVE-2026-32475)
