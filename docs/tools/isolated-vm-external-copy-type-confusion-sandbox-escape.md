# isolated-vm ExternalCopy type-confusion sandbox escape (GHSA-864f-rcv7-6rh4)

## Summary
**isolated-vm** (npm, 1M+ downloads/week), the V8-based JavaScript sandbox that n8n, Activepieces, Mastra, Sim.ai, Directus, and many other AI-agent and low-code/automation platforms use to run model- and user-generated code inside a real V8 isolate, was breakable from the guest side. A critical type-confusion flaw in the host-to-sandbox data handoff — `ivm.ExternalCopy(value, { transferList })` — let a single `Reference` shared into the sandbox be weaponized into a guest-to-host sandbox escape with demonstrated control-flow hijacking (full host RCE), not just a crash.

The root cause is a time-of-check-to-time-of-use (TOCTOU) gap in `src/external_copy/serializer.cc`: the `transfer_list` array is walked **twice**. Walk 1 validates each element with `handle->IsArrayBuffer()`. Walk 2 does an unchecked `handle.As<ArrayBuffer>()` reinterpret-cast. Because `transfer_list` is an ordinary JS array read through `array->Get(context, index)`, a stateful index-getter can return a real `ArrayBuffer` on walk 1 (passing validation) and a different value — e.g. the integer `0x41414141` — on walk 2, so the unchecked cast corrupts a V8 object handle.

Because the confused object can be steered into a JS string, the attacker controls which bytes are later read as an object's fields, and `Transfer`'s destruction path ends in an indirect call through a vtable pointer read from that memory — a classic control-flow-hijack primitive. Endor Labs demonstrated a PoC that (1) recovers the host's ASLR base from a leaked pointer, (2) forges a fake control block and vtable in sprayed heap, and (3) drives the indirect call to a chosen libc function. Working entirely inside the sandbox, with only a single `Reference` endowment and no debugger.

Fixed in **isolated-vm 7.0.1** and **6.2.0** (published 2026-08-05 / 2026-08-06), which wrap `ExternalCopy::Copy` in `v8::Isolate::DisallowJavascriptExecutionScope`, preventing user JS (getters, proxies, interceptors) from running during the copy. The advisory **GHSA-864f-rcv7-6rh4** was published to the GitHub Advisory Database 2026-08-07 (critical); a CVE assignment is still pending. No in-the-wild exploitation is reported.

## Tags
- tools
- isolated-vm
- Node.js
- JavaScript
- V8
- sandbox escape
- type confusion
- TOCTOU
- control-flow hijacking
- host RCE
- npm
- AI agent
- supply-chain
- critical vulnerability
- GHSA-864f-rcv7-6rh4
- Endor Labs

## Why this matters
- isolated-vm is the load-bearing trust boundary for a large class of production systems that run untrusted or model-generated JavaScript: n8n (~200k stars) Code-node task runners, Activepieces (~23k) sandboxed "pieces", Mastra (~27k) "code mode" tool-orchestration, Budibase (~28k, which migrated off the deprecated vm2 to isolated-vm in v2.20.0), Sim.ai (~29k) Function/Code workflow blocks, Directus (~37k, which replaced vm2 with isolated-vm in v10.6.0) "Run Script" in Flows, and Rocket.Chat (~46k) integration scripts. The project's own documentation also lists Screeps (MMO player code), Fly.io (edge compute), Algolia (Custom Crawler), and TripAdvisor (SSR).
- These platforms deliberately lock the isolate down to input/output value sharing only — no filesystem, no network — and rely entirely on the V8 isolate boundary. The flaw shows that boundary is only as strong as the C++ native binding/glue code that carries data across it. As Endor Labs frames it: "When a safe building block is wrapped in native binding code, the security of the whole system is reduced to that of the binding."
- The minimum impact is a reliable, attacker-controlled host crash (DoS); the maximum is host RCE. For a host running an AI-agent or automation backend that also holds credentials, registry access, or cloud tokens, that is a full compromise primitive reachable by any code the platform is willing to sandbox.

## Mechanism
The guest needs only a single `ivm.Reference` — the standard host-to-sandbox capability handoff. From inside the guest the attacker recovers the `ExternalCopy` constructor via `const ExternalCopy = ref.getSync('anyKey', { externalCopy: true }).constructor;`, then constructs a confused `transferList`.

`ExternalCopy` uses V8's structured-clone machinery (`ValueSerializer`) and supports a `transferList` optimization borrowed from the `postMessage` API: instead of copying large `ArrayBuffer`s byte-for-byte, the caller lists them and their underlying memory is transferred (detached). The serialization code in `src/external_copy/serializer.cc` iterates that list twice:

```cc
// walk 1 — validates
for (auto handle : transfer_list) {
  if (handle->IsArrayBuffer()) {
    serializer.TransferArrayBuffer(ii++, handle.As<ArrayBuffer>());
  } else {
    throw RuntimeError("Non-ArrayBuffer passed in `transferList`");
  }
}
// walk 2 — unchecked cast
... handle.As<ArrayBuffer>() ...
```

