# The `algamil7x` npm cluster: five corporate-squat scoped packages beacon installer identity over DNS labels to one attacker domain (Amazon Inspector via GitHub Advisories, Sep 18, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- DNS-exfiltration
- DNS-tunneling
- reconnaissance
- typosquat
- scope-squat
- obfuscation
- install-script
- Amazon-Inspector
- GitHub-Advisories
- algamil7x

## Summary

Between 00:31 and 21:31 UTC on **September 18, 2026**, GitHub published five malware-class advisories — all sourced to **Amazon Inspector** — for five differently named npm packages that share one code family and one destination: a `dns.resolve4()` lookup whose subdomain is built from **the installer's OS username, hostname, and current-working-directory basename**, sent under attacker-controlled **`oob.algamil7x.xyz`**. The payload is not a stealer or a loader — it is **target qualification**: every `npm install` tells the operator who (username), where (hostname), and on what project (cwd) the package landed, exfiltrated through the attacker's own **authoritative DNS logs** with zero HTTP egress. Four of the five names were gone from the registry within a day; at this wiki's live check on **Sep 19–20, 2026**, **`@insiderintelligence/googleadmanager` (latest `9.9.10`, created Sep 18 14:11 UTC) still resolves on npm**.

| Package | Advisory | Published (UTC) | Prefix in DNS label | Registry state (live check Sep 19–20) |
|---|---|---|---|---|
| `@tink/tink-link-core` | GHSA-hvcc-qwg6-972c | Sep 18 00:31 | (prefix + hardcoded domain) | **unpublished / not found** |
| `@shared-web/assets` | GHSA-vmr9-5w3x-4v98 | Sep 18 15:31 | `<pkg>` chain | **unpublished / not found** |
| `@shared-web/utils` | GHSA-29f7-pqf4-c94j | Sep 18 21:31 | `swutils` | **unpublished / not found** |
| `@shared-runtime/modules@9.9.10` | GHSA-g85c-jph7-8q4r | Sep 18 21:31 | `srmods` | **unpublished / not found** |
| `@insiderintelligence/googleadmanager` | GHSA-76rx-jxhm-vhww | Sep 18 21:31 | (values directly) | **STILL PRESENT — latest 9.9.10, 2 versions, created 2026-09-18T14:11Z** |

OSV mirrors exist for the cluster (e.g. `MAL-2026-16292` for `@shared-web/utils`, `MAL-2026-16290` for `@insiderintelligence/googleadmanager`), so consumer tooling will surface these even though npm-side packages are gone.

## Confirmed mechanics (from the advisories' Amazon Inspector analyses)

- **Trigger:** `package.json` declares an `install` lifecycle script (`node index.js`), which loads `lib/core.js`. At least one member (`@shared-web/assets`) **also executes `./lib/core.js` on plain `require`** — install-script approval gates (npm ≥ 12) don't cover that path.
- **Collection:** `os.userInfo().username`, `os.hostname()`, and the basename of `process.cwd()` — a per-install host fingerprint plus a project identifier.
- **Exfiltration:** a `dns.resolve4()` query for a label chain of the form `<prefix>.<user>.<host>.<cwd>.<timestamp>.oob.algamil7x.xyz` (`@shared-web/utils` uses prefix `swutils`; `@shared-runtime/modules` uses `srmods`). The answer never matters — the data is recorded in the **authoritative nameserver logs** for `algamil7x.xyz`.
- **Obfuscation lineage:** the destination hostname and the `os` / `dns` / `process` module names are stored as **hex byte arrays / char-code arrays** in numbered `lib/*.js` files and reconstructed at runtime with `String.fromCharCode`, with modules loaded through **`module.constructor._load`** (bypassing ordinary `require` strings). Same file-layout trick across all five, with different file names (`lib/a9b3de.js`, `lib/c5df9a.js`, `lib/a74d1f.js`, `lib/g7h8i9.js`, …) — one author or one template.
- **Naming:** all five impersonate **plausible internal/corporate scopes** — `@shared-web`, `@shared-runtime`, `@insiderintelligence` (Insider Intelligence / eMarketer), and `@tink` (the real **Tink** open-banking SDK, with a `github.com/tink-link/core` homepage decoy). These are names a developer could plausibly see in a company lockfile and not question.
- **No second stage observed** in any advisory: no downloader, no reverse shell, no credential reader. This is the reconnaissance/telemetry layer, not the payload layer.

## Why it matters (durable reads)

