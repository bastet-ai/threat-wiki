---
title: "eMudhra: private keys of EIGHT intermediate CAs compromised via weak key generation — keys derivable from the public certificates themselves, all eight revoked cACompromise 18 Oct 09:24–09:38Z, browser/OS trust collapse in progress (this wiki capture Oct 22)"
---

# eMudhra intermediate CA private-key compromise — the weak-key edition: forgeable trust for everything the eight intermediates ever issued

**Observed:** reported to root programs **Oct 17, 2026 18:05 UTC**; revoked **Oct 18, 2026 09:24:32–09:38:46 UTC**; Unit 42 brief **Oct 22, 2026** (full text captured by this wiki from `unit42.paloaltonetworks.com/emudhra-certificate-compromise/`, published 17:15:32Z). Corroborated against Mozilla bug **2083449** (the CCADB record: all eight identities with SHA-256 fingerprints, serials, CCADB IDs, and the revocation table), the reporter's public proof site (`emudhra.we-have-a-problem.com`), and Cloudflare's disclosure post (aware ~Oct 19 17:00 UTC).

## The observation

The private keys of **eight eMudhra Limited intermediate CA certificates** were compromised — not by intrusion into a signing system, but because the keys were **generated with insufficient randomness and are mathematically derivable from the public certificates**. Anyone who can fetch the public cert can compute the private key. The reporter demonstrated possession by signing proof messages with each of the eight keys and published per-intermediate live endpoints where a visitor's own client chain-validation reveals whether it still trusts a compromised intermediate. SOCRadar's tally (as of Oct 21): **no confirmed abuse yet**, keys recoverable **in under a second**, exposed window on the order of **~17 months**.

What a holder of these keys can do (Unit 42, corroborated by the bug record):

- **Sign unauthorized public TLS certificates** for any domain — full MitM against every client that still trusts the chain;
- **Execute MitM traffic interception, impersonation, or session hijacking** against targeted domains;
- and — the axis most TLS write-ups miss — two of the eight are **code-signing intermediates** (`EM OV CS CA - G3B` / `G3C`, chains to `emSign Root CS CA - G3`): the compromise reaches **software publisher trust**, not just transport.

## The eight (from the CCADB/Mozilla record)

All eight revoked reason **cACompromise** within a **14-minute window, Oct 18 09:24:32–09:38:46 UTC**:

| Intermediate | Org | Chain | Revoked (UTC) |
|---|---|---|---|
| EM DV TLS CA - G3B | eMudhra BV | emSign Root TLS CA - G3 | 10-18 09:24:32 |
| EM DV TLS CA - G3C | eMudhra Inc | emSign Root TLS CA - G3 | 10-18 09:27:07 |
| EM EV TLS CA - G3B | eMudhra BV | emSign Root TLS CA - G3 | 10-18 09:28:53 |
| EM EV TLS CA - G3C | eMudhra Inc | emSign Root TLS CA - G3 | 10-18 09:30:49 |
| EM OV CS CA - G3B | eMudhra BV | emSign Root CS CA - G3 | 10-18 09:33:37 |
| EM OV CS CA - G3C | eMudhra Inc | emSign Root CS CA - G3 | 10-18 09:35:24 |
| EM OV TLS CA - G3B | eMudhra BV | emSign Root TLS CA - G3 | 10-18 09:37:19 |
| EM OV TLS CA - G3C | eMudhra Inc | emSign Root TLS CA - G3 | 10-18 09:38:46 |

Full SHA-256 fingerprints and serials are in bug 2083449 comment 10 — quote the bug, do not retype from memory.

**Record-divergence note (this wiki):** eMudhra's own status page says it was made aware "October 18, 2026 (late evening, India time)" and revoked Oct 19; the CCADB bug records the report at **Oct 17 18:05 UTC** and eMudhra's acknowledgment at **Oct 17 21:28 UTC**, with revocations executed **Oct 18**. When incident timelines are material, read the root-program bug, not the vendor status page — the machine-logged clock beats the prose.

## Trust collapse status (as captured Oct 22)

