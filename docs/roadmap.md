# Roadmap

## Phase 1: Baseline Foundation

- Publish baseline controls for AI-assisted SDLC and agent runtime operations.
- Build initial case studies around infrastructure-as-code and container risks.
- Define taxonomy for workflow-level attack surfaces.

## Phase 2: Workflow Attack Graphing

- Model multi-step agent execution paths across tools and systems.
- Identify privilege-escalation edges and trust-boundary crossings.
- Produce reusable graph templates for common CI/CD patterns.

## Phase 3: Agent Permission Analysis

- Implement methods to map granted vs. required permissions.
- Detect over-scoped identities in AI-driven workflows.
- Add policy checks for least-privilege conformance.

## Phase 4: MCP Risk Scanner

- Develop checks for connector/server identity, auth, and transport controls.
- Detect unsafe tool exposure and cross-domain data flow risks.
- Add baseline policy packs for MCP deployments.

## Phase 5: AI-Generated Code Scoring

- Build a scoring framework for common AI-generated vulnerability classes.
- Prioritize findings by exploitability and operational impact.
- Integrate scoring into pull request and CI workflows.

## Phase 6: Runtime Observability

- Define telemetry schema for prompt/tool/action traceability.
- Build anomaly detection rules for agent behavior drift.
- Integrate observability outputs with incident response workflows.
