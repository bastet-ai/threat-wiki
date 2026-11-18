# CISA KEV November 18, 2026 (LiteLLM, Apache Axis, REDCap, Synology)

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- LiteLLM
- BerriAI
- AI gateway
- LLM proxy
- sandbox escape
- bytecode
- CWE-420
- CVE-2026-40217
- Apache Axis
- SOAP
- unsafe reflection
- CWE-470
- CVE-2026-90436
- Confluence
- N-able N-central
- REDCap
- Vanderbilt
- code injection
- CWE-94
- CWE-73
- CVE-2026-90817
- Synology
- DSM
- BeeStation
- CVE-2024-10441

## Summary

CISA's November 18, 2026 KEV batch is **four** additions (catalog `2026.11.18`, now **1,786 entries**), breaking this wiki's THIRTEEN-reading hold on `2026.11.17`/`1,782`. The headline for this wiki's beat: **the exploited-software list now includes the AI gateway the whole industry installed** — BerriAI **LiteLLM** `CVE-2026-40217`, a sandbox escape in the proxy's custom-guardrail test endpoint that turns a proxy-admin credential into root code execution on the box holding every provider key, master key, and virtual key the gateway serves. Two of this wiki's three on-wiki LiteLLM incidents were supply-chain (the `1.107.0` poisoned wheel, the MCP stdio injection); this one is the product's own code, and the working exploit has been **public for seven months** (X41 D-Sec, X41-2026-001, April 8) while KEV only just confirmed exploitation. The durable read: **the KEV clock started in April for everyone who was listening; KEV is confirmation, not alarm** — same law the 318th wrote for Puppet.

