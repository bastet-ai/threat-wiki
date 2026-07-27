# TELESHIM Middle East government espionage campaign

## Summary
In July 2026, Zscaler ThreatLabz observed an unattributed, East Asia-linked actor targeting government entities in the Middle East with a multi-stage Windows intrusion chain. The operation used three previously undocumented components: the **TELESHIM** first-stage backdoor, the **MIXEDKEY** reflective loader, and the **BINDCLOAK** C2 implant.

The chain begins with an ISO image and DLL side-loading through a legitimate ASUSTek executable. TELESHIM establishes Telegram-based command and control, stages follow-on components, and persists through a scheduled task. MIXEDKEY then decrypts a victim-bound BINDCLOAK payload using the machine's volume serial number and reflectively loads it. ThreatLabz captured hands-on-keyboard reconnaissance and payload deployment between July 7 and July 9, 2026.

## Tags
- ops
- operations
- espionage
- TELESHIM
- MIXEDKEY
- BINDCLOAK
- East Asia
- East Asia-linked
- Middle East
- government targeting
- Windows malware
- DLL side-loading
- Telegram C2
- environmental keying
- reflective loading
- scheduled task
- anti-analysis
- control flow flattening
- mixed boolean arithmetic
- ISO image

## Why this matters
- The operation joins trusted-binary side-loading, Telegram C2, scheduled-task persistence, and victim-specific payload encryption into a layered chain that can evade controls focused on one stage.
- ThreatLabz observed post-compromise operator activity, not just malware in a repository or sandbox. The published file, task, path, process, and network artifacts therefore map to an intrusion sequence.
- BINDCLOAK's second encryption layer is bound to the target's volume serial number. A collected encrypted payload may not decrypt away from the original host, making disk and system metadata preservation important.
- Zscaler assessed an East Asian origin with moderate-to-high confidence from operator IP, locale, geolocation, and working hours, but did **not** attribute the campaign to a known group.

