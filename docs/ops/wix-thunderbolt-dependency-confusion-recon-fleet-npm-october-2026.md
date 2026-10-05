# Wix Thunderbolt dependency-confusion recon fleet — 27 npm names, one `thunderboltRegistry.js`, require-time host beacon to three collectors (Oct 4 wave)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- dependency-confusion
- Wix
- Thunderbolt
- parastorage
- host-reconnaissance
- DNS-exfiltration
- Burp-Collaborator
- webhook-site
- require-time-beacon
- Amazon-Inspector
- OSV

## Summary

A single Amazon-Inspector ingest batch (OSV `MAL-2026-17473`–`MAL-2026-17530`, published 2026-10-04 23:12–23:29 UTC) contains a **27-name npm fleet purpose-built to look like modules from Wix's internal Thunderbolt build namespace**. Every member ships the same payload file — `thunderboltRegistry.js` — whose load-time IIFE runs host reconnaissance (`id`, `whoami`, `uname -a`, `ifconfig`/`ip addr`, `cat /etc/hosts`, some also `hostname`, `pwd`, `cat /etc/resolv.conf`, `env | head -50`) and exfiltrates the output to one of three shared collectors. The public names resolve ONLY for installers configured to fall back to the public registry when an internal `thunderboltRegistry`-style module fails to resolve — a textbook dependency-confusion qualification shape, and the first on-wiki fleet explicitly dressed for ONE named company's internal namespace at 27-name scale.

This wiki verified at capture (Oct 4 ~23:55–00:20 UTC sweep): **every sampled member of the fleet is STILL LIVE and installable on npm (27/27 sampled `registry.npmjs.org` 200)**, zero GHSA mirrors across the family at check.

## The shape (from the OSV detail texts + this wiki's liveness checks)

