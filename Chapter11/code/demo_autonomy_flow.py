from plan_validation import ResponsibilityRegistry, validate_plan
from cost import select_lowest_cost_valid_plan
from autonomy import resolve_stop_condition


def main():
    registry = ResponsibilityRegistry({
        "retrieve_policy": "policy_retrieval_service",
        "retrieve_order": "order_lookup_service",
        "retrieve_chargeback_status": "chargeback_lookup_service",
    })
    plan = {
        "tasks": [
            {"responsibility": "retrieve_policy", "owner": "policy_retrieval_service", "output_contract": "policy_findings_v1"},
            {"responsibility": "retrieve_order", "owner": "order_lookup_service", "output_contract": "order_summary_v1"},
        ]
    }
    policy = {"maximum_tasks": 6, "prohibited_responsibilities": ["issue_refund"]}
    validation = validate_plan(plan, registry, policy)
    selected = select_lowest_cost_valid_plan([
        {"plan_id": "simple", "estimated_cost_usd": 0.02, "meets_requirements": False},
        {"plan_id": "composite", "estimated_cost_usd": 0.18, "meets_requirements": True},
    ])
    stop = resolve_stop_condition(
        "human_authority_required",
        {"stop_conditions": [{"condition": "human_authority_required", "outcome": "awaiting_human_review"}]},
    )
    print({"validation": validation.status, "selected_plan": selected["plan_id"], "stop": stop})


if __name__ == "__main__":
    main()
