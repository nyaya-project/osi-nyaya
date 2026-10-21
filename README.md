# OSI Nyaya

Private project repository for code, artifacts, and documentation produced during the OSI hackathon.

## Nyaya causal-reasoning harness

The project uses four dedicated Telegram bot profiles as a structured causal-reasoning loop grounded in Nyaya Shastra:

- `@CausalKnowledgeBot` → `causal-knowledge-mapper` → **Pramana**: evidence provenance and causal-model audit.
- `@NyayaProponentBot` → `nyaya-proponent` → **Paksha**: causal hypothesis formulation.
- `@NyayaOpponentBot` → `nyaya-opponent` → **Pratipaksha**: adversarial challenge and alternative explanations.
- `@NyayaJudgeBot` → `nyaya-judge` → **Nirnaya**: calibrated provisional decision and next-test recommendation.

```text
Causal Knowledge Mapper (evidence ledger)
  → Nyaya Proponent (hypothesis card)
  → Nyaya Opponent (challenge dossier)
  → Nyaya Judge (decision record and next test)
```

The portable, non-secret role definitions are versioned in [`agents/nyaya/`](agents/nyaya/). Each profile has a `SOUL.md` role instruction and a `nyaya_reasoning.yaml` reasoning contract. Profile-scoped reusable skills live beside the role that uses them; the causal-mapper skills are under [`agents/nyaya/profiles/causal-knowledge-mapper/skills/`](agents/nyaya/profiles/causal-knowledge-mapper/skills/).

## Repository hygiene

This repository is intended to retain project code and shareable artifacts. Runtime-only or sensitive profile state is deliberately excluded, including `.env` files, API credentials, Telegram bot tokens, access allowlists, session histories, memories, and logs.