1. **DNS-label beaconing is the lowest-egress telemetry channel.** No HTTP(S) request, no destination socket your egress proxy logs matter to — the "exfiltration" is a resolver query whose content the attacker reads from their own zone logs. Egress allow-lists that permit DNS (everyone's) do not constrain it. Hunt belongs in **DNS logs**, not web-proxy logs.
2. **This is target qualification, read as an attack precursor.** Username+hostname+cwd answers "which organizations installed this and on which repo" before any payload is committed to. Expect a follow-on wave aimed at the orgs that beaconed back; treat every install as a disclosed target list, which is why removal alone does not close exposure — **the operator already learned who you are and what project dir you work in**.
3. **The corporate-scope-squat pattern targets trust, not popularity.** Unlike classic typosquats (`crytpto-js`), these names succeed by reading like your employer's private scope. Defender control: **private scopes should be actually private** — npm's scope-claiming for reserved orgs, plus lockfile linting that flags any scoped install not on an internal-scope allow-list.
4. **Amazon Inspector is now a recurring primary feeder for npm malware advisories** (this cluster is Inspector-sourced, as were several Sep 18 singles and the earlier `wshu.net` campaign's dynamic analysis). Malware-class GitHub Advisories with `## Source: amazon-inspector` headers are a durable, structured intel channel worth programmatic watching — the descriptions carry behavior-level detail (file names, obfuscation methods, exact DNS shape) that registry takedown notices do not.
5. **Same-day cluster, one-day partial takedown, one survivor.** The Sep 18 publish burst (00:31→21:31 UTC) plus four removals inside ~24 h reads as registry action after advisory intake; the still-live `@insiderintelligence/googleadmanager` is either missed or lagging — a reminder that **`latest` on a suspicious scope is live exposure regardless of how many siblings were pulled** (`npm audit` won't flag what npm still serves).

## Hunt guidance

- **DNS telemetry (primary):** any query at or under `algamil7x.xyz`, and generically any A/AAAA lookup whose leftmost labels embed a lowercase username, hostname, and a Unix-style timestamp joined by dots — the label grammar (`<prefix>.<user>.<host>.<cwd>.<ts>.oob.<domain>`) is distinctive even after the domain rotates.
- **Registry/lockfile audit:** the five names above at **all versions**, plus anything under scopes `@shared-web`, `@shared-runtime`, `@insiderintelligence`, `@tink` that is not on your internal allow-list; check both lockfiles and what CI resolved Sep 17–20.
- **Package-content statics:** packages shipping numbered `lib/<hexish>.js` files that `String.fromCharCode`-assemble module names and require via `module.constructor._load`; `dns.resolve4` in a dependency whose stated purpose has nothing to do with DNS.
- **Lifecycle posture:** treat an `install` script in a scoped package that merely "assembles strings" as this class until proven otherwise; npm ≥ 12's install-script approval denies the install-script path but not the `require`-time path seen in `@shared-web/assets`.

## September 20 sweep follow-up: survivor still live, and a neighboring same-day dependency-confusion recon wave (verified by this wiki)

**Re-check (Sep 20, ~05:25 UTC, this wiki):** `@insiderintelligence/googleadmanager` is **STILL on npm** — `latest 9.9.10`, manifest modified timestamp unchanged (`2026-09-18T17:00Z`). ~36 hours after the advisory, one beacon survives while its four siblings are gone.

The same Sep 18–19 Amazon-Inspector/OpenSSF advisory burst that produced the algamil7x cluster also carried a **separate, neighboring set of dependency-confusion / name-squat payloads** — same intake window, different authors and mechanisms. All verified via the GitHub Advisories API and npm registry this sweep; **none carry a CVE**:

| Package | Advisory (published UTC) | Payload shape | Registry state (Sep 20) |
|---|---|---|---|
| `x509-escaping` (npm) | GHSA-fq85-7xqm-cgj9, Sep 18 21:31 | `preinstall` collects hostname/username/home/DNS servers/cwd + reads `/etc/passwd` and `/etc/hosts`, POSTs the bundle to a hardcoded **Burp Collaborator subdomain** (`*.oob…oastify.com`) — recon, no library code shipped | name remains, all versions gone (no `latest`) |
| `chai-as-indexed` (npm) | GHSA-727r-6hg5-947x, Sep 18 21:31 | on `require`, POSTs the **full `process.env`** to a base64-concealed endpoint (`ipcheck-hashed[.]vercel[.]app/api/auth/…`) and pipes the **response body into `new Function('require', …)`** = remote server executes arbitrary code in the importing process on every load, with real `require` | name remains, all versions gone |
| `internallib_v949` (npm) | GHSA-4qw5-jqr6-c4fj / GHSA-f863-m366-9cfm, Sep 18 21:53 | `index.js` runs `child_process.exec` of a `curl https://reverse-shell.sh/…` pipe-to-shell against endpoint `10.0.16.19:443`; self-referential dependency on its own name = internal-name squat for internal-build interception | now `0.0.1-security` reservation (taken down) |
| `tailwindcss-forms-ui` (npm) | GHSA-fc5q-m33g-rp9c, Sep 18 21:31 | typosquat of `@tailwindcss/forms` (payload detail in OSV) | name remains, all versions gone |
| `py-venv-doctor` (PyPI) | GHSA-94w6-hr49-qjm7, Sep 19 00:32 | "healthcheck report" + opt-out telemetry that **exfiltrates the full environment-variable set**; OpenSSF campaign `2026-09-py-venv-doctor` | gone from PyPI (Sep 20 check) |
| `keroeltop` (npm) | GHSA-gg5m-rqpp-c9xf, Sep 19 03:32 | OpenSSF package-analysis flag (malicious-domain communication) | — |
| `urc` (PyPI) | GHSA-3c7m-3qhf-wqrr, Sep 19 06:32 | install-time host-info exfil; OpenSSF categories it `PROBABLY_PENTEST` (low-harm possibility) | — |

**Durable reads from the wave:**

1. **Legitimate-platform C2 hosting keeps winning.** `chai-as-indexed`'s C2 is a `vercel.app` function and `x509-escaping`'s is a **Burp Collaborator (`oastify.com`)** subdomain — a commercial pentest tool's own OOB channel as attacker exfil. Both destinations live on infrastructure no sane egress policy blocks. Hunt by *behavior* (env-dump POST at require time, resolver/proxy queries for `*.oastify.com` from build hosts) rather than destination reputation.
2. **The `new Function(require, serverResponse)` pattern is the require-time twin of WeaselBiscuit's Npoint fetch** — remote server supplies code executed with real module privileges on every import. Two independent npm payloads using it in one week says the pattern has left DPRK tooling and entered commodity malware templates.
3. **The `reverse-shell.sh → 10.0.16.19:443` payload in `internallib_v949` targets a private IP** — either a test build caught by the pipeline or an actor with a staging script left misconfigured; either way a reminder that some registry malware is low-skill noise around the same intake window, and triage should read the payload, not just the advisory class.
4. **Same intake window ≠ same campaign.** Five+ packages on Sep 18–19 advisories share a date and source, not an author: algamil7x is one code family; these neighbors are unrelated one-offs. Date-collapsing in threat feeds over-reports clusters — compare obfuscation lineage and destination before merging.

Hunt delta from this section: flag build hosts querying `*.oastify.com`; alert on any dependency POSTing `process.env` or reading `/etc/passwd` at install/require; treat `vercel.app` API endpoints as C2-capable in package-audit context.

## Monitoring

- Takedown of the surviving `@insiderintelligence/googleadmanager` (re-check registry state each sweep).
- Domain rotation away from `algamil7x.xyz` (new `oob.*` domains using the same label grammar).
- Whether a **second wave / payload** appears aimed at orgs that beaconed (this cluster's reconnaissance shape invites a follow-on targeted drop).
- Whether Amazon Inspector or others publish more packages sharing the `lib/<hexish>.js` + `module.constructor._load` lineage (cluster growth beyond five).
- Any vendor writeup (Socket, SafeDep, StepSecurity, Sonatype) naming the campaign or linking it to a known actor — **no attribution currently exists or is implied here**; the domain string hints at nothing we treat as evidence.

## Sources

- GitHub Advisories (Amazon Inspector-sourced): [GHSA-hvcc-qwg6-972c](https://github.com/advisories/GHSA-hvcc-qwg6-972c) (`@tink/tink-link-core`), [GHSA-vmr9-5w3x-4v98](https://github.com/advisories/GHSA-vmr9-5w3x-4v98) (`@shared-web/assets`), [GHSA-29f7-pqf4-c94j](https://github.com/advisories/GHSA-29f7-pqf4-c94j) (`@shared-web/utils`), [GHSA-g85c-jph7-8q4r](https://github.com/advisories/GHSA-g85c-jph7-8q4r) (`@shared-runtime/modules`), [GHSA-76rx-jxhm-vhww](https://github.com/advisories/GHSA-76rx-jxhm-vhww) (`@insiderintelligence/googleadmanager`), all published Sep 18, 2026.
- OSV mirrors: `MAL-2026-16292` (`@shared-web/utils`), `MAL-2026-16290` (`@insiderintelligence/googleadmanager`).
- npm registry live re-checks (this wiki, Sep 19–20, 2026): four names return `Not found`; `@insiderintelligence/googleadmanager` resolves with `dist-tags.latest = 9.9.10`, created `2026-09-18T14:11Z`, 2 versions.

## Related pages

- [WeaselBiscuit npm stealer cluster](../tools/weaselbiscuit-npm-stealer-beavertail-ottercookie-dprk-opensourcemalware-september-2026.md) — same week's npm campaign coverage; different design (import-time stealer vs DNS recon)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — the priority-watch propagation campaign this cluster is NOT linked to on current evidence
- [mathmain encrypted-loader npm trio](mathmain-encrypted-loader-npm-trojanised-mathjs-trio-safedep-september-2026.md) — the standing npm watch item; different lineage and mechanism
