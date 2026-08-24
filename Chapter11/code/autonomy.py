def action_requires_human_approval(action: str, autonomy_boundary: dict) -> bool:
    boundary = autonomy_boundary.get("autonomy_boundary", autonomy_boundary)
    return action in set(boundary.get("requires_human_approval", []))


def is_always_prohibited(action: str, autonomy_boundary: dict) -> bool:
    boundary = autonomy_boundary.get("autonomy_boundary", autonomy_boundary)
    return action in set(boundary.get("always_prohibited", []))


def resolve_stop_condition(condition: str, stopping_policy: dict) -> str | None:
    policy = stopping_policy.get("stopping_policy", stopping_policy)
    for item in policy.get("stop_conditions", []):
        if item.get("condition") == condition:
            return item.get("outcome")
    return None
