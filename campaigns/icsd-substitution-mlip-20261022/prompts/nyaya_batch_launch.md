# Nyaya batch <N>

Create the specified active `vaada-cycle/v1` artifact in `~/.hermes/vaada-runs/` and debate exactly the ten rendered candidates. Use only pair catalogue, existing ICSD graph, campaign CKB graph, and frozen packs. No live search. Cite literature only by evidence_id.

Proponent: one record, all ten `claim_ids`, one prediction per candidate, and candidate ID at the beginning of each prediction statement. Prefix every source_id with candidate ID. Opponent: tag each objection with affected_claim_ids. Judge: place every candidate exactly once into accepted_components, unresolved_components, or rejected_components as `Cnn: retained/reconstructed`; write `pramana-ledger/v1` to `ledgers/<debate_id>.json`; do not recommend or run MLIP. Usual experimental slate is waived. Follow existing Vāda-cycle rules otherwise.
