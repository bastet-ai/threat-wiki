---
title: threat.wiki
---

# threat.wiki

Threat intelligence notes, group profiles, named-person records, and defensive guidance.

## Recent entries
- [Citrix NetScaler CVE-2026-8452(?): watchTowr's pre-auth RCE chain — SAML SignedInfo canonicalization heap overflow in nsppe (oversized InclusiveNamespaces PrefixList) reaches root code execution unauthenticated on SAML SP/IdP configs, with a pitboss-reboot bypass; first public NetScaler RCE writeup in 3 years, supersedes the KEV DoS-only framing (watchTowr, Aug 14; CISA KEV, Aug 26)](ops/citrix-netscaler-cve-2026-8452-preauth-rce-watchtowr.md)
- [Pimcore Studio: five coordinated flaws — DataObject field-name RCE (CVE-2026-55634, 9.9) and Hotspotimage PHP object injection (CVE-2026-55220, guzzle FileCookieJar gadget confirmed) plus class-definition privesc, DateFilter blind SQLi incl. admin-hash extraction, and password-reset-URL account takeover with 2FA bypass; fixed 2026.1.6 / 12.3.10 / Studio 2025.4.6, no exploitation or actor named (GitHub GHSAs, Aug 28)](ops/pimcore-studio-dataobject-rce-php-object-injection-cve-2026-55634-batch-august-28-2026.md)
- [Five critical WordPress flaws: WPMU DEV Dashboard Hub-SSO auth bypass (CVE-2026-76581), Avada+Fusion Builder unauth arbitrary-file-write RCE (CVE-2026-18431), TranslatePress admin password-reset URL exposure (CVE-2026-19632), Pods JSON meta-box-loader authorization bypass (CVE-2026-19598), and GiveWP PHP object injection → RCE (CVE-2026-82222, CVSS 10.0) — all unauthenticated site-takeover / RCE paths (Wordfence / Patchstack via THN, Aug 29)](ops/wordpress-wpmu-dev-avada-translatepress-pods-givewp-critical-batch-august-29-2026.md)
- [Unitree G1 EDU humanoid robot: two independent unauthenticated root-RCE chains — CVE-2026-76639 via the TCP 9991 WebRTC-to-DDS bridge + static AES key + chat_go path traversal into bashrunner, and CVE-2026-76640 via a BLE unpaired bootstrap, key-recovery cloud gap, and Wi-Fi-provisioning overflow to system() as root; no confirmed fixed firmware yet (Laflamme / VulnCheck / THN, Aug 27–28)](ops/unitree-g1-edu-two-root-rce-chains-cve-2026-76639-76640.md)
- [Next.js August 2026 security release: two unauthenticated RCEs — a libheif/AVIF heap buffer overflow (GHSA-2xp9-vwfh-vxw4, no CVE, Vercel disabled AVIF optimization pending libheif v1.23.2) and a Windows path traversal (CVE-2026-75604, CVSS 9.0, no known workaround); fixed in 15.5.24 / 16.3.3, Vercel-hosted apps protected (Vercel, Aug 25)](ops/nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md)
- [GitHub Security Advisories Aug 29: argocd-mcp unauthenticated MCP tool-surface bypass using the operator's ARGOCD_API_TOKEN (CVE-2026-82456, Critical), Sigma Forms Pro WordPress unauth RCE via unfiltered_upload + no MIME gate (CVE-2026-14494, Critical), Omnivore Apple-Sign-In JWT algorithm confusion (CVE-2026-82454, Critical), plus Skyvern Jinja sandbox escape, BookStack ZIP-import RCE, Shinobi hardcoded child-node key, rust-iot-platform auth bypass, and @better-auth/sso domain-ownership bypass](ops/github-advisories-argocd-mcp-sigma-forms-omnivore-skyvern-bookstack-august-29-2026.md)
- [TerminalFix: ClickFix variant that directs victims to Windows Terminal/PowerShell, then chains DLL sideloading (LockScreenContentServer.exe + forged dui70.dll), steganographic PNG payload extraction, AD recon, and a custom Python reverse-tunnel implant over WebSocket to gitnow[.]dev — full SOCKS-style network pivot (Microsoft, Aug 28)](ops/terminalfix-clickfix-reverse-tunnel-multistage-microsoft-august-2026.md)
- [Berlin state network: Rhysida extortion after the August compromise of the state administrative network — Aug 7–12 exfiltration in the Senate Mobility/Transport/Climate portfolio, 5.79 TB / ~1.44M-file leak-site claim, and a public refusal to pay (THN / Der Spiegel, Aug 28–29)](ops/berlin-state-network-rhysida-extortion-august-2026.md)
- [Cosmos EVM vesting-account balance overflow exploited across six chains: unchecked subtraction wraps the EVM balance to ≈2^256, reconciliation mints/burns to drain or burn real holdings (GHSA-7g4w-cg88-2cq2, Critical, fixed v0.6.2 / v0.7.2, THN / Cosmos Labs post-mortem)](ops/cosmos-evm-vesting-balance-overflow-exploited-august-2026.md)
- [@7nohe/openapi-react-query-codegen npm compromise: 10 malicious versions published through an exposed issue-comment-triggered release workflow using GitHub Actions OIDC / npm Trusted Publishing — preinstall + binding.gyp payloads download Bun and steal GitHub / cloud / CI credentials; OX now identifies the payload as a "Trinitite" Shai-Hulud variant with rotated public keys (post-arrest copycat wave, StepSecurity + OX)](ops/7nohe-openapi-react-query-codegen-npm-compromised-august-2026.md)

## Sections
- **Ops** — campaign timelines, compromise chains, and sequencing
- **Tools** — malware, payloads, implants, and attacker infrastructure
- **Groups** — crews, cluster names, and shared operational personas
- **People** — publicly identified individuals or project personas when public sourcing supports it
- **Patterns** — reusable defender heuristics
- **Notes** — taxonomy, usage, and editorial guidance
