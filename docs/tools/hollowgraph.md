# HOLLOWGRAPH

## Summary
**HOLLOWGRAPH** is a Windows espionage implant documented by Group-IB on July 20, 2026. The .NET NativeAOT DLL turns a compromised Microsoft 365 mailbox calendar into a two-way dead drop: operators place encrypted tasking in far-future calendar events, and the implant creates its own events with encrypted stolen files attached.

Group-IB links HOLLOWGRAPH to the [Cavern](cavern.md) framework with high confidence based on shared command syntax and tasking. It identified at least 12 infected systems, about three of which were actively communicating during the observation window from June 3 through July 9, 2026. Telemetry and a compromised Israeli organization's mailbox suggest focused interest in Israeli entities. Group-IB does **not** attribute the operation to a known actor; it assesses only a low-confidence technical overlap with Lyceum.

## Tags
- tools
- malware
- HOLLOWGRAPH
- Cavern
- .NET malware
- NativeAOT
- espionage
- Israel
- Microsoft 365
- Microsoft Graph
- calendar dead drop
- cloud C2
- SaaS abuse
- DNS tunneling
- IPv6
- Entra ID
- OAuth client credentials
- data exfiltration
- AES-256-GCM
- RSA-OAEP
- low-confidence attribution

## Why it matters
- Graph API traffic goes to legitimate Microsoft infrastructure, reducing the value of destination-based network blocking and conventional C2-domain detection.
- The implant uses normal calendar and attachment functions rather than a Microsoft vulnerability; there is no product patch that removes the access path.
- An application identity can perform mailbox operations without normal interactive-user behavior, making OAuth application governance and mailbox auditing central to detection.
- The DNS channel refreshes the cloud credentials needed by the Graph channel, allowing operators to replace tenant, client, secret, and mailbox configuration without redeploying the implant.
- Fixed dates, event naming, attachment naming, DNS structure, and an on-disk configuration name provide strong behavioral hunts despite the trusted cloud transport.

## Execution and command interface
HOLLOWGRAPH is a .NET NativeAOT-compiled DLL that Group-IB describes as one component of a larger toolkit. A loader invokes it with a wide-character command string:

`<command>_;;_<arg0>_,_<arg1>_,_<arg2>`

It implements two commands:

- `get` retrieves operator tasking from a mailbox-calendar attachment, decrypts it, and returns the plaintext to the loader.
- `send` encrypts a supplied file and uploads it to a new calendar event as one or more attachments.

A seven-character task identifier derived from the supplied arguments labels the C2 exchange. The `_;;_` and `_,_` delimiters match Cavern's command grammar. Group-IB also observed a Cavern-style self-command, `003`, for debug-logging control. These details underpin its high-confidence framework linkage; they do not establish actor attribution.

## Microsoft 365 calendar channel

### Task retrieval
For `get`, the implant uses Microsoft Graph to query a fixed calendar window on **May 13, 2050, from 22:00 to 23:00 UTC**. It searches for an event whose subject contains `Event ID: <taskID>`, obtains the event's attachments, downloads `File{n}.txt`, and decrypts the result.

The Graph request sequence reported by Group-IB is behaviorally equivalent to:

1. Query `/users/{mailbox}/calendarView` for the fixed 2050 time window and `Event ID:` subject.
2. Retrieve the matching event.
3. Retrieve the event's attachments.
4. Decrypt the attachment and pass tasking to the controller.

### File exfiltration
For `send`, the implant:

1. encrypts the supplied data;
2. creates a calendar event dated May 13, 2050 with a GUID-like placeholder subject;
3. uploads one or more Base64-encoded `application/octet-stream` attachments named `File{n}.txt`; and
4. renames the subject to an operator-recognizable `Boss{...}ID{...}` form.

Tasking and exfiltration use separate RSA key pairs. Each payload uses RSA-OAEP to wrap a newly generated AES-256 key, while AES-256-GCM encrypts the content.

## DNS credential-refresh channel
HOLLOWGRAPH uses AAAA queries under `cloudlanecdn[.]com` to refresh four Microsoft Entra ID / Graph configuration values: tenant ID, client ID, client secret, and target mailbox. The DNS payload is not independently encrypted.

Reported query forms are:

- Length: `{random}.{taskID}.{fieldIndex}.p.cloudlanecdn[.]com`
- Data: `{random}.{taskID}.{fieldIndex}.{byteOffset}.q.cloudlanecdn[.]com`

The first two bytes of the IPv6 response to a `.p.` query encode the total length. Each response to a `.q.` query contributes 14 payload bytes, with the byte offset increasing by 14. The implant reassembles and UTF-8 decodes the values, then writes the updated configuration to `logAzure.txt`.

