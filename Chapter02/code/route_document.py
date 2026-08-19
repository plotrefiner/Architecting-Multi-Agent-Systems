def route_document(document):
    document_type = classify_document(document)
    risk_level = classify_risk(document)

    if risk_level == "high":
        return "human_review"

    if document_type == "legal":
        return "legal_policy_extraction"

    if document_type == "financial":
        return "financial_validation"

    return "general_summary"
