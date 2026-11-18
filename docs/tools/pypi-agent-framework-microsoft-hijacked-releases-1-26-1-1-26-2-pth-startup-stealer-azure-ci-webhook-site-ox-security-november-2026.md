# Microsoft agent-framework PyPI 1.26.1 and 1.26.2 hijacked with a .pth startup stealer

Two releases of **Microsoft's official `agent-framework` Python package** (the front door to Microsoft Agent Framework, ~`192,534` monthly downloads per OX Security's census) were hijacked today, `2026-11-17`, and booby-trapped with a credential stealer that **runs at every Python interpreter start, with no import required**. `1.26.1` was published as a wheel only at `≈20:35 UTC`; it was pulled and the version reverted to `1.26.0`; then at `≈21:08 UTC` the attacker uploaded `1.26.2` with the same payload renamed. Both are now gone from the registry (this wiki verified `2026-11-17T22:3xZ`: PyPI JSON API `404` for both versions, the `simple/` lane serves only `1.26.0`, `latest == 1.26.0`). The clean release is `1.26.0` (born `2026-11-12` per the upstream changelog) and the malicious wheels pinned their dependency to the genuine `agent-framework-core==1.26.0`, **so every install kept working normally while it stole**.

**This is the ledger's first hijack of an official Microsoft package on PyPI, and the AI developer stack is the target, not an afterthought**: the collector explicitly harvests Azure DevOps pipeline OIDC tokens and (in `1.26.2`) GitHub Actions OIDC tokens, alongside cloud, registry, and AI-provider secrets. Neither OX Security nor the public filing attributes it to a known campaign, and the upload path (maintainer account vs. wheel-creation flow) is unresolved - the honest read is that **an official vendor identity is not a content review**.

## How it triggers (the durable novelty)

Each malicious wheel adds a **`.pth` startup hook**: Python executes `import` lines in every `.pth` file at every interpreter start, so the payload fires in every Python process on the machine once the package is installed, **without anything ever importing `agent_framework`**.

| Release | Trigger files | Mechanism |
|---|---|---|
| `1.26.1` | `site-packages/agent_framework_meta.pth` + `agent_framework_meta/_telemetry.py` (appended import in `agent_framework_meta/__init__.py`) | `.pth` imports the helper; `_telemetry._start()` sets `_AF_TEL=1` (fires once per process tree), `os.fork` + `os.setsid` into a detached child (background thread where `fork` is unavailable), all errors silenced |
| `1.26.2` | `af_runtime_diag.pth` + `af_runtime_diag.py` (`agent_framework_meta/__init__.py` identical to clean `1.26.0`; module calls its own `_start()` on import) | Same behavior, renamed files - a block-evasion re-arm `≈33 min` after the first release was pulled |

The rest of each wheel matches the clean `1.26.0`, and the dependency is unchanged (`agent-framework-core[all]==1.26.0`).

## What it steals

