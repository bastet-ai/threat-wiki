# Unit 42: CL-CRI-1131 / CL-CRI-1163 — LLM-orchestrated Latin America intrusion campaigns with exposed AI backends (Sep 3, 2026)

## Tags
- ops
- operations
- Unit 42
- CL-CRI-1131
- CL-CRI-1163
- agentic AI
- AI-augmented operations
- LLM
- commercial LLM abuse
- Latin America
- Mexico
- Brazil
- Ecuador
- transportation sector
- financial sector
- NextChat
- SockTz
- SOCKS5
- proxy infrastructure
- OpSec failure
- exposed staging
- multi-SAN certificate
- data exfiltration
- job-themed phishing
- JBoss
- Operation Escaneo
- SHADOW-AETHER

## Summary

On **September 3, 2026**, Unit 42 (Reese Lewis, Sara McBroom) published "**Attackers Expose Ongoing AI Tool Use Targeting Organizations in Latin America**," describing two ongoing multi-stage intrusion and data-exfiltration campaigns tracked as **CL-CRI-1131** (Mexican transportation campaign: a transportation organization plus federal government ministries and municipal water utilities in Mexico and Ecuador; LotL batch-script tradecraft, infrastructure persisted February–June 2026) and **CL-CRI-1163** (Brazilian financial campaign: expansion of previously reported job-themed phishing against vulnerable web servers, homebrewed RATs, and a Go-based reverse-SOCKS5 proxy **SockTz** with iterative versioned filenames indicating AI-generated tooling). Both clusters share overlapping SOCKS5 relay infrastructure and both use **commercial LLMs as the operational workbench** — the durable read is that the LLM itself became part of the attack infrastructure, and the operators' failure to secure that infrastructure (an internet-exposed NextChat instance, an open staging directory) handed researchers their playbook, prompt history, and staging scripts.

## Corroboration and attribution context

- **CloudSEK** tracks CL-CRI-1131 as **Operation Escaneo** (June 2026 activity); **Gambit Security** previously reported the February 2026 wave ("The AI-Assisted Breach of Mexico's Government Infrastructure"), describing multiple LLMs including Claude and GPT-4.1 used to troubleshoot the operators' own execution failures.
- Unit 42 explicitly corroborates the broader threat-intel picture: the Brazilian campaign's SockTz proxy tool and IP `167.148.195[.]53` were previously tied to **persistent targeting of vulnerable JBoss servers** in Trend Micro's **SHADOW-AETHER** reporting — the same iterative `_output`-suffixed LLM-generated script naming appears in both. Treat CL-CRI-1131 / CL-CRI-1163 as the Unit 42 cluster labels for activity that overlaps with (and extends) the SHADOW-AETHER-040 / SHADOW-AETHER-064 trend; no single confirmed operator identity is asserted.

## CL-CRI-1131: Mexican transportation campaign

- **April 2026 intrusion:** LotL batch scripts (numbered, iteratively patched) used to dump SAM hives and `NTDS.dit` — with visible LLM trial-and-error (failed dumps, volume-shadow-copy workarounds, successive script fixes).
- **Exfiltration infrastructure:** pivot on exfil IP `62.171.185[.]97` revealed a Let's Encrypt certificate on **`m-doxa-apodo.duckdns[.]org`**; the `m-doxa` naming convention exposed a **February 2026 multi-SAN certificate** covering the campaign's subdomains and, by name, its intended targets:
  - `m-doxa-apodo.duckdns[.]org` (apodo = alias)
  - `m-doxa-geo.duckdns[.]org` (geolocation)
  - `m-doxa-intel.duckdns[.]org` (intelligence)
  - `m-doxa-vacunas.duckdns[.]org` (vaccines)
  - plus `m-doxa-repuve.duckdns[.]org` and `m-doxa-sre.duckdns[.]org` in the published IOC set
