def compare(value, operator, threshold):
    if operator == "<":
        return value < threshold
    if operator == ">":
        return value > threshold
    if operator == "==":
        return value == threshold
    if operator == "in":
        return value in threshold
    raise ValueError(f"Unsupported operator: {operator}")


def handoff_required(policy: dict, signals: dict) -> bool:
    for rule in policy["handoff_policy"]["handoff_required_if"]:
        value = signals.get(rule["signal"])
        if compare(value, rule["operator"], rule["threshold"]):
            return True
    return False
