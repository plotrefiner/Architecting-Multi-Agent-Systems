from execution import choose_execution_mode, join_ready
from resilience import choose_fallback, retry_allowed, safety_controls_enabled

parallelism_policy = {
    "missing_order_identifier": {"execution": "no_parallel_work", "reason": "required field missing"},
    "composite_refund_chargeback": {"execution": "parallel_evidence_collection", "reason": "independent evidence"},
}
join_policy = {"required": ["policy_findings", "order_summary"], "conditionally_required": {"chargeback_status": "chargeback_mentioned_or_detected"}}
retry_policy = {"maximum_total_attempts_per_workflow": 8, "retryable": ["timeout"], "non_retryable": ["approval_expired"]}
fallback_policy = [{"failure": "chargeback_lookup_unavailable", "fallback": "human_review_or_wait"}]
degradation_policy = {"must_not_disable": ["approval_gates", "pii_redaction", "tool_permission_checks", "audit_logging"]}

if __name__ == "__main__":
    decision = choose_execution_mode("composite_refund_chargeback", True, parallelism_policy)
    print(f"execution={decision.execution}")
    print("join_ready=", join_ready(["policy_findings", "order_summary", "chargeback_status"], join_policy, {"chargeback_mentioned_or_detected": True}))
    print("retry_timeout=", retry_allowed("timeout", 1, retry_policy))
    print("fallback=", choose_fallback("chargeback_lookup_unavailable", fallback_policy))
    print("safety_controls_enabled=", safety_controls_enabled(degradation_policy))
