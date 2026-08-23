"""Message contract helpers."""


class ContractError(ValueError):
    """Raised when a message violates its envelope contract."""


REQUIRED_ENVELOPE_FIELDS = {
    "envelope_version",
    "message_id",
    "message_kind",
    "message_type",
    "schema",
    "workflow_id",
    "causation_id",
    "producer",
    "occurred_at",
    "data_classification",
}


def validate_envelope(message):
    missing = REQUIRED_ENVELOPE_FIELDS - set(message)

    if missing:
        raise ContractError(f"missing required envelope fields: {sorted(missing)}")

    if message["message_kind"] not in {"command", "event"}:
        raise ContractError("message_kind must be command or event")

    schema = message.get("schema", {})
    if "name" not in schema or "version" not in schema:
        raise ContractError("schema must include name and version")

    return True
