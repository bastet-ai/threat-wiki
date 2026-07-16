# procwire / routecraft npm Windows dropper

## Summary
SafeDep reported a five-package npm campaign published on June 16, 2026 that split Windows dropper logic across plausible-looking micro-utilities. The armed packages were `procwire@1.3.0`, which runs a `preinstall` loader directly, and `routecraft@4.2.0`, an Express clone that pulls in `procwire` on Windows. Three companion packages, `bytecraft@1.5.0`, `endpointmap@2.1.0`, and `staticlayer@1.1.0`, supplied XOR helpers, encoded C2 data, and a self-hostable payload server.

Treat Windows hosts that installed `procwire` or `routecraft` on or after June 16, 2026 as compromised. The campaign executes before project code runs, downloads an executable from a public file host, strips Mark-of-the-Web prompts, and launches the payload hidden with multiple fallback methods.

## Tags
- ops
- operations
- supply-chain
- npm
- JavaScript
- Windows
- developer-targeting
- preinstall
- npm lifecycle hook
- dropper
- binary execution
- payload staging
- evasion
- package-splitting

## Why this matters
- The malicious behavior is split across packages, so reviewing each package in isolation can miss the chain.
- `routecraft` hides the risky dependency behind an Express-like package name and only requires `procwire` on Windows.
- The C2 URL is not stored as a string: `endpointmap` stores byte arrays, `bytecraft` performs XOR, and the key is derived from the `endpointmap` package name.
- The loader uses `preinstall`, so bare `npm install` is enough for execution before any application import.
- The dropper uses redundant download and execution paths, making simple hardening controls partial rather than complete protection.

## Reported chain
1. Between 14:44 and 14:56 UTC on June 16, 2026, one operator published five npm packages across two fabricated GitHub organizations, `akuznetsov-oss` and `vpetrov-oss`.
2. The packages used separate one-off maintainer accounts but shared the throwaway maintainer email domain `deltajohnsons[.]com`.
3. `procwire@1.3.0` declared a `preinstall` script, `node lib/setup.js`, and depended on `endpointmap` and `bytecraft`.
4. `routecraft@4.2.0` cloned Express and added Windows-only logic that requires `procwire` when Node.js is version 18 or newer.
5. `procwire` exits on non-Windows systems, then loads byte arrays from `endpointmap`, uses `bytecraft.xor`, derives the XOR key from the first eight bytes of the `endpointmap` package name, and reconstructs the payload URL.
6. The decoded payload location is `https://files[.]catbox[.]moe/j4loim[.]chk`.
7. `procwire` downloads a Windows executable, saves it under an updater-like name in a writable temp directory, writes a fake `Zone.Identifier` alternate data stream with `ZoneId=0`, and executes the payload hidden.
8. `staticlayer` is not victim-side malware by itself; SafeDep describes it as the operator's server-side kit for serving `/d/` payload paths only to clients using the expected User-Agent.

## Packages and infrastructure
| Package | Version | Role |
| --- | --- | --- |
| `procwire` | `1.3.0` | Armed Windows `preinstall` dropper. |
| `routecraft` | `4.2.0` | Express clone that reaches `procwire` on Windows. |
| `endpointmap` | `2.1.0` | Holds XOR-encoded C2 host and path arrays. |
| `bytecraft` | `1.5.0` | XOR helper used to decode the endpoint. |
| `staticlayer` | `1.1.0` | Server-side payload-serving kit exposed through npm publication. |

Reported pivots:

- Payload host: `files[.]catbox[.]moe`
- Payload path: `/j4loim.chk`
- Full staged URL: `hxxps://files[.]catbox[.]moe/j4loim[.]chk`
- Required / magic User-Agent: `Microsoft-Delivery-Optimization/10.0`
- Fake GitHub orgs: `github[.]com/akuznetsov-oss`, `github[.]com/vpetrov-oss`
- Maintainer email domain: `deltajohnsons[.]com`
- Claimed author personas: Anton Kuznetsov and Viktor Petrov, which SafeDep treats as fabricated personas rather than public identities.

## Malware behavior
### Execution trigger
- `procwire` runs `node lib/setup.js` from `preinstall`.
- `routecraft` uses Windows-gated loader code to require `procwire` only when `os.platform() === "win32"` and Node.js is at least version 18.
- `procwire` itself exits unless Node.js is at least version 16 and the platform is Windows.

