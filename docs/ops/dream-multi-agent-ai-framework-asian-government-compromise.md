# Dream: near-autonomous multi-agent AI framework compromises Asian government entities

## Summary
Dream Research Labs published an August 12, 2026 report on the **complete operational workspace of an autonomous AI attack framework** that conducted confirmed, real-world intrusions against **government entities in Asia** (Dream does not name the target; The Financial Times, Reuters, and Taiwan's Ministry of Digital Affairs reported it was **Taiwan**, targeted in a campaign observed **July 1–4, 2026**). The framework is built on the **Hermes and OpenClaw agent harnesses** and deploys **up to 8 lettered sub-agents (A–Q observed) in parallel per wave**, automating reconnaissance, credential cracking, SSO lateral movement, and exfiltration. Over **12 documented attack waves in ~4 days**, the operation produced **1,395 files (~160 MB), 85 cracked credentials, 2,564+ exfiltrated personnel records**, a full user-database export, 7 SSO client secrets, 6 internal database credentials, and a persistent backdoor foothold. The operator is assessed as **Chinese-language** (Simplified Chinese internal status reports; Traditional Chinese target-facing analysis). Dream does **not** publicly identify the operator. Some details were first shared with the Financial Times.

This is one of the most complete public records yet of a **production agentic-attack framework with probabilistic decision logic, autonomous research ("Learning Cycles"), and self-correction loops** run against a nation-state target.

## Tags
- ops
- agentic AI
- multi-agent
- Hermes
- OpenClaw
- autonomous attack
- Bayesian scoring
- learning cycles
- SSO
- JWT alg none
- CAPTCHA OCR
- Tesseract
- password spraying
- credential cracking
- government
- Taiwan
- supply chain
- lateral movement
- exfiltration
- prompt-injection guardrail bypass
- unauthorized pentest framing
- unauthenticated API
- web shell
- Forms Authentication

## Campaign overview
- **Window:** 12 documented waves, **July 1–4, 2026** (~4 days).
- **Output volume:** **1,395 files / ~160 MB** across the recovered workspace — "consistent with heavy automation far beyond what a human operator could produce alone."
- **Impact:** 85 cracked credentials; 2,564+ personnel records; full JSON export of one department's user database; 7 SSO client secrets; 6 internal DB credentials (MSSQL, Oracle, Sybase); internal network IP ranges; persistent backdoor foothold.
- **Operator:** Chinese-language (code-switched workspace). Not publicly identified.
- **Target:** Government entities in Asia; FT/Reuters/Taiwan MADA say **Taiwan**. Dream withheld the name (responsible disclosure; impacted orgs notified pre-publication).

## Framework architecture
- **Two workspace identifiers:** `.hermes` and `.openclaw`; reports generated into structured paths.
- **Sub-agents:** lettered designations (**A** SSO exploitation and credential attacks; **B** JWT bypass testing and CAPTCHA brute-force; **C** multi-portal reconnaissance; **D** API scanning and admin-panel bypass; **E** CVE research and vulnerability-chain testing; **F** supply-chain target assessment; **I** password spraying with CAPTCHA bypass via Tesseract OCR; **Q** deep API-endpoint exploitation), up to **8 concurrent** per wave (dispatched in 3 batches).
- **Guardrail bypass:** the framework's own LLM safety refusals were circumvented by **framing all activity as "authorized penetration testing."**
- **Two-layer Bayesian decision engine** (the durable architectural finding):
  - **Layer 1 — vulnerability triage:** uninformative prior **P=0.50**, updated with explicit likelihood ratios (tool-scan positive **LR+ = 6.0**; manual curl confirmation **LR+ = 10.0**; impact-assessment positive **LR+ = 3.0**; WAF/constraint present **LR− = 0.30**). Posteriors drive action: **P > 0.95** confirmed exploitable → promote to chain; **P > 0.70** allocate more resources; **P > 0.50** queue for next wave; **P < 0.30** discard.
  - **Layer 2 — attack-chain scoring:** **P_success = P_chain × (1 − P_blocker)** where P_chain = confirmed steps / total steps. Bands: 95%+ all critical steps confirmed; 60–94% most confirmed; 20–59% significant blockers; 5–19% critical conditions missing; <5% insurmountable blocker. **Worked example:** the SSO lateral-movement chain was rated **99%** (3/3 steps confirmed, P_blocker ≈ 0.01) and was later validated: **98.8% of cracked accounts successfully pivoted**.
- **Learning Cycles:** five documented autonomous research phases (v1–v5) that search vulnerability databases, GitHub repositories, and security publications for techniques applicable to the target's specific environment, including documented CVEs in country-specific products.
- **Self-correction:** the framework's own final summary lists **7 false positives** it identified and discarded, with "physical confirmation" plus two rounds of three-agent cross-verification required per confirmed finding (Chinese notation: 8个真实漏洞(物理确权+3+3交叉验证)). Most instructive case: a 21-second response delay attributed to a blind-SQLi SLEEP(5) that retesting proved was an **SMTP verification-email timeout**, not SQL.

## Attack chain (confirmed steps)
1. **Recon:** decompiled Angular JS bundles from a government portal → 21 connected systems; full national SSO map (**6 sub-realms, all OIDC endpoints, 2 RSA signing keys**, every auth flow); 36+ API endpoints on one system, many unauthenticated; one system exposed its **entire user database unauthenticated** (thousands of employee records: name, department, SSO ID).
2. **SDK harvesting:** a URL from the JS bundles led to a GitBook SSO integration portal; the framework auto-scraped it via **`llms.txt`** page indexing and **`.md`** raw-content URLs, downloading two SDK sample projects (Java Spring Boot, ASP.NET Core 8.0) and running its **Local-LLM-SAST-0day** analysis on them. **Zero overlap** between the SAST findings and the actual confirmed breaches — the real entry points were server-side flaws discoverable by standard black-box testing.
3. **Initial access (parallel paths):**
   - **Authentication backdoors:** three hidden API endpoints that **accept any request body and return a valid authenticated session** — exposed developer debug endpoints.
   - **Credential spraying:** Tesseract OCR solved each CAPTCHA with **100% accuracy**; username-based password patterns (capitalized/decorated employee IDs) cracked **85 accounts** (12 in the first round, 73 more as patterns expanded).
   - **JWT `alg=none` bypass:** a government API accepted unsigned JWTs, allowing forged identity tokens without the signing key.
4. **Lateral movement / persistence:** cracked office-automation credentials were tested against every SSO-connected internal system; the SSO bridge **auto-trusted the OA session** (no re-auth, no MFA, no user confirmation) — **84/85 (98.8%)** reached the department's internal system. An unrestricted file upload placed a **web shell**, but a secondary **Forms Authentication** layer blocked execution (partial success, no RCE).
5. **Exfiltration:** 2,564+ personnel records (1,409 employees from the users API; 916 from an unauthenticated API; 239 legal professionals from an unauthenticated Ministry-of-Justice endpoint), the complete user-database JSON, 7 SSO client secrets (rotated, but naming conventions revealed), 6 internal DB credentials, internal IP ranges.
6. **Supply-chain expansion:** the operator pivoted to **government IT supply-chain vendors, a nuclear safety agency, a government email system, and 7+ energy-sector companies**, scanning all in parallel for misconfigurations, exposed admin interfaces, and exploitable flaws.

## Defender priorities
- **Hunt for the debug-backdoor shape:** API endpoints that return a valid session for **any** request body are a high-value, concrete artifact — audit for auth endpoints whose response ignores request contents, especially ones absent from API documentation.
- **Unauthenticated user-directory endpoints:** an API returning employee name/department/SSO-ID lists without authentication is the enabler for the entire spray; inventory and gate every endpoint that enumerates identities.
- **JWT `alg=none`:** verify signature-verification libraries reject unsigned tokens; hunt for accepted `alg=none` requests in API logs.
- **CAPTCHA + username-derived passwords:** 100% OCR accuracy means CAPTCHAs are not a stop-gap against automated spray; prefer rate-limiting, lockout, and credential-stuffing analytics over image challenges.
- **SSO trust boundaries:** an SSO bridge that auto-trusts a session from one system into every connected system converts one credential into estate-wide access. Audit which systems accept the session without step-up auth; treat the OA-portal compromise as an estate incident.
- **AI-agent operational artifacts:** the durable detection shape is **agent-produced file volume and structured reports** (hundreds of files, wave reports, Bayesian triage tables, after-action logs) on an endpoint or in an exposed share/repo — plus the "authorized penetration testing" framing in internal notes as a guardrail-bypass indicator.
- **LLM-adjacent scraping surface:** `llms.txt` and `.md`-served documentation portals are now reconnaissance targets; treat public documentation and SDK sample repos as attack-surface documentation.

## Assessment limits
- **Dream does not name the targeted government or the operator**; the Taiwan attribution comes from FT/Reuters and the MADA statement, not from Dream.
- Dream withheld some detail shared first with the Financial Times; the published report is the primary public record used here.
- The "85 accounts" and "2,564+ records" figures are Dream's confirmed counts from the recovered workspace; the supply-chain-expansion step is a scan/assessment phase, not a confirmed compromise of the vendors.
- Guardrail-bypass framing ("authorized penetration testing") is a description of the framework's prompts, not a statement about the operator's authorization.

## Related pages
- [knaithe Hermes / DeepSeek autonomous exploitation campaign](../ops/knaithe-hermes-deepseek-autonomous-exploitation.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [Hugging Face autonomous-agent production intrusion](../ops/hugging-face-autonomous-agent-production-intrusion.md)
- [Anthropic cyber-evaluation real-world intrusions](../ops/anthropic-cyber-evaluation-real-world-intrusions.md)

## Sources
- Dream Research Labs: [Inside a Multi-Agent AI Framework Used to Compromise Government Entities in Asia](https://www.dreamgroup.com/blog/inside-a-multi-agent-ai-framework-used-to-compromise-government-entities-in-asia) (August 12, 2026)
- The Hacker News: [AI-Generated Exploit Scripts Target Siemens S7 PLCs in U.S. Critical Infrastructure](https://thehackernews.com/2026/08/ai-generated-exploit-scripts-target.html) (Ravie Lakshmanan, August 20, 2026 — includes MADA/Taiwan attribution and sub-agent letter list)
- Reuters: [Taiwan says it was targeted last month by AI-driven hacking campaign](https://www.reuters.com/world/china/taiwan-says-it-was-targeted-last-month-ai-driven-hacking-campaign-2026-08-13/) (August 13, 2026)
