# Cloud bucket namespace hijacking

## Summary
Unit 42 disclosed a cross-cloud bucket-hijacking technique on June 22, 2026: if an attacker can delete a storage bucket that is the destination for logs, replication, transfer jobs, Pub/Sub delivery, Firehose delivery, or Azure Monitor diagnostics, they may be able to recreate the same globally unique name under attacker control and silently receive the victim's continuing data stream.

Track this as a reusable cloud pattern, not an actor operation. The issue is the combination of long-lived router resources, globally unique storage names, and overbroad delete permissions. Unit 42 reported no observed in-the-wild use at publication time, but warned that successful attempts could be difficult to detect because the original data stream may keep working while the destination identity has changed.

Wiz added a related multi-provider risk on July 31, 2026: S3-compatible object stores in newer cloud platforms preserve global bucket namespaces and presigned-URL behavior while often omitting AWS's mature secret-detection, quarantine, least-privilege, logging, public-access, and transport assumptions. An attacker can pre-register names that software expects to create, not only reclaim a deleted destination. Treat S3 API compatibility as a protocol property, not evidence that AWS security controls or semantics are present.

## Tags
- patterns
- cloud security
- cloud storage
- bucket hijacking
- namespace squatting
- data exfiltration
- AWS S3
- Google Cloud Storage
- Azure Storage
- logging
- replication
- least privilege
- dangling resources
- S3-compatible storage
- neocloud
- access keys
- presigned URLs

## Reported technique
1. A cloud environment has a data router that writes to object storage by bucket or storage-account name.
2. The attacker compromises an identity with storage deletion rights, or finds a dangling router after a legitimate bucket deletion.
3. The original bucket or storage account is deleted and the global name becomes reusable.
4. The attacker recreates the same name in an attacker-controlled account, project, subscription, or tenant scope.
5. The existing router keeps delivering logs, replicated objects, messages, or transfer outputs to the new destination.
6. Defenders may see a still-valid routing configuration while the data is now leaving the trusted boundary.

## Provider-specific shapes from Unit 42

### Google Cloud
- Demonstrated with Cloud Logging sinks that export logs to Cloud Storage.
- Also tested against Pub/Sub subscriptions writing to GCS and Storage Transfer Service jobs writing to a destination GCS bucket.
- Relevant permissions called out by Unit 42 include `storage.objects.delete` to empty a bucket and `storage.buckets.delete` to remove it.
- The practical risk is that storage-delete permissions can bypass the more obvious route-update permissions, such as `logging.sinks.update`, `pubsub.subscriptions.update`, or `storagetransfer.jobs.update`.
- Unit 42 said Google adjusted how router resources interact with target storage resources after the research.

### AWS
- Demonstrated with S3 bucket replication: after a destination bucket was deleted and recreated under an external account with the same name, replicated objects appeared in the attacker-controlled bucket.
- Unit 42 also observed the same behavior in an Amazon Data Firehose path where S3 was the destination.
- AWS account regional namespaces for S3 general purpose buckets are a direct mitigation where available because the bucket name is scoped to the owning account and region rather than the single global namespace.

### Azure
- Unit 42 found the Azure variant less severe than AWS or Google Cloud because storage-account names could not be immediately reused cross-tenant in the same way.
- The demonstrated path was cross-subscription inside the same tenant, with Azure Monitor diagnostic settings exporting logs to Azure Storage.
- The report notes that although the configuration stores an Azure Resource Manager resource ID, the internal pipeline resolves the storage account at runtime through its DNS name, such as `{accountname}.blob.core.windows.net`.
- The attack depended on recreating a storage account with the same globally unique name and soft-delete conditions that allowed the name to be released.

## Why this matters
- **Name is not ownership**: globally unique storage names are human-readable routing targets, not immutable security principals.
- **Delete can become redirect**: identities with broad storage administrator roles may not need direct permission to modify the sink, subscription, transfer job, replication rule, or diagnostic setting.
- **Backups and retention paths are quiet targets**: long-term retention buckets may not be watched as closely as production databases, and autonomous routers can keep sending data after a destination swap.
- **Dangling routers extend exposure**: deleting a bucket without removing the associated sink, replication, transfer, or diagnostic configuration can leave an interception path.

## S3-compatible clone risk

Wiz examined object storage from Nebius, Crusoe, Vultr, Lambda Labs, Cloudflare, DigitalOcean, and other providers that expose subsets of the S3 API. The research did not report exploitation; it documented control and semantic gaps defenders should validate before treating a clone like AWS S3.

