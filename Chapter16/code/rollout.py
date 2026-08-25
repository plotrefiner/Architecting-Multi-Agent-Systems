from __future__ import annotations


def next_rollout_stage(stages: list[dict], current_stage: str) -> dict | None:
    names = [stage.get("stage") for stage in stages]
    if current_stage not in names:
        return stages[0] if stages else None
    index = names.index(current_stage) + 1
    return stages[index] if index < len(stages) else None


def should_rollback(metrics: dict, rollback_conditions: list[str]) -> bool:
    checks = {
        "unsupported_claim_rate_above_threshold": metrics.get("unsupported_claim_rate", 0) > metrics.get("unsupported_claim_threshold", 0.02),
        "sql_policy_violation_detected": metrics.get("sql_policy_violations", 0) > 0,
        "pii_exposure_detected": metrics.get("pii_exposure_incidents", 0) > 0,
        "p95_latency_above_slo": metrics.get("p95_latency", 0) > metrics.get("p95_latency_slo", 20),
    }
    return any(checks.get(condition, False) for condition in rollback_conditions)
