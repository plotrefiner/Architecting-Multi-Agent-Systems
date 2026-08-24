from dataclasses import dataclass


@dataclass(frozen=True)
class TaskAdmission:
    status: str
    reason: str | None = None


def authorize_task_creation(parent_task, proposed_task: dict, policy) -> TaskAdmission:
    if parent_task.depth + 1 > policy.maximum_depth:
        return TaskAdmission("rejected", "maximum_depth_exceeded")

    if policy.task_count >= policy.maximum_total_tasks:
        return TaskAdmission("rejected", "task_budget_exhausted")

    if proposed_task.get("responsibility") not in policy.allowed_responsibilities:
        return TaskAdmission("rejected", "unknown_responsibility")

    if proposed_task.get("may_trigger_external_action"):
        return TaskAdmission("rejected", "authority_violation")

    return TaskAdmission("accepted", None)
