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

- A debate is **strictly sequential**. Do not generate a later role's substantive turn before every required earlier turn is present and valid.
- Keep one append-only `vaada-cycle/v1` JSON document per `debate_id`. Do **not** create independent, competing debate JSON files.
- Every appended turn contains one `vaada-record/v1` role record. That embedded record must conform to `schemas/vaada-record.schema.json`.
- Never overwrite, rewrite, or silently drop an earlier turn. A revision or defense is a new appended turn with `responds_to` pointing to the earlier record IDs.
- Preserve provenance. Label synthetic data as synthetic; distinguish `knowledge_graph`, `direct_observation`, and `proposed_link`; do not present a proposal or inference as observation.
- A debate terminates only when the Judge selects an end disposition (`end_hypothesis_accepted` or `end_hypothesis_rejected`) or requests new evidence/experiment. A `revision_requested` disposition begins the next sequential round, subject to `max_rounds`.

## Human launch and Telegram constraint

The human scientist may invoke all three roles in one **human-authored** message. That launch must include the three bot mentions, research question, and a unique `debate_id`.

Telegram bots cannot receive messages sent by other bots. Therefore, a Telegram message is a public transcript surface, not the role-to-role transport. A coordinator or shared durable debate artifact must pass the appended JSON to the next role. A role must never claim it has read another bot's Telegram output unless that output is present in the shared debate artifact supplied to it.

When a role is invoked before its turn:

1. Read the current shared artifact.
2. If `current_turn` is not that role, make no substantive Vaada contribution.
3. Wait through the coordinator/state mechanism; do not manufacture a missing earlier turn, answer a different debate, or produce an out-of-order verdict.

For group launches, Telegram privacy mode must allow every named bot to receive the human launch message. This platform setting does not remove the bot-to-bot visibility restriction.

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

Set `current_turn` to `vyapti_check` after the Proponent turn.

### 2. Causal grounding: Vyapti check

Audit each proposed `hetu → sadhya` link against the available causal map and evidence. Mark a link as grounded, uncertain, or weak causal support. A weak link is not discarded: it is carried to the Opponent with its flag and provenance intact.

Set `current_turn` to `opponent` after this audit.

### 3. Opponent: adversarial critique

The Opponent appends a Challenge Dossier for each candidate. It must fairly restate the claim; identify the strongest Tarka/counterargument; test for hetvabhasa; identify alternative causal graphs, confounders, and measurement weaknesses; run novelty/deduplication checks; and name decisive tests plus a repair path.

Set `current_turn` to `proponent_defense` after the Opponent turn.

### 4. Proponent: one defense

The original Proponent appends exactly one defense to the validated critique, choosing `reinforce`, `narrow`, `revise`, or `concede`. The defense must respond to the Challenge Dossier's `record_id` and retain the affected claim lineage. Do not parallelize defenses or generate unbounded rebuttal loops.

Set `current_turn` to `judge` after the defense.

### 5. Judge: evidence validation and decision

The Judge appends a Decision Record after reviewing the shared artifact, including direct evidence available from the Knowledge Pool and both sides' claims. Grade evidence using Pramana categories without treating a category as an automatic strength score. Separate accepted, rejected, and unresolved components; preserve material dissent; name a key defeater, next test, and update condition.

Map the operational outcome as follows:

- **Accept** → `verdict: provisionally_supported`, `action_item: end_hypothesis_accepted`.
- **Reject** → `verdict: provisionally_rejected`, `action_item: end_hypothesis_rejected`.
- **Revise** → `action_item: revision_requested`.
- **Escalate to human / new evidence required** → `action_item: experimental_data_requested` or `status: escalated_to_human` when the round limit is reached.

### 6. Termination or next round

- On acceptance or rejection, set `status: terminated`, set `current_turn: null`, and write `termination` with the Judge record ID and rationale.
- On experimental-data request, terminate the current debate outcome as evidence-pending and name the required experiment or observation. Do not pretend a final acceptance/rejection was reached.
- On revision, increment `round_count`, set `current_turn: proponent`, and begin the next sequential round. If `round_count` would exceed `max_rounds`, set `status: escalated_to_human` rather than silently continuing.

## Public transcript rule

The coordinator posts every appended turn visibly in the shared Telegram topic with its `debate_id`, `record_id`, `round`, stage, and complete JSON. The public messages are an audit trail; the shared artifact is the authoritative state used to trigger the next role.

## Role-specific guardrails

- **Proponent:** never self-certifies acceptance and never converts a weak Vyapti link into established evidence.
- **Opponent:** attacks the strongest charitable version, does not infer falsity from missing evidence, and names what would repair the claim.
- **Judge:** never issues a substantive decision without the preceding Proponent, Vyapti, Opponent, and Proponent-defense stages for the same candidate and round. Prefer insufficient identification, revision, experiment, or escalation to unsupported causation.

## Verification before appending

Before adding a turn, verify:

1. `debate_id`, `round`, and claim lineage match the shared artifact.
2. The role matches `current_turn`.
3. The embedded record validates against `vaada-record/v1`.
4. Source units have correct provenance and uncertainty labels.
5. The append leaves all prior `turns` byte-for-byte unchanged.
6. The next `current_turn`, `status`, and termination fields follow this skill.
