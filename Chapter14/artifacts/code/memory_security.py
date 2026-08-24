from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List


def memory_requires_review(memory: Dict[str, Any], admission_policy: Dict[str, Any]) -> bool:
    memory_type = memory.get("memory_type")
    for rule in admission_policy.get("requires_review", []):
        if rule.get("memory_type") == memory_type:
            return True
    return bool(memory.get("requires_review"))


def memory_always_rejected(memory: Dict[str, Any], admission_policy: Dict[str, Any]) -> bool:
    memory_type = memory.get("memory_type")
    return any(rule.get("memory_type") == memory_type for rule in admission_policy.get("always_reject", []))


def retrieve_safe_memory(agent_name: str, query: str, memory_store: Iterable[Dict[str, Any]], policy: Dict[str, Any], now: datetime | None = None) -> List[Dict[str, Any]]:
    now = now or datetime.now(timezone.utc)
    results: List[Dict[str, Any]] = []
    allowed_types = set(policy.get("allowed_types", {}).get(agent_name, []))
    allowed_sensitivity = set(policy.get("allowed_sensitivity", {}).get(agent_name, []))

    for memory in memory_store:
        if allowed_types and memory.get("memory_type") not in allowed_types:
            continue
        if allowed_sensitivity and memory.get("sensitivity") not in allowed_sensitivity:
            continue
        expires_at = memory.get("expires_at")
        if expires_at:
            exp = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if exp < now:
                continue
        if memory.get("authority") == "unverified":
            continue
        if query.lower() not in memory.get("content", "").lower():
            continue
        results.append(memory)

    return results
