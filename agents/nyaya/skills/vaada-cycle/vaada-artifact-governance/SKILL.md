---
name: vaada-artifact-governance
description: Govern append-only, multi-role Nyaya Vaada debate artifacts with validated sequencing, provenance, and restart hygiene.
version: 1.0.0
---

# Vaada Artifact Governance

Use this skill when coordinating, participating in, or auditing a multi-role Vaada cycle whose authoritative state is a shared append-only JSON artifact.

## Core invariants

- The shared artifact, not chat messages, is authoritative for role sequencing.
- Read the artifact before acting. Append only if its `current_turn` equals the role you are executing.
- Preserve every earlier turn unchanged. A correction, rebuttal, defense, or revision is a new record with lineage in `responds_to`.
- A Judge must not decide before lineage-matched Proponent hypothesis, Vyapti, Opponent dossier, and Proponent defense are present.

## Start and restart hygiene

1. Treat the stated `shared_artifact` path as a run-specific authority.
2. If the file does not exist, only the initializing Proponent/coordinator may create it. Other roles wait rather than fabricate earlier stages.
3. If a later launch repeats a question but points to an existing artifact, do not reset or overwrite it. Continue only according to its recorded `current_turn`.
4. Deleting or restarting an existing artifact requires explicit user authorization. Even then, later roles wait until the Proponent has initialized the new artifact and completed the required preceding stages.
5. Reusing a `debate_id` at a different path creates a lineage hazard. Preserve the requested ID, state the artifact path publicly, and require a fresh initialization at that path. Do not merge artifacts.
6. If the live launch's question/evidence disagrees with the recorded artifact, never retrofit prior turns. Preserve them; identify a lineage mismatch and request a defense, revision, or coordinator reconciliation.

## Pre-append procedure

1. Locate and read the repository's actual `vaada-record.schema.json`; do not infer schema fields from an existing artifact, which may itself be malformed.
2. Confirm: `debate_id`, round, role, current turn, prior sequence, and target stage.
3. Build a new immutable record ID and populate required schema fields.
4. Keep evidence categories distinct:
   - `knowledge_graph`: cited graph claim/evidence only; use the graph ID as `source_id` and its JSON path as `locator`.
   - `direct_observation`: artifact state, supplied launch text, or actual measurements—not an inference.
   - `proposed_link`: causal proposal; identify its premise evidence IDs.
5. For an Opponent record: fairly restate; rank nonempty objections; name alternatives, decisive tests, residual uncertainty, and a repair path. Missing evidence weakens identification; it does not itself prove falsity.
6. Validate the new embedded record against the schema before writing. Then append it as exactly one new turn, update only allowed top-level state (`current_turn`, status/termination where applicable), and re-read/revalidate after write.

## CdTe / graph-only debate guardrail

When the evidence corpus documents a theory–experiment disagreement, distinguish:

- observed disagreement;
- a graph-supported candidate mechanism; and
- the proposed link that incomplete structural search explains it.

A conflict alone does not establish omitted configurations as its cause. Require a documented original search boundary and a controlled expanded search that improves a pre-specified structural, EPR, or electronic discriminator. Do not bridge from defect structure to recombination/lifetime without defect-resolved kinetics and relevant sample abundance/speciation evidence.

## Public audit message

After a valid append, publish debate ID, record ID, round, responds-to IDs, explicit provenance labels, and the complete appended record. State validation status and the next `current_turn`. If it is not your turn, say no record was appended and give the observed artifact state.
