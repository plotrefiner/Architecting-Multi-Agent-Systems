REQUIRED_PACKET_FIELDS = {
    "review_packet_id",
    "workflow_id",
    "review_type",
    "requested_role",
    "requested_authority",
    "accepted_artifacts",
    "decision_options",
    "expires_at",
}


def validate_review_packet(packet: dict) -> tuple[bool, list[str]]:
    missing = sorted(REQUIRED_PACKET_FIELDS - set(packet))
    if missing:
        return False, missing
    if not packet["accepted_artifacts"]:
        return False, ["accepted_artifacts_empty"]
    if packet.get("agent_recommendation", {}).get("type") != "proposal_only":
        return False, ["agent_recommendation_must_be_proposal_only"]
    return True, []
