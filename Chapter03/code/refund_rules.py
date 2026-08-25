from dataclasses import dataclass


@dataclass(frozen=True)
class RefundCase:
    order_id: str
    delivery_age_days: int
    return_window_days: int
    product_category: str
    item_condition_known: bool
    refund_amount: float


@dataclass(frozen=True)
class RefundDecision:
    eligible: bool
    outcome: str
    reasons: list[str]
    requires_human_review: bool


NON_RETURNABLE_CATEGORIES = {
    "final_sale",
    "personalized",
    "hazardous_material",
}


def evaluate_refund_rules(case: RefundCase, high_value_threshold: float = 500.0) -> RefundDecision:
    reasons = []
    requires_review = False

    if case.delivery_age_days > case.return_window_days:
        reasons.append("outside_return_window")

    if case.product_category in NON_RETURNABLE_CATEGORIES:
        reasons.append("non_returnable_category")

    if not case.item_condition_known:
        reasons.append("missing_item_condition")
        requires_review = True

    if case.refund_amount >= high_value_threshold:
        reasons.append("high_value_refund")
        requires_review = True

    if reasons:
        if requires_review:
            return RefundDecision(
                eligible=False,
                outcome="human_review_required",
                reasons=reasons,
                requires_human_review=True,
            )

        return RefundDecision(
            eligible=False,
            outcome="not_eligible",
            reasons=reasons,
            requires_human_review=False,
        )

    return RefundDecision(
        eligible=True,
        outcome="eligible_standard_case",
        reasons=[],
        requires_human_review=False,
    )
