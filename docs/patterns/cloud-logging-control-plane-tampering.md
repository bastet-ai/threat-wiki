# Cloud logging control-plane tampering

## Summary

Unit 42 describes a reusable cloud-defense-evasion pattern: attackers who gain permissions over logging control planes can blind downstream security tools, poison forensic records, or route victim telemetry to infrastructure they control. The research focuses on AWS CloudTrail and Google Cloud Logging, but the defender lesson is broader: cloud audit-log configuration is a privileged security control, not ordinary plumbing.

The durable risk is two-sided:
- **Defense evasion** — stop logging, delete or alter log routing, delete the log destination, make encrypted logs unreadable, or modify stored log objects.
- **Continuous visibility** — create or change log routes so victim activity is copied to an attacker-controlled destination, reducing the need for noisy discovery commands.

## Tags
- patterns
- cloud security
- cloud logging
- defense evasion
- continuous visibility
- AWS CloudTrail
- Google Cloud Logging
- log poisoning
- MITRE ATT&CK T1562
- MITRE ATT&CK T1005

## Operational shape

### Stop or impair logging
- Disable logging directly, such as stopping an AWS CloudTrail trail or changing Google Cloud Logging collection / sink behavior.
- Delete the log-routing resource, such as an AWS trail or Google Cloud sink, so new events stop flowing to the expected destination.
- Delete or alter the storage destination, such as the S3 bucket or cloud log bucket / exported destination receiving the records.
- Change encryption-key access so logs continue to exist but responders can no longer read them.

### Poison forensic records
- If logs are written to mutable object storage, an attacker with storage permissions can delete, add, or modify JSON log objects.
- Unit 42 highlights AWS CloudTrail log file integrity validation as a mitigation for detecting post-delivery tampering; it is enabled by default for console-created trails, but not for API or CLI-created trails.

### Turn logging into reconnaissance
- Create a new log-routing resource that copies logs to an attacker-controlled account, bucket, sink, or analytics destination.
- Change an existing route so defenders may still see some telemetry while the attacker also receives real-time operational visibility.
- This can support quiet discovery of users, roles, services, data stores, and incident-response activity without repeatedly calling noisy enumeration APIs.

## Defender heuristics

### Treat logging configuration as tier-zero
- Restrict permissions such as AWS `UpdateTrail`, `DeleteTrail`, CloudTrail destination-bucket policy changes, Google Cloud `logging.sinks.update`, and log-destination administration to a small set of privileged identities.
- Separate duties: identities that administer workloads should not automatically be able to disable or redirect security logging.
- Require change control and peer review for audit-log routing, destination, retention, and encryption-key changes.

### Alert on routing and destination changes
- Alert on creation, deletion, disabling, or update of CloudTrail trails, Google Cloud sinks, log buckets, destination buckets, Pub/Sub topics, BigQuery exports, EventBridge / CloudWatch integrations, and KMS / Cloud KMS keys used for logs.
- Baseline known log destinations and alert when routes point to unfamiliar accounts, projects, regions, buckets, topics, or external identities.
- Watch for rapid sequences: privilege change → logging update → storage-policy or KMS change → high-value data access.

### Preserve immutable fallbacks
- In AWS, use the 90-day CloudTrail Event History for management events as a fallback, but remember it does not cover all data and network events.
- In Google Cloud, rely on built-in `_Required` audit logs for Admin Activity and System Event records, but do not assume external SIEM export paths are equally protected.
- Enable integrity validation where available and store high-value audit logs in write-once / retention-locked storage where operationally feasible.

### Response checks
- During cloud incident response, verify that logging is still enabled, still routed to approved destinations, still readable, and still complete.
- Review recent log-routing changes before trusting an apparent gap in telemetry.
- If attacker-controlled destinations are suspected, scope what logs were copied and whether sensitive payloads, secrets, or investigation activity appeared in those logs.

## Related pages
- [PCPJack cloud SMTP relay network](../ops/pcpjack-cloud-smtp-relay-network.md)
- [UNC6692 SNOW malware social-engineering campaign](../ops/unc6692-snow-malware-social-engineering.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/cloud-logging-defense-evasion/](https://unit42.paloaltonetworks.com/cloud-logging-defense-evasion/)