- **Certificate timeline:** Feb 27, 2026 (SHA-256 `7d766942…fcb40bf8`, 1 SAN, host `165.22.184[.]26`) → Apr 20, 2026 and Jun 19, 2026 (SHA-256 `4e218e70…963a8fee5` / `46ac289c…6d3899c`, 5 SANs each, host `178.128.87[.]160`).
- **AI backend exposure:** `178.128.87[.]160` hosted an open-source **NextChat** instance on TCP 3000 — a multi-model LLM web UI on attacker infrastructure. Unit 42 assesses the operators relied on LLMs to generate the workaround scripts after SAM/NTDS collection failures; the exposed NextChat directory left the playbook and prompt history visible.

## CL-CRI-1163: Brazilian financial campaign

- **Initial access (February 2026):** resume/job-themed phishing attachment → multiple homebrewed RATs.
- **SockTz tooling:** install attempts of **SockTz versions 1–9 within a two-hour window** (`socktz_v8.exe` fetched from a compromised WordPress site, then pivot to `hxxp[:]//167.148.195[.]53:8888/socktz_v9.exe` when v8 failed to install) — the rapid version churn is itself an LLM signature (the model is asked to "try again" with a new build).
- **Open staging directory:** `167.148.195[.]53` exposed the SockTz installers plus **hundreds of campaign scripts** across multiple attack phases, many with LLM-tell filenames: `*_output` identifiers and descriptive-adjective exploit names (`exploit_creative.py`, `exploit_careful.py`, `rce_focused.py`).
- **Published payload hashes (SHA-256):** `a38b2cf8beff32a276eed8783723ecf8cc53d7dc88669e1b998dddc4db6fe996`, `87bf8bc8b4a2cf34f0af1afe161f123a3d200e77f6c6f41b81bf6ae66ee172ec`.

## Durable defender lessons

1. **The LLM is now attack infrastructure — hunt for it.** Exposed NextChat / open-web-UI instances on internal or staging ranges are a high-fidelity indicator of LLM-assisted operations; treat public LLM chat UIs reachable from the internet on attacker-owned or staging infrastructure as a campaign artifact, not just a misconfiguration.
2. **OpSec failures outpace AI capability.** Even as operators' tooling quality rises, foundational mistakes (open directories, unauthenticated NextChat, descriptive LLM-generated filenames, consolidated multi-SAN certs that reveal target lists) remain the most reliable disruption vector. Defenders should hunt for the tells: iterative versioned filenames (`*_v1…v9`), `_output`-suffixed scripts, adjectival exploit naming.
3. **Certificate-pivot tracking is effective against duckdns-style DDI.** A single multi-SAN Let's Encrypt certificate can reveal the entire campaign's staging domains and, by name, the intended government targets — index SAN names and correlate across DDI providers.
4. **Shared relay infrastructure links clusters.** Overlapping SOCKS5 relay infrastructure between geographically distinct campaigns is a clustering signal that does not require tooling identity.

## Related pages

- [SHADOW-AETHER AI-augmented Latin America intrusions](shadow-aether-ai-augmented-latam-intrusions.md) — the Trend Micro reporting this post corroborates (SockTz, `167.148.195[.]53`, JBoss targeting)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md) — the pattern umbrella
- [Patriot Bait: AI-operated disposable C2 botnet](patriot-bait-ai-assisted-c2-botnet.md) — AI as C2 operator

## Sources

- Unit 42 — "Attackers Expose Ongoing AI Tool Use Targeting Organizations in Latin America" (Reese Lewis, Sara McBroom; published 2026-09-03): [https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/)
- Corroborating reporting referenced by Unit 42: CloudSEK "Operation Escaneo"; Gambit Security "The AI-Assisted Breach of Mexico's Government Infrastructure"; Trend Micro "Vibe Hacking: Two AI-Augmented Campaigns Target Government and Financial Sectors in Latin America" (SHADOW-AETHER).
