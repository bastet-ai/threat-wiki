# shopsprint/decimal Go typosquat DNS backdoor

## Summary
Socket reported a long-running Go module typosquat, **`github.com/shopsprint/decimal`**, impersonating the popular `github.com/shopspring/decimal` fixed-point arithmetic library. The typosquat reportedly existed for years as a benign-looking mirror before version `v1.3.3` added an `init()` backdoor that polled DNS TXT records and executed returned commands.

The original GitHub repository and owner account were removed, but Socket noted that Go module proxy caching can continue serving the malicious version. That makes this a durable ecosystem lesson: deleted upstream source does not necessarily erase a poisoned module artifact from package-resolution paths.

## Tags
- ops
- operations
- supply-chain
- Go
- typosquatting
- DNS C2
- backdoor
- command-execution
- module-proxy

## Why this matters
- A one-character namespace typo (`shopspring` → `shopsprint`) can pass compilation and tests when the malicious package preserves the legitimate API.
- Go `init()` execution means the payload can run automatically at process startup when the package is imported.
- Go module proxy retention can preserve malicious artifacts after the source repository and owner account disappear.

## Reported chain
1. The typosquat `github.com/shopsprint/decimal` mirrored `shopspring/decimal` releases from 2017 onward.
2. Version `v1.3.2` added legitimate-looking upstream bugfixes.
3. Seven minutes later, version `v1.3.3` retained those fixes and added imports for `net`, `os/exec`, and `time` plus a malicious `init()` function.
4. The backdoor spawned a goroutine, queried TXT records for `dnslog-cdn-images[.]freemyip[.]com` every five minutes, and executed each returned TXT value with `os/exec.Command`.

## Defender heuristics
- Search Go source, `go.mod`, dependency graphs, module proxy caches, and build logs for `github.com/shopsprint/decimal`; the expected legitimate import path is `github.com/shopspring/decimal`.
- Flag Go modules that add `init()` functions, process execution, DNS lookups, or network imports to libraries that should be pure data/math code.
- Treat module-path typo detection as a supply-chain control, not just a linting nicety.
- Account for Go module proxy retention during incident response; removing a GitHub repository may not remove the cached malicious zip from all consumers.
- Hunt DNS logs for repeated TXT lookups to `dnslog-cdn-images[.]freemyip[.]com` and process telemetry for commands spawned by applications importing the typosquat.

## Related pages
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- [Socket](https://socket.dev/blog/popular-go-decimal-library-typosquat-dns-backdoor)
