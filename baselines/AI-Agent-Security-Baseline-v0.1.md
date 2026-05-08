# AI Agent Security Baseline v0.1

## 1) AI-Generated Code Review

- Require human security review for AI-generated code touching auth, crypto, deserialization, shell execution, file I/O, and network egress.
- Enforce static analysis and dependency scanning before merge.
- Flag insecure defaults (`verify=False`, weak ciphers, permissive CORS, debug mode in prod).
- Require provenance notes when code is generated from prompts that include architecture/security assumptions.

## 2) Secret Handling

- Disallow hardcoded secrets and long-lived tokens in prompts, source, or logs.
- Use secret managers (cloud KMS/Secrets Manager/Vault) with short-lived credentials.
- Redact secrets from agent transcripts and tool execution logs.
- Scope credentials per workflow, per environment, and per task.

## 3) Dangerous Shell Execution

- Block raw shell execution for high-risk commands by default (`curl|bash`, privilege escalation, unrestricted `rm`).
- Require allowlists for command families and argument validation.
- Enforce no-network or egress-restricted mode for untrusted generation tasks.
- Capture full command provenance (who/what prompted execution, timestamp, repo ref).

## 4) CI/CD Risks

- Prevent agent-generated pipeline changes from auto-merging without policy checks.
- Require branch protection, signed commits where feasible, and mandatory security checks.
- Pin actions, containers, and dependencies to immutable versions.
- Restrict artifact trust: verify signatures and provenance before deployment.

## 5) GitHub Actions Risks

- Minimize `GITHUB_TOKEN` permissions; default to read-only.
- Avoid `pull_request_target` with untrusted code paths unless carefully sandboxed.
- Pin third-party actions by commit SHA, not mutable tags.
- Isolate secrets from workflows triggered by forks/untrusted contributors.

## 6) Dockerfile Risks

- Disallow `latest` base images; pin digest or explicit version.
- Require non-root runtime user and explicit file ownership.
- Forbid embedding credentials and sensitive build args in layers.
- Minimize installed packages; remove build-only tools from runtime image.

## 7) Terraform Risks

- Require policy checks for public exposure, over-broad IAM, and open security groups.
- Block wildcard IAM (`*`) unless documented exception approved.
- Enforce remote state encryption and state access controls.
- Detect drift and unauthorized changes before apply.

## 8) MCP Trust Boundaries

- Treat each MCP server/tool as a separate trust domain.
- Require explicit tool authorization policies by action and data scope.
- Validate connector identity and transport security.
- Log tool calls with principal, scope, and resource targets.

## 9) Agent Permission Minimization

- Use task-scoped, time-bounded credentials.
- Separate read/write/execute capabilities per workflow stage.
- Deny filesystem/network access not required for task objective.
- Apply just-in-time approval for privileged operations.

## 10) Runtime Observability

- Emit audit events for prompt context, tool calls, code diffs, and deployment actions.
- Correlate agent actions with identity, repository, and environment metadata.
- Alert on anomalous behavior (sudden permission expansion, unusual command patterns).
- Preserve tamper-evident logs for investigations.

## 11) Token Scope Control

- Use least-privilege OAuth/PAT scopes for repos and automation services.
- Rotate tokens automatically and revoke on inactivity.
- Segment tokens by environment and blast radius.
- Enforce policy checks to reject over-scoped tokens in CI.
