# AI Agent Security Baseline v0.1

## AI-generated code review

- Require human review for AI-generated changes affecting authentication, authorization, cryptography, deserialization, shell execution, and CI/CD configuration.
- Require static analysis and dependency scanning before merge.
- Block merges when generated code introduces insecure defaults (for example disabled TLS verification or permissive wildcard policies).

## GitHub Actions permissions

- Set default workflow permissions to read-only (`permissions: read-all`) and elevate per job only when required.
- Restrict `contents: write`, `actions: write`, and `id-token: write` to narrowly scoped jobs.
- Pin third-party actions by commit SHA.

## Secret handling

- Do not expose long-lived secrets to workflows triggered by forks or untrusted pull requests.
- Use short-lived credentials via OIDC federation when possible.
- Mask and redact secret values from logs, artifacts, and step outputs.

## Dockerfile review

- Pin base images to explicit versions or digests.
- Use non-root runtime users unless a documented exception exists.
- Remove build-only tooling from runtime stages.

## Shell execution restrictions

- Disallow high-risk shell patterns in generated scripts (`curl|bash`, unbounded wildcard deletes, dynamic command eval).
- Apply command allowlists and argument validation for automation agents.
- Require reviewer approval for newly introduced shell execution in workflows.

## MCP trust boundaries

- Treat each MCP connector/server as a separate trust domain.
- Enforce per-tool authorization scopes and deny-by-default access.
- Log MCP tool calls with identity, scope, and target resource metadata.

## CI/CD approval controls

- Require CODEOWNERS or protected-environment approval for workflow file changes.
- Require security checks before auto-merge of AI-generated pull requests.
- Restrict deployment jobs to protected branches and trusted actors.

## Runtime observability

- Emit audit events for prompt-to-change lineage, workflow edits, and privileged executions.
- Alert on anomalous permission expansion or secret access patterns.
- Preserve tamper-evident logs for incident response.