The PoC makes `transferList[0]` a stateful getter that returns the real `ArrayBuffer` on the first read and `0x41414141` on the second:

```js
let reads = 0;
Object.defineProperty(transferList, 0, {
  enumerable: true,
  get() { return ++reads === 1 ? real : 0x41414141; }  // valid on read #1, confused on read #2
});
```

Walk 1 sees `real`, passes `IsArrayBuffer()`, and proceeds. Walk 2 receives `0x41414141`, casts it to `ArrayBuffer`, and dereferences it — the crash PoC faults in `v8::ArrayBuffer::IsDetachable` at address `0x4141414100000047`.

**Escalation.** By steering the confused object into a JS string, the attacker controls which bytes are read as the object's fields. `Transfer`'s destruction path ends in an indirect call through a vtable pointer read from that attacker-influenced memory. The demonstrated PoC (1) recovers the host ASLR base from a pointer leaked through ordinary buffer operations, (2) forges a fake control block and vtable in heap it sprays, and (3) drives the indirect call to a chosen libc function. The full exploit was withheld publicly and shared privately with the maintainer.

## Affected and patched versions
| Product | Affected | Patched |
|---|---|---|
| isolated-vm (npm) | < 7.0.1 and < 6.2.0 | 7.0.1 (latest), 6.2.0 (backport-v6) |

npm dist-tags: `latest` = 7.0.1, `backport-v6` = 6.2.0, `legacy` = 1.7.11. The 7.0.1 / 6.2.0 releases landed 2026-08-05 / 2026-08-06, ahead of the 2026-08-07 advisory publication. The fix wraps `ExternalCopy::Copy` in `v8::Isolate::DisallowJavascriptExecutionScope`, so no user JavaScript (getters, proxies, interceptors) can run while the transfer list is being walked.

## Upgrade notes
- Bump to **isolated-vm ≥ 7.0.1** (or ≥ 6.2.0 on the v6 line). Verify the resolved version in `package.json`, lockfiles, and `node_modules/isolated-vm/package.json` across any host that runs n8n, Mastra, Activepieces, Budibase, Sim.ai, Directus, Rocket.Chat, or similar isolated-vm-based backends.
- If you embed isolated-vm directly, the fix is version-only — there is no embedder-side configuration or workaround; the flaw is reachable with the default single-`Reference` handoff.
- Treat any other V8-isolate or native-binding sandbox the same way: audit the C++ glue that moves data across the boundary, not just the isolate flag settings.

## Detection
- Inventory every host that runs isolated-vm-based services and check the resolved version; anything < 7.0.1 / < 6.2.0 is exposed to the guest→host primitive.
- Host-crash correlation: unexplained Node host process crashes (SIGSEGV in V8 internals such as `v8::ArrayBuffer::IsDetachable`) on sandboxing services, especially ones that just started executing user/model-generated code, are consistent with the crash PoC.
- Memory-forensics / ASLR hints: for a host suspected of a full exploit, look for sprayed heap with forged control blocks and vtables, and for indirect calls into libc from paths that should be sandboxed.
- Supply-chain lens: watch for any isolated-vm-based platform shipping a pinned or vendored copy of isolated-vm below 7.0.1, and for typosquat/dependency-confusion attempts against the `isolated-vm` name while the advisory is hot.

## Assessment limits
- Endor Labs (Cris Staicu) published the analysis on 2026-08-20; the full RCE exploit was not made public and was shared privately with the maintainer, so independent public confirmation of the full host-RCE chain is not yet available.
- No in-the-wild exploitation, PoC abuse, or actor linkage is reported as of publication.
- No CVE has been assigned yet (GHSA-864f-rcv7-6rh4 only); track the advisory for the CVE backfill.
- The practical blast radius for a given host depends on what that host can reach once RCE is achieved; containerized or heavily-egress-gated hosts lose less than bare-metal ones, but the host-process primitive still applies.

## Related pages
- [vm2 NodeVM host state exposure and DNS hijack](vm2-nodevm-host-dns-hijack.md)
- [Agentic workflow trust-boundary failures](../patterns/agentic-workflow-trust-boundary-failures.md)
- [Agent localhost control-plane RCE](../patterns/agent-localhost-control-plane-rce.md)

## Sources
- Endor Labs (Cris Staicu): [GHSA-864f-rcv7-6rh4: Critical Type Confusion Vulnerability in isolated-vm](https://www.endorlabs.com/learn/ghsa-864f-rcv7-6rh4-critical-type-confusion-vulnerability-in-isolated-vm) — August 20, 2026
- GitHub: [GHSA-864f-rcv7-6rh4 advisory](https://github.com/advisories/GHSA-864f-rcv7-6rh4)
- Repository: [laverdet/isolated-vm](https://github.com/laverdet/isolated-vm) (npm `isolated-vm`, 7.0.1 / 6.2.0 fixes)
