# ClickOnce COM hijacking abuse

## Summary
CrowdStrike documented how Microsoft ClickOnce deployment can be abused as a low-friction Windows execution and persistence surface. The durable defender lesson is broader than a single malware family: trusted deployment plumbing, per-user installs, self-updates, and user-writable COM registration can turn “click once” software distribution into attacker-controlled execution under legitimate Microsoft process trees.

CrowdStrike's June 18, 2026 research describes both known ClickOnce weaponization and a newly disclosed COM-hijacking variant. The new variant defines the hardcoded ClickOnce deployment-service CLSID in the current user's registry hive so the next ClickOnce deployment can launch attacker-selected code before Windows falls back to the legitimate `dfsvc.exe` deployment service.

## Tags
- patterns
- Windows
- ClickOnce
- COM-hijacking
- persistence
- initial-access
- defense-evasion
- endpoint-detection
- software-deployment

## What CrowdStrike described
- ClickOnce applications can be run, installed, and updated with minimal user interaction and normally without administrator privileges.
- Deployment can be initiated through browser download flows, `.application` manifests, `setup.exe`, direct `rundll32.exe` invocation through `dfshim.dll`, or `.appref-ms` application-reference files.
- Offline ClickOnce applications place `.appref-ms` references under the user's Start Menu path, enabling later launches and update checks from the deployment server.
- Malicious or trojanized ClickOnce packages can benefit from legitimate-looking Windows UI and execution chains involving `rundll32.exe`, `dfsvc.exe`, and Microsoft .NET deployment components.
- CrowdStrike's new abuse targets the hardcoded ClickOnce deployment-service CLSID `{20FD4E26-8E0F-4F73-A0E0-F27B8C57BE6F}`.
- An attacker with current-user registry write access can create `HKCU\SOFTWARE\Classes\CLSID\{20FD4E26-8E0F-4F73-A0E0-F27B8C57BE6F}` entries that point COM activation at attacker-controlled code.
- When `dfsvc.exe` is not already running, a later ClickOnce deployment causes `rundll32.exe` / .NET deployment code to attempt COM activation for that CLSID; the attacker-registered server can execute before the deployment flow falls back to the legitimate service.

## Why this matters
- **No admin requirement:** Per-user ClickOnce deployment and per-user COM registration fit standard-user compromises.
- **Legitimate process cover:** Execution can appear under normal Windows deployment components instead of a plainly suspicious downloaded executable.
- **Update-backed persistence:** `.appref-ms` launches and ClickOnce update checks can refresh or replace payloads if an attacker controls the deployment server or trojanized package path.
- **Low user friction:** A web button, manifest file, or application reference can be enough to trigger deployment.
- **Non-overwrite COM hijack:** CrowdStrike notes the new variant defines a COM object that is normally absent rather than overwriting an existing registration, reducing obvious breakage.

## Defender heuristics

### Prevent and reduce exposure
- Treat ClickOnce as executable software deployment, not just a document or web-download flow.
- Restrict untrusted `.application`, `.appref-ms`, and ClickOnce `setup.exe` launches through application control where business use allows.
- Require trusted signing and known deployment origins for ClickOnce applications used in the enterprise.
- Review which business applications legitimately use ClickOnce, then baseline their deployment URLs, publisher identities, Start Menu `.appref-ms` paths, and update cadence.
- Avoid assuming standard users are safe from software-install persistence; ClickOnce and HKCU COM registration are both user-writable paths.

### Detection pivots
- Alert on creation or modification of:
  - `HKCU\SOFTWARE\Classes\CLSID\{20FD4E26-8E0F-4F73-A0E0-F27B8C57BE6F}`
  - `HKCU\SOFTWARE\Classes\CLSID\{20FD4E26-8E0F-4F73-A0E0-F27B8C57BE6F}\LocalServer32`
  - `HKCU\SOFTWARE\Classes\CLSID\{20FD4E26-8E0F-4F73-A0E0-F27B8C57BE6F}\InprocServer32`
- Hunt for `rundll32.exe` invoking `dfshim.dll` with `ShOpenVerbApplication` or related ClickOnce activation paths from unusual parents, downloads, archives, chat clients, or browser cache locations.
- Hunt for unusual `dfsvc.exe` starts, `rundll32.exe` → `dfsvc.exe` sequences, and delayed deployment flows where an unexpected process launches before `dfsvc.exe`.
- Inventory `.appref-ms` files in user Start Menu and Startup locations, especially newly created entries or references to unfamiliar domains, IP addresses, file shares, or user-writable paths.
- Monitor scheduled tasks, Run keys, Startup folders, and script launchers that open `.appref-ms` files instead of launching a normal executable.
- Correlate ClickOnce deployment activity with outbound requests to new deployment servers and file writes under `%LocalAppData%\Apps\2.0\` or `%TEMP%\Deployment\`.

### Incident response
- Preserve registry hives before cleanup when ClickOnce COM hijacking is suspected.
- Capture `.application`, `.manifest`, `.appref-ms`, and downloaded application files; the deployment metadata is often the fastest way to identify origin, update URL, and publisher claims.
- Terminate malicious deployment processes only after collecting process command lines, parent/child relationships, loaded modules, and network connections.
- Revoke or block malicious ClickOnce deployment URLs at proxy, DNS, and endpoint controls.
- Remove malicious HKCU COM registration and malicious `.appref-ms` persistence entries for every affected user profile, not just the active profile.

## Related pages
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Microsoft Teams external-chat phishing](microsoft-teams-external-chat-phishing.md)
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)

## Sources
- CrowdStrike: https://www.crowdstrike.com/en-us/blog/new-abuse-of-the-clickonce-technology-part-one.html
- CrowdStrike: https://www.crowdstrike.com/en-us/blog/new-abuse-of-the-clickonce-technology-part-two.html