### Namespace and API assumptions
- S3-compatible services maintain provider-specific global namespaces. An attacker may reserve names that follow predictable region, environment, customer, or tool-generated patterns and cause software to read from or write to an attacker-owned bucket.
- Compatibility can be partial or misleading. Wiz observed one implementation return list results through a bucket-policy API shape and map a policy-deletion request to bucket deletion. Validate destructive behavior in a non-production tenant rather than assuming AWS API semantics.
- Public-access behavior varies by provider and control plane. Some services do not support public buckets, while others expose public access through provider APIs, ACLs, or bucket policies; anonymous listing may be blocked even when known objects remain retrievable.

### Credential and least-privilege gaps
- Clone access keys may use non-AWS prefixes, unstructured values, or unexpected lengths. Existing secret scanners, GitHub quarantine workflows, and detection rules may not recognize them consistently.
- GitHub secret scanning covers some DigitalOcean and Cloudflare credentials, but defenders should not infer equivalent coverage for every provider or key type.
- Wiz found materially different authorization depth. Cloudflare and DigitalOcean supported some bucket-scoped or read-only controls, and Cloudflare supported IP restrictions; Nebius offered limited policy controls. The tested Vultr, Crusoe, and Lambda Labs access keys lacked comparable least-privilege capabilities.
- Some provider APIs can return long-lived access and secret keys after creation, contrary to the common AWS expectation that a secret is shown only once. Inventory every administrative API that can reveal object-storage credentials.

### Presigned URLs, encryption, and logs
- S3 signing compatibility carries presigned-URL bearer risk into every clone. URLs may be reusable until expiry and can leak through browser history, extensions, proxies, support captures, analytics, or application logs.
- Do not inherit AWS encryption assumptions. Verify at-rest encryption, minimum TLS policy, customer-managed-key support, and key-rotation behavior per provider; Wiz noted that Cloudflare object storage supported TLS 1.0 by default at publication time.
- Verify both control-plane and object-level data-plane audit coverage. A service may log bucket creation and deletion without recording `GetObject`, `PutObject`, or equivalent activity needed to investigate exposure or theft.

## Defender heuristics

### Reduce blast radius
- Remove broad storage-delete permissions from day-to-day workload, developer, and CI identities.
- Separate data-router administration from storage-destination deletion rights.
- Require break-glass review for destructive permissions such as Google Cloud `storage.buckets.delete`, AWS S3 bucket deletion actions, and Azure `Microsoft.Storage/storageAccounts/delete`.
- Keep an inventory of logging sinks, Pub/Sub export subscriptions, transfer jobs, S3 replication rules, Firehose destinations, and Azure Monitor diagnostic settings that write to object storage.
- Reserve predictable bucket names before deploying applications, and make bucket creation an authenticated infrastructure-provisioning step rather than an implicit runtime fallback.
- Replace broad clone credentials with bucket-scoped, read-only, IP-bound, or short-lived credentials where supported; isolate providers that cannot express the required privilege boundary.
- Add provider-specific access-key patterns and validation to secret scanning. Avoid committing example keys that resemble live credentials, and test revocation and quarantine workflows with synthetic canaries.

### Keep data inside the boundary
- Use AWS service control policies and VPC endpoint policies to prevent organizational workloads from writing to S3 buckets owned by external accounts.
- Use Google Cloud VPC Service Controls to block access to Cloud Storage buckets outside the expected perimeter.
- Prefer bucket and storage-account controls that bind destination use to an owning account, project, subscription, organization, or immutable resource identifier where the provider supports it.
- In AWS, evaluate S3 account regional namespaces for new designs that need bucket-name reuse protection.

### Detect and respond
- Alert on bucket or storage-account deletion, especially for destinations attached to logs, backups, replication, message delivery, transfer jobs, data lakes, and security telemetry.
- Correlate deletion events with immediate same-name bucket or storage-account creation in another account, project, subscription, region, or tenant boundary.
- Monitor router resources for destination-owner drift, not just destination-name drift.
- During cloud incident response, verify that every configured storage destination still belongs to the expected organization and that recent data landed in the expected account or project.
- If hijacking is suspected, scope what logs, objects, messages, diagnostics, and transfer outputs were delivered after the deletion time and rotate secrets that appeared in those streams.
- Alert when applications unexpectedly create buckets, switch S3 endpoint URLs, encounter an already-owned expected name, or access a bucket whose owner/account identifier differs from deployment inventory.
- Redact query strings from presigned-URL logging and review browser, proxy, analytics, ticketing, and observability retention when a URL is exposed.
- Test that object reads, writes, ACL or policy changes, credential retrieval, and bucket deletion generate usable audit events before storing sensitive data.

## Related pages
- [Cloud logging control-plane tampering](cloud-logging-control-plane-tampering.md)
- [Vertex AI staging-bucket squatting](vertex-ai-staging-bucket-squatting.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/cloud-bucket-hijacking-risks/](https://unit42.paloaltonetworks.com/cloud-bucket-hijacking-risks/)
- Wiz Research: [S3 Clones in the Neoclouds](https://www.wiz.io/blog/s3-clones-in-the-neoclouds)
