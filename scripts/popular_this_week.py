#!/usr/bin/env python3
"""Refresh the 'Popular this week' block on docs/index.md from Cloudflare zone analytics.

Reads the last 7 days of per-path request counts for every published page
(git ls-files docs/**) via the Cloudflare GraphQL API, then rewrites the
auto-generated block between the popular-this-week markers. Deterministic,
stdlib-only, no network writes beyond the one local file edit.

Token resolution order: $CLOUDFLARE_API_TOKEN, then the wrangler config
(~/.config/.wrangler/config/default.toml oauth_token). The token needs
zone Analytics: read. Nothing is uploaded or posted anywhere.

Usage: python3 scripts/popular_this_week.py [--dry-run] [--top N]
Exit 0 always (unless token/network hard-fails); prints changed=true/false.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import tomllib
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNT = "b6d1478423f0bb0c0477df387305e46b"
ZONE = "867b93404f8e123a874dbe3fbf5a0bc0"
START = "<!-- popular-this-week:auto -->"
END = "<!-- /popular-this-week:auto -->"
BATCH = 25
EXCLUDE_PREFIX = ("/blog", "/search/")


def token() -> str:
    t = os.environ.get("CLOUDFLARE_API_TOKEN")
    if t:
        return t.strip()
    cfg = os.path.expanduser("~/.config/.wrangler/config/default.toml")
    with open(cfg, "rb") as fh:
        return tomllib.load(fh)["oauth_token"]


def _gql_once(tok: str, query: str):
    body = json.dumps({"query": query, "variables": {"z": ZONE}}).encode()
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4/graphql",
        data=body,
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=40) as resp:
        out = json.load(resp)
    if out.get("errors"):
        raise RuntimeError(str(out["errors"])[:300])
    return out["data"]["viewer"]["zones"][0]


def gql(tok: str, query: str):
    """401 means the wrangler device-auth token expired in place; `wrangler
    whoami` refreshes it on disk, so re-read the config and retry once."""
    import urllib.error
    try:
        return _gql_once(tok, query)
    except urllib.error.HTTPError as e:
        if e.code != 401:
            raise
        subprocess.run(["npx", "wrangler", "whoami"], capture_output=True, timeout=120, cwd=REPO)
        return _gql_once(token(), query)


def page_paths():
    """Map tracked docs to their published URLs: docs/ops/foo.md -> /ops/foo/."""
    out = subprocess.run(
        ["git", "-C", REPO, "ls-files", "docs"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    paths = {}
    for f in out:
        if not f.endswith(".md"):
            continue
        rel = f[len("docs/"):]
        url = "/" + rel[: -len(".md")] + "/"
        if url == "/index/":
            continue
        paths[url] = os.path.join(REPO, f)
    return paths


def short_title(md_path: str) -> str:
    with open(md_path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        else:
            title = os.path.basename(md_path)[:-3]
    title = re.sub(r"`|\*\*", "", title)
    for cut in (" — ", " - ", "(", ":"):
        i = title.find(cut)
        if 40 < i < 110:
            title = title[:i].rstrip(" ,")
            break
    return title[:118]


def _cache_load():
    path = os.path.join(REPO, ".popular-cache.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:  # noqa: BLE001 - missing/corrupt cache just means no merge
        return {}


def _cache_save(counts):
    with open(os.path.join(REPO, ".popular-cache.json"), "w", encoding="utf-8") as fh:
        json.dump(counts, fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    tok = token()
    now = dt.datetime.now(dt.timezone.utc)
    geq = (now - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    leq = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    pages = page_paths()
    paths = [p for p in sorted(pages) if not any(p.startswith(x) for x in EXCLUDE_PREFIX)]
    cache = _cache_load()
    counts = {}
    batch_fail = 0
    for i in range(0, len(paths), BATCH):
        batch = paths[i:i + BATCH]
        inner = "".join(
            'a%d: httpRequestsAdaptiveGroups(limit:1, filter:{datetime_geq:"%s",'
            ' datetime_leq:"%s", clientRequestPath:"%s"}){count}' % (j, geq, leq, p)
            for j, p in enumerate(batch)
        )
        q = "query($z:String!){viewer{zones(filter:{zoneTag:$z}){%s}}}" % inner
        zone = None
        for attempt in range(3):
            try:
                zone = gql(tok, q)
                break
            except Exception as e:  # noqa: BLE001
                if "budget" in str(e) and attempt < 2:
                    time.sleep(90)  # rate-limiter budget refills on ~5-min windows
                    continue
                batch_fail += 1
                print("batch %d failed: %s" % (i, str(e)[:200]), file=sys.stderr)
                break
        if zone is None:
            for p in batch:  # fall back to the freshest cached number we have
                if p in cache:
                    counts[p] = cache[p]
            continue
        for j, p in enumerate(batch):
            g = zone.get("a%d" % j) or []
            counts[p] = g[0]["count"] if g else 0
        time.sleep(0.35)
    counts = {p: c for p, c in {**cache, **counts}.items() if p in pages}
    _cache_save(counts)

    measured = sum(counts.values())
    ranked = sorted(((c, p) for p, c in counts.items() if c > 0), reverse=True)
    picked = [(c, p) for c, p in ranked if p not in ("/", "/blog/")][: args.top]

    lines = [
        START,
        "_Auto-maintained from Cloudflare zone analytics, last 7 days ending %s UTC "
        "(%d of ~%d on-page requests attributable; %d of %d path batches ok)._"
        % (geq[:10], measured, len(paths), len(paths) - batch_fail * BATCH, len(paths)),
    ]
    for c, p in picked:
        lines.append("- [%s](%s) — %s reads" % (short_title(pages[p]), p, f"{c:,}"))
    lines.append(END)
    block = "\n".join(lines)

    idx = os.path.join(REPO, "docs", "index.md")
    with open(idx, encoding="utf-8") as fh:
        text = fh.read()
    if START in text and END in text:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    else:
        anchor = "## Recent entries"
        new = text.replace(anchor, "## Popular this week\n" + block + "\n\n" + anchor, 1)
    changed = new != text
    print("changed=%s measured=%d top=%d" % (changed, measured, len(picked)))
    if changed and not args.dry_run:
        with open(idx, "w", encoding="utf-8") as fh:
            fh.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
