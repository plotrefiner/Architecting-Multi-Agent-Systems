"""Shared workflow state ownership utilities."""

STATE_OWNERS = {
    "intent": "router_agent",
    "risk_level": "router_agent",
    "policy_findings": "policy_agent",
    "customer_context_summary": "customer_context_agent",
    "draft_response": "response_writer_agent",
    "verification_result": "verifier_agent",
    "approval_status": "human_review_agent",
    "final_response": "orchestrator",
}


def update_shared_state(state: dict, field: str, value, agent_name: str) -> dict:
    """Update shared workflow state only when the agent owns the field."""
    owner = STATE_OWNERS.get(field)

    if owner is not None and owner != agent_name:
        raise PermissionError(
            f"{agent_name} cannot update {field}. Expected owner: {owner}"
        )

    state[field] = value
    return state
