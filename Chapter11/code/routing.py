def validate_route(routing_result: dict, allowed_routes: set[str], prohibited_components: set[str]) -> tuple[bool, str | None]:
    result = routing_result.get("routing_result", routing_result)

    if result.get("selected_route") not in allowed_routes:
        return False, "unknown_route"

    next_component = result.get("recommended_next_component")
    if next_component in prohibited_components:
        return False, "prohibited_next_component"

    for component in result.get("prohibited_next_components", []):
        if component not in prohibited_components:
            continue

    return True, None


def choose_model(task_name: str, policy: dict, classifier_confidence: float | None = None) -> str:
    routing = policy["model_routing_policy"][task_name]
    if task_name == "intent_classification" and classifier_confidence is not None:
        if classifier_confidence < 0.85:
            return routing.get("fallback", routing["default"])
    return routing["default"]
