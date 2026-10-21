# Nyaya causal-reasoning harness

This directory versions the non-secret role artifacts for four Telegram bot profiles. It is a portable record of each bot's reasoning contract, not a dump of its Hermes runtime state.

## Bot and profile mapping

- `@CausalKnowledgeBot` → `causal-knowledge-mapper` → **Pramana**: evidence provenance and causal-model audit.
- `@NyayaProponentBot` → `nyaya-proponent` → **Paksha**: causal hypothesis formulation.
- `@NyayaOpponentBot` → `nyaya-opponent` → **Pratipaksha**: adversarial challenge and alternative explanations.
- `@NyayaJudgeBot` → `nyaya-judge` → **Nirnaya**: calibrated provisional decision.

## Files

Each profile directory contains:

- `SOUL.md`: the Hermes profile instruction actually used to define the role.
- `nyaya_reasoning.yaml`: a machine-readable reasoning contract, including inputs, outputs, quality gates, and agent handoffs.

## Deliberately excluded

Runtime profile configuration is intentionally not committed. In particular, `.env`, API credentials, Telegram bot tokens, user allowlists, session histories, memories, and logs remain under `~/.hermes/profiles/<profile>/` on the host.

## Reasoning flow

```text
Causal Knowledge Mapper (evidence ledger)
  → Nyaya Proponent (hypothesis card)
  → Nyaya Opponent (challenge dossier)
  → Nyaya Judge (decision record and next test)
```
