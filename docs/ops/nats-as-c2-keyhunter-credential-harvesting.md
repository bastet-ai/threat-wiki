# NATS-as-C2 KeyHunter credential-harvesting operation

## Summary
Sysdig Threat Research reports a May 2026 intrusion in which an unknown actor exploited an internet-reachable Langflow instance through **CVE-2026-33017**, harvested cloud credentials, and attempted to enroll the compromised host into a distributed credential-harvesting worker pool coordinated through **NATS**.

The durable signal is the command-and-control architecture. Instead of a conventional HTTP panel, Discord bot, or Telegram channel, the actor used an authenticated NATS message broker with subject-level ACLs and JetStream-style durable task queues. Sysdig dubbed the technique **NATS-as-C2**; the operator called the worker project **KeyHunter**.

## Tags
- ops
- operations
- cloud credential theft
- AI credential theft
- C2
- NATS
- JetStream
- Langflow
- CVE-2026-33017
- KeyHunter
- LLMjacking
- code sandbox scraping
- AWS
- Bedrock
- AI agents
- uTLS
- gitleaks

## Why this matters
- NATS gives operators queue durability, pub/sub fan-out, pull consumers, explicit acknowledgements, and role-scoped subjects without building custom botnet infrastructure.
- The observed worker model joined cloud-key validation and AI-token validation in one pipeline, creating parallel monetization paths through AWS access, Bedrock / LLMjacking, and SaaS model-provider keys.
- The worker targeted online code-sandbox platforms such as CodePen, JSFiddle, StackBlitz, and CodeSandbox, not just GitHub, reflecting a quieter source of pasted developer secrets.
- Subject-level ACLs limited what a captured worker could publish or subscribe to, showing least-privilege botnet design: compromise of one node did not automatically expose the operator command stream.
- The operation connects exploitation of AI workflow runtimes with cloud and model-provider abuse: Langflow RCE led directly to environment theft, AWS reconnaissance, and attempted worker deployment.

## Reported chain
1. Sysdig observed probes against LMDeploy and LiteLLM surfaces before the actor shifted to a Langflow target.
2. The actor exploited Langflow **CVE-2026-33017** through `/api/v1/build_public_tmp//flow` and dumped process environment variables.
3. Harvested AWS credentials were replayed quickly through `sts:GetCallerIdentity` and then used for reconnaissance across Bedrock, S3, EC2, Cost Explorer, Lambda, CloudWatch Logs, ECS, SageMaker, SSO, and IAM.
4. The actor attempted to deploy two worker paths from `159.89.205.184:8888`: a Python fallback worker and a stripped Go binary.
5. The worker configuration pointed at an authenticated NATS broker at `45.192.109.25:14222` and exposed task subjects such as `task.scan_cde`, `task.scan_web`, `task.validate_aws`, and `task.validate_ai`.
6. ACL errors forced live debugging of allowed publish subjects such as `heartbeat.worker`, `worker.hb`, `result.scan`, `kh.result`, and `keyhunter.result`.
7. The Go worker failed in the captured environment with a runtime memory panic and a leaked Windows build path; the Python worker remained the operational path.

## Tool characteristics
- **KeyHunter worker identity:** Python worker IDs used a `py-XXXXXX` pattern and declared capabilities for code-development-environment scraping, web scraping, AWS validation, and AI-key validation.
- **AWS validation:** the worker used the same liveness check seen in the manual intrusion path: `sts:GetCallerIdentity` followed by account / ARN / user-ID capture.
- **AI-key validation:** Sysdig reported model-provider validation logic and Bedrock invocation attempts consistent with direct LLMjacking monetization.
- **Code-sandbox scraping:** the Go binary carried dedicated extraction logic for CodePen, JSFiddle, StackBlitz, and CodeSandbox, including multiple fallback strategies per platform.
- **uTLS fingerprint mimicry:** imports of `github.com/refraction-networking/utls` indicate browser-ClientHello impersonation to evade JA3/JA4-style bot detection in front of code-sandbox services.
- **Headless-browser sidecar:** the CodeSandbox fallback path used a sidecar process for rendered web content, suggesting the scraper could handle JavaScript-heavy pages.
- **JetStream consumers:** `PullSubscribe` plus explicit acknowledgements match durable NATS task queues where dropped workers return tasks for redelivery.
- **Secret detection:** Sysdig observed regex coverage for AWS, GitHub, OpenAI, Anthropic, Google, Slack, Stripe, private keys, JWTs, database URLs, and optional `gitleaks` use.

## Defender heuristics
- Treat exploitation of Langflow, LiteLLM, LMDeploy, notebook, and AI-workflow runtimes as immediate secret-spill incidents; rotate cloud, model-provider, SaaS, database, repository, and CI/CD tokens reachable from the process environment or workspace.
- Hunt for outbound NATS traffic, especially unusual connections to high ports such as TCP `14222`, NATS protocol banners, or subjects containing `task.scan_*`, `validate_aws`, `validate_ai`, `worker.hb`, `kh.result`, or `keyhunter.result`.
- Correlate AI-runtime exploitation with near-immediate AWS API sweeps: `sts:GetCallerIdentity`, `bedrock:InvokeModel`, `bedrock:ListInferenceProfiles`, `s3:ListBuckets`, `ec2:DescribeInstances`, `ce:GetCostAndUsage`, `lambda:ListFunctions`, `logs:DescribeLogGroups`, `ecs:ListClusters`, `sagemaker:ListEndpoints`, `sso:ListInstances`, and IAM policy enumeration.
- Monitor code-sandbox, paste, and snippet platforms for leaked organizational credentials; do not limit secret-scanning programs to GitHub repositories.
- Flag unexpected `utls`, `gitleaks`, headless-browser sidecar, or code-sandbox scraper artifacts on servers that recently exposed AI or developer workflow applications.
- Block or inspect outbound message-broker protocols from workloads that should only make application egress; NATS, MQTT, AMQP, Redis pub/sub, and Kafka-like channels can all become durable C2 planes.
- Preserve staging artifacts and memory before cleanup; worker configs may reveal broker endpoints, subject names, ACL boundaries, and tasking semantics.

## Related pages
- [Langflow CVE-2025-34291 exploitation](langflow-cve-2025-34291-exploitation.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [oob.moika.tech dependency-confusion environment stealer](oob-moika-dependency-confusion-env-stealer.md)

## Sources
- Sysdig Threat Research: <https://www.sysdig.com/blog/nats-as-c2-inside-a-new-technique-attackers-are-using-to-harvest-cloud-credentials-and-ai-api-keys>
