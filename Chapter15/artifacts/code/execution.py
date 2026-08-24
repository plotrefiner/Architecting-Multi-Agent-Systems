from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Mapping, Any

@dataclass(frozen=True)
class ExecutionDecision:
    execution: str
    reason: str

def choose_execution_mode(task_class: str, required_fields_present: bool, policy: Mapping[str, Any]) -> ExecutionDecision:
    if not required_fields_present:
        entry = policy["missing_order_identifier"]
        return ExecutionDecision(entry["execution"], entry["reason"])
    if task_class in policy:
        entry = policy[task_class]
        return ExecutionDecision(entry["execution"], entry["reason"])
    return ExecutionDecision("sequential", "default to simplest safe path")

def join_ready(accepted_artifacts: Iterable[str], join_policy: Mapping[str, Any], facts: Mapping[str, Any] | None = None) -> bool:
    accepted = set(accepted_artifacts)
    if any(a not in accepted for a in join_policy.get("required", [])):
        return False
    facts = facts or {}
    for artifact, condition in join_policy.get("conditionally_required", {}).items():
        if facts.get(condition, False) and artifact not in accepted:
            return False
    return True

def concurrency_allowed(active_tasks: int, limits: Mapping[str, Any]) -> bool:
    return active_tasks < int(limits["maximum_parallel_tasks_per_workflow"])
