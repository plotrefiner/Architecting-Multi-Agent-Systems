"""Memory access and retrieval utilities."""

from datetime import datetime, timezone

MEMORY_ACCESS_RULES = {
    "router_agent": {"allowed_memory_types": ["task_memory", "intent_catalog"]},
    "policy_agent": {"allowed_memory_types": ["organizational_policy", "task_memory"]},
    "customer_context_agent": {"allowed_memory_types": ["task_memory"]},
    "response_writer_agent": {
        "allowed_memory_types": ["task_memory", "user_preference", "approved_response_guideline"]
    },
    "verifier_agent": {
        "allowed_memory_types": ["organizational_policy", "retrieved_evidence", "task_memory"]
    },
    "human_review_agent": {
        "allowed_memory_types": ["task_memory", "organizational_policy", "audit_memory"]
    },
}


def can_access_memory(agent_name: str, memory_item: dict) -> bool:
    allowed_types = MEMORY_ACCESS_RULES[agent_name]["allowed_memory_types"]
    return memory_item["memory_type"] in allowed_types


def parse_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def is_expired(memory: dict, now: datetime) -> bool:
    expires_at = memory.get("expires_at")
    return False if expires_at is None else parse_datetime(expires_at) < now


def matches_query(query: str, memory: dict) -> bool:
    haystack = " ".join(str(memory.get(field, "")) for field in ("title", "content", "memory_type", "source")).lower()
    return any(token.lower() in haystack for token in query.split())


def score_memory(query: str, memory: dict, now: datetime) -> float:
    relevance = 1.0 if matches_query(query, memory) else 0.0
    authority = {"approved_policy": 1.0, "official_repository": 0.9, "unverified_note": 0.2}.get(memory.get("authority"), 0.3)
    confidence = {"high": 1.0, "medium": 0.6, "low": 0.3}.get(memory.get("confidence", "medium"), 0.5)
    return 0.55 * relevance + 0.30 * authority + 0.15 * confidence


def retrieve_memory(agent_name: str, query: str, memory_store: list[dict], now=None, limit: int = 5) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    candidates = []
    for memory in memory_store:
        if not can_access_memory(agent_name, memory):
            continue
        if is_expired(memory, now):
            continue
        if not matches_query(query, memory):
            continue
        candidates.append((score_memory(query, memory, now), memory))
    ranked = sorted(candidates, key=lambda item: item[0], reverse=True)
    return [memory for score, memory in ranked[:limit]]
