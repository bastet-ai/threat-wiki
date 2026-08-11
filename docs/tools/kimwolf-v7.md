# Kimwolf v7

## Summary
**Kimwolf v7** is an Android and internet-of-things DDoS bot documented by Unit 42. It primarily targets Android TV boxes and set-top boxes and belongs to the same operator ecosystem as **AISURU**: public reporting distinguishes AISURU's Linux IoT codebase from Kimwolf's Android codebase.

The v7 payload adds an HTTP/2 flood that builds Chrome-like browser fingerprints and a layered command-and-control design using Ethereum Name Service (ENS) resolution, a Tor hidden-service fallback, and a local proxy. Unit 42 discovered the analyzed variant on February 3, 2026; the research does not establish how many devices ran v7.

## Tags
- tools
- malware
- botnet
- Kimwolf
- Kimwolf v7
- AISURU
- Android
- Android TV
- IoT
- DDoS
- HTTP/2
- browser fingerprint spoofing
- Ethereum Name Service
- blockchain C2
- Tor
- residential proxy abuse
- Android Debug Bridge
- ADB TCP/5555

## Why this matters
- Kimwolf reaches unauthenticated ADB services on private networks through residential-proxy endpoints. An Android TV box can therefore be infected even when TCP/5555 is not directly exposed to the internet.
- Its HTTP/2 flood supplies a fuller browser fingerprint than a basic request flood, reducing the value of header-only bot filtering.
- Five legitimate public Ethereum RPC services provide redundant ENS resolution. Tor and a modular localhost proxy remain available when the clearnet path fails.
- The v7 bot no longer contains scanning, exploitation, or brute-force modules. Unit 42 assesses that propagation has moved to external loaders while the bot focuses on DDoS and proxy relay; absence of scanning in the payload is not evidence of a safe device.
- Unit 42 linked 22 hosts in one Russian address range through a shared SSH host key. Those historical infrastructure observations are useful pivots, not a current bot-size estimate.

## Infection and execution
Kimwolf operators misuse residential proxy services to reach ADB listeners inside subscriber or enterprise networks. Devices that ship with ADB enabled on TCP/5555 can accept unauthenticated malware installation through that tunnel.

The analyzed baseline is a stripped, statically linked 32-bit ARM ELF built with the Android NDK. It uses Bionic libc, BoringSSL, and `nghttp2`, creates an abstract Unix socket containing the internal v7 marker to prevent duplicate execution, and masquerades as `netd_service`.

Unit 42 also identified Android APK wrappers from October through December 2025. They masqueraded as `SystemService`, probed for root access, and launched an embedded ELF. Related payload names included `libdevice.so` and a redacted `lib*kernel.so`; observed process names included `TVHelper` and `inetd`. The earliest x86 sample's `libcow.so` naming and behavior suggested a Dirty COW lineage before the operation shifted toward Android/ADB propagation.

## DDoS capability
The dispatch table contains 15 methods across Layers 3–7, including:

- TCP socket, SYN, ACK, SYN-ACK, RST, connection, and epoll-based floods;
- multiple UDP floods, a game-server UDP method for port 27015, and a DNS flood;
- ICMP flooding;
- TLS/HTTPS flooding with BoringSSL; and
- HTTP/2 flooding with `nghttp2` and Chrome-like request fingerprints.

The high-performance UDP method uses a Xorshift256 generator seeded from `/dev/urandom` and ARM NEON vector instructions to reduce checksum overhead. Defenders should not assume that v7 is only an application-layer HTTP bot.

## Layered command and control
### ENS through public Ethereum RPC
The baseline binary shuffles five legitimate public RPC endpoints before querying ENS:

- `0xrpc[.]io/eth`
- `eth.llamarpc[.]com`
- `ethereum-rpc.publicnode[.]com`
- `eth-protect.rpc.blxrbdn[.]com`
- `eth.merkle[.]io`

These are shared services. Monitor unexpected Ethereum RPC traffic from Android TV and IoT segments, but do not classify the providers themselves as malicious.

Unit 42 assessed with **moderate confidence** that `eth[.]rpcuniverse[.]com` was an operator-controlled RPC facade. The assessment rests on dedicated hosting, registration and certificate timing, exclusive appearance in Kimwolf samples, and direct-to-IP contact by ELF and APK variants; domain ownership was not confirmed.

### Tor and localhost proxy
If ENS resolution fails, v7 can use:

```text
edctgwib2n5l34t525zkxqzk5bqb6e5il2yiq5r6zu7gtlxa4uosn3qd[.]onion
```

The bot implements SOCKS5 negotiation and then performs TLS through the tunnel. Both clearnet and Tor C2 traffic route through `127.0.0.1:23075`, allowing the local proxy component to change independently of the bot binary.

## Public hunt pivots
Treat network infrastructure as historical and time-bounded.

### Files
- Kimwolf v7 baseline ELF SHA-256: `406647de09a0ffa279756b4ccb344b1b76a333320c5b50fd367901fa006cf0ff`
- Additional v7 ELF SHA-256: `345222bca004595977f971d76900b0c65fd9bf9d91c50cd0c5bf5a93f1ad9e49`
- ELF carrying `eth.rpcuniverse[.]com`: `2ec2e85b0358e0c681cb5067489a9086ec97dbbf7e3c952dd9cd496b319d5af5`
- APK `com.android.logcatd`: `951c94809aa6c7ab587125f9d4df30fa6a49ee0cbba76a4b7ceedaaa0e5dcd36`
- APK `com.android.logcatd`: `f07821e313c16cbbd82def45094a22c8d474164051bdbc7648d6869e012014b4`
- Embedded `libdevice.so`: `8242443dfcec66e3fe04cbfa2fbd211ad34065ee07aa93813d792a437caab212`
- APK signing-certificate SHA-1: `2a1d96f1b066877812587ac94f45f82dfff5f5f9`

### Infrastructure
- `23.94.221[.]104` — hosted `rpcuniverse[.]com`; contacted directly by ELF and APK samples
- `212.193.31[.]158:443`
- `212.193.31[.]92:443`
- `212.193.31[.]119:13`
- `212.193.31[.]122:13`
- `212.193.31[.]102` — pivot linked by the shared SSH host key

## Detection and response
- Inventory Android TV boxes, set-top boxes, and other unmanaged Android devices. Disable network ADB, restrict ADB to USB-only operation where possible, and verify that TCP/5555 is not reachable from local, guest, VPN, or residential-proxy paths.
- Segment consumer Android and IoT devices from corporate workstations, identity infrastructure, administration networks, and production services. Treat inexpensive or unsupported TV boxes as untrusted.
- Hunt for `netd_service`, `TVHelper`, or unexpected `inetd` processes on Android/IoT devices; abstract localhost sockets containing a v7 marker; the documented hashes; and unexplained APKs named `com.android.logcatd` or `com.n2.systemservice0644`.
- Alert on blockchain RPC requests from device classes that have no business need for Ethereum, especially when followed by localhost TCP/23075, SOCKS5/Tor activity, or connections to the published C2 range.
- Inspect DDoS telemetry behaviorally. Chrome-like HTTP/2 headers do not prove a browser generated the traffic; correlate request volume, connection reuse, TLS traits, destination concentration, and the source device class.
- If infection is suspected, preserve volatile process, network, ADB, package, proxy, and gateway state before power-cycling. Isolate the device, remove its proxy reachability, reflash with trusted vendor firmware or replace it, and rotate credentials that were configured on or reused from the device.

## Scope and attribution caveats
- Unit 42 links Kimwolf and AISURU to the same operators but describes them as separate Android and Linux codebases.
- The publication analyzes six clustered ELF samples and eight earlier APKs; it does not publish a v7 victim count or prove that every historical Kimwolf device upgraded to v7.
- Public Ethereum RPC endpoints are legitimate shared infrastructure. The operator-control assessment for `eth[.]rpcuniverse[.]com` is moderate-confidence, not confirmed ownership.
- Geolocation of the 22-host C2 cluster to Saint Petersburg does not establish operator nationality or physical location.

## Related pages
- [Dysphoria IoT botnet](../ops/dysphoria-iot-botnet.md)
- [C0XMO Gafgyt DD-WRT botnet](../ops/c0xmo-gafgyt-dd-wrt-botnet.md)
- [NadMesh AI-service and cloud-credential botnet](../ops/nadmesh-ai-service-cloud-credential-botnet.md)
- [Aeternum](aeternum.md)

## Sources
- Unit 42: [Kimwolf v7: An Evolution of the Kimwolf Botnet](https://unit42.paloaltonetworks.com/kimwolf-v7-botnet-malware/)
