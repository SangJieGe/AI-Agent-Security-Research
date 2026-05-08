# Case Study: GitHub Actions Risks in AI-Agent-Assisted Repositories

## Context

AI assistants increasingly generate or modify GitHub Actions workflows. Small changes in YAML can materially change trust boundaries, token scope, and secret exposure paths.

This case study documents common failure modes and practical mitigations for repository maintainers.

## Threat model assumptions

- Repository accepts pull requests from contributors, including forks.
- AI tooling is used to propose or apply workflow changes.
- Workflows may access secrets, artifacts, deployment credentials, or cloud federation.

---

## 1) `GITHUB_TOKEN` permission risks

### Failure mode

Workflow-level write permissions are granted by default or over-broadened for convenience.

```yaml
name: ci
on: [push, pull_request]
permissions: write-all    # <-- overly broad
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

`write-all` grants the `GITHUB_TOKEN` full access to:

| Scope | Risk |
|-------|------|
| `contents: write` | Push commits, create/delete tags, modify releases |
| `issues: write` | Close/modify issues, inject misleading metadata |
| `pull-requests: write` | Merge PRs, approve reviews, manipulate labels |
| `actions: write` | Cancel/rerun workflows, modify secrets |
| `packages: write` | Push poisoned container images |
| `deployments: write` | Trigger unauthorized deployments |
| `id-token: write` | Request OIDC tokens for cloud federation |

If any step in the workflow is compromised (via dependency, action, or injected input), an attacker inherits all these capabilities.

### Mitigation

Use read-only defaults and job-scoped elevation:

```yaml
permissions: read-all   # safe default
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test

  release:
    needs: test
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: write
      id-token: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make release
```

---

## 2) `pull_request_target` abuse

### Failure mode

`pull_request_target` runs in the **base repository context** and can access secrets/tokens intended for trusted code. If the workflow checks out attacker-controlled PR code and executes it, secret compromise becomes plausible.

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
          ref: ${{ github.event.pull_request.head.sha }}  # attacker-controlled
      - run: ./scripts/run-tests.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}   # leaked to fork code
```

**Attack scenario:**
1. Attacker forks repo, modifies `scripts/run-tests.sh` to exfiltrate `API_KEY`
2. Opens PR — workflow triggers on `pull_request_target`
3. Workflow checks out attacker's SHA and runs their script
4. Secret is exfiltrated to attacker-controlled endpoint

### Mitigation

- Prefer `pull_request` for untrusted contributions (runs in fork context, no secrets).
- If `pull_request_target` is required, do **not** check out PR code before approval gates.
- Use `github.event.pull_request.head.sha` only for metadata, not execution.

```yaml
on:
  pull_request_target:
    types: [labeled]    # only trigger after manual label
jobs:
  check:
    if: contains(github.event.pull_request.labels.*.name, 'safe-to-test')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./scripts/ci-check.sh
```

---

## 3) AI-generated workflow modification risks

### Failure mode

AI-generated updates may introduce subtle but high-impact changes:

```yaml
# Before (pinned, safe)
- uses: vendor/action@v3

# After (AI "updated" to latest)
- uses: vendor/action@main   # mutable ref, supply-chain risk
```

Other patterns AI assistants commonly introduce:

- Adding `permissions: write-all` "to fix permission errors"
- Changing `pull_request` to `pull_request_target` "to access secrets"
- Inserting `env | sort` debug steps that leak masked secrets
- Using `${{ github.event.* }}` directly in `run:` blocks without sanitization

### Mitigation

- Require CODEOWNERS review on `.github/workflows/**`.
- Enforce policy-as-code checks (e.g., `actionlint`, custom OPA/Rego rules).
- Require provenance notes for AI-generated workflow PRs.

---

## 4) Secret exposure paths

### Failure mode

Secrets leak through multiple vectors:

**Direct log exposure:**
```yaml
- name: Debug
  run: echo "API key is ${{ secrets.API_KEY }}"   # masked but risky
```

**Indirect exposure via env dump:**
```yaml
- name: Debug environment
  run: env | sort    # ALL secrets visible in logs
```

**Artifact leakage:**
```yaml
- name: Upload debug logs
  uses: actions/upload-artifact@v4
  with:
    name: debug
    path: /tmp/     # may contain .env, tokens, credentials
```

**Shell expansion:**
```yaml
- name: Process PR title
  run: |
    TITLE="${{ github.event.pull_request.title }}"
    eval "echo $TITLE"    # command injection via PR title
```

### Mitigation

- Never echo or log secret values, even masked ones.
- Avoid `env | sort` in jobs handling secrets.
- Use `::add-mask::` for dynamically generated sensitive values.
- Scope secrets by environment and workflow purpose.
- Prevent secrets on fork-triggered workflows.

---

## 5) Artifact poisoning

### Failure mode

One workflow uploads build artifacts that are later consumed by a separate privileged workflow without provenance validation.

```yaml
# Untrusted build workflow
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/

# Privileged deploy workflow (separate file)
- uses: actions/download-artifact@v4
  with:
    name: build-output
- run: ./deploy.sh    # deploys tampered binary
```

If the producing workflow is attacker-influenced (via compromised dependency, injected code, or PR manipulation), downstream jobs may deploy tampered binaries.

### Mitigation

- Separate untrusted build artifacts from release artifacts.
- Verify artifact origin (workflow, commit SHA, signer identity) before promotion.
- Use attestations/signatures and enforce verification in deployment workflows.
- Consider `actions/attest-build-provenance` for supply chain integrity.

---

## 6) Shell execution chains

### Failure mode

Workflow shells execute user-controlled values without sanitization.

```yaml
- name: Run label command
  run: ./tools/${{ github.event.label.name }}.sh

- name: Process issue body
  run: |
    BODY="${{ github.event.issue.body }}"
    curl -X POST -d "$BODY" https://internal-api.example.com/hook
```

An attacker controlling label names, issue bodies, or PR metadata can influence command execution paths.

### Mitigation

- Treat all GitHub event fields as untrusted input.
- Map external input through strict allowlists.
- Prefer purpose-built actions over dynamic shell expansion.
- Use environment variables with validation, not direct interpolation.

---

## 7) Workflow trigger scope creep

### Failure mode

AI-generated workflows often add unnecessary triggers:

```yaml
on:
  push:
    pull_request:
    issue_comment:      # <-- why?
    workflow_dispatch:
    schedule:
      - cron: '0 * * * *'   # hourly, for a CI workflow?
```

Each trigger expands the attack surface and may activate in unexpected contexts.

### Mitigation

- Document why each trigger exists.
- Remove triggers that don't serve a clear purpose.
- Be especially cautious with `issue_comment` (anyone can trigger) and `schedule` (runs unattended).

---

## Practical review checklist for workflow PRs

1. Does the PR add or broaden token permissions?
2. Does it introduce or modify `pull_request_target`?
3. Are all third-party actions pinned by commit SHA?
4. Are any secrets exposed to untrusted triggers?
5. Are artifacts promoted across trust boundaries without verification?
6. Do shell commands execute untrusted inputs?
7. Are there unnecessary triggers that expand attack surface?
8. Does any step dump environment variables or secrets to logs?

---

## Conclusion

In AI-assisted repositories, workflow YAML must be treated as security-sensitive code. The highest-risk issues are usually not syntax errors — they are trust-boundary mistakes: token overreach, unsafe triggers, untrusted code execution, and artifact trust failures.

Review workflow changes with the same rigor you would apply to IAM policy modifications.
