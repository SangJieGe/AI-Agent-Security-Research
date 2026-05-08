# AI Agent Security Research

A technical research repository focused on production security risks in AI-assisted software development and autonomous workflow execution.

## Focus Areas

- AI-generated code security: insecure defaults, unsafe dependencies, hidden attack paths.
- Agent runtime risks: excessive permissions, unsafe execution paths, lateral movement potential.
- Workflow attack surfaces: CI/CD, GitHub Actions, artifact flow, and automation trust chains.
- MCP security: trust boundaries, tool authorization, and cross-connector data exposure.
- AI DevSecOps: controls for integrating AI tooling into secure software delivery.
- Tool permission boundaries: least privilege design for shells, APIs, repos, and cloud resources.
- AI deployment risks: runtime governance, observability, and incident response for AI-driven operations.

## Repository Structure

- `baselines/` - security baselines and control checklists.
- `case-studies/` - technical analyses of realistic failures and exploit paths.
- `workflow-risks/` - agent workflow threat models and anti-pattern documentation.
- `mcp-security/` - Model Context Protocol trust and authorization research.
- `ai-generated-code/` - patterns and findings in AI-produced code vulnerabilities.
- `tools/` - scripts and prototypes for detection, scoring, and validation.
- `benchmarks/` - measurable test scenarios and evaluation datasets.
- `payloads/` - controlled test inputs and red-team style fixtures.
- `docs/` - project roadmap and supporting architecture notes.

## Initial Research Scope

1. Baseline controls for AI-enabled SDLC pipelines.
2. Common vulnerability classes in AI-generated infrastructure code.
3. Agent/tool trust boundaries in local and cloud runtime environments.
4. Security telemetry requirements for agent-driven automation.
5. Permission minimization strategies for tool-calling agents.

## Roadmap Snapshot

- Workflow attack graphing for multi-step agent execution.
- Permission analysis engine for agent/tool invocation paths.
- MCP risk scanner for connector and server policy drift.
- AI-generated code scoring model for security review prioritization.
- Runtime observability primitives for AI-assisted operations.

See `docs/roadmap.md` for planned phases.

## Planned Tooling

- Static rule packs for AI-generated code anti-pattern detection.
- Policy checks for CI/CD and GitHub Actions hardening.
- MCP trust-boundary linting and connector permission analysis.
- Baseline conformance scoring for AI-assisted repositories.

## Contributing

Contributions are expected to be reproducible, evidence-based, and technically specific. See `CONTRIBUTING.md` and `SECURITY.md` before submitting.
