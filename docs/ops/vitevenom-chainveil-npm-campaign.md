# ViteVenom / ChainVeil npm campaign

## Summary
Checkmarx Zero reported **ViteVenom**, a cluster of seven malicious scoped npm packages impersonating Vite ecosystem tooling. The nine malicious versions were published from approximately June 29 through July 3, 2026 and accumulated 2,420 downloads before removal.

ViteVenom is linked with high confidence to the previously reported **ChainVeil** campaign and actor label **SuccessKey** through shared Tier-2 blockchain wallets, XOR keys, loader structure, and the same final 77 KB remote-access trojan. Checkmarx notes that a shared malware-as-a-service backend cannot be ruled out, so the operator relationship should not be treated as identity-level attribution.

## Tags
- ops
- operations
- ViteVenom
- ChainVeil
- SuccessKey
- npm
- npm supply-chain
- malicious packages
- scoped package impersonation
- Vite
- Vitest
- import-time execution
- blockchain C2
- Tron
- Aptos
- Binance Smart Chain
- remote access trojan
- developer targeting
- credential theft
- Checkmarx

## Affected packages
| Package | Malicious version(s) |
| --- | --- |
| `@uw010010/vite-tree` | `3.4.2`, `3.4.3`, `3.6.1` |
| `@vite-tab/tab` | `3.15.10` |
| `@vite-ln/build-ts` | `5.15.10` |
| `@vite-mcp/vite-type` | `6.44.1` |
| `@vite-pro/vite-ui` | `2.5.10` |
| `@vitets/vite-ts` | `1.5.10` |
| `@vite-ts/vite-ui` | `6.44.1` |

The fake scopes imitate the legitimate `@vitejs/*` namespace and, in the case of `@vitets`, differ by one character from the legitimate `@vitest` scope. `@uw010010/vite-tree` also published clean versions `3.4.1` and `8.1.0`; checking only the latest release can therefore miss exposure to an older malicious version.

## Execution and infrastructure
- All seven packages contain the malicious entry point `bin/vite.js`, with only the `global.i='*5-*'` campaign marker varying.
- Execution occurs when the package is imported, not through an install script. The loader hides sensitive strings behind array-index lookups and uses a 30-second anti-replay guard.
- The first path resolves an encrypted payload through Tron, falls back to Aptos, follows the resulting Binance Smart Chain transaction pointer, XOR-decrypts the transaction data, and evaluates it in the main Node.js process.
- A second path launches a detached, hidden `node -e` child and can retrieve the RAT directly from `198.105.127[.]210` at `/$/boot`.
- The shared Tier-2 wallets and cryptographic material match ChainVeil. The campaign-specific Tier-1 wallets and C2 assignment differ, consistent with compartmentalized delivery tracks.
- Checkmarx reports the packages were removed on July 3, but the blockchain pointers and backend infrastructure remained operational at publication time.

### Durable pivots
- ViteVenom C2: `198.105.127[.]210` on ports 80 and 443.
- Related ChainVeil infrastructure: `166.88.54[.]158:443` and `23.27.202[.]27:443/27017`.
- Tier-1 Tron wallets: `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` and `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH`.
- Shared Tier-2 Tron wallet: `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`.
- Shared Tier-2 Aptos account: `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1`.
- BSC transactions: `0x5ab85abe6c67adb94322e5700a36915c38d1db1e604920da8aa4fcb530408af0` and `0xbcc976e1c8f3dfd93e146ff424836a9635ab36d991a54675635d7fdf30e60616`.
- Loader strings: `api.trongrid.io`, `fullnode.mainnet.aptoslabs.com`, `bsc-dataseed.binance.org`, `eth_getTransactionByHash`, and the `?.?` BSC payload delimiter.

## Defender guidance
- Search SBOMs, lockfiles, package-manager caches, build artifacts, and developer workstations for the exact package/version pairs; do not rely on current npm state or the latest package version.
- Hunt `node_modules/**/bin/vite.js` for `global.i`, the blockchain API strings, shared wallet addresses, or the reported XOR-key material. Review detached `node -e` children and orphaned Node.js processes.
- Investigate network access to the reported C2 addresses and unusual developer-workstation calls to Tron, Aptos, or BSC RPC APIs immediately after Node.js package imports.
- Inspect `.bashrc`, `.zshrc`, and `.profile` for RAT persistence hidden after long whitespace padding, and search for unexpected `machineId` files in hidden directories.
- If execution is plausible, isolate affected developer and CI systems, preserve package and process evidence, then rotate npm, source-control, SSH, cloud, API, wallet, and CI credentials available to the process. Rebuild from known-clean dependencies and invalidate caches.
- Treat the shared blockchain and loader signatures as campaign-family detections: package names and first-tier wallets are disposable, while the backend has supported multiple delivery clusters.

## Related pages
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)
- [Astro config blockchain C2 PR injection](astro-config-blockchain-c2-pr-injection.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- Checkmarx Zero: <https://checkmarx.com/zero-post/sequel-to-chainveil-npm-malware-targets-vite-ecosystem/>
- Checkmarx Zero: <https://checkmarx.com/zero-post/chainveil-a-malicious-npm-supply-chain-attack-by-successkey/>
