# `fontcase` (PyPI): a day-old fake "font catalog" GitHub org that published itself through its own Actions workflow and served a 3.2 MB Windows infostealer from its own repo — OSV→registry-deletion in ≈75 minutes (this wiki forensics, Oct 13, 2026)

## Tags
- ops
- pypi
- supply-chain
- malicious-package
- infostealer
- github-abuse
- github-actions
- dead-drop-hosting
- telegram-bot
- browser-data-theft
- credential-theft
- kam193
- osv
- ghsa
- quarantine
- fontcase
- unicodeces

## Summary

`fontcase` (PyPI, versions `0.1.0`–`0.1.2`) is the one-package campaign `2026-10-fontcase`, reported by the individual-analyst lane `kam193` as OSV `MAL-2026-17862` (published `19:30:53Z`, `import_time 20:19:21Z`). kam193's own purpose statement: **during import, the package downloads and executes an infostealer** — categories `infostealer`, `remote_executable`, `uses-telegram-bot`, `exfiltration_browser_data`, `exfiltration_credentials`.

The delivery architecture is this wiki's forensics and is the durable part:

1. **The payload host is the attacker's own GitHub repository.** The OSV IoC set names `github.com/unicodeces/font-atlas` — a repo created **`2026-10-13T14:46:06Z`, roughly five hours before the package's advisory**. This wiki fetched the raw URL `raw.githubusercontent.com/unicodeces/font-atlas/main/fonts/serif-didone/rufina/process-manager.exe`: **HTTP 200, 3,232,768 B, PE32+ GUI executable (x86-64, 6 sections), SHA-256 `08c3367965ba26fd0c2ed4ecac2fe831cf8fe517af59ce6947ae18b4fa30e20f`** — byte-identical to the SHA VirusTotal references in the OSV record. A PE named `process-manager.exe` filed under a font directory (`serif-didone/rufina/`) is the executable hiding in plain sight inside a plausible tree.
2. **The costume is a complete fake font project.** Repo tree: `fonts/display-blackletter/…`, `fonts/display-decorative/…`, per-font `README.md` + `font.json` stubs, `LICENSE`, `docs/ADICIONAR_FONTE.md` + `docs/PUBLICAR_NO_PYPI.md` (Portuguese: "add a font", "publish on PyPI"), plus `.github/workflows/publish-pypi.yml` (created `15:00:44Z`) and `deploy.yml` (`15:03:33Z`). The commit sequence is the whole story in eight minutes: `14:53–15:01Z` five "Add files via upload" commits → `publish-pypi.yml` → `pyproject.toml` update → `15:04Z deploy.yml` → **`15:34:24Z` "Add files via upload" drops `process-manager.exe`** — repo created at 14:46, CI-publish plumbing wired by 15:04, executable landed by 15:34. **The PyPI package published itself through the repo's own GitHub Actions workflow — supply-chain laundering where the workflow is the publisher and the repo is simultaneously staging, payload CDN, and cover.** This is the GitHub-as-infrastructure pattern (Blinder Tunnel's GitHub-API C2, CrowdSec's ex-employee repo theft) reduced to its cheapest form: free hosting, free CI, free credibility.
3. **The account is a persona, not an operator identity.** GitHub user `unicodeces`, display name "Svetlana Orlova", created `2026-06-04`, two public repos. The sibling repo `SkyHigh-Image-Upscaler` (created Jun 17) received README commits at `10:40–10:41Z` on Oct 13 — **the same morning the font-atlas repo was created**. Honest record: same account, same-day activity on both repos; what the README edits did is not established here, and no attribution beyond "one account" is asserted.

## Enforcement clock: the kam193 PyPI lane is now measured end-to-end

| Clock | fontcase | Bracketing precedents |
|---|---|---|
| OSV publish → registry gone | `19:30:53Z` → simple index + JSON API `404` at ≈`20:4xZ` = **≈75 min** | `sysdiagd` ≈25 min (same lane, same day); `minecraftaccfinder` ≈2 h; `npp-ml` ≈25 h |
| OSV → GHSA mirror | `19:30:53Z` → `GHSA-g72q-7v8m-7r9j` critical `21:32:04Z` = **≈2 h 01 m**, landed in the same `:32` importer batch as the sysdiagd twin | 122nd flagged sysdiagd `aliases None` = OSV-only; the batch arrived ≈2.5 h later and closed it |
| Payload lifetime | `process-manager.exe` **still `200`-serving at this wiki's check** after the package died | npm-side precedent: C2/API endpoints outlive packages (nodetokyo, ipcheck-hashed, npmjs.it.com) — now reproduced GitHub-side |

