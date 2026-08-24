def estimate_plan_cost(plan: dict, cost_model) -> dict:
    total = {
        "model_calls": 0,
        "tool_calls": 0,
        "estimated_usd": 0.0,
        "estimated_latency_seconds": 0,
    }

    for task in plan.get("tasks", []):
        estimate = cost_model.estimate(task)

        total["model_calls"] += estimate.model_calls
        total["tool_calls"] += estimate.tool_calls
        total["estimated_usd"] += estimate.usd
        total["estimated_latency_seconds"] += estimate.latency_seconds

    return total


def select_lowest_cost_valid_plan(candidate_plans: list[dict]) -> dict | None:
    valid = [plan for plan in candidate_plans if plan.get("meets_requirements")]
    if not valid:
        return None
    return min(valid, key=lambda plan: plan.get("estimated_cost_usd", float("inf")))
