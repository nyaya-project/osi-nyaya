---
name: vaada-artifact-integrity
description: Safely reconcile, validate, and append shared Vaada JSON debate artifacts across multi-role chat workflows.
version: 1.0.0
---

# Vaada Artifact Integrity

Use when a Vaada cycle has a shared append-only JSON artifact, particularly when the chat transcript, quoted records, launch parameters, or artifact paths may conflict.

## Authority and artifact identity

1. The user/coordinator-declared `shared_artifact` is authoritative for that invocation. Read it before doing any role-specific work.
2. Treat a quoted Telegram message, reply, or record ID from another path as diagnostic evidence only—not authorization to switch paths.
3. If the declared artifact is absent but another artifact with the same `debate_id` is active, report both facts and request an explicit coordinator choice. Do not append to the alternate artifact solely because it contains a familiar lineage.
4. If two artifacts with the same `debate_id` have divergent lineages, do not merge them or copy turns between them. Require an explicit restart or authoritative-path selection.
5. Deletion/restart requires explicit user authorization. After deletion, only the Proponent/coordinator creates the new artifact; later roles wait for their required predecessors.

## Pre-append validation

- Read the repository `vaada-record.schema.json` and validate the new record against it; do not infer correctness from prior records.
- Confirm `debate_id`, question, round, stage order, `current_turn`, and `responds_to` lineage against the declared artifact.
- Keep `knowledge_graph`, `direct_observation`, and `proposed_link` distinct. A proposed causal relation must identify its premise evidence IDs.
- Preserve all earlier turns as immutable records. Append exactly one new turn and alter only top-level state mandated by the protocol.
- Use an atomic write/replace, then re-read the saved file and validate JSON, schema, new sequence number, record ID, `current_turn`, status, and termination state.

## Judge gate

A Judge appends only after the same artifact contains, for the same round and candidate lineage: Hypothesis Card, Vyapti audit, Opponent dossier, and Proponent defense. Do not decide from a partial Telegram quote.

## Public handoff

State the declared artifact path, debate ID, record ID, round, response lineage, provenance labels, validation result, and next state. If no append is permissible, state the observed artifact state and the blocking predecessor.
