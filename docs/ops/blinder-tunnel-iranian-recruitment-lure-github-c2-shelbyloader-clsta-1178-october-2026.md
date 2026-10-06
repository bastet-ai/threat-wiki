# Blinder Tunnel: Iranian CL-STA-1178 fake-Dubai-Airports recruitment lure, weaponized .csproj, and GitHub-API C2 with Issues dead-drop fallback (ShelbyLoader V2 / ShelbyC2 V2 / PsProxy / Blackwood) — Unit 42, October 6, 2026

**Actor:** CL-STA-1178 (Unit 42 tracking), assessed **high confidence Iranian state-aligned**; previously linked by Elastic Security Labs to "The Shelby Strategy" and TTP-overlapping with Screening Serpens / Agent Serpens (low-confidence TTP overlap per Unit 42).
**Campaign:** "Blinder Tunnel" (named after attacker infrastructure terms + the malware's tunneling capability), "Peaky Blinders"-themed branding, theme song embedded in malware. Targets: Iraqi critical infrastructure (telecom, aviation); staging observed as early as **Nov 18, 2025**, activation **March 2026**.
**Source:** Unit 42, published **October 6, 2026 10:00 UTC** — full text captured by this wiki same-day. GitHub has taken down the identified malicious infrastructure. Unit 42 notes other vendors covered fragments (Elastic, CPX, Group IB, Sophos/Drokbk, Cybereason); this is the first report tying the cluster together.

## Initial access: the recruitment three-act

1. **Fake career portal (credibility builder).** Inno Setup installer "Dubai Airport Careers" presenting an offline, self-contained mock Dubai Airports IT careers site with recruiter-supplied login and a 10-question HR questionnaire. **The questionnaire is a pure decoy — zero network activity, zero exfil, zero execution.** Its only function is lowering the target's guard.
2. **Weaponized "coding challenge" (April 2026).** Archive `DubaiAirport_Carrers_IT_Test.zip` (misspelling in the archive name is the attacker's) with a personalized Readme.md ("Dear <full name>"), a C# Flight Management System project, and an intentional planted bug (a for-loop skipping the last element) to make the "fix it and run it" instruction credible to a real engineer.
3. **Execution via the IDE itself.** The `.csproj` **overrides MSBuild's `GetFrameworkPaths` target** — during Visual Studio's design-time build this executes the attacker's custom target the MOMENT the project loads, before any compile or run. It copies hidden binaries from the project's Resources folder to `%LOCALAPPDATA%\Microsoft\RuntimeBrokers\` and launches a sideloaded `RuntimeBroker.exe`. Hunt: **any `GetFrameworkPaths` (or other standard-target override) defined inside a .csproj**, and any repo shipping binaries under Resources.

Chain = weaponized .csproj → **AppDomainManager hijacking** (an emerging evasion technique Unit 42 reports Iranian groups adopting; also used to disable ETW) → **DLL sideloading**.

## Tool set (all .NET, all Obfuscar-obfuscated with runtime string decryption + non-printable Unicode identifiers)

| Component | File | Role |
|---|---|---|
| ShelbyLoader V2 | `RuntimeBroker.dll` | Loader/persistence/fingerprint + C2 registrar |
| PsProxy.dll | `PsProxy.dll` | Stateless in-memory PowerShell engine — hooks `System.Management.Automation.dll`, custom runspace, **never spawns powershell.exe**, no disk scripts |
| ShelbyC2 V2 | `RuntimeBrokerApi.dll` (AES-CBC file, decrypted at runtime) | Primary RAT; stages Blackwood |
| Blackwood | `Blackwood.dll` sideloaded via Microsoft-signed `vshost32.exe` + `.config` | Zero-disk **Chisel** tunneling wrapper — reflective-loads an 8.4 MB AES-256-CBC-encrypted `Blackwood.Cheese.xml` manifest resource; reverse SOCKS proxy `R:0.0.0.0:10999:socks` |

**ShelbyLoader V2 mechanics:** persistence = registry Run key `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\MicrosoftRuntime` (120-s check, four logged states reported to C2: already persisted / newly persisted / key not found / executable not found); 63-s beacon loop authenticating with a hard-coded GitHub PAT against repo `peakyblinders-tm/myLic`: uploads Base64 machine fingerprint to `/{machineId}/Lic.txt`, polls `/{machineId}/Inf.txt` for Base64 commands, acknowledges by uploading the SHA-256 of the file to clear it; HTTP 403 (rate limit) → one-hour sleep. `machineId` = first 16 lowercase-hex chars of SHA-256(`"Peaky Blinders 2.1" + machine fingerprint`). Anti-analysis: WMI/process/registry/file VM markers, CPU/RAM/disk checks, must be spawned by `explorer.exe`.
**ShelbyC2 V2 decryption key** = full SHA-256 of the license string fetched live from the Lic.txt C2 path (IV = first 16 bytes of that hash) — the RAT binary on disk is inert without the live GitHub key.
**Blackwood config crypto:** if the loader's extension is `.dll`, `Blackwood.dll.conf` is Base64 + **RC4 with hardcoded key `My name is Blackwood !`**; renaming the extension makes the loader read it as plaintext and fail (anti-analysis tripwire). Chisel payload key = SHA-256 of hardcoded passphrase `y0Da+QH#pwSg38E?=8R;71-jQu8Tqq`.
**GitHub Issues C2 fallback (the durable mechanic):** if the PAT is revoked or primary channel returns 401, a **dead-drop resolver** queries the GitHub Issues **Search** API for issues created that day (`yyyymmdd` query + repo + is:issue filter), fetches comment bodies, extracts ciphertext between `<!--` `-->` HTML comment markers, AES-256-CBC-decrypts with key = MD5(date-string + machineId), IV = MD5-of-key iterated 5×, then regex-updates its own config: `Owner=(\w.+)` / `LicRepo=(\w.+)` / `LicToken=(\w.+)`. Operators also planted encrypted fallback C2 data **in comments of benign unrelated GitHub issues** — undecryptable without the victim's machineId. This is the Sophos-documented Drokbk dead-drop pattern hardened with per-victim keys.

## Attribution artifacts (Unit 42)

- Blackwood C2 IP hosted on Iranian ISP **TOSE'EH ERTEBATAT NOVIN ARIA**; secondary Hetzner tunneling server resolves to Persian-language domains likely bought via an Iranian reseller.
- Attacker-hosted `.mp3` in the public GitHub repo retained metadata pointing to **MusicDel.ir** (Iranian music platform).
- Victimology (Iraqi critical infrastructure, Israeli entity, UAE lure) + TTP convergence (aviation lures, AppDomainManager hijacking resembling Screening Serpens, GitHub dead-drop resolvers, in-memory .NET PowerShell wrappers resembling Agent Serpens).

## Operational-testing artifacts (how they were burned)

- Nov 18, 2025: dead-drop C2 validated via a public GitHub issue comment before campaign activation.
- Apr 24, 2026: issue titled `asasas` in `peakyblinders-tm` used as a mock "New device Found / Login detected" telemetry dashboard — including fabricated IP `138.256.21.23` (invalid octet, non-routable by design) tagged country `IQ`.
- May–Jun 2026: the same server `65.109.214.145` carried BOTH the Blackwood backend (port 8080) AND a credential-harvesting phishing site against an Israeli entity — Google Drive typosquats (`cloud.g-drive.cam`, `googeldrive.cam`, `drivegoogel.cam`, `googelmeet.online`, `meetonline.cam`) serving a fake Drive error page luring `WarUnPublishedDocuments.zip` download then a fake Google login. Earlier staging on `asdfafadafg.online` → `38.180.136.127`. Google confirmed no Drive infrastructure involved; Safe Browsing blocks the domains.

## Indicators (from Unit 42's published set)

SHA-256:
- `DubaiAirport_Carrers_IT_Test.zip` `6e7d9b33f1e72ea1ede71373a604ecdb060dab7d42055179c1eede9ecd1fd239`
- `FlightManager.csproj` `f5b12772db6817f7a765a6fe7565fd3d4f87edc28e42fe3ec0244a372a410fc9`
- `RuntimeBroker.dll` (ShelbyLoader V2) `53f35e49eb9b271fd8cbcd3daacb525328dbf159a03dbd1c7adebe0363daa402`
- `PsProxy.dll` `3fd810a3aa0039993393741b32287c367a9a5037a41e826906440887cdd3ed13`
- `Blackwood.dll` `76273382e4252c1f60a2251141e108942494409c759358320735891762c0682e`
- `Blackwood.dll.conf` (→ `91.107.156.29`) `d3561bd4aad003dc3e08157b0891860bb496b80cd6e44901692e08ab1d4e8260`
- Blackwood archive → `65.109.214.145`: `f5ba1645694c62f527ed6ceda8c68a5c3dd92b4032439167e8e937e72803b4bd`
- Blackwood archive → `87.248.129.239`: `7cc571aca6d8715d9aaad3d83e1bcd30467565d583db1dfe73697c5d00a1f875`

IPs: `91.107.156.29`, `87.248.129.239`, `65.109.214.145`, `38.180.136.127`.
Domains: `cloud.g-drive.cam`, `googeldrive.cam`, `drivegoogel.cam`, `googelmeet.online`, `meetonline.cam`, `asdfafadafg.online`.
Registry: `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\MicrosoftRuntime`; payload dir `%LOCALAPPDATA%\Microsoft\RuntimeBrokers\`.
GitHub accounts (taken down): `peakyblinders-tm` (repos `myLic`, `pubs`), `GreenBeret0`.

## Durable reads for this wiki's audience

1. **The IDE build pipeline is an execution path.** A `.csproj` is code. Design-time build targets (`GetFrameworkPaths` and siblings) run with the developer's full privileges the moment a project opens — no build, no run, no script consent prompt. Hunt: standard MSBuild target names defined inside project files; binaries under project `Resources/`; `RuntimeBrokers` under `%LOCALAPPDATA%\Microsoft\` (the attacker chose a folder that looks native).
2. **GitHub-API C2 with Issues dead-drop is the hardest C2 to block** — the traffic is TLS to api.github.com indistinguishable from developer traffic, tasking lives in repo file contents, and rotation lives in HTML comments on public issues, including innocent third-party issues. Blocking is per-account/report, not per-domain. Detection is behavioral: unusual GET volume to `/repos/*/contents/*` + `/search/issues` from non-development processes (a .NET process that isn't git/gh polling the search API every 63 s is the tell).
3. **Per-victim-keyed dead-drops defeat sweep-and-patrol hunting.** The planted comments are ciphertext without the victim's machineId — defenders cannot IoC the tasking itself, only the query grammar (`yyyymmdd` + `is:issue` search patterns) and account reputation.
4. **Recruitment lures now stage credibility as a separate artifact.** The zero-network decoy portal defeats sandbox triage (it IS clean) and is a deliberate trust-investment device; the malicious step is the SECOND delivery days later. Corporate recruiting-awareness programs keyed on "malicious attachment" miss this: the first artifact never is.
5. **OpSec, not tech, attributed them**: theme-song MP3 metadata, an Iranian ISP on one C2 IP, QWERTY-smash test issues, and reusing one server for tunneling AND phishing. Infrastructure hygiene failures still collapse "living off the cloud" ops.
6. This is the **developer-estate-targeting** class this wiki tracks from the registry side (see SubQuery, abstract-claude, virgil-cli entries) approached from the APT side: the same laptops — IDEs, GitHub identities, cloud creds — are the target, via code-repo intrusion here instead of package installation.

## Related pages
- [SubQuery release-pipeline compromise](subql-common-ci-artifact-substitution-release-pipeline-compromise-october-2026.md) — same developer/GitHub estate, registry-side technique, unrelated actor
- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — this wiki's standing OSV watch stream carrying the eighty-first-sweep verification of this publication
- [ai-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md) — actor-tooling context

**Sources:** Unit 42 "Blinder Tunnel Campaign Targets Iraqi Infrastructure" (October 6, 2026, full text captured by this wiki same-day, including appendices A–C and the published IOC set); Elastic "The Shelby Strategy", CPX Blackwood analysis, Sophos Drokbk, ClearSky Iranian Dream Job campaign — all cited via the Unit 42 report. Public sources only.
