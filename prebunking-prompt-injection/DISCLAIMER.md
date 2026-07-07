# Disclaimer

## Purpose

This research is conducted for **defensive security purposes only**. The goal is to understand how indirect prompt injection attacks can be amplified by psychological "prebunking" narratives, in order to inform the design of more robust runtime safety defenses for AI agent systems.

## Scope

- All experiments were performed in a **local sandbox environment** (localhost only).
- **No real third-party systems, APIs, or users were targeted or affected.**
- All API keys, credentials, and data used in the experiments are **fabricated test data** (e.g., `sk-test-FAKE1234567890abcdef`).
- The mock server (`localhost:8000`) simulates an external data collection endpoint but processes no real information.

## What This Repository Is NOT

- This is **NOT** a ready-to-use attack toolkit. The payloads and agent harness are designed for experimental replication in controlled laboratory settings, not for deployment against production systems.
- The payloads, while functional in the experimental setup, are **minimally weaponized** — they target a toy ReAct agent with a known tool set and mock endpoints, not real-world LLM applications.

## Ethical Use

- If you use this code or methodology in your own research, please:
  1. Run experiments in isolated sandbox environments.
  2. Use only fabricated test data.
  3. Cite this work appropriately.
  4. Do not deploy these payloads against production systems without explicit authorization.

## Reporting

If you discover security vulnerabilities based on insights from this research, we encourage responsible disclosure to the affected vendors or platform providers.

## Contact

For questions, open an issue on this repository or contact the repository owner.
