from board_admission import Artifact, ArtifactStore, Board, GraphState, Proposal, Registry, admit_board_entry
from verification import ClaimChecker, Instance, Policy, Services, VerificationGate, Verifier, run_bounded_verification
from consensus import bounded_consensus
from swarm import CandidateMerger, SwarmBudget


def main():
    board = Board(
        allowed_producers=["chargeback_lookup_service"],
        allowed_entry_contracts=["evidence_claim_v1"],
        evidence_scope="composite_refund_case",
    )
    graph = GraphState(
        current_tasks={("task_1", 5)},
        current_artifacts={("chargeback_303", 5)},
    )
    artifact_store = ArtifactStore({
        "artifact:chargeback_303": Artifact(
            artifact_id="chargeback_303",
            producer="chargeback_lookup_service",
            input_state_version=5,
            accepted=True,
        )
    })
    proposal = Proposal(
        entry_id="eb_401",
        producer="chargeback_lookup_service",
        entry_contract="evidence_claim_v1",
        task_id="task_1",
        input_state_version=5,
        artifact_ref="artifact:chargeback_303",
        payload={"claim": "chargeback open"},
        evidence_refs=["chargeback:cb_908:snapshot_17"],
    )
    admission = admit_board_entry(proposal, board, graph, Registry(), artifact_store)

    services = Services(ClaimChecker(), Verifier(), VerificationGate())
    verification = run_bounded_verification(Instance(), "artifact:draft_501", services, Policy())

    consensus = bounded_consensus(["needs_review", "needs_review", "abstain"])

    budget = SwarmBudget(maximum_participants=4, maximum_tasks=12, maximum_messages=24, maximum_rounds=2)
    budget.consume_task()
    merger = CandidateMerger()
    candidate_added = merger.add_candidate("clause_1:source_hash_1")

    print({
        "board_admission": admission.status,
        "verification": verification.status,
        "consensus": consensus.outcome,
        "swarm_tasks_used": budget.tasks_used,
        "candidate_added": candidate_added,
    })


if __name__ == "__main__":
    main()
