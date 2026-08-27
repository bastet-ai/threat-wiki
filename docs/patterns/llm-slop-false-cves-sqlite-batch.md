# LLM-slop false CVEs: AI-generated vulnerability advisories poisoning NVD / CISA

## Summary
JFrog Security Research's July 30, 2026 analysis, "SQLite Critical CVEs or LLM Slop?", documents a newly created GitHub repository, `programmervuln/cveadvisory-`, that published a batch of SQLite vulnerability advisories alongside 50+ other CVEs that the researchers assessed as also being AI-generated. NVD quickly flagged several as critical and CISA's ADP agreed — but JFrog's verification found the claims fell apart: the cited code did not exist in the referenced versions, the PoC payloads did not trigger any crash, none of the CVEs appear on SQLite's official advisory page (the gold standard for real SQLite vulnerabilities), and the advisories flag as AI-generated under GPTZero.

This is a pattern page, not a named-actor or campaign profile. The durable defender lesson is that **the vulnerability data pipeline itself is now an attack surface**: LLM-generated, plausibly structured advisories can reach NVD/CISA with high severity scores, drive automated patching and alerting, and create a "false-critical" class of noise that degrades triage. Defenders should treat any CVE that cites non-existent functions, contradicts vendor advisory pages, or ships a non-functional PoC as unverified until checked against primary vendor sources.

## Tags
- patterns
- AI agents
- AI tooling
- LLM
- vulnerability management
- CVE
- NVD
- CISA ADP
- false positive
- SQLite
- CVE-2026-51302
- CVE-2026-51303
- CVE-2026-51300
- CVE-2026-51297
- CVE-2026-51296
- CVE-2026-51304
- JFrog Security Research
- vulnerability database pollution
- LLM slop
- AI-generated advisory
- supply-chain
- patching
- triage

## Why this matters
- A batch of AI-generated "critical" SQLite CVEs was accepted into NVD and CISA ADP with high severity before being debunked. Automated vulnerability-management and patching systems that ingest NVD/CISA will treat these as real, critical, and urgent.
- CVE-2026-51302 in particular was initially assigned a 10.0 Critical score by Red Hat and later downgraded to 7.6 High — evidence that downstream scorers can propagate a fabricated severity until the flaw is disproven.
- The false-critical class inflates patching urgency, distracts triage, and can drive risky emergency-change behavior against a flaw that does not exist. The same mechanism could be used to bury a real high-severity CVE in a flood of AI noise.
- The failure mode is general, not SQLite-specific: any project whose advisories are machine-ingested into NVD/GHSA is exposed to LLM-generated, structurally plausible, but technically false reports.
- It is a distinct and complementary risk to AI-assisted offensive tradecraft (AI-generated malware, exploit scripts, phishing) documented elsewhere in the wiki. Here the adversary's product is the *vulnerability record itself*.

## The JFrog audit (SQLite batch, 30 Jul 2026)
JFrog established an isolated verification workflow: clone the official `sqlite/sqlite` repository, check out the target tags (3.41.0, 3.51.2, 3.51.3), compile official releases in isolated Docker containers, feed each advisory's PoC SQL verbatim into the compiled binaries under AddressSanitizer, and cross-check CPE/advisory metadata across NVD and GHSA. Findings:

- **CVE-2026-51302** (reported UAF in `exprComputeOperands()`, 9.8 Critical): `exprComputeOperands()` did not exist in SQLite 3.41.0 (added mid-2025). `sqlite3ReleaseTempReg()` merely recycles register indices and does not perform heap deallocation, so a UAF is impossible by design. PoC ran without crashing. Red Hat initially scored it 10.0, later downgraded to 7.6 High.
- **CVE-2026-51303** (reported UAF in `ExprListDelete()` back-refs, 9.8 Critical, "patched in 3.51.3"): no evidence of back-reference pointers in the relevant structures; a diff between 3.51.2 and 3.51.3 shows **no changes to `src/expr.c`**, so the "patch" was fabricated. PoC is invalid SQL that fails at the parser.
- **CVE-2026-51300** (reported UAF in `sqlite3ExprDelete()`, 9.1 Critical): the cited line numbers (1012, 1026) are a comment and a memory-allocation call, unrelated to `pLeft` or deletion logic. PoC executed successfully with zero leaks or errors.
- **CVE-2026-51297** (reported UAF via `jsonBlobEdit()`, 8.8 High): `jsonBlobEdit()` was not present in 3.41.0 (added later with the JSONB implementation). PoC hit a malformed-JSON error and never reached the JSON-modification logic.
- **CVE-2026-51296** (reported UAF in `jsonRemoveFunc`, 7.5 High): cited lines do not exist.
- **CVE-2026-51304** (reported UAF via `pOrderBy->nExpr` post-free, 7.5 High): cited a real function with a wrong argument number.

Additional signals: none of these CVEs are listed on SQLite's official advisory page; the repository's advisories flag as AI-generated under GPTZero; and combining all advisories into one file triggers AI-generated-content warnings.

## Defender heuristics
1. **Verify against the vendor's advisory page first.** For any "critical" CVE affecting a project that publishes an authoritative advisory page (SQLite, OpenSSL, etc.), cross-check the CVE against that page before acting. A CVE absent from the vendor's own advisory page is a strong red flag.
2. **Treat non-existent code references as disqualifying.** If an advisory cites a function, line, or structure that does not exist in the claimed target version, mark the record unverified rather than urgent.
3. **Prefer primary metadata over inherited severity.** Do not act solely on NVD/CISA-ADP or vendor CVSS scores for recently published, low-provenance CVEs; check whether a downstream scorer's high score (e.g., an initial 10.0) has been downgraded after review.
4. **Watch for the "patch that didn't happen."** If an advisory claims a fix in a specific release, diff the relevant source files between the adjacent versions; a claimed fix with no code change is fabricated.
5. **PoC-verify before emergency patching.** For unconfirmed high-severity CVEs, run the published PoC in an isolated, instrumented (ASan/UBSan) build before treating the flaw as real.
6. **Flag the LLM-slop signature.** Structurally plausible advisories with generic wording, GPTZero-positive text, pinned CPEs that don't match the real release, or `n/a` placeholders in NVD metadata are more likely AI-generated; route them to a secondary-verification queue.
7. **Track the source of the advisories.** A single newly-created repository publishing a large batch of "advisories" across many products is a pattern worth watching (compare the `programmervuln/cveadvisory-` batch); monitor that repository and any similar high-volume, low-history CVE publishers.
8. **Protect downstream automation.** Ensure automated patching, alerting, and SLA tooling has a provenance/verification gate so AI-generated false-critical records cannot trigger emergency changes or bury real ones.

## Related pages
- [AI-agent-found Log4j FilteredObjectInputStream bypass framed as "critical RCE" (Sonatype-2026-006746, Aug 27 2026)](../patterns/log4j-filteredobjectinputstream-ai-agent-bypass-sonatype-2026-006746.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [Phantom squatting: AI-hallucinated domains](../patterns/phantom-squatting-ai-hallucinated-domains.md)
- [ChocOpoc fake-PoC supply-chain campaign](../ops/chocopoc-fake-poc-supply-chain-campaign.md)

## Sources
- JFrog Security Research (Afek Berger), "SQLite Critical CVEs or LLM Slop?", 30 Jul 2026: [https://research.jfrog.com/post/sqlite-critical-cves-or-llm-slops/](https://research.jfrog.com/post/sqlite-critical-cves-or-llm-slops/)
- Adversary advisory batch repository (low provenance; treat as untrusted): `https://github.com/programmervuln/cveadvisory-`
