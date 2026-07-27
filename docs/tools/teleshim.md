# TELESHIM

## Summary
**TELESHIM** is a 32-bit C++ Windows backdoor documented by Zscaler ThreatLabz in July 2026 during an East Asia-linked campaign against Middle Eastern government entities. It is side-loaded as `AsTaskSched.dll` by a legitimate ASUSTek `RegSchdTask.exe`, persists through a scheduled task, and uses the Telegram Bot API for command and control.

ThreatLabz identified three TELESHIM instances. Two were compiled in 2025; the July 2026 campaign variant added heavy obfuscation and encrypted strings.

## Tags
- tools
- malware
- backdoor
- TELESHIM
- Windows
- C++
- Telegram C2
- DLL side-loading
- scheduled task
- anti-analysis
- control flow flattening
- mixed boolean arithmetic
- opaque predicates
- WMI
- CPUID
- MAC address

## Execution and persistence
- `RegSchdTask.exe` side-loads malicious `AsTaskSched.dll`.
- TELESHIM installs a seven-byte hook at hardcoded host offset `0x1394` to redirect execution into the implant.
- It creates `C:\ProgramData\shimgen_Data\`, copying the host to `shimgen.exe` and retaining `AsTaskSched.dll` beside it.
- A scheduled task named `shimgen` runs the staged executable every six minutes.
- Mutex `----WebKitFormBoundary7MA4YWxkTrZu0g` prevents duplicate execution.

## Command and control
TELESHIM decrypts an embedded Telegram bot token and chat ID, obtains the host MAC address with `GetAdaptersInfo`, and polls `api.telegram.org/bot[BOT_TOKEN]/getUpdates?offset=[N]`.

It supports:
- Registration by returning the encrypted, encoded MAC address.
- MAC-addressed command execution through `cmd.exe /C`.
- Encrypted result exfiltration, chunked when output exceeds 1,000 bytes.
- Telegram document download by `file_id`, payload decryption, and scheduled-task execution.

## Anti-analysis
- Writes and reads approximately 1 MB of random data 1,000 times through `%TEMP%\CVR9EEA.tmp`, producing roughly 1 GB of I/O.
- Checks CPUID ECX bit 31 for a hypervisor.
- Executes `wmic memorychip get speed` and exits on zero or unparseable virtualized results.
- Uses control-flow flattening, mixed boolean arithmetic, opaque predicates, Base64, and rolling XOR string/network encryption.

## Defender heuristics
- Correlate `RegSchdTask.exe` loading `AsTaskSched.dll` with creation of `C:\ProgramData\shimgen_Data` and the `shimgen` task.
- Alert when `shimgen.exe` contacts `api.telegram.org`, writes executable content, creates tasks, or launches `cmd.exe`.
- Hunt for the mutex and unusually high I/O to `CVR9EEA.tmp` immediately before network activity.
- Telegram access alone is not malicious; process ancestry, path, task, and side-loading context are essential.

## Public SHA-256 indicators
- `5c2fe953da53da66fbcbb3be0fd6b63907c10714c337f287b2fc258857bbff6d` — July 2026 `AsTaskSched.dll`.
- `cac1f37beaa814461f7709a073aeec468c74e5d70f7d693a9e367ece4a3a78be` — older `AsTaskSched.dll`.
- `0637069c7052118fd5c0f1113541bdd35e5f71cd9689f2516045da152c6fa8d9` — older `dlpprem64.dll`.

## Related pages
- [TELESHIM Middle East government espionage campaign](../ops/teleshim-middle-east-government-espionage.md)
- [MIXEDKEY](mixedkey.md)
- [BINDCLOAK](bindcloak.md)

## Sources
- Zscaler ThreatLabz: [Targeted Attack on Government Entities in the Middle East — Part 1](https://www.zscaler.com/blogs/security-research/targeted-attack-government-entities-middle-east-part-1)
