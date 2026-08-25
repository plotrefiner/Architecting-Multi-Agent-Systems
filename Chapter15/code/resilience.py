from __future__ import annotations
from typing import Mapping, Any

def retry_allowed(error_type: str, attempt_count: int, retry_policy: Mapping[str, Any]) -> bool:
    if error_type in retry_policy.get("non_retryable", []):
        return False
    return error_type in retry_policy.get("retryable", []) and attempt_count < int(retry_policy["maximum_total_attempts_per_workflow"])

def choose_fallback(failure: str, fallback_policy: list[Mapping[str, Any]]) -> str | None:
    for rule in fallback_policy:
        if rule.get("failure") == failure:
            return rule.get("fallback")
    return None

def safety_controls_enabled(degradation_policy: Mapping[str, Any]) -> bool:
    required = {"approval_gates", "pii_redaction", "tool_permission_checks", "audit_logging"}
    return required.issubset(set(degradation_policy.get("must_not_disable", [])))
