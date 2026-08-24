def should_create_eval_case(correction_record: dict, feedback_classification: dict) -> bool:
    if feedback_classification.get("classification") == "business_exception":
        return bool(feedback_classification.get("should_add_eval_case"))
    return bool(correction_record.get("should_add_eval_case"))


def should_update_memory(correction_record: dict) -> bool:
    return bool(correction_record.get("should_update_memory"))
