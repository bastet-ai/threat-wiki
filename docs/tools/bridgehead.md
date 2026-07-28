# BridgeHead

## Summary
**BridgeHead** is a Mirage Kitten Windows WebSocket tunneler described by Kaspersky in July 2026. Once connected, it acts as a SOCKS5 relay: the operator selects destinations from the server side and traffic exits through the compromised host and victim network.

## Tags
- tool
- tools
- BridgeHead
- Mirage Kitten
- UNC1549
- Windows
- WebSocket
- WSS
- SOCKS5
- tunneling
- proxy
- NTLM
- Negotiate
- enterprise proxy
- username environmental keying
- espionage

## Reported deployments
- `%LocalAppData%\Microsoft\VisualStudio\unbcl.dll` on a machine in Egypt.
- `C:\program files (x86)\univpn\promote\libwinpthread-1.dll` in a Pakistan-based environment.
- A second variant communicated with `businessmixture[.]com/blog` over WSS rather than Azure-hosted infrastructure.

## Environmental keying
- BridgeHead dynamically resolves `GetUserNameA`, lowercases the current username, and requires a hard-coded substring to be present before activating.
- Kaspersky assessed this as evidence of prior reconnaissance and per-target tailoring. It also limits accidental execution in analysis systems.

## Network behavior
- One reported build upgrades `GET /connect` to a WebSocket at `smartconnect[.]azurewebsites[.]net`, then sends the literal binary message `token`.
- The implant handles HTTP `407 Proxy Auth Required`, preferring Windows **Negotiate** and then **NTLM**, and retries with the current user's integrated SSO context.
- It uses exponential retry backoff capped at 60 seconds.
- The binary protocol supports connect, response, data, disconnect, ping, pong, and flow-control messages with SOCKS5-formatted IPv4, domain, or IPv6 destinations.

## Defender heuristics
- Hunt for unexpected WebSocket upgrades from user workstations to Azure Websites or newly registered business-themed domains, especially followed by long-lived bidirectional traffic.
- Correlate HTTP 407 responses and Negotiate/NTLM proxy authentication with DLLs loaded from Visual Studio or UniVPN-like user and program directories.
- Look for `unbcl.dll`, unexpected `libwinpthread-1.dll`, and outbound `/connect` or `/blog` WSS sessions.
- Per-user variants mean a sample that exits in a sandbox is not proof of benign behavior; preserve and test with the victim context isolated from production.

## Public indicators
- `6038D42AF0AFFD1FB263F470C0956F6B` — `unbcl.dll`
- `AE628EFA305387B633DCE82F9364875B` — `unbcl.dll`
- `F7D36CC5904A53252D2BB3D21615134F` — `libwinpthread-1.dll`
- `C90F0EFADBF322E5EB1C4103A38C30E6` — `libwinpthread-1.dll`
- `D09B14A2FE01C7363ECC56F5D046162C` — `IPHLPAPI.dll`
- `C832ECD135781B11F59E3FFFB3D2B6AC` — separately described WSS variant

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](../ops/mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [ArcBridge](arcbridge.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