### Endpoint reconstruction
- `endpointmap` stores `_ep` and `_p` byte arrays rather than a literal URL.
- `bytecraft` XORs those arrays with a key derived from `Buffer.from("endpointmap").slice(0, 8)`, yielding `endpoint`.
- The decoded host and path are `https://files.catbox.moe` and `/j4loim.chk`.

### Download and execution
SafeDep reports `procwire/lib/worker.js`:

- Builds sensitive strings with `String.fromCharCode` to reduce simple static detections.
- Uses a Microsoft-looking User-Agent, `Microsoft-Delivery-Optimization/10.0`.
- Disables TLS verification for the Node.js HTTPS request.
- Attempts download through three methods:
  - Node.js `https` with range/resume support and retries.
  - `curl.exe` with quiet download flags.
  - `bitsadmin` as a fallback.
- Saves into writable temp locations such as `%LOCALAPPDATA%\Temp`, `%TEMP%`, `%TMP%`, or `%USERPROFILE%\AppData\Local\Temp`.
- Randomizes filenames under updater-like prefixes:
  - `msedge_update_*.exe`
  - `chrome_installer_*.exe`
  - `dotnet_host_*.exe`
  - `onedrive_setup_*.exe`
  - `teams_update_*.exe`
- Writes `Zone.Identifier` with `ZoneId=0` to suppress Mark-of-the-Web / SmartScreen warning behavior.
- Attempts execution through direct detached spawn, `cmd.exe /c start "" /min`, and PowerShell `Start-Process -WindowStyle Hidden`.

### Server-side kit
- `staticlayer` serves from a `payloads/` directory only for `GET` requests under `/d/` with User-Agent `Microsoft-Delivery-Optimization/10.0`.
- Requests that do not match the expected method, path, and User-Agent have their socket destroyed.
- The server supports range responses and `application/octet-stream`, mirroring the client dropper's resumable download behavior.

## Defender heuristics
### Exposure triage
- Search package manifests, lockfiles, SBOMs, private registries, package-manager caches, CI logs, and developer endpoint telemetry for the five package names and versions above.
- Prioritize Windows developer machines and self-hosted Windows runners that ran `npm install` on or after June 16, 2026.
- Do not limit review to direct dependencies; `routecraft` can pull `procwire` one hop away.
- Treat any successful install of `procwire@1.3.0` or `routecraft@4.2.0` on Windows as host compromise pending forensic review.

### Endpoint and network hunting
- Hunt outbound requests to `files[.]catbox[.]moe` and path `/j4loim.chk`.
- Look for User-Agent `Microsoft-Delivery-Optimization/10.0` from developer workstations, build hosts, and CI runners where that traffic is not expected.
- Inspect `%LOCALAPPDATA%\Temp`, `%TEMP%`, `%TMP%`, and `%USERPROFILE%\AppData\Local\Temp` for recently created executables matching the updater-like prefixes listed above.
- Review process lineage for `node.exe` spawning `curl.exe`, `bitsadmin`, `cmd.exe`, `powershell.exe`, or updater-named executables during npm install windows.
- Inspect downloaded executables for suspicious `Zone.Identifier` alternate data streams set to `ZoneId=0` rather than ordinary internet-zone markings.
- Rotate credentials, npm tokens, GitHub tokens, cloud keys, and CI secrets accessible to affected Windows hosts after containment.

### Package-review lessons
- Flag lifecycle hooks in packages that do not need native builds or installation-time setup.
- Correlate package publication bursts by shared maintainer email domain, repository URL patterns, and helper-package dependency relationships, not just account names.
- Detect package sets whose logic only becomes malicious when multiple dependencies are composed.
- Run install-time behavior analysis in sandboxed Windows environments; Linux-only analysis would miss this campaign's active path.

## Related pages
- [Mastra `easy-day-js` npm scope compromise](mastra-easy-day-js-npm-scope-compromise.md)
- [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [AI scanner anti-analysis](../patterns/ai-scanner-anti-analysis.md)

## Sources
- SafeDep: [https://safedep.io/procwire-npm-windows-dropper-campaign](https://safedep.io/procwire-npm-windows-dropper-campaign)
