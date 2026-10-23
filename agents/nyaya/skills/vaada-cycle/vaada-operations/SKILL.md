---
name: vaada-operations
description: Operate, dispatch, and repair public append-only Nyaya Vaada cycles when several debate artifacts share an orchestration directory.
version: 1.0.0
---

# Vaada Operations

Use this skill for launching or driving a public `vaada-cycle/v1` debate after its substantive record format has been selected. It complements the general Vāda-cycle protocol with operational integrity checks for dispatch selection and public-delivery reliability.

## Core invariants

- The user-declared artifact path is the authority for that invocation. Never merge it with an artifact at another path, even when `debate_id` is the same.
- The artifact controls role eligibility. Before every role dispatch, re-read it and require `status: active` plus the expected `current_turn`.
- A role record is complete only when both conditions hold: (1) its exact JSON is appended and schema-valid in the authority artifact and (2) the same exact JSON has been publicly delivered to the artifact's `delivery_target`.
- No MLIP or other downstream work belongs in a Vāda-only cycle unless the artifact’s terminal decision explicitly authorizes it.

## Dispatch procedure

1. Read the declared artifact and identify the exact next role.
2. Run the standard dispatcher. Its usual one-transition-per-tick behavior is desirable for append-only integrity.
3. Re-read the **declared path** after the dispatcher returns. Do not infer success from a dispatcher exit code or output about another artifact.
4. If another older active artifact in the same runs directory was selected, retain the declared artifact unchanged. For required path-specific orchestration, invoke the dispatcher’s ordinary role prompt/state-check logic for the exact declared path. Do not copy the artifact to a temporary run, and do not manually write an Opponent or Judge record.
5. Confirm the newly appended record’s ID, round, stage, response lineage, schema validity, next state, and public audit post.

## Public-delivery repair

Telegram delivery failure after a successful append is a provenance problem, not a reason to append a replacement record.

1. Re-read the saved artifact and extract its last appended record only after matching the expected record ID, role, and round.
2. Serialize that extracted record verbatim to a UTF-8 `.json` attachment.
3. Compute and state attachment byte length and SHA-256.
4. Send a clearly titled **delivery repair** to the original delivery target containing debate ID, record ID, round, stage, response lineage, explicit provenance labels, artifact path, checksum, and the JSON attachment.
5. Do not reconstruct or summarize the JSON from memory. Do not issue an extra Vāda turn.

## Multi-artifact hazards

- A repeated `debate_id` at a new path is a lineage hazard. Name both path and record ID in every public audit header.
- Generic dispatcher scans can prioritize older files. Check the chosen file explicitly, especially after a long-running dispatch.
- A dispatcher subprocess can append correctly yet fail during its final post/eligibility re-check. Treat the artifact as authoritative, then repair the public audit delivery from the exact saved object.

## Completion checklist

Before reporting a role or cycle as complete, verify:

- The current artifact path is the requested one.
- Earlier turns are retained unchanged.
- Each required record is schema-valid and ordered sequentially.
- Each public post has either inline exact JSON or a checksum-addressed verbatim JSON attachment.
- `current_turn`, `status`, `round_count`, and termination agree with the last Judge action.
- Any nonterminal `revision_requested` is explicitly reported as active—not as a completed debate.
