# nodemon-sudo / tslint-conf runtime npm backdoor

## Summary
SafeDep's July 9, 2026 analysis describes `nodemon-sudo@3.1.16` as a malicious npm package that impersonated the popular `nodemon` process monitor while adding a single extra dependency, `tslint-conf@7.2.1`. SafeDep found that `nodemon-sudo` itself was a working, near-verbatim copy of real `nodemon`; the backdoor lived one dependency hop away in `tslint-conf`, a repackaged `pino` logger carrying runtime-triggered remote code execution.

The important defender lesson is that the campaign did **not** use install scripts and did **not** trigger on import. The payload executed only when application code called the exported logger/middleware function, which spawned a detached Node.js child process, fetched a second stage from a Pinata IPFS gateway, and evaluated it with Node's real `require` in scope.

## Tags
- ops
- supply chain
- npm
- JavaScript
- Node.js
- typosquatting
- runtime execution
- remote code execution
- credential theft
- dependency confusion
- IPFS
- dead drop
- SafeDep

## Why this matters
- `npm install`, `--ignore-scripts`, and install-hook monitoring do not expose this chain because neither package declares `preinstall`, `postinstall`, or `prepare`.
- Import-time sandboxes can also miss it: requiring `tslint-conf` is inert until the exported function is called, such as `app.use(require("tslint-conf")())`.
- Reviewing only the top-level package is insufficient. SafeDep reports that `nodemon-sudo` contained no malicious code and merely introduced the malicious dependency.
- The second stage is compiled with `new Function("require", s)` and invoked with the real `require`, giving fetched code full filesystem, environment, and module access in the running Node.js process context.
- SafeDep notes that `tslint-conf` declared dependencies such as `sqlite3` and `request`, consistent with browser-cookie / credential-database theft intent, though that is an inference from package metadata rather than observed second-stage code.

## Reported timeline and package set
- **July 7, 2026 ~20:28-20:33 UTC:** npm account `conodeeth` published `nodemon-sudo@3.1.16` and `tslint-conf@7.2.1`.
- **Earlier first pair:** SafeDep links the same backdoor scheme to `nodemon-node` and `ts-await`; npm had converted those to `0.0.1-security` holding packages.
- **July 9, 2026:** SafeDep published the analysis and reported `nodemon-sudo` and `tslint-conf` as live at time of writing.

SafeDep reports OSV advisory `MAL-2026-7022` for `tslint-conf`.

## Technical details
### Carrier package
`nodemon-sudo` copied real `nodemon` metadata and behavior closely enough to work as a process monitor. Its package metadata retained the real author string and `bin/nodemon.js` entry, but added suspicious runtime dependencies that real `nodemon` did not need, including `chai` and `tslint-conf`.

SafeDep's trace found that `nodemon-sudo` did not import `tslint-conf`; the package existed to place the malicious package in `node_modules` behind a trusted-looking top-level name.

### Payload host
`tslint-conf` masqueraded as a logger package. SafeDep found it was largely a repackaged copy of `pino`, but with three non-`pino` files:

- `index.js` — exports middleware / logger-looking functions and starts the hidden child process only when called.
- `lib/caller.js` — fetches and evaluates the second stage.
- `lib/const.js` — unused campaign metadata / dead-drop artifact linking the pair to earlier tooling.

When called, `index.js` used `spawn("node", [script, JSON.stringify(args)], { detached: true, stdio: "ignore" })` followed by `child.unref()`. That hides output and allows the parent process to exit while the child continues.

### Second-stage retrieval and evaluation
`lib/caller.js` fetched a JSON document from a Pinata IPFS gateway and read the `cookie` field. It then constructed and executed the fetched JavaScript with:

```javascript
const handler = new Function.constructor("require", s);
handler(require);
```

The script retried up to five times and saved/restored `console.log` around execution to reduce visible output. SafeDep also decoded local base64 strings that matched the request's dead-drop and header configuration.

## Indicators
### Packages and accounts
- `nodemon-sudo@3.1.16` — malicious top-level package
- `tslint-conf@7.2.1` — malicious payload host
- `nodemon-node` — earlier package pair, later `0.0.1-security`
- `ts-await` — earlier package pair, later `0.0.1-security`
- npm maintainer: `conodeeth`
- Forged author string reported by SafeDep: `Alexus111`
- Forged bugs URL: `jsonspack[.]com/issues`

### Network
- `hxxps://peach-eligible-penguin-917[.]mypinata[.]cloud/ipfs/`
- IPFS CID: `bafkreigjnxn5vnn34rc5r43ajwwkmk4akqpm4awmq5gdhakgszpeqiffsu`
- Dead drop: `hxxps://jsonkeeper[.]com/b/XRGF3`
- Orphaned / first-pair dead drop: `hxxps://jsonkeeper[.]com/b/4NAKK`
- Request header: `x-secret-key: _`

### Hashes reported by SafeDep
- `aa9b9847e4ffd894a19ec9712848651882b0195de5f4953eef9b47791adddabf` — `nodemon-sudo` artifact
- `d4b7add83e5c716b5e52082f713d71ec9d7bfd93e358d500d77c2393302dd004` — `tslint-conf` artifact
- `2956b023858d706a5e241cd28b845088e5f414c5f70bd5d8cb73cb427d081065` — `index.js`
- `541c35bd90653c9d7f93cdadb7f52c281d7a1375ffc9c0e118cf1d9df977dea7` — `lib/caller.js`
- `d10853dde92fdc48d8cb5505d89e0030fd35e1416a16a820fe5ec4aceef01c4f` — `lib/const.js`

## Defender heuristics
- Search package manifests, lockfiles, SBOMs, npm caches, private registries, CI runners, containers, and developer workstations for `nodemon-sudo`, `tslint-conf`, `nodemon-node`, or `ts-await`.
- Treat hosts that installed or executed `nodemon-sudo` or `tslint-conf` as compromised. Rotate npm, Git, cloud, CI/CD, SSH, API, browser-session, and application secrets reachable from the host or its environment.
- Hunt process telemetry for Node.js applications spawning detached child `node` processes from `node_modules/tslint-conf/lib/caller.js` with ignored stdio or no terminal ancestry.
- Hunt outbound HTTP/S requests to the Pinata gateway, the reported IPFS CID, and `jsonkeeper[.]com` dead drops, especially with header `x-secret-key: _`.
- Add dependency-graph rules for packages that clone a trusted project but add unused runtime dependencies, and for logger-looking packages that spawn hidden child processes or evaluate fetched strings with `Function` constructors.
- Extend malware scanning beyond install-time and import-time behavior. Exercise exported functions in suspicious packages inside an isolated sandbox when safe to do so.

## Related pages
- [wshu.net npm credential-stealer campaign](wshu-net-npm-credential-stealer-campaign.md)
- [Operation Muck and Load GitHub lure network](operation-muck-and-load-github-lure-network.md)
- [Lazarus-linked Rollup polyfill npm malware](lazarus-rollup-polyfill-npm-malware.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- SafeDep: [https://safedep.io/malicious-nodemon-sudo-tslint-conf-npm-backdoor](https://safedep.io/malicious-nodemon-sudo-tslint-conf-npm-backdoor)
