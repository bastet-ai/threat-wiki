# Suspected Chinese operators use Claude Code and DeepSeek in government intrusions

## Summary
Hunt.io reported a June 2026 intrusion set in which suspected China-based operators used **Claude Code** and **DeepSeek-v4-pro** as active parts of the attack workflow against government, supply-chain, and financial targets. The public reporting is durable because it moves beyond generic "AI-assisted" phrasing: recovered operator files showed a two-model split where Claude Code handled agentic execution, shell/tool use, persistence of working sessions, task parallelization, and phishing-page iteration, while DeepSeek-v4-pro supplied reasoning, exploit adaptation, and decision support.

Hunt.io found the activity after pivoting from known **TencShell** command-and-control infrastructure to an exposed open directory on `112.213.124[.]132`. The directory contained payloads, operator scripts and logs, exploit material, cloned login pages, victim-specific folders, and victim source code. Hunt.io said affected organizations and national CERTs were notified on July 6, 2026 before publication.

## Tags
- ops
- operations
- China-nexus
- suspected China-linked
- agentic AI
- AI-assisted intrusion
- Claude Code
- DeepSeek
- TencShell
- Gshell
- Vshell
- DeepAudit
- ARL
- government targeting
- Afghanistan
- Thailand
- Taiwan
- United States
- financial services
- SQL injection
- Laravel deserialization
- web shell
- credential harvesting
- open directory
- Hong Kong infrastructure

## Why this matters
- The case shows LLMs used inside a live intrusion workflow, not only during pre-attack research or malware development.
- The exposed files tie AI-agent logs to hands-on exploitation, credential-harvesting infrastructure, and post-compromise tasking.
- The same infrastructure hosted reconnaissance tooling, code-audit tooling, C2 services, malware delivery, open directories, and victim data, creating multiple defensive pivots.
- The campaign mixed government-sector collection with supply-chain, manufacturing, telecommunications, and payment-platform targeting.
- The operators used public dual-use tooling such as ARL, DeepAudit, and Vshell, so defenders should correlate those services with exposed directories, victim material, malware delivery, and suspicious hosting relationships rather than treating tool banners alone as proof of compromise.

## Infrastructure and tooling
Hunt.io pivoted on an HTTP header hash seen on TencShell port `1111` and identified **13 Hong Kong-based servers** across VMISS Inc., MEGA-II IDC, CTG Server Limited, and Antbox Networks Limited. Some nodes exposed additional services on ports `1212` and `8090`.

The main exposed host, `112.213.124[.]132`, showed a complete attack-support stack:

| Port | Service / role reported by Hunt.io |
| --- | --- |
| `22` | SSH remote access |
| `1111` | Malware download |
| `3000` | DeepAudit code vulnerability scanning |
| `5003` | Asset Reconnaissance Lighthouse (ARL) |
| `8084` | Vshell C2 server |
| `8888` | Python SimpleHTTP open directory |

`112.213.124[.]132`, `112.213.124[.]159`, and `112.213.124[.]163` shared an SSH host-key fingerprint and ARL TLS certificate history. Hunt.io also observed that those three systems exposed the same pattern of ARL, Vshell, open-directory, and malware-delivery services.

## Malware and C2 notes
HTTP GET requests to port `1111` on the MEGA-II IDC hosts returned Linux payloads. Hunt.io recovered a Linux/ARM 32-bit Golang binary named `HSEWH-Ur` from `112.213.124[.]132:1111`; it beaconed over WebSocket to `112.213.124[.]132:4081` and used `X-NITRO-USER` / `X-NITRO-PASS` HTTP authentication headers. The malware capabilities included Tencent QQ/IM credential extraction, enterprise messaging credential theft, cloud-service access-key theft, and file upload/download.

A related Linux/x86 sample from `38.55.105[.]143:8088` used `garble` to strip names, differed from the ARM files, but shared the same 80-byte encryption key, suggesting at least a shared codebase across architectures. Hunt.io was careful not to call the Linux samples confirmed TencShell builds because Cato CTRL's earlier TencShell sample was Windows-based and code-level matching was not established in the public report.

