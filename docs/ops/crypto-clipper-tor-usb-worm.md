# Crypto Clipper Tor / USB worm

## Summary
Microsoft Threat Intelligence reported a Windows cryptocurrency clipper campaign active since February 2026. The malware is delivered through malicious `.lnk` shortcuts, spreads through removable USB media, launches a bundled Tor client, monitors clipboard content for wallet material, substitutes cryptocurrency addresses, captures screenshots, and can execute attacker-supplied code returned by its hidden-service command-and-control server.

Treat this as more than a simple clipper. The campaign combines immediate wallet theft with persistence, anonymized C2, and a lightweight backdoor capability.

## Tags
- ops
- operations
- malware
- Windows
- cryptocurrency
- clipper
- stealer
- worm
- USB propagation
- LNK
- Tor
- hidden service
- clipboard theft
- screenshot theft
- remote code execution
- scheduled task
- WScript
- ActiveX

## Why this matters
- Clipboard clippers are often triaged as commodity theftware, but this campaign also keeps control of the endpoint through Tor-routed tasking and runtime code execution.
- The `.lnk` and USB propagation path makes removable-media controls and shortcut telemetry relevant even outside classic enterprise phishing flows.
- The local Tor SOCKS5 proxy means destination-based detection is weak; defenders need process, command-line, localhost proxy, and script-engine correlations.
- Wallet users and crypto operations should treat seed phrases, private keys, copied payment addresses, and screenshots from affected hosts as exposed.

## Reported chain
1. Initial execution begins from malicious `.lnk` shortcut files. Microsoft observed instances distributed on USB storage devices.
2. The shortcut stages a worm component that checks whether the host is already infected.
3. The worm creates additional malicious shortcuts for legitimate files found on the device, enabling propagation to newly inserted USB media.
4. The malware adds Defender exclusions for file-based payloads and creates scheduled tasks for both spreading and stealer execution.
5. The clipper / stealer runs as a script-based payload using Windows Script Host and `ActiveXObject`.
6. An anti-analysis check queries `Win32_Process` through WMI and exits if Task Manager is detected.
7. The malware launches a renamed portable Tor binary, `ugate.exe`, waits roughly 60 seconds for bootstrap, and uses the local SOCKS5 listener on `127.0.0.1:9050` to reach `.onion` C2 infrastructure.
8. After registration with a victim GUID, it polls for tasking and monitors the clipboard roughly every 500 milliseconds.
9. If the C2 returns an `EVAL` response, the malware executes attacker-supplied code at runtime.

## Theft and tasking behavior
Microsoft reports the clipper can:

- Detect 12- or 24-word BIP39 seed phrases in clipboard content.
- Capture Ethereum and Bitcoin WIF private keys.
- Save stolen wallet material locally as a backup, retry Tor exfiltration until acknowledged, then remove the local backup after successful transmission.
- Replace copied cryptocurrency wallet addresses with attacker-controlled alternatives, including BTC, Ethereum, and Tron address formats.
- Take five screenshots at ten-second intervals and upload them through Tor to give the operator context.
- Poll C2 for additional runtime instructions and execute attacker-supplied script code.

## Defender heuristics
### Endpoint hunting
- Investigate `wscript.exe`, `cscript.exe`, or related script engines launching `cmd.exe`, `powershell.exe`, `curl`, or unexpected executables.
- Hunt for scheduled tasks that launch JavaScript or script payloads wrapped in XML.
- Search for command lines or network telemetry showing local Tor SOCKS proxy use on `127.0.0.1:9050` / `localhost:9050`.
- Correlate Tor proxy activity with script-engine parents, PowerShell screenshot behavior, or clipboard-access patterns.
- Review WMI queries against `Win32_Process` from suspicious scripts, especially when paired with Task Manager checks.
- Look for renamed portable Tor binaries such as `ugate.exe` in unusual user-writable or removable-media paths.

### Removable-media controls
- Disable AutoRun / AutoPlay for removable media.
- Alert on `.lnk` creation bursts on USB volumes or shortcuts that masquerade as legitimate files.
- Inspect removable media from affected hosts for hidden or newly created shortcuts before reuse.

