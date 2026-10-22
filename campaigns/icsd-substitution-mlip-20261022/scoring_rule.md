# Campaign-only pramāṇa scoring rule

This pre-registered rule applies only to this campaign and does not amend the general evidence-hierarchy rubric. Count only items accepted by the Judge. Items sharing an `evidence_origin_id` count once using largest absolute weight.

- Class points: `pratyaksha/direct` 4; `anumana/inference` 3; `upamana/analogy` 2; `shabda/unexplained lit. claim` 1; `unassessed` 0.
- Strength: strong 1.0; moderate 0.6; weak 0.3; unassessed 0.
- Direction sign: retained +1; reconstructed -1.
- Weighted item score = class points × strength × sign. Strength-only item score = strength × sign.
- `p_retained = 0.5 + 0.5 * sum(w) / (sum(abs(w)) + 1)`; `uncertainty = 1 - abs(2*p_retained - 1)`; prediction is retained iff `p_retained >= 0.5`.

The official Nyaya prediction uses weighted scoring. Rank all shared candidates by tier ascending, confidence distance `abs(2p-1)` descending, then evidence magnitude descending. Tier 1/2/3 comes respectively from accepted/unresolved/rejected Judge components; otherwise tier 2. Judge confidence maps high/moderate/low to 0.85/0.65/0.55. Missing ledgers use the documented Judge-source fallback and must be logged.
