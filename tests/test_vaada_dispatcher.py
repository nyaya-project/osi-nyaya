import importlib.util
import json
from pathlib import Path
import sys


SPEC = importlib.util.spec_from_file_location(
    "vaada_dispatcher", Path(__file__).parents[1] / "scripts" / "vaada_dispatcher.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def artifact(*, current_turn, roles=(), autonomous=True):
    return {
        "schema_version": "vaada-cycle/v1",
        "debate_id": "dummy-debate",
        "round_count": 1,
        "max_rounds": 3,
        "status": "active",
        "autonomous_dispatch": autonomous,
        "delivery_target": "telegram:-100:182",
        "current_turn": current_turn,
        "turns": [
            {"sequence": index, "record": {"round": 1, "agent": {"role": role}}}
            for index, role in enumerate(roles, start=1)
        ],
    }


def write_artifact(tmp_path, name, document):
    path = tmp_path / name
    path.write_text(json.dumps(document))
    return path


def test_proponent_is_eligible_at_human_launch(tmp_path):
    write_artifact(tmp_path, "launch.json", artifact(current_turn="proponent"))
    found = MODULE.find_dispatches(tmp_path)
    assert [(item.role, item.profile) for item in found] == [("proponent", "nyaya-proponent")]


def test_opponent_requires_proponent_record(tmp_path):
    write_artifact(tmp_path, "blocked.json", artifact(current_turn="opponent"))
    write_artifact(tmp_path, "ready.json", artifact(current_turn="opponent", roles=("proponent",)))
    found = MODULE.find_dispatches(tmp_path)
    assert [item.path.name for item in found] == ["ready.json"]


def test_judge_requires_proponent_and_opponent_records(tmp_path):
    write_artifact(tmp_path, "blocked.json", artifact(current_turn="judge", roles=("proponent",)))
    write_artifact(tmp_path, "ready.json", artifact(current_turn="judge", roles=("proponent", "opponent")))
    found = MODULE.find_dispatches(tmp_path)
    assert [item.path.name for item in found] == ["ready.json"]


def test_non_opted_in_artifact_is_not_dispatched(tmp_path):
    write_artifact(tmp_path, "manual.json", artifact(current_turn="proponent", autonomous=False))
    assert MODULE.find_dispatches(tmp_path) == []


def test_role_prompt_has_three_stage_transitions(tmp_path):
    path = tmp_path / "launch.json"
    dispatch = MODULE.Dispatch(path, "dummy-debate", "opponent", "nyaya-opponent", "telegram:-100:182")
    prompt = MODULE.role_prompt(dispatch)
    assert "Proponent → Opponent → Judge" in prompt
    assert "no separate Vyapti stage" in prompt
    assert "no Proponent defense turn" in prompt
    assert "current_turn = judge" in prompt
