from __future__ import annotations


def validate_graph_spec(spec: dict) -> bool:
    required = {"graph_id", "state_owner", "start", "nodes", "edges"}
    if not required.issubset(spec):
        return False
    if spec["start"] not in spec["nodes"]:
        return False
    nodes = set(spec["nodes"])
    for edge in spec["edges"]:
        if len(edge) != 3:
            return False
        source, target, outcome = edge
        if source not in nodes or target not in nodes or not outcome:
            return False
    return True


def terminal_nodes(spec: dict) -> set[str]:
    return {name for name, kind in spec.get("nodes", {}).items() if kind == "terminal"}
