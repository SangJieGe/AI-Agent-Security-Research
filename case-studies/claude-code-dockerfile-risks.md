# Case Study: AI-Generated Dockerfile Risks

## Context

AI assistants often generate Dockerfiles that build successfully but encode insecure defaults. These risks are frequently accepted in early development and later shipped into production pipelines.

## Common Risk Patterns

### 1) Running as root

**Pattern:** No `USER` directive, container runs with root privileges.

**Risk:** Privilege escalation impact increases significantly if application compromise occurs.

**Mitigation:** Create dedicated non-root user and set ownership explicitly.

### 2) Mutable `latest` tags

**Pattern:** `FROM node:latest` or similar.

**Risk:** Non-deterministic builds and unreviewed upstream changes.

**Mitigation:** Pin explicit version and digest.

### 3) `chmod 777` overuse

**Pattern:** Broad write permissions on app directories.

**Risk:** Weakens filesystem integrity and enables tampering.

**Mitigation:** Apply least-privilege permissions and ownership-specific access.

### 4) Secret exposure in layers

**Pattern:** `ENV API_KEY=...` or `ARG TOKEN=...` persisted in build history.

**Risk:** Credential leakage via image history, registry access, or scanning tools.

**Mitigation:** Inject secrets at runtime using secret managers or orchestration secrets.

### 5) `curl | bash` install flows

**Pattern:** Piping remote script output directly to shell.

**Risk:** Supply-chain compromise or MITM leads to arbitrary code execution.

**Mitigation:** Verify checksums/signatures and use trusted package sources.

### 6) Broad `COPY . .`

**Pattern:** Copying full repository context into image.

**Risk:** Includes unnecessary files (`.env`, keys, test fixtures), expanding attack surface.

**Mitigation:** Use explicit `COPY` targets and strict `.dockerignore`.

### 7) Unnecessary package installation

**Pattern:** Installing editors, compilers, and debugging tools in runtime image.

**Risk:** Enlarges attack surface and vulnerability footprint.

**Mitigation:** Use multi-stage builds and minimal runtime base images.

### 8) Missing healthcheck

**Pattern:** No `HEALTHCHECK` for long-running service containers.

**Risk:** Delayed detection of failure states, weak recovery behavior.

**Mitigation:** Add health checks aligned with real application readiness/liveness.

### 9) Excessive runtime privileges

**Pattern:** Container expects privileged mode or root-like capabilities.

**Risk:** Host-level impact if compromised.

**Mitigation:** Drop Linux capabilities, enforce seccomp/apparmor profiles, read-only FS where feasible.

## Example: Safer Baseline Snippet

```Dockerfile
FROM python:3.12.3-slim@sha256:<digest>

RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
USER app

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',8080))"

CMD ["python", "-m", "src.main"]
```

## Operational Takeaway

Treat AI-generated Dockerfiles as untrusted drafts. Enforce policy-as-code checks for image provenance, privilege level, secret handling, and package minimization before merge.
