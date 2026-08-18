# npm bin-entry dependency confusion: Google-scoped bin name harvesting

## Summary
On August 12, 2026, an actor published **21 npm packages** that did not squat package names — they squatted **CLI binary names** exposed by Google's scoped packages through the `bin` field of `package.json`. Every scoped package that declares a `bin` entry creates an unscoped binary name that anyone can register on the public registry, and none of the standard dependency-confusion mitigations (scoped publishing, registry allowlists, lockfile pinning) cover that gap. Each package carried a minimal `postinstall` beacon that collected a system fingerprint (hostname, platform, architecture, Node version) and POSTed it to a per-package C2 subdomain. All 21 packages were unpublished within about an hour; artifacts were recovered from npmmirror.com. SafeDep's August 14 writeup documents the technique, the 21 package names, the publisher, the C2 infrastructure, and the defensive gap.

## Tags
- patterns
- supply-chain
- npm
- dependency confusion
- bin entry
- postinstall
- binary squatting
- npx confusion
- Google
- build pipeline
- CI-CD
- SafeDep
- unclaimed names
- registry metadata

## Why this matters
- **The structural gap.** When `@angular/service-worker` declares a `bin` entry `ngsw-config`, that binary name cannot include the scope and lives in public npm metadata. If an internal build system references `ngsw-config` as a bare dependency instead of consuming it through `@angular/service-worker`, the public package wins. The attack surface shifts from individual developers running `npx` to **automated build pipelines** resolving dependencies.
- **Prior art did not target this surface.** alxndrsn documented npm binary confusion in August 2024 (npm rejected the report as "consistent with documented expectations"), and Roni Carta and Adnan Khan formalized "npx confusion" at DEF CON 33 in August 2025; Aikido found 128 unclaimed package names referenced in documentation with 121,000 downloads over seven months. Prior work focused on `npx` execution hijacking where a developer types the binary name; this campaign targets `npm install` via postinstall hooks.
- **None of the mitigations cover bin names.** Scoped packages, unscoped placeholder claims, `.npmrc` registry allowlists, and lockfile pinning all govern package names. Binary names are not claimed because nobody thinks to reserve them.

## The technique
The pipeline, as reconstructed from the campaign's own `source.txt` breadcrumbs:

1. Query Google-affiliated scoped packages for their `bin` entries.
2. Strip the scope; check which binary names have no matching standalone package on the public registry.
3. Register the unclaimed names; publish packages with a `postinstall` beacon and a `source.txt` file pointing at the legitimate Google repository (commit-SHA permalinks, not branch references) documenting where each squatted name was found.

Eighteen of the 21 names matched confirmed `bin` entries on public npm packages (`@angular/localize` → `localize-extract` / `localize-translate`; `google-ads-api-report-fetcher` → `gaarf`, `gaarf-bq`, `gaarf-node`, `gaarf-node-bq`; `chromecast-webdriver-server` → `chromecast-webdriver-cli`; scoped packages `@google/gemini-cli-a2a-server`, `@google/chrome-enterprise-premium-mcp`, `@googlemaps/code-assist-mcp`, `@googlemaps/github-policy-bot`, `@bazel/bazelisk`; even the Polymer project `koa-karma-proxy` → `karma-proxy`). Three names — `broadcast-graphics-mcp`, `upload-to-gcp`, `tfjs-inference` — had no matching public bin entry; their `source.txt` files point at GitHub repositories or Sourcegraph searches, indicating the researcher found them in `package.json` files inside Google repositories that were never published to npm (e.g. `@tensorflow/tfjs-inference` exists in the tensorflow/tfjs monorepo with `private: false` set, but was never published).

## The 21 packages
| Ecosystem | Package | Version |
|---|---|---|
| npm | `bazelisk` | 1.0.0 |
| npm | `broadcast-graphics-mcp` | 1.0.0 |
| npm | `chrome-enterprise-premium-mcp` | 1.0.0 |
| npm | `chromecast-webdriver-cli` | 1.0.0 |
| npm | `chromeos-webdriver-cli` | 1.0.0 |
| npm | `code-assist-mcp` | 1.0.0 |
| npm | `gaarf` | 3.2.1 |
| npm | `gaarf-bq` | 1.0.0 |
| npm | `gaarf-node` | 1.0.0 |
| npm | `gaarf-node-bq` | 1.0.0 |
| npm | `gemini-cli-a2a-server` | 1.0.0 |
| npm | `github-policy-bot` | 1.0.0 |
| npm | `karma-proxy` | 1.0.0 |
| npm | `localize-extract` | 1.0.0 |
| npm | `localize-translate` | 1.0.0 |
| npm | `ngsw-config` | 1.0.0 |
| npm | `tfjs-inference` | 1.0.0 |
| npm | `tizen-webdriver-cli` | 1.0.0 |
| npm | `upload-to-gcp` | 3.2.1 |
| npm | `wct-st` | 1.0.0 |
| npm | `xbox-one-webdriver-cli` | 1.0.0 |

