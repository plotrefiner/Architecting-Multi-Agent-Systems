from datetime import datetime, timezone


class ApprovalResult(str):
    pass


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_approval(action_command: dict, approval: dict | None, clock) -> ApprovalResult:
    if approval is None:
        return ApprovalResult("missing_approval")

    if approval["workflow_id"] != action_command["workflow_id"]:
        return ApprovalResult("scope_mismatch")

    if approval["approved_action"] != action_command["action"]:
        return ApprovalResult("action_mismatch")

    for field in ["order_id", "item_id", "amount", "currency"]:
        if approval[field] != action_command[field]:
            return ApprovalResult("scope_mismatch")

    if clock.now() > parse_datetime(approval["expires_at"]):
        return ApprovalResult("approval_expired")

    if approval["reviewed_state_version"] != action_command["state_version"]:
        return ApprovalResult("state_version_mismatch")

    return ApprovalResult("approved")
