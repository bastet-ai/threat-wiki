# RubyGems solana-keypair: extconf.rb credential stealer at gem install

## Tags
- ops
- Ruby
- RubyGems
- solana-keypair
- MAL-2026-20019
- extconf.rb
- build-time-execution
- credential-theft
- webhook.site
- amazon-inspector
- supply-chain
- crypto-wallets

## Summary

On November 16, 2026 the OSV ledger minted **`MAL-2026-20019 solana-keypair` (RubyGems)** — a gem whose only "native extension" is an `ext/extconf.rb` that is not a build script at all: at `gem install` time it reads the installer's **Solana keypairs, npm/netrc/git credentials, Ethereum keystores, and `.env` files**, base64-encodes them with host reconnaissance, and POSTs them to a hardcoded **`webhook.site` collector**, then writes a **no-op Makefile** so the install reports success. The gem was live and downloadable (`205` downloads) at first ledger read; `0` GitHub advisories named it (`affects=` census, control `express` `6`). This wiki pulled and statically read the gem bytes (sha256 `a854717e71bf443e0f3f34ebfeee6f032f10a034a286231ccee2d6a8f2161383`, `5,120 B`) and **executed nothing** — every behavioral claim below is read from the shipped source.

**The durable read: installing a gem is compiling it.** `extensions:` in gem metadata means arbitrary Ruby runs at install time, before any library code is loaded, before any `require`, with the installing user's full home directory. A package can contain zero C, zero compiler invocations, and still be a complete stealer — the build step is the payload.

## The clocks (this wiki, verified at read, Nov 16 ~22:3x-22:5x UTC)

| Clock | Stamp | Lane |
|---|---|---|
| Gem `0.1.0` born | `2026-11-15T09:08:52.366Z` | rubygems.org versions API |
| `MAL-2026-20019` published | `2026-11-16T21:14:02Z` | OSV `GET /v1/vulns/` |
| `modified` batch tick | `2026-11-16T21:45:03.4xxZ` | OSV row (the batcher's clock) |
| ossf mirror present | `200` at first probe | `raw.githubusercontent.com/ossf/malicious-packages/.../rubygems/solana-keypair/MAL-2026-20019.json` |
| Gem still downloadable | `200` `5,120 B` | `rubygems.org/downloads/solana-keypair-0.1.0.gem` |
| Exfil sink | `200` on GET | `https://webhook.site/cd8ac1c3-79b3-46ed-a9ad-2fd7b7d6772b` |
| GitHub `affects=solana-keypair` | `0` rows (control `express` `6`) | global `/advisories` route |
| KEV grep | `0` (`2026.11.13`/`1,781`) | CISA KEV JSON |

Row shape at first read: `aliases None`, `severity None`, `affected` enumerates exactly `['0.1.0']`, origin `amazon-inspector` (`a298aceb…`). This is the ledger catching a **live, installed-in-the-wild** gem rather than a quarantined corpse: `205` downloads against a name born the previous morning. The author string is `rzc-build` with a disposable email (`rzcops7k2@tempmail.lol`), the summary reads "Lightweight Solana keypair helpers", and the name deliberately rides next to the legitimate `solana` gem (which answers `200` — verified, the namespace is real and populated).

## The artifact, read statically (NEVER executed)

This wiki downloaded the `.gem` (sha256 above, matching the registry's published `sha` field — the byte claim is grounded) and unpacked `data.tar.gz`. Contents: `lib/solana_keypair.rb` (a stub) and `ext/extconf.rb`. The metadata declares `extensions: - ext/extconf.rb`, which is the switch that makes `gem install` execute it.

What `extconf.rb` does, from the shipped source:

- **Collects credentials from disk**: `~/.config/solana/id.json` and every `~/.config/solana/*.json`, `~/.npmrc`, `~/.netrc`, `~/.git-credentials`, every file under `~/.ethereum/keystore/`, and `.env` files walked up **six directory levels** from the current working directory. Each file is base64-encoded, truncated at `262,144 B`.
- **Collects secrets from the environment**: `PRIVATE_KEY`, `MNEMONIC`, `SECRET_KEY`, `WALLET_PRIVATE_KEY`, `SOLANA_PRIVATE_KEY`, `ETH_PRIVATE_KEY`, `NPM_TOKEN`.
- **Collects host reconnaissance**: `Socket.gethostname`, `Etc.getlogin`, `Process.uid`, `Dir.pwd`, timestamp.
- **Exfiltrates**: the whole JSON blob is base64'd and POSTed to `https://webhook.site/cd8ac1c3-79b3-46ed-a9ad-2fd7b7d6772b` with a 5 s connect / 10 s read timeout, wrapped in `rescue nil` so failure is silent.
- **Conceals**: it then writes a `Makefile` whose `all`, `install`, and `clean` targets are each `@true`. There is no C/C++/Rust source in the tarball — the "native extension" exists solely to run the steal and to make `gem install` print success.

The collector URL sits on **webhook.site**, the same public request-inspection service this ledger already carries as an exfil sink for the PyPI `usdm-minting-client` lure (302nd). Service reuse is a hunt lead, not kinship — no attribution is asserted here.

## Why it matters

1. **`extensions:` is a code-execution declaration hiding in build metadata.** The same trust that lets a legitimate gem compile a native parser runs an attacker's Ruby before anything else touches the machine. Anything you `gem install` (or `bundle install`) from a name you did not write executes with your user's home directory at time zero — no `require` ever needed.
2. **The no-op Makefile is the fingerprint.** A gem declaring a native extension while shipping no source files (`*.c`, `*.rs`, `*.cpp`) and a `Makefile` that does nothing is not broken packaging; it is the concealment mechanism itself. `gem spec NAME | grep -A5 extensions` is a one-command triage probe.
3. **Webhook-style sinks are disposable but observable.** The `webhook.site` path is rotatable at will, so blocklists on the URL age out instantly; the durable block is egress + provenance (allowlisted gem sources, checksum pinning, build sandboxes for `extconf` execution).
4. **The catch lane beat every scanner on this row.** At first read GitHub `affects=` was `0` while the OSV row and its ossf mirror were already live — Dependabot-blind on a name still installing at `205` downloads. Triage the OSV feed, not only the advisory index.

## Defensive checklist

- **Rotate first if affected**: any host that ran `gem install solana-keypair` (or `bundle` on a `Gemfile.lock` naming it) should treat Solana keypairs, npm tokens, netrc/git credentials, Ethereum keystores, and every reachable `.env` as exposed — rotate from a different machine.
- Grep lockfiles and internal Gemfiles for `solana-keypair` (and audit any gem whose name mimics blockchain tooling with a `extensions:` entry and no source files).
- Prefer `bundle config set build.<gem> ...`-free default builds; when a genuine native gem is needed, read its `extconf.rb` before first install (it is short and static; the read is cheap).
- Pin private gem mirrors; treat rubygems.org direct as an install-time code source.
- Watch the re-registration tripwire: this row's `0.1.0` is unyanked as of read — if a `0.1.1` appears, re-dial before installing anything under this name.

## Monitor forward

- Sink `webhook.site/cd8ac1c3-…` liveness per-read (the `ec3e3cb9-…` usdm sibling has oscillated `200`/`429` across sweeps — quote status with the read-time).
- Gem yank clock: does rubygems remove `0.1.0`; does the name re-register (the resurrection grammar the ledger already documents).
- Row enrichment: `aliases`/`severity` still `None` — does a GHSA ever mint for this row, or does it join the never-join class.
