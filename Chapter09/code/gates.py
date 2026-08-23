"""Artifact gate evaluation."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class GateResult:
    outcome: str
    artifact_ref: Optional[str] = None


@dataclass
class Artifact:
    artifact_id: str
    artifact_contract: str
    producer: str
    payload_ref: str
    evidence_refs: List[str]


@dataclass
class Task:
    task_id: str
    output_contract: str
    assigned_owner: str
    input_state_version: int
    deadline: datetime
    evidence_scope: str


class Registry:
    def validates(self, artifact_contract: str, payload_ref: str) -> bool:
        return bool(artifact_contract and payload_ref)

    def evidence_within_scope(self, evidence_refs: List[str], evidence_scope: str) -> bool:
        prefix = evidence_scope.split(":")[0]
        return all(ref.startswith(prefix) for ref in evidence_refs)


class Graph:
    def __init__(self, current_tasks: set[tuple[str, int]]) -> None:
        self.current_tasks = current_tasks

    def is_task_current(self, task_id: str, input_state_version: int) -> bool:
        return (task_id, input_state_version) in self.current_tasks


class Clock:
    def __init__(self, now_value: datetime | None = None) -> None:
        self.now_value = now_value or datetime.now(timezone.utc)

    def now(self) -> datetime:
        return self.now_value


def evaluate_gate(artifact: Artifact, task: Task, graph: Graph, registry: Registry, clock: Clock) -> GateResult:
    if artifact.artifact_contract != task.output_contract:
        return GateResult("contract_rejected")

    if not registry.validates(
        artifact.artifact_contract,
        artifact.payload_ref,
    ):
        return GateResult("contract_rejected")

    if artifact.producer != task.assigned_owner:
        return GateResult("owner_rejected")

    if not graph.is_task_current(
        task.task_id,
        task.input_state_version,
    ):
        return GateResult("task_invalidated")

    if clock.now() > task.deadline:
        return GateResult("deadline_expired")

    if not registry.evidence_within_scope(
        artifact.evidence_refs,
        task.evidence_scope,
    ):
        return GateResult("scope_rejected")

    return GateResult("accepted", artifact_ref=artifact.artifact_id)