### Wallet and finance response
- Assume clipboard-copied wallet addresses from affected hosts may have been swapped.
- Rotate wallet seed phrases and private keys only from a known-clean device.
- Review recent transactions for address-substitution theft.
- Treat screenshots from affected systems as potentially exposed if they displayed wallet, exchange, custody, or recovery material.

## Microsoft-reported indicators
### Filenames and network pivots
- `ugate.exe` — renamed portable Tor binary.
- Local Tor SOCKS5 proxy: `127.0.0.1:9050` / `localhost:9050`.
- Hidden-service C2 domains reported by Microsoft:
  - `cgky6bn6ux5wvlybtmm3z255igt52ljml2ngnc5qp3cnw5jlglamisad[.]onion`
  - `gfoqsewps57xcyxoedle2gd53o6jne6y5nq5eh25muksqwzutzq7b3ad[.]onion`
  - `he5vnov645txpcv57el2theky2elesn24ebvgwfoewlpftksxp4fnxad[.]onion`
  - `lyhizqy2js2eh6ufngkbzntouiikdek5zsdj3qwa22b4z6knpqorgiad[.]onion`
  - `j3bv7g27oramhbxxuv6gl3dcyfmf44qnvju3offdyrap7hurfprq74qd[.]onion`
  - `shinypogk4jjniry5qi7247tznop6mxdrdte2k6pdu5cyo43vdzmrwid[.]onion`
  - `7goms4byw26kkbaanz5a5u5234gusot7rp5imzc3ozh66wwcvmcudjid[.]onion`
  - `facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd[.]onion`
  - `wt26llpl5k6gok3vnaxmucwgzv2wk3l7nuibbh25clghrtus3p5ctsid[.]onion`
  - `ijzn3sicrcy7guixkzjkib4ukbiilwc3xhnmby4mcbccnsd7j2rekvqd[.]onion`

### SHA-256 values
Microsoft lists the following SHA-256 indicators for the Crypto Clipper Worm:

- `7630debd35cac6b7d58c4427695579b3e3a8b1cc462f523234cd6c698882a68c`
- `a7abf1d9d6686af1cefcd60b17a312e7eb8cfe267def1ec34aeab6128c811630`
- `23c1e673f315dafa14b73034a90dd3d393a984451ff6601b8be8142be6487b43`
- `cf9fc891ea5ca5ecd8113ef3e69f6f52ff538b6cccbdaa9559106fc72bc6da30`
- `100407796028bf3649752d9d2a67a0e4394d752eb8de86daa42920e814f3fae8`
- `d14b80cbd1a19d4ad0473a0661297f8fdf598e81ff6c4ab24e212dcad2e54b3f`
- `9d90f54ae36c6c5435d5b8bed40faf54cc91f6db28574a6310b5ffaeb0362e96`
- `67fc5cf395e28294bbb91ed0e954fdf2e80ebd9119022a115a42c286dc8bacf5`
- `0020d23b0f9c5e6851a7f737af73fd143175ee47054931166369edd93338538a`
- `35a6bc44b176a050fd6824904b7604f0f45b0fdfa26bf9500b9e05973b387cfd`
- `c824630154ac4fdfce94ded01f037c305eab51e9bef3f493c60ff3184a640502`
- `d43bf94f0cb0ab97c88113b7e07d1a4024d1610617b5ad05882b1dbab89e15ba`
- `b2777b73a4c33ac6a409d475057843be6b5d32262ef28a1f1ff5bb52e3834c5f`
- `7787a9a7d8ae393aa32f257d083903c4dc9b97a1e5b0458c4cd480d4f3cb5b05`
- `f3b54984caca95fd496bcfe5d7db1611b08d2f5b7d250b43b430e5d76393f9e0`
- `20db98af3037b197c8a846dbf17b87fc6f049c3e0d9a188f9b9a74d3916dd5e1`

## Related pages
- [Pirated media SilentCryptoMiner RAT campaign](pirated-media-silentcryptominer-rat-campaign.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/06/17/crypto-clipper-uses-tor-worm-like-propagation-for-persistence-control/>
