# Water-sector PLC configuration-tampering campaign

## Summary
On July 30, 2026, CISA, the FBI, and the US Environmental Protection Agency warned that malicious actors were directly accessing internet-facing programmable logic controllers in US water and wastewater utilities and changing network and authentication configuration. The FBI said utilities in **at least seven states** had reported incidents since July 27.

The confirmed target set is Rockwell Automation / Allen-Bradley **MicroLogix 1100 and 1400** PLCs. Public reporting does not name an actor, exploit, malware family, source address, or credential-acquisition method. The reliable defensive conclusion is narrower: direct PLC internet exposure, including undocumented cellular paths, gave actors a route to alter IP addresses, enable or change passwords, modify project files, and disrupt monitoring or control.

Reported consequences include operator lockout, loss of monitoring and control, pressure loss, flooding, boil-water notices, and sustained manual operations. Treat unexplained PLC configuration drift as a safety and incident-response event, preserve volatile and engineering evidence where operations permit, and do not restore unvalidated project backups.

## Tags
- ops
- operations
- active threat
- water sector
- wastewater
- operational technology
- industrial control systems
- PLC
- Rockwell Automation
- Allen-Bradley
- MicroLogix 1100
- MicroLogix 1400
- configuration tampering
- operator lockout
- cellular modem
- critical infrastructure
- incident response

## Why this matters
- The FBI observed incidents across at least seven states within four days, and some degraded water operations.
- The actors changed IP addresses and passwords rather than relying on a named malware payload. Detection must emphasize PLC state and engineering-change integrity, not endpoint signatures.
- At least one victim found modified PLC project files and ladder-logic discrepancies across several sites.
- Similar third-party network setups across victims may have multiplied exposure, creating an integrator and shared-architecture blast radius.
- Cellular modems installed by operators, vendors, or integrators may be absent from normal asset inventories and external attack-surface scans.
- Operational effects included loss of pressure and flooding. Pressure loss can create a contamination pathway by allowing untreated groundwater into pipes.

## Observed activity
The joint public reporting describes this sequence:

1. Actors remotely accessed directly internet-facing PLCs.
2. They changed device IP addresses and enabled or changed passwords.
3. Operators lost visibility or control of connected equipment.
4. Some facilities switched to manual operations; reported effects included pressure loss, flooding, boil-water notices, and sustained manual operation.
5. One organization identified altered project files and ladder-logic differences across multiple sites.

Impact depended on whether the PLC monitored or controlled equipment, the MicroLogix model, the process function, and the facility's ability to operate manually.

## Scope and evidence limits
- **Confirmed devices:** Rockwell Automation / Allen-Bradley MicroLogix 1100 and 1400 series.
- **Confirmed victim scope:** water and wastewater utilities in at least seven US states reporting incidents to the FBI since July 27, 2026.
- **Not publicly established:** actor identity, intent beyond the observed tampering, vulnerability exploitation, password source, source infrastructure, malicious tooling, or a complete victim count.
- The FBI recommends applying the same exposure controls to other PLC brands, but says it had only observed this behavior on the named Rockwell models at publication time.
- Similar network design across several victims is evidence of a repeatable exposure pattern, not proof that a vendor or integrator itself was compromised.

## Immediate defensive actions

### Contain exposure safely
1. Inventory every MicroLogix 1100 and 1400, then expand to all PLCs, engineering workstations, HMIs, gateways, and remote-access paths. Include cellular modems, private APNs, vendor circuits, temporary maintenance links, disaster-recovery paths, and undocumented integrator access.
2. Remove direct inbound internet exposure. Broker approved remote access through a monitored secure gateway or jump host and a site-to-site VPN, ZTNA path, private APN, cellular SD-WAN, or comparable isolated architecture.
3. Apply firewall or controller ACLs so only expected engineering and control-system assets can communicate with PLCs. Do not use a public blocklist as the primary control; no source indicators were released.
4. Change default, reused, or weak PLC and modem credentials to unique strong credentials. Preserve current configuration and logs first when compromise is suspected and safe operation permits.
5. Enable and retain cellular-modem, gateway, firewall, VPN, engineering-workstation, HMI, and controller logs.

