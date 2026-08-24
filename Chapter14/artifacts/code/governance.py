from typing import Any, Dict, List


def required_reviews_for_change(change: Dict[str, Any]) -> List[str]:
    risk = change.get("risk_assessment", "low")
    reviews = set(change.get("required_reviews", []))
    if risk in {"medium", "high", "critical"}:
        reviews.update({"data_owner", "privacy_owner", "ai_quality_owner"})
    if change.get("change_type") in {"expand_tool_permission", "enable_autonomous_action"}:
        reviews.add("security_owner")
    return sorted(reviews)


def route_governance_escalation(trigger: str, policy: Dict[str, str]) -> str:
    return policy.get(trigger, "ai_quality_review")
