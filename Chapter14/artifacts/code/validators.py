from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class ValidationResult:
    status: str
    reason: str | None = None


def validate_required_fields(payload: Dict[str, Any], required: Iterable[str]) -> ValidationResult:
    missing = [field for field in required if field not in payload or payload[field] in (None, "")]
    if missing:
        return ValidationResult("rejected", f"missing:{','.join(missing)}")
    return ValidationResult("accepted")


def reject_prohibited_fields(payload: Dict[str, Any], prohibited: Iterable[str]) -> ValidationResult:
    present = [field for field in prohibited if field in payload]
    if present:
        return ValidationResult("rejected", f"prohibited:{','.join(present)}")
    return ValidationResult("accepted")


def classify_validation_failure(failure_type: str, policy: List[Dict[str, Any]]) -> Dict[str, Any]:
    for rule in policy:
        if rule.get("failure_type") == failure_type:
            return rule
    return {"failure_type": failure_type, "outcome": "safe_stop", "retry": False}
