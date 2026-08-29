# @7nohe/openapi-react-query-codegen npm compromise via exposed publishing workflow (Aug 28, 2026)

## Tags
- ops
- operations
- supply-chain
- npm
- GitHub Actions
- trusted-publishing
- OIDC
- workflow-abuse
- CI/CD
- credential-theft
- Bun
- binding.gyp
- preinstall
- unauthenticated-publish
- Shai-Hulud
- Mini Shai-Hulud
- Trinitite
- OX Security
- copycat
- TeamPCP
- open-source-malware
- attribution

## Summary

On **August 28, 2026**, an external GitHub user (public account **`p00paboot`**) abused the release workflow of **`@7nohe/openapi-react-query-codegen`** and published **ten malicious npm versions** that execute attacker-supplied code at install time. No maintainer npm password or long-lived npm token was involved: the repository's release workflow listened for **`issue_comment`** events, accepted a trigger comment whose body exactly matched **`npm publish`** on any pull request **without checking the commenter's role or repository association**, checked out the attacker's PR head, and published through **npm Trusted Publishing** using a GitHub Actions **OIDC** identity (`id-token: write`).

StepSecurity (August 28, 2026) reproduced the installation behavior on isolated GitHub-hosted runners under Harden-Runner and captured the runtime behavior: the payload downloads the **Bun** runtime from GitHub release infrastructure, then steals **GitHub authentication** (`gh auth token`, `git credential-manager github list --no-ui`), probes for SSH tooling and the **Google Cloud metadata hostname**, and shells out through a staged `updater.py`.

This is a clean example of the **issue-comment-triggered release-workflow / OIDC trusted-publishing abuse** pattern: an unauthenticated actor gains arbitrary package publication rights by posting one comment, because the workflow confers publish rights to *any* PR participant.

