# SatyOne — Security, Privacy and AI Governance Baseline

Status: Engineering baseline. Last reviewed: 12 November 2026.

## 1. Current posture
The current product is a local-first single-user starter: React/Vite, FastAPI, SQLAlchemy and SQLite, with an optional server-side OpenAI adapter. Production-grade identity, tenant isolation, secrets vault, audit service and public multi-user authorization are not established. The saved-prompt owner_key is an ownership label, not authentication. Unauthenticated saved-prompt endpoints must remain local-only until real authentication and authorization exist.

## 2. Trust boundaries
Treat user prompts, uploaded files, pasted code, generated text/code/JSON/tool arguments, retrieved webpages/documents, third-party APIs, plugins, packages and provider metadata as untrusted. Never execute generated code or tool instructions merely because a model produced them.

## 3. Local edition minimum controls
- Bind API to loopback by default; do not unintentionally expose it to LAN/public internet.
- Restrict CORS to exact local origins.
- Keep environment files, SQLite database, backups and logs out of Git.
- Validate inputs and cap text size, upload size, request frequency and execution time.
- Use parameterized ORM/database operations.
- Avoid returning stack traces, filesystem paths, secrets or provider internals.
- Pin or lock dependencies and review advisories.
- Back up SQLite safely; protect backups with OS permissions and encryption where appropriate.
- Document that SQLite is not automatically encrypted, synchronized or backed up.

## 4. Before public multi-user release
**Identity:** established authentication, secure sessions/tokens, server-derived identity, object-level authorization, tenant isolation, recovery, session revocation and appropriate MFA.

**API:** per-user/IP rate limits, request-size limits, timeouts, concurrency and quotas; input validation; context-aware output encoding; CSRF protection for cookie auth; HTTPS, secure headers, trusted hosts and strict CORS.

**Secrets:** server-side secret storage, rotation/revocation, least-privilege scopes, usage caps and redaction. Never expose provider credentials in VITE variables, browser bundles, source maps, URLs, logs or prompts.

**Data:** inventory and classification; purpose, retention, access, deletion and backup lifecycle; encryption in transit and at rest for hosted production; privileged-access logs; incident response.

**Operations:** database migrations, tested backups/restores, dependency and secret scanning, monitoring, vulnerability disclosure, staging, rollback and patch ownership.

## 5. AI-specific threat controls
Use OWASP Top 10 for LLM Applications 2025 as a threat checklist:
- Prompt injection: retrieved content is data, not authority.
- Sensitive information disclosure: minimize/redact secrets and personal data.
- Supply chain: verify models, packages, plugins, datasets and connectors.
- Data/model poisoning: track source and integrity of catalogue/retrieval content.
- Improper output handling: validate schemas and encode rendered output.
- Excessive agency: least privilege, narrow tools, bounded steps and approvals.
- System prompt leakage: never put secrets or authorization rules only in hidden prompts.
- Vector/embedding weaknesses: tenant-isolate indexes and enforce retrieval authorization.
- Misinformation: show sources, uncertainty and verification state.
- Unbounded consumption: quotas, timeouts, token budgets, caching and cost alerts.

## 6. Agent and automation safety
Each tool declares name/version, schema, permissions/resources, read-only or side-effect status, risk, step/call budget, approval requirement, timeout/retry/cancel behavior and audit policy. Require fresh explicit human confirmation before sending, publishing, purchasing, deleting, changing permissions, modifying production data or other consequential side effects. Models cannot expand their own permissions. Stop must halt queued actions.

## 7. Logging
Log security-relevant metadata: event ID, timestamp, actor, action, resource, outcome, correlation ID, provider/model/version, cost metadata, approval and policy version. Avoid raw prompts, credentials, personal data and uploaded content by default. Define retention and access controls.

## 8. Secure development lifecycle
Threat-model each new integration; review permissions/data flows/terms; add validation and authorization tests; run unit/integration/negative tests; scan dependencies and secrets; review accessibility/privacy/security; release to staging; monitor errors/cost/abuse; maintain rollback and incident response; reassess after material changes.

## 9. Production release blockers
A feature is not production-ready if it trusts client-supplied identity, exposes secrets to the browser, executes untrusted model output without sandboxing/approval, lacks object-level authorization, permits unbounded cost or side effects, stores personal data without purpose/retention/deletion, or lacks cancellation and auditability for high-risk actions.

## References
- OWASP Top 10:2025: https://top10.owasp.org/2025/
- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
- CERT-In Directions: https://www.cert-in.org.in/Directions70B.jsp
- MeitY DPDP Rules: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