## Reported chain
1. A lure archive contains an ISO image with legitimate `RegSchdTask.exe` and malicious `AsTaskSched.dll`.
2. The ASUSTek executable side-loads `AsTaskSched.dll`, the 32-bit TELESHIM backdoor.
3. TELESHIM hooks a hardcoded host-executable offset, creates `C:\ProgramData\shimgen_Data\`, and copies the pair as `shimgen.exe` and `AsTaskSched.dll`.
4. A scheduled task named `shimgen` runs the staged executable every six minutes.
5. TELESHIM polls the Telegram Bot API, registers the host by MAC address, accepts target-addressed shell commands, returns encrypted output, and can download and execute additional files.
6. The operator enumerates the host and `C:\ProgramData` to choose plausible staging paths.
7. A legitimate GoPro binary, `MSVCP120.dll`, `MSVCR120.dll`, and malicious `pthreadVC2.dll` are staged together. Names can be adapted to the selected directory.
8. A scheduled task named `Feedback` launches the legitimate binary every ten minutes, causing it to side-load `pthreadVC2.dll`, which ThreatLabz named MIXEDKEY.
9. MIXEDKEY reads `C:\ProgramData\Crypto\DSS\C99F29AC08454855B3D538960BB2F34F.PCPKEY`, removes two XOR layers, and reflectively loads BINDCLOAK.
10. BINDCLOAK beacons to `cert.hypersnet[.]com`.

## TELESHIM behavior
- Uses control-flow flattening, mixed boolean arithmetic, opaque predicates, and encrypted strings.
- Checks the `----WebKitFormBoundary7MA4YWxkTrZu0g` mutex.
- Performs roughly 1 GB of temporary-file I/O through `%TEMP%\CVR9EEA.tmp` to delay or disrupt analysis.
- Checks the CPUID hypervisor bit and queries RAM speed with `wmic memorychip get speed`; it exits on virtualization-like results.
- Polls `api.telegram.org/bot[BOT_TOKEN]/getUpdates?offset=[N]` with an old Chrome-on-macOS user-agent.
- Executes commands with `cmd.exe /C` only when the decrypted command is addressed to the host's MAC address.
- Encrypts command output and splits output larger than 1,000 bytes into chunks.
- Retrieves Telegram-hosted documents by `file_id`, decrypts them with its rolling XOR scheme, and launches them through scheduled tasks.

## Observed operator activity
ThreatLabz reported that most captured activity occurred from July 7 through July 9, 2026. Commands were issued between 04:00 and 12:00 UTC, with the heaviest concentration between 07:00 and 11:00 UTC. Timing is supporting attribution context, not a reliable standalone detector.

Observed commands included:
- Host discovery: `net user`, `tasklist`, `hostname`.
- Network discovery: `ipconfig /all`, `ipconfig /displaydns`, `netstat -ano`.
- File discovery under user profiles, Desktop, Downloads, `C:\ProgramData`, `C:\ProgramData\Crypto\DSS`, and plausible vendor directories.
- Connectivity checks to `cert.hypersnet[.]com`, `ssl.blsouqs[.]com`, and `contacts.ftabnews[.]com`.
- Creation and verification of the `Feedback` scheduled task.

## Environmental keying
MIXEDKEY derives a 20-byte rolling key by repeating the host's four-byte volume serial number five times. It uses the first 311 bytes of the `.PCPKEY` file as another rolling XOR key, applies both decryption layers, restores a PE whose `MZ` signature was removed, and loads it from memory.

This binding is useful to the operator because the final implant detonates only on the intended host. For defenders, it means incident collection should preserve the original volume serial number and encrypted payload together.

## Defender actions
1. **Isolate confirmed hosts before cleanup.** Preserve memory, the ISO or archive, side-loaded file pairs, scheduled-task definitions and operational logs, Telegram traffic metadata, DNS/proxy logs, and volume metadata.
2. **Hunt both scheduled tasks.** Search for tasks named `shimgen` and `Feedback`, especially six- or ten-minute recurrence and execution from `C:\ProgramData` vendor-like paths.
3. **Detect trusted-binary side-loading.** Alert on `RegSchdTask.exe` loading `AsTaskSched.dll` and GoPro service binaries loading `pthreadVC2.dll` outside expected installation paths.
4. **Correlate Telegram with endpoint behavior.** A process under `C:\ProgramData\shimgen_Data\` contacting `api.telegram.org`, spawning `cmd.exe`, writing executables, or creating tasks is substantially stronger than Telegram access alone.
5. **Hunt staging artifacts.** Review `C:\ProgramData\shimgen_Data\`, `C:\ProgramData\Crypto\DSS\`, `.PCPKEY` files, `CVR9EEA.tmp`, `shimgen.exe`, `AsTaskSched.dll`, and `pthreadVC2.dll`.
6. **Treat IOC matches as compromise evidence.** Scope command execution, credential access, additional payloads, persistence, and lateral movement. Rebuild affected systems and rotate credentials used or stored there based on evidence.
7. **Preserve attribution discipline.** Do not map the activity to a named East Asian group from geography, locale, or working hours alone.

## Public indicators
### Network
- `cert.hypersnet[.]com` — BINDCLOAK C2.
- `ssl.blsouqs[.]com` — operator connectivity check.
- `contacts.ftabnews[.]com` — operator connectivity check.
- `api.telegram.org` — TELESHIM's legitimate-service C2 channel; require process and path context.

### Host artifacts
- `RegSchdTask.exe` + `AsTaskSched.dll`
- `C:\ProgramData\shimgen_Data\shimgen.exe`
- `C:\ProgramData\shimgen_Data\AsTaskSched.dll`
- `C:\ProgramData\Crypto\DSS\C99F29AC08454855B3D538960BB2F34F.PCPKEY`
- `GoProAlertService.exe` + `pthreadVC2.dll`
- `%TEMP%\CVR9EEA.tmp`
- Mutex `----WebKitFormBoundary7MA4YWxkTrZu0g`
- Scheduled tasks `shimgen` and `Feedback`

### SHA-256
| SHA-256 | Context |
| --- | --- |
| `789fd11285642861190dc074c1e9a5957073f1a2afebd5160f9cc907f7f320bd` | Petroleum/gas cooperation lure archive |
| `c84542ac30cbe9bb8bd648bad323c37801023bf9451c1c0990452466e084340f` | Petroleum/gas cooperation ISO image |
| `32529043d15e9111ba284f1d8a9e4b3f58e071c6b69c8f271d4d02feacd44e66` | Border-offices agreement lure archive |
| `db11ff3f37a8b2aa25c480871504b886a6364167ecb501eacf7345f6bbf9582b` | Border-offices agreement ISO image |
| `5c2fe953da53da66fbcbb3be0fd6b63907c10714c337f287b2fc258857bbff6d` | New TELESHIM `AsTaskSched.dll` |
| `cac1f37beaa814461f7709a073aeec468c74e5d70f7d693a9e367ece4a3a78be` | Older TELESHIM `AsTaskSched.dll` |
| `0637069c7052118fd5c0f1113541bdd35e5f71cd9689f2516045da152c6fa8d9` | Older TELESHIM `dlpprem64.dll` |
| `3b3eaea783fd6dab90f0408274bf8a9c49adbdc70c0efd70658d65b0e1684a3f` | MIXEDKEY `pthreadVC2.dll` |
| `3b0c658ebaa2bae80af97f390b9b2bb20a2f815eb584b2251255e84da4fa669d` | BINDCLOAK |

## Analytical caveats
- Zscaler did not publish victim names or a victim count; government targeting should not be expanded beyond the source's wording.
- Initial delivery before the ISO is not established in Part 1.
- The actor is not assigned to a known APT. The East Asia assessment is moderate-to-high confidence, not identity proof.
- BINDCLOAK behavior beyond its 64-bit C++ implant role and C2 destination remains limited pending Zscaler's planned Part 2.
- Compile timestamps from 2025 and 2026 support malware evolution but should not be treated as exact build chronology without corroboration.

## Related pages
- [TELESHIM](../tools/teleshim.md)
- [MIXEDKEY](../tools/mixedkey.md)
- [BINDCLOAK](../tools/bindcloak.md)
- [CL-STA-1062 Southeast Asia government and energy intrusions](cl-sta-1062-southeast-asia-tinyrct.md)

## Sources
- Zscaler ThreatLabz: [Targeted Attack on Government Entities in the Middle East — Part 1](https://www.zscaler.com/blogs/security-research/targeted-attack-government-entities-middle-east-part-1)
- The Hacker News: [TELESHIM Abuses Telegram for C2 in Attacks Against Middle East Governments](https://thehackernews.com/2026/07/teleshim-abuses-telegram-for-c2-in.html)
