# ChocoPoC fake PoC supply-chain campaign

## Summary
YesWeHack and Sekoia reported **ChocoPoC** on July 1, 2026 as an undocumented supply-chain campaign targeting vulnerability researchers, pentesters, and scanner authors through fake GitHub proof-of-concept repositories for high-profile CVEs. The campaign had been used in malicious PoCs since late 2025, and the researchers warned that malware and C2 infrastructure were still active at publication time.

The durable defender lesson is that the dangerous boundary is often the PoC's dependency graph, not the visible exploit script. In this campaign, fake CVE PoC repositories pulled a malicious PyPI dependency chain: `frint` depended on `skytext`, `skytext` shipped native extensions (`gradient.so` / `gradient.pyd`), and the native loader only activated when the expected PoC module context was present. The chain then installed Python startup persistence and used Mapbox datasets as dead-drop resolvers for a Python RAT.

## Tags
- ops
- operation
- supply chain
- developer targeting
- vulnerability research
- pentesting
- fake PoC
- GitHub
- PyPI
- Python
- native extension
- RAT
- credential theft
- persistence
- Mapbox
- ChocoPoC
- Sekoia
- YesWeHack

## Why this matters
- PoC urgency is part of the lure: defenders and researchers race to validate newly disclosed vulnerabilities, creating pressure to clone repositories and install requirements quickly.
- A quick review of the top-level PoC can miss the malicious payload because execution is hidden in a transitive package dependency and native extension.
- The malware uses runtime-context gating, so detonation of `skytext` in isolation can produce a false negative.
- Persistence through Python `.pth` files and `_distutils_hack` tampering makes this a developer-environment incident, not a one-time failed package install.

## Reported chain
1. A GitHub user suggested PoC repositories for critical CVEs to researchers building detection templates.
2. The fake PoC repository's `requirements.txt` included the newly published PyPI package `frint`.
3. `frint` transitively installed `skytext`, which presented itself as a terminal-colors package.
4. `skytext` shipped precompiled native wheels with `gradient.so` on Linux and `gradient.pyd` on Windows.
5. The native extension used obfuscation, compressed / XOR-encrypted payload blobs, hash-based module checks, PEB walking, and anti-debugging logic.
6. The loader checked the current Python module context and only proceeded when it saw PoC-like basenames such as `EXPLOIT_POC.py`, `exploit.py`, or `exploit_poc.py`.
7. After activation, it dropped a trojanized `_distutils_hack` package and `.pth` startup files, including `distutils-precedence.pth`, for interpreter-start persistence.
8. A `choco.py` downloader fetched subsequent code from Mapbox dataset URLs acting as dead-drop resolvers and executed it.
9. The final ChocoPoC RAT provided command execution, file and secret exfiltration, and credential theft capabilities.

## Lure repositories and CVE themes
YesWeHack / Sekoia listed at least seven lure repositories, many now deleted, including:

- `github.com/lincemorado97/CVE-2025-64446_CVE-2025-58034`
- `github.com/lincemorado97/CVE-2025-55182_CVE-2025-66478`
- `github.com/lincemorado97/CVE-2025-14847`
- `github.com/ogenich/CVE-2026-10520`
- `github.com/ogenich/CVE-2026-48908`
- `github.com/bolubey/CVE-2026-0257`
- `github.com/bolubey/CVE-2026-5075`

The CVE themes included high-interest vulnerability classes such as Joomla JCE, Ivanti Sentry, PAN-OS GlobalProtect, React2Shell, and Fortinet / FortiWeb-related lures.

## Public indicators and pivots
Treat these as public reporting pivots, not a complete detection set.

### Packages and files
- PyPI packages: `frint`, `skytext`.
- Native extensions: `gradient.so`, `gradient.pyd`.
- Python persistence artifacts: `distutils-precedence.pth`, `_distutils_hack/override.py`, `_distutils_hack/__init__.py`.
- Environment-variable pivots: `ZEBUWIAKGPHOQAP006=PTsjBGKQUxZorq2`, `JKHWQVEKRASDF12=JKHKJ23VAS8DF9`.

### Dead-drop and network pivots
- Mapbox accounts reported by YesWeHack / Sekoia: `frankley`, `mattallahsaed`, `james09790`.
- Mapbox dataset: `cmor0tcxf008i1mmpd7apt903`.
- Mapbox feature key: `dm370543acmdopk296nahbtua`.
- Stage-3 exfiltration endpoint: `91[.]132[.]163[.]78:8001`.

## Defender heuristics
- Run untrusted PoCs only inside disposable, network-restricted environments with no mounted home directory, browser profile, SSH key, package-registry token, cloud credential, source-control token, API key, or wallet material.
- Before installing PoC requirements, inspect package age, maintainer history, wheels vs source distributions, native extensions, `setup.py` / `pyproject.toml`, and transitive dependencies.
- Prefer static review and controlled reproduction over `pip install -r requirements.txt` on a trusted host.
- Hunt researcher workstations and CI/scanner hosts for unexpected `frint` or `skytext` installations, suspicious `.pth` files, modified `_distutils_hack` packages, and `gradient.so` / `gradient.pyd` artifacts.
- Review Python package caches and virtual environments for timestomped files, binary-only wheels, and package installs followed by network calls to Mapbox dataset APIs or `91[.]132[.]163[.]78:8001`.
- If exposure is confirmed, rebuild the environment and rotate credentials reachable from the host after endpoint containment.

## Related pages
- [ChocoPoC](../tools/chocopoc.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [UNK_DeadDrop developer repository phishing](unk-deaddrop-developer-repository-phishing.md)
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [Joomla JCE CVE-2026-48907 exploitation](joomla-jce-cve-2026-48907-exploitation.md)
- [Ivanti Sentry CVE-2026-10520 exploitation](ivanti-sentry-cve-2026-10520-exploitation.md)
- [PAN-OS GlobalProtect CVE-2026-0257 exploitation](pan-os-globalprotect-cve-2026-0257-exploitation.md)

## Sources
- YesWeHack / Sekoia: [https://www.yeswehack.com/news/chocopocs-vulnerability-researchers-trojanised-exploits](https://www.yeswehack.com/news/chocopocs-vulnerability-researchers-trojanised-exploits)
- The Hacker News: [https://thehackernews.com/2026/07/new-chocopoc-rat-targets-vulnerability.html](https://thehackernews.com/2026/07/new-chocopoc-rat-targets-vulnerability.html)
