#!/usr/bin/env python3
"""Render a sanitized campaign status payload; never emits ICSD CollectionCodes or structure data."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "status.json"


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default


def main() -> None:
    rejection = read_json(ROOT / "phase1_rejection_report.json", {})
    # pool.json is the approved canonical pool; pool.proposed.json is only a pre-freeze fallback.
    pool = read_json(ROOT / "pool.json", read_json(ROOT / "pool.proposed.json", {}))
    candidates = pool.get("candidates", [])
    accepted_candidates = candidates
    evidence_count = len([p for p in (ROOT / "evidence").glob("*.json") if p.stem in {c["candidate_id"] for c in candidates}])
    safe_candidates = []
    # This dashboard deliberately omits CollectionCode, CIF text, coordinates, and cell parameters.
    for c in accepted_candidates:
        safe_candidates.append({
            "candidate_id": c["candidate_id"],
            "source_formula": c["source_formula"],
            "site_label": c["site_label"],
            "substitution": f"{c['element_out']} → {c['element_in']}",
            "formula_B": c["formula_B"],
            "charge_preserving": c["charge_preserving"],
            "delta_r_over_r": c["delta_r_over_r"],
            "anion": c["anion"],
            "framework_family": c["framework_family"],
        })
    data = {
        "campaign_id": "icsd-substitution-mlip-20261022",
        "updated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "phase": "Phase 1: shared-pool validation and frozen literature packs",
        "status": "replacement_pool_in_progress" if not candidates else "literature_regeneration_in_progress",
        "safe_notice": "No ICSD CollectionCodes, CIF text, coordinates, or cell parameters are exposed here.",
        "counts": {
            "target_shared_pool": len(candidates),
            "accepted_pool": len(accepted_candidates),
            "pending_novelty_replacements": 0,
            "frozen_evidence_packs": evidence_count,
            "nyaya_predictions": 0,
            "control_predictions": 0,
            "mlip_labels": 0,
        },
        "last_validation": rejection,
        "candidates": safe_candidates,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
