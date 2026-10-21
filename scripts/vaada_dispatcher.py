#!/usr/bin/env python3
"""Advance one eligible Nyaya Vaada artifact without bot-to-bot Telegram messages.

The dispatcher is deliberately state-driven: a human starts a debate by creating an
active ``vaada-cycle/v1`` JSON artifact with ``autonomous_dispatch: true`` and a
``delivery_target``.  On each tick this program invokes only the role named by
``current_turn``.  That role appends its own vaada-record, updates the state, and
posts the completed turn to the public Telegram topic using its own bot identity.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any

ROLE_PROFILES = {
    "proponent": "nyaya-proponent",
    "opponent": "nyaya-opponent",
    "judge": "nyaya-judge",
}


@dataclass(frozen=True)
class Dispatch:
    path: Path
    debate_id: str
    role: str
    profile: str
    delivery_target: str


def _records_for_round(document: dict[str, Any]) -> list[dict[str, Any]]:
    round_count = document.get("round_count")
    return [
        turn.get("record", {})
        for turn in document.get("turns", [])
        if isinstance(turn, dict)
        and isinstance(turn.get("record"), dict)
        and turn["record"].get("round") == round_count
    ]


def _role_present(document: dict[str, Any], role: str) -> bool:
    return any(record.get("agent", {}).get("role") == role for record in _records_for_round(document))


def _is_eligible(document: dict[str, Any]) -> bool:
    if document.get("schema_version") != "vaada-cycle/v1":
        return False
    if document.get("status") != "active" or not document.get("autonomous_dispatch"):
        return False
    role = document.get("current_turn")
    if role not in ROLE_PROFILES:
        return False
    if not isinstance(document.get("debate_id"), str) or not document["debate_id"]:
        return False
    if not isinstance(document.get("delivery_target"), str) or not document["delivery_target"]:
        return False
    if not isinstance(document.get("round_count"), int) or document["round_count"] < 1:
        return False

    # Do not invoke a role until every earlier role in the same round exists.
    if role == "opponent":
        return _role_present(document, "proponent")
    if role == "judge":
        return _role_present(document, "proponent") and _role_present(document, "opponent")
    return True  # A human launch or a Judge-authorized revision begins with the Proponent.


def find_dispatches(runs_dir: Path) -> list[Dispatch]:
    dispatches: list[Dispatch] = []
    for path in runs_dir.glob("*.json"):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(document, dict) or not _is_eligible(document):
            continue
        role = document["current_turn"]
        dispatches.append(
            Dispatch(
                path=path,
                debate_id=document["debate_id"],
                role=role,
                profile=ROLE_PROFILES[role],
                delivery_target=document["delivery_target"],
            )
        )
    return sorted(dispatches, key=lambda item: item.path.stat().st_mtime)


def role_prompt(dispatch: Dispatch) -> str:
    return f"""You are being invoked by the Nyaya Vaada dispatcher. Advance exactly one role turn now.

Authoritative state artifact: {dispatch.path}
Debate ID: {dispatch.debate_id}
Your required role: {dispatch.role}
Telegram delivery target: {dispatch.delivery_target}

Read the artifact first. Act only if it remains active and current_turn is exactly {dispatch.role}. Follow the shared vaada-cycle skill's three-stage protocol: Proponent → Opponent → Judge. There is no separate Vyapti stage and no Proponent defense turn.

Append exactly one valid vaada-record/v1 contribution for your role without changing prior turns. Atomically write the updated artifact. Then set the state as follows:
- proponent: current_turn = opponent
- opponent: current_turn = judge
- judge with action_item = revision_requested and round_count < max_rounds: increment round_count and set current_turn = proponent
- judge with any other action_item: set status = terminated and current_turn = null

After a successful append, use send_message to post the complete appended JSON record to exactly {dispatch.delivery_target}. Include debate_id, record_id, round, stage, and the JSON. Do not mention or wait for another bot. If the artifact is not eligible, make no edits and do not send a message."""


def run_dispatch(dispatch: Dispatch, hermes_bin: str, timeout: int, dry_run: bool) -> int:
    command = [hermes_bin, "--profile", dispatch.profile, "chat", "-q", role_prompt(dispatch)]
    print(json.dumps({"event": "dispatch", "debate_id": dispatch.debate_id, "role": dispatch.role, "artifact": str(dispatch.path), "command": command[:-1]}))
    if dry_run:
        return 0
    before = dispatch.path.stat().st_mtime_ns
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout, check=False)
    after = dispatch.path.stat().st_mtime_ns
    print(result.stdout[-4000:])
    if result.returncode:
        print(f"dispatcher: {dispatch.profile} exited {result.returncode}", file=sys.stderr)
        return result.returncode
    if after == before:
        print("dispatcher: role completed without changing the artifact", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=Path.home() / ".hermes" / "vaada-runs")
    parser.add_argument("--hermes-bin", default="hermes")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    args.runs_dir.mkdir(parents=True, exist_ok=True)

    lock_path = args.runs_dir / ".vaada-dispatcher.lock"
    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("dispatcher: another tick is active")
            return 0
        dispatches = find_dispatches(args.runs_dir)
        if not dispatches:
            print("dispatcher: no eligible debate")
            return 0
        # One state transition per tick limits duplicate work and preserves an auditable sequence.
        return run_dispatch(dispatches[0], args.hermes_bin, args.timeout, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
