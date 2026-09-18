# CISA KEV September 18, 2026: three Linux kernel vulnerabilities — remotely triggerable kTLS zero-length-record mishandling (CVSS 9.8 AV:N) plus two local privilege escalations (AF_ALG concurrent-write race, ebtables SNAT out-of-bounds write into splice-shared file pages) — ALL THREE carrying CISA SSVC "active exploitation," all on a compressed 3-day BOD 26-04 deadline (due 2026-09-21)

## Tags
- ops
- operations
- CISA
- CISA KEV
- Linux
- Linux kernel
- local privilege escalation
- active exploitation
- BOD 26-04
- CVE-2025-39964
- CVE-2025-39682
- CVE-2026-53266
- kTLS
- TLS
- net/tls
- remote code execution
- AF_ALG
- crypto
- ebtables
- netfilter
- bridge
- out-of-bounds write
- CWE-362
- CWE-787
- container hosts
- shared hosting

## Summary

CISA's **September 18, 2026** KEV additions (catalog `2026.09.18`, **1,716 entries** — a third row landed later in the day, raising the batch from two to three) are **three Linux kernel vulnerabilities, ALL THREE with CISA SSVC assessments published Sep 18, 2026 grading exploitation "active," all on a compressed BOD 26-04 due date of 2026-09-21 — three days** — and Forensics Triage requirements on all three. None names an actor; ransomware use is unknown on all three. **Two 2025-vintage CVEs receiving 72-hour KEV deadlines ~12 months after their fixes shipped — and a June-2026 CVE getting one three months after its fix — is itself the exploitation-signal event.**

| CVE | Subsystem | Class | CVSS (kernel CNA) | CWE | KEV added | BOD due | CISA SSVC (Sep 18) |
|---|---|---|---|---|---|---|---|
| **CVE-2025-39682** | `net/tls` (kTLS RX path) | **Improper check for unusual/exceptional conditions** — a **zero-length record retrieved from the `rx_list`** bypasses the intended `recvmsg()` record-type handling, so **subsequent TLS records are processed under incorrect zero-copy and queuing assumptions** | **9.8 CRITICAL** (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) — **remote, no auth, no user interaction** | CWE-754 | 2026-09-18 | **2026-09-21** | **Exploitation: ACTIVE · Automatable: YES · Technical Impact: TOTAL** |
| **CVE-2025-39964** | `crypto: af_alg` | Race condition — concurrent writes to the same AF_ALG socket interleave data unpredictably and corrupt internal socket state | **7.8** (`AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`) | CWE-362 | 2026-09-18 | **2026-09-21** | Exploitation: ACTIVE · Automatable: NO · Technical Impact: TOTAL |
| **CVE-2026-53266** | `netfilter: bridge` (ebtables SNAT target) | **Out-of-bounds write** — the ARP sender-hardware-address rewrite writes directly into a **nonlinear socket-buffer fragment backed by a splice-imported file page** | **8.8** (`AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`, scope-changed) | CWE-787 | 2026-09-18 | **2026-09-21** | Exploitation: ACTIVE · Automatable: NO · Technical Impact: TOTAL |

All three rows carry the standard kernel language — "could be end-of-life (EoL) and/or end-of-service (EoS)… discontinue use and/or transition to a supported version" — and BOD 26-04 risk-based patching plus forensic-triage requirements. **Note the CVSS split on CVE-2025-39682:** the kernel CNA scored it 9.8 fully remote; NVD's own primary assessment scored it 7.1 local (`AV:L/PR:L`) — see the CVE section below for why the CNA's remote reading is the one that matches the commit.

## CVE-2025-39682 — kTLS zero-length record on the rx_list (the remote one)

