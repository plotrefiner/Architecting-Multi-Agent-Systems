"""Deterministic-first routing examples."""

def build_supervision_context(request, state):
    return {
        "request_text": request.text,
        "state_version": state.version,
        "purpose": "select_responsibilities_for_composite_support_case",
    }

def choose_route(request, state, classifier, supervisor):
    intent = classifier.classify(request.text)
    if intent == "refund_policy_question":
        return {"route": "policy_only", "supervisor_required": False}
    missing_fields = state.required_fields_missing(request, intent)
    if intent == "refund_case" and missing_fields:
        return {"route": "request_required_fields", "fields": missing_fields, "supervisor_required": False}
    if state.has_current_matching_approval:
        return {"route": "controller_validates_action", "supervisor_required": False}
    if intent == "composite_support_case":
        return supervisor.route(build_supervision_context(request, state))
    return {"route": "safe_escalation", "supervisor_required": False}
