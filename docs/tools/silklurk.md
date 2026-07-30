# SilkLurk

## Summary
**SilkLurk** is a tailored modular Windows backdoor reported by Kaspersky GReAT in an unattributed Chinese-speaking espionage campaign. Its loaders sideload beside legitimate NVIDIA or Realtek binaries and bind decryption to a hash of the victim's computer name. The loader decrypts PE metadata, sections, relocations, and the entry point before reflectively injecting the backdoor. SilkLurk supports multiple C2 endpoints, optional HTTP proxies, configuration updates, and memory-only plugin injection.

## Tags
- tools
- malware
- backdoor
- SilkLurk
- Windows
- DLL sideloading
- reflective loading
- environmental keying
- computer name
- modular malware
- PlugX
- cyber-espionage

## Capabilities
- Collects computer/domain/user identity, architecture, OS/build, IP address, process ID, uptime, and module name.
- Supports four C2 hosts and ports plus two optional authenticated proxy configurations.
- Retrieves and updates configuration, changes reconnect delay, and receives and invokes memory-only plugins.
- Uses victim-specific decryption and multiple custom arithmetic/logic transforms for payload, PE metadata, configuration, key exchange, and network data.
- In observed post-compromise use, opened command shells, accessed network shares with administrative credentials, searched for confidential documents, staged archives, and delivered PlugX.

## Loading and persistence
Reported sideload pairs included legitimate `nvgwls.exe`, `NetSetSvc.exe`, `RtkSmbus.exe`, and `RtkNGUI64.exe` with malicious `vulkan-1.dll`, `nvml.dll`, `RtkSmbusLoc.dll`, or `RtkNGUI64Loc.dll`. One loader moved `OneDrive.dat` into a configured payload path and created the auto-start `RmSs` service with restart-on-failure behavior.

The computer-name hash is required across several decryption stages. Preserve the exact hostname and original artifacts during forensic collection.

## Public indicators
- C2 domains: `tyhbgtyuj.gleeze[.]com`, `wedfcvbn.gleeze[.]com`, `rgnojb.casacam[.]net`, `ctyuhjerf.kozow[.]com`, `uyhvfredc.accesscam[.]org`.
- Related PlugX C2: `gycudore.kozow[.]com` / `64.7.198[.]130`.
- C2 IPs: `95.179.210[.]138`, `45.77.136[.]228`, `95.179.141[.]26`, `45.32.152[.]50`, `212.11.39[.]138`, `195.86.120[.]2`, `154.196.187[.]73`, `45.61.149[.]112`.
- Representative loader MD5: `8269d6ba1b6842f9152c90cf7add9b93`.
- PlugX dropper/loader MD5s: `3c9a1ba8e0c7475706adc6376e9d7b7c`, `ef59aad625eebda8650aec5820d6ce69`.
- Representative paths: `C:\ProgramData\Microsoft\Network\Connections\nvgwls.exe`, adjacent `vulkan-1.dll`, `C:\ProgramData\Microsoft OneDrive\setup\OneDrive.dat`, and the `C:\ProgramData\Symantec\RasTls.exe` / `RasTls.dll` PlugX pair.

## Defender notes
- Alert when legitimate NVIDIA, Realtek, or Symantec executables load unsigned adjacent DLLs from ProgramData, user-public, Windows locale, VMware-lookalike, Veeam-lookalike, or other nonstandard directories.
- Hunt new auto-start services such as `RmSs`, especially when configured to restart vendor-lookalike processes after failure.
- Preserve memory, hostname, loader, encrypted payload, and configuration files together.
- Review command shells for `net use`, recursive document search, share disconnection, and WinRAR/7-Zip execution from unusual paths.
- Scope for OctLurk, LurkProxy, PlugX, Pandora RC, stolen administrative credentials, and archive exfiltration rather than removing one DLL in isolation.

## Related pages
- [OctLurk and SilkLurk Central Asia espionage campaign](../ops/octlurk-silklurk-central-asia-espionage.md)
- [OctLurk](octlurk.md)
- [LurkProxy](lurkproxy.md)

## Sources
- Kaspersky GReAT: [https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/](https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/)
