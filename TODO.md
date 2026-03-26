# TODO

Internal profiling backlog for future `Groups`, `People`, and `Ops` coverage.

This file is a working queue, not a set of claims. Inclusion here means "worth evaluating for durable public coverage," not "already verified enough to publish." The goal is to keep the backlog aligned with the public taxonomy: named groups, publicly supported people pages, and specific operations or campaign writeups.

## Triage rules

- Prefer subjects that recur across multiple operations, ecosystems, or vendor reports.
- Prefer groups, people, and ops with strong public sourcing, indictments, advisories, or maintainer records.
- When writing an `Ops` page, check this list for companion `Groups` and `People` pages that should be added in the same pass.
- Remove or trim items once the repo has durable coverage.

## Groups

### State-linked and espionage

- [ ] APT29 / Cozy Bear / Midnight Blizzard
- [ ] APT28 / Fancy Bear / Forest Blizzard
- [ ] Sandworm / Seashell Blizzard / Voodoo Bear
- [ ] Turla
- [ ] Gamaredon / Shuckworm / Aqua Blizzard
- [ ] UNC1151 / Ghostwriter
- [ ] Dragonfly / Energetic Bear / Crouching Yeti
- [ ] Lazarus Group
- [ ] Andariel / Onyx Sleet
- [ ] BlueNoroff / Sapphire Sleet
- [ ] Kimsuky / Emerald Sleet / TA427
- [ ] ScarCruft / APT37 / Reaper
- [ ] APT41 / Winnti / Brass Typhoon
- [ ] APT31 / Zirconium / Judgment Panda
- [ ] Mustang Panda / Bronze President
- [ ] Volt Typhoon
- [ ] Flax Typhoon
- [ ] Salt Typhoon
- [ ] Silk Typhoon / Hafnium
- [ ] Earth Krahang
- [ ] UNC3886
- [ ] UNC5221
- [ ] UNC4899

### Financial, extortion, and access crews

- [ ] FIN7 / Carbanak / Navigator Group
- [ ] FIN8
- [ ] FIN11
- [ ] Wizard Spider / TrickBot / Conti
- [ ] Scattered Spider / UNC3944 / Octo Tempest
- [ ] LAPSUS$
- [ ] Evil Corp / Indrik Spider
- [ ] Black Basta
- [ ] ALPHV / BlackCat
- [ ] Cl0p
- [ ] LockBit
- [ ] Akira
- [ ] Play
- [ ] BianLian
- [ ] Rhysida
- [ ] Vice Society
- [ ] TA505
- [ ] TA544
- [ ] TA577
- [ ] TeamTNT
- [ ] TeamPCP expansion pass
- [ ] UNC5537
- [ ] Hunters International
- [ ] DragonForce

### Supply-chain, cloud, and ecosystem abuse clusters

- [ ] TraderTraitor
- [ ] UNC4736
- [ ] Famous Chollima
- [ ] LabHost operators and reseller clusters
- [ ] 0ktapus operator cluster
- [ ] 911 S5 ecosystem operators
- [ ] Storm-0558
- [ ] Storm-1113
- [ ] Storm-1811
- [ ] Node package typosquatting clusters with repeated infrastructure reuse
- [ ] PyPI credential-stealer publisher clusters
- [ ] GitHub Action tag-tampering clusters

## People

### Publicly identified operators, admins, and facilitators

- [ ] Park Jin Hyok
- [ ] Jon Chang Hyok
- [ ] Kim Il
- [ ] Rim Jong Hyok
- [ ] Dmitry Yuryevich Khoroshev / LockBitSupp
- [ ] Maksim Yakubets
- [ ] Evgeniy Bogachev
- [ ] Roman Seleznev
- [ ] Alexsey Belan
- [ ] Andrey Tyurin
- [ ] Mikhail Pavlovich Matveev
- [ ] Rustam Rafailevich Gallyamov
- [ ] Aleksei Besciokov
- [ ] Alexander Vinnik
- [ ] Dmitry Badin
- [ ] Aleksei Morenets
- [ ] Anatoliy Kovalev
- [ ] Pavel Frolov
- [ ] Ivan Yermakov
- [ ] Nikolay Kozachek
- [ ] Maksim Rudometov
- [ ] YunHe Wang

### People and public personas tied to high-signal supply-chain or ecosystem incidents

