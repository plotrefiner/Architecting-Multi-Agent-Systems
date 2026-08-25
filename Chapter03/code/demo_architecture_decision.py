from architecture_ladder import explain_ladder
from architecture_selector import select_architecture
from refund_rules import RefundCase, evaluate_refund_rules
from risk_value_matrix import classify_value_risk


def main() -> None:
    requirements = {
        "requires_external_knowledge": True,
        "requires_user_specific_data": True,
        "requires_action": False,
        "requires_dynamic_tool_choice": True,
    }

    recommendation = select_architecture(
        requirements=requirements,
        value="high",
        risk="high",
    )

    refund_case = RefundCase(
        order_id="order_123",
        delivery_age_days=18,
        return_window_days=30,
        product_category="standard",
        item_condition_known=True,
        refund_amount=129.99,
    )

    refund_decision = evaluate_refund_rules(refund_case)
    matrix_decision = classify_value_risk(value="high", risk="high")

    print("Architecture ladder levels:", len(explain_ladder()))
    print("Value-risk recommendation:", matrix_decision.recommendation)
    print("Selected architecture:", recommendation.selected_architecture)
    print("Why not simpler:", recommendation.why_not_simpler)
    print("Required controls:", recommendation.required_controls)
    print("Refund rules outcome:", refund_decision.outcome)


if __name__ == "__main__":
    main()