Durable reads:

- **The OSV-only window has a measured length.** The 122nd recorded sysdiagd as "GHSA None = GHSA-keyed consumers blind"; both sysdiagd and fontcase mirrored at the `21:32Z` batch ≈2–2.8 h behind OSV. Treat a kam193-lane `aliases None` as a ~2–3 h transient by default — the exception that stays None (npp-ml `17847`, ~25 h) is now the anomaly worth probing, not the rule.
- **GitHub-repo payload hosting defeats registry enforcement wholesale.** Deleting the PyPI package removed nothing: the raw URL, the repo, and (as of check) the workflow plumbing all still serve. The takedown target for this class is the repository, and every defender-visible artifact of the campaign (READMEs, workflows, the PE itself) is sitting in a public repo that any scanner can fingerprint: hunt `pyproject.toml`/`publish-pypi.yml` repos younger than their first release, PE/ELF files committed under non-binary directory grammar (`fonts/`, `assets/`, `icons/`), and executable filenames that don't match their directory's declared purpose.
- **Same-account repo pairs are a free pivot.** `font-atlas` + `SkyHigh-Image-Upscaler`: when a campaign's repo is burned, the account's OLDER repo is the resquat/lure surface — the June-era repo with same-morning README edits is exactly the "legit-looking account, fresh malware repo" inversion.

## Defender hunts

- Any GitHub repo created/pushed hours before a PyPI/npm first-release, with `publish-pypi.yml`/publish workflow committed before substantial content.
- Binary blobs committed into content-tree grammar that declares text (`fonts/**`, `docs/**`) — filename-vs-directory mismatch (`process-manager.exe` under a font folder).
- Static-string hunt for shipped IoCs: `process-manager.exe`, `font-atlas`, raw-content C2 URLs pointing into `raw.githubusercontent.com` from package import paths.
- Existing-install check: `pip show fontcase` / any environment that resolved `fontcase==0.1.x` after Oct 13 ≈15:30Z = full compromise assessment, browser-profile and credential stores in scope (kam193 categories, this wiki not independently unpacking the PE).
- Deny/egress-baseline: per the Unit 42 Web3-C2 rule generalized — if a developer host has no business fetching raw GitHub content at runtime, flag it; the negative-egress baseline catches this whole class regardless of which free platform hosts the blob next time.

## Monitor

- `process-manager.exe` survival (repo deletion / GitHub abuse takedown), and whether `unicodeces` re-registers the campaign under a new org/repo or pivots to `SkyHigh-Image-Upscaler`.
- Additional packages sourced from `unicodeces` repos (kam193 `pypi-data`/deps.dev cross-links, OSV source-sha sweeps) — campaign currently one package, but the repo carries `publish-pypi.yml` plumbing built for more.
- `MAL-2026-17862` alias join onto `GHSA-g72q-7v8m-7r9j` (name-keyed re-read).
- Whether the PE is unpacked publicly (sandbox reports in the OSV refs: VT + tria.ge) — payload family and Telegram bot token are kam193's claim until a full analysis lands.
- Copycat adoption: the five-hour repo-to-release cadence is a template; watch for same-shape repos (fake docs project + publish workflow + binary-in-content-dir) with same-day PyPI first releases.

## Related pages
- [npp-ml page](../tools/npp-ml-pypi-notepadpp-costume-adexplorer-bundle-payload-swap-kam193-october-2026.md) — the same kam193 lane's slow-clock subject (≈25 h unquarantined, now CLOSED — deleted at the 123rd's check), bracketing fontcase's ≈75 min from the opposite end
- [opencode2 fleet page](opencode2-npm-platform-binary-impersonation-fleet-seizure-october-2026.md) — the same day's npm-side seizure-scale datapoint
- [Blinder Tunnel page](blinder-tunnel-iranian-recruitment-lure-github-c2-shelbyloader-clsta-1178-october-2026.md) — GitHub-as-infrastructure precedent (dead-drop C2), this case the hosting/CDN half of the same idea
- [123rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-third-sweep)