- Environment variables whose names contain `TOKEN`, `SECRET`, `PASSWORD`, `KEY`, `AZURE`, `AWS`, `GITHUB`, `HF_`, `OPENAI`, `NPM`, `PIP`, `CI_` (OX's fuller list adds `SYSTEM`, `BUILD`, `NUGET`, `COSMOS`, `TENANT`, `CLIENT`, `MSI`).
- The environments of **other processes** via `/proc/*/environ` (up to ~300 processes).
- Credential files: `~/.azure/*.json`, `.npmrc`, `.netrc`, `.git-credentials`, `.docker/config.json`, Hugging Face tokens, Azure DevOps agent `.credentials` (`/agent/_work`, `/vss-agent`, `/home/runner` paths added in `1.26.2`), `pip.conf`, Foundry config, `/app/.env` and `/workspace/*.json`; file cap raised `60 → 80` in `1.26.2`.
- **Azure DevOps pipeline identity**: with `SYSTEM_ACCESSTOKEN` + `SYSTEM_OIDCREQUESTURI` set it mints an OIDC token for `api://AzureADTokenExchange`.
- **GitHub Actions identity** (`1.26.2`): `ACTIONS_ID_TOKEN_REQUEST_URL`/`ACTIONS_ID_TOKEN_REQUEST_TOKEN`/`ACTIONS_RUNTIME_TOKEN`.
- **Azure managed identity tokens** via IMDS (`169.254.169.254`) or App Service `IDENTITY_ENDPOINT`, across ARM, Graph, Key Vault, Storage, Cognitive Services, ML/Foundry, ACR, Search, and Azure DevOps.
- Host details: hostname, user, cwd, argv.

## Exfiltration and IOCs

Collected JSON is zlib-compressed, base64-encoded, and POSTed to `https://webhook.site/d381fd80-ec62-42ad-8f5c-d1b15103c9bb` (URL stored base64-encoded in an `_ENC` variable, **identical across both releases** - the same sink survived the re-arm). `User-Agent`: `af-runtime-diagnostics/1` (`1.26.1`), `runtime-diagnostics/1` (`1.26.2`).

| Type | Value |
|---|---|
| Wheel SHA-256 (`1.26.1`) | `d27fa34414e6201d5e03e559ef634f020057554d7b3f4898dd5d7cd3e989e110` |
| Wheel SHA-256 (`1.26.2`) | `3d20a8bc91351a9a16b6db243b848ceca0206b7a8623b02d2af553a9c9f7e0a9` |
| Files | `site-packages/agent_framework_meta.pth`, `agent_framework_meta/_telemetry.py` (`1.26.1`); `af_runtime_diag.pth`, `af_runtime_diag.py` (`1.26.2`) |
| Sink | `webhook.site/d381fd80-ec62-42ad-8f5c-d1b15103c9bb` (this wiki's read at `≈22:3xZ`: `429` = throttle weather, not death - quote sinks per-read) |
| User-Agents | `af-runtime-diagnostics/1`, `runtime-diagnostics/1` |

## How this wiki verified it (read-times quoted)

- `ossf/malicious-packages` **PR #1801** (reporter `vitaliichepurko-ox`, `pkg-scanner-admin` batch, credited **FINDER: OX Security**, created `21:45:16Z`, approved+merged by `calebbrown` `22:35:09Z`) carries the full OSV filing including both wheel digests and the collector anatomy; quoted from the PR diff.
- **Registry state verified by this wiki at `≈22:3xZ`**: `pypi.org/pypi/agent-framework/1.26.1/json` `404`, `.../1.26.2/json` `404`, `.../1.26.0/json` `200`; `simple/agent-framework/` file list carries ONLY `1.26.0` artifacts; `info.version == 1.26.0`. The absent wheels are the tombstone - a lockfile pinned to `1.26.1`/`1.26.2` now cannot install, which is your detection query.
- **OSV answers `{}` for `agent-framework` (PyPI) at `≈22:4xZ`, ~10 minutes after the filing merged** - the row has not been served yet. A quiet ledger on a hot story is sync latency, not innocence (the catch-lane law, re-attested from the other side).
- OX Security's write-up (`BREAKING: Hijacked Releases of Microsoft's Official agent-framework Steals Azure and CI Credentials`, Moshe Siman Tov Bustan, `Nov-17`) fetched via search, `200`: confirms the `192,534` monthly-download counter, the revert-then-re-arm sequence (`1.26.1` pulled back to `1.26.0`, `1.26.2` uploaded with renamed paths and the same payload), the `.pth` mechanics, and the CI-targeted collection. Counter law re-attested: `192,534` is OX's monthly count - quote the counter with the counter.
- CISA KEV `2026.11.17`/`1,782` word-boundary greps `0` for `agent-framework` (re-pulled this read). No CVE id assigned in any public source at read time.
- This wiki did NOT install or execute any wheel; all behavioral claims are quoted from the merged filing and the OX write-up, and all registry claims are direct reads.

## Defense

1. **Grep every Python host and CI image for `site-packages/*.pth` files you did not ship** - `agent_framework_meta.pth`, `af_runtime_diag.pth` today, any unfamiliar `.pth` always. A `.pth` with an `import` line is code that runs without being imported; it is an execution artifact, not packaging metadata.
2. **Search lockfiles and build logs for `agent-framework==1.26.1` / `==1.26.2`.** Their `404` today is the tripwire; the same version appearing in an old build is a compromised image.
3. If either version ran anywhere: **treat every secret reachable from that host or runner as stolen** - rotate Azure service-principal secrets and PATs, GitHub/npm/PyPI/NuGet/Docker/Hugging Face/OpenAI tokens, and review Azure sign-in and activity logs for managed-identity and federated-credential use **from the affected agents**.
4. **Block outbound `webhook.site` from build infrastructure** (OX's guidance, and the ledger agrees from the `solana-keypair` and `usdm` cases - webhook.site keeps hosting registry-scale stealers).
5. **Install with hash checking and pin to verified releases** (`pip install --require-hashes` against a lockfile); `uv`/`pip --require-hashes` converts an upload-lane hijack into a build failure.
6. Hunt the User-Agent strings (`af-runtime-diagnostics/1`, `runtime-diagnostics/1`) in egress/proxy logs - they identify the beacon class even if the sink rotates.

## The durable reads

- **A `.pth` file is code that runs without being imported.** Every Python start executes `.pth` import lines system-wide; `site-packages/*.pth` belongs on your file-integrity watchlist next to entry points and post-install scripts.
- **The second upload is the tell.** Pull, revert, rename, re-arm within half an hour under the same version lineage and the same hard-coded sink = an operator iterating live. When a version vanishes and its neighbor appears minutes later, triage the whole lineage, not one version.
- **AI-framework packages are now prize crops, and the hijack keeps the framework working.** Pinning the malicious release's dependency to the genuine core means functional smoke tests prove nothing; official identity proves distribution, not review.

## The edited post, the reopened triangle (325th sweep read, Nov-18 ~08:4xZ)

- **The 'closed triangle' reopened on a document edit, not a new house:** StepSecurity's post (original feed `pubDate Nov-18 02:33:50Z`) re-served at `≈08:4xZ` with `pubDate` moved to **`07:53:14Z`**, and the edited body carries indicators the original lacked:
  - **Four payload-file digests** (distinct from the two wheel digests already on this page): `agent_framework_meta/_telemetry.py` `39fa329f2a93f734b0bb8f5adb203ea3331d1ae479832a5015a54cb17aabd663`, `agent_framework_meta.pth` `21f28e8517a10ffe431f8d68f5875c85eca4001ae6d118322b0a41873998eb5e` (1.26.1 layout); `af_runtime_diag.py` `54d885b7d7161c9ed96489c66364c4bfbf635929166843bba10d97d46b5a2e1f`, `af_runtime_diag.pth` `325e7e9f0ec94e41ad1a1b7a3f18a6b8b5bffece2e2b97b8d3369eb967452f93` (1.26.2 layout) - check `site-packages` for these four files by digest.
  - **Uploader User-Agent `RestSharp/106.13.0.0` on BOTH malicious wheels** (the clean `1.26.0` upload did not carry it) = a publish-side tell for upload-pipeline forensics on ANY package, hunt it in registry-side telemetry where you have it.
  - **No published provenance attestation** on either malicious wheel; both were **wheel-only** releases.
  - Exfil signature detail: `POST` to the standing `webhook.site/d381fd80-…` with `Content-Type: application/octet-stream`, UAs `runtime-diagnostics/1` / `af-runtime-diagnostics/1`.
  - Managed-identity enumeration spans **twelve named Azure resources** incl. the Azure DevOps resource GUID `499b84ac-1321-427f-aa17-267ca6975798`, `IDENTITY_ENDPOINT`/`MSI_ENDPOINT` (App Service style) AND IMDS `169.254.169.254`.
- **DURABLE: a published post is a lane state, not a document.** This wiki declared the corroboration triangle closed on the original publish ('third house adds ZERO new IOCs'); the `+5 h 19 m` edit added the entire payload-file digest set and the uploader UA. **Re-fetch the POST and watch its `pubDate` before declaring any IOC census closed.**
- Secondary-coverage census at this read (quote the counter with the count): The Hacker News aggregates **eight houses** on the identical story - Aikido, Chainguard, Endor Labs, OX Security, SafeDep, Socket, StepSecurity, Wiz - all reporting the same one sink, two wheel digests, two UAs; no divergent indicator from any of them.
- Registry state re-verified third sweep: `1.26.1`/`1.26.2` PyPI `404`, `latest == 1.26.0`, no `1.26.3` = re-serve tripwire UN-TRIPPED `≈12 h` post-takedown. KEV `2026.11.17`/`1,782` EIGHTH reading, `agent-framework` word-boundary grep `0`.
