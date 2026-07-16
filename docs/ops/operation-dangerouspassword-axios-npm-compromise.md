# Operation DangerousPassword axios npm compromise

## Summary
ESET's May 28, 2026 APT activity report says Lazarus continued **Operation DangerousPassword** during Q4 2025–Q1 2026 and that the activity led to compromise of the widely used `axios` JavaScript library.

According to ESET, attackers used compromised lead-maintainer credentials to publish malicious `axios` versions to npm. Socket's March 31, 2026 technical analysis identifies the poisoned npm releases as `axios@1.14.1` and `axios@0.30.4`, which pulled the malicious dependency `plain-crypto-js@4.2.1`. Because `axios` has more than 100 million weekly npm downloads and is embedded across web, mobile, and server-side JavaScript applications, the incident represents a high-blast-radius maintainer-account compromise with durable downstream cache and lockfile risk.

## Tags
- ops
- operations
- Lazarus
- North Korea
- Operation DangerousPassword
- npm
- axios
- JavaScript
- supply-chain
- maintainer compromise
- compromised credentials
- package registry
- developer-targeting
- CI/CD
- credential-theft
- RAT
- macOS
- Windows
- Linux
- postinstall
- npm lifecycle hook

## Why this matters
- A single maintainer credential compromise against a core JavaScript dependency can expose far more downstream organizations than direct intrusion against one target.
- The public reporting ties the compromise to Lazarus activity that also targets developers and cryptocurrency organizations, so defenders should treat package-registry credentials, developer workstations, and CI/CD secrets as likely objectives.
- Even after malicious releases are removed, lockfiles, private mirrors, build caches, container layers, vendored dependencies, and generated artifacts can preserve exposure.
- Socket observed related packages that captured the poisoned dependency transitively or through vendoring, showing how a short-lived compromise of one high-download package can spread into AI tooling and downstream package builds within hours.
- Hunt.io's payload analysis shows that the incident was not just dependency confusion or token theft: the `postinstall` path deployed OS-specific remote-access tooling and tried to erase package-level evidence after execution.
- The incident reinforces that high-download dependencies need publisher-account hardening, provenance checks, and rapid dependency-inventory response paths, not only source-code review.

## Reported chain
ESET's public summary gives the following high-level chain:

1. Lazarus activity under Operation DangerousPassword compromised credentials belonging to a lead maintainer of `axios`.
2. The attackers used the maintainer access to publish malicious `axios` versions to npm.
3. The malicious versions injected trojanized code into systems that installed or built with the affected releases.
4. The packages were later detected and removed.

Socket's technical writeup adds package and payload detail:

1. The suspicious releases were `axios@1.14.1` and `axios@0.30.4`, published directly to npm without matching normal GitHub release tags.
2. Both releases introduced `plain-crypto-js@4.2.1`, a malicious dependency published minutes before the Axios release and executed through an npm `postinstall` hook.
3. The dropper used reversed-Base64 plus XOR string obfuscation, contacted `sfrclak[.]com:8000`, and selected OS-specific payload paths for macOS, Windows, and Linux.
4. The malware deleted `setup.js`, replaced the malicious `package.json` with a clean `package.md` copy, and attempted to make the installed dependency appear benign after execution.
5. Socket also found the same malware in related downstream packages, including vendored or transitive exposure through `@shadanai/openclaw` and `@qqbrowser/openclaw-qbot`.

### Hunt.io payload analysis
Hunt.io later published a reverse-engineering writeup that expands the payload and infrastructure picture:

- The attacker reportedly staged `plain-crypto-js` as a clean `4.2.0` release, then weaponized `plain-crypto-js@4.2.1` roughly 18 hours later with the obfuscated `postinstall` dropper.
- The dropper hid strings with reversed Base64 plus XOR using the key `OrDeR_7077`, then selected a platform-specific payload path.
- Hunt.io described three payload families behind the same npm install path: a compiled C++ Mach-O RAT for macOS, a fileless PowerShell implant for Windows, and a Python standard-library-only backdoor for Linux.
- The C2 at `sfrclak[.]com:8000` / `142.11.206.73` routed payloads by POST body: `packages[.]npm[.]org/product0` for macOS, `product1` for Windows, and `product2` for Linux.
- Hunt.io identified shared RAT commands across platforms: `kill`, `peinject` for binary drop / injection, `runscript` for script execution, and `rundir` for directory browsing.
- Windows was the only variant Hunt.io observed with persistence, using a Registry Run key named `MicrosoftUpdate`; the macOS payload used ad-hoc code signing for Gatekeeper bypass, and the Linux `peinject` path appeared broken because of an undefined-variable bug.
- Hunt.io attributed the infrastructure to TA444 / BlueNoroff (DPRK) based on overlaps including a shared ETag with a known JustJoin server, the same Hostwinds AS54290 subnet, and NukeSped malware classification. Keep that as Hunt.io's infrastructure assessment alongside ESET's Lazarus / Operation DangerousPassword framing.