- [ ] `hackerfantastic` and other public handles central to disclosure or exploitation chains when the persona itself is operationally relevant
- [ ] Publicly named maintainers tied to signed malicious release artifacts
- [ ] Public GitHub personas behind repeated package hijacks or tag tampering
- [ ] Public operators behind 3CX, Polyfill.io, or SolarWinds-adjacent administrative control paths when strong sourcing supports a page
- [ ] Public admins, marketplace operators, or laundering facilitators tightly coupled to ransomware and access-broker ecosystems

### Expansion candidates for already-touched themes

- [ ] Additional XZ-maintainer context around `JiaT75` if new durable public sourcing appears
- [ ] Public people tied to `tj-actions` or `reviewdog` compromise paths if later advisories or indictments name them
- [ ] Public people tied to TeamPCP operations if strong sourcing emerges beyond the current group-level page
- [ ] Public maintainers or personas tied to Trivy, LiteLLM, or adjacent package compromises

## Ops

### Supply-chain and release-chain compromise

- [ ] SolarWinds Orion / SUNBURST / SUNSPOT
- [ ] Kaseya VSA mass ransomware event
- [ ] 3CX desktop app compromise
- [ ] MOVEit Transfer exploitation and Cl0p extortion wave
- [ ] Polyfill.io downstream website compromise
- [ ] Codecov Bash Uploader compromise
- [ ] ShadowHammer ASUS Live Update compromise
- [ ] CCleaner signed-update compromise
- [ ] event-stream / flatmap-stream npm compromise
- [ ] ua-parser-js / coa / rc npm takeover
- [ ] GitHub OAuth token theft against downstream integrators
- [ ] CircleCI 2023 customer secret exposure incident
- [ ] GitHub Actions tag-tampering waves beyond `tj-actions`
- [ ] PyPI credential-stealer publisher campaigns with repeated infrastructure
- [ ] npm typosquatting or dependency-confusion campaigns with clear operator clustering

### Identity, SaaS, and cloud compromise chains

- [x] 0ktapus phishing campaign
- [ ] Okta support-system breach and downstream customer token theft
- [ ] Cloudflare / Okta token theft incident
- [ ] Twilio / Authy admin phishing campaign
- [ ] Snowflake customer-environment extortion campaign
- [ ] MGM Resorts and Caesars Scattered Spider intrusions
- [ ] Microsoft Storm-0558 email intrusion
- [ ] Microsoft Midnight Blizzard mailbox theft from Microsoft
- [ ] Dropbox phishing and code-signing material theft incident
- [ ] LastPass 2022-2023 compromise chain
- [ ] TeamTNT cloud credential-harvesting campaigns

### Mass exploitation and edge-device campaigns

- [ ] Microsoft Exchange ProxyLogon exploitation wave
- [ ] Microsoft Exchange ProxyShell exploitation wave
- [ ] Ivanti Connect Secure zero-day exploitation wave
- [ ] Barracuda ESG zero-day backdoor campaign
- [ ] Fortinet FortiOS / FortiGate exploitation waves
- [ ] PAN-OS GlobalProtect zero-day campaign
- [ ] CitrixBleed session-hijack wave
- [ ] GoAnywhere MFT mass exploitation
- [ ] Accellion FTA exploitation campaign
- [ ] ConnectWise ScreenConnect exploitation wave
- [ ] SonicWall SMA exploitation campaigns
- [ ] VMware ESXiArgs and related ESXi ransomware waves

### Espionage, telecom, and destructive operations

- [ ] NotPetya
- [ ] WannaCry
- [ ] Olympic Destroyer
- [ ] Operation Aurora
- [ ] Operation Cloud Hopper
- [ ] Operation CuckooBees
- [ ] Operation Triangulation
- [ ] ShadowPad NetSarang supply-chain compromise
- [ ] Volt Typhoon critical-infrastructure prepositioning campaign
- [ ] Salt Typhoon telecom intrusion campaign
- [ ] HAFNIUM Exchange intrusion campaign
- [ ] Dragonfly energy-sector intrusion campaigns
- [ ] Havex / ICS targeting campaign
- [ ] Shamoon destructive campaigns
- [ ] HermeticWiper / IsaacWiper campaign cluster

## Suggested near-term passes

- [ ] Build a first wave of canonical espionage group pages: APT29, APT28, Sandworm, Lazarus, Volt Typhoon
- [ ] Build a first wave of eCrime group pages: Scattered Spider, FIN7, Black Basta, Cl0p, LockBit
- [ ] Build a first wave of canonical ops pages: SolarWinds, 3CX, MOVEit, ProxyLogon, Snowflake
- [ ] Build people pages for a first wave of publicly indicted operators with strong DOJ/FBI or sanctions sourcing
- [ ] Add missing companion group or people pages whenever a new op clearly points back to one of the items above
