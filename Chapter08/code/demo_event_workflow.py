"""Run a small delivery and idempotency demo."""

from idempotency import InMemoryIdempotencyStore, complete_idempotent_command
from message_contracts import validate_envelope
from retry_policy import should_retry


def main():
    message = {
        "envelope_version": 1,
        "message_id": "cmd_refund_810",
        "message_kind": "command",
        "message_type": "execute_approved_refund",
        "schema": {"name": "approved_action_command", "version": 1},
        "workflow_id": "refund_case_123",
        "causation_id": "approval_456",
        "producer": {"component": "workflow_controller"},
        "occurred_at": "2026-08-03T15:10:00Z",
        "data_classification": "confidential",
    }
    print({"valid_envelope": validate_envelope(message)})

    policy = {
        "maximum_attempts": 3,
        "retry_on": ["timeout", "rate_limited"],
        "never_retry": ["contract_invalid", "permission_denied"],
        "workflow_deadline_required": True,
    }
    print({"retry_timeout": should_retry("timeout", 1, policy)})

    store = InMemoryIdempotencyStore()
    command = {
        "idempotency_key": "refund_case_123:refund:approval_456",
        "request_hash": "sha256:abc123",
    }

    first = complete_idempotent_command(command, "artifact:refund_result_811", store)
    duplicate = complete_idempotent_command(command, "artifact:refund_result_811", store)

    print({"first_status": first.status, "duplicate_status": duplicate.status})
    print({"outbox_count": len(store.outbox())})


if __name__ == "__main__":
    main()
