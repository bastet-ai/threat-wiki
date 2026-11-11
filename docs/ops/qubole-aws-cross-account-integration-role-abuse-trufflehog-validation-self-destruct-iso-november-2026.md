# Qubole cross-account role abuse: vendor trust, TruffleHog validation, and the self-erasing ISO

**Captured November 11, 2026 (243rd sweep) by this wiki from the Wiz Research post (Nov 9, via Sentra and Mandiant), full text fetched and read same-window; this wiki's own static probes are marked. No artifact was ever executed. Attribution NOT asserted (Wiz asserts none).**

## Summary

Between October 14 and October 26, 2026 a threat actor used IAM credentials from AWS account `805246085872`, the account Qubole's platform uses to assume customer integration roles, to walk INTO multiple victim AWS environments through the ordinary vendor cross-account trust pattern: customer-created role, trust policy to the vendor account, `sts:ExternalId` gate. Every assumed role was a role the victims had left behind after their Qubole integration went quiet or dead — the trust policies were still in place, so every call succeeded, and in most victim environments the attacker's requests were the ONLY AssumeRole traffic from the vendor account all month. Inside, the actor enumerated broadly, harvested Lambda environment variables, Secrets Manager values, and SSM parameters, validated what it found with **TruffleHog** across three identity planes (AWS keys via `GetCallerIdentity`, Entra ID service principals via client secrets, Okta via client credentials), and downloaded reachable S3 buckets wholesale. The durable artifacts for defenders are three: the **`quiam-` role-session-name prefix** as a free detection string; the finding that **a source-IP condition alone on the trust policy would have blocked every observed assumption**; and a **bootable Linux ISO hosted on the actor's VPS that self-destructs on a 90-minute hard-reboot timer** — a dead-man erasure design on a remote-boot artifact, loaded `ntfs3` at boot, suggesting Windows hosts as the target, never observed deployed.

## Timeline (Wiz-documented)

| Window (UTC) | Event |
|---|---|
| Oct 14 | First attributed `AssumeRole` from `45.83.220[.]211` (Mullvad VPN exit), account `805246085872`, IAM user `AIDA3W7DIFLYOLTK63SFS` |
| Oct 15 onward | Most activity shifts to OVH VPS `57.129.54[.]120` |
| Oct 18 | Second IAM user `AIDAJYRRH5Y3A7AAJM2HW` (also carries legitimate Qubole traffic) begins; second Mullvad exit `185.209.199[.]73` assumes roles across multiple victims in quick succession |
| Oct 14-26 | Enumeration, credential harvesting, TruffleHog validation, S3 exfiltration across victim environments |
| Oct 8-11 | SEPARATE, UNLINKED activity: actor uses customer-owned AWS keys created for Qubole integrations, tests all within one hour, few victim environments compromised |

## The mechanics that mattered

- **Trust, not exploit.** No vulnerability was needed. The customer-side role with `Principal.AWS: arn:aws:iam::<vendor>:root` still existed; the External ID, which Wiz explicitly instructs defenders to treat as NON-secret (plaintext in CloudTrail, often committed in IaC), was supplied correctly every time.
- **The `quiam-` session grammar.** Role session names followed `quiam-<action>` (`quiam-enum`, `quiam-scope-full`) — a free CloudTrail filter with near-zero legitimate collision.
- **Harvest triad:** `ListFunctions` + `GetFunctionConfiguration` (Lambda env vars), `ListSecrets` + `GetSecretValue`, `DescribeParameters` + `GetParameter` (SSM).
- **Validation is loud even when theft is quiet.** TruffleHog user-agent `GetCallerIdentity` bursts across SEVERAL AWS accounts within seconds; the same UA against Entra ID sign-in and Okta token endpoints. These are detection events independent of CloudTrail.
- **The log gap is the exfil.** CloudTrail management events record the role assumption and `ListBuckets`; they do NOT record the `GetObject` reads that are the actual theft. Environments without S3 data events could not answer "what was taken."
- **The ISO (Wiz, via Validin):** `sso_agent.iso` at `57.129.54[.]120`, SHA-256 `65f061281c9a712e9502793dc4c5035cae490b84da05f7d4223cefa65ad396e4` (third-party hash, NOT verified by this wiki — the file was never fetched). Bootable Linux image, believed remotely booted on victim machines: starts a 90-minute clock, reports interfaces/disks/partitions to the VPS, polls TCP `23458` for a script to run as shell, and HARD-REBOOTS at `T+90:00`, wiping the only local evidence of its presence. Loads the `ntfs3` driver at boot → Windows hosts plausibly targeted. No deployments identified by Wiz; usage unconfirmed.

