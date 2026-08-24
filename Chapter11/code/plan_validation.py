from dataclasses import dataclass


@dataclass(frozen=True)
class PlanValidation:
    status: str
    reason: str | None = None


class ResponsibilityRegistry:
    def __init__(self, owners: dict[str, str]):
        self.owners = owners

    def has_responsibility(self, responsibility: str) -> bool:
        return responsibility in self.owners

    def owner_matches(self, responsibility: str, owner: str) -> bool:
        return self.owners.get(responsibility) == owner


def validate_plan(plan: dict, registry: ResponsibilityRegistry, policy: dict) -> PlanValidation:
    if len(plan.get("tasks", [])) > policy["maximum_tasks"]:
        return PlanValidation("rejected", "too_many_tasks")

    for task in plan.get("tasks", []):
        responsibility = task.get("responsibility")

        if not registry.has_responsibility(responsibility):
            return PlanValidation("rejected", "unknown_responsibility")

        if not registry.owner_matches(responsibility, task.get("owner")):
            return PlanValidation("rejected", "invalid_owner")

        if responsibility in policy.get("prohibited_responsibilities", []):
            return PlanValidation("rejected", "authority_violation")

        if "output_contract" not in task:
            return PlanValidation("rejected", "missing_output_contract")

    return PlanValidation("accepted", None)
