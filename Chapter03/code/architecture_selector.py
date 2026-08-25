from dataclasses import dataclass

from baseline_evaluator import compare_baselines
from risk_value_matrix import classify_value_risk


@dataclass(frozen=True)
class ArchitectureRecommendation:
    selected_architecture: str
    why_not_simpler: list[str]
    required_controls: list[str]


def select_architecture(requirements: dict[str, bool], value: str, risk: str) -> ArchitectureRecommendation:
    baselines = compare_baselines(requirements)
    matrix_decision = classify_value_risk(value=value, risk=risk)

    why_not_simpler = []
    for baseline in baselines:
        if not baseline.sufficient:
            why_not_simpler.append(
                f"{baseline.baseline}: " + "; ".join(baseline.limitations)
            )

    if matrix_decision.recommendation == "bounded_multi_agent_with_human_oversight":
        return ArchitectureRecommendation(
            selected_architecture="hybrid_multi_agent_workflow",
            why_not_simpler=why_not_simpler,
            required_controls=[
                "deterministic_router",
                "tool_permissions",
                "refund_rules_engine",
                "verification",
                "human_approval_for_high_risk_actions",
                "audit_logging",
            ],
        )

    if requirements.get("requires_dynamic_tool_choice", False):
        return ArchitectureRecommendation(
            selected_architecture="single_agent_or_graph_based_agent_workflow",
            why_not_simpler=why_not_simpler,
            required_controls=[
                "tool_permissions",
                "bounded_decisions",
                "stopping_rules",
                "audit_logging",
            ],
        )

    if requirements.get("requires_user_specific_data", False):
        return ArchitectureRecommendation(
            selected_architecture="deterministic_workflow_with_tools_and_rag",
            why_not_simpler=why_not_simpler,
            required_controls=[
                "read_only_tool_access",
                "rules_engine",
                "output_validation",
            ],
        )

    if requirements.get("requires_external_knowledge", False):
        return ArchitectureRecommendation(
            selected_architecture="rag_pipeline",
            why_not_simpler=why_not_simpler,
            required_controls=[
                "source_citations",
                "groundedness_check",
                "insufficient_evidence_response",
            ],
        )

    return ArchitectureRecommendation(
        selected_architecture="prompt_only",
        why_not_simpler=[],
        required_controls=[
            "input_output_examples",
            "basic_output_review",
        ],
    )
