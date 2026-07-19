# HelloNet ViPNet update-system campaign

## Summary
Kaspersky reported **HelloNet**, an active targeted campaign observed since at least May 2026 against large Russian organizations in government, energy, transport, education, logistics, and industry. The attackers place a malicious `wtsapi32.dll` beside the ViPNet update component `itcsrvup64.exe`; the signed update executable then sideloads the DLL at system startup.

This is persistence through a vulnerable trusted-software loading path, not evidence that InfoTeCS distributed a malicious update. Kaspersky links the activity to an unknown Chinese-speaking APT with **low confidence** and explicitly notes that the limited language and build-environment artifacts could be false flags.

## Tags
- ops
- operations
- HelloNet
- HelloInjector
- HelloProxy
- HelloExecutor
- HelloCleaner
- HelloBackdoor
- ViPNet
- InfoTeCS
- supply-chain-adjacent
- DLL sideloading
- process injection
- proxy
- SSH tunneling
- Rust malware
- APT
- espionage
- Russia
- government
- energy sector
- transport
- education
- industrial targeting
- Chinese-speaking
- low-confidence attribution
- Kaspersky GReAT

## Intrusion chain
1. A malicious `wtsapi32.dll`, dubbed **HelloInjector**, is placed in `C:\Program Files (x86)\InfoTeCS\VIPNet Update System`.
2. ViPNet's startup-launched `itcsrvup64.exe` sideloads the DLL. HelloInjector locates an `svchost.exe` instance whose command line contains `netsvcs`, injects itself with `NtWriteVirtualMemory` and `NtCreateThreadEx`, and runs its embedded payload in memory.
3. **HelloProxy** hooks socket-related functions with Microsoft Detours, listens on ports 5003 and 5060, forwards traffic, and loads additional executable content into memory. It logs intercepted receive activity to `C:\Users\Public\tesh4RPC.txt`.
4. Follow-on modules include **HelloExecutor** for command execution and reconnaissance and **HelloCleaner** for removing ViPNet logs.
5. The actor used a renamed PuTTY/Plink binary such as `C:\Users\Public\Music\frontpage.exe` to establish reverse SSH tunnels to attacker infrastructure.
6. A separate Rust implant, **HelloBackdoor**, listens on TCP/443 and activates after receiving `47c6235b4d2611184`. It supports upload, download, command execution, and self-removal/service restart behavior.

HelloProxy's handshake sends bytes `05 02` and expects `ASDFASFSAFASDF`. These protocol constants are stronger durable detections than filenames alone.

## Detection pivots
- `wtsapi32.dll` created or loaded from a ViPNet Update System or ViPNet Client directory, especially without a valid InfoTeCS signature.
- `itcsrvup64.exe` or `itcsrvup.exe` injecting into `svchost.exe`, loading an unsigned sidecar DLL, or spawning a process outside the expected ViPNet process set.
- TCP listeners on 5003/5060 with the HelloProxy handshake, or a TCP/443 service waiting for `47c6235b4d2611184`.
- Renamed PuTTY/Plink executables identified by original PE metadata and launched with `-R`, `-P`, `-pw`, or compressed SSH tunneling options from public user directories.
- Reconnaissance such as `query user`, `ipconfig /all`, `net user`, and `net group` originating from an unusual `svchost.exe` instance.
- `C:\Users\Public\tesh4RPC.txt`, `C:\Users\Public\Music\frontpage.exe`, unexpected `puh.exe` or `store.exe` files under ViPNet paths, and suspicious service creation or Defender-exclusion activity.

Public infrastructure includes `5.39.253[.]206` and `176.32.34[.]135`. Kaspersky also published sample hashes and detection rules in the primary report.

## Defender guidance
- Prioritize ViPNet hosts for triage and compare every executable and DLL in InfoTeCS directories with vendor-signed, known-good baselines. Do not treat a clean update package alone as proof that the endpoint is clean.
- Alert on side-loading and process-injection behavior from the ViPNet update service, not only known hashes. Preserve the sidecar DLL, update executable, service state, memory, network connections, and ViPNet logs before remediation.
- Hunt all systems reachable through ViPNet networks for reverse tunnels, credential use, staged files, and lateral movement. Rotate exposed credentials only after containment and persistence removal.
- Restrict update-system hosts from unnecessary inbound listeners and outbound SSH. Monitor ports 443, 5003, and 5060 for the protocol markers above.
- Keep attribution confidence separate from detection: the `sina.com` string and Chinese Rust crate mirror are weak context, not identity proof.

## Related pages
- [Operation Highland Velvet Ant authentication-stack backdoors](operation-highland-velvet-ant-authentication-stack-backdoors.md)
- [ScarCruft Yanbian game-platform supply-chain attack](scarcruft-yanbian-game-platform-supply-chain.md)
- [DAEMON Tools Lite supply-chain compromise](daemon-tools-lite-supply-chain-compromise.md)

## Sources
- Kaspersky Securelist: <https://securelist.com/hellonet-vipnet/120700/>