Hunt.io also identified a possible second C2 framework, **Gshell**, through TLS certificates with `CN = Gshell Server` and `O = Gshell C2` on `192.229.115[.]229` and `192.229.115[.]230`. Those nodes overlapped the TencShell cluster, leading Hunt.io to assess with moderate confidence that Gshell was operated in tandem with TencShell.

## Victimology and activity
### Taiwan
The open directories included reconnaissance against Taiwanese supply-chain and manufacturing organizations, including container shipping, semiconductor/UAV, robotics/drone, industrial, RC/uncrewed vehicle, and embedded-computing targets. Hunt.io described eight companies as enumerated or fingerprinted without confirmed exploitation.

Two Taiwan-linked organizations moved beyond reconnaissance:

- A chemical manufacturing and trading company was attacked through SQL injection; operators extracted development-environment source code and database information, then staged cloned web pages for credential harvesting.
- A multinational telecom and edge-device manufacturer exposed hardcoded Supabase anon keys and Azure Logic App SAS tokens in public JavaScript, enabling backend cloud enumeration and cloud-service account compromise.

### Thailand
A Thai government administrative system was compromised through SQL injection using SQLMap. Hunt.io reported authentication bypass, admin-panel access, and deployment of a GIF polyglot web shell controlled through GET parameters. The exfiltrated database contained government employee names, national ID numbers, and positions. Attacker-created test entries and June 9, 2026 activity indicated hands-on access and data manipulation.

### Afghanistan
An Afghan government application was compromised, exposing citizen complaint submissions and core application infrastructure. Dumped source code showed Laravel `5.8.38`, encryption keys, database credentials, and mail-handling code. Operators used recovered credentials to build a Python exploit against Laravel deserialization paths for remote code execution. Hunt.io noted the compromise could allow monitoring of complaint/grievance channels in real time.

### United States
Hunt.io did not report confirmed U.S. compromise. Logs showed reconnaissance of NASA hosts `launchpad.nasa[.]gov` and `ngis.nasa[.]gov`, while cloned pages impersonated D.C. Council and Delaware County, Pennsylvania web properties. The D.C. Council WordPress login clone was more complete than surrounding page clones, suggesting priority on credential capture.

### Financial services
The same infrastructure supported targeting of financial services firms. Hunt.io described an attacker-built CORS exploit page on `112.213.124[.]159` that extracted WordPress administrator account data from a large payment processor, plus enumeration scripts, logs, and screenshots tied to billing-platform targets across Europe, Australia, and Asia.

## LLM workflow
Recovered logs and a `CLAUDE.md` file documented an AI-assisted operating model:

- **Claude Code `2.1.165`** managed agentic tool use, Bash execution, persistent sessions, parallelization, and cloned-page creation/testing/iteration.
- **DeepSeek-v4-pro** provided reasoning, attack logic, script generation, bypass ideas, and exploit rework after failures.
- Session timestamps covered June 8-12, 2026, with Taiwan-specific operations saved in dedicated working directories.

This differs from commodity AI use for phishing copy or code snippets. The AI tools were embedded in the attack loop that staged pages, adapted exploitation, and coordinated operator work.

## Indicators and hunt pivots
### File hashes
| File name | SHA-256 | Notes |
| --- | --- | --- |
| `HSEWH-Ur` | `90b7b2c6f3d05234dc55678243039d7e51f0d54190239e5234a0005533337dc8` | Retrieved from `112.213.124[.]132:1111`. |
| `8eA-GlbK` | `90b7b2c6f3d05234dc55678243039d7e51f0d54190239e5234a0005533337dc8` | Retrieved from `112.213.124[.]159:1111`. |
| `r4l3DqLA` | `90b7b2c6f3d05234dc55678243039d7e51f0d54190239e5234a0005533337dc8` | Retrieved from `112.213.124[.]163:1111`. |
| `Ar70qICi` | `643de2a1cf9148b896efecf560c9476fa56118ec477c4e15eb5c2da4b318061f` | Retrieved from `38.55.105[.]143:8088`. |

