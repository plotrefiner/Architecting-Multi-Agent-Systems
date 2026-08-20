"""Demo event-driven refund workflow.

Run:
    python code/demo_refund_workflow.py
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import sys

# Allow running from either repo root or this code directory.
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from event_bus import EventBus
from workflow_state import WorkflowState


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_event(
    event_type: str,
    workflow_id: str,
    producer: str,
    payload: dict,
    status: str = "success",
    correlation_id: str = "req_456",
) -> dict:
    return {
        "event_id": f"evt_{len(event_type)}_{len(producer)}",
        "event_type": event_type,
        "workflow_id": workflow_id,
        "correlation_id": correlation_id,
        "producer": producer,
        "timestamp": now_iso(),
        "schema_version": "1.0",
        "status": status,
        "payload": payload,
        "error": None,
    }


def main() -> None:
    workflow_id = "refund_case_123"
    state = WorkflowState(workflow_id=workflow_id)
    bus = EventBus()

    def router(event: dict) -> None:
        state.mark_step_completed("intent_classified")
        bus.publish(
            make_event(
                event_type="refund_intent_detected",
                workflow_id=workflow_id,
                producer="router_agent",
                payload={"intent": "refund_eligibility", "risk_level": "medium"},
            )
        )

    def policy_agent(event: dict) -> None:
        output = {
            "policy_findings": [
                {
                    "claim_id": "claim_001",
                    "claim": "Refunds are available within 30 days of delivery.",
                    "source_id": "refund_policy_v4",
                    "section": "3.2",
                    "confidence": "high",
                }
            ],
            "limitations": ["Item condition has not been verified."],
        }
        state.add_agent_output("policy_agent", output)
        bus.publish(
            make_event(
                event_type="policy_findings_created",
                workflow_id=workflow_id,
                producer="policy_agent",
                payload=output,
                status="partial",
            )
        )

    def customer_context_agent(event: dict) -> None:
        output = {
            "order_id": "order_456",
            "delivery_age_days": 12,
            "item_condition": "unknown",
        }
        state.add_agent_output("customer_context_agent", output)
        bus.publish(
            make_event(
                event_type="customer_context_retrieved",
                workflow_id=workflow_id,
                producer="customer_context_agent",
                payload=output,
            )
        )

    bus.subscribe("user_request_received", router)
    bus.subscribe("refund_intent_detected", policy_agent)
    bus.subscribe("refund_intent_detected", customer_context_agent)

    bus.publish(
        make_event(
            event_type="user_request_received",
            workflow_id=workflow_id,
            producer="api_gateway",
            payload={"user_request": "Can I return this item?"},
        )
    )

    print("Event log:")
    print(json.dumps(bus.event_log, indent=2))
    print("\nWorkflow state:")
    print(json.dumps(state.to_dict(), indent=2))


if __name__ == "__main__":
    main()
