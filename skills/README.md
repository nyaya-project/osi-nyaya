# Portable skills

This directory versions the shareable, non-secret Hermes skills used by the OSI Nyaya work.

- [`causal-knowledge-mapper/`](causal-knowledge-mapper/) builds a provenance-linked graph of causal claims, evidence, conditions, contradictions, and unresolved research gaps.
- [`nyaya-evidence-hierarchy/`](nyaya-evidence-hierarchy/) applies the project-defined Nyāya-inspired evidence classes and scoped `vyapti`/`upadhi` review.

The skills contain no runtime profile state, credentials, tokens, sessions, memories, or logs.

To install them in a compatible Hermes profile, copy each skill directory into that profile's `skills/` directory, preserving its contents. The causal-mapper skill's generated `graph.json`, `report.md`, `run.json`, and validation outputs belong in a project output directory, not in the installed skill.
