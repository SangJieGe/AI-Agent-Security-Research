# AI Agent Security Baseline v0.1

Early-stage, actionable security controls for AI-assisted development workflows.

This baseline targets teams using AI coding assistants, CI/CD automation agents, and MCP-connected toolchains.

---

## AI-generated code review

- Require human review for AI-generated changes affecting authentication, authorization, cryptography, deserialization, shell execution, and CI/CD configuration.
- Require static analysis (Semgrep, CodeQL, or equivalent) and dependency scanning before merge.
- Block merges when generated code introduces insecure defaults (for example disabled TLS verification, permissive wildcard policies, or hardcoded credentials).
- Flag AI-generated PRs with a label so reviewers apply heightened scrutiny to trust-critical paths.

## GitHub Actions permissions

- Set default workflow permissions to read-only (`permissions: read-all`) and elevate per job only when required.
- Restrict `contents: write`, `actions: write`, and `id-token: write` to narrowly scoped jobs with explicit justification.
- Pin third-party actions by full commit SHA (not mutable tags like `v4` or `main`).
- Require CODEOWNERS review on all changes to `.github/workflows/`.
- Audit `pull_request_target` usage — prefer `pull_request` for untrusted contributions.

## Secret handling

- Do not expose long-lived secrets to workflows triggered by forks or untrusted pull requests.
- Use short-lived credentials via OIDC federation when possible.
- Mask and redact secret values from logs, artifacts, and step outputs.
- Never use `env | sort` or similar debug patterns in jobs that handle secrets.
- Scope secrets per environment (dev/staging/production) — do not share across all workflows.
- Rotate credentials on a defined schedule; audit access logs quarterly.

## Dockerfile review

- Pin base images to explicit versions or digests (`@sha256:...`).
- Use non-root runtime users unless a documented exception exists.
- Remove build-only tooling from runtime stages (use multi-stage builds).
- Avoid `curl | bash` install patterns — verify checksums or use trusted package registries.
- Use explicit `COPY` targets instead of `COPY . .` to avoid leaking `.env`, keys, or test fixtures.
- Add `HEALTHCHECK` directives for long-running service containers.

## Shell execution restrictions

- Disallow high-risk shell patterns in generated scripts (`curl|bash`, unbounded wildcard deletes, dynamic `eval`).
- Apply command allowlists and argument validation for automation agents.
- Require reviewer approval for newly introduced shell execution in workflows.
- Treat all GitHub event fields (`github.event.*`) as untrusted input — never interpolate directly into `run:` blocks.
- Use environment variables with explicit validation instead of direct expression interpolation.

## MCP trust boundaries

- Treat each MCP connector/server as a separate trust domain.
- Enforce per-tool authorization scopes and deny-by-default access.
- Log MCP tool calls with identity, scope, and target resource metadata.
- Validate tool input schemas server-side — do not trust client-provided parameters blindly.
- Implement rate limiting and timeout controls on MCP tool invocations.
- Audit MCP configurations for overly broad filesystem, network, or command access.

## CI/CD approval controls

- Require CODEOWNERS or protected-environment approval for workflow file changes.
- Require security checks (SAST, dependency scan, secret scan) before auto-merge of AI-generated pull requests.
- Restrict deployment jobs to protected branches and trusted actors.
- Use GitHub Environments with protection rules for production deployments.
- Require manual approval for workflow changes that modify permission scopes or trigger conditions.

## Runtime observability

- Emit audit events for prompt-to-change lineage, workflow edits, and privileged executions.
- Alert on anomalous permission expansion or secret access patterns.
- Preserve tamper-evident logs for incident response.
- Track which AI assistant generated which code change (commit metadata, PR labels).
- Monitor for unexpected outbound network connections from CI runners.

---

## Version history

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-05 | Initial baseline — CI/CD, code review, MCP, runtime controls |
