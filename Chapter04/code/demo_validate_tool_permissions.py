from validate_tool_permissions import validate_tool_call


def main():
    cases = [
        ("policy_agent", "policy_search", None),
        ("router_agent", "policy_search", None),
        ("action_agent", "issue_refund", None),
        ("action_agent", "issue_refund", "approval_789"),
        ("verifier_agent", "issue_refund", "approval_789"),
    ]

    for agent_name, tool_name, approval_id in cases:
        result = validate_tool_call(agent_name, tool_name, approval_id)
        print(f"{agent_name} -> {tool_name}: {result}")


if __name__ == "__main__":
    main()
