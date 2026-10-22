import json
from pathlib import Path

ROOT = Path(__file__).parents[1]

def load(name):
    return json.loads((ROOT / "schemas" / name).read_text())

def test_experiment_plan_requires_five_falsifiable_tests():
    schema = load("materials-experiment-plan.schema.json")
    assert schema["properties"]["recommended_tests"]["minItems"] == 5
    required = schema["$defs"]["test"]["required"]
    assert {"prediction", "falsifier", "intervention_or_control", "hypothesis_record_ref"} <= set(required)

def test_simulation_lock_excludes_licensed_structure_payloads():
    schema = load("materials-simulation-decision-lock.schema.json")
    inputs = schema["properties"]["structure_inputs"]["items"]
    assert inputs["additionalProperties"] is False
    assert set(inputs["required"]) == {"input_id", "provenance", "representation", "sha256"}
    assert "cif" not in inputs["properties"]
