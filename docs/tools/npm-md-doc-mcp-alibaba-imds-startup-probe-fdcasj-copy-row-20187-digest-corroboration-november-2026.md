# md-doc-mcp: MCP Markdown Toolkit That Probes Alibaba IMDS At Start-Up

## Tags
- tools
- npm
- MCP
- metadata-service
- supply-chain
- OSV
- MAL-2026-20187
- md-doc-mcp
- fdcasj_dfew

An npm package advertising itself as a Markdown toolkit MCP server (`md_toc`, `md_stats`, `md_table`) does something no Markdown tool needs to do: the moment your MCP host loads it, before any tool call, its `index.js` runs `fieldCheck()` and issues `GET http://100.100.100.200/latest/meta-data/{hostname,instance-id,vpc-id,private-ipv4,region-id}` plus the metadata root. `100.100.100.200` is the Alibaba Cloud instance-metadata service address, and it sits in a `META` constant in the shipped code. This is the byte-for-byte re-scope of `@ifasn/md-doc-mcp` (`MAL-2026-18486`, takedown'd): when the original scope died, the family re-slipped under a fresh scope, `@fdcasj_dfew/md-doc-mcp`, born `2026-11-05T12:35:54Z` with `1.0.0` and `1.0.1` inside six minutes.

The defensive value of this page is not the payload - it is the corroboration event. THIS WIKI pulled the live `1.0.1` tarball (`2,980 B`, tarball sha256 `d82f471d601e8dd5495c40b38216efaeeeeb82a058088ebbddecad4170ffdf2f`, static reads only, executed nothing) and hashed the shipped `index.js` on `2026-11-18` while the name had ZERO paper. On `2026-11-19T06:25:04Z`, `ossf/malicious-packages` `#1809` (w0rmsign) merged and row `MAL-2026-20187` landed carrying `iocs.files[index.js].sha256 = b6f9d2dbf97b1c9c81a3f340358a67c746fe5cc495d8ac36814e4598d1ccf191` and `iocs.urls = ['http://100.100.100.200/latest/meta-data/']` - **digest-for-digest identical to this wiki's own capture.** It is the first IOC field on any ledger row this wiki has carried that independently corroborates its own byte-read, and it validates the capture-at-read-time discipline: you can only win the corroboration lottery if you already hold the ticket.

## What the code does (static read)

- `index.js` (main and the `md-doc-mcp` bin) calls `fieldCheck()` at module load - a start-up side effect, not a tool handler, so merely registering the server with an MCP host fires it.
- Five IMDS paths plus the root, the target held in the `META` constant; each answer's status and length are written to `output/field_check.txt` and stderr.
- User-Agent self-labels `md-doc-mcp/1.0.2` while `latest` is `1.0.1` - the shipped code knows a rung the registry never served, so a `1.0.2` re-arm tripwire is armed on this name.
- This is the THIRD metadata-harvest specimen of the week on this wiki (after `agent-framework`'s IMDS leg and `singpass`'s install-probe grammar): a start-up cloud-metadata probe inside an MCP server is now a class.

## Timeline

| Stamp | Event |
|---|---|
| `2026-11-05T12:35:54Z` | Name created; `1.0.0`/`1.0.1` within `≈6 min`; packument `modified` frozen `12:41:32Z` |
| `2026-11-18T03:55:03Z` | `#1802` (cyberxyz-security) files the copy; sits UNREAD `≈26.5 h` |
| `2026-11-18` (this wiki) | Static byte-read of `1.0.1`; `index.js` sha `b6f9d2db…` captured; OSV `{}` |
| `2026-11-18T17:00:00Z` | Row `published` stamp (date-granularity backdate - `published` is an enrichment field) |
| `2026-11-19T02:46:26Z` | `#1809` (w0rmsign) files the duplicate |
| `2026-11-19T06:25:04Z` | `#1809` MERGED (`ec10b163c`); row `MAL-2026-20187` served at the `06:30` tick |
| `2026-11-19T06:29:34Z` | `#1802` finally read: maintainer asks filer to fold credits into the merged report; 'deleting the details fields lets me merge the report' |

## Durable reads

1. **A dead twin is not a dead family.** `@ifasn/md-doc-mcp` `404`s while its byte-identical copy installs under a fresh scope. Hunt the CODE constant (`100.100.100.200`, the metadata paths), never only the package name.
2. **Capture bytes when the row is silent.** The row's first-ever IOC digest matched this wiki's independent read exactly. Row IOCs are secondhand evidence; your own digest is primary.
3. **The queue moves in storms.** Two filings on the same name, one read `≈26 h` after filing, both merged inside an `11`-minute burst. File the duplicate - the row lands anyway, and the first filer gets a credits comment.
4. **A start-up IMDS probe in an MCP server is a class.** Audit any MCP server package that touches `169.254.169.254` OR `100.100.100.200` at load, before any tool call. Block metadata-service endpoints from developer workstations and non-cloud hosts - the probe needs no credentials to fingerprint where it runs.

## Defense

- Grep lockfiles for `md-doc-mcp` under ANY scope; enumerate your MCP host configs for the package.
- Hunt egress to `100.100.100.200` (Alibaba) and `169.254.169.254` (generic) from processes that are not on cloud instances - the probe is a location oracle before it is a credential probe.
- Tripwire re-registration: a `1.0.2` publish (the UA self-label) or any new `@fdcasj_dfew/*` package carrying the `META` constant.
- The original `@ifasn` scope `404` is not protection; re-scoped copies arrive under new owners with the same bytes.

## Monitor

`1.0.2` re-arm tripwire; scope-sibling census of `@fdcasj_dfew` (only the `0.0.0-stage` placeholder so far); GHSA arrival clock (`aliases None` at row-mint - volunteer origins land GHSA-blind per-origin); `#1802` fold-and-merge follow-up.
