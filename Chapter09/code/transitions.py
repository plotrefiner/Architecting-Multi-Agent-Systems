"""Transition authorization and bounded loop budgets."""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional


class TransitionError(Exception):
    pass


@dataclass
class TransitionResult:
    outcome: str
    expected_version: Optional[int] = None
    consume_loop_iteration: bool = False


@dataclass
class Guard:
    allowed: bool = True

    def evaluate(self, instance: "GraphInstance", evidence: "Evidence") -> bool:
        return self.allowed


@dataclass
class Evidence:
    contracts_satisfied: set[str]

    def satisfies(self, contract: str) -> bool:
        return contract in self.contracts_satisfied


@dataclass
class Edge:
    source: str
    guard: Guard
    loop_id: Optional[str] = None
    maximum_iterations: int = 0
    progress_contract: Optional[str] = None


@dataclass
class GraphInstance:
    current_node: str
    workflow_deadline: datetime
    version: int
    loop_iterations: Dict[str, int] = field(default_factory=dict)


class Clock:
    def __init__(self, now_value: datetime | None = None) -> None:
        self.now_value = now_value or datetime.now(timezone.utc)

    def now(self) -> datetime:
        return self.now_value


def authorize_transition(instance: GraphInstance, edge: Edge, evidence: Evidence, clock: Clock) -> TransitionResult:
    if edge.source != instance.current_node:
        raise TransitionError("edge source is not current")

    if clock.now() > instance.workflow_deadline:
        return TransitionResult("deadline_exhausted")

    if edge.loop_id:
        used = instance.loop_iterations.get(edge.loop_id, 0)

        if used >= edge.maximum_iterations:
            return TransitionResult("loop_budget_exhausted")

        if not edge.progress_contract or not evidence.satisfies(edge.progress_contract):
            return TransitionResult("no_progress_evidence")

    if not edge.guard.evaluate(instance, evidence):
        return TransitionResult("guard_rejected")

    return TransitionResult(
        "authorized",
        expected_version=instance.version,
        consume_loop_iteration=bool(edge.loop_id),
    )


def future_deadline(minutes: int = 30) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)
