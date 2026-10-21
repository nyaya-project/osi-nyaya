---
name: causal-knowledge-mapper
description: Build an evidence-linked causal-claim graph from documents and research questions, preserving provenance, conditions, contradictions, uncertainty, and research gaps. Use for literature-based mechanism mapping and experimental-planning questions.
version: 1.0.0
created_by: agent
---

# Causal Knowledge Mapper

## Purpose

Given a bounded set of sources and a research question, create an inspectable graph of *reported causal claims*. A claim being extracted is **not** a finding that it is true.

This core skill is domain-general. For Nyāya-inspired evidence classification and invariant anchors, load `nyaya-evidence-hierarchy` too.

## Required outputs

Place outputs in a user/project-selected directory, never inside the installed skill:

- `graph.json`: canonical graph conforming to `references/schemas/graph.schema.json`.
- `report.md`: question-focused answer derived from the graph, with citations, contradictions, limitations, and next discriminating checks.
- `validation.json`: machine-readable result from `scripts/validate_graph.py`.
- `run.json`: inputs, source fingerprints where available, scope, method/version, and timestamps.
- Optional: `graph.svg` or `graph.html`, rendered from `graph.json`.

The graph is the source of truth. Do not add claims to the report which are absent from it.

## Workflow

1. **Frame the question.** State the outcome, system boundary, intended decision/use, included sources, excluded sources, and time or operating-condition limits.
2. **Register sources.** Give every source a stable `source_id`. Preserve DOI/URL or local fingerprint and a page, section, figure, table, or other locator.
3. **Extract atomic claims.** Record subject, relation, object, direction/effect sign, conditions, negation, modality, and epistemic status. A source statement is an extraction, not validation.
4. **Normalize without erasing scope.** Consolidate genuine aliases only. Do not merge different compositions, device stacks, protocols, temperatures, timescales, or physical meanings into a single entity.
5. **Attach evidence.** Evidence is claim-specific. Capture quoted or faithfully delimited support, stance, locator, study type, limitations, and verification status. Use `evidence_origin_id` when records share an experiment or primary source.
6. **Reconcile rather than average.** Retain supporting and contradictory records. Explain differences in conditions or unresolved conflicts; do not infer a consensus solely by number of papers.
7. **Validate.** Run `scripts/validate_graph.py graph.json`. Repair only structural/provenance problems. Missing evidence remains unresolved; never invent it to satisfy validation.
8. **Answer narrowly.** Render only the subgraph material to the research question. Separate established observations, inferred mechanisms, hypotheses, and unresolved alternatives.
9. **Propose discriminating next checks.** Identify a measurement, control, intervention, or source inspection that would distinguish important rival explanations.

## Non-negotiable rules

- Preserve `associated_with` as association; never silently promote it to `causes`.
- Direct observation of a phenomenon does not directly establish a mechanism.
- Absence of an edge means **not established in this scoped corpus**, never proof of no relationship.
- Do not count restatements, shared experiments, or citation chains as independent confirmation.
- Cycles and contradictory claims are valid in the knowledge graph. A DAG requirement applies only to a separately selected causal model.
- Record unavailable supplements/references as `unresolved`, not as absent support.
- Use the explicit conditions field whenever scope could change the result.

## Stopping rules

Create an unresolved item instead of guessing when identity is ambiguous, the source cannot be located/read, the relationship direction is unsupported, or a passage lacks enough context to classify.

## References and tooling

- Data contract: `references/schemas/graph.schema.json`
- Run metadata contract: `references/schemas/run.schema.json`
- Method/rubric: `references/method.md`
- Validation: `scripts/validate_graph.py graph.json --output validation.json`
- Example: `references/examples/minimal_graph.json`
