---
name: vaada-evidence-interpretation
description: Interpret Vaada evidence artifacts, reconcile amended analyses, and explain calibrated results plainly to human decision-makers.
version: 1.0.0
---

# Vaada Evidence Interpretation

Use when a human asks whether debate artifacts agree, whether an experiment corroborates a hypothesis, what remains to validate it, or why a conclusion changed after a method correction.

## Core discipline

1. Read the relevant artifacts and distinguish direct file contents from inference.
2. Identify the precise endpoint each file addresses: e.g., a framework-comparator result, a network-topology result, a mechanism claim, or a synthesis claim.
3. Check whether later amendments explicitly supersede an earlier interpretation. Do not merge incompatible artifact lineages or silently select one result.
4. If different comparators, representations, or acceptance criteria yield different labels, call the disagreement **method-dependent**, not a materials reversal.
5. Preserve scope: a static MLIP relaxation result is workflow-qualified. It does not by itself establish mechanism, thermodynamic stability, finite-temperature behavior, or synthesis feasibility.

## Human-readable response format

When the human asks for an explanation rather than a machine-facing Decision Record:

- Start with the direct answer in plain English.
- Avoid Nyaya, graph, and simulation jargon unless the human uses it or asks for it.
- State three things separately:
  1. **What the files show.**
  2. **What that supports, and only under what conditions.**
  3. **Exactly what remains to be checked.**
- Use a short numbered checklist for the remaining work. Do not bury the answer under schema names or record IDs.

## Structural-comparison corrections

A corrected post-processing comparator may reuse saved relaxed structures and logs; it does not require rerunning relaxation solely because the comparison method changed. It must, however:

- name the superseded comparator/interpretation;
- specify the corrected comparator and complete settings;
- preserve input and relaxed structure hashes plus per-cell logs;
- state the new endpoint narrowly.

A framework match supports framework correspondence under the corrected workflow. It does not prove the causal reason for correspondence.

## Periodic connectivity validation

Do not treat equal edge counts as proof that two periodic connection networks are identical. Literal site indices and periodic-image vectors can change after CIF round-tripping or an equivalent cell/basis transformation.

For a valid independent connection-network test:

1. Retain the preregistered cutoff, species policy, and boundary rule.
2. Compare using species-labelled periodic graph isomorphism that is invariant to atom ordering and equivalent lattice-cell choices.
3. Preserve sufficient periodic information to distinguish genuinely different periodic networks; a plain edge-count test is inadequate.
4. Output, for every panel cell: pass/fail, site correspondence, lattice/basis handling, settings, structure hashes, and logs.
5. Mark any earlier index/image-vector comparison as invalid for adjudication rather than as evidence of changed connectivity.

## Corroboration checklist

For a hypothesis that predicts retained framework correspondence plus unchanged connectivity and a local mediator pattern, all of the following must be present before calling the full workflow-qualified prediction supported:

- the approved comparator matches every valid preregistered cell;
- complete mapping is documented for every cell;
- the invariant periodic connectivity comparison passes every cell;
- the mediator is defined before result interpretation and measured within its declared band for every cell;
- model, input, and analysis provenance are sufficient to reproduce the result;
- no valid cell is contradictory or diagnostically discordant.

If only the structural comparator passes, describe the result as **partial support for the structural-prediction component**. Do not state that the mechanism is validated.

## Pitfalls

- Do not say a hypothesis is fully validated; say what the evidence supports and its scope.
- Do not infer reconstruction or retention from catalogue associations alone.
- Do not let a later amended comparator erase the historical result; retain it as a result under its original method while stating whether it has been superseded for the intended endpoint.
- Do not call missing saved output a negative result. It is an unverified criterion.