- **Mechanism (from the fix, `tls: fix handling of zero-length records on the rx_list`):** kTLS `recvmsg()` must process either contiguous DATA records or exactly one non-DATA record per call; when a record has already been decrypted (TLS 1.3 — record type is unknown until decryption) it is queued to `rx_list` for the next `recvmsg()`. Zero-copy decryption (decrypted straight into the user buffer, no skb to queue) is only allowed for DATA records, so the type-change-after-zero-copy case was assumed impossible — **except when the initial record picked up from `rx_list` is zero-length**, the corner case the code missed. A subsequent record is then processed under the wrong zero-copy/queuing assumptions: kernel memory-corruption mechanics in the TLS receive path.
- **Why the CNA calls it remote:** the kernel CNA's CVSS scenario is explicit — *"the bug is triggered entirely by the sequence and content of TLS records arriving from the remote peer on a kTLS-enabled TCP socket; no local access is needed,"* and AC:L because **three back-to-back records (`[DATA][zero-length non-DATA][DATA]`) make the corruption deterministic — no race to win, no memory-layout dependency** (a kernel selftest ships with the fix). Any kTLS RX consumer is remotely reachable: **OpenSSL-with-kTLS servers/clients, NFS-over-TLS, SMB/RPC-over-TLS via `net/handshake`** (`net/tls/tls_sw.c` is the affected file). Treat this as **remote unauthenticated kernel memory corruption**, not a postfoothold bug — NVD's 7.1 `AV:L` primary appears to reflect a local-trigger interpretation; the SSVC adds **Automatable: YES** (the only one of the three), the combination CISA reserves for worm-adjacent risk.
- **Same late-listing story as its batch-mates:** CVE **published 2025-09-05**, fix upstream Aug 2025 with stable backports cited in the KEV row, then **~12 months un-KEV'd before a 72-hour deadline**. CISA does not state what changed; the listing plus SSVC "active" is the signal.
- **Public exploit code has existed since October 2025:** a published kernelCTF 1-day exploit for this CVE (a variant of the CVE-2024-58239 zero-length-record family) has been on GitHub since 2025-10-14 — attacker-reachable working code against the same `mitigation-*` kernel builds Google's kernelCTF runs, so the "what changed in the exploitation picture" question already has a public answer for anyone who looked: weaponization was not the missing piece; KEV listing lagged the public 1-day by a year.
- **Durable defense:** the exposed surface is hosts with **kTLS offload enabled** (kernel-config `CONFIG_TLS`, plus any consumer that negotiates it). Identify TLS terminators relying on kernel TLS rather than userspace TLS; patch is the answer — there is no practical workaround short of disabling `CONFIG_TLS`/kTLS usage, and SSVC "active + automatable" makes the 3-day federal deadline the right tempo for internet-facing kTLS hosts.

## CVE-2025-39964 — AF_ALG concurrent-write race

- **Upstream fix:** `crypto: af_alg - Disallow concurrent writes in af_alg_sendmsg` — the commit message is blunt: *"Issuing two writes to the same af_alg socket is bogus as the data will be interleaved in an unpredictable fashion. Furthermore, concurrent writes may create inconsistencies in the internal socket state."* Fixed by adding a `ctx->write` ownership field (multiple stable-tree commits, Sep–Oct 2025, cited in the KEV row).
- **Timeline is the story:** this CVE was **published 2025-10-13 and sat un-KEV'd for ~11 months** before CISA listed it on a 3-day deadline. KEV additions long after a fix ships are how CISA signals the exploitation picture *changed* — either in-the-wild use surfaced or field evidence accumulated. CISA does not state which; treat the listing as the signal, not a confirmed campaign.
- **Why AF_ALG matters:** AF_ALG is the kernel's socket-based userspace crypto API, reachable from **unprivileged** processes (historically via unprivileged user namespaces). It has a deep history as an LPE primitive family precisely because the internal `af_alg` state machine handles async I/O with shared buffers. The fix disallows concurrent writes outright rather than serializing them — a hint at how untrustworthy the interleaved path was.
- **Durable defense:** AF_ALG is **not needed** on most hosts — blocklisted by many hardened kernels and container runtimes already. `modprobe` blacklist `algif_aead`/`algif_skcipher` (or disable AF_ALG socket creation via seccomp in container profiles) removes the class regardless of patch state.

## CVE-2026-53266 — ebtables SNAT rewrite into splice-shared file pages