The configuration includes sensitive application credentials, mailbox identity, C2 domain, and RSA material. Do not collect or redistribute live credential contents as threat intelligence; preserve the file under incident-response controls and revoke the exposed application secret.

## Attribution and victim scope
- Group-IB identified at least 12 infected systems; approximately three communicated actively during its observation period.
- The earliest observed victim communication was June 3, 2026, and the latest was July 9, 2026.
- An Israeli organization's compromised mailbox and malware-upload telemetry support focused Israeli targeting, but victim geography is not actor attribution.
- Group-IB links HOLLOWGRAPH to Cavern with high confidence.
- Group-IB notes similarities with Lyceum, a subgroup of OilRig, but rates that relationship **low confidence** and leaves the operator unnamed.
- Check Point separately attributes the modular Cavern activity it documented to Cavern Manticore. That assessment should not be automatically transferred to this HOLLOWGRAPH operation.

## Detection and hunting

### Microsoft 365 and Graph
- Search for calendar events dated `2050-05-13`, especially during `22:00–23:00 UTC`.
- Hunt event subjects containing `Event ID:`, matching `Boss{...}ID{...}`, or consisting only of a GUID.
- Correlate those events with attachments named `File{n}.txt` and `application/octet-stream` content.
- Audit application-driven Graph operations that create calendar events, upload attachments, or patch event subjects, especially where no corresponding user session exists.
- Review service principals and OAuth applications with application permissions to mailboxes or calendars; identify unexpected client-credential use and newly added client secrets.
- Preserve Entra service-principal sign-in, audit, Graph, Exchange mailbox-audit, and Unified Audit Log records before rotating credentials.

### Endpoint and DNS
- Hunt for `logAzure.txt` in unexpected application, loader, user-profile, and temporary directories. Treat it as potentially credential-bearing evidence.
- Alert on repeated AAAA queries with long or high-entropy subdomains, particularly labels containing `.p.` or `.q.` immediately below `cloudlanecdn[.]com`.
- Correlate DNS activity with processes loading NativeAOT DLLs and with subsequent application-only Graph access.
- Block or sinkhole `cloudlanecdn[.]com` through controlled resolvers, but do not treat blocking alone as containment because the Graph application credentials may remain valid.

## Incident response
1. Isolate affected hosts while preserving memory, loaded-module, process, DNS, and file telemetry.
2. Disable or restrict the implicated Entra application and revoke or rotate its client secret before restoring the host.
3. Review the application's permission grants, service-principal sign-ins, mailbox access, and all mailboxes reachable with the compromised permissions.
4. Export suspicious far-future events, attachment metadata, and Graph / Exchange audit records under evidence-handling controls.
5. Search for the same application ID, service principal, DNS pattern, event names, attachment names, and file hashes across the tenant and endpoint fleet.
6. Determine what files were accessible to the loader and what calendar attachments were uploaded; calendar-event deletion does not prove that exfiltration did not occur.
7. Remove persistence and malware only after identity containment and evidence preservation.

## Reported indicators
- DNS C2: `cloudlanecdn[.]com`
- Local configuration: `logAzure.txt`
- Event date: `2050-05-13`
- Retrieval subject: `Event ID: <taskID>`
- Exfiltration subject pattern: `Boss{...}ID{...}`
- Attachment pattern: `File{n}.txt`
- SHA-256:
  - `75e51774b8f79e5f256eaae639635f911b3e744d4774fd6068dd980255621509`
  - `f3f3006f8304788251b153d53b305322b8acab0c66ec816b8d9f101bcc851da3`
  - `b3d0f6e4e3be395fd7cf9e8101c89963d77216578cbb117a6ac9bc3564485eff`

## Related pages
- [Cavern](cavern.md)
- [Cavern Manticore](../actors/cavern-manticore.md)
- [Seedworm / MuddyWater](../actors/seedworm-muddywater.md)
- [ToddyCat Umbrij Gmail OAuth operation](../ops/toddycat-umbrij-gmail-oauth.md)
- [Turla STOCKSTAY backdoor operations](../ops/turla-stockstay-backdoor-operations.md)

## Sources
- Group-IB: [HOLLOWGRAPH: Turning Microsoft 365 Calendars into Covert Command-and-Control Channels](https://www.group-ib.com/blog/hollowgraph-microsoft-365/)
- The Hacker News: [HollowGraph Malware Hides C2 and Stolen Files in Microsoft 365 Events Dated 2050](https://thehackernews.com/2026/07/hollowgraph-malware-hides-c2-and-stolen.html)
