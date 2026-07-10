# WP-SHELLSTORM webshell access brokerage

## Summary
SOCRadar's July 2026 report describes **WP-SHELLSTORM**, a financially motivated webshell access-brokerage operation exposed when an operator left a Python SimpleHTTPServer directory open for 22 days. The exposed server at `137.175.93[.]126` contained roughly 800 MB across 434 files, including webshells, exploit scripts, scan results, bash history, and C2 configuration.

SOCRadar reports over **1.4 million targeted domains**, **27 weaponized CVEs**, more than **5,700 active webshells**, and a parallel Java / Nacos campaign affecting 11 victims across 9 organizations with 613 Nacos configuration files exfiltrated.

## Tags
- ops
- WordPress
- Joomla
- Nacos
- webshells
- access broker
- vulnerability exploitation
- exposed attacker infrastructure
- SimpleHTTPServer exposure
- FOFA
- Chinese-speaking cybercrime
- WP-SHELLSTORM
- Breeze Cache Cleaner
- ThemeREX Addons
- Joomla JCE
- CVE-2026-48907
- SOCRadar
- The Hacker News

## Why this matters
- Exposed attacker infrastructure gave defenders a rare view into the full operational workflow: target lists, exploit selection, shell naming, credential reuse, and cleanup attempts.
- WP-SHELLSTORM is not only WordPress noise. The same staging environment also exposed a quieter enterprise Java / Nacos credential-theft campaign.
- SOCRadar's numbers show why patch priority must consider exploit productivity, not just CVSS or target count: Breeze Cache Cleaner generated far more confirmed shells than broader Joomla JCE spray activity.
- Webshell access brokerage creates downstream ransomware, carding, SEO poisoning, data theft, and botnet risk even when the initial exploit appears to hit “just a CMS.”

## Reported scale and exploitation
| Metric | SOCRadar-reported value |
| --- | --- |
| Target domains identified | 1.4M+ |
| Weaponized CVEs | 27 |
| Critical CVEs | 14 |
| High-severity CVEs | 9 |
| Active webshells confirmed | 5,700+ |
| Open-directory exposure | 22 days |
| Parallel Nacos campaign victims | 11 victims across 9 organizations |
| Nacos configuration files exfiltrated | 613 |

SOCRadar reported Breeze Cache Cleaner as the most productive single exploit, with more than 45,000 targets and 17,000+ confirmed shells. ThemeREX Addons produced 3,378 shells from 46,600 targets. Joomla JCE was sprayed at more than 560,000 targets but produced only 77 confirmed shells in SOCRadar's analysis.

## Actor clues and operational security failures
- The exposed directory included `/home/tance` and `/root` material from a US-based VPS.
- SOCRadar observed the system user `tance`, a `chen-kk` handle in tooling, and a separate `chenyk` / `163.com` developer identifier in related victim configuration data, while treating the name overlap as circumstantial.
- The actor used FOFA for target discovery; SOCRadar notes FOFA registration requires a Chinese phone number and has a law-enforcement cooperation channel.
- Simplified Chinese appeared in comments and directory names such as `nacos-xxljob批量`.
- Between SOCRadar's July 2 and July 4 checks, the actor deleted access-log entries covering the discovery window, indicating awareness and attempted cleanup.

## Defensive guidance
- Patch and validate exposed WordPress, Joomla, and plugin estates, prioritizing Breeze Cache Cleaner, ThemeREX Addons, Joomla JCE, and any CMS paths seen in exploit telemetry.
- Block and investigate traffic involving `137.175.93[.]126`, `43.108.17[.]80`, `113.196.56[.]150`, and `xs.xxooonline[.]eu[.]cc` where no business relationship exists.
- Search web roots for new PHP, JSP, ASPX, or archive files with recent timestamps, unusual names, or hardcoded credentials; preserve copies before removal.
- On Linux hosts, inspect processes named like `[kworker/X:Y]` and verify `/proc/<pid>/exe`; SOCRadar warns that fake kernel-thread names were part of the campaign's defense-evasion guidance.
- For Nacos, upgrade to 2.2.1 or later, enable `nacos.core.auth.enabled=true`, rotate credentials found in Nacos configs, and review access logs for bulk reads.
- Use web-server logs, file integrity monitoring, EDR, WAF, DNS, and outbound proxy logs to determine whether a webshell was used after initial placement.
- Treat confirmed shells as potential access-broker inventory: rotate application secrets, database credentials, cloud keys, payment keys, and CMS administrator credentials exposed to the host.

## Indicators
- `137.175.93[.]126` — exposed operator server / open directory
- `43.108.17[.]80` — reported infrastructure
- `113.196.56[.]150` — reported infrastructure
- `xs.xxooonline[.]eu[.]cc` — reported domain
- `/home/tance` — exposed operator home directory path
- `nacos-xxljob批量` — reported directory naming clue

## Related pages
- [Joomla JCE CVE-2026-48907 exploitation](joomla-jce-cve-2026-48907-exploitation.md)
- [Everest Forms Pro CVE-2026-3300 exploitation](everest-forms-pro-cve-2026-3300-exploitation.md)
- [WP Maps Pro CVE-2026-8732 exploitation](wp-maps-pro-cve-2026-8732-exploitation.md)
- [Operation Endgame SocGholish disruption](operation-endgame-socgholish-disruption.md)

## Sources
- SOCRadar: https://socradar.io/blog/wp-shellstorm-expose-1-4m-wordpress-sites/
- The Hacker News: https://thehackernews.com/2026/07/exposed-hacker-server-reveals-wp.html
