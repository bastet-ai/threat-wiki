# ArcBridge

## Summary
**ArcBridge** is a separate Mirage Kitten WebSocket tunneling tool first identified by Kaspersky in April 2026 activity targeting the Middle East. It accepts server-side commands to open operator-selected proxy sessions and resolve hostnames or addresses.

## Tags
- tool
- tools
- ArcBridge
- Mirage Kitten
- UNC1549
- Windows
- WebSocket
- tunneling
- proxy
- DNS resolution
- embedded configuration
- mutex
- Middle East
- espionage

## Configuration and behavior
- ArcBridge creates mutex `F56E68DA-4A89-46B4-9AC8-7290A7651000` to enforce one running instance.
- Kaspersky recovered an embedded configuration delimited by `<<STARTXX>>` and `<<ENDXX>>`.
- The example configuration contained C2 host `aecert[.]org`, port `443`, value `5000`, SSL flag `0`, and probable implant identifier `4B8CC395-A26F-41F1-A1DC-8B993D9D41D2`.
- `OPEN:` directs the client to create a proxy or tunnel session to an operator-selected target.
- `DNS:` resolves a hostname or address and returns the result.

## Defender heuristics
- Search binaries and memory for `<<STARTXX>>`, `<<ENDXX>>`, `OPEN:`, `DNS:`, and the UUID-style mutex.
- Correlate WebSocket-like egress with subsequent access to internal destinations or DNS resolution not expected from the originating process.
- Treat a fixed C2 or implant identifier as one campaign pivot, not a complete signature; Kaspersky reports a broader actor shift from Azure-style hosts toward Cloudflare-backed domains.

## Public indicators
- `5FA15EF96808EA82F0A6176F0BB4B386`
- `42F847597109DA2A220391BB09D00676`
- `AFB1C1583606599C7272CFB33CC6F498`
- `aecert[.]org`

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](../ops/mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [BridgeHead](bridgehead.md)

## Sources
- Kaspersky GReAT: [Mirage Kitten targets Middle East and Africa region with new malware](https://securelist.com/mirage-kitten-new-tools/120811/)
