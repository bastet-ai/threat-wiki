# ConnectWise SaaS application-identity compromise — seven Entra app identities disabled, Cloud Backup suspended, ~1,000 tenants probed (Oct 13–18, 2026)

**What happened.** ConnectWise disclosed that unknown threat actors obtained unauthorized access to its own SaaS application identities and used them to reach customer Microsoft 365 tenants. On **October 17, 2026 07:00 UTC** the company disabled seven application identities and revoked the certificates used for affected application connections **across all users**, suspending ConnectWise Cloud Backup entirely; SaaS Security and Cloud Management were temporarily taken offline. The issue was identified **October 14, 2026** via internal monitoring; whether a product vulnerability contributed, and the credential-exposure mechanism, were both unresolved at disclosure.

This is the SaaS-side mirror of the pattern this wiki tracks on the package side: **the vendor's own shared credential is the supply-chain vector.** One stolen application credential authenticates into every customer tenant that trusts the app — no per-user password theft required.

## The seven disabled application identities (as published by ConnectWise)

| Application identity | Entra app object ID |
|---|---|
| ConnectWise Cloud Backup | `506e08f9-6e9a-4da4-942b-a099a03644ae` |
| ConnectWise Cloud Management | `2399d300-6fca-4e6a-a686-399fefe75b83` |
| ConnectWise Cloud Management - MS Teams | `24205314-2b89-4e07-a2a4-579e898a5640` |
| ConnectWise Cloud Management - Exchange Online | `b78f6a77-d4e5-46fb-87e5-d1648bd02519` |
| ConnectWise Cloud Management - MS Graph | `0de14c77-b9b0-4137-9360-34878a929827` |
| ConnectWise Cloud Management - Partner Center | `412dcf96-176d-4b3a-a1b0-4981ad66971e` |
| ConnectWise Cloud Management - SharePoint Online | `b2b55f5b-7758-4719-8d8f-88ae172e6bdb` |

**Vendor caveats recorded verbatim in effect:** disabling the connections prevents NEW authentication but "does not reverse changes previously made inside a tenant"; previously issued access tokens may remain usable until expiry; any unauthorized credentials/permissions established through separate identities require per-tenant remediation. Scheduled backups are not running; archives remain encrypted, isolated, and preserved with no evidence of access.

## Huntress telemetry (relayed by The Hacker News, Oct 17–18)

- Last malicious sign-ins from the ORIGINAL attacker address: **Oct 15, 08:45 UTC**, with targeted manual activity until `≈14:20 UTC` that day. No new malicious activity observed after Oct 15 — and no evidence the stoppage resulted from public disclosure.
- High confidence the actor also targeted the Cloud Management apps for Exchange Online, Teams, and SharePoint; **abuse of the Teams app confirmed in one tenant**. Those apps were NOT among the disabled set at Huntress's check — residual live surface.
- **Second, targeted wave Oct 15 from `144.172.64[.]128`** against a narrow set of **16 tenants** (policy, national-security, trade, and critical-mineral sectors): sweep 1 harvested Graph tokens from the **SkyKick** app `09:25:04–12:35:50 UTC`; sweep 2 (`13:54:39–14:20:24 UTC`, apparently manual) hit Exchange Online, SharePoint Online, Teams, Azure Resource Manager, Entra, and Office 365 Management APIs. Both sweeps unsuccessful against that set.
- Census: **almost 1,000 Entra tenants** showed sign-in activity from the IP; **300 succeeded**; in some tenants the absence of the relevant service principal was the only thing that stopped access after a successful sign-in.

## Why application-identity theft is a distinct failure class

- Authenticating AS the application lets the actor mint tokens against whatever permissions the app already holds (mailboxes, SharePoint, Teams, directory) — the victim's users never authenticate and no user credential rotates out the access.
- With Application Administrator-equivalent reach inside a tenant the actor can escalate to Global Administrator, **add client secrets to other trusted applications**, and register new apps — planted secrets survive revocation of the original stolen credential. This is the identity-side equivalent of the registry-side "purge the package, the published secret lane stays open" asymmetry.
- Huntress's durable control list: application-management policies blocking/limiting client secrets and capping credential lifetimes; restricting Application Administrator / Cloud Application Administrator holders; **Conditional Access for workload identities**; Entra ID Protection risky-service-principal flagging. None replace credential review; each makes a planted secret harder to use or easier to spot.

## Partner remediation checklist (published guidance, condensed)

Review own tenant + every managed customer tenant including **dormant SkyKick connections**; verify status of the seven listed connections and keep affected apps disabled; review sign-ins **from Oct 13, 2026** for activity from `144.172.64[.]128`; **preserve sign-in and audit records BEFORE containment**; review application/user authentication, application credentials and federation trusts, directory roles, owners, consent grants, recent policy changes; check unauthorized mailbox forwarding, inbox/transport rules, delegated access; investigate any identities changed or used during suspicious activity.

## Durable reads

1. **Detection was vendor-side (Oct 14) but enforcement was collective (Oct 17)** — a three-day window where the credential was known-bad to the vendor and still valid for every customer. Compare the ledger's four-lane enforcement-speed taxonomy on the package side: SaaS identity enforcement has the same advisory→action lag problem, one level up.
2. **A dark service principal is the accidental control.** Dozens of successful sign-ins produced no access only because the tenant lacked the app registration — a defense nobody configured. Tenants that never onboarded the vendor service can still be probed and logged; treat unexpected sign-ins from vendor-integration IPs as reconnaissance.
3. **The MSP blast radius is the real number:** ConnectWise's downstream customers are MSPs, so each compromised app identity is a federated trust path into hundreds of tenants at once. The 1,000-tenant probe / 300-success split is a lower bound on exposure, not on access.
4. Recorded-not-asserted: no attribution, no named actor, no confirmed vulnerability, no confirmed data-access scope beyond the one Teams-abused tenant at capture time.

## Sources

- The Hacker News, "ConnectWise Suspends Cloud Backup After Attackers Compromise Microsoft 365 Tenants" (Oct 18, 2026) — <https://thehackernews.com/2026/10/connectwise-suspends-cloud-backup-after.html> (full text captured by this wiki Oct 18; includes the Huntress detail and the seven-app list)
- The Hacker News, "Hackers Use Compromised ConnectWise Credential to Sign In to 173 Microsoft 365 Tenants" (Oct 17, 2026) — <https://thehackernews.com/2026/10/hackers-use-compromised-connectwise.html> (first wave: 173 tenants at that count)
- Huntress incident blog (linked from the THN piece)
- ConnectWise advisory/trust post (linked from the THN piece)

**Monitor:** ConnectWise's root-cause disclosure (credential-exposure mechanism; whether a product vulnerability contributed); re-enablement or replacement of the seven identities; the un-disabled Cloud Management rails (Exchange Online/Teams/SharePoint) for follow-on activity; SkyKick-name copycats against other backup/M365-integration vendors; additional MSP-side victim disclosures; whether any of this lands a KEV row (none at capture); actor attribution.
