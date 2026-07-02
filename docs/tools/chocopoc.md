# ChocoPoC

## Summary
**ChocoPoC** is a Python remote-access trojan documented by YesWeHack and Sekoia on July 1, 2026 after a suspicious GitHub contribution request led researchers into a fake proof-of-concept exploit repository. The malware targets vulnerability researchers, pentesters, and scanner authors by hiding inside Python dependencies for alleged CVE PoCs.

The durable tradecraft is not just “malicious PoC code.” The visible repository can look plausible while the malicious behavior sits in a transitive PyPI dependency, executes through a native extension only in the expected PoC runtime context, persists through Python startup hooks, and resolves later payloads through a Mapbox dataset dead drop.

## Tags
- tool
- malware
- RAT
- Python
- PyPI
- native extension
- developer targeting
- vulnerability research
- fake PoC
- credential theft
- persistence
- dead drop resolver
- Mapbox
- supply chain

## Reported capabilities
- Executes commands and provides remote shell access.
- Exfiltrates files and secrets from researcher workstations.
- Harvests browser credentials and cookies, according to The Hacker News' summary of the YesWeHack / Sekoia findings.
- Uses a stage-3 exfiltration endpoint with chunked upload behavior.
- Uses Python persistence so later interpreter starts can continue execution.

## Loader and persistence details
- Fake PoC repositories listed `frint` as a dependency.
- `frint` pulled in the `skytext` PyPI package.
- `skytext` shipped precompiled native extensions named `gradient.so` on Linux and `gradient.pyd` on Windows.
- The native extension used obfuscation, hash-based module checks, PEB walking, compressed / XOR-encrypted blobs, and anti-debugging logic.
- Execution was gated on the PoC runtime context by hashing loaded module basenames and matching names such as `EXPLOIT_POC.py`, `exploit.py`, or `exploit_poc.py`. That gate explains why isolated sandbox detonation may see no malicious behavior.
- The loader dropped a trojanized `_distutils_hack` package and `.pth` startup hooks, including `distutils-precedence.pth`, so the next Python interpreter start could import and run `choco.py`.
- The next stage fetched code from Mapbox dataset URLs used as dead-drop resolvers, then executed the fetched code.

## Notable reported indicators
Treat these as historical public reporting pivots; confirm against the original YesWeHack / Sekoia article before operational blocking.

- PyPI packages: `frint`, `skytext`.
- Native extension filenames: `gradient.so`, `gradient.pyd`.
- Python startup artifacts: `distutils-precedence.pth`, `_distutils_hack/override.py`, `_distutils_hack/__init__.py`.
- Runtime / mutex-like environment variables: `ZEBUWIAKGPHOQAP006=PTsjBGKQUxZorq2`, `JKHWQVEKRASDF12=JKHKJ23VAS8DF9`.
- Mapbox account / dataset pivots reported by YesWeHack / Sekoia: `frankley`, `mattallahsaed`, `james09790`, dataset `cmor0tcxf008i1mmpd7apt903`, feature key `dm370543acmdopk296nahbtua`.
- Stage-3 endpoint reported by YesWeHack / Sekoia: `91[.]132[.]163[.]78:8001`.

## Defensive notes
- Do not run newly published PoCs or install their requirements on a normal workstation or trusted scanner host.
- Review dependency trees for newly registered or low-reputation packages pulled by PoC repositories, especially packages shipping binary wheels or native extensions.
- Hunt Python environments for unexpected `.pth` files, altered `_distutils_hack` packages, and package files that are timestomped or inconsistent with known-good package contents.
- Execute PoCs only in disposable, network-restricted sandboxes with no browser profiles, SSH keys, source-control tokens, registry tokens, cloud credentials, API keys, or wallet material.
- Treat a positive hit as developer-endpoint compromise: rebuild the environment and rotate secrets that were reachable from the host after containment.

## Related pages
- [ChocoPoC fake PoC supply-chain campaign](../ops/chocopoc-fake-poc-supply-chain-campaign.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Solana FakeFix npm / PyPI developer stealer](../ops/solana-fakefix-npm-pypi-developer-stealer.md)
- [UNK_DeadDrop developer repository phishing](../ops/unk-deaddrop-developer-repository-phishing.md)

## Sources
- YesWeHack / Sekoia: https://www.yeswehack.com/news/chocopocs-vulnerability-researchers-trojanised-exploits
- The Hacker News: https://thehackernews.com/2026/07/new-chocopoc-rat-targets-vulnerability.html
