# Aeternum

## Summary
**Aeternum** is a Windows botnet loader and command-and-control framework that stores mutable instructions in Polygon smart contracts. Unit 42 documented C++, PyInstaller/Python, and Python-source samples that query public JSON-RPC endpoints, call a shared `getDomain()` function, and use the returned value to retrieve commands, payload locations, or replacement infrastructure.

The analyzed activity combined blockchain dead-drop resolution with GitHub and Pastebin staging, Telegram collection, conventional HTTP exfiltration, XWorm remote access, XMRig mining, credential theft, and cryptocurrency-wallet targeting. Public RPC infrastructure makes the control path resilient, but Aeternum is not fully decentralized: it still exposes stable contract selectors, operator transactions, staging repositories, payload hashes, endpoint persistence, and off-chain destinations.

## Tags
- tools
- malware
- botnet
- loader
- Aeternum
- Windows
- C++
- Python
- PyInstaller
- Polygon
- blockchain C2
- smart contracts
- JSON-RPC
- dead-drop resolver
- Telegram
- GitHub
- Pastebin
- XWorm
- XMRig
- cryptocurrency mining
- credential theft
- cryptocurrency wallet theft
- Early Bird APC injection

## Why this matters
- The same four-byte Polygon selector, `0xb68d1809`, appeared across all three analyzed samples. Unit 42 treats it as a durable family fingerprint even when contract addresses and off-chain domains rotate.
- The operator can update a contract's stored destination through `updateDomain()` without rebuilding the malware. Monitoring contract state and setter transactions can reveal infrastructure rotation before static indicator lists catch up.
- Blockchain resolution is one layer in a hybrid chain. Samples also depended on GitHub, Telegram, Pastebin, DuckDNS, raw-IP HTTP infrastructure, and conventional Windows persistence, leaving multiple detection and disruption points.
- Unit 42 recorded more than 29,000 detections associated with the studied activity by June 4, 2026. This is a security-product event count, not a count of unique infections, devices, or victims.
- Unit 42 found iterative contract compiler and implementation changes consistent with continued development, but did not publicly attribute the operation to a named threat actor.

## Shared blockchain control plane
Aeternum samples issue read-only `eth_call` requests to public Polygon JSON-RPC endpoints. The request supplies a contract address in the `to` field and a function selector in `data`.

| Selector | Reported function | Defender value |
|---|---|---|
| `0xb68d1809` | `getDomain()` | Shared retrieval fingerprint across the three samples |
| `0xb249cd2d` | `updateDomain()` | Admin-only infrastructure rotation |
| `0xf851a440` | `admin()` | Contract administrator lookup |

Unit 42 identified `0xcaf2c54e400437da717cf215181b170f65187abf` as the primary operator address associated with the moniker **LenAI** and observed `updateDomain()` push `cdnjsdelivr[.]beer`. Treat the moniker as an infrastructure label, not a verified real-world identity.

The C++ loader's returned value used PBKDF2-HMAC-SHA256 and AES-GCM, but derived the salt and password from the same publicly recoverable contract address. Unit 42 could therefore decrypt a returned command such as `all:url:<URI>`. Other samples returned plaintext or differently encrypted values. Detection should focus on the contract call and process ancestry rather than assuming one encoding.

## Sample 1: C++ loader and Telegram collection
Unit 42 analyzed UPX-packed 32-bit `Build.exe`, SHA-256 `5bfb25b8255b61e5ffdf6804451534bcfa9f1dfd225e6c8cdcefb5f50d846898`.

The loader:

1. copies itself beneath `%LocalAppData%`;
2. creates `Wmi_Framework_APIKEY_wmsnet_<random>.lnk` in the user's Startup folder;
3. runs supporting binaries named `wmiframework.exe`, `ZrvEsJQzWQ.exe`, and `STAAAAAS.exe`;
4. queries Polygon contracts through a rotating list of public RPC services;
5. downloads a clean `putty.exe` and malicious `DotNetZip.dll` from GitHub; and
6. executes the DLL, which inventories the host and sends a screenshot and system data through Telegram's bot API.

The malicious DLL has SHA-256 `1505eda3da68e2ff9919b55a31018bd30a991236f041aee835f3bc4e430ce505`. Unit 42 reported 22 contract addresses for this sample and repositories under `github[.]com/lencod/` and `github[.]com/Mash3Do/`; use the source IOC table for the complete time-bounded address list.

## Sample 2: XWorm, XMRig, and HTTP exfiltration
The 64-bit PyInstaller-packed sample `XBinderOutput_protected.exe`, SHA-256 `f2a326cff405299e4ebdfaac955c52fc7e496544eaa0921ecad4816cb3ae3a27`, recovered and ran a Python payload after virtual-machine and debugger checks.