### Network infrastructure
| Indicator | Role / note |
| --- | --- |
| `112.213.124[.]132:1111` | Malware delivery / open-directory-adjacent TencShell pivot. |
| `112.213.124[.]132:4081` | WebSocket C2 hub observed for Linux/ARM payloads. |
| `112.213.124[.]132:8888` | Python SimpleHTTP open directory. |
| `112.213.124[.]159:1111` | Malware delivery / open directory. |
| `112.213.124[.]163:1111` | Malware delivery / open directory. |
| `38.55.105[.]143:8088` | Malware delivery for related Linux/x86 sample. |
| `192.238.134[.]166:1212` | Suspected TencShell infrastructure. |
| `134.122.200[.]153:443` | Suspected TencShell infrastructure. |
| `134.122.200[.]154:443` | Suspected TencShell infrastructure. |
| `134.122.200[.]155:443` | Suspected TencShell infrastructure. |
| `192.229.115[.]229:8090` | Suspected TencShell / Gshell overlap. |
| `192.229.115[.]230:8090` | Suspected TencShell / Gshell overlap. |
| `45.64.52[.]242:1111` | Cato Networks TencShell IOC. |
| `45.64.52[.]245:1111` | Suspected TencShell infrastructure. |
| `45.64.52[.]246:1111` | Suspected TencShell infrastructure. |

Additional Gshell certificate-match IPs reported by Hunt.io include `192.163.167[.]5`, `192.163.167[.]6`, `192.163.167[.]7`, `192.163.167[.]10`, `134.122.200[.]114`, `134.122.200[.]115`, and `134.122.200[.]116`.

### Behavioral pivots
- Exposed ARL (`5003`), DeepAudit (`3000`), Vshell (`8084`), malware delivery (`1111`), and Python SimpleHTTP open directories (`8888`) on the same small server cluster.
- Shared SSH host key `64107E3E0A333F685D1BE6386426223A030C4126AC7C295AA7B1D54C508BBACE` across the MEGA-II IDC hosts.
- ARL default certificate fields `C = CN`, `ST = Shanghai`, `L = Shanghai`, `CN = 127.0.0.1`, `O = Example Inc.`, `OU = Web Security`; Hunt.io observed SHA-256 `AD1A0B3E22A10A2BD680B773B178A0D3824CFCBDF3551016F3D052A0B823079F`, later reissued as `2954639BE599F23C2229A9743ABA09A1D9D11BF2BECC62BF353384437DB37DEE`.
- Gshell TLS certificate subject `CN = Gshell Server`, `O = Gshell C2`.
- Claude Code working directories, `CLAUDE.md` files, and saved agent sessions on attacker infrastructure tied to exploit and phishing page generation.
- GIF polyglot web shells and JSP/PHP web shells disguised as images in staging directories.

## Response guidance
1. For exposed government and supplier portals, hunt for SQL injection and Laravel deserialization exploitation, not just commodity credential phishing.
2. Search web roots and upload paths for GIF polyglot shells, JSP/PHP shells masquerading as media, and cloned administrative login pages.
3. Review public JavaScript for backend cloud secrets, including Supabase anon keys and Azure Logic App SAS tokens, then rotate exposed material and validate account activity.
4. Monitor for the TencShell/Gshell infrastructure and certificate pivots above, but treat single-tool banners such as ARL, DeepAudit, or Vshell as triage leads requiring correlation.
5. Preserve web logs, database audit logs, source-code repository access logs, cloud-control-plane logs, and uploaded-file artifacts before remediation.
6. Add AI-agent audit artifacts to attacker-infrastructure reviews: `CLAUDE.md`, saved session IDs, model/tool logs, shell transcripts, and generated phishing templates can expose objectives and next steps.

## Attribution notes
Hunt.io assessed the observable indicators as consistent with China-based threat actor activity: Simplified Chinese operator notes, Hong Kong infrastructure concentration, TencShell lineage, Gshell overlap, and multi-continent government/financial targeting. The public report uses cautious language; this page tracks the activity as **suspected China-linked** rather than assigning it to a named APT.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [SHADOW-AETHER AI-augmented Latin America intrusions](shadow-aether-ai-augmented-latam-intrusions.md)
- [Patriot Bait AI-assisted C2 botnet](patriot-bait-ai-assisted-c2-botnet.md)
- [CL-STA-1062 Southeast Asia government and energy intrusions](cl-sta-1062-southeast-asia-tinyrct.md)
- [Hunt.io global smishing infrastructure campaign](huntio-global-smishing-government-postal-telecom.md)

## Sources
- Hunt.io: https://hunt.io/blog/chinese-operators-claude-deepseek-government-intrusion
