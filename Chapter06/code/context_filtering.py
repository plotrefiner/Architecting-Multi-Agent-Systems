"""Context filtering and redaction utilities."""

from memory_access import retrieve_memory

SENSITIVE_FIELDS = {
    "payment_method", "credit_card_number", "internal_risk_score",
    "private_customer_notes", "access_token", "api_key",
}


def redact_sensitive_fields(data):
    if isinstance(data, dict):
        return {
            key: "[REDACTED]" if key in SENSITIVE_FIELDS else redact_sensitive_fields(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [redact_sensitive_fields(item) for item in data]
    return data


def extract_claims(draft_response: str) -> list[dict]:
    return [] if not draft_response else [{"claim_id": "claim_001", "claim": draft_response}]


def collect_evidence(workflow_state: dict) -> list[dict]:
    return [
        {"source": finding.get("source", "unknown"), "claim": finding.get("claim")}
        for finding in workflow_state.get("policy_findings", [])
        if isinstance(finding, dict)
    ]


def build_context_for_agent(agent_name: str, workflow_state: dict, memory_store: list[dict]):
    if agent_name == "router_agent":
        return {
            "user_request": workflow_state["user_request"],
            "supported_intents": ["refund_eligibility", "order_status", "product_question", "technical_support"],
        }

    if agent_name == "policy_agent":
        return {
            "intent": workflow_state["intent"],
            "product_category": workflow_state.get("product_category"),
            "region": workflow_state.get("region", "US"),
            "policy_memory": retrieve_memory("policy_agent", workflow_state["intent"], memory_store),
        }

    if agent_name == "response_writer_agent":
        return {
            "user_request": workflow_state["user_request"],
            "approved_policy_findings": workflow_state["policy_findings"],
            "customer_context_summary": workflow_state["customer_context_summary"],
            "limitations": workflow_state.get("limitations", []),
            "user_preferences": retrieve_memory("response_writer_agent", "communication preference", memory_store),
        }

    if agent_name == "verifier_agent":
        return {
            "draft_response": workflow_state["draft_response"],
            "claims_to_verify": extract_claims(workflow_state["draft_response"]),
            "evidence": collect_evidence(workflow_state),
        }

    raise ValueError(f"Unknown agent: {agent_name}")
