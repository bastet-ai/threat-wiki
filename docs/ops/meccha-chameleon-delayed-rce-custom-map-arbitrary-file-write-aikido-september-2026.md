# MECCHA CHAMELEON: second delayed RCE via custom map — arbitrary file write, HTA-in-WAV payload, Startup persistence (Aikido, Sep 3, 2026)

## Tags
- ops
- operations
- game exploitation
- Steam Workshop
- custom map
- remote code execution
- delayed execution
- path traversal
- arbitrary file write
- HTA
- mshta
- WAV
- PCM
- Startup folder persistence
- null byte truncation
- Unreal Engine
- Blueprints
- consumer software
- Aikido
- Robbe Van Roey
- MECCHA CHAMELEON

## Summary

On **September 3, 2026**, Aikido (Robbe Van Roey) published **"MECCHA CHAMELEON can't hide from the RCE"**, documenting a **second delayed remote-code-execution flaw** in the online hide-and-seek game **MECCHA CHAMELEON** (15M copies sold in its first month). When a victim joins a lobby on an attacker-selected map, the lobby host prompts every player to **download and execute a custom Steam Workshop map**. Because the game (Unreal Engine **5.6.1**) allows maps to embed **Blueprints** — its visual scripting that runs inside the game process with the player's account and permissions — a malicious map can call an exposed engine function, **`StopRecordingOutput`/`Finish Recording Output`**, to **write an arbitrary file to an arbitrary path**. Writing an executable to the **Windows Startup folder** yields **delayed RCE after the next reboot**. The game forces a `.wav` suffix on the filename, which the PoC defeats with a **null-byte path truncation** (`poc.exe\u0000IGNORED`) and carries the real payload as an **HTA embedded inside the 16-bit PCM sample data** of a WAV file. The flaw was **patched in MECCHA CHAMELEON 4.0.0 (Aug 20, 2026)**; no malicious Workshop maps were found in the wild. The game had already suffered a **first RCE on map load** (patched earlier), so this is a repeat class: the map-load attack surface is fundamentally dangerous for this game.

## Why this matters
- **Consumer game = mass attack surface.** A lobby host (any stranger) can get every player in a match to run attacker-supplied code in the game process, and the game's own "download this map" nudge lowers the friction.
- **Delayed RCE, not just map-load RCE.** The first map-load RCE was patched, but a *separate* exposed function still allowed arbitrary file write → persistence. Patching one sink does not remove the class.
- **Novel payload technique.** The `.wav` suffix can't be removed, so the PoC uses a **null-byte filename truncation** plus **HTA-in-WAV-PCM** steganography — a reusable trick for any "engine writes audio, Windows executes it" situation.
- **Persistence over remote trigger.** Execution happens at **next boot**, decoupling the delivery (playing one match) from the RCE (reboot), which evades "it only happens while the game runs" intuition.

## Technical detail
- **Engine / maps:** Built on **Unreal Engine 5.6.1**. Maps are not just assets — they can contain **Blueprints**, which execute in the game process using the player's account and permissions.
- **Trigger:** Lobby host selects the map; the UI urges all lobby members to download and run it. Custom maps are thus executed on every joiner.
- **Exposed function:** `StopRecordingOutput` / `Finish Recording Output` (a recording/ audio-export API). Supplying an **absolute or relative path** writes the recorded audio to that path. Default dir is `C:\Users\<user>\AppData\Local\Chameleon\Saved\BouncedWavFiles`, so a leading `../../../../` reaches the user's home folder without knowing the username.
- **Arbitrary file write → delayed RCE:** Writing an executable to `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` runs it at the next startup.
- **`.wav` suffix problem:** The engine appends `.wav` to the supplied filename, so a `poc.exe` lands as `poc.exe.wav` (treated as audio).
- **Null-byte truncation:** Some low-level Windows APIs treat a null byte (`\u0000`) in a filename as a terminator and discard the rest. Supplying `poc.exe\u0000IGNORED` produces a clean `poc.exe`. (This is the classic "two systems disagree on path rules" discrepancy.)
- **Payload-in-audio (HTA-in-WAV):** The file content is the engine's WAV header (uncontrollable) + the **PCM data section** (attacker-controlled). A normal `.exe`/`.dll` won't work because it needs a valid PE header at byte 0. Instead the PoC uses **Windows HTML Application (`.hta`)**: `mshta.exe` runs the file as a **desktop application** (not browser-sandboxed), whose embedded JScript can create a `WScript.Shell` COM object and launch arbitrary processes.
  - **Encoding trick:** 16-bit PCM stores each sample as a 2-byte **little-endian** value, so an ASCII byte pair becomes one sample. E.g. the bytes `3C 68 74 6D 6C 3E` (`<html>`) become samples `0x683C 0x6D74 0x3E6C`, which write back to the original bytes. The HTA payload (`<html><head><hta:application/><script>new ActiveXObject("WScript.Shell").Run("calc.exe");</script>...</head></html>`) is packed into the PCM section.
- **Map flow (BeginPlay):**
  1. `StartRecordingOutput` on a **private submix** (isolates the attacker's audio from normal game sound).
  2. `PlaySound2D` with the prepared **uncompressed PCM** WAV.
  3. `StopRecordingOutput` with filename `../../../../Roaming/Microsoft/Windows/Start Menu/Programs/Startup/poc.exe\u0000IGNORED`.

## Detection / defensive heuristics
- **Game-level:** treat all third-party / Workshop custom maps in MECCHA CHAMELEON as untrusted executable content; prefer official maps only.
- **Host level (Windows):** alert on **new files written into the Startup folder** (`AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`) by a **game / Unreal process**; `.hta` files being created or executed; `mshta.exe` spawning from an unusual parent; `WScript.Shell` object creation by non-Office processes.
- **Behavioral:** arbitrary file writes by the game process outside its own `AppData\Local\Chameleon\...` tree; a game process writing an audio file whose name contains a null byte or escapes the default directory.
- **Patch:** confirm the client is on **≥ 4.0.0** (the fix makes `StopRecordingOutput` stop creating files entirely).

## Assessment limits
- **No CVE published.** Aikido describes the flaw; the game vendor shipped a 4.0.0 patch (Aug 20, 2026) but the public post does not assign a CVE ID.
- **No in-the-wild exploitation of this specific sink.** Aikido scanned all Steam Workshop maps and found **none** exploiting it.
- **Possible additional unconfirmed vulnerabilities.** While building the PoC, "several individuals" reported *other* possible MECCHA CHAMELEON vulnerabilities that are **not proven or checked** by Aikido — the map-load attack surface should still be treated as risky.
- **Timing / restart requirement.** The RCE is **delayed** (next boot), which may reduce immediate impact but means an infected host stays dangerous until rebooted/re-imaged.

## Related pages
- [Microsoft Defender CVE-2026-50656 RoguePlanet / ShieldBreak patch bypass](microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md)
- [TerminalFix: ClickFix variant that delivers a reverse-tunnel implant (Microsoft, Aug 28)](terminalfix-clickfix-reverse-tunnel-multistage-microsoft-august-2026.md)

## Sources
- Aikido — "MECCHA CHAMELEON can't hide from the RCE" (Robbe Van Roey; published 2026-09-03, updated 2026-09-04): [https://www.aikido.dev/blog/meccha-chameleon-rce](https://www.aikido.dev/blog/meccha-chameleon-rce)
