from dataclasses import dataclass
from enum import Enum


class ValueLevel(str, Enum):
    LOW = "low"
    HIGH = "high"


class RiskLevel(str, Enum):
    LOW = "low"
    HIGH = "high"


@dataclass(frozen=True)
class MatrixDecision:
    value: ValueLevel
    risk: RiskLevel
    recommendation: str
    rationale: str


def classify_value_risk(value: str, risk: str) -> MatrixDecision:
    value_level = ValueLevel(value)
    risk_level = RiskLevel(risk)

    if value_level == ValueLevel.LOW and risk_level == RiskLevel.LOW:
        return MatrixDecision(
            value_level,
            risk_level,
            "prompt_only_or_simple_chain",
            "Low value and low risk do not justify added agentic complexity.",
        )

    if value_level == ValueLevel.HIGH and risk_level == RiskLevel.LOW:
        return MatrixDecision(
            value_level,
            risk_level,
            "rag_tool_calling_or_single_agent",
            "Higher value may justify retrieval, tools, or a bounded agent.",
        )

    if value_level == ValueLevel.LOW and risk_level == RiskLevel.HIGH:
        return MatrixDecision(
            value_level,
            risk_level,
            "human_owned_or_avoid_automation",
            "High risk with limited value is usually not worth automation.",
        )

    return MatrixDecision(
        value_level,
        risk_level,
        "bounded_multi_agent_with_human_oversight",
        "High-value, high-risk workflows may justify separation, verification, guardrails, and human review.",
    )
