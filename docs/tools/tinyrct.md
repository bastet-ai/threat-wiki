# TinyRCT

## Summary
**TinyRCT** is a lightweight C# / .NET Windows backdoor publicly documented by Unit 42 in June 2026 during analysis of CL-STA-1062 activity against Southeast Asian government and critical-infrastructure targets.

Unit 42 found TinyRCT hosted as `PerfWatson2.exe` on `139.180.134[.]221`. The malware checks that it is running from `%LOCALAPPDATA%`, fingerprints the host, registers with an HTTP C2 channel, encrypts C2 traffic with hardcoded AES-128-CBC material, supports file and screen collection, and includes a self-destruct routine that removes its scheduled task and deletes the payload.

## Tags
- tools
- malware
- backdoor
- RAT
- TinyRCT
- CL-STA-1062
- UAT-7237
- .NET
- C#
- Windows
- AES-128-CBC
- HTTP C2
- screen capture
- file exfiltration
- self-delete
- scheduled task
- AppDomainManager injection
- PerfWatson2.exe

## Why this matters
- TinyRCT gives CL-STA-1062 a custom remote-management implant beyond the cluster's public use of web shells, SoftEther VPN, VNT, yuze, and commodity post-exploitation tools.
- The loader and payload both use location checks (`%USERPROFILE%\Downloads` for the loader and `%LOCALAPPDATA%` for the payload), creating concrete anti-analysis and detection pivots.
- The C2 design uses ordinary HTTP with encrypted payloads, so defenders need process, path, and destination context rather than relying only on protocol anomalies.
- The self-destruct path deletes the scheduled task and payload, making timely preservation of task history, process telemetry, and network logs important.

## Infection chain
1. Unit 42 reconstructed the chain from a malicious archive named `chrome_setup.zip`.
2. The archive contained a legitimate signed `chrome_setup.exe`, an adjacent `chrome_setup.exe.config`, and a malicious `MyAppDomainManager.dll`.
3. Running the executable caused the .NET runtime to read the adjacent configuration file and load the malicious DLL through AppDomainManager injection.
4. The loader checked that the host process ran from `%USERPROFILE%\Downloads`; if not, it terminated, likely to avoid sandboxes or analyst desktops.
5. If the check passed, the loader contacted `139.180.134[.]221` and saved the secondary payload under `%LOCALAPPDATA%` as `PerfWatson2.exe`, mimicking the Microsoft Visual Studio telemetry component name.
6. The loader created a logon scheduled task named `GoogleUpdaterTaskSystem140.0.7272.0 {ACE7A46F-50FD-481C-AB32-3D838871DB40}` with highest-privilege execution.

## Payload behavior
- Verifies execution from `%LOCALAPPDATA%`; exits when launched from another location.
- Collects username, machine name, OS version, local IP addresses, full execution path, process ID, and a randomly generated GUID bot identifier.
- Sends the host-registration packet to C2 by HTTP POST.
- Beacons by HTTP GET, with a default 10-second sleep interval.
- Uses AES-128-CBC for exchanged data; Unit 42 reported hardcoded key material `ThisIsASecretKey87654321` and a null IV.

## Supported commands reported by Unit 42
- Execute shell commands via `cmd.exe` or direct process execution and return stdout/stderr.
- Update the sleep interval.
- List files and directories, returning `Filename*Date*Size` style output.
- Read text files.
- Download a file from a URL to a requested path.
- Exfiltrate binary files by gzip-compressing, AES-encrypting, and sending them to C2 in 40 KB chunks.
- Capture the primary screen as JPEG, then compress, encrypt, and exfiltrate it.
- Self-destruct by deleting the `GoogleUpdater` scheduled task and using a delayed `choice.exe` batch technique to remove `PerfWatson2.exe`.

## Defender heuristics
- Alert on AppDomainManager injection from user download paths, especially legitimate `.exe` plus adjacent `.config` and unexpected `MyAppDomainManager.dll` patterns.
- Hunt for `PerfWatson2.exe` outside legitimate Visual Studio contexts, particularly under `%LOCALAPPDATA%`.
- Review scheduled tasks named like `GoogleUpdaterTaskSystem140.0.7272.0 {GUID}` or logon tasks that run `%LOCALAPPDATA%\PerfWatson2.exe` with highest privileges.
- Correlate `chrome_setup.zip`, `chrome_setup.exe.config`, `MyAppDomainManager.dll`, HTTP retrieval from `139.180.134[.]221`, and subsequent beaconing to `45.32.113[.]172`.
- Preserve scheduled-task operational logs and command-line telemetry quickly; the self-destruct routine explicitly removes persistence and payload artifacts.

## Public indicators highlighted by Unit 42
| Indicator | Type | Context |
| --- | --- | --- |
| `00e09754526d0fe836ba27e3144ae161b0ecd3774abec5560504a16a67f0087c` | SHA-256 | `chrome_setup.zip` |
| `cbfe8de6ffadbb1d396f61e63eb18e8b11c29527c1528641e3223d4c516cf7c3` | SHA-256 | TinyRCT downloader |
| `4e1f8888d020decd09799ec946f1bf677cac6612b24582ddbf4d8ede425d8384` | SHA-256 | TinyRCT |
| `139.180.134[.]221` | IP address | Payload / tool staging |
| `45.32.113[.]172` | IP address | TinyRCT C2 |
| `hxxp[:]//139.180.134[.]221/PerfWatson2.exe` | URL | TinyRCT staged payload |
| `ThisIsASecretKey87654321` | Cryptographic artifact | Hardcoded AES key material reported by Unit 42 |
| `GoogleUpdaterTaskSystem140.0.7272.0 {ACE7A46F-50FD-481C-AB32-3D838871DB40}` | Scheduled task | Loader-created persistence |

## Related pages
- [CL-STA-1062](../actors/cl-sta-1062.md)
- [CL-STA-1062 Southeast Asia government and energy intrusions](../ops/cl-sta-1062-southeast-asia-tinyrct.md)

## Sources
- Unit 42: https://unit42.paloaltonetworks.com/cl-sta-1062-tinyrct-backdoor/
