"""Idempotency helpers."""

from dataclasses import dataclass


class IdempotencyConflict(ValueError):
    """Raised when a key is reused with different request parameters."""


@dataclass
class Outcome:
    idempotency_key: str
    request_hash: str
    status: str
    artifact_ref: str


class InMemoryIdempotencyStore:
    def __init__(self):
        self._outcomes = {}
        self._outbox = []

    def command_outcome(self, idempotency_key):
        return self._outcomes.get(idempotency_key)

    def record_command_completed(self, command, artifact_ref):
        outcome = Outcome(
            idempotency_key=command["idempotency_key"],
            request_hash=command["request_hash"],
            status="completed",
            artifact_ref=artifact_ref,
        )
        self._outcomes[command["idempotency_key"]] = outcome
        return outcome

    def add_outbox_message(self, message):
        self._outbox.append(message)

    def outbox(self):
        return list(self._outbox)


def complete_idempotent_command(command, result_artifact_ref, store):
    previous = store.command_outcome(command["idempotency_key"])

    if previous:
        if previous.request_hash != command["request_hash"]:
            raise IdempotencyConflict("key reused with different request")

        return previous

    outcome = store.record_command_completed(command, result_artifact_ref)
    store.add_outbox_message(
        {
            "message_kind": "event",
            "message_type": "command_completed",
            "idempotency_key": command["idempotency_key"],
            "artifact_ref": result_artifact_ref,
        }
    )
    return outcome