**Shai-Hulud lineage confirmed.** OX Security (August 29, 2026) identified the payload as a variant of the **Shai-Hulud** supply-chain malware family that now self-identifies as **"Trinitite: Sponsored by Preview 2 Effects"** — the same open-sourced codebase and signatures as the original Shai-Hulud / June Red Hat (Miasma) compromise, rebundled with new public encryption keys that make pinning to a specific operator harder. OX frames it as a **post-arrest copycat wave**: the first Trinitite-marker commit appeared ~12 hours before publication, and the compromise landed within 24 hours of the AFP/WAPF/FBI charging of the two men alleged to be behind TeamPCP. Treat it as a **Shai-Hulud-lineage / copycat assessment, not confirmed TeamPCP operator identity** — the new keys break the marker chain that previously tied variants together. See [OX Security: the payload is a "Trinitite" Shai-Hulud variant](#ox-security-the-payload-is-a-trinitite-shai-hulud-variant).

## Affected versions

Ten malicious versions:

- `0.5.4`, `0.5.5`
- `1.6.3`, `1.6.4`
- `2.2.1`, `2.2.2`
- `3.0.3`, `3.0.4`
- `0.0.0-365d4eb738d3146583431948d3ba6e27a32556be`
- `0.0.0-ec7876d6c917dad516ba69bbfafc948b834bf0ab`

The eight malicious **stable** versions were published between **20:00:43 and 20:20:53 UTC** on August 28, 2026. `0.5.4` grew from 41,621 bytes (in 0.5.3) to **5,658,449 bytes**; the other malicious stable artifacts ranged from 4.46 MB to 6.53 MB.

**Clean pin targets (known-good release lines):** `0.5.3`, `1.6.2`, `2.2.0`, `3.0.2`.

> As of the StepSecurity post, the npm registry still mapped the `latest` tag to malicious `3.0.4` and had **not** deprecated it. Verify current registry state before acting on `latest`.

## Attack mechanics

1. **Untrusted trigger reaches a privileged publisher.** The release workflow fires on `issue_comment` and required only that the comment belonged to a pull request and that its body exactly matched `npm publish`. It did **not** verify the commenter's repository role or association.
2. **The workflow grants `id-token: write`.** It checked out the PR head, ran `pnpm install`, and published via npm Trusted Publishing (GitHub Actions OIDC). This placed **untrusted pull-request code inside a privileged release job**.
3. **Attacker execution.** `p00paboot` opened **PR #215 and #216**, then posted the trigger comment. The resulting workflow runs reached their publish steps; npm registry timestamps followed within seconds. npm provenance ties the published packages to GitHub Actions and the repository's `release.yml`.

## Payload behavior (Harden-Runner runtime evidence)

The stable releases detonate so far (`1.6.3`, `2.2.1`, `3.0.3`, `3.0.4`) all caused `curl` to contact GitHub and `release-assets.githubusercontent.com` during installation. Registry metadata confirms the same `preinstall` command in the newly identified `0.5.5`, `1.6.4`, and `2.2.2`.

- **Explicit preinstall hook (3.0.4):** `"preinstall": "node 3FWCvzduYZg.js"` — a **6,384,601-byte** payload. SHA256 of `3FWCvzduYZg.js`:
  - `b24d121667f21f492cb9db34fbfd515d5922a8dd30b9c45215c7220abbb10ca8`
- **Malicious `binding.gyp` (3.0.4, and other stable releases):** a condition that traverses Python objects to reach `os.system()` and decodes to `node 3FWCvzduYZg.js` — a second execution path when `node-gyp` evaluates the file.
- **Direct payload execution (3.0.4, CI markers removed):** Node ran `3FWCvzduYZg.js`, which:
  - spawned `curl` and downloaded **Bun** from GitHub release infrastructure,
  - ran the executable from `/tmp/trinnyyyy-*/bun`,
  - ran **`gh auth token`** and **`git credential-manager github list --no-ui`**,
  - checked for `ssh` and `scp`, enumerated running processes, and invoked a shell with a temporary `updater.py` path,
  - contacted the GitHub API and **probed the Google Cloud metadata hostname**.

StepSecurity's OSS AI Package Analyst independently scored `3.0.4` **critical / risk 0 / rejected**, identifying XOR-decoded code passed to the JavaScript `Function` constructor, the malicious preinstall hook, and the obfuscated `binding.gyp` execution path.

## Indicators of Compromise

**Package versions** — see the ten affected versions above.

**Files / artifacts**
- `3FWCvzduYZg.js` (preinstall payload; SHA256 above)
- malicious `binding.gyp`
- `is_it_this_simple.js`, `nu.js`
- `/tmp/trinnyyyy-*/bun` (staged Bun runtime)
- `/tmp/*.js`, `/tmp/*/updater.py`

**Registry tarball hashes (npm tarball SHA1)**

| Version | SHA1 |
| --- | --- |
| 0.5.4 | `2d934cf137a4e62519f88e7ab669d2fabda33867` |
| 0.5.5 | `337ae261e4e73a9f365f892dcef2dc6f6932e90a` |
| 1.6.3 | `0f9bc76952b67d7a28a57d1e726293f417df0119` |
| 1.6.4 | `6499c9ab4e60f9b1db6756cb0de55ebc334a72d1` |
| 2.2.1 | `5ab130e4736d4582899af2385ec7eb5a33619d05` |
| 2.2.2 | `fc60551b23485829c0a6e910224b049c891a49b8` |
| 0.0.0-365d4eb738d3146583431948d3ba6e27a32556be | `e7a07ca4a3cd51c262495f473abe4c4e505b7be4` |
| 3.0.3 | `bafa4edaa6812fce10ae703ae450cc88ebbe1730` |
| 3.0.4 | `3fc635b988db2bd647b8578dfc1a85769913b708` |
| 0.0.0-ec7876d6c917dad516ba69bbfafc948b834bf0ab | `206b18c418434abc994bd40e021edcc334eee89b` |

## Am I affected?

- **CI/CD pipelines:** search workflow logs, dependency caches, lockfiles, SBOMs, and build provenance for the affected versions. Look for new Bun execution and unexpected GitHub API traffic during dependency installation.
- **Developer machines:** search workstations for the payload filename, the `trinnyyyy` temporary directories, and unexpected Bun executables created at install time.

## Recovery

- Stop builds and isolate systems that installed an affected version with lifecycle scripts enabled.
- From a **separate clean machine**, rotate npm, GitHub, cloud, CI/CD, SSH, signing, and deployment credentials the affected process could reach.
- Invalidate active sessions; review audit logs for unusual repository access, package publication, cloud API calls, or newly created credentials.
- Remove affected dependency caches and discard artifacts built on exposed runners.
- Pin to known-clean `0.5.3`, `1.6.2`, `2.2.0`, or `3.0.2` and rebuild from a clean environment with a reviewed lockfile.

## Why this matters

- **Root cause is workflow authorization, not a stolen token.** Unlike the Hades / Mini Shai-Hulud PyPI branch (stolen long-lived publisher token, see [pantheon-agents](pantheon-agents-pypi-trojanized-ghsa-93qj-5q5v-3c2h.md)), this compromise needed **no credential**: the workflow itself granted unauthenticated actors publish rights through `issue_comment` + `id-token: write`. Trusted Publishing (OIDC) is the mitigation *only if* the workflow authorizes the *actor*, not just the event.
- **Durable pattern:** release workflows that trigger on `issue_comment` (or PR events) and hold `id-token: write` for npm Trusted Publishing must verify the trigger author's repository role/membership before publishing. An exact-match comment body (`npm publish`) is not authentication.
- **Detection shape:** unexpected Bun downloads from GitHub release infrastructure during `npm install`, `gh auth token` / `git credential-manager` execution from install hooks, and `binding.gyp` → `os.system()` decode chains are the high-value hunt pivots.

## OX Security: the payload is a "Trinitite" Shai-Hulud variant
OX Security (August 29, 2026) reverse-engineered the `@7nohe/openapi-react-query-codegen` install-time payload and identified it as a **variant of the Shai-Hulud supply-chain malware family** that now brands itself **"Trinitite: Sponsored by Preview 2 Effects"** (also observed as `trinitite`). This is the same open-sourced codebase, string table, and behavioral signatures as the original **Shai-Hulud** and the June **Red Hat (`@redhat-cloud-services` / Miasma)** compromise — the actor re-shelled the public tooling under a new label.

Key OX findings that extend the StepSecurity capture:

- **New self-identification.** The payload's internal strings and version markers read as "Trinitite: Sponsored by Preview 2 Effects" (and `trinitite`), distinct from the earlier "Shai-Hulud" / "Miasma" markers but built on the same open-sourced engine.
- **New public keys.** The Trinitite builds ship a **different set of RSA public keys** than the original Shai-Hulud samples. OX notes this is deliberate: rotating the embedded public keys breaks the key-fingerprint that defenders and researchers previously used to correlate Shai-Hulud variants, so the new label + new keys make it harder to pin this wave to a single operator.
- **Same behavioral core.** Install-time credential theft, cloud/Kubernetes/GitHub secret collection, and exfiltration consistent with the Shai-Hulud tradecraft already documented on the [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) page and the [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md) page.
- **Timing context.** OX observed the first Trinitite-marker commit roughly **12 hours before** the malicious `@7nohe` publication, and the compromise landed **within 24 hours of the AFP/WAPF/FBI charging** of the two men alleged to be behind TeamPCP (see [TeamPCP charging page](teampcp-afp-wapf-fbi-charged-two-men-august-2026.md)).

**Attribution posture.** OX explicitly frames Trinitite as a **copycat / post-arrest wave** — an actor reusing the now-public Shai-Hulud codebase after TeamPCP's tooling leaked — **not** confirmed TeamPCP operator identity. The rotating public keys mean the marker chain that once tied Shai-Hulud variants to each other is broken. For defenders, the operationally important fact is the **lineage** (Shai-Hulud family → Trinitite rebrand), not the operator. Keep TeamPCP-operator attribution caveated unless a first-party operator statement or official source is produced; track Trinitite as **Shai-Hulud-lineage / copycat** on the [TeamPCP](../actors/teampcp.md) and [Mini Shai-Hulud](mini-shai-hulud-npm-pypi-worm-campaign.md) pages until stronger attribution emerges.

## Related pages

- [binding.gyp npm CI/CD worm (Miasma / Mini Shai-Hulud / Hades)](binding-gyp-npm-cicd-worm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Trojanized pantheon-agents (Hades / Mini Shai-Hulud, GHSA-93qj-5q5v-3c2h)](pantheon-agents-pypi-trojanized-ghsa-93qj-5q5v-3c2h.md)
- [npm install explicit trust controls (pattern)](../patterns/npm-install-explicit-trust-controls.md)

## Sources

- OX Security — "Shai-Hulud: Trinitite — Sponsored by Preview 2 Effects" (August 29, 2026), identifying the `@7nohe` install-time payload as a Shai-Hulud-lineage variant with new public keys (copycat / post-arrest framing, not confirmed TeamPCP operator): [https://www.ox.security/blog/shai-hulud-trinitite-sponsored-by-preview-2-effects](https://www.ox.security/blog/shai-hulud-trinitite-sponsored-by-preview-2-effects)
- StepSecurity — "@7nohe/openapi-react-query-codegen Compromised Through an Exposed npm Publishing Workflow" (August 28, 2026): [https://www.stepsecurity.io/blog/7nohe-openapi-react-query-codegen-compromised-npm-publishing-workflow](https://www.stepsecurity.io/blog/7nohe-openapi-react-query-codegen-compromised-npm-publishing-workflow)
- GitHub issue #217 (first report by Charlie Eriksen), PRs #215 / #216 (attacker-triggered workflow runs) — referenced by the StepSecurity post.
- npm package page for version 3.0.4 (registry tarball hashes and `latest`-tag state at capture).
