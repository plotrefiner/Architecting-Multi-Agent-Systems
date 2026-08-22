"""Delegation authorization utilities."""

class RoutingError(Exception):
    pass

def authorize_delegation(task, registry, active_path, budget):
    if task.assigned_worker not in registry.workers_for(task.responsibility):
        raise RoutingError("worker lacks registered capability")
    if task.assigned_worker in active_path:
        raise RoutingError("delegation cycle detected")
    if task.delegation_depth > budget.maximum_depth:
        raise RoutingError("delegation depth exceeded")
    if budget.remaining_tasks < 1:
        raise RoutingError("delegation budget exhausted")
    if task.may_redelegate:
        raise RoutingError("worker redelegation is not permitted")
    return True
