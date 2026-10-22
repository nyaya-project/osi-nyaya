# Materials hypothesis-to-simulation extension

Use this extension when a causal knowledge graph is intended to lead to laboratory tests and, only later, atomistic/MLIP simulations. It extends the Causal Knowledge Mapper and Vāda artifacts; it does not replace their evidence or debate contracts.

## Data and licensing boundary

- ICSD CIFs, coordinates, cell parameters, and reversible structure-bearing extracts must never be committed to this repository.
- An ICSD-derived claim may cite an allowed collection identifier, a non-reversible scalar feature, source fingerprint, and extraction method. Keep raw files outside Git in an access-controlled location.
- Literature PDFs and other licensed source files are likewise external. Commit only permitted citation metadata, locators, claim extracts, and hashes where allowed.
- Do not present a database annotation as an experimentally validated causal relation without a claim-level source and scope.

## Required progression

1. Create and validate the canonical `graph.json` plus `run.json` using the causal-mapper contract.
2. Start one append-only `vaada-cycle/v1` artifact. Use the existing Proponent → Opponent → Judge sequence and preserve revisions as additional records.
3. Select a slate conforming to `schemas/materials-experiment-plan.schema.json`. It must contain at least five ranked, falsifiable tests. Every test needs an intervention/control, prediction, and falsifier.
4. Stop for human approval of the test slate. Do not create or relax simulation structures at this point.
5. If simulations are approved, create and commit a `materials-simulation-decision-lock/v1` document before model loading, relaxation, threshold tuning, or outcome inspection. It must name input provenance, hashes, model/checkpoint, relaxation protocol, observables, predictions, and outcome rules.
6. Run only the locked simulations. Report failures, unavailable results, and deviations separately from scientific outcomes.

## Integration boundary

This repository records causal evidence, debate artifacts, test plans, and simulation locks. Atomistic execution belongs in an approved external project or runtime. Link to its non-secret run manifest and result hashes; do not import a licensed ICSD structure merely to make a local simulation artifact self-contained.