Two version details: the legitimate `google-ads-api-report-fetcher` has 3.2.0 and 3.3.0 but never published 3.2.1 — the researcher fabricated a plausible patch version — and `upload-to-gcp` 3.2.1 version-matched a real release line.

## Campaign timeline
| Wave | Time (UTC) | Packages | Version | Notes |
|---|---|---|---|---|
| 1 | 2026-08-12 13:23 | `gaarf`, `upload-to-gcp` | 3.2.1 | Version-matched real release lines |
| 2 | 2026-08-12 16:57–16:59 | remaining 19 | 1.0.0 | Bulk publish in 70 seconds |
| Unpublish | 2026-08-12 17:22:18–17:22:50 | all 21 | — | Alphabetical order, 32-second window |

The four-hour gap between wave 1 and wave 2 suggests the researcher waited for callbacks before committing the full list; the 32-second alphabetical unpublish window indicates an automated script.

## Indicators of compromise
- **npm publisher:** `rootdaddy-msrc` (ayyitscompton@gmail[.]com), author field `r00tdaddy`
- **C2 domain:** `*.instances.poc.jchunt[.]top` (wildcard DNS, resolves to 152.53.138.110)
- **C2 apex:** `jchunt[.]top` (behind Cloudflare at 104.21.61.226 / 172.67.216.7)
- **Payload:** `postinstall.js` POSTs a system fingerprint (hostname, platform, architecture, Node version) — no credentials, tokens, files, or environment variables
- **POST path:** `/<package-name>` (one path per package; 21 unique C2 subdomains, one per package)
- **Registry status:** all 21 removed from npm within hours of publication; artifacts recovered from npmmirror.com

## Defensive gap and mitigations
Standard dependency-confusion mitigations do not cover bin entry names:

| Mitigation | Covers package names | Covers bin names |
|---|---|---|
| Scoped packages (`@org/pkg`) | Yes | No (bin names cannot include scopes) |
| Claim unscoped placeholders | Yes (if names known) | No (nobody claims bin names) |
| Registry allowlists (`.npmrc`) | Yes | No |
| Lockfile pinning | Yes | No |

Organizations that publish scoped packages should audit the `bin` entries those packages expose and register the unscoped names as placeholder packages on the public registry. A scope-wide query produces the list:

```bash
# List all bin entries exposed by packages in an npm scope
for pkg in $(npm search --json "@myorg" 2>/dev/null | jq -r '.[].name'); do
  curl -s "https://registry.npmjs.org/$pkg/latest" | jq -r '.bin // empty | keys[]'
done | sort -u
```

Any name in that list that does not exist as a standalone npm package is a dependency-confusion vector.

## Assessment limits
- The beacon collects no credentials; the technique is a proof-of-concept pattern, not a credential-stealer. No victim data was reported to have been exfiltrated.
- SafeDep published the writeup on August 14, 2026; attribution is limited to the npm publisher account and C2 infrastructure — no operator identity is claimed.
- The packages targeted Google-affiliated names; the same technique applies to any publisher whose scoped packages expose `bin` entries.

## Related pages
- [oob.moika.tech dependency-confusion environment stealer](../ops/oob-moika-dependency-confusion-env-stealer.md)
- [Marketfront / TQM-MFE dependency-confusion stealer campaign](../ops/marketfront-tqm-mfe-dependency-confusion-stealer.md)
- [npm install explicit-trust controls](npm-install-explicit-trust-controls.md)

## Sources
- SafeDep: [npm Bin Entry Harvesting: A Dependency Confusion Blind Spot](https://safedep.io/google-dep-confusion-bin-harvesting) — August 14, 2026
- alxndrsn: Squatting npm for Remote Code Execution (August 2024)
- Roni Carta and Adnan Khan: "npx confusion," DEF CON 33 (August 2025)
- Alex Birsan: Dependency Confusion (February 2021)
