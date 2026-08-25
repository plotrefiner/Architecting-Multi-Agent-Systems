from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureLevel:
    level: int
    name: str
    capability: str
    added_burden: str


ARCHITECTURE_LADDER = [
    ArchitectureLevel(
        1,
        "prompt_only",
        "One model call with instructions.",
        "Lowest operational burden.",
    ),
    ArchitectureLevel(
        2,
        "prompt_chain",
        "Multiple fixed LLM steps.",
        "More prompts and intermediate outputs to test.",
    ),
    ArchitectureLevel(
        3,
        "rag_pipeline",
        "Retrieval plus generation from controlled sources.",
        "Requires retrieval evaluation and citation checks.",
    ),
    ArchitectureLevel(
        4,
        "deterministic_workflow",
        "Explicit rules, branches, and validations.",
        "Requires rule maintenance and branch testing.",
    ),
    ArchitectureLevel(
        5,
        "tool_calling_application",
        "Controlled read or write access to external systems.",
        "Requires permissions, schemas, and tool-call validation.",
    ),
    ArchitectureLevel(
        6,
        "single_agent_system",
        "One bounded agent makes runtime decisions.",
        "Requires trajectory evaluation and stopping rules.",
    ),
    ArchitectureLevel(
        7,
        "graph_based_agent_workflow",
        "Explicit state transitions and conditional paths.",
        "Requires graph orchestration and state management.",
    ),
    ArchitectureLevel(
        8,
        "multi_agent_system",
        "Specialized agents coordinate across responsibilities.",
        "Requires contracts, routing, verification, and observability.",
    ),
    ArchitectureLevel(
        9,
        "human_supervised_multi_agent_system",
        "Agents plus review, approval, audit, and governance.",
        "Highest operational and governance burden.",
    ),
]


def get_architecture_level(name: str) -> ArchitectureLevel:
    for level in ARCHITECTURE_LADDER:
        if level.name == name:
            return level

    raise ValueError(f"Unknown architecture level: {name}")


def explain_ladder() -> list[dict[str, str | int]]:
    return [
        {
            "level": item.level,
            "name": item.name,
            "capability": item.capability,
            "added_burden": item.added_burden,
        }
        for item in ARCHITECTURE_LADDER
    ]