- **Costume:** package names advertise CSS/a11y utilities (`css-*-polyfill`, `css-*-shim`, `a11y-*`, `tiny-*`, `rgx33-*`, `popover-anchor-polyfill`, `dom-focus-sentinel`, `wcag-color-a11y-helpers`…). `index.js` is typically an empty stub or a Proxy of no-op functions.
- **Namespace bait:** the shipped module exports factories under Wix-internal registry names — `thunderboltRegistry`, `siteAssetsRegistry`, `documentManagementRegistry`, `editorRegistry`, `corvidRegistry`, and similar — and bundles a `registry-manifest.min.json` mapping those names to `static.parastorage.com/unpkg/...` URLs (Wix's public CDN), reinforcing the internal-module illusion for resolver humans and machines alike.
- **Payload:** a load-time IIFE in `thunderboltRegistry.js` runs the recon command set via `child_process.execSync` and ships each result (plus hostname, Node version, platform, pid) to a hardcoded collector. Several variants base64- or `String.fromCharCode`-encode every sensitive string (module/method names, commands, destination host, OAST subdomain) to defeat static inspection; several walk `require.cache` deleting `thunderboltRegistry` entries so the beacon **re-fires on every `require`**, and use `node:child_process` / `new module.constructor().require('child_process')` fallbacks to obtain the exec primitive. One variant self-labels `beacon=rce-poc`, another `beacon=poc15` — the POC labeling is either cover or a qualification-program tell; do not read it as authorization evidence.
- **Activation:** no install hook needed — the beacon fires at `require()` time, so even a resolve-and-import in a CI dependency tree triggers it.

## Shared collectors (durable cluster keys — the subdomain/token survives every name)

| Collector | Role | This wiki's probe (Oct 4 ~23:55Z) |
|---|---|---|
| `dxpoc.gt.tc/callback.php[/<32-hex-token>]` | primary HTTP beacon (plain HTTP AND HTTPS variants; tokens `bb8968d0f67000433bf7005dd5ad2d1f`, `ef9ea0e191006f3cc6670720c99c26f3`) | DNS resolves `185.27.134.102`; HTTP 000 at check (listener down, domain/DNS armed) |
| `webhook.site/0492a36c-4d7b-408a-865c-226db25987ba` | secondary HTTP collector (shared token across ≥4 names) | 429 (rate-limited — endpoint live) |
| `davdpb8lhot13kgmnhp0863x9g83mpswq.oast.live` | DNS-exfil collector (Burp Collaborator class, `dns.resolve` on per-command subdomains) | wildcard resolves `178.128.210.172` = ARMED |

The `.oast.live`/`.oastify.com` subdomain string is the same class of durable cluster key this wiki recorded on the UOL-afiliados and @uh-platform fleets: hunt resolver logs for the subdomain itself — it survives renames and version bumps, and you do not need to know the label grammar.

## The 27 names (OSV IDs, all amazon-inspector origin, all 1.0.0, all published 2026-10-04T23:12–23:29Z in one ingest window)

`css-a11y-contrast-utils` (17475), `css-anchor-pos-fallback` (17476), `css-env-function-shim` (17477), `css-field-sizing-polyfill` (17478), `css-gap-decorations-polyfill` (17479), `css-interop-observer-polyfill` (17480), `css-light-dark-polyfill` (17481), `css-logical-prop-shim` (17482), `css-reading-flow-polyfill` (17483), `css-relative-color-util` (17484), `css-scroll-anchor-polyfill` (17485), `css-scroll-state-polyfill` (17486), `css-snap-target-polyfill` (17487), `css-starting-style-polyfill` (17488), `focus-visible-polyfill-lite` (17491), `a11y-tabindex-manager` (17501), `dom-focus-sentinel` (17503), `minimal-a11y-contrast-check` (17514), `popover-anchor-polyfill` (17517), `postcss-gap-fallback-util` (17518), `rgx33-css-grid-utils` (17520), `rgx33-flex-layout-core` (17521), `tiny-css-token-parser` (17525), `tiny-dom-focus-trap` (17526), `tiny-focusgroup-helper` (17527), `tiny-viewport-unit-calc` (17528), `wcag-color-a11y-helpers` (17530).

Registry disposition at check: **27/27 sampled STILL 200 installable** — no npm action despite advisories being <1 h old; downloads are near-zero (`css-a11y-contrast-utils` 0/wk, `css-env-function-shim` 170/wk), consistent with a targeting play rather than a volume spray.

## Why it matters (durable reads)

1. **Company-namespaced dependency confusion at fleet scale.** Prior on-wiki confusion squats borrowed generic internal names (`@uh-platform`, `@uol-afiliados`, Telegram-chat fleet). This is the first fleet that dresses itself INSIDE one company's real internal module grammar — down to a manifest aliasing that company's real CDN asset URLs. Defensive read: the squat no longer needs your scope to be forgotten; it needs your resolver's public-registry fallback to exist.
2. **Recon-before-arming shape.** Every artifact observed is host-reconnaissance beaconing, nothing more — the qualification/engagement-testing pattern this wiki has repeatedly seen precede a payload wave at beaconed orgs (Telegram chat fleet precedent). The fleet's live-and-unremoved state means the next push can ride the same names.
3. **Advisory ≠ enforcement, again.** 27 advisory-backed names, all installable <1 h post-advisory, zero GHSA mirrors = Dependabot blind; npm-side action was pending at check.

## Hunt guidance

- **npm/org:** lockfile + resolver-log grep for the 27 names above; any package shipping `thunderboltRegistry.js`, a `registry-manifest.min.json` referencing `parastorage.com`, or exporting `corvidRegistry`/`siteAssetsRegistry` without being Wix-published.
- **DNS/HTTP logs:** queries to `*.davdpb8lhot13kgmnhp0863x9g83mpswq.oast.live`; requests to `dxpoc.gt.tc/callback.php*`; to `webhook.site/0492a36c-4d7b-408a-865c-226db25987ba`. Any resolver hit = an internal module name resolved to the public registry somewhere in your build estate — that is the finding, independent of payload.
- **Config:** for any org with internal namespaces resolving to npm, enforce scope-allowlists / internal-registry-only resolution for unscoped-and-internal-looking names; audit `.npmrc`/`.yarnrc` fallback ordering.

## <a id="october-5-second-wave"></a>October 5 follow-up (seventy-eighth sweep, ~05:15–05:35 UTC): the fleet GREW while its first wave was still unadvised-enforced — a SECOND 13-name wave in OSV batch `MAL-2026-17531`–`17566`, four hours after the first wave's advisories, with fresh collector tokens

The OSV stream moved again +36 (contiguous `17531`–`17566`, all npm/amazon-inspector, published 03:12–03:38Z) and **thirteen of the thirty-six are new Wix-Thunderbolt-costumed names** — the fleet has been built out from 27 to 40 names across two waves, the second publishing ~4 h AFTER the first wave's 23:12–23:29Z advisories. Second-wave names and records: `aria-live-region-helper` (17546), `css-at-scope-polyfill` (17547), `css-ayucyz-polyfill` (17548), `css-display-reading-polyfill` (17549), `css-dwsawd-polyfill` (17550), `css-gvqmfn-polyfill` (17551), `css-hgwctv-polyfill` (17552), `css-ikomdq-polyfill` (17553), `css-mpmdds-polyfill` (17554), `css-nbanqq-polyfill` (17555), `css-ogojwh-polyfill` (17556), `css-svqggc-polyfill` (17557), `css-txedrf-polyfill` (17558) — all 1.0.0, published 03:35–03:37Z in a two-minute window (scripted).

**New collector strings (hunt these, not the names):** the `dxpoc.gt.tc` endpoint now carries per-program path tokens — `/callback.php/ef9ea0e191006f3cc6670720c99c26f3` (aria-live-region-helper) and `/callback.php/bb8968d0f67000433bf7005dd5ad2d1f` SHARED across ≥6 names (css-ayucyz, css-dwsawd, css-gvqmfn, css-hgwctv, css-mpmdds, css-ogojwh, css-svqggc, css-txedrf) = a path-level cluster key that survives any name churn; `css-ikomdq-polyfill` uses the bare `/callback.php/` and adds `require.cache` purging so the beacon RE-FIRES on every require; `css-display-reading-polyfill` is the wave's webhook.site member (`webhook.site/5e52603d-f802-4a6f-b91b-43c3a5b45b6b`, verified 200 LIVE at check) shipped as `payload.bundle.min.js` and explicitly declares itself as the loader entry in shipped Wix thunderbolt manifest JSONs. `css-nbanqq`/`css-svqggc` carry the `registry-manifest.min.json` → `parastorage.com` aliasing again; `css-gvqmfn` ships the Proxy no-op stub set. One variant self-labels `beacon=rce-poc` again — same POC-shaped cover tell as wave one.

**This wiki's disposition checks (~05:20Z):** sampled second-wave names `aria-live-region-helper`, `css-at-scope-polyfill`, `css-ikomdq-polyfill` ALL 200 installable minutes-to-hours post-advisory (downloads still near-zero: css-at-scope 0/wk = qualification, not spray); `dxpoc.gt.tc` still resolves `185.27.134.102` with HTTP still down (DNS armed); webhook.site `5e52603d` 200. Zero GHSA mirrors for any of the 36 new records; GHSA global feed top unchanged Oct-2 23:18:12Z.

**Durable read updated:** a 27-name fleet that was STILL ENTIRELY INSTALLABLE when this wiki reported it grew by 13 more names four hours later — the operator treats the advisory wave as a build trigger, the same advisories-as-build-trigger loop previously measured on the @baanx and starlette-healthchecks names, now at fleet scale. The `bb8968d0…` path token is the single best hunt string on this campaign.

## Monitor

- npm takedown of the 27 + 13 second-wave names (all re-registerable if delete-only — check for security-holder blocks on next sweep).
- A THIRD wave in the same grammar (two waves ~4 h apart = the campaign is in build-out phase).
- GHSA mirrors for any member; second-wave names reusing the same three collectors (the collector strings are the hunt, not the names).
- Wix public confirmation/response (none at check); any payload escalation riding live names (require-time code is re-fetchable only via re-publish — watch version bumps).
- `dxpoc.gt.tc` listener returning at `185.27.134.102` (currently DNS-armed, HTTP-down); the `.oast.live` collector resolves regardless.

## Sources

- OSV `MAL-2026-17473`–`MAL-2026-17530` amazon-inspector detail texts (all 58 wave records read in full by this wiki Oct 4 ~23:45–00:10 UTC; family subset listed above).
- This wiki: npm registry liveness (27/27 sample), npm downloads API pulls, DNS/HTTP probes of all three collectors, Oct 4–5 ~23:55–00:20 UTC.

## Related pages

- [DirtyBlanket npm→AUR→SSH Wayback-fed worm](dirtyblanket-npm-express-clone-linux-worm-wayback-codeberg-aur-chaos-tor-safedep-september-2026.md) — same `hellscripter` actor's earlier Wayback/Codeberg rail (now re-armed on gitflic.ru, see below)
- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — the require-time DNS-beacon pattern this fleet reuses with a company-namespaced costume
