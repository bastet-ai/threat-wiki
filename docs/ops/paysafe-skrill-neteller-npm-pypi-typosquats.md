# Paysafe / Skrill / Neteller npm and PyPI typosquat stealer campaign

## Summary
Socket reported a coordinated **July 7, 2026** npm and PyPI malware cluster targeting developers and CI systems that integrate with payment applications. The campaign published **17 malicious packages** that typosquatted Paysafe, Skrill, and Neteller SDK names, presented fake SDK facades, then harvested environment secrets and exfiltrated them to Ngrok-hosted infrastructure.

This is durable defender signal because it targets payment-SDK developers and CI runners, uses cross-ecosystem package publication, includes sandbox checks, and steals broadly named secrets rather than only the payment API key that attracted installation.

## Tags
- ops
- operations
- supply chain
- npm
- PyPI
- typosquatting
- payment SDK
- Paysafe
- Skrill
- Neteller
- credential theft
- environment variable theft
- CI secrets
- Ngrok C2
- anti-analysis
- sandbox evasion
- Socket

## Why this matters
- The lure is business-critical payment integration code, so a successful install can expose production payment keys, cloud credentials, source-control tokens, package-registry tokens, and CI secrets.
- Socket says all npm packages published four malicious versions (`1.0.0` through `1.0.3`), while the PyPI packages each had a malicious `1.0.0` release at publication time.
- The npm packages masqueraded as real SDKs and only exfiltrated after an API-key-backed method call, reducing noise during shallow install-only scans.
- The PyPI packages executed from `__init__.py` and were not gated on an API key, making import-time execution the main exposure path.
- The actor used multi-step C2 hostname decoding, per-package/version obfuscation keys, CPU/hostname/user sandbox checks, and Ngrok infrastructure, suggesting this is likely to recur with new brands.

## Affected package set

### npm
Socket listed these npm packages:

- `paysafe-checkout`
- `paysafe-vault`
- `neteller`
- `skrill-payments`
- `paysafe-js`
- `paysafe-api`
- `paysafe-node`
- `paysafe-cards`
- `paysafe-fraud`
- `paysafe-kyc`
- `skrill`
- `skrill-sdk`
- `paysafe-payments`

### PyPI
Socket listed these PyPI packages:

- `paysafe-kyc`
- `paysafe-payments`
- `paysafe-sdk`
- `paysafe-api`

## Reported behavior
- The npm `paysafe-node` sample exported a fake `PaysafeClient`, read `PAYSAFE_API_KEY` and `PAYSAFE_ENV`, exposed plausible `payments` and `customers` methods, and returned success without reaching the real Paysafe endpoints.
- Exfiltration was delayed and gated on an API key being present; when triggered, the malware sent host/user/current-working-directory details plus selected environment variables.
- The secret-selection regex matched environment variable names containing `KEY`, `SECRET`, `TOKEN`, `PASS`, `AUTH`, or `API`, which can sweep in `PAYSAFE_API_KEY`, `AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, `NPM_TOKEN`, and similarly named CI variables.
- Sandbox checks skipped exfiltration on hosts with fewer than two CPU cores or host/user strings containing `sandbox`, `analyzer`, `cuckoo`, `virus`, `malware`, `vmware`, or `vbox`.
- Socket decoded the C2 hostname to `caliber-spinner-finishing[.]ngrok-free.dev`.

## Defender heuristics
1. Search dependency manifests, lockfiles, package-manager audit logs, artifact caches, and CI workspaces for the npm and PyPI package names above.
2. Treat any execution/import as a credential incident, not just a malicious-package cleanup. Rotate payment API keys, cloud credentials, GitHub/GitLab tokens, package-registry tokens, CI secrets, and any environment variable with names matching `KEY`, `SECRET`, `TOKEN`, `PASS`, `AUTH`, or `API`.
3. Hunt egress from developer endpoints and CI runners to `caliber-spinner-finishing[.]ngrok-free.dev`, `*.ngrok-free.dev`, and unusual HTTPS POST traffic from package install/test/build jobs.
4. Review CI logs for payment-SDK test runs that include `PAYSAFE_API_KEY` or package imports immediately after dependency changes.
5. Add registry-proxy or package-policy blocks for the package names and require manual review for new payment-SDK dependencies whose names differ slightly from official vendor packages.
6. For PyPI, scan for unexpected `__init__.py` network or environment-harvesting code in newly introduced internal payment integrations.

## Related pages
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [oob.moika.tech dependency-confusion environment stealer](oob-moika-dependency-confusion-env-stealer.md)
- [Sicoob.Sdk NuGet banking certificate stealer](sicoob-sdk-nuget-banking-certificate-stealer.md)

## Sources
- Socket: <https://socket.dev/blog/npm-pypi-campaign-typosquats-popular-secure-payment-apps>