Its Polygon response decoded to a Pastebin raw URL containing XMRig configuration. The configuration supported process suspension when diagnostic tools appeared and process termination targeting security and distributed-computing software. The same chain dropped:

- `XWormClient.exe` / XWorm v7.4, SHA-256 `4e24bbd0fabac6c3efcec943046afbfd332b2c0108a13becfda23a0e26f9ff5f`;
- `miner.exe` / XMRig, SHA-256 `81bb80d9c5a97dc41b65f6248c131963c91346eb4fb672836b3d53ae67564d9f`; and
- an exfiltration component that posted AES-128-ECB-encrypted data to `193.221.200[.]219` using user agent `cpp-httplib/0.18.3`.

Unit 42 linked the IP to `sekirolegion.duckdns[.]org/api/endpoint.php` and reported Polygon contract `0x75cD25791A60ab3451E2d2feB5ec46c6f541C2B8`. Some behavior overlapped a previously reported ZingoStealer pattern, but Unit 42 did not consider that sufficient attribution.

## Sample 3: DBeaver lure and wallet theft
A Python source sample, SHA-256 `ea1b6ff3a0c1a749b9f09d66789973321d63d8896b48f7345193bdad512950a2`, described a social-engineering chain impersonating a DBeaver installer.

It checked sandbox usernames and machine names, required at least 8 GB RAM, and looked for `Zone.Identifier` alternate data streams in the Downloads folder as evidence of a used workstation. It then created `PythonLauncher-*.lnk`, spawned signed `dpapimig.exe` suspended, and used Early Bird APC injection. Collection targeted more than 55 cryptocurrency browser extensions and 10 desktop wallets.

Reported pivots include:

- contract `0xb0874252a7359AA701F3F144A1f03A6e0DA8aE6D`;
- staging domain `download.sftp-api-group-wechat[.]com`;
- contract-resolved domains `update.constant-path[.]xyz`, `update-launcher[.]xyz`, and `test-steve[.]cyou`;
- disguised binary `WmiPrvSE.exe`; and
- Telegram-based reconnaissance followed by obfuscated JSON C2 traffic.

## Detection and response
- Alert on non-browser Windows processes issuing Polygon JSON-RPC `eth_call` requests containing selector `0xb68d1809`. Correlate with the contract address, subsequent GitHub/Pastebin/Telegram access, and child execution.
- Monitor the operator address and known contracts for `0xb249cd2d` setter transactions. Preserve transaction hash, block time, prior value, replacement value, and the endpoint process that queried it.
- Hunt Startup-folder shortcuts matching `Wmi_Framework_APIKEY_wmsnet_*.lnk` or `PythonLauncher-*.lnk`, especially with the supporting filenames documented above.
- Detect `dpapimig.exe` spawned suspended or receiving remote memory writes/APC activity from Python, PyInstaller, or an unsigned loader.
- Correlate access to GitHub-hosted `DotNetZip.dll`, Telegram `/sendDocument`, Pastebin raw content, or public Polygon RPC hosts with unknown local executables. These services are legitimate and should not be treated as malicious without process and contract context.
- Hunt the three primary sample hashes and the downloaded XWorm, XMRig, and DLL hashes across EDR, proxies, caches, and software inventories.
- If execution is confirmed, isolate the host, preserve memory and network state, collect Startup entries and injected-process evidence, revoke credentials and wallet secrets available to the user, and investigate mining, remote-access, and exfiltration activity separately.
- Do not block all Polygon, GitHub, Telegram, or Pastebin traffic solely from this report. Restrict unnecessary developer-host egress and use contract selectors, process lineage, file artifacts, and destination combinations for higher-confidence controls.

## Attribution limits
Unit 42's bytecode comparison suggests one threat group iteratively refined the smart-contract codebase, and its transaction analysis associates the primary administration address with the LenAI moniker. The publication does not identify a named actor, nationality, victim set, or initial-distribution campaign beyond the DBeaver lure represented in the source sample. Shared XWorm, XMRig, Telegram, GitHub, and public-RPC use are not sufficient attribution signals.

## Related pages
- [DeadLock ransomware](deadlock-ransomware.md)
- [ChainDrop keyv / cacheable npm worm](../ops/chaindrop-keyv-cacheable-npm-worm.md)
- [Dysphoria IoT botnet](../ops/dysphoria-iot-botnet.md)
- [Joyfill npm blockchain-RAT compromise](../ops/joyfill-npm-blockchain-rat-compromise.md)

## Sources
- Unit 42: [The Permanent Threat: Analyzing Aeternum's Blockchain-Based C2 Operations and Communications](https://unit42.paloaltonetworks.com/aeternum-blockchain-c2-analysis/)
