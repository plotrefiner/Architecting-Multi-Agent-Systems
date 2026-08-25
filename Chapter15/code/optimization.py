from __future__ import annotations
from typing import Mapping, Any

def cache_key(operation: str, fields: Mapping[str, Any]) -> str:
    ordered = ":".join(f"{key}={fields[key]}" for key in sorted(fields))
    return f"{operation}:{ordered}"

def under_context_budget(component: str, input_tokens: int, budget: Mapping[str, Any]) -> bool:
    return input_tokens <= int(budget[component]["maximum_input_tokens"])
