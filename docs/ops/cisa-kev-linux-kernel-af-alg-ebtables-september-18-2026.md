# CISA KEV September 18, 2026: two Linux kernel local privilege escalations — AF_ALG concurrent-write race and ebtables SNAT out-of-bounds write into splice-shared file pages — both on a compressed 3-day BOD 26-04 deadline (due 2026-09-21)

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
- CVE-2026-53266
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

CISA's **September 18, 2026** KEV additions (catalog `2026.09.18`, **1,715 entries**) are **two Linux kernel vulnerabilities, both local privilege escalations, both with a compressed BOD 26-04 due date of 2026-09-21 — three days** — and Forensics Triage requirements on both. Neither names an actor; ransomware use is unknown on both.

| CVE | Subsystem | Class | CVSS (kernel CNA) | CWE | KEV added | BOD due |
|---|---|---|---|---|---|---|
| **CVE-2025-39964** | `crypto: af_alg` | Race condition — concurrent writes to the same AF_ALG socket interleave data unpredictably and corrupt internal socket state | **7.8** (`AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`) | CWE-362 | 2026-09-18 | **2026-09-21** |
| **CVE-2026-53266** | `netfilter: bridge` (ebtables SNAT target) | **Out-of-bounds write** — the ARP sender-hardware-address rewrite writes directly into a **nonlinear socket-buffer fragment backed by a splice-imported file page** | **8.8** (`AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`, scope-changed) | CWE-787 | 2026-09-18 | **2026-09-21** |

Both rows carry the standard kernel language — "could be end-of-life (EoL) and/or end-of-service (EoS)… discontinue use and/or transition to a supported version" — and BOD 26-04 risk-based patching plus forensic-triage requirements.

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

- **Three-day BOD deadline on both (2026-09-21) is the urgency signal.** Federal assets must patch or mitigate in 72 hours; that cadence is what CISA reserves for exploitation-informed items.
- **Both are postfoothold LPEs, not remote 0-days — the listing presumes attackers already have local code execution.** The defensive question is what your local-foothold blast radius looks like: a kernel LPE converts a single webshell or container escape into whole-host compromise, and on shared hosts every tenant with it.
- **Patch level:** apply the stable-tree commits per the KEV notes (kernel.org links in the row) or the distro kernel errata that carry them; EoL kernels (the KEV's explicit EoL/EoS note) have **no fix path — migrate or remove from internet/namespace-reachable hosts**.
- **Forensics Triage = Yes on both:** preserve memory/disk evidence per the BOD 26-04 triage guidance before re-imaging; a page-cache-corruption LPE leaves file-backed evidence in odd places.
- **Container-runtime hardening closes both classes ahead of patch cycles:** seccomp profiles that deny `socket(AF_ALG)` and drop `CAP_NET_ADMIN` in user namespaces remove the reach for both bugs; the CVEs are then depth, not the primary control.
- **Pattern read:** this is the second September 2026 KEV pair arriving on **compressed deadlines with the EoL warning language** (after the Cisco ISE batch on 3-day-comparable windows) — CISA's 2026 cadence increasingly treats "supported version" as the remediation, not "patch the version you're on."

## Related pages

- [CISA KEV September 16, 2026 batch (Cisco ISE + Acronis)](cisa-kev-cisco-ise-acronis-backup-september-16-2026.md) — the immediately preceding batch, also compressed deadlines
- [CISA KEV September 10–11, 2026 batch](cisa-kev-screenconnect-artifactory-gitlab-mikrotik-september-10-11-2026.md)
- [Google Pixel cellular-modem CVE-2026-58704 KEV page](google-pixel-cellular-modem-cve-2026-58704-kev-targeted-exploitation-september-2026.md) — earlier in the same September run of short-deadline listings
