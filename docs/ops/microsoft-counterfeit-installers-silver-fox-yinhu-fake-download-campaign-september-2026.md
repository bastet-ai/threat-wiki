# Counterfeit installers to system compromise: deceptive software-download campaign assessed as Silver Fox / Yinhu (Microsoft, Sep 1, 2026)

## Tags
- ops
- counterfeit software
- fake installers
- SEO poisoning
- social engineering
- Silver Fox
- Yinhu
- UTG-Q-1000
- Ghost
- Windows Installer
- msiexec
- scheduled task
- Alibaba OSS
- defense impairment
- Windows Update
- shadow copy
- Microsoft Security Research
- Microsoft Defender Experts

## Summary
On **September 1, 2026**, Microsoft Security Research and Microsoft Defender Experts (Parth Jomadkar) published "Counterfeit installers to system compromise: Tracking a deceptive software download campaign." It tracks an **active malware campaign that spoofs trusted-vendor download sites** to distribute **counterfeit installers** to users looking for popular software. Microsoft **assesses with moderate confidence that the activity is consistent with the publicly reported Silver Fox (aka Yinhu, 银狐) fake-software campaign** but **does not attribute it to a nation-state**. Confirmed compromises span **healthcare, manufacturing, gaming, technology, logistics, government, and higher education**, predominantly **China-based operations of multinationals and Chinese-speaking users**, consistent with Chinese-language lures and `.com.cn` / `.hl.cn` infrastructure.

The defining technical behavior: **the installer archive keeps the same filename while its hash changes on every download** — a direct, repeatedly observed signature of **server-side, per-request payload regeneration** (Microsoft captured two content-distinct copies of `app_setup.6653004.zip` written within ~69 seconds from the same URL).

## Why this matters
- This is the classic **Silver Fox / Yinhu commodity fake-software economy** at scale: high-fidelity vendor-clone download pages on look-alike domains, funneling to shared delivery infrastructure and a **regenerated, self-protecting implant** — the same campaign family Qianxin documented behind the MODBEACON Ghost/MODBEACON distributor (Operation Phnom Penh).
- Per-request payload regeneration defeats static-hash monitoring and any "same filename, trusted hash" assumptions; **detection must key on behavior and structure, not name or hash**.
- The implant actively **impairs defenses** (sweeping Microsoft Defender exclusion writes, shadow-copy deletion, Windows Update neutralization) and uses **disguised scheduled tasks in a ~60-second re-execution loop** plus **`msiexec -Embedding`** execution — a durable, recognizable post-exploitation shape.