Mozilla: bug 2083449 opened, intermediates distrusted per root-program process. Google/Android: update shipped via Google Play Services (SOCRadar timeline). Apple: blocked Oct 19. Sectigo: revoked its **cross-signed copies** of the affected intermediates Oct 19 — the cross-sign angle is the part fleets forget: distrusting eMudhra roots does NOT clear a chain that an unaffected CA cross-signed. The reporter's check endpoints (`curl https://dv-g3b-emudhra.we-have-a-problem.com/` and variants, incl. No-CT and `aaa-` copies) give any operator a **client-side self-test of residual trust** — a rare, immediately-actionable artifact in a CA incident.

## What defenders should do now (Unit 42 interim guidance + this wiki hunts)

1. **Inventory by ISSUER CHAIN, not by leaf**: any cert chaining to the eight intermediates (or to the emSign roots through them) must be reissued under a different CA — immediately, regardless of expiry.
2. **Hunt embedded trust, not just served certs**: code repos, containers, API clients, custom runtime trust stores (`/etc/ssl/certs`, Java keystores, Python `certifi` bundles, Docker base images, mobile app bundles) that bundled eMudhra intermediates as anchors will keep validating forged chains after every browser has distrusted them.
3. **Force distrust through MDM/config management** and **enforce strict CRL/OCSP checking** at egress proxies and API gateways — block revoked chains at the perimeter for the unpatchable stragglers.
4. **Hunt active MitM**: unexplained TLS handshake-failure/cert-validation-error spikes, egress sessions to unknown IPs presenting eMudhra-signed certs, and auth/session anomalies (SSO, VPN, cloud portals) in the Oct-17→Oct-18→distrust window for replayed-session exposure.
5. **CT + CAA hygiene**: crt.sh/CT-log monitoring for unauthorized issuance against your domains; CAA records restricting who may issue; longer-term, short-lived certificates via ACME/CLM to shrink the blast radius of the NEXT key compromise (this is the second trust-store-scale event this class — Sectigo/HKICCA-style cross-sign failures keep recurring, and revocation is always the slow path).
6. **Code-signing exposure**: audit whether anything in your supply chain pinned trust to eMudhra CS intermediates (`EM OV CS CA - G3B/G3C`) — a forged code-signing cert under a live trust anchor is a publisher-impersonation factory.

## Durable reads

- **A CA's population, not its perimeter, is the attack surface**: weak key generation defeats every operational control the CA ran later. Auditable proof of key-strength hygiene at issuance time (deterministic generation from audited HSM entropy, post-issuance weakness scanning of the public set) is the only class of control for it — and this wiki's hunt rule: **CA-incident blast radius = every client with a stale trust store, not every browser**.
- **Revocation is a broadcast; distrust is a state each system must reach independently.** The gap between the two is the exploitation window, and cross-signs (Sectigo here) extend it into networks that never heard of eMudhra.
- **Timeline discipline**: vendor status pages lag and contradict root-program logs by 24 h+; the CCADB/Mozilla bug is the primary record for CA incidents.

## Monitor

- Confirmation (or continued absence) of in-the-wild forged certificates — the abuse clock is still at zero as captured.
- Mozilla/Google final distrust timelines and any eMudhra remediation/root-preservation plan (does eMudhra get a corrected re-key, or is the brand's trust terminated?).
- Whether the `emSign` ROOTS themselves stay trusted (currently only intermediates are revoked — root exposure via cross-signs is the tail risk).
- Copycat weakness-scan disclosure: does the reporter-style derivation sweep get run against other CAs, and what else falls out (the `we-have-a-problem` proof pattern is trivially replicable).
- Any code-signing trust-list action on the two CS intermediates beyond the CA/Browser Forum baseline.

## Sources

- Unit 42: [EMudhra Intermediate CA Certificates Compromised](https://unit42.paloaltonetworks.com/emudhra-certificate-compromise/) (Oct 22, 2026 — full text captured by this wiki)
- Mozilla CCADB bug: [bugzilla.mozilla.org/show_bug.cgi?id=2083449](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449) (fingerprints, serials, revocation table, reporting timeline)
- Reporter proof site: [emudhra.we-have-a-problem.com](https://emudhra.we-have-a-problem.com/)
- Cloudflare: [8 eMudhra certificates are compromised](https://blog.cloudflare.com/emudhra-certificate-compromise)
- eMudhra status page: [certificate-security-incident](https://emudhra.com/en/post/certificate-security-incident)
- Secondary corroboration: SOCRadar (abence/no-abuse status as of Oct 21), Help Net Security (Oct 21)
