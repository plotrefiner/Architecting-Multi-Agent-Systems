TOOL_PERMISSIONS = {
    "policy_search": {
        "allowed_agents": {"policy_agent", "verifier_agent"},
        "approval_required": False,
    },
    "order_lookup": {
        "allowed_agents": {"customer_context_agent"},
        "approval_required": False,
    },
    "issue_refund": {
        "allowed_agents": {"action_agent"},
        "approval_required": True,
    },
}


def validate_tool_call(agent_name, tool_name, approval_id=None):
    policy = TOOL_PERMISSIONS.get(tool_name)

    if policy is None:
        return {"allowed": False, "reason": "Unknown tool."}

    if agent_name not in policy["allowed_agents"]:
        return {
            "allowed": False,
            "reason": f"{agent_name} cannot call {tool_name}.",
        }

    if policy["approval_required"] and approval_id is None:
        return {
            "allowed": False,
            "reason": f"{tool_name} requires approval.",
        }

    return {"allowed": True, "reason": "Tool call allowed."}
