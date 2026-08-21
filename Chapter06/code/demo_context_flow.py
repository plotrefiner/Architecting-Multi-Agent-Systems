"""Demo: communication, state, memory, and context engineering."""

from context_filtering import build_context_for_agent, redact_sensitive_fields
from message_validation import validate_agent_message
from state_management import update_shared_state


def main():
    workflow_state = {
        "workflow_id": "refund_case_123",
        "user_request": "Can I return this item?",
        "intent": "refund_eligibility",
        "policy_findings": [{"claim": "Refunds are available within 30 days of delivery.", "source": "refund_policy_v4", "confidence": "high"}],
        "customer_context_summary": {"delivery_age_days": 12, "payment_method": "card_ending_1234"},
        "draft_response": "Based on the policy, you may be eligible for a return.",
        "limitations": ["Item condition still needs to be verified."],
    }

    memory_store = [
        {
            "memory_id": "org_policy_001",
            "memory_type": "organizational_policy",
            "title": "Refund Policy",
            "content": "Refunds are available within 30 days of delivery.",
            "authority": "approved_policy",
            "confidence": "high",
            "created_at": "2026-01-01T00:00:00Z",
            "expires_at": "2026-12-31T23:59:59Z",
        },
        {
            "memory_id": "user_mem_001",
            "memory_type": "user_preference",
            "content": "User prefers concise support responses.",
            "authority": "human_approved_case_note",
            "confidence": "high",
            "created_at": "2026-01-10T09:00:00Z",
            "expires_at": None,
        },
    ]

    message = {
        "message_id": "msg_101",
        "workflow_id": "refund_case_123",
        "task_id": "policy_review",
        "message_type": "policy_findings_created",
        "sender": "policy_agent",
        "receiver": "response_writer_agent",
        "status": "partial",
        "schema_version": "1.0",
        "payload": {"policy_findings": workflow_state["policy_findings"]},
        "uncertainties": ["The item condition has not been verified."],
    }

    print("Message validation:", validate_agent_message(message))
    update_shared_state(workflow_state, "verification_result", {"status": "supported_with_limitations"}, "verifier_agent")
    context = build_context_for_agent("response_writer_agent", workflow_state, memory_store)
    print("Response writer context:", redact_sensitive_fields(context))


if __name__ == "__main__":
    main()
