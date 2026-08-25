from dataclasses import dataclass


@dataclass(frozen=True)
class BaselineResult:
    baseline: str
    sufficient: bool
    limitations: list[str]


def evaluate_prompt_only(
    requires_external_knowledge: bool,
    requires_user_specific_data: bool,
    requires_action: bool,
) -> BaselineResult:
    limitations = []

    if requires_external_knowledge:
        limitations.append("cannot access authoritative external knowledge")

    if requires_user_specific_data:
        limitations.append("cannot inspect user-specific or order-specific state")

    if requires_action:
        limitations.append("cannot safely execute or approve external actions")

    return BaselineResult(
        baseline="prompt_only",
        sufficient=len(limitations) == 0,
        limitations=limitations,
    )


def evaluate_rag(
    requires_user_specific_data: bool,
    requires_action: bool,
    requires_dynamic_tool_choice: bool,
) -> BaselineResult:
    limitations = []

    if requires_user_specific_data:
        limitations.append("RAG alone cannot inspect user-specific operational state")

    if requires_action:
        limitations.append("RAG alone should not execute write-capable actions")

    if requires_dynamic_tool_choice:
        limitations.append("RAG alone does not decide among tools or recovery paths")

    return BaselineResult(
        baseline="rag_pipeline",
        sufficient=len(limitations) == 0,
        limitations=limitations,
    )


def compare_baselines(requirements: dict[str, bool]) -> list[BaselineResult]:
    return [
        evaluate_prompt_only(
            requires_external_knowledge=requirements.get("requires_external_knowledge", False),
            requires_user_specific_data=requirements.get("requires_user_specific_data", False),
            requires_action=requirements.get("requires_action", False),
        ),
        evaluate_rag(
            requires_user_specific_data=requirements.get("requires_user_specific_data", False),
            requires_action=requirements.get("requires_action", False),
            requires_dynamic_tool_choice=requirements.get("requires_dynamic_tool_choice", False),
        ),
    ]
