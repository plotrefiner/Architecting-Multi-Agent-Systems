from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AdmissionResult:
    status: str
    entry_ref: Optional[str] = None


@dataclass
class Proposal:
    entry_id: str
    producer: str
    entry_contract: str
    task_id: str
    input_state_version: int
    artifact_ref: str
    payload: Dict[str, Any]
    evidence_refs: List[str]
    claims_authority: bool = False
    claims_external_effect: bool = False


@dataclass
class Artifact:
    artifact_id: str
    producer: str
    input_state_version: int
    accepted: bool


@dataclass
class Board:
    allowed_producers: List[str]
    allowed_entry_contracts: List[str]
    evidence_scope: str
    version: int = 1
    entries: Dict[str, Proposal] = field(default_factory=dict)

    def append_once(self, proposal: Proposal, dedupe_key: str, expected_version: int) -> AdmissionResult:
        if expected_version != self.version:
            return AdmissionResult("version_conflict")
        if dedupe_key in self.entries:
            return AdmissionResult("duplicate", entry_ref=dedupe_key)
        self.entries[dedupe_key] = proposal
        self.version += 1
        return AdmissionResult("accepted", entry_ref=dedupe_key)


class GraphState:
    def __init__(self, current_tasks=None, current_artifacts=None):
        self.current_tasks = current_tasks or set()
        self.current_artifacts = current_artifacts or set()

    def is_task_current(self, task_id: str, input_state_version: int) -> bool:
        return (task_id, input_state_version) in self.current_tasks

    def is_artifact_current(self, artifact_id: str, input_state_version: int) -> bool:
        return (artifact_id, input_state_version) in self.current_artifacts


class Registry:
    def validates(self, entry_contract: str, payload: Dict[str, Any]) -> bool:
        return bool(entry_contract) and isinstance(payload, dict)

    def evidence_within_scope(self, evidence_refs: List[str], evidence_scope: str) -> bool:
        return all(isinstance(ref, str) and ref for ref in evidence_refs) and bool(evidence_scope)


class ArtifactStore:
    def __init__(self, artifacts: Dict[str, Artifact]):
        self.artifacts = artifacts

    def load(self, artifact_ref: str) -> Artifact:
        return self.artifacts[artifact_ref]


def admit_board_entry(proposal: Proposal, board: Board, graph: GraphState, registry: Registry, artifact_store: ArtifactStore) -> AdmissionResult:
    if proposal.producer not in board.allowed_producers:
        return AdmissionResult("producer_rejected")

    if proposal.entry_contract not in board.allowed_entry_contracts:
        return AdmissionResult("contract_rejected")

    if not graph.is_task_current(proposal.task_id, proposal.input_state_version):
        return AdmissionResult("task_invalidated")

    artifact = artifact_store.load(proposal.artifact_ref)

    if artifact.producer != proposal.producer:
        return AdmissionResult("artifact_owner_mismatch")

    if not artifact.accepted:
        return AdmissionResult("artifact_not_accepted")

    if not graph.is_artifact_current(artifact.artifact_id, artifact.input_state_version):
        return AdmissionResult("artifact_invalidated")

    if not registry.validates(proposal.entry_contract, proposal.payload):
        return AdmissionResult("payload_rejected")

    if not registry.evidence_within_scope(proposal.evidence_refs, board.evidence_scope):
        return AdmissionResult("scope_rejected")

    if proposal.claims_authority or proposal.claims_external_effect:
        return AdmissionResult("authority_claim_rejected")

    return board.append_once(
        proposal=proposal,
        dedupe_key=proposal.entry_id,
        expected_version=board.version,
    )
