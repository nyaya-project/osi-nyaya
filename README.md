# Nyāya Causal Engine

A provenance-first, multi-agent engine for causal reasoning and research deliberation, grounded in **Nyāya**. It turns a bounded corpus and a research question into an auditable sequence of causal claims, adversarial checks, and calibrated next-step decisions.

> Extracting a causal claim from a source does **not** establish that the claim is true. The engine preserves this distinction in its records, provenance, uncertainty labels, and decision rules.

## What exists today

- An evidence-led **Causal Knowledge Mapper** that creates inspectable graphs of *reported* causal claims from documents and a scoped question.
- A four-role Nyāya reasoning loop: evidence audit, hypothesis formation, adversarial challenge, and provisional decision.
- A sequential **Vāda** protocol for an append-only debate artifact with bounded revision rounds.
- A versioned JSON interchange schema for the Proponent, Opponent, and Judge records.
- Portable, non-secret Hermes role definitions, reasoning contracts, skills, schemas, example data, report template, and graph validator.
- A registered materials campaign that evaluates Nyāya-guided causal knowledge graphs and Vāda debate against fixed control workflows before any downstream MLIP label is read.

The repository intentionally contains reusable research protocol, auditable campaign controls, and non-sensitive artifacts. It does not claim automated truth discovery or a complete causal-discovery system.

## Reasoning loop

```text
Causal Knowledge Mapper ── evidence ledger and causal-claim graph
          │
          ▼
Nyāya Proponent ─────────── hypothesis card (Pakṣa)
          │
          ▼
Nyāya Opponent ──────────── challenge dossier (Pratipakṣa)
          │
          ▼
Nyāya Judge ─────────────── provisional decision and next test (Nirṇaya)
```

The mapper distinguishes direct observation, inferred mechanism, association, and hypothesis. The Vāda cycle then requires each later role to preserve the provenance and uncertainty of the earlier record rather than silently upgrading a proposal into evidence.

## Operating principles

- **Evidence-linked, not assertion-led.** Every material claim carries source provenance, a locator, scope, conditions, and limitations where available.
- **Causal precision.** An association is never silently promoted to a causal relation; a direct observation does not by itself prove a mechanism.
- **Contradictions stay visible.** Conflicting records are reconciled by condition and provenance when possible, otherwise retained as unresolved.
- **Sequential and append-only deliberation.** The Proponent, causal grounding check, Opponent, Proponent defense, and Judge act in order. Revisions add records; they do not rewrite history.
- **Calibrated decisions.** The Judge may request a discriminating experiment or escalate to a human rather than force acceptance or rejection.
- **Bounded scope.** Absence of an edge means “not established in this scoped corpus,” never proof that no relationship exists.

## Repository map

- [`agents/nyaya/`](agents/nyaya/) — portable bot-role documentation and shared Vāda-cycle skill.
  - [`profiles/causal-knowledge-mapper/`](agents/nyaya/profiles/causal-knowledge-mapper/) — evidence-led causal graph workflow, Nyāya evidence rubric, graph/run schemas, validator, example graph, and report template.
  - [`profiles/nyaya-proponent/`](agents/nyaya/profiles/nyaya-proponent/) — Pakṣa hypothesis-formulation role.
  - [`profiles/nyaya-opponent/`](agents/nyaya/profiles/nyaya-opponent/) — Pratipakṣa adversarial-review role.
  - [`profiles/nyaya-judge/`](agents/nyaya/profiles/nyaya-judge/) — Nirṇaya decision and next-test role.
  - [`skills/vaada-cycle/SKILL.md`](agents/nyaya/skills/vaada-cycle/SKILL.md) — shared sequential debate protocol and Telegram coordination constraint.
- [`schemas/vaada-record.schema.json`](schemas/vaada-record.schema.json) — common `vaada-record/v1` contract for role records.
- [`schemas/materials-experiment-plan.schema.json`](schemas/materials-experiment-plan.schema.json) — a five-or-more, falsifiable materials test-slate contract.
- [`schemas/materials-simulation-decision-lock.schema.json`](schemas/materials-simulation-decision-lock.schema.json) — the required pre-simulation protocol lock, with no licensed CIF payload field.

## Core artifacts

### Causal knowledge graph

The Causal Knowledge Mapper produces a canonical `graph.json`, a scoped `report.md`, `validation.json`, and `run.json`. The graph, not the prose report, is the source of truth. Its workflow and validation tooling are defined in the [mapper skill](agents/nyaya/profiles/causal-knowledge-mapper/skills/causal-knowledge-mapper/SKILL.md).

### Vāda debate artifact

A debate is one append-only `vaada-cycle/v1` JSON document per `debate_id`. Embedded role records conform to [`vaada-record/v1`](schemas/vaada-record.schema.json). The shared artifact is the authoritative state; Telegram messages are the public audit transcript.

This distinction matters because Telegram bots cannot directly read one another’s messages. A human or coordinator must pass the updated shared artifact to the next role, and a role must not claim to have seen a prior bot’s Telegram output unless that record is present in the artifact it received.

## Active campaign: ICSD substitution MLIP evaluation

The registered [`icsd-substitution-mlip-20261022`](campaigns/icsd-substitution-mlip-20261022/) campaign is a prospective evaluation of the engine, not a catalogue-mining exercise. It compares three pre-label reasoning conditions on one frozen 99-candidate pool:

1. **Nyāya Causal Knowledge Builder:** evidence-linked causal graph plus provenance and uncertainty audit.
2. **Nyāya Vāda:** Proponent, Opponent, and Judge deliberate sequentially on the same evidence.
3. **Controls:** fixed non-Nyāya baselines evaluated against the same pool and prediction contract.

The protocol locks the candidate pool, literature-evidence workflow, prediction schema, and scoring rule before the TensorNet-MatPES-PBE MLIP outcome is available. The campaign asks whether the Nyāya-guided causal graph and debate improve calibrated, falsifiable predictions of framework retention after relaxation. It does **not** treat a static relaxation as proof of a mechanism, stability, or synthesizability.

Campaign-controlled files, validation scripts, and the current safe status summary are under [`campaigns/icsd-substitution-mlip-20261022/`](campaigns/icsd-substitution-mlip-20261022/). Raw/licensed ICSD CIF text, coordinates, cell parameters, and collection codes remain external to Git; only non-sensitive campaign identifiers and derived, auditable controls are versioned.

## Deliberately excluded

No runtime or credential material is versioned here. This includes `.env` files, API keys, Telegram bot tokens, allowlists, session histories, memories, and logs. Licensed ICSD CIF payloads, coordinates, cell parameters, and collection codes are also excluded. These remain in their authorized local stores or profile-local locations under `~/.hermes/profiles/<profile>/`.

## Status and direction

This is a small, inspectable foundation: readable role instructions, explicit data contracts, validation, examples, and evaluation-ready outputs. Near-term work should strengthen evaluation cases and coordinator/runtime integration without weakening provenance, contradiction handling, or the separation between extracted claims and established findings.
