# Source index

Feeds and primary sources we consider worth monitoring for future threat coverage.

## High-value RSS / update feeds
- **Aikido Security Research** — https://www.aikido.dev/blog/index.xml
- **Wiz Research** — https://www.wiz.io/blog (HTML watch; prior RSS path returned 404 in current checks)
- **Socket Security Research** — https://socket.dev/blog (HTML watch; prior RSS paths returned 404/403 in current checks; watch Shai-Hulud/Mini Shai-Hulud variants, registry-response notices such as npm token invalidation, TeamPCP/copycat reporting, and AI-toolchain supply-chain tradecraft such as MCP or coding-assistant poisoning)
- **Akamai Security Research** — https://www.akamai.com/blog/security-research (HTML watch; RSS blocked/unavailable in current checks)
- **Lumen Black Lotus Labs** — https://www.lumen.com/blog/en-us/ (HTML watch; filter for Black Lotus Labs posts covering telecom, routing, botnet, and nation-state infrastructure research)
- **Snyk Blog / Security Research** — https://snyk.io/blog/feed/
- **JFrog Security Research** — https://research.jfrog.com/ (HTML watch) and JFrog Blog RSS https://jfrog.com/blog/feed/
- **Unit 42 Research** — https://unit42.paloaltonetworks.com/feed/ (watch recurring npm threat-landscape updates for Shai-Hulud/Mini Shai-Hulud wave metrics, SLSA/OIDC findings, and containment-order warnings)
- **ESET WeLiveSecurity / ESET Research** — https://www.welivesecurity.com/en/eset-research/ (HTML/RSS watch)
- **Microsoft Security Blog** — https://www.microsoft.com/en-us/security/blog/ (HTML watch; RSS may return 403)
- **GitHub Security Blog** — https://github.blog/security/ (HTML watch for GitHub platform incident notes and postmortems)
- **The Hacker News** — https://feeds.feedburner.com/TheHackersNews
- **Boost Security Labs** — https://labs.boostsecurity.io/rss.xml (watch CI/CD supply-chain techniques such as deployment poisoning and TeamPCP follow-ups)
- **StepSecurity blog** — https://www.stepsecurity.io/blog/rss.xml
- **Trail of Bits blog** — https://blog.trailofbits.com/feed/
- **PortSwigger Research** — https://portswigger.net/research/rss
- **ProjectDiscovery blog** — https://projectdiscovery.io/blog/rss
- **CISA KEV** — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- **GitHub Security Advisories** — https://github.com/advisories.atom

## Maintainer / vendor incident posts to watch during active campaigns
- **Nx / nrwl security advisories and issues** — https://github.com/nrwl/nx/security/advisories and https://github.com/nrwl/nx/issues
- **Grafana Labs security posts** — https://grafana.com/blog/tags/security/
- **PyPI project and malware-report pages for affected packages** — use package-specific release history as confirmation for yanked or restored versions.

## Notes
- Prefer RSS/Atom over ad hoc web searches.
- If a feed URL changes, update this page and the monitoring config together.
- If a source produces repeated noise, lower its priority before removing it.

## Active watch topics
- **Shai-Hulud / Mini Shai-Hulud / TeamPCP supply-chain activity** — monitor vendor research, affected-package appendices, maintainer postmortems, CISA/GitHub advisories, and registry notices for new package families, propagation methods, persistence paths, infrastructure, and attribution changes.
