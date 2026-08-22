"""Worker result validation utilities."""

class ContractError(Exception):
    pass

class StateError(Exception):
    pass

class DeadlineError(Exception):
    pass

def validate_worker_result(result, delegation, registry, state):
    if result.delegation_id != delegation.delegation_id:
        raise ContractError("result does not match delegated task")
    if result.producer != delegation.assigned_worker:
        raise ContractError("unexpected producer")
    registry.validate(delegation.output_contract, result.payload)
    if not state.is_delegation_current(delegation.delegation_id, delegation.state_version):
        raise StateError("delegation is no longer current")
    if result.state_version != delegation.state_version:
        raise StateError("result was produced from a different state version")
    if result.created_at > delegation.deadline:
        raise DeadlineError("late result requires controller policy")
    registry.require_evidence_scope(result.evidence_refs, delegation.evidence_scope)
    return result.to_accepted_artifact()
