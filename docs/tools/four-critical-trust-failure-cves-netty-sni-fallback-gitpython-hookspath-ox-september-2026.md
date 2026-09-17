# Four critical CVEs in one 24-hour window, one shared failure: OX Security's root-cause analysis of Netty CVE-2026-75595 (fragmented ClientHello → mTLS bypass) and GitPython CVE-2026-78676 (dormant config value → live `core.hooksPath` → RCE), alongside the two Next.js RCEs (Sep 14, 2026)

## Summary
On **September 14, 2026**, OX Security published a paired disclosure round-up ("Four Critical CVEs, the Same Trust Issue" + a detailed technical analysis) covering **four unauthenticated-critical vulnerabilities that landed within a single 24-hour window** across widely deployed infrastructure: two in **Next.js**, one in **Netty**, one in **GitPython**. All four are remotely reachable, all require no authentication, and **three of the four sit in code paths that are on by default**. OX's durable framing: *every one is the same story — two pieces of software that had blind trust in each other, and neither checked*. Two of the four are new here: **Netty CVE-2026-75595** (`GHSA-c4c3-7fpv-j4q5`, CVSS v4.0 **9.1**) — a five-byte offset error in the TLS ClientHello parser lets a legally-fragmented handshake fall back to the **default `SslContext`**, escalating to a full **unauthenticated mTLS bypass** wherever per-SNI context selection is the sole gate; and **GitPython CVE-2026-78676** (`GHSA-284h-m62q-gf8w`, CVSS **9.8**, fixed **3.1.59**) — a **read-then-corrupt-on-rewrite** bug in `GitConfigParser` that turns a dormant, spec-compliant multi-line config value into **live injected directives such as `core.hooksPath`** on any unrelated write, i.e. code execution through git's own hook mechanism. The two Next.js flaws (AVIF/libheif heap overflow `GHSA-2xp9-vwfh-vxw4` and Windows path traversal **CVE-2026-75604**) are covered on the [Next.js August 2026 security release page](../ops/nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md) — that page now carries OX's newly disclosed Windows attack mechanism.

## Tags
- tools
- Netty
- CVE-2026-75595
- GHSA-c4c3-7fpv-j4q5
- GitPython
- CVE-2026-78676
- GHSA-284h-m62q-gf8w
- SNI routing bypass
- mTLS bypass
- fragmented ClientHello
- SslClientHelloHandler
- fail-open
- git config injection
- core.hooksPath
- argument injection
- code injection
- trust boundary
- OX Security
- Next.js
- libheif

## Netty CVE-2026-75595 — a bounds check five bytes short becomes an authentication decision
`io.netty.handler.ssl.SslClientHelloHandler` parses the TLS ClientHello to extract the SNI hostname so an `SslContext` can be selected **per hostname** (the common way to enforce per-route mTLS on a shared listener). TLS permits a handshake message to be split across records, so the handler must tolerate an incomplete header — and its guard for that case is **five bytes short**:

- The guard asks whether **4** readable bytes remain (`readerIndex + 4 > endOffset`), but the reads that follow start at `readerIndex + SSL_RECORD_HEADER_LENGTH` (the **5-byte TLS record header**), so completing the handshake-type + 3-byte-length read actually needs **9** readable bytes. `readerIndex` before vs. after the record header — the two lines disagree.
- A legal input — a first record with a **1–3 byte payload** — passes the guard, then reads past the readable region and raises `IndexOutOfBoundsException`.
- The generic `catch (Exception)` handler treats an unparseable ClientHello as "ignore SNI and use default": `select(ctx, null)` — **the default `SslContext`**. Not rejected, not deferred: **granted the fallback**.
- Escalation to unauthenticated mTLS bypass requires the deployment shape named in the advisory: mTLS enforced **solely** via a per-SNI context (`clientAuth=REQUIRE`), the **default/fallback context permissive** (`NONE`/`OPTIONAL`), and **no application-layer peer-certificate verification**.
- A second defect in the same method had the same effect: `handshakeLength` was a **local** variable reset to `-1` on every `decode()` call, so partial parsing could never survive across reads.

**The patch** (fixed in **4.1.137.Final** and **4.2.17.Final**) corrects the bounds check to include the record header and inverts it so parsing proceeds only when the full header is present, moves parser state (`aggregatedBytes`, `handshakeLength`) from locals onto the handler so fragmented ClientHellos are reassembled, and routes incomplete headers to an aggregation path. **Critically, the patch does NOT remove the fail-open handler** — `select(ctx, null)` on parse failure remains (at debug logging). The fix closes *this route* to the fallback; the advisory itself names the design as the reason the bug mattered: **fallback-to-default on parse failure is a problem when per-SNI selection is the sole gate**. Defenders should treat "which SslContext answers when SNI is absent/unparseable" as an audit item on every Netty-based TLS terminator, independent of this CVE.

## GitPython CVE-2026-78676 — dormant config values weaponized on the next unrelated write
GitPython ≤ **3.1.58** round-trips git config files **read-then-rewrite**, and the writer corrupts legal syntax into injected directives:

- **Read side (correct):** `_read()` supports git's own backslash-continuation syntax for multi-line quoted values, and `string_decode()` applies `unicode_escape` — so a literal `\n` sequence inside a quoted value becomes a **real embedded newline** in the Python string. Given `[core] zzz = "A\nhooksPath = ../evil-hooks\"`, both real `git config --get core.zzz` and GitPython return one inert string; `git config --get core.hooksPath` returns nothing. **The value is one option, and it is harmless.**
- **Write side (the bug):** `write_section()` calls the **unsafe** `_value_to_string()` and "handles" embedded newlines with `.replace("\n", "\n\t")` — emitting a real newline + tab, **unquoted, with no continuation backslash**. Git's rule is that a value continues only when the previous line ends in a literal backslash. So git re-reads the file as **two options**: `zzz = A` **and `hooksPath = ../evil-hooks`** — `core.hooksPath` now exists, **created by GitPython**, in whatever section the dormant value sat in.
- **Why guards didn't help:** GitPython already had `UNSAFE_CONFIG_CHARS_RE` / `_value_to_string_safe()` / `_assure_config_name_safe()` — added to close **four earlier config-injection GHSAs** — but they only guard values passed as **arguments** to `set()` / `set_value()` / `add_value()` / `add_section()`. They are **never consulted for values that entered via `_read()`** from an on-disk config file, and no raw control byte is ever written to disk — the on-disk syntax is exactly what real `git` accepts.
- **Impact:** any GitPython-mediated write to a repo's config (an unrelated `set()`, a tool that touches config at all) **activates a dormant payload planted by any earlier attacker/tool that could write config text** — e.g. `core.hooksPath` pointing at attacker-named hooks = **arbitrary code execution on the next git operation** (commit, checkout, clone-side tooling). CVE-2026-78676, CVSS **9.8**, CWE-88/CWE-94, fixed in **GitPython 3.1.59**.

## Why it matters
- **Fail-open TLS parsing is an authentication boundary.** Netty is the TLS substrate for a vast share of Java services, gateways, and API servers (including mTLS-fronted internal service meshes). Where per-SNI selection is the only mTLS enforcement, an unauthenticated remote client could pick the permissive default context at will. The patch leaves the fail-open handler standing — **inventory your fallback context now**.
- **A git config value that is inert today is armed tomorrow.** Any CI runner, automation, or AI-agent tooling that writes git config through GitPython can silently promote a planted value into `core.hooksPath` / `core.fsmonitor`-class execution directives. Audit repo config files in automation images for **quoted multi-line values with embedded escape sequences** — that is the dormant-value fingerprint.
- **The 24-hour cluster is itself the signal.** Four unauthenticated criticals across Next.js (×2), Netty, and GitPython in one day is the LLM-assisted-discovery volume showing up in real patch cadence — the same "remediation problem" shape the ecosystem has been tracking all September.
- **Cross-vendor timing note:** all four advisories were published on GitHub **September 8, 2026**; OX's write-ups followed Sep 14. No in-the-wild exploitation was reported for any of the four at publication.

## Defender heuristics
1. **Netty:** upgrade `io.netty:netty-handler` to **4.1.137.Final / 4.2.17.Final**. Independent of patching: ask what happens when SNI is missing or unparseable on every TLS terminator you run — if per-SNI `clientAuth=REQUIRE` is your only mTLS gate and the default context is permissive, you were bypassable and are one parser-bug away from it again. Add application-layer peer-cert verification where mTLS is load-bearing.
2. **GitPython:** upgrade to **3.1.59** everywhere (CI images, automation venvs, agent toolchains). Hunt repo/global git configs for quoted multi-line values (`"..."` spanning lines, embedded `\n` escapes) that you did not intentionally author; treat `core.hooksPath` appearing in a config you never set as a compromise indicator, not a bug report.
3. **Next.js apps** (same cluster): see the [Next.js release page](../ops/nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md) — 15.5.24 / 16.3.3, Windows hosts first (no workaround), track libheif 1.23.2 for the AVIF path.
4. **Pattern-level:** the four CVEs are one lesson wearing four uniforms — **validate the thing you're about to trust, not the layer next to you**: Netty trusted its own parser's exception path, GitPython trusted its own reader's output, Next.js trusted libheif with attacker bytes, and the Windows cache-path join trusted that route segments contained no backslash.

## Sources
- OX Security: [Four Critical CVEs, the Same Trust Issue](https://www.ox.security/blog/four-critical-cves-the-same-trust-issue/) (Sep 14, 2026)
- OX Security: [Technical Analysis: Netty CVE-2026-75595, Next.js CVE-2026-75604, GHSA-2xp9-vwfh-vxw4 & GitPython CVE-2026-78676](https://www.ox.security/blog/technical-analysis-netty-cve-2026-75595-next-js-cve-2026-75604-ghsa-2xp9-vwfh-vxw4-gitpython-cve-2026-78676/) (Sep 14, 2026)
- GitHub Advisory: [GHSA-c4c3-7fpv-j4q5 — Netty SNI Routing Bypass via Fragmented TLS ClientHello (CVE-2026-75595)](https://github.com/advisories/GHSA-c4c3-7fpv-j4q5)
- GitHub Advisory: [GHSA-284h-m62q-gf8w — GitPython dormant multi-line config values corrupted into live injected directives (CVE-2026-78676)](https://github.com/advisories/GHSA-284h-m62q-gf8w)
- GitHub Advisory: [GHSA-2xp9-vwfh-vxw4 — Next.js unauth RCE via AVIF image optimization](https://github.com/advisories/GHSA-2xp9-vwfh-vxw4)
- GitHub Advisory: [GHSA-p293-qw3h-jr36 — Next.js unauth RCE on Windows-hosted servers (CVE-2026-75604)](https://github.com/advisories/GHSA-p293-qw3h-jr36)

## Related pages
- [Next.js August 2026 security release (AVIF/libheif + Windows path traversal)](../ops/nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md)
- [Bifrost CVE-2026-90898 unauthenticated MCP stdio RCE](bifrost-cve-2026-90898-mcp-stdio-unauthenticated-rce.md) — same month's auth-boundary failures in AI infrastructure
- [ParaShells — Parallels Desktop argument injection to root](parashells-parallels-desktop-appliance-extract-argument-injection-root-cve-2026-90894.md) — the same "parameters become code" family on the exec side
