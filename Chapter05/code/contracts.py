"""Contract validation helpers."""

from __future__ import annotations

from typing import Any, Mapping


class ContractValidationError(ValueError):
    """Raised when an event does not satisfy its contract."""


def validate_required_fields(event: Mapping[str, Any], required_fields: list[str]) -> None:
    """Validate that all required top-level fields are present."""
    missing = [field for field in required_fields if field not in event]
    if missing:
        raise ContractValidationError(f"Missing required fields: {missing}")


def validate_status(event: Mapping[str, Any], allowed_statuses: list[str]) -> None:
    """Validate that the event status is one of the allowed values."""
    status = event.get("status")
    if status not in allowed_statuses:
        raise ContractValidationError(
            f"Invalid status {status!r}. Expected one of {allowed_statuses}."
        )


def validate_payload_types(
    event: Mapping[str, Any], payload_schema: Mapping[str, str]
) -> None:
    """Validate a simple payload schema.

    This demo supports the lightweight type names used in the chapter:
    array, boolean, string, object, and number.
    """
    payload = event.get("payload")
    if not isinstance(payload, dict):
        raise ContractValidationError("Event payload must be an object.")

    type_map = {
        "array": list,
        "boolean": bool,
        "string": str,
        "object": dict,
        "number": (int, float),
    }

    for field, expected_type_name in payload_schema.items():
        if field not in payload:
            raise ContractValidationError(f"Missing payload field: {field}")

        expected_type = type_map.get(expected_type_name)
        if expected_type is None:
            raise ContractValidationError(
                f"Unsupported schema type {expected_type_name!r} for {field}."
            )

        if not isinstance(payload[field], expected_type):
            raise ContractValidationError(
                f"Payload field {field!r} must be {expected_type_name}."
            )


def validate_event(event: Mapping[str, Any], contract: Mapping[str, Any]) -> None:
    """Validate an event against a lightweight event contract."""
    validate_required_fields(event, list(contract["required_fields"]))
    validate_status(event, list(contract["status_values"]))
    validate_payload_types(event, dict(contract["payload_schema"]))
