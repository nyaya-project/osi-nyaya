# Nyaya causal-reasoning harness

This directory versions the non-secret role artifacts for four Telegram bot profiles. It is a portable record of each bot's reasoning contract, not a dump of its Hermes runtime state.

## Bot and profile mapping

- `@CausalKnowledgeBot` → `causal-knowledge-mapper` → **Pramana**: evidence provenance and causal-model audit.
- `@NyayaProponentBot` → `nyaya-proponent` → **Paksha**: causal hypothesis formulation.
- `@NyayaOpponentBot` → `nyaya-opponent` → **Pratipaksha**: adversarial challenge and alternative explanations.
- `@NyayaJudgeBot` → `nyaya-judge` → **Nirnaya**: calibrated provisional decision.

## Files

Each profile directory contains:

- `SOUL.md`: the Hermes profile instruction that defines the role.
- `AGENT.md`: the operational workflow and the shared record contract.
- `nyaya_reasoning.yaml`: a machine-readable reasoning contract, including inputs, outputs, quality gates, and agent handoffs.
- `skills/` when needed: profile-scoped, portable skills used only by that role. The `causal-knowledge-mapper` profile includes the causal graph workflow and the Nyāya evidence-hierarchy rubric.

The Proponent, Opponent, and Judge share [`skills/vaada-cycle/SKILL.md`](skills/vaada-cycle/SKILL.md). It defines the sequential **Human/Proponent → Opponent → Judge** `vaada-cycle/v1` artifact, provenance rules, and bounded revision rounds. [`scripts/vaada_dispatcher.py`](../../scripts/vaada_dispatcher.py) polls opted-in artifacts and invokes the next role from `current_turn`; Telegram remains a public audit transcript, not bot-to-bot transport.

## Vaada interchange schema

[`schemas/vaada-record.schema.json`](../../schemas/vaada-record.schema.json) is the common JSON Schema for the Proponent's Hypothesis Card, the Opponent's Challenge Dossier, and the Judge's Decision Record. It requires immutable record/debate IDs, one-based debate round, explicitly typed source provenance (`knowledge_graph`, `direct_observation`, or `proposed_link`), a role-appropriate summary, and a role-specific payload. `responds_to` and `claim_ids` retain the debate chain for later graph use.

## Deliberately excluded

Runtime profile configuration is intentionally not committed. In particular, `.env`, API credentials, Telegram bot tokens, user allowlists, session histories, memories, and logs remain under `~/.hermes/profiles/<profile>/` on the host.

## Reasoning flow

```text
Human / Nyaya Proponent (hypothesis card)
  → Nyaya Opponent (challenge dossier)
  → Nyaya Judge (decision record)
      ├─ revision_requested → next Proponent round
      └─ any other action item → end
```

The Causal Knowledge Mapper remains an optional evidence source, not a blocking debate turn.