- **Upstream fix:** `netfilter: bridge: make ebt_snat ARP rewrite writable` — at the bridge ebtables hooks the Ethernet header is addressed through `skb_mac_header()`/`eth_hdr()`, while `skb->data` points at the payload; the SNAT target's ARP sender-hardware-address rewrite was **not preceded by a writability/linearization check** for the nonlinear case, so when the header region sat in a **nonlinear skb fragment backed by a page imported via `splice`** (i.e., a **page-cache file page shared with the original file**), the rewrite **modified shared file-backed memory directly** — an out-of-bounds/shared-memory write class of the `Dirty Pipe`/`dirty pagetable` family, where corrupting page cache contents is the LPE lever. Scope-changed CVSS 8.8 (kernel CNA), published 2026-06-25, stable commits cited in the KEV row.
- **Preconditions matter for triage:** the vector is **local** (`AV:L`, low privileges) and reaches the bridge ebtables SNAT path with `CAP_NET_ADMIN`-adjacent namespace access — the realistic ITW shape is a **container or unprivileged-user-namespace foothold** using ARP-path crafted frames against bridge processing. That is exactly the shared-hosting / container-host kill chain: webshell → namespace foothold → kernel LPE → root on every tenant's workload.
- **Durable defense:** the class fix is systemic — **reject nonlinear skb writes to shared pages**; the durable host control is that **unprivileged user namespaces + network namespace creation = kernel attack surface**, and hosts running untrusted code (shared hosting, CI runners, agent sandboxes) should gate `net`/`bridge`/`ebtables` capabilities in the namespace, or disable unprivileged userns entirely where the workload allows.

## Defender takeaways

- **Read the batch through SSVC, not just the CVSS column: CISA graded ALL THREE "active exploitation" on Sep 18, and only the kTLS bug "Automatable: yes."** A remote, deterministic, no-race kernel TLS-corruption bug with active exploitation is the loudest signal in the set — triage kTLS-enabled internet-facing hosts first, then the two local escalations.
- **Three-day BOD deadline on all three (2026-09-21) is the urgency signal.** Federal assets must patch or mitigate in 72 hours; that cadence is what CISA reserves for exploitation-informed items.
- **Two 2025-vintage kernel CVEs listed ~12 months after their fixes shipped — plus a fresh June-2026 CVE on the same 72-hour window — all SSVC-active the same day says CISA holds field evidence across the kernel exploit space, not one campaign.** Treat the listings jointly: something changed in the exploitation picture for kernel primitives broadly.
- **The AF_ALG and ebtables bugs are postfoothold LPEs; the kTLS bug is not.** The defensive question for the LPE pair is what your local-foothold blast radius looks like: a kernel LPE converts a single webshell or container escape into whole-host compromise, and on shared hosts every tenant with it. The kTLS bug reaches you before any foothold.
- **Patch level:** apply the stable-tree commits per the KEV notes (kernel.org links in each row) or the distro kernel errata that carry them; EoL kernels (the KEV's explicit EoL/EoS note) have **no fix path — migrate or remove from internet/namespace-reachable hosts**.
- **Forensics Triage = Yes on all three:** preserve memory/disk evidence per the BOD 26-04 triage guidance before re-imaging; a page-cache-corruption LPE leaves file-backed evidence in odd places, and TLS-path memory corruption may leave evidence only in memory.
- **Container-runtime hardening closes the two LPE classes ahead of patch cycles:** seccomp profiles that deny `socket(AF_ALG)` and drop `CAP_NET_ADMIN` in user namespaces remove the reach for both bugs; the CVEs are then depth, not the primary control. No comparable mitigation exists for kTLS short of patching — inventory which TLS terminators use kernel TLS.
- **Pattern read:** this is the second September 2026 KEV group arriving on **compressed deadlines with the EoL warning language** (after the Cisco ISE batch on 3-day-comparable windows) — CISA's 2026 cadence increasingly treats "supported version" as the remediation, not "patch the version you're on."

## Related pages

- [CISA KEV September 16, 2026 batch (Cisco ISE + Acronis)](cisa-kev-cisco-ise-acronis-backup-september-16-2026.md) — the immediately preceding batch, also compressed deadlines
- [CISA KEV September 10–11, 2026 batch](cisa-kev-screenconnect-artifactory-gitlab-mikrotik-september-10-11-2026.md)
- [Google Pixel cellular-modem CVE-2026-58704 KEV page](google-pixel-cellular-modem-cve-2026-58704-kev-targeted-exploitation-september-2026.md) — earlier in the same September run of short-deadline listings
