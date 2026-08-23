"""Small demo for utilities."""

from datetime import datetime, timezone, timedelta

from gates import Artifact, Clock as GateClock, Graph, Registry as GateRegistry, Task, evaluate_gate
from transitions import Clock, Edge, Evidence, GraphInstance, Guard, authorize_transition


def demo() -> None:
    task = Task(
        task_id="del_701",
        output_contract="policy_findings_v1",
        assigned_owner="policy_retrieval_service",
        input_state_version=4,
        deadline=datetime.now(timezone.utc) + timedelta(minutes=5),
        evidence_scope="policy:region_us",
    )
    artifact = Artifact(
        artifact_id="pf_101",
        artifact_contract="policy_findings_v1",
        producer="policy_retrieval_service",
        payload_ref="artifact_payload:pf_101",
        evidence_refs=["policy:v4:section3.2"],
    )
    gate = evaluate_gate(
        artifact=artifact,
        task=task,
        graph=Graph({("del_701", 4)}),
        registry=GateRegistry(),
        clock=GateClock(),
    )
    print({"gate_result": gate.outcome, "artifact_ref": gate.artifact_ref})

    instance = GraphInstance(
        current_node="draft_conditional_response",
        workflow_deadline=datetime.now(timezone.utc) + timedelta(minutes=10),
        version=8,
    )
    edge = Edge(
        source="draft_conditional_response",
        guard=Guard(True),
        loop_id="response_revision_v1",
        maximum_iterations=1,
        progress_contract="unsupported_claims_resolved_v1",
    )
    result = authorize_transition(
        instance=instance,
        edge=edge,
        evidence=Evidence({"unsupported_claims_resolved_v1"}),
        clock=Clock(),
    )
    print({"transition_result": result.outcome, "expected_version": result.expected_version})


if __name__ == "__main__":
    demo()
