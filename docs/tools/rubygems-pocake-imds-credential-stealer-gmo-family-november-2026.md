# RubyGems pocake trio: payment-name gems stealing AWS IAM creds via IMDS at install and require

## Tags
- tools
- Ruby
- RubyGems
- pocake
- gmo-payment
- gmo-payment-carrier
- aws_sdk_wrapper
- MAL-2026-20210
- MAL-2026-20211
- MAL-2026-20212
- extconf.rb
- build-time-execution
- require-time-execution
- IMDS
- AWS-IAM-credential-theft
- webhook.site
- supply-chain
- ci-cd

## Summary

On November 19, 2026 at the `09:15` OSV batch tick the ledger minted **three contiguous RubyGems rows - `MAL-2026-20210 aws_sdk_wrapper`, `MAL-2026-20211 gmo-payment`, `MAL-2026-20212 gmo-payment-carrier` - and all three are the same kit wearing three payment-brand costumes.** THIS WIKI pulled all three `.gem` archives (`5,120 B` each) and statically read every shipped byte (nothing executed): the `lib/runtime_payload.rb` is **byte-identical across the trio (sha256 `3722a762ad6ab7bc694d3e19e806bd221d1530d5b1cbe8a2a92825d6d4ba278c`)** and the `ext/*/extconf.rb` build hook is **byte-identical too (sha256 `45855ecfdd3577b4a1b5ef0d0bc78ce74931051925ae30aa6b87b56c554a9b66`)**. One operator, one build, three names.

