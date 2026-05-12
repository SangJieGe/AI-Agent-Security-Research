# AI Agent Security Research

Research repository focused on AI agent security, AI-generated code risks, workflow attack surfaces, MCP security, and AI DevSecOps.

## Current Scope

This repository documents early-stage, engineering-focused security research for AI-assisted development and automation workflows.

### Active research areas
- AI-generated code risk patterns and review controls.
- GitHub Actions and CI/CD attack surfaces in AI-assisted workflows.
- MCP trust boundaries and tool authorization concerns.
- Practical baseline controls for AI-enabled software delivery.

## Background Reading

- [`docs/ai-security-landscape-2026.md`](docs/ai-security-landscape-2026.md) — AI Security Landscape 2026 (ZH): A panoramic overview of LLM security, AI Agent security, and AI-assisted security research. Provides the conceptual foundation for this repository's research scope.
- [`docs/agent-governance-ai-devsecops-2026.md`](docs/agent-governance-ai-devsecops-2026.md) — When the State Starts Regulating Agents: Policy, Engineering Reality, and the Rise of AI DevSecOps (ZH, 2026-05)
- [`docs/ai-security-three-directions-2026.md`](docs/ai-security-three-directions-2026.md) — AI Security 的三个方向 2026 (ZH): Analysis of how AI security is diverging into LLM Security, Agentic Security, and AI for Security — with focus on MCP protocol risks, memory poisoning, emergent组合式 vulnerabilities, and AI-assisted vulnerability research.

## Repository Structure (current)

- `baselines/` - concise security baseline guidance.
- `case-studies/` - technical writeups of concrete attack paths.
  - [ai-generated-dockerfile-risks.md](case-studies/ai-generated-dockerfile-risks.md) — AI-Generated Dockerfile Security Risks: insecure defaults, supply chain drift, and compounding vulnerabilities in agentic pipelines.
- `docs/` - roadmap and planning notes.

## Current Documents

- `baselines/ai-agent-security-baseline-v0.1.md`
- `case-studies/github-actions-ai-agent-risks.md`
- `case-studies/claude-code-dockerfile-risks.md`
- `docs/roadmap.md`

## Contributing

Contributions should be technically specific, reproducible, and evidence-based. See `CONTRIBUTING.md` and `SECURITY.md` before submitting.