## Defender heuristics
- Inventory all `axios` versions installed from npm across source repositories, lockfiles, build systems, private registries, package caches, container images, and deployed artifacts around the Q4 2025–Q1 2026 window. Explicitly hunt for `axios@1.14.1`, `axios@0.30.4`, `plain-crypto-js@4.2.1`, and suspicious vendored copies of those packages.
- Prefer registry provenance, signed publish metadata, package-integrity hashes, and reproducible-build comparisons where available; do not rely only on current npm package state after removal.
- Review npm, GitHub, SSO, cloud, and CI/CD audit logs for unusual maintainer-token use, package-publish events, release automation changes, unexpected two-factor resets, and new automation tokens.
- Rebuild affected applications from known-good dependency sets after cache eviction; stale lockfiles or private mirrors can continue serving removed malicious versions.
- Rotate package-registry, GitHub, CI/CD, cloud, API, and signing credentials that were present on systems that built with suspect releases.
- Hunt endpoints for `sfrclak[.]com`, `142.11.206.73`, `http://sfrclak[.]com:8000/6202033`, POST bodies resembling `packages[.]npm[.]org/product0`, `product1`, or `product2`, and file artifacts such as `/Library/Caches/com.apple.act.mond`, `%PROGRAMDATA%\\wt.exe`, `%TEMP%\\6202033.vbs`, `%TEMP%\\6202033.ps1`, and `/tmp/ld.py`.
- Treat successful `postinstall` execution as remote-code-execution and RAT exposure, not only package tampering. Socket's macOS sample supported command execution, directory enumeration, payload injection, and beaconing with a fake Internet Explorer 8 user agent.
- On Windows developer workstations and self-hosted runners, inspect Run keys for unexpected `MicrosoftUpdate` values and review PowerShell execution policy bypass events around `axios` or `plain-crypto-js` installation windows.
- On macOS, treat ad-hoc signed binaries under cache locations as suspicious when paired with npm install activity; on Linux, inspect temporary Python payloads even if later command branches failed.
- Apply least-privilege and phishing-resistant MFA to maintainer and release accounts, and separate human maintainer credentials from automated package-publish tokens.

## Attribution notes
ESET reports the compromise in the context of Lazarus and Operation DangerousPassword. Socket states it had not observed evidence linking this Axios activity to TeamPCP campaigns at the time of publication. Track the incident as ESET-attributed North Korea-aligned supply-chain activity while keeping the package-level technical indicators separate from TeamPCP / Mini Shai-Hulud attribution unless stronger public evidence emerges.

## Related pages
- [RemotePE](../tools/remotepe.md)
- [3CX desktop app compromise](3cx-desktop-app-compromise.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- ESET: [https://www.welivesecurity.com/en/eset-research/eset-apt-activity-report-q4-2025-q1-2026/](https://www.welivesecurity.com/en/eset-research/eset-apt-activity-report-q4-2025-q1-2026/)
- ESET PDF: [https://web-assets.esetstatic.com/wls/en/papers/threat-reports/eset-apt-activity-report-q4-2025-q1-2026.pdf](https://web-assets.esetstatic.com/wls/en/papers/threat-reports/eset-apt-activity-report-q4-2025-q1-2026.pdf)
- Socket: [https://socket.dev/blog/axios-npm-package-compromised](https://socket.dev/blog/axios-npm-package-compromised)
- Hunt.io: [https://hunt.io/blog/axios-supply-chain-attack-ta444-bluenoroff](https://hunt.io/blog/axios-supply-chain-attack-ta444-bluenoroff)
