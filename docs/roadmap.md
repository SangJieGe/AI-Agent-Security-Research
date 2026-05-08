# Roadmap

This roadmap tracks planned research directions. Items are exploratory and may change as findings mature.

---

## Near-term (current focus)

- Expand case studies for AI-assisted CI/CD and deployment workflows.
- Refine baseline controls with implementation examples and detection heuristics.
- Add MCP security analysis for tool trust boundaries and authorization gaps.
- Document real-world AI-generated code failure patterns observed in production-adjacent workflows.

## Medium-term

- **MCP trust boundary research**: Map authorization scope escalation paths across common MCP server implementations. Analyze how tool schemas can be abused to bypass intended access controls.
- **Workflow attack chain analysis**: Document end-to-end attack chains from untrusted PR to secret exfiltration or deployment compromise. Focus on multi-step scenarios that cross trust boundaries.
- **Agent permission mapping**: Build a reference for how agent-to-tool execution paths inherit and propagate permissions across GitHub Actions, MCP, and cloud IAM.
- **Detection heuristics**: Draft practical detection rules for risky AI-generated workflow changes — patterns that security teams can implement as CI checks.

## Research questions

- How do AI assistants handle permission escalation suggestions in workflow YAML?
- What are the failure modes when MCP tools have overlapping scope boundaries?
- Can we define a minimal set of policy-as-code rules that catches 80% of AI-generated workflow risks?
- What artifact provenance signals are most reliable for detecting supply chain compromise in CI/CD?

## Scope limitations

This is an individual researcher project. Work prioritizes depth over breadth — better to have three well-documented case studies than ten shallow outlines. Contributions that add concrete, reproducible findings are welcome.