## Attack chain
1. **Spoofed download page.** High-fidelity vendor clones with a prominent "Download now" button. Lure domains are `.com.cn` / `.hl.cn` / `.cn` and embed the brand name: `pc-razerzone[.]com[.]cn` (Razer Synapse), `app-microsoft-edge[.]com[.]cn`, `kaspersky-lab[.]hl[.]cn`, `sejda[.]hl[.]cn`, `translate-youdao[.]hl[.]cn`, `zh-diskgenius[.]com[.]cn`, `baidu-pan[.]com[.]cn`, `ocam-pc[.]com[.]cn`, `cn-drawio[.]com[.]cn`, `steelseries-cn[.]com[.]cn`, `gw-sogou[.]com[.]cn`, `calibre-ebook[.]com[.]cn`, `mindmoster[.]com[.]cn` (MindMaster typosquat), plus pc-codex / jinshan-cibapc / zh-tbtool / web-tbtool / zh-doubaosrf / ieway-cn.
2. **Regenerated installer archive.** Downloads come from a small set of dedicated delivery hosts — `www[.]gehie246[.]com/712down`, `yimxg25tiy[.]com/73inst`, `cc8ttkv35b[.]com/7qinst`, `n7b8t85zsg[.]com/ins711` — and a suspected attacker-controlled **Alibaba Cloud OSS** bucket. Same-named archive families (`app_setup.*`, `zinst.*`, `zintall.*`, `intsoft.*`, `innstll.*`) differ in content across downloads while the URL stays constant.
3. **Wrapper → randomized stage-one.** The archive contains a generated-named wrapper (`a_instapp83353001.exe`, `ainst8663586104.exe`); executing it drops and launches a **stage-one payload at a randomized path** under world-writable/system locations. The **same SHA-256 content appears under many randomized names**: stage-one `676a2a7b94ca…`, later-stage `6d6ba2bc9ad4…` (masquerading as "Philips Speech Driver Client Configuration" with a fabricated "TODO: <Product name>" resource — confirmed forged version metadata), persistent `c6100166e2d3…`, persistent/networking `f33d160d…`, supporting DLL `e4fe2dee…`, networking `c4100ad3…`. Observed chain: `msedge.exe` writes the archive → `7zFM.exe`/`360zip.exe`/`WinRAR.exe` extracts → wrapper → randomized stage-one (e.g. `C:\Users\Public\sE94yD\aLcUaw.exe`).
4. **TrueUpdate-abusing persistent stage.** A payload in `C:\ProgramData\<random>\` carries the version metadata of the **Indigo Rose TrueUpdate Client** (`tu_rt.exe`, v3.8.0.0) and behaves like it: writes `_ir_tu2_temp_*` artifacts, is **launched repeatedly by the Task Scheduler service (`svchost.exe -k netsvcs -s Schedule`)**, and connects over TLS to the **Alibaba OSS bucket** to fetch further payloads — a legitimate update mechanism repurposed for delivery.
5. **Defense impairment + recovery inhibition.** PowerShell/cmd write **sweeping Microsoft Defender path/registry exclusions** (via SYSTEM scheduled tasks), run **`vssadmin delete shadows`**, and **disable/rename Windows Update services** (`wuauserv`, `UsoSvc`, `uhssvc`, `WaaSMedicSvc`; "NoAutoUpdate" patterns) — the classic pre-ransomware posture.
6. **Parallel delivery vector.** `msiexec.exe -Embedding` launches a randomized payload from `C:\Users\Public\` (tracked via `Global\MSI0000`).
7. **C2.** Callbacks to a **C2 IP:port set** and **six-character `.net` C2 domains**; a **~60-second re-execution loop** via disguised scheduled tasks from user-writable directories.

## Indicators of Compromise (IOCs)
**Payload SHA-256 set:** `676a2a7b94ca2f8ec76352ee656e4d075bb342bd7ad6efbc7c19c060001eace7` (stage-one), `6d6ba2bc9ad414837826f7278bc3e0116f1aeda02d0c2284ed65819f5d9180a8` (later-stage), `c4100ad39d8db98f063feb6c3b6c8e9a9f9d9bf25a1e0233f43b058ff8a7dbdf` (networking), `1bd3662d784840e410d2d3c0a1040277f7f549089447359f01e05c2559cb1f17` (persistent), `c6100166e2d3b40388980f7674712ef39e937ac04925ca5d370415399ed73faf` (TrueUpdate loader), `f33d160d757e4b39019fdef21cf90cafb501b800ca0d4039366bc30856e3d81b` (persistent/networking), `e4fe2dee8f0bb132fa15fc686d1f93df39530a2d3a8d3a1f3a605a057c04e7b3` (supporting DLL).

**C2 IPs:** `202.95.14.237`, `47.239.232.245`, `161.248.87.157`, `103.156.25.35`, `103.183.3.162`, `43.99.100.248`, `47.239.175.163`, `47.86.205.97`, `47.243.218.255` (ports `5090, 7031, 7032, 7088, 7089, 7090, 8050, 28290, 28300`). **C2 domains:** `iualef.net`, `euioxu.net`, `czijbh.net`, `wfmwsj.net`, `tbdqxq.net`, `oijfwe.net`.

**Delivery domains:** `gehie246.com`, `yimxg25tiy.com`, `cc8ttkv35b.com`, `n7b8t85zsg.com`, `bxfh.tzcdq.cn`, `tmsq.tzcdq.cn`, `mebx78e02.com`, `qwjre1487.com`; download paths `/712down`, `/73inst`, `/7qinst`, `/ins711`.

**Infrastructure grouping:** six look-alike domains in **AS132839** (four netblocks, three registered countries, shared nameserver pair) + two in **AS8796** (single /21, different nameservers) + one CDN-fronted — two consistent commercial hosting/DNS procurement channels. **ASN/nameserver are hunting pivots, not blocklist entries** (shared commercial resellers with unrelated tenancy).

## Durable detection / defensive heuristics
- **Same filename, changing hash per download** from a dedicated delivery host = server-side payload regeneration; block/hunt the delivery URL families and the randomized-drop pattern `C:\(Users\Public|ProgramData|Program Files (x86))\<4-10 alnum>\<4-10 alnum>.exe` written by `msiexec`/`explorer`/`svchost`/`cmd`/archivers.
- **`msiexec -Embedding`** with `Global\MSI0000` from `C:\Users\Public\`; `svchost.exe` executing from non-`System32` paths; forged version resources (a "TODO: <Product name>" ProductName is a confirmed fabrication tell); TrueUpdate `_ir_tu2_temp_*` artifacts on non-Indigo-Rose hosts.
- **Recovery-inhibition triad:** `vssadmin delete shadows` + Defender exclusion writes (`Add-MpPreference -ExclusionPath`, SYSTEM scheduled task exclusions) + Windows Update service disable/rename — on the same host, this is pre-ransomware posture; escalate and contain.
- **~60-second scheduled-task re-execution loop** from user-writable directories; TLS callbacks to a six-character `.net` C2 domain set or the listed IP:port set.
- **Hunt the ASN/nameserver channel** (AS132839 / AS8796 pairings) for additional look-alike domains; treat SmartScreen bypass + counterfeit-vendor landing + archiver-parented execution as the high-signal combination.

## Attribution note
Microsoft's **moderate-confidence** assessment ties this to the **Silver Fox / Yinhu** fake-software campaign family (commodity, financially motivated; not nation-state). It is the same campaign family seen in Qianxin's Operation Phnom Penh (UTG-Q-1000 Ghost distributor, MODBEACON) — correlate infrastructure and lure pages across reports, but do not assume a single operator across the whole family.

## Related pages
- [Operation Phnom Penh: MODBEACON delivery by a Silver Fox / UTG-Q-1000 Ghost distributor (Qianxin, Jul 2026)](modbeacon-operation-phnom-penh.md)
- [MODBEACON tool page](../tools/modbeacon.md)
- [TA4922: Chinese-speaking cybercriminal cluster with Silver Fox / Void Arachne tooling overlap (Proofpoint)](../actors/ta4922.md)
- [Node.js runtime as a malware-delivery channel (Symantec, Sep 4)](../patterns/nodejs-runtime-malware-delivery-symantec-september-2026.md)

## Sources
- Microsoft Security Research / Defender Experts — "Counterfeit installers to system compromise: Tracking a deceptive software download campaign" (Parth Jomadkar; published 2026-09-01): [https://www.microsoft.com/en-us/security/blog/2026-09-01/counterfeit-installers-to-system-compromise-tracking-a-deceptive-software-download-campaign/](https://www.microsoft.com/en-us/security/blog/2026-09-01/counterfeit-installers-to-system-compromise-tracking-a-deceptive-software-download-campaign/)
