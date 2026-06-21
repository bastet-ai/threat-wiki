# FishMonger

## Summary
**FishMonger** is a China-linked cyberespionage group that ESET places under the broader Winnti Group umbrella and believes is operated by the Chengdu-based contractor **I-SOON**. ESET also lists the public aliases **Earth Lusca**, **TAG-22**, **Aquatic Panda**, and **Red Dev 10**.

FishMonger has targeted government, university, and strategic-sector environments. In June 2026, ESET published Windows variants of the previously Linux-only **SprySOCKS** backdoor and attributed them to FishMonger with high confidence after observing activity during 2023-2024 against mostly government organizations in Honduras, Taiwan, Thailand, and Pakistan.

## Tags
- China-linked
- Winnti Group
- I-SOON
- Earth Lusca
- TAG-22
- Aquatic Panda
- Red Dev 10
- espionage
- government targeting
- Honduras
- Taiwan
- Thailand
- Pakistan
- SprySOCKS
- ShadowPad
- Cobalt Strike
- BIOPASS RAT
- watering hole
- kernel driver

## Primary motivation
- **Espionage** against government and strategic-sector targets.
- **Long-term access** through custom backdoors, commodity tooling, and stealth components.
- **Regional intelligence collection** aligned with China-nexus operational interests, while keeping source-attributed caveats attached.

## Naming and attribution
- Keep `FishMonger` as the page title because it is the operator name used by ESET in the June 2026 SprySOCKS Windows analysis.
- ESET says FishMonger is believed to be operated by I-SOON, falls under the Winnti Group umbrella, and is also known as Earth Lusca, TAG-22, Aquatic Panda, or Red Dev 10.
- Avoid treating contractor, umbrella, and vendor-cluster names as automatically interchangeable outside the source that makes the connection.

## Core tradecraft
- Custom malware and backdoors, including **SprySOCKS**, ShadowPad, Spyder, FunnySwitch, BIOPASS RAT, and Cobalt Strike use documented by ESET.
- Watering-hole operations and targeted delivery against universities and government entities.
- Windows DLL side-loading and encrypted payload containers in the SprySOCKS Windows chain.
- Kernel-driver-assisted stealth in the SprySOCKS `WIN_DRV` variant, including process, file, registry, and network hiding.
- TCP traffic diversion that lets operators reach the backdoor through an apparently random victim TCP port while hiding the real listening port.

## 2026 reporting
### SprySOCKS Windows variants
ESET reported two previously undocumented Windows variants of SprySOCKS, internally marked `WIN_DRV` and `WIN_PLUS`. Both variants include hardcoded C2 configuration, support TCP, UDP, and WebSocket communications, and implement more than 30 C2 commands for host discovery, process enumeration, service management, and file operations.

The `WIN_DRV` variant adds kernel-driver support and network redirection. ESET also saw limited indications that some SprySOCKS attack scenarios may involve a UEFI bootkit component, possibly exploiting CVE-2023-24932, but that part should remain caveated until more public detail is available.

See [SprySOCKS](../tools/sprysocks.md).

## Defender signals
- Unexpected DLL side-loading chains that stage encrypted `.dat` payload containers and then move execution into `%SystemRoot%\Fonts\`.
- Scheduled-task persistence that restarts malware from the Windows Fonts directory.
- Suspicious service-key creation for a minifilter driver named `msidiskserver` and transient driver drops such as `C:\Windows\System32\drivers\fsdiskbit.sys`.
- Kernel-driver activity signed with leaked or unusual certificates, especially on outdated or misconfigured hosts where driver-signature enforcement can be bypassed.
- Hidden backdoor traffic patterns where a random inbound TCP port redirects to a local hidden listener.
- Government-sector endpoints in Honduras, Taiwan, Thailand, Pakistan, and adjacent regions should prioritize review if SprySOCKS indicators appear.

## Related pages
- [SprySOCKS](../tools/sprysocks.md)
- [Velvet Ant](velvet-ant.md)
- [OceanLotus](oceanlotus.md)

## Sources
- ESET WeLiveSecurity: https://www.welivesecurity.com/en/eset-research/fishmongers-arsenal-upgraded-sprysocks-windows/
