# Cloudflare Workers remote Spectre attack leaks co-tenant JWT

## Summary
Researchers (TU Graz and independent collaborators, paper on arXiv: 2608.17043) demonstrated a **remote Spectre attack against production Cloudflare Workers** that leaked a JSON Web Token from a co-located worker at up to **12 bits per second** — about 360× faster than the 2021 remote-Spectre demonstration against the same platform. The end-to-end experiment used an attacker worker and a victim worker both under the researchers' control, with a JWT intentionally placed in the victim's memory; **no customer data was accessed**, and Cloudflare found **no indicators of active exploitation** over the preceding three years. Cloudflare states the attack is **mitigated in production** after improving Dynamic Process Isolation (DyPrIs), integrating the V8 Sandbox, and deploying Memory Protection Keys (MPK)-based in-process isolation.

## Tags
- ops
- operations
- Cloudflare Workers
- Spectre
- side channel
- multi-tenant isolation
- V8 isolate
- Durable Objects
- JWT
- cross-tenant leakage
- timing attack
- DyPrIs
- MPK

## Why this matters
- **The architectural lesson is durable:** Workers runs multiple tenants' code in separate V8 isolates within the *same* OS process, trading strict process isolation for startup latency. Any memory read in the shared process can become a cross-tenant leak channel.
- **DyPrIs is an after-the-fact mitigation, not a hard boundary.** It isolates a suspicious script into a separate process *after an invocation finishes*. A long-lived Durable Object invocation can keep an isolate alive for 5–20+ hours and keep running *before* isolation triggers.
- **The attacker can evade the isolation detector.** WebSocket-heavy I/O raises instruction-TLB (iTLB) activity, which suppresses the normalized branch-misprediction signal DyPrIs uses, dropping it below its detection threshold.
- **Remote timing sources exist in the Workers model.** Workers freeze or coarsen local timers during CPU execution and expose no shared memory or multithreading to worker scripts, but WebSocket communications provide a remote timing channel sufficient for the leak.
- **Cross-tenant token theft changes the blast radius of any misconfigured secret** placed in worker memory: a co-located malicious worker need not exploit V8 or escape a sandbox at all.

## Attack model
1. Attacker and victim workers are co-located in separate V8 isolates inside one Worker OS process; the attacker runs its own valid code in its isolate.
2. The attacker's Spectre gadget turns branch-prediction side channels into a byte-wise read of the victim isolate's memory.
3. WebSocket round-trips supply the timing source (local timers are frozen/coarsened; shared memory is not exposed).
4. Durable Objects let a single isolate stay alive long enough for slow exfiltration (5–20+ hour invocations observed), and heavy WebSocket I/O degrades DyPrIs's misprediction-based detection.
5. The experiment exfiltrated a deliberately planted JWT at up to 12 bits/second.

## Defender takeaways
- **Harden the boundary assumption:** treat co-tenancy on shared-process edge platforms as a real threat model; do not rely on language-level isolate isolation for secrets.
- **Keep secrets out of worker memory where possible;** prefer signed, short-lived, per-tenant credentials and external secret stores with per-call scoping rather than long-lived tokens resident in isolate memory.
- **Watch for platform mitigation changes** (V8 Sandbox integration, MPK in-process isolation) and re-benchmark any in-house isolation assumptions after they land.
- **For operators of Durable Object–style long-lived isolates:** prefer shorter invocations, avoid placing cross-tenant secrets in long-lived isolate state, and monitor for abnormal cross-worker timing patterns.
- This is a platform-vendor-disclosed mitigation, not a KEV/actively-exploited determination: Cloudflare reports no active exploitation in the last three years and the production implementation is described as insufficient only in the pre-mitigation state.

## Assessment limits
- The researchers' victim worker and JWT were self-controlled; the demonstration does not prove exploitation against real customers.
- No CVE is referenced; the write-up frames the issue as a DyPrIs implementation limitation plus the general shared-process tenancy model.
- Mitigation status (DyPrIs improvements, V8 Sandbox, MPK) is Cloudflare's statement; independent confirmation is not yet public.

## Sources
- Paper: [arXiv:2608.17043 — remote Spectre attack on Cloudflare Workers](https://arxiv.org/abs/2608.17043)
- Cloudflare: [Safe in the sandbox: security hardening for Cloudflare Workers](https://blog.cloudflare.com/safe-in-the-sandbox-security-hardening-for-cloudflare-workers/)
- The Hacker News: [Cloudflare Workers Spectre Attack Leaks JWT From Co-Located Worker at 12 Bits/Second](https://thehackernews.com/2026/08/cloudflare-workers-spectre-attack-leaks.html) — August 19, 2026
