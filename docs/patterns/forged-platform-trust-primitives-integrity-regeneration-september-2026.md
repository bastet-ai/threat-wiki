# Pattern: forging the operating system's own trust primitives — when attackers regenerate integrity checks instead of bypassing them (synthesis from Sep 2026 reporting)

## Tags
- patterns
- defender heuristics
- trust primitives
- integrity forgery
- Secure Preferences
- HMAC forging
- App-Bound encryption
- rogue certificate authority
- root certificate store
- TLS interception
- MsBuild hollowing
- browser extension abuse
- tamper detection
- EDR blind spot
- per-host regeneration
- blocklist futility
- detection-by-structure
- KREMLIN
- REF9334
- Docro Hijacker
- Huntress
- Elastic Security Labs
- Unit 42

## Summary

Three independent September 2026 reports converge on one durable pattern: rather than bypassing an OS or browser's tamper-detection mechanism, attackers are now **recomputing and regenerating the mechanism's own cryptographic outputs**, so the platform itself vouches for the malicious state. A detection or response strategy built on "the integrity check will flag it" or "we blocklisted the bad certificate/hash" is structurally defeated by this class.

The three sightings, from unrelated actors and unrelated telemetry:

1. **KREMLIN / REF9334 (Elastic Security Labs, Sep 14, 2026)** — the installer writes a malicious Chrome/Edge extension into the profile and **regenerates the Secure Preferences HMACs and App-Bound encrypted hashes that Chromium computes over extension entries**, so the browser and any endpoint tool reading those structures see a legitimately-installed extension. ([KREMLIN page](../ops/kremlin-ref9334-chrome-integrity-forgery-ethereum-c2-brazilian-banking-malware-elastic-september-2026.md))
2. **Docro Hijacker, inside Unit 42 CL-CRI-1171's OfferLoader PPI marketplace (Sep 9, 2026)** — a Chrome hijacker that **bypasses the Secure Preferences HMAC-SHA256 check via a side-loaded `Adblock.dll`**, letting the `docro` MV3 extension persist and rewrite search to `mqsearch[.]com`. ([CL-CRI-1171 page](../ops/unit42-clcri-1171-offerloader-ppi-marketplace-september-2026.md))
3. **Huntress Google Doc sidebar campaign (Sep 15, 2026)** — a payload **builds its own public key infrastructure on the victim**: a self-signed root CA in the system root store masquerading as Google Trust Services `CN=WR3`, a forged `www.virustotal.com` leaf (SAN covering the real domain and localhost), a hosts entry, and a LocalProxy firewall rule — producing a locally-answered HTTPS channel that fully validates, so the operator can block, read, or fabricate VirusTotal verdicts (and by extension intercept crypto domains or AV update signals). The CA is **regenerated per host**. ([Google Doc sidebar page](../ops/google-docs-apps-script-sidebar-clickfix-rogue-ca-ledger-implant-huntress-september-2026.md))

## Why this matters for defenders

- **The trust anchor is the attack surface.** Secure Preferences HMACs, App-Bound encryption, and the root certificate store are all designed to be "the part the OS checks for you." Once an attacker with user/admin code execution can *write the check's inputs and recompute its outputs* (all three mechanisms are keyed with material recoverable by user-mode code — OSCrypt/App-Bound keys on Windows, the root CA store via standard APIs), the platform's verdict flips to "clean." Treat any user-mode process able to touch these stores as already-persuaded-of-the-attacker's-presence, not as a candidate anomaly to dismiss.
- **Per-host regeneration defeats IOC blocklisting by design.** A per-host CA has a unique thumbprint on every victim; a recomputed HMAC is unique per profile. Detection must key on **structure and sequence**, never on hashes of the forged artifact.
- **These artifacts survive the obvious cleanup.** Killing the malicious process removes nothing: the CA, hosts entry, and firewall rule persist past reboot in the Huntress chain; KREMLIN's forged preference entries persist in the profile. Remediation is clinical removal of each component or reimaging — Huntress's own analysts note a rogue CA in the trusted store is not the first thing a triager checks.

## Detection recipes (structural, not IOC-based)

| Primitive | Hunt |
|---|---|
| Browser integrity stores | Writes to `Secure Preferences` / `Preferences` with **recomputed HMACs from a non-browser process**; new extension entries with no Web Store / policy provenance and no install-event in browser logs |
| OS key material access | Processes reading **OSCrypt / App-Bound encryption keys** (LSA-protected or `%LOCALAPPDATA%\...` state) outside browser processes |
| Root certificate store | **New root-CA install events** (CryptInstallCACert / certutil add-store / API equivalents) from non-enrollment, non-IT-tooling processes; watch for CA names impersonating public CAs (`CN=WR3`, "Google Trust Services", "Let's Encrypt") |
| Local TLS interception | **hosts-file writes** paired with new firewall allow rules (Huntress chain names the rule `LocalProxy`); localhost listeners on 443/any port presenting non-store-issued leaves for domains the host actually connects to |
| Process hollowing tells | `msbuild.exe` / other signed binaries with a **stripped import table** (kernel32-only imports), spawned by Office/browser/script ancestry |
| Certificate inventory | Leaf certificates issued by non-enterprise CAs for domains the host contacts (especially security-vendor domains: virustotal.com, AV update endpoints) |

## Boundary conditions

- All three sightings require **user- or admin-level code execution first** — this is a post-compromise persistence/stealth layer, not an initial-access technique. It multiplies the blast radius of any prior foothold (phishing, ClickFix, supply chain).
- Reading the keys is on Windows the common enabler (OSCrypt/App-Bound recovery); equivalent macOS/Linux primitives differ and none of the three reports demonstrates cross-platform forgery of the same store.
- These are *three specific implementations by unrelated actors* within a week of reporting — the pattern is a lens for hunting, not evidence of a shared toolkit or collaboration.

## Related
- [KREMLIN / REF9334 page](../ops/kremlin-ref9334-chrome-integrity-forgery-ethereum-c2-brazilian-banking-malware-elastic-september-2026.md)
- [Unit 42 CL-CRI-1171 Untracked Nightmares page](../ops/unit42-clcri-1171-offerloader-ppi-marketplace-september-2026.md)
- [Huntress Google Doc sidebar campaign page](../ops/google-docs-apps-script-sidebar-clickfix-rogue-ca-ledger-implant-huntress-september-2026.md)
- [Unit 42 SPIFFE/SPIRE cgroup identity spoofing (Sep 10, 2026)](unit42-spiffe-spire-cgroup-workload-identity-spoofing-spooffe-september-2026.md) — the cloud-native sibling of the same idea: forge the attestation inputs and the platform hands you the victim's identity.
