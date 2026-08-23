"""Pipeline advancement utilities.

The controller validates a stage result before committing it. A stage result cannot
choose its own successor.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


class ContractError(Exception):
    pass


class StateError(Exception):
    pass


class PermissionError(Exception):
    pass


@dataclass
class Stage:
    stage_id: str
    owner: str
    output_contract: str
    evidence_scope: str


@dataclass
class StageResult:
    producer: str
    payload: Dict[str, Any]
    input_state_version: int
    evidence_refs: List[str]


class Registry:
    def validate(self, contract: str, payload: Dict[str, Any]) -> None:
        if not contract:
            raise ContractError("missing output contract")
        if not isinstance(payload, dict):
            raise ContractError("payload must be an object")

    def evidence_within_scope(self, evidence_refs: List[str], evidence_scope: str) -> bool:
        return all(ref.startswith(evidence_scope.split(":")[0]) for ref in evidence_refs)


class Store:
    def __init__(self) -> None:
        self.artifacts: List[StageResult] = []

    def accept_artifact(self, stage_result: StageResult) -> str:
        self.artifacts.append(stage_result)
        return f"artifact:{len(self.artifacts)}"


@dataclass
class PipelineInstance:
    current_stage: Stage
    version: int
    current_stage_id: str
    current_input_state_version: int

    def is_stage_current(self, stage_id: str, input_state_version: int) -> bool:
        return (
            stage_id == self.current_stage_id
            and input_state_version == self.current_input_state_version
        )

    def commit_stage_result(self, stage_id: str, artifact_ref: str, expected_version: int) -> Dict[str, Any]:
        if expected_version != self.version:
            raise StateError("pipeline version changed before commit")
        self.version += 1
        return {
            "status": "committed",
            "stage_id": stage_id,
            "artifact_ref": artifact_ref,
            "new_version": self.version,
        }


def advance_pipeline(instance: PipelineInstance, stage_result: StageResult, registry: Registry, store: Store) -> Dict[str, Any]:
    stage = instance.current_stage

    registry.validate(stage.output_contract, stage_result.payload)

    if stage_result.producer != stage.owner:
        raise ContractError("unexpected stage producer")

    if not instance.is_stage_current(
        stage.stage_id,
        stage_result.input_state_version,
    ):
        raise StateError("pipeline stage is no longer current")

    if not registry.evidence_within_scope(
        stage_result.evidence_refs,
        stage.evidence_scope,
    ):
        raise PermissionError("artifact exceeds stage evidence scope")

    accepted_ref = store.accept_artifact(stage_result)

    return instance.commit_stage_result(
        stage_id=stage.stage_id,
        artifact_ref=accepted_ref,
        expected_version=instance.version,
    )
