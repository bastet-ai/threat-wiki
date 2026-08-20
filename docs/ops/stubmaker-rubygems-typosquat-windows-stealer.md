# StubMaker: 16 typosquatted RubyGems packages deliver Windows stealer

## Summary
OpenSourceMalware (with researcher Paul "6mile" McCarty) tracked a typosquatting campaign it named **StubMaker**, published by RubyGems owner accounts `mod8rz41mje` ("Riley Miller") and `rbq95bwt6q` ("Alex Davis") between at least mid-August 2026. Sixteen gems — clumsy typosquats of popular Ruby dependencies such as `r18n`, `i18n`, `active_support`, `brakeman`-style tooling, and `builder` — all deliver the same **Windows-based information stealer**. Discovered August 15, 2026; the packages have been yanked from RubyGems. The durable finding is how the campaign **weaponized RubyGems' yank-and-reclaim behavior**: when a gem's versions are all yanked, its name becomes available for anyone to claim, letting the attacker re-publish malicious versions under previously "dead" package names.

## Tags
- ops
- operations
- StubMaker
- RubyGems
- typosquatting
- extconf.rb
- install-time execution
- information stealer
- Windows
- cryptocurrency wallet theft
- browser credential theft
- app-bound encryption
- Go stealer
- Rust loader
- package name reuse
- OpenSourceMalware
- supply chain

## Why this matters
- **RubyGems name reclaiming is an amplification vector.** Unlike npm or PyPI, once all versions of a gem are yanked the name opens up for a *new owner account* to claim. OpenSourceMalware's Jenn Gile: "When one of the malicious gems was yanked, the threat actor was able to spin up a new owner account and publish a new malicious version under the same package name. What should have been forever dead was revived to compromise more people."
- **The Author field is unvalidated plaintext.** The attacker assigned a different "Author" name per gem to look unrelated, though all came from the same owner account — a reminder that author metadata is not an integrity signal.
- **`extconf.rb` is Ruby's lifecycle hook.** Like npm's install hooks, `extconf.rb` runs automatically at gem install (used for native C/C++/Rust extension configuration). StubMaker abuses it as the execution trigger while the rest of the build fakes success.
- **The payload is cross-language and modern:** a 22 MB Rust loader fetched from a GitHub release launches a Go stealer ("wincfg") that includes an `abe_payload.dll` for Chromium-credential extraction that circumvents app-bound encryption (Chrome, Edge, Brave, Opera, Opera GX, Vivaldi, Yandex, Avast, AVG, CCleaner Browser).

## The sixteen packages
`ubnuler`, `ubnlder`, `ri18nr`, `reaker`, `rakier`, `orakw`, `joxn`, `ise18n`, `ioe18n`, `ie18u`, `iai8n`, `i1l8n`, `i18om`, `activesupmport`, `brumdler`, `brundlef`.

All are clumsy typos of popular gems (per McCarty, unlike the SEO-clever typosquats some other actors produce — here the goal was low-effort volume, and two names were reclaimed after yanking). `brumdler` and `brundlef` were originally published by a third account ("gemlewqqhu1", "Taylor Moore") before being reclaimed by the two campaign accounts — the concrete name-reclaiming instances.

## Attack chain
1. Victim installs a typosquatted gem (developer dependency or CI environment).
2. `extconf.rb` runs at install time — the real trigger. It is engineered to look like a no-op native-extension build: it generates a Makefile with empty `all`, `install`, and `clean` targets plus Unix/Windows stub scripts that merely return success, so the extension phase reports a clean build.
3. The hook fetches a **22 MB Rust-based loader** from a GitHub release (`github[.]com/bebraz1` — since gone).
4. The Rust loader launches the embedded **Go stealer** ("wincfg"), which on Windows deploys `abe_payload.dll` to extract Chromium-based browser credentials (circumventing app-bound encryption), extension data, browsing history, and payment card numbers.
5. The stealer also hunts cryptocurrency wallets and seed phrases, extracts Telegram Desktop data, gathers system information, and resolves the victim's public IP via `api.ipify[.]org`.
6. Stolen data is packaged as a **password-protected ZIP uploaded to Gofile**; the download link is sent to the actor's contact (`dresslee[.]com`) over **unencrypted HTTP**.

## Indicators and pivots
- RubyGems owner accounts: `mod8rz41mje`, `rbq95bwt6q` (profiles publicly viewable on rubygems.org).
- The sixteen package names above (yanked; names may be reclaimable).
- Third-party reclaim source account: `gemlewqqhu1` (original publisher of `brumdler` / `brundlef`).
- Loader host: `github[.]com/bebraz1` (inaccessible at publication).
- Exfil path: Gofile password-protected ZIP + HTTP link to `dresslee[.]com`.
- Behavior: `extconf.rb` install hook generating an empty-target Makefile while making a network fetch.

## Defender actions
- **Hunt for install-time network fetches** in Ruby build logs: `extconf.rb`/`bundle install` activity that contacts GitHub releases or unencrypted HTTP endpoints is anomalous for legitimate extension builds.
- **Treat yanked-then-reclaimed names as compromised history:** audit your lockfiles and CI caches for the sixteen names and for any gem whose publisher recently changed.
- **Verify publisher continuity**, not just gem name: a name with a new owner account after a yank is a red flag, regardless of "Author" field.
- **Isolate gem install steps** (network egress controls during `bundle install`) where feasible, and review the two reclaim names `brumdler`/`brundlef` specifically.
- Note the disclosure coincided with a separate cluster of **21 npm typosquats of Google-scoped CLI binary names** (same-day THN reporting); check both ecosystems if you build Ruby and Node.js tooling.

## Confidence and limits
- Packages are yanked and the loader host is gone; the campaign was disrupted early, which is why the durable lessons are the platform behavior (name reclaiming, unvalidated Author field) and the `extconf.rb` abuse pattern rather than active IOCs.
- No attribution to a named actor; "StubMaker" is OpenSourceMalware's moniker for the threat (named for the fake-build-toolchain move).
- Victim counts are not published.

## Related pages
- [SleeperGem RubyGems maintainer-account compromise](sleepergem-rubygems-maintainer-account-compromise.md)
- [BufferZoneCorp RubyGems / Go module CI poisoning](bufferzonecorp-ruby-go-ci-poisoning.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- OpenSourceMalware: [StubMaker — RubyGems Windows infostealer](https://opensourcemalware.com/blog/stubmaker-rubygems-windows-infostealer)
- The Hacker News: [16 Typosquatted RubyGems Packages Steal Browser Credentials and Crypto Wallets](https://thehackernews.com/2026/08/16-typosquatted-rubygems-packages-steal.html) — August 18, 2026
