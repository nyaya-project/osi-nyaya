---
name: vaada-cycle
description: Run a sequential, provenance-aware Nyaya Vaada debate as one append-only debate artifact shared by the Proponent, Opponent, and Judge.
version: 1.0.0
author: OSI Nyaya
license: MIT
metadata:
  hermes:
    tags: [nyaya, vaada, debate, causal-reasoning, multi-agent]
---

# Vaada Cycle

Use this skill whenever a human asks the Nyaya Proponent, Opponent, and Judge to deliberate on one research question or hypothesis.

## Non-negotiable protocol

- A debate is **strictly sequential**: **Human/Proponent → Opponent → Judge**. Do not generate a later role's substantive turn before every required earlier turn is present and valid.
- Keep one append-only `vaada-cycle/v1` JSON document per `debate_id`. Do **not** create independent, competing debate JSON files.
- Every appended turn contains one `vaada-record/v1` role record. That embedded record must conform to `schemas/vaada-record.schema.json`.
- Never overwrite, rewrite, or silently drop an earlier turn. A Judge-authorized revision is a new round; it does not create a Proponent defense/rebuttal turn within the previous round.
- Preserve provenance. Label synthetic data as synthetic; distinguish `knowledge_graph`, `direct_observation`, and `proposed_link`; do not present a proposal or inference as observation.
- The Judge ends the debate for every disposition except `revision_requested`. A `revision_requested` disposition begins the next sequential round, subject to `max_rounds`.

## Human launch and Telegram constraint

The human scientist launches a debate by mentioning the Proponent (or by supplying a first Hypothesis Card), a research question, and a unique `debate_id`. The launch artifact must set `autonomous_dispatch: true` and a `delivery_target` such as `telegram:-1004419031322:182`.

Telegram bots cannot receive messages sent by other bots. Therefore Telegram is only the public audit transcript. The installed `scripts/vaada_dispatcher.py` is the authoritative coordinator: it polls eligible shared artifacts, invokes exactly the profile named by `current_turn`, and that profile appends its record and posts it with its own Telegram identity. This eliminates human turn-by-turn nudges.

When a role is invoked by the dispatcher:

1. Read the current shared artifact.
2. If `current_turn` is not that role, make no substantive Vaada contribution.
3. Append exactly one valid record, advance state, and post the complete appended record to `delivery_target`.
4. Never invoke, mention, or wait for another bot; the dispatcher starts the next role from artifact state.

For group launches, Telegram privacy mode must allow the named Proponent to receive the human launch message. This platform setting does not remove the bot-to-bot visibility restriction.

## Shared debate artifact

Use this shape. `turns[*].record` is the existing role-specific `vaada-record/v1` JSON object.

```json
{
  "schema_version": "vaada-cycle/v1",
  "debate_id": "immutable-debate-id",
  "question": "The exact research question",
  "round_count": 1,
  "max_rounds": 3,
  "status": "active",
  "autonomous_dispatch": true,
  "delivery_target": "telegram:-1004419031322:182",
  "current_turn": "proponent",
  "turns": [
    {
      "sequence": 1,
      "stage": "hypothesis_generation",
      "record": { "...": "valid vaada-record/v1 Proponent record" }
    }
  ],
  "termination": null
}
```

Allowed `status` values are `active`, `terminated`, and `escalated_to_human`.

Each appended turn must have:

- a strictly increasing `sequence`;
- the current `round` in its embedded record;
- a role-appropriate `stage`;
- immutable prior turns unchanged;
- `responds_to` populated for every response/defense/verdict that depends on prior turns.

## Required sequence per hypothesis

### 0. Intake and deduplication

Establish the question, scope, unit of analysis, decision context, `debate_id`, and `max_rounds` (default `3`). Check the Knowledge Pool for causal maps, literature, and prior hypotheses. Record duplicates or near-duplicates rather than presenting them as novel.

### 1. Proponent: hypothesis generation

The Proponent appends one or more independently evaluable candidate hypotheses. For each candidate provide:

- `pratijna` / `paksha`: the claim;
- `hetu`: the proposed reason or mechanism;
- `drstanta`: a relevant supporting example or analogy when available;
- list-valued `vyapti_links` identifying the proposed reason-to-outcome links;
- assumptions, scope, uncertainty, evidence gaps, discriminating predictions, and falsifiers.

Set `current_turn` to `opponent` after the Proponent turn.

### 2. Opponent: adversarial critique

The Opponent appends a Challenge Dossier for each candidate after the Proponent turn. It must fairly restate the claim; identify the strongest Tarka/counterargument; test for hetvabhasa; identify alternative causal graphs, confounders, and measurement weaknesses; run novelty/deduplication checks; and name decisive tests plus a repair path.

Set `current_turn` to `judge` after the Opponent turn.

### 3. Judge: evidence validation and decision

The Judge appends a Decision Record after reviewing the Proponent and Opponent records in the shared artifact, together with available Knowledge Pool evidence. Grade evidence using Pramana categories without treating a category as an automatic strength score. Separate accepted, rejected, and unresolved components; preserve material dissent; name a key defeater, next test, and update condition.

Map the operational outcome as follows:

- **Accept** → `verdict: provisionally_supported`, `action_item: end_hypothesis_accepted`.
- **Reject** → `verdict: provisionally_rejected`, `action_item: end_hypothesis_rejected`.
- **Revise** → `action_item: revision_requested`.
- **Escalate to human / new evidence required** → `action_item: experimental_data_requested` or `status: escalated_to_human` when the round limit is reached.

### 4. Termination or next round

- On acceptance, rejection, or experimental-data request, set `status: terminated`, set `current_turn: null`, and write `termination` with the Judge record ID and rationale.
- On revision, increment `round_count`, set `current_turn: proponent`, and begin the next **Human/Proponent → Opponent → Judge** round. If `round_count` would exceed `max_rounds`, set `status: escalated_to_human` rather than silently continuing.

## Public transcript rule

Each dispatched role posts its own appended turn visibly in the shared Telegram topic with its `debate_id`, `record_id`, `round`, stage, and complete JSON. The public messages are an audit trail; the shared artifact is the authoritative state used by the dispatcher to trigger the next role.

## Role-specific guardrails

- **Proponent:** never self-certifies acceptance and never converts a weak Vyapti link into established evidence.
- **Opponent:** attacks the strongest charitable version, does not infer falsity from missing evidence, and names what would repair the claim.
- **Judge:** never issues a substantive decision without the preceding Proponent and Opponent stages for the same candidate and round. Prefer insufficient identification, revision, experiment, or escalation to unsupported causation.

## Verification before appending

Before adding a turn, verify:

1. `debate_id`, `round`, and claim lineage match the shared artifact.
2. The role matches `current_turn`.
3. The embedded record validates against `vaada-record/v1`.
4. Source units have correct provenance and uncertainty labels.
5. The append leaves all prior `turns` byte-for-byte unchanged.
6. The next `current_turn`, `status`, and termination fields follow this skill.
