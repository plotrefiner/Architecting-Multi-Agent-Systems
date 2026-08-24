from datetime import datetime, timezone
from approval import validate_approval
from handoff import handoff_required
from review_packets import validate_review_packet


class Clock:
    def now(self):
        return datetime(2026, 8, 3, 15, 30, tzinfo=timezone.utc)


def main():
    action_command = {
        "workflow_id": "refund_case_123",
        "action": "offer_replacement",
        "order_id": "order_456",
        "item_id": "item_1",
        "amount": 129.99,
        "currency": "USD",
        "state_version": 7,
    }
    approval = {
        "workflow_id": "refund_case_123",
        "approved_action": "offer_replacement",
        "order_id": "order_456",
        "item_id": "item_1",
        "amount": 129.99,
        "currency": "USD",
        "reviewed_state_version": 7,
        "expires_at": "2026-08-03T16:00:00Z",
    }
    print("approval:", validate_approval(action_command, approval, Clock()))


if __name__ == "__main__":
    main()
