from tool_gateway import validate_order_lookup_call
from approval import validate_approval


def main():
    state = {"workflow_id": "refund_case_123", "order_id": "order_456"}
    tool_call = {
        "tool": "order_lookup",
        "arguments": {"order_id": "order_456", "fields": ["order_id", "delivery_date"]},
    }
    print(validate_order_lookup_call(tool_call, state))

    approval = {
        "workflow_id": "refund_case_123",
        "approved_action": "offer_replacement",
        "scope": {"order_id": "order_456", "item_id": "item_1", "maximum_value": 129.99, "currency": "USD"},
        "expires_at": "2099-08-03T16:00:00Z",
    }
    action = {
        "workflow_id": "refund_case_123",
        "action": "offer_replacement",
        "order_id": "order_456",
        "item_id": "item_1",
        "amount": 129.99,
        "currency": "USD",
        "idempotency_key": "replacement_order_456_item_1",
    }
    print(validate_approval(action, approval))


if __name__ == "__main__":
    main()
