# node-ipc 2026 npm maintainer-account compromise

## Summary

In May 2026, Socket and Snyk reported malicious releases of the widely used npm package **`node-ipc`**. The compromised versions were `9.1.6`, `9.2.3`, and `12.0.1`, all published on May 14, 2026, and contained an obfuscated credential-stealing payload in the CommonJS bundle `node-ipc.cjs`.

Current public reporting points to abuse of a legitimate npm maintainer account rather than compromise of the upstream project CI/CD pipeline. Researchers highlighted a likely expired-domain/account-recovery path involving a dormant maintainer account, but that root cause should be kept as a strong public lead rather than independently proven fact.

## Tags
- ops
- operations
- supply-chain
- npm
- maintainer-compromise
- account-takeover
- credential-theft
- node-ipc

## Why this matters
- `node-ipc` is a high-reach dependency with historic supply-chain significance, so a malicious release can affect both direct and transitive consumers.
- The 2026 payload did **not** rely on npm lifecycle hooks; it executed when CommonJS consumers loaded `require("node-ipc")`, which bypasses defenses focused only on install scripts.
- The suspected maintainer-account path illustrates a durable package-registry risk: dormant accounts and expired maintainer email domains can become publish-right recovery channels.

## Reported chain
1. On May 14, 2026, `node-ipc@9.1.6`, `node-ipc@9.2.3`, and `node-ipc@12.0.1` were published to npm.
2. The publishes were attributed in public reporting to the dormant npm maintainer account `atiertant`, which had publish rights but no recent normal publishing history for the package.
3. Public analysis from Socket and Snyk reported malicious code appended to the CommonJS entrypoint `node-ipc.cjs`; the ESM path was not modified in the same way.
4. When `require("node-ipc")` loaded the CommonJS bundle, the payload forked a detached child process using an internal `__ntw=1` execution path and attempted credential and host-data collection.
5. Socket reported host fingerprinting, environment-variable capture, local file collection, archive/chunking behavior, cryptographic wrapping, and network exfiltration selected through DNS/address logic.

## Tradecraft notes
- The malicious CommonJS bundle exposed a `__ntRun` runner path, creating a secondary activation route if downstream code or tests called the exported property.
- Socket reported a forensic tarball indicator where files in the reviewed malicious artifacts carried an `Oct 26 1985` timestamp.
- Snyk reported the likely initial access path as maintainer-account abuse, with public reporting suggesting that an expired maintainer email domain may have enabled npm account recovery. Treat this as an account-governance lesson even if later root-cause details change.
- This incident appears separate from the 2022 `node-ipc` / `peacenotwar` protestware event; the 2026 payload is reported as credential theft and stealthy exfiltration rather than protestware behavior.

## Defender heuristics
- Search lockfiles, package-manager caches, SBOMs, artifact repositories, CI logs, and registry mirrors for `node-ipc` versions `9.1.6`, `9.2.3`, and `12.0.1`.
- Treat any environment that loaded the affected CommonJS package as potentially exposed, including developer machines, CI runners, build containers, and test jobs.
- Hunt for unexpected detached Node child processes, `__ntw=1` environment markers, `__ntRun` references, broad environment-variable collection, archive/chunking behavior, and outbound exfiltration soon after `node-ipc` was loaded.
- Rotate credentials available to exposed processes: GitHub/npm tokens, CI secrets, cloud credentials, Kubernetes/Vault tokens, SSH keys, and application secrets in environment variables.
- Audit package publisher accounts for dormant maintainers, expired email domains, missing MFA, account-recovery exposure, and legacy publish rights that no longer match active stewardship.
- Prefer runtime dependency execution controls and dependency allow/cooldown policies in addition to install-script blocking; this payload activates at module load, not just at install time.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Socket: https://socket.dev/blog/node-ipc-package-compromised
- Snyk: https://snyk.io/blog/malicious-node-ipc-versions-published-npm/
- Snyk advisory: https://security.snyk.io/vuln/SNYK-JS-NODEIPC-16697063
