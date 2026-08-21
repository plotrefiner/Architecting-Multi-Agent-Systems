"""Message validation utilities."""

REQUIRED_MESSAGE_FIELDS = {
    "message_id", "workflow_id", "task_id", "message_type",
    "sender", "status", "schema_version", "payload",
}

VALID_STATUSES = {"success", "partial", "failed", "uncertain", "needs_human_review"}


def validate_agent_message(message: dict) -> dict:
    """Validate a structured inter-agent message."""
    missing_fields = REQUIRED_MESSAGE_FIELDS - set(message)

    if missing_fields:
        return {
            "valid": False,
            "error_type": "missing_required_fields",
            "details": sorted(missing_fields),
        }

    if message["status"] not in VALID_STATUSES:
        return {
            "valid": False,
            "error_type": "invalid_status",
            "details": message["status"],
        }

    if message["status"] in {"failed", "uncertain"}:
        if not message.get("error") and not message.get("uncertainties"):
            return {
                "valid": False,
                "error_type": "missing_failure_details",
                "details": "Failed or uncertain messages need error or uncertainty details.",
            }

    return {"valid": True, "error_type": None, "details": None}
