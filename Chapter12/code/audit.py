REQUIRED_AUDIT_FIELDS = {
    "workflow_id",
    "user_request_ref",
    "workflow_graph_version",
    "accepted_artifacts",
    "human_review",
    "action",
    "final_response_ref",
    "terminal_status",
}


def validate_audit_trail(audit_trail: dict) -> tuple[bool, list[str]]:
    record = audit_trail.get("audit_trail", audit_trail)
    missing = sorted(REQUIRED_AUDIT_FIELDS - set(record))
    if missing:
        return False, missing
    if not record["accepted_artifacts"]:
        return False, ["accepted_artifacts_empty"]
    if "decision_id" not in record["human_review"]:
        return False, ["missing_decision_id"]
    return True, []
