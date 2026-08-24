from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class ApprovalValidation:
    status: str
    reason: str | None = None


def validate_approval(action_command: Dict[str, Any], approval: Dict[str, Any] | None, now: datetime | None = None) -> ApprovalValidation:
    now = now or datetime.now(timezone.utc)
    if approval is None:
        return ApprovalValidation("rejected", "missing_approval")

    if approval.get("workflow_id") != action_command.get("workflow_id"):
        return ApprovalValidation("rejected", "workflow_mismatch")

    if approval.get("approved_action") != action_command.get("action"):
        return ApprovalValidation("rejected", "action_mismatch")

    scope = approval.get("scope", {})
    for field in ["order_id", "item_id", "currency"]:
        if scope.get(field) != action_command.get(field):
            return ApprovalValidation("rejected", "scope_mismatch")

    amount = action_command.get("amount")
    max_value = scope.get("maximum_value")
    if amount is not None and max_value is not None and amount > max_value:
        return ApprovalValidation("rejected", "amount_exceeds_scope")

    expires_at = approval.get("expires_at")
    if expires_at:
        exp = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if exp < now:
            return ApprovalValidation("rejected", "approval_expired")

    if "idempotency_key" not in action_command:
        return ApprovalValidation("rejected", "missing_idempotency_key")

    return ApprovalValidation("accepted")