## This wiki's static verification (243rd sweep, ~12:3x UTC Nov 11, GET-only, nothing executed)

- `57.129.54.120` answers **nothing** on HTTP/HTTPS (`000`, connection-fail) at read time = the VPS is dark, not proven dead; the ISO's availability state as of this read is UNCONFIRMED (the `000` covers HTTP routes only).
- `api[.]frameworkmetrics[.]xyz` still `523` (shared read with the [bee-js page](ethersphere-bee-js-npm-swarm-desktop-release-pipeline-compromise-sleepyduck-ethereum-contract-c2-november-2026.md)) — collector-dark class re-lands, dark ≠ dead.
- Registry-ledger lanes were genuinely quiet this sweep (`MAL-2026-19116`+ `404`); nothing on this campaign touches the OSV mirrors.

## Durable hunt shapes

1. **Inventory trust, not just assets.** Every IAM role whose trust policy names an EXTERNAL AWS account is a standing door. List them org-wide, per region; the Qubole victims' doors were the ones nobody remembered closing.
2. **Unused-role signal:** a vendor integration role whose only October `AssumeRole` events are from the vendor account but whose source IPs are non-AWS (VPN/hosting ranges) is this attack. `userIdentity.accountId == <vendor>` AND source not in vendor-documented ranges = high-signal alert class (Wiz's own recommendation; a source-IP condition alone would have blocked 100% of observed assumptions).
3. **Principal-pin the trust.** Replace `:root` with the specific vendor IAM principal where the vendor supports it, add `aws:SourceIp`/`aws:SourceVpce` conditions, use distinct External IDs per role — and rotate the External ID after any incident, coordinating with the vendor.
4. **`quiam-` (and its successor grammars) as session-name canary:** alert on any role-session-name prefix that no legitimate integration of yours uses.
5. **TruffleHog UA correlation across THREE logs,** not one: CloudTrail `GetCallerIdentity`, Entra ID sign-in logs, Okta OAuth-token endpoints.
6. **Rotation does not end issued sessions.** After any suspected role assumption: rotate every secret the role could read AND revoke active sessions for the role — the two are separate actions and the second is the one teams forget.
7. **S3 data events are the exfil census.** If they were off during the window, "what did they take" is unanswerable; treat that blindness as an incident finding in itself.
8. **Remote-boot ISO + countdown reboot = evidence erasure as a service.** Defenders hunting later have NO local artifact; the durable traces are the network (poll to TCP `23458`), the hosting IOC, and the ISO's own hash at its host. Hunt the poll, not the disk.

## Related on this wiki

- [Ethersphere bee-js / Swarm Desktop release-pipeline compromise](ethersphere-bee-js-npm-swarm-desktop-release-pipeline-compromise-sleepyduck-ethereum-contract-c2-november-2026.md) (same-era lesson: trusted infrastructure as the attack surface; campaign kinship NOT asserted)
- [Railway build-system breach: build escape to stolen AI keys](railway-build-system-breach-oidc-trust-stolen-customer-ai-api-keys-november-2026.md) (the same week's other third-party-trust story: a platform's own credential accepted where it shouldn't have been)
- [GitHub Actions OIDC subject-claim collisions](../patterns/github-actions-oidc-subject-claim-collisions.md) (the identity-side sibling class)
- [ALGAMIL7X stream, 243rd sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-third-sweep)

## Sources

- Wiz Research, "Trusted by Default: Qubole Cross-Account Access Abused in the Wild" (Nov 9, 2026; Sentra + Mandiant collaboration): [https://www.wiz.io/blog/qubole-cross-account-access-abused-in-the-wild](https://www.wiz.io/blog/qubole-cross-account-access-abused-in-the-wild) (full text captured by this wiki Nov 11)
