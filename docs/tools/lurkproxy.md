# LurkProxy

## Summary
**LurkProxy** is a Windows network-proxy implant reported by Kaspersky GReAT alongside OctLurk and SilkLurk. It shares a heavily obfuscated loader and broadly similar architecture with OctLurk but is not itself a general-purpose backdoor. The analyzed build listened on all interfaces on TCP/64980 and created a TLS-encrypted proprietary channel to attacker infrastructure, forwarding traffic as a SOCKS5 reverse proxy.

## Tags
- tools
- malware
- proxy
- LurkProxy
- Windows
- SOCKS5
- transparent proxy
- lateral movement
- encrypted C2
- environmental keying
- cyber-espionage

## Behavior
- Uses an OctLurk-like loader with double-XOR and zlib-protected content.
- Listens on `0.0.0.0:64980` in the reported configuration.
- Connects to `154.196.162[.]76` over TLS and uses a proprietary compressed and double-XOR-encrypted binary protocol.
- Supports two statically selected modes: SOCKS5 reverse proxy or transparent forwarding to a fixed target. Kaspersky observed SOCKS5 mode.
- Opens target connections through C2, forwards bidirectional raw TCP data, and lets the controller pause or terminate sessions.

## Public indicators
- C2: `dns.ssentialserv[.]xyz`, `154.196.162[.]76`.
- Representative deployment script MD5: `b874123a80fc4f40e06872b9cb54ebc6` (`auto.bat`).
- Representative service: `Cusrxsrv` loading `msbasesysdc.dll` through its `RegisterService` export.
- Additional reported service names associated with the broader loader family include `specitsrc`, `cmtastsvc`, `PNRPHostSvc`, `vmictimerosync`, and `vmicagent`.

## Defender notes
- Alert on new TCP/64980 listeners, especially service-hosted or unsigned processes with outbound TLS to the public indicators.
- Correlate the listener with new services, remote scheduled tasks, OctLurk/SilkLurk artifacts, and subsequent internal connections that do not match the host's role.
- During response, inspect routing and connection telemetry to identify downstream systems reached through the proxy; removing the implant does not scope lateral movement.
- Block inbound access to unnecessary high ports and restrict server egress so compromised services cannot become network pivots.

## Related pages
- [OctLurk and SilkLurk Central Asia espionage campaign](../ops/octlurk-silklurk-central-asia-espionage.md)
- [OctLurk](octlurk.md)
- [SilkLurk](silklurk.md)

## Sources
- Kaspersky GReAT: [https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/](https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/)
