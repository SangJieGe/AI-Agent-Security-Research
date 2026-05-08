# Case Study: GitHub Actions Risks in AI-Agent-Assisted Repositories

## Context

AI assistants increasingly generate or modify GitHub Actions workflows. Small changes in YAML can materially change trust boundaries, token scope, and secret exposure paths.

This case study documents common failure modes and practical mitigations for repository maintainers.

## Threat model assumptions

- Repository accepts pull requests from contributors, including forks.
- AI tooling is used to propose or apply workflow changes.
- Workflows may access secrets, artifacts, deployment credentials, or cloud federation.

## 1) `GITHUB_TOKEN` permission risks

### Failure mode

Workflow-level write permissions are granted by default or over-broadened for convenience.

```yaml
name: ci
on: [push, pull_request]
permissions: write-all
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

`write-all` allows unnecessary repository mutation paths (for example creating tags/releases, altering issues, or writing checks) if any step is compromised.

### Mitigation

Use read-only defaults and job-scoped elevation.

```yaml
permissions: read-all
jobs:
  release:
    permissions:
      contents: write
      id-token: write
```

## 2) `pull_request_target` abuse

### Failure mode

`pull_request_target` runs in the base repository context and can access secrets/tokens intended for trusted code. If the workflow checks out attacker-controlled PR code and executes it, secret compromise becomes plausible.

```yaml
on:
  pull_request_target:
    types: [opened, synchronize]
jobs:
  pr-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./scripts/run-tests.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

### Mitigation

- Prefer `pull_request` for untrusted contributions.
- If `pull_request_target` is required, do not execute PR code before policy gates.
- Split metadata/comment workflows from build/test workflows.

## 3) AI-generated workflow modification risks

### Failure mode

AI-generated updates may introduce subtle but high-impact changes such as:

- adding privileged permissions blocks,
- changing triggers to execute on more events,
- introducing unpinned third-party actions,
- adding shell steps that process untrusted inputs.

Example risky delta:

```yaml
- uses: vendor/action@v2
+ uses: vendor/action@main
```

Mutable references create supply-chain drift and make review reproducibility difficult.

### Mitigation

- Require CODEOWNERS review on `.github/workflows/**`.
- Enforce policy checks (forbidden patterns: `write-all`, unpinned actions, unsafe `pull_request_target` execution).
- Require provenance notes for AI-generated workflow PRs.

## 4) Secret exposure risks

### Failure mode

Secrets leak through logs, outputs, artifacts, or command tracing.

```yaml
- name: Debug env
  run: env | sort
```

Even masked values can leak via transformed outputs, base64 wrappers, or copied files uploaded as artifacts.

### Mitigation

- Disable verbose debugging on jobs handling secrets.
- Avoid passing secrets through shell arguments when possible.
- Scope secrets by environment and workflow purpose.
- Prevent secrets on fork-triggered workflows.

## 5) Artifact poisoning

### Failure mode

One workflow uploads build artifacts that are later consumed by a separate privileged workflow without provenance validation.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
```

If the producing workflow is attacker-influenced, downstream jobs may deploy tampered binaries/scripts.

### Mitigation

- Separate untrusted build artifacts from release artifacts.
- Verify artifact origin (workflow, commit SHA, signer identity) before promotion.
- Use attestations/signatures and enforce verification in deployment workflows.

## 6) Shell execution chains

### Failure mode

Workflow shells execute user-controlled values without sanitization.

```yaml
- name: Run label command
  run: ./tools/${{ github.event.label.name }}.sh
```

An attacker controlling label names or PR metadata can influence command execution paths.

### Mitigation

- Treat all GitHub event fields as untrusted input.
- Map external input through strict allowlists.
- Prefer purpose-built actions over dynamic shell expansion.

## 7) Excessive GitHub Actions permissions

### Failure mode

Repository settings grant broad Actions capabilities (write tokens, broad reusable workflow trust, permissive self-hosted runner access) inconsistent with project risk.

### Mitigation checklist

- Restrict workflow permissions at repository level to read by default.
- Limit which actions/reusable workflows are allowed.
- Restrict self-hosted runner groups to trusted repositories and branches.
- Require environment protection rules for deployment secrets.

## Practical review checklist for workflow PRs

1. Does the PR add or broaden token permissions?
2. Does it introduce/modify `pull_request_target`?
3. Are all third-party actions pinned by commit SHA?
4. Are any secrets exposed to untrusted triggers?
5. Are artifacts promoted across trust boundaries without verification?
6. Do shell commands execute untrusted inputs?

## Conclusion

In AI-assisted repositories, workflow YAML must be treated as security-sensitive code. The highest-risk issues are usually not syntax errors; they are trust-boundary mistakes: token overreach, unsafe triggers, untrusted code execution, and artifact trust failures.
