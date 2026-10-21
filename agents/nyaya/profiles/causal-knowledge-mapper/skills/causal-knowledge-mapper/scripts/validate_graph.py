#!/usr/bin/env python3
"""Deterministic integrity checks for causal-knowledge-mapper graph JSON."""
import argparse
import json
import sys
from pathlib import Path


def ids(items):
    return [x.get("id") for x in items if isinstance(x, dict)]


def add(findings, level, code, message, item_id=None):
    row = {"level": level, "code": code, "message": message}
    if item_id:
        row["item_id"] = item_id
    findings.append(row)


def validate(graph):
    findings = []
    for key in ("sources", "entities", "claims", "evidence"):
        if not isinstance(graph.get(key), list):
            add(findings, "error", "missing_collection", f"'{key}' must be an array")
    if findings:
        return findings

    collections = {k: ids(graph.get(k, [])) for k in ("sources", "entities", "claims", "evidence", "anchors")}
    for kind, values in collections.items():
        seen = set()
        for value in values:
            if not value:
                add(findings, "error", "missing_id", f"{kind} entry has no id")
            elif value in seen:
                add(findings, "error", "duplicate_id", f"Duplicate id '{value}'", value)
            seen.add(value)

    entity_ids, source_ids, claim_ids, evidence_ids = (set(collections[x]) for x in ("entities", "sources", "claims", "evidence"))
    for claim in graph["claims"]:
        cid = claim.get("id")
        for field in ("subject_id", "object_id"):
            if claim.get(field) not in entity_ids:
                add(findings, "error", "bad_entity_reference", f"{field} does not name an entity", cid)
        if claim.get("relation") == "associated_with":
            add(findings, "warning", "association_not_causation", "Association must not be reported as causal without separate evidence", cid)
        if not claim.get("conditions"):
            add(findings, "warning", "missing_conditions", "No stated conditions; confirm that scope is truly general", cid)

    for ev in graph["evidence"]:
        eid, cls = ev.get("id"), ev.get("pramana_class")
        if ev.get("claim_id") not in claim_ids:
            add(findings, "error", "bad_claim_reference", "claim_id does not name a claim", eid)
        if ev.get("source_id") not in source_ids:
            add(findings, "error", "bad_source_reference", "source_id does not name a source", eid)
        if not ev.get("source_locator"):
            add(findings, "error", "missing_locator", "Evidence requires a source locator", eid)
        if not ev.get("classification_reason"):
            add(findings, "warning", "missing_classification_reason", "Evidence class has no reason", eid)
        if cls == "anumana" and not ev.get("premise_evidence_ids"):
            add(findings, "warning", "inference_without_premises", "Anumana should name inspected premises", eid)
        if cls == "upamana" and not ev.get("analogy_mapping"):
            add(findings, "warning", "analogy_without_mapping", "Upamana should state similarities and differences", eid)
        for premise in ev.get("premise_evidence_ids", []):
            if premise not in evidence_ids:
                add(findings, "error", "bad_premise_reference", f"Unknown premise evidence '{premise}'", eid)

    for anchor in graph.get("anchors", []):
        aid = anchor.get("id")
        if anchor.get("status") == "vyapti_anchor":
            for required in ("proposition", "scope", "upadhi_assessment", "review_rationale"):
                if not anchor.get(required):
                    add(findings, "error", "incomplete_vyapti_anchor", f"Vyapti anchor lacks '{required}'", aid)
            for src in anchor.get("foundation_source_ids", []):
                if src not in source_ids:
                    add(findings, "error", "bad_anchor_source_reference", f"Unknown foundation source '{src}'", aid)
    return findings


def main():
    p = argparse.ArgumentParser()
    p.add_argument("graph")
    p.add_argument("--output")
    args = p.parse_args()
    try:
        graph = json.loads(Path(args.graph).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "findings": [{"level": "error", "code": "unreadable_json", "message": str(exc)}]}, indent=2))
        return 2
    findings = validate(graph)
    result = {"valid": not any(x["level"] == "error" for x in findings), "findings": findings}
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text, end="")
    return 0 if result["valid"] else 1

if __name__ == "__main__":
    sys.exit(main())