**The kit is an AWS credential thief, not an environment thief.** Both hooks (build-time `extconf.rb` via the gemspec `extensions:` entry, require-time `lib/runtime_payload.rb` via `require_relative` from the gem's entry point) run the same routine:

1. **IMDS harvest, both protocols:** GETs `http://169.254.169.254/latest/api/token` with the `X-aws-ec2-metadata-token-ttl-seconds: 21600` header (IMDSv2), then reads `/latest/meta-data/iam/security-credentials/` and the role's credential doc - **falling back to un-tokened IMDSv1 when the v2 token or role list comes back empty**. The stolen IAM role name and credential body are exfiltrated as `stage=iam` / `stage=runtime_iam` captures.
2. **Host fingerprint:** `hostname`, `whoami`, `uname -a`, `pwd`, and the IMDS local-ipv4 (`stage=extconf` / `stage=runtime_require`).
3. **ECS metadata:** if `ECS_CONTAINER_METADATA_URI_V4`/`_URI` is set, its body is exfiltrated (`stage=ecs`).
4. **Database secrets by regex:** every env var matching `/DATABASE|DB_|MYSQL|AURORA|POSTGRES|REDIS|RDS/i` is joined and exfiltrated (`stage=db` / `stage=runtime_db`).
5. **Success forgery:** `extconf.rb` ends with `File.write('Makefile', "all:\ninstall:\nclean:\n")` - the same no-op-Makefile tell as `rechargeapps` (`MAL-2026-20137`) and `solana-keypair` (`MAL-2026-20019`): the native-extension lane makes the build-step execution automatic, then the stub Makefile makes the install print success with nothing compiled.

**Exfil transport is a GET query string, not a POST body:** the payload opens `#{CANARY}?#{URI.encode_www_form(params)}` - everything (hostnames, ECS metadata, DB env lines, **and raw IAM credential JSON**) rides URL query parameters to `https://webhook.site/4b2354a7-67fd-4641-92ac-e18bac8c09e8`, overridable via a `CANARY_URL` env var (the same operator-OOB pattern as `rechargeapps`' `CW_OOB`). Chinese-language author comments ride in both files (`运行时 payload：当 note 服务 require 此 gem 时执行 (IMDSv1+v2 双协议)` - "runtime payload: executes when the note service requires this gem"), a target-profile clue pointing at some "note" service.

**Registry state at read (~10:3x-11:0x UTC Nov 19):** all three gems API `200`, `yanked: false`, all `version 0.0.99`, all born `2026-11-19T09:03:14-09:03:29Z` (**three names inside 15 seconds**), all `downloads ≈100` each (`99`/`102`/`104`) **within one hour of birth** - the implausible-flat ~100 pattern this ledger has seen on inflated counters. Publisher identity on all three: `authors: pocake`, `email: info@pieceofcake.co.jp`, `homepage: github.com/pocake/<gem>` - **and all three GitHub repos answer `200` today**, a live public front behind the kit. The names are payment-brand costumes: `gmo` (real gem, `0.5.9`) / `gmo_payment` / `gmo_payment_gem` exist on RubyGems, and the hyphenated `gmo-payment`/`gmo-payment-carrier` squat the vocabulary of the Japanese PSP "GMO Payment" while `aws_sdk_wrapper` glues AWS-SDK trust words (no genuine `aws-sdk-wrapper` exists; `aws-sdk 3.3.0` by Amazon Web Services does).

**THE SINK IS A PUBLIC DASHBOARD AND IT IS LIVE: THIS WIKI GETted the webhook.site token (GET-only, no interaction) and the operator's victim feed answered JSON `total: 35`, of which 11 are staged captures.** The capture anatomy reads like a live test-and-deploy sequence (field names and hostnames quoted, secret values never):
- `09:04:14Z` and `09:04:32Z`, UA `curl/8.5.0`: `stage=extconf&hostname=test-host&whoami=test-user` = **the operator's own self-test inside 60 s of birth**.
- `09:21:12-09:21:45Z`, UA `Ruby`: THREE victim installs - full `stage=extconf` captures (`hostname`, `whoami`, `uname`, `pwd`, `ts`) each followed by a `stage=db` follow-up whose env list came back empty. Distinct victim hostnames: **`fv-az1319-984`, `fv-az1359-335`, `fv-az1507-172` - the `fv-az*` naming is GitHub-hosted Actions runners. The victims are CI, again.**
- `09:23:31-09:24:00Z`, UA `Ruby`: TWO `stage=runtime_require` captures with `stage=runtime_db` follows = **the second (require-time) hook verified firing in the wild, on the same CI hosts.**
- **No `stage=iam` / `stage=ecs` capture had landed at read** - consistent with GitHub runners blocking IMDS (nothing to steal there yet), NOT with the credential leg being dead code: on any EC2/ECS host that installs these gems, the role credentials ride out in a GET query string.
- The remaining `total` is scanner weather (`Mozilla/compatible`, `Twitterbot`, `GPTBot`, `SkypeUriPreview` hits on the token URL).

**The clock story: paper raced the gem and LOST anyway.** All three names born `09:03:14-09:03:29Z`; operator self-test `09:04:14Z`; **rows `published 09:08:19-09:08:39Z` = `≈5 m` after birth (the fastest birth-to-paper this ledger has measured)**; `amazon-inspector` `import_time 09:13:05Z`; rows served at the `09:15` tick; first victims installing at `09:21Z` = **the advisories were live 13 minutes before the first victim pulled the gem, and the gems are STILL `200`/un-yanked with ~100 downloads each.** Advisory coverage does not gate installs - the registry does, and the registry kept serving.

**Row quality note (mirror of the rechargeapps law):** all three rows carry `aliases None` / `iocs None` / `severity None` - the structured IOC fields are blank - while the amazon-inspector `details` prose spells the whole scheme, **naming the webhook.site endpoint and the IMDS role-credential theft explicitly**. The row knows the sink in prose and not in fields; defenders scanning only `iocs` stay blind to what the row itself already says.

**Durable reads:**
- **`extensions:` is a build-time execution primitive.** Any gem declaring a native extension gets arbitrary Ruby executed at `gem install` by every RubyGems client - audit lockfiles for gems whose `extensions` point at `extconf.rb` with `net/http`/`open-uri` requires and no compilation targets. `gem install --ignore-scripts` stops the extconf hook; **the `runtime_payload.rb` require-time hook still fires on every `require`** (same half-shield law as `rechargeapps`).
- **Byte-identical payloads across brand costumes are one operator by construction** - hash the payload file, not the gem name; the trio's `3722a762…` `runtime_payload.rb` is the cluster key for every future `pocake` sibling.
- **IMDSv1-fallback code in a supply-chain payload is a doubled attack surface:** the kit tries the hardened v2 token path first and silently downgrades - blocking IMDSv1 on your fleet kills this leg; route 169.254.169.254 egress like you route metadata endpoints in any untrusted-code path.
- **A `200` on a webhook.site token URL is a free victim census for defenders** (GET the token page, quote totals with read-time, never interact).
- **Paper speed proves detection, not protection:** `≈5 min` birth-to-advisory with installs continuing anyway; enforcement is yank/blocklist action, not row mint.

**Defender actions:** grep lockfiles/`Gemfile.lock` for `aws_sdk_wrapper`, `gmo-payment`, `gmo-payment-carrier` (and any gem shipping a `lib/runtime_payload.rb`); on any host that installed them: rotate every IAM role reachable, every DB secret matching the payload's regex, and treat ECS task metadata as disclosed; hunt egress logs for `webhook.site/4b2354a7-67fd-4641-92ac-e18bac8c09e8` (field names in the query string: `stage`, `role`, `creds`, `env`, `meta`); check GH Actions inventories for installs (`fv-az*` victims prove the vector is already CI-native); block IMDSv1 where policy allows.

## Timeline as measured (all reads by THIS WIKI, artifacts pulled and statically read, none executed)

| Time (UTC) | Event |
|---|---|
| `2026-11-19 09:03:14-09:03:29Z` | `gmo-payment`, `gmo-payment-carrier`, `aws_sdk_wrapper` `0.0.99` born inside 15 s (gems API `version_created_at`) |
| `09:04:14Z` / `09:04:32Z` | Operator self-test hits the sink (`test` param, then `stage=extconf&hostname=test-host`, UA `curl/8.5.0`) |
| `09:08:19-09:08:39Z` | OSV rows `20210`/`20211`/`20212` `published` = `≈5 m` post-birth |
| `09:13:05Z` | `amazon-inspector` `import_time` (all three, same second) |
| `09:15:03Z` | Rows served at the `09:15` batcher tick (`modified`) |
| `09:21:12-09:21:45Z` | Three CI-victim `stage=extconf` installs (`fv-az1319-984`, `fv-az1359-335`, `fv-az1507-172`), UA `Ruby` |
| `09:23:31-09:24:00Z` | Two `stage=runtime_require` captures = require-time hook live in the wild |
| `~10:3x-11:0xZ` | THIS WIKI read: gems API `200` × 3, `yanked:false`, downloads `102`/`99`/`104`; tarballs `200`/`5,120 B`; sink `total 35` (11 staged); `github.com/pocake/*` `200` × 3; KEV greps `0` for all three names + `pocake` |

## Indicators (public, ON-LANE)
- RubyGems: `aws_sdk_wrapper 0.0.99`, `gmo-payment 0.0.99`, `gmo-payment-carrier 0.0.99` (publisher `pocake`, `info@pieceofcake.co.jp`)
- Gem sha256 (registry-listed, re-verified on pull): `7b1ca113f18bb8b3…` / `2ea2b445f3826fab…` / `66bfdd78ea5da36a…`
- Payload (shared): `lib/runtime_payload.rb` sha256 `3722a762ad6ab7bc694d3e19e806bd221d1530d5b1cbe8a2a92825d6d4ba278c`; `ext/*/extconf.rb` sha256 `45855ecfdd3577b4a1b5ef0d0bc78ce74931051925ae30aa6b87b56c554a9b66`
- Sink: `https://webhook.site/4b2354a7-67fd-4641-92ac-e18bac8c09e8` (GET-query exfil; `CANARY_URL` override)
- IMDS: `169.254.169.254` (`/latest/api/token`, `/latest/meta-data/iam/security-credentials/`, `/latest/meta-data/local-ipv4`)
- OSV: `MAL-2026-20210`, `MAL-2026-20211`, `MAL-2026-20212` (origin `amazon-inspector`, `aliases None`, `iocs None`)
- GitHub front: `github.com/pocake/aws_sdk_wrapper`, `/gmo-payment`, `/gmo-payment-carrier` (`200` at read)

## Same-family context on this wiki
- `rechargeapps` (`MAL-2026-20137`): the sibling RubyGems double-hook env stealer of the same week - same extconf+require pattern, same no-op Makefile, same webhook.site sink class, POST transport. This trio is the **IAM-specialized** variant: narrower env regex, deeper cloud-credential harvest, GET-query transport.
- `solana-keypair` (`MAL-2026-20019`) and `vuln-app` (`MAL-2026-20103`): the extconf/mkrf build-step-stealer class; RubyGems build-time theft is now a five-specimen month, four of them webhook.site sightings = service reuse, not attribution.

## Monitor forward
- Does the trio get yanked, or join the `rechargeapps`-style permanent-installable set (watch `yanked`, download climb past the ~100 flat).
- Sink `total` climb (GET-only, quote with read-time); **any `stage=iam` capture = an EC2/ECS victim with live role creds stolen - that capture shape is the alarm**, re-read without interacting.
- `pocake` sibling sweep: new `0.0.99`-shape payment/infra names by the same publisher grammar; `runtime_payload.rb` sha `3722a762…` as the grep key.
- Rows `20210`-`20212` `aliases`/`iocs` enrichment clocks (GHSA-blind at mint, vendor-origin law).
- `github.com/pocake/*` repo state (live front; takedown would flip these `404`/renamed).
- Any second house writing up the trio (feed lane is silent so far: NO feed coverage at the 338th).
