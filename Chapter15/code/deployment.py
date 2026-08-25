from __future__ import annotations
from typing import Mapping, Any

SAFETY_CRITICAL_CONTROLS = {"audit_logging", "pii_redaction", "approval_gates", "tool_permission_enforcement", "idempotency_for_actions"}

def validate_environment_policy(policy: Mapping[str, Any]) -> bool:
    replay = policy["replay"]
    return replay["real_action_tools"] is False and replay["send_customer_messages"] is False

def kill_switch_allowed(switch_name: str, kill_switches: Mapping[str, Any]) -> bool:
    return kill_switches.get(switch_name, {}).get("allowed", True) is not False

def disables_safety_control(control: str) -> bool:
    return control in SAFETY_CRITICAL_CONTROLS
