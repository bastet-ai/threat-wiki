# `string-utils-assistant` (npm), a two-year-old string helper with a raw-TCP reverse shell

## Summary
On 2026-11-20 the queue filer `w0rmsign` filed `ossf/malicious-packages#1819` (`05:22:52Z`, open) against `string-utils-assistant 1.0.0` (npm): a package this wiki verified as **born `2024-11-05T07:15:11Z`, single rung, single maintainer `acd125` (`Yeshen10@outlook.com`), zero OSV rows and zero GHSAs at read** - two years of silent installation paper under a five-function string-helper costume (`toUpperCase`/`toLowerCase`/`reverseString`/`trimString`/`capitalize`, all real). This wiki pulled the `1,976 B` tarball (sha256 `b036c02739a9873a2cad1959ee28dcd6e86f8b1b73f322168543f5eee5078fcf`, shasum `37895b47…`, executed nothing) and statically read every byte of its 4 files: `package.json` carries `postinstall: node postinstall.js`; `postinstall.js` spawns `node index.js` **detached with stdio ignored and unref'd** (survives the installer); `index.js` (`4,799 B`) opens a raw `net.Socket` to **`47.251.102.182:8057`** (Alibaba Cloud US-range class at read, grep `0` wiki-wide before this sweep), beacons `SYSTEM_TYPE:<platform>` on connect, then runs **every line the server sends through `child_process.exec` and writes the output back** - a full command-execution reverse shell - and additionally implements `FILE_START:<path>` / `FILE_END` framed **file uploads written to any server-chosen path** (a second-stage dropper channel). On close/error it reconnects on a randomized `60,000`-`300,000 ms` loop. One curiosity: a dormant time-logic `collectUserInfo()` that fires a one-time OS/arch beacon only on `2024-11-30 10:00` local - expired two years ago, the fingerprint of a campaign skeleton repurposed rather than rewritten. The filing reports a sandboxed install DID connect to `47.251.102.182`, so the listener was live at the reporter's read-time; this wiki made no outbound contact.

**Why the ledger carries it:** this is the ledger's cleanest specimen of the **old-name shell**: not a husk, not a squat, not a security-placeholder costume - a genuine, maintained-looking, never-advisored utility that has shipped the SAME byte since November 2024 while every name-keyed feed stayed blind for two years. It landed `≈17 min` after the `#1817` merge that finally papered the `@fedfub` worm, same filer, same hour = the volunteer catch lane is currently out-running the vendor lanes on shells the registries never ate.

## Defender actions
- Grep lockfiles and SBOMs for `string-utils-assistant` (exact name; the five helper functions it exports exist in dozens of packages, the NAME is the indicator here, not the API).
- Hunt egress/proxy logs for TCP to `47.251.102.182:8057`; any established session is a compromise, not a failed dependency - the protocol speaks `SYSTEM_TYPE:<os>` in cleartext, so a packet capture names the family instantly.
- The `postinstall` fires on plain `npm install`: `--ignore-scripts` blocks the spawn, and any host that installed it should be treated as having had an outbound exec channel and an inbound file-write channel to one IP for its full install lifetime.
- Ledger-side tripwires armed: `1.0.1`+ new-rung publish, `#1819` merge + row mint (watch OSV name-query), `47.251.102.182` reappearance in any other name, `acd125` scope census for sibling names.

## Evidence (this wiki's reads, 2026-11-20 ~06:4x-07:0x UTC)
- Packument `200`: `created 2024-11-05T07:15:11.637Z`, `time` carries only `1.0.0` + `modified 2024-11-05T07:15:12.189Z` - no publish has touched the name in ~`715 d`; maintainer `acd125`, `latest 1.0.0`.
- Tarball `200`: `string-utils-assistant-1.0.0.tgz` `1,976 B`, sha256 `b036c02739a9873a2cad1959ee28dcd6e86f8b1b73f322168543f5eee5078fcf`; files `index.js` / `postinstall.js` / `package.json` / `README.MD`.
- `index.js` verbatim constants: `const SERVER_HOST = '47.251.102.182'; const SERVER_PORT = 8057;`; `client.on('data')` splits lines, `FILE_START:`/`FILE_END` write a `fs.createWriteStream` at the server-chosen path, everything else goes to `exec(command)` with output written back; `reconnectToServer()` uses `Math.floor(Math.random() * (300000 - 60000 + 1)) + 60000`.
- OSV `POST /v1/query` for the exact name returns `{}` (express-style control verified same route); GitHub security-advisory search `0`; KEV `2026.11.18`/`1,786` grep `0` for the name and for `47.251.102.182`.
- `#1819` (w0rmsign) `created 2026-11-20T05:22:52Z`, `updated_at == created_at`, `merged None` = merge clock not started at read; filing body names the same host/port and confirms a sandboxed connection.

## Tags
- tools
- npm
- supply chain attack
- reverse shell
- raw TCP
- postinstall hook
- detached process
- exec backdoor
- file upload backdoor
- old name
- zero advisory
- w0rmsign
- 47.251.102.182
- Alibaba Cloud egress
- time bomb expired
- catch lane

## Related
- [algamil7x stream, 346th sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-20-three-hundred-and-forty-sixth-sweep)