| CVE | Product | Class | Score | BOD 26-04 due | Notes |
|---|---|---|---|---|---|
| **CVE-2026-40217** | BerriAI LiteLLM (proxy) | Unprotected alternate channel (`POST /guardrails/test_custom_code` runs user Python in a hand-rolled keyword filter; bytecode rewriting escapes it) → RCE as the proxy user (**root in the default Docker image**) | **8.8** (CVSS 3.1, `PR:L` — needs proxy-admin) | **2026-12-02** | Affected `>= 1.81.8, < 1.83.10` (endpoint born `1.81.8`, Feb 5); GHSA-wxxx-gvqv-xp7p text says fix `1.83.11`, OSV/advisory table says `1.83.10` — go to `1.83.11`, the highest named floor. Finder X41 D-Sec; fix = RestrictedPython rewrite (PR #25818, merged Apr 15). |
| **CVE-2026-90436** | Apache Axis **1.x** (EOL) | Unsafe reflection: SOAP `<Fault><detail><exceptionName>` loads/instantiates an attacker-named class (String constructor, static initializers run) **before any per-service auth handler executes** → unauth RCE with a suitable gadget class on the classpath | **9.8** (CISA-assigned; Apache CNA `2026-11-06`, `unsupported-when-assigned`) | **2026-11-21** (forensics triage required) | **No Axis 1.x fix will ship** — migrate engines or apply the published patch commit. Real victims are the products that bundle it: **Atlassian Confluence Data Center** (Rapid7 MDR detected exploitation in a customer env Nov 13) and **N-able N-central** (vendor-reported ITW exploitation Nov 13; PoC published Nov 12; fix = `2026.4 HF3` which disables the Legacy API). Both need non-default config to be vulnerable — check both anyway. |
| **CVE-2026-90817** | Vanderbilt REDCap | Code injection via survey passthrough routing + crafted file-path/stream param in Data Import from a **public survey context**; unauth **given a valid public survey hash** | **9.8** (CVSS 3.1) | **2026-11-21** (forensics triage required) | `>= 13.3.0`; fixed `16.0.49` / `17.3.10` / `17.4.4`. Securifera advisory (Ryan Wincey), CVE published Sep 20 — **two months paperless before KEV**; a third-party tracker asserted successful exploitation as early as Oct 13. Research-institution fleets run REDCap on lab-network boxes that never see the enterprise patch cycle. |
| **CVE-2024-10441** | Synology DSM / BeeStation OS (BSM) | Improper encoding/escaping of output in the system plugin daemon → RCE, remote, unspecified vectors | — | **2026-11-21** | A **2024** CVE finally KEV'd two years later — the backlog law again: a 2024 ID on the 2026 list means recent weaponization surfaced old code. |

All four carry BOD 26-04, ransomware use **Unknown**, no named actor.

## The LiteLLM entry, read close (the one that matters for AI-infra owners)

- **The endpoint**: `POST /guardrails/test_custom_code` exists so an admin can trial a custom guardrail in the UI. `1.81.8`–`1.83.9` ran that Python in a home-built sandbox that scanned the source text for banned words (`import`, `__globals__`, `os.`).
- **The escape** (CWE-420 — the protected path and the alternate path disagree): X41's PoC builds banned names from string pieces at runtime, then rewrites a generator's bytecode to reach the sandbox's own `http_get` helper and pull Python's real `__import__` out of its frame — `import os`, run commands, **root in the default container**.
- **The blast radius**: the gateway holds provider API keys, the master key, issued virtual keys, and (absent `LITELLM_SALT_KEY`) encrypts stored credentials with the master key — owning the proxy owns every AI credential downstream. Master keys leak via env files and CI variables, which is how `PR:L` becomes `PR:N` in practice.
- **Verify with the proxy's real version, not the lockfile**; grep reverse-proxy/access logs for `POST /guardrails/test_custom_code` — most teams never call it; unscheduled hits = rebuild from clean image, rotate master key + every provider key.
- **Stopgap is free**: block `= /guardrails/test_custom_code` at the front end (403); normal chat/completion traffic never touches it.
- **Stay off `1.107.0`** — that is the release that shipped this wiki's on-wiki `PrivCollect` startup-hook stealer (Oct 21); the two LiteLLM incidents are independent bug classes on one product, and the compound advice is identical: treat the gateway's master key like a root password and keep the admin UI off the open internet.

## Timeline (LiteLLM leg)

- **2026-02-05** `1.81.8` ships the guardrail-test endpoint.
- **2026-02-13** X41 D-Sec builds a working escape.
- **2026-04-08** X41-2026-001 published with full exploit — **no patch existed**.
- **2026-04-15** RestrictedPython rewrite merged; fixed releases follow within a week.
- **2026-05-07/11** GitHub advisory GHSA-wxxx-gvqv-xp7p published/reviewed.
- **2026-11-18** CISA adds it to KEV — first KEV movement on this wiki since the Puppet entry Nov 17.

## THIS WIKI verified (read-time claims, ~20:3xZ Nov 18 UTC)

- KEV JSON fetched directly: `catalogVersion 2026.11.18`, `count 1,786` (+4 over the 13-read `1,782` hold; the Puppet `CVE-2026-115731` entry stays in place).
- Word-boundary greps `0` for the on-wiki supply-chain names at this read: `qrcode-reader`, `wechat-companion`, `react-cache-hook`, `tixte`, `rpc-websockets`, `basis-theory`, `clikwraps`, `datepickerror`, plus both NGINX HTTP/2 CVEs (`123633`/`123007`) — the **NGINX KEV WATCH stays armed**, still no KEV entry for the AI-discovered HTTP/2 pair.
- LiteLLM is the **third LiteLLM CVE** on this wiki's books (`1.107.0` wheel poisoning; MCP stdio injection `CVE-2026-42271`; now this) — one product, three incident classes, now two of three KEV-relevant ecosystems touched it (PyPI supply chain + KEV product bug).
- No CVE on any of this week's npm spy-estate names (`@clikwraps/navigate`, `react-native-datepickerror`, `@basis-theory-elements/api-client`) — those stay OSV-lane paper, still `{}` at the sweep read (see the 331st stream).

## Defensive actions

1. **LiteLLM proxy owners (highest urgency)**: upgrade to `>= 1.83.11` (restart required), block the one endpoint at the front end if you cannot patch tonight, grep access logs for unscheduled `test_custom_code` POSTs, rotate master + provider keys if any hit is unexplained, and keep the admin plane off the internet. Library-only users (`import litellm`) are not in scope — the endpoint is proxy-only.
2. **Confluence Data Center / N-able N-central admins**: emergency patch per vendor (N-central `2026.4 HF3`), prioritize internet-exposed instances with the relevant APIs on even though the vulnerable config is non-default; hunt Rapid7-published IOCs in logs, remembering absence proves nothing.
3. **Anything still running Axis 1.x** (count your SOAP endpoints before you say none): migration decision now, not patch decision later — unauthenticated, pre-auth-handler, and no upstream fix is coming.
4. **REDCap operators**: confirm version against `16.0.49`/`17.3.10`/`17.4.4`; audit which surveys are public (the hash is a speed bump, not a wall).
5. **Durable**: a KEV addition on an old-published CVE means active exploitation surfaced NOW — pull the original advisory's technical detail (it is usually the best patch note you will get) and start your exposure clock at the original disclosure, not at the KEV stamp.
