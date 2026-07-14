# LabubaRAT

## Summary
Blackpoint Cyber's July 14, 2026 analysis, summarized publicly by The Hacker News, describes **LabubaRAT** as a previously undocumented Rust-based Windows remote-access trojan that masquerades as NVIDIA software. The sample reported as `nvidia-sysruntime.exe` impersonates NVIDIA container-runtime tooling while enrolling hosts into a reusable operator-controlled RAT framework.

The durable defender point is the framework design: LabubaRAT separates runtime configuration from the compiled payload, persists local state in SQLite, profiles browsers and security products, and can shift among HTTPS, WebView2, and DNS-tunneling communications. That makes one binary reusable across infrastructure and victim sets instead of a one-off loader.

## Tags
- tools
- malware
- RAT
- remote access trojan
- Rust malware
- Windows
- NVIDIA impersonation
- LabubaRAT
- LabubaPanel
- malware-as-a-service
- HTTPS C2
- WebView2 C2
- DNS tunneling
- SOCKS5 proxy
- PowerShell execution
- JavaScript execution
- screenshot capture
- SQLite state
- security-tool discovery
- Blackpoint Cyber

## Why this matters
- The reported sample accepts C2 and polling configuration at launch, either as individual command-line values or a Base64-encoded argument, so defenders should not rely only on hard-coded infrastructure extraction.
- Local SQLite state plus runtime configuration lets operators reuse the same compiled payload across deployments and change infrastructure without rebuilding the binary.
- LabubaRAT profiles the host before tasking, including browsers, endpoint/security tools, hostname, RAM, CPU model, and Windows UAC state.
- Its communication options provide fallback paths: HTTPS, WebView2, and DNS tunneling can keep operator access alive after one channel is blocked.
- The tool is broad enough for hands-on intrusion work: command execution, PowerShell, JavaScript, file transfer, archive handling, screenshots, and SOCKS5 proxying.
- Public reporting notes signs the tooling may be offered as malware-as-a-service; track LabubaRAT as a tool family rather than a single campaign.

## Execution and configuration
- Reported masquerade filename: `nvidia-sysruntime.exe`.
- Reported lure/cover: NVIDIA container runtime tooling.
- Configuration can be supplied on the command line instead of embedded in the binary.
- The reported C2 example was `pipicka[.]xyz`.
- The malware stores configuration/state in a local SQLite database after launch.
- Naming pivots include the `LabubaPanel` C2 panel title and a Labubu-themed favicon.

## Capabilities
- Host profiling and environment discovery.
- Browser and security-product inventory.
- Operator command execution.
- PowerShell execution.
- JavaScript execution.
- Screenshot capture.
- File upload and download.
- Archive handling.
- SOCKS5 proxy support.
- Multiple C2 paths: HTTPS, WebView2, and DNS tunneling.

## Defender heuristics
- Hunt for binaries named like NVIDIA runtime components, especially `nvidia-sysruntime.exe`, outside expected NVIDIA install paths and without valid NVIDIA signing / installation provenance.
- Alert on NVIDIA-looking processes launched with unusual long Base64 command-line arguments, C2-looking hostnames, or polling-interval parameters.
- Investigate non-browser processes that create WebView2 runtime activity and then initiate suspicious external communications.
- Baseline DNS tunneling indicators from endpoints: high-entropy subdomains, unusual query volume from workstation processes, and DNS traffic correlated with RAT-like process creation.
- Monitor for new SQLite databases created by suspicious user-writable binaries, especially when followed by security-tool discovery or outbound C2.
- Treat host profiling of many security products from a newly dropped binary as intrusion staging; LabubaRAT reportedly checks for Microsoft Defender, CrowdStrike, SentinelOne, Carbon Black, Sophos, Malwarebytes, Bitdefender, ESET, Kaspersky, McAfee, Symantec, and Trend Micro.
- Combine process-lineage detections for command / PowerShell / JavaScript execution with screenshot capture or SOCKS proxy behavior from the same process.

## Related pages
- [Djinn Stealer](djinn-stealer.md)
- [TaskWeaver](taskweaver.md)
- [QuimaRAT](quimarat.md)
- [ScreenConnect freeware / AsyncRAT SEO campaign](../ops/screenconnect-freeware-asyncrat-seo-campaign.md)

## Sources
- Blackpoint Cyber: https://blackpointcyber.com/blog/labubarat-a-rust-based-remote-access-tool-masquerading-as-nvidia-software/
- The Hacker News: https://thehackernews.com/2026/07/labubarat-masquerades-as-nvidia.html