### Protect logic and recovery
- Place physical and software key switches in **run** mode to block unauthorized logic, configuration, and firmware changes except during controlled maintenance.
- Before changing mode, validate the project currently loaded on the controller; switching to run mode can lock in malicious or incorrect logic.
- Compare running PLC programs, ladder logic, reusable logic, I/O configuration, IP settings, and authentication state with known-good engineering baselines.
- Preserve copies of current and suspect project files for investigation. Validate backups before restoration so altered logic is not reintroduced.
- Maintain a known-clean PLC image and tested offline project backup after removing internet exposure.
- Exercise safe manual operation, fail-safe mechanisms, islanding, standby systems, and business-continuity procedures.

## Hunting and triage
Prioritize:

- unapproved PLC IP-address, subnet, gateway, password, mode, firmware, project, ladder-logic, I/O, or communication changes;
- unexpected transitions into program or remote mode;
- controller project-file hashes or logic that differ across nominally identical sites;
- new or failed engineering-session authentication and remote configuration activity;
- inbound PLC access from public networks, hosting providers, unknown cellular paths, or devices outside the approved engineering allowlist;
- cellular-modem configuration changes, new management sessions, weak/default authentication, and missing or disabled logs;
- suspicious access from HMIs, engineering workstations, gateways, or vendor systems connected to the same PLC segment; and
- unexplained pressure, pump, valve, level, alarm, telemetry, or communication-state changes aligned with network events.

If telemetry suggests access to connected systems, review all adjacent devices and reimage workstations or gateways where malicious changes or access tooling cannot be ruled out. Preserve controller state, project files, network captures, gateway/firewall/modem logs, engineering-workstation evidence, operator timelines, and physical-process telemetry before recovery actions where this can be done safely.

## Recovery and long-term hardening
- Coordinate cyber response with plant operations and safety personnel; do not make controller changes that could worsen physical conditions.
- Restore only validated logic and configuration, then verify process outputs against safe operating expectations.
- Replace or isolate end-of-life PLCs. Maintain a rolling 12-month EOL forecast with owner, location, model, and retirement date.
- Require integrators and vendors to document remote paths, cellular assets, authentication, logging, and decommissioning. Validate the inventory independently.
- Segment PLCs from enterprise and public networks, centralize remote-access approval and logging, and test recovery from clean engineering baselines.

## Related pages
- [Siemens ROX II zero-day exploit chain](siemens-rox-ii-zero-day-chain.md)
- [KNX Protocol CVE-2023-4346 KEV exploitation](knx-protocol-cve-2023-4346-kev-exploitation.md)
- [Russian state IP-camera military-logistics espionage](russian-state-ip-camera-military-logistics-espionage.md)

## Sources
- CISA alert, July 30, 2026: [https://www.cisa.gov/news-events/alerts/2026/07/30/cisa-urges-water-and-wastewater-systems-sector-protect-ot-against-activity-targeting-plcs](https://www.cisa.gov/news-events/alerts/2026/07/30/cisa-urges-water-and-wastewater-systems-sector-protect-ot-against-activity-targeting-plcs)
- FBI / EPA Public Service Announcement `I-073026-PSA`, July 30, 2026: [https://www.ic3.gov/PSA/2026/PSA260730.pdf](https://www.ic3.gov/PSA/2026/PSA260730.pdf)
- CISA, FBI, EPA, and DOE, Primary Mitigations to Reduce Cyber Threats to Operational Technology: [https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology](https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology)
- UK NCSC, Secure connectivity principles for operational technology: [https://www.ncsc.gov.uk/collection/operational-technology/secure-connectivity](https://www.ncsc.gov.uk/collection/operational-technology/secure-connectivity)
