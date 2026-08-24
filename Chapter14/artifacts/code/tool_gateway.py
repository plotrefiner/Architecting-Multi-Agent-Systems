from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ToolValidation:
    status: str
    reason: str | None = None


def validate_order_lookup_call(tool_call: Dict[str, Any], workflow_state: Dict[str, Any]) -> ToolValidation:
    if tool_call.get("tool") != "order_lookup":
        return ToolValidation("rejected", "wrong_tool")

    arguments = tool_call.get("arguments", {})
    if arguments.get("order_id") != workflow_state.get("order_id"):
        return ToolValidation("rejected", "order_id_mismatch")

    allowed_fields = {"order_id", "delivery_date", "item_status", "shipping_region"}
    requested_fields = set(arguments.get("fields", []))

    if not requested_fields.issubset(allowed_fields):
        return ToolValidation("rejected", "field_scope_violation")

    return ToolValidation("accepted")
