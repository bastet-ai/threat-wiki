# Void Dokkaebi

## Summary
Void Dokkaebi is a North Korea-aligned intrusion set that Trend Micro also maps to **Famous Chollima**. Public reporting describes the cluster targeting software developers, cryptocurrency users, and organizations where developer workstations have access to wallet material, signing keys, CI/CD systems, or production infrastructure.

Trend Micro's 2026 reporting adds a durable malware-evolution lesson: the group migrated **InvisibleFerret** from readable Python scripts into Cython-compiled Python extension modules (`.pyd` on Windows and `.so` on macOS). Defenders should therefore treat native Python extension modules and their small launcher scripts as part of the same detection surface as obvious Python malware.

## Tags
- groups
- North Korea
- developer targeting
- cryptocurrency theft
- supply-chain
- social engineering
- fake recruiting
- BeaverTail
- InvisibleFerret
- Cython
- Python extension modules
- browser credential theft
- wallet theft

## Why this matters
- The cluster targets developers through fake cryptocurrency / AI job-interview lures, making developer laptops and cloned interview repositories the entry surface.
- The target value is not only personal wallet theft: developer hosts can hold package-registry tokens, CI/CD credentials, signing keys, cloud credentials, and production access.
- Cython compilation can bypass rules that only search for readable Python scripts while leaving importable native modules that still execute Python payload logic.
- Browser-extension tampering and wallet trojanization can convert a developer endpoint into a cryptocurrency theft platform even after the initial lure is removed.

## Publicly reported tradecraft

### Initial access and delivery
- Trend Micro says Void Dokkaebi has historically posed as recruiters from cryptocurrency and AI firms and lured developers into cloning and executing repositories during fabricated job interviews.
- The 2026 InvisibleFerret chain still uses **BeaverTail** as a JavaScript-stage component, but BeaverTail now overlaps more with InvisibleFerret's own capabilities rather than acting only as a downloader / stealer.
- BeaverTail can download platform-specific InvisibleFerret components such as `mod.pyd` for Windows and `mod.so` for macOS.

### BeaverTail evolution
Trend Micro reports multiple BeaverTail variants with layered string protection and decoding logic. The reported capabilities include:

- browser credential and cryptocurrency-wallet data theft;
- downloader behavior for additional BeaverTail variants and InvisibleFerret;
- backdoor functions whose names begin with `ssh_`;
- system and network collection, including geolocation lookup through `ip-api[.]com/json`;
- developer-setting theft;
- trojanized Chrome / Brave wallet-extension installation for wallets such as MetaMask, Coinbase Wallet, and Phantom;
- Chrome downgrade behavior on macOS to keep Manifest V2 extension behavior available for wallet tampering.

### Cython-obfuscated InvisibleFerret
Trend Micro observed InvisibleFerret converted from plain Python into Cython-generated extension modules:

- Windows payloads use `.pyd` Python extension modules.
- macOS payloads use `.so` shared-library extension modules.
- The modules are not standalone executables; the chain writes a small Python launcher such as `.mod` to import the extension module and pass runtime arguments.
- Some modules can receive encoded C2 values from the launcher script, so the final C2 destination may not be recoverable from the binary alone.
- Trend Micro observed the `mc.so` module deleting its execution script and expects that behavior may expand to other modules.

The migration is defensive-relevant because the underlying deobfuscation stayed recognizable: Trend Micro reports that strings are Zlib-compressed in binary sections and that the embedded Python payload still uses a repeated reverse-Base64-decode-and-Zlib-decompress pattern before execution through Python runtime APIs.

### Capability map
Public reporting describes the combined BeaverTail / InvisibleFerret capability set as including:

- backdoor access and command execution;
- browser credential and credit-card theft;
- clipboard monitoring;
- keylogging on Windows;
- cryptocurrency wallet data, seed phrase, private key, and password theft;
- service key and developer setting collection;
- trojanized wallet-browser-extension installation;
- AnyDesk execution-environment staging, though Trend Micro observed some Cython-transition code paths as incomplete.

## Defender heuristics

### Hunt beyond script files
- Search for unexpected Python extension modules (`*.pyd`, `*.so`) dropped with small Python launchers such as `.mod` in recently cloned or interview-related repositories.
- Treat a Python launcher that imports a local native module and passes encoded IP / port arguments as suspicious even if the native module has no obvious standalone execution path.
- Preserve both the native module and its launcher script during response; Trend Micro notes that C2 values may be supplied at runtime by the launcher.
- Inspect Cython artifacts for `PyInit_` exports, `PyRun_StringFlags`, compressed string tables, retained build paths, and CPython-version-specific build strings.

### Developer endpoint triage
- Prioritize developers who ran code from recruiter-supplied cryptocurrency, AI, Web3, or interview repositories.
- Review browser extension directories for unexpected MetaMask, Coinbase Wallet, Phantom, Chrome, or Brave modifications.
- On macOS, investigate Chrome downgrade artifacts and wallet-extension changes that could preserve Manifest V2 behavior.
- Scope wallet, SSH, Git, package-registry, cloud, CI/CD, signing, and password-store credentials present on exposed developer hosts.

### Containment and recovery
- Isolate affected hosts before rotating credentials when active malware may still be running.
- Rotate wallet and developer credentials from a clean device; do not reuse browser profiles or extension state from the compromised host.
- Rebuild developer environments from trusted media if browser-extension tampering, Python extension-module execution, or keylogging is confirmed.
- Review CI/CD and package-registry audit logs for activity after the suspected developer-host exposure window.

## Related pages
- [Famous Chollima Packagist dev-branch loader](../ops/famous-chollima-packagist-dev-branch-loader.md)
- [UNK_DeadDrop developer repository phishing](../ops/unk-deaddrop-developer-repository-phishing.md)
- [JINX-0164 crypto developer infrastructure campaign](../ops/jinx-0164-crypto-developer-infrastructure-campaign.md)
- [Solana FakeFix npm / PyPI developer stealer](../ops/solana-fakefix-npm-pypi-developer-stealer.md)

## Sources
- [Trend Micro](https://www.trendmicro.com/en_us/research/26/e/analyzing-void-dokkaebi-invisibleferret-malware.html)
