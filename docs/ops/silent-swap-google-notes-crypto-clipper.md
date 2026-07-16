# Silent Swap Google Notes crypto clipper

## Summary
McAfee Labs reported an active cryptocurrency-clipper campaign tracked as **Silent Swap** that deploys a malicious Chromium extension masquerading as a benign **Google Notes** utility. The campaign uses unsigned .NET and Golang installers to force-load the extension into Chromium-family browsers, then replaces copied cryptocurrency wallet addresses with attacker-controlled destinations.

The durable defender signal is the browser-extension installation path: rather than relying on a marketplace listing, the installer modifies Chromium profile preference files and recalculates the browser's integrity values so the extension appears legitimately installed. That makes ordinary extension inventory, browser-profile file monitoring, clipboard-risk controls, and wallet-transaction verification important even when the payload never arrives through the Chrome Web Store.

## Tags
- ops
- operations
- Silent Swap
- McAfee Labs
- crypto clipper
- cryptocurrency theft
- wallet address replacement
- browser extension
- Chromium extension
- Google Notes
- unsigned installer
- BaseZipInstaller
- Golang malware
- .NET malware
- EtherHiding
- blockchain dead drop
- clipboard theft
- Secure Preferences
- developer mode
- browser credential theft
- seed phrase theft

## Why this matters
- Clipboard clippers sit directly in the transaction path: a user can paste what looks like a normal wallet address while the extension silently substitutes the destination.
- McAfee says the extension can target patterns associated with Bitcoin, Ethereum, Bitcoin Cash, Ripple, Dash, and Solana; submitted Solana addresses resolved to a single attacker address with about $1,902 reported at publication.
- The same clipboard and page-access posture can expose more than wallet addresses. THN's summary of McAfee's report says the behavior can also siphon passwords, authentication codes, API keys, OAuth tokens, and seed phrases.
- The campaign uses **EtherHiding** as a C2/dead-drop resolver: blockchain smart-contract data can point the malware to current backend infrastructure without republishing the extension or installer.
- Forced extension installation through local profile tampering bypasses the normal extension-store review path and may not trigger controls that focus only on marketplace extension IDs.

## Reported chain
1. The victim runs an unsigned installer observed in .NET and Golang variants.
2. The .NET installer, named `BaseZipInstaller` in McAfee's reporting, retrieves a ZIP archive that contains the extension foundation.
3. The installer scans for Chromium-family browser profiles, including Google Chrome, Microsoft Edge, Brave, and Vivaldi.
4. For each detected profile, the installer terminates the browser process and modifies `Secure Preferences` and `Preferences` files to register the extension.
5. The malware recalculates the hash / HMAC-style verification values Chromium stores near sensitive settings, causing the browser to treat the malicious extension as legitimate.
6. In Brave and Opera paths, the malware also attempts to enable developer mode programmatically; newer browser versions may still require social engineering to complete that step.
7. The installer self-deletes after deployment, reducing the initial-access artifact available to responders.
8. Once loaded, the extension monitors clipboard content and replaces matching wallet addresses through server-side mapping.
9. If the backend request fails, the extension can fall back to a predefined hardcoded wallet address so clipping continues.

## Infrastructure and behavior notes
- Campaign name: `Silent Swap`
- Masqueraded extension: `Google Notes`
- Installer family name reported by McAfee: `BaseZipInstaller`
- Browser targets named in public reporting: Google Chrome, Microsoft Edge, Brave, Vivaldi, Opera
- Persistence path: extension registration by altering Chromium profile `Secure Preferences` / `Preferences`
- C2/dead-drop method: EtherHiding / blockchain smart-contract resolver
- Dynamic substitution: intercepted wallet address is sent to attacker backend; the backend returns a matching attacker-controlled address
- Fallback behavior: hardcoded wallet address substitution if backend lookup fails

## Defender heuristics
- Inventory Chromium-family extensions from disk, not only from extension-management consoles. Compare profile `Secure Preferences` / `Preferences` extension entries against approved extension baselines and browser-store installation records.
- Hunt for unsigned installers, recently deleted installer artifacts, or processes that terminate browsers and then write browser profile preference files.
- Monitor for unexpected developer-mode enablement, extension directories that do not map to known enterprise policy or marketplace installation, and new extensions branded as notes, wallet, productivity, VPN, AI assistant, or utility tooling.
- For finance, treasury, and cryptocurrency users, treat copied wallet addresses as sensitive. Require out-of-band address verification or hardware-wallet display verification before signing transactions.
- Scope impact beyond wallet theft: rotate passwords, API keys, OAuth tokens, seed phrases, and recovery material copied while the extension may have been active.
- Use proxy, DNS, and endpoint telemetry to detect blockchain resolver lookups or suspicious wallet-substitution API calls from browser-extension contexts.
- During response, preserve the browser profile before cleanup. The profile files may show when the extension was registered and whether settings integrity values were tampered with.

## Related pages
- [VPN Go browser-extension clipboard stealer](vpn-go-browser-extension-clipboard-stealer.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [Crypto Clipper Tor / USB worm](crypto-clipper-tor-usb-worm.md)
- [StegoAd Edge extension steganography campaign](stegoad-edge-extension-steganography-campaign.md)
- [Chrome live-wallpaper extension ad-fraud network](chrome-live-wallpaper-extension-ad-fraud.md)

## Sources
- [McAfee Labs](https://www.mcafee.com/blogs/other-blogs/mcafee-labs/crypto-clipper-wallet-swapping-browser-extension-malware/)
- [The Hacker News summary](https://thehackernews.com/2026/06/silent-swap-crypto-clipper-uses-fake.html)
