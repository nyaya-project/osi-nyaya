---
name: nyaya-evidence-hierarchy
description: "Apply a Nyāya-inspired evidence hierarchy to research claims: pratyaksha (direct observation), anumana (inference), upamana (analogy), shabda (assertion/testimony), plus scoped vyapti anchors and upadhi review."
version: 1.0.0
created_by: agent
---

# Nyāya-Inspired Evidence Hierarchy

## Use

Use with `causal-knowledge-mapper` when evidence needs transparent classification by how a source supports a claim, when citation chains must be traced, or when principles are proposed as anchor constraints.

This is a **project-defined, Nyāya-inspired scientific framework**, not a claim that traditional terms have been exhaustively or universally translated into these operational labels.

## Classify support, not papers

One paper may yield several evidence classes. Classify each evidence record for the specific claim it supports or challenges.

- **Pratyaksha**: the relevant phenomenon is directly observed or measured in the source's reported work. Capture observable, method, locator, conditions, controls, and limitations.
- **Anumana**: conclusion inferred through a model, mechanism, statistical analysis, or explicit reasoning. Record premises/evidence IDs, model/reasoning, assumptions, and plausible alternatives.
- **Upamana**: claim transferred by comparison with a reference system. Record the reference system, similarity basis, material differences, and why transfer is proposed.
- **Shabda**: source asserts the claim without data or substantive derivation supporting it within that source. Record the exact statement, cited support, whether the cited support was inspected, and its unresolved status if unavailable.

Keep three axes separate:

1. `pramana_class`: how the source supports the claim.
2. `support_strength`: strong, moderate, weak, or unassessed, with a written justification.
3. `causal_relevance`: observation_only, association, mechanism_inference, or intervention_evidence.

Never assign automatic numeric weights to the four classes. A poorly controlled direct observation need not be stronger than a well-tested inference.

## Citation and dependency discipline

- An inference based on an experiment is not independent confirmation of that experiment. Link it by `premise_evidence_ids` and use a common `evidence_origin_id` where appropriate.
- If Paper A repeats a mechanism and cites Paper B, retain A as `shabda` in A. Inspect B when it is in scope, classify B independently, and link the records. Do not rewrite A's original evidential basis.
- “Support not found in inspected material” differs from “support does not exist.”

## Vyapti anchors and upadhi review

A `vyapti_anchor` is a precisely formulated, established principle admitted to an explicit anchor registry within a stated domain. It is not a high-citation empirical generalization.

Use statuses: `ordinary_claim`, `candidate_invariant`, `vyapti_anchor`, and `contested_anchor`.

Elevate only after recording a precise proposition or equation; defined terms, scope, quantifiers, and applicability conditions; authoritative foundations; apparent counterexamples and an `upadhi_assessment`; and a named review rationale and status.

An explicit domain condition is not a hidden upadhi. The defect is silently omitting a condition necessary for the conclusion. Compatibility with an anchor does **not** prove a proposed mechanism.

## Concomitance and graph visual grammar

Do not conflate logical concomitance with physical response sign or causal direction.

- `concomitance_type`: `anvaya` (positive presence case), `vyatireka` (negative/absence case), `anvaya_vyatireka`, or `unassessed`.
- `effect_sign`: `positive`, `negative`, `nonmonotonic`, `context_dependent`, `unknown`, or `not_applicable`.
- Arrow direction: the stated causal or inferential relation only.
- Suggested colour: blue for `anvaya`, orange for `vyatireka`, purple for `anvaya_vyatireka`; also include a text label for grayscale/accessibility.
- Line thickness: ordinal evidential support only, never effect magnitude.
- Dashed line: proposed or unresolved.
- Double outline plus `V` badge: vyapti anchor.
- Condition marker: applicability condition or unresolved upadhi.

`H ⇒ S` does not imply the reverse causal arrow. A negative effect sign (increasing X decreases Y) is not automatically `vyatireka`.

## Required reporting

For each question-relevant claim, report the evidence profile: claim, pramana class, stance, support-strength rationale, causal relevance, dependencies, limitations, and source locator. Include an explicit list of claims relying primarily on analogy or assertion and a concrete observation/intervention that could strengthen them.

## Reference

Use `references/pramana-vyapti-rubric.md` for decision boundaries and examples.
