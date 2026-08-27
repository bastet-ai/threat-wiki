# Trojanized pantheon-agents 0.6.1 / 0.6.2 on PyPI (GHSA-93qj-5q5v-3c2h)

## Tags
- ops
- operations
- supply-chain
- PyPI
- Hades
- Mini Shai-Hulud
- Miasma
- Shai-Hulud
- credential-theft
- .pth
- Bun
- maintainer-account-compromise
- trusted-publishing

## Summary

On August 26, 2026, a GitHub Security Advisory **GHSA-93qj-5q5v-3c2h** ("Trojanized pantheon-agents 0.6.1 and 0.6.2 on PyPI ship a credential stealer (supply-chain account compromise)", severity **critical**, CWE-506 / CWE-522) was published, formalizing first-party confirmation that the PyPI account publishing **`pantheon-agents`** was compromised in the **June 2026 "Hades" PyPI supply-chain attack** (Mini Shai-Hulud / Miasma lineage).

The attacker used a stolen, long-lived PyPI API token to upload trojanized releases **`pantheon-agents` 0.6.1 and 0.6.2 directly to PyPI**. The advisory states that **only the PyPI artifacts are affected**: the GitHub source repository, its git tags, and all other distribution channels are clean. `first_patched_version` is recorded as **0.6.4**.

This page captures the durable operational and remediation detail from the first-party advisory and its linkage to the broader Hades campaign tracked on the [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md) page.

## Key facts from the advisory
- **Affected:** `pantheon-agents` **0.6.1** and **0.6.2** on PyPI (vulnerable range `>= 0.6.1, <= 0.6.2`).
- **Not affected:** installs from the GitHub source, version **0.6.0 and earlier**, and the maintainer's Desktop / Online apps.
- **Root cause:** a stolen, long-lived PyPI API token used to upload the malicious wheels — a **maintainer / publisher-account compromise**, not a flaw in the package's code.
- **Distribution:** PyPI distribution is suspended; it will resume after account recovery and migration to **PyPI Trusted Publishing (OIDC)**.

## Attack behavior
- The malicious wheels ship a **`*-setup.pth`** file that executes on **Python startup** (via the `site` module's handling of executable `import`-prefixed lines), not only when the package is imported.
- On startup the `.pth` hook downloads the **Bun** JavaScript runtime and runs an obfuscated credential stealer (**`_index.js`**).
- The stealer harvests and exfiltrates credentials reachable from the host: environment variables, `~/.pypirc`, `~/.npmrc`, cloud credentials (`~/.aws`, etc.), SSH keys, and API tokens.
- This `.pth` + Bun + `_index.js` shape matches the Hades PyPI delivery branch already documented in the June 7 Socket report (see the [Hades PyPI wave](binding-gyp-npm-cicd-worm.md#june-7-hades-pypi-wheel-wave) section).

## Indicators to hunt
- An unexpected **`*-setup.pth`** file in `site-packages` of any environment that had `pantheon-agents` 0.6.1/0.6.2 installed.
- A stray **`_index.js`** in the user's home directory.
- A **Bun runtime** under `~/.bun` that was not intentionally installed.

## Impact assessment
Anyone who `pip install`ed `pantheon-agents` 0.6.1 or 0.6.2 should **assume every credential present on that machine has been exfiltrated** — environment variables, registry tokens, cloud credentials, and SSH keys are all in scope.

## Remediation
1. **Do not install `pantheon-agents` from PyPI** until distribution resumes.
2. If 0.6.1 or 0.6.2 was installed:
   - Run `pip uninstall pantheon-agents` immediately and check for the IoCs above.
   - **Rotate every credential** that was present on that machine (API keys, tokens, SSH keys, cloud credentials) — but only after containing the host and removing the persistence artifacts.
3. Install only from the clean GitHub source:
   ```
   pip install "git+https://github.com/aristoteleo/PantheonOS.git"
   ```

## Campaign context
The PyPI account that publishes `pantheon-agents` was hit in the same **Hades / Mini Shai-Hulud / Miasma** wave that Socket and StepSecurity documented in June 2026. The advisory names the **sibling projects by the same maintainer** that were hit by the same campaign and are being remediated separately: **`executor-engine`, `funcdesc`, `cmd2func`, `pantheon-toolsets`, `coolbox`, `ufish`, `magique`, and `executor-http`**. `pantheon-agents` 0.6.1 and 0.6.2 were already in Socket's June 7 Hades PyPI affected list (alongside `pantheon-toolsets@0.5.5`/`0.5.6`).

### Status
The PyPI account is **suspended** and the malicious token has been **disabled**. The move to **Trusted Publishing (OIDC)** is the durable control: it ties publish rights to the verified GitHub repository's OIDC identity rather than a long-lived API token that can be stolen and reused, directly addressing the root cause of this compromise.

## Why this matters
- A **first-party GHSA** turns a vendor-tracked supply-chain incident into a citable, durable advisory with a defined affected range, a clean-source fallback, and a specific root cause (stolen long-lived PyPI token).
- It confirms the **Hades lineage's PyPI delivery shape** (`.pth` startup hook → Bun → `_index.js` stealer) in the wild with a named, remediated victim, strengthening hunts for that exact artifact shape across other affected packages.
- The **Trusted Publishing (OIDC)** migration is the reusable lesson: replace long-lived publisher API tokens with OIDC-bound publishing so a stolen token cannot be used to republish poisoned versions.
- Because the compromise is at the **publisher-account** level, sibling packages by the same maintainer are in scope even if the originally installed package is clean — defenders should audit every package the affected maintainer publishes.

## Related pages
- [binding.gyp npm CI/CD worm (Miasma / Mini Shai-Hulud / Hades)](binding-gyp-npm-cicd-worm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [LiteLLM compromise](litellm-compromise.md)

## Sources
- GitHub Security Advisory GHSA-93qj-5q5v-3c2h (published 2026-08-26, severity critical, CWE-506 / CWE-522): [https://github.com/advisories/GHSA-93qj-5q5v-3c2h](https://github.com/advisories/GHSA-93qj-5q5v-3c2h)
- Repository advisory (aristoteleo/PantheonOS): [https://github.com/aristoteleo/PantheonOS/security/advisories/GHSA-93qj-5q5v-3c2h](https://github.com/aristoteleo/PantheonOS/security/advisories/GHSA-93qj-5q5v-3c2h)
- Socket Hades PyPI wave analysis (June 7): [https://socket.dev/blog/shai-hulud-descends-to-hades-miasma-pypi-wave](https://socket.dev/blog/shai-hulud-descends-to-hades-miasma-pypi-wave)
