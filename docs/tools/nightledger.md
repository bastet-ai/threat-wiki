# NightLedger

## Summary
**NightLedger** is a Windows HTTPS backdoor attributed by Kaspersky to **Mirage Kitten**. It masquerades as `SspiCli.dll` and is designed for DLL search-order hijacking through a co-located legitimate `AppVShNotify.exe`. Kaspersky linked it to the actor's historical **TWOSTROKE** implant through code and command-protocol similarities.

## Tags
- tool
- tools
- NightLedger
- Mirage Kitten
- UNC1549
- Windows
- backdoor
- DLL search-order hijacking
- HTTPS C2
- screenshot capture
- process discovery
- file operations
- NetSetup.log
- espionage

## Execution and persistence characteristics
- The malicious `SspiCli.dll` forwards expected exports to the legitimate DLL.
- `AppVShNotify.exe` does not directly import `SspiCli.dll`; its imported `RPCRT4.dll` can delay-load the DLL when an RPC authentication API is invoked.
- The implant creates mutex `A8215357-F99A-44FE-BC65-D8F0434B0C03` and exits if an instance already exists.

## Command and control
- Primary host: `realhealthshop[.]com`
- Fallback host: `tjconsultingservices[.]com`
- Poll path: `/edfcvfgbhnjmkqwasderfgg`
- Output path: `/wsdefvvbnhyuijkplmbgfrtt`
- File-upload path: `/qasxcdfvgbhnmyuioplkhnj`
- C2 task fields use the custom delimiter `#%%#`; Kaspersky compared this design with TWOSTROKE's `@##@` separator.

## Reported capabilities
- Gather user, host, network, drive, directory, and process information.
- Execute programs and load DLLs.
- Download, upload, copy, and delete files.
- Take screenshots, kill processes, adjust beacon timing, and terminate its thread.
- Collect `C:\Windows\debug\NetSetup.log` together with process output. This log can expose domain or workgroup join, unjoin, and network-setup history.

## Defender heuristics
- Alert on `AppVShNotify.exe` loading `SspiCli.dll` from a non-system or application-local directory, then making outbound HTTPS requests.
- Search for the mutex, three distinctive URL paths, and the `#%%#` task delimiter in memory, proxy captures, or recovered payloads.
- Investigate collection of `C:\Windows\debug\NetSetup.log` by a non-administrative utility or an unsigned DLL-hosting chain.
- Preserve both the malicious and legitimate DLLs and record their load paths before remediation.

## Public indicator
- `A239E655709A2518DD0B7BDBED163679` — reported `sspicli.dll` file hash

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](../ops/mirage-kitten-nightledger-bridgehead-arcbridge.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
