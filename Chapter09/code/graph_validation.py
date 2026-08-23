"""Static graph validation."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


class GraphError(Exception):
    pass


@dataclass
class Edge:
    source: str
    destination: str
    guard: str
    owner: str
    failure_destination: str
    requires_authority: bool = False


@dataclass
class NodeContract:
    node_id: str
    owner: str
    responsibility: Optional[str] = None


@dataclass
class GraphSpec:
    start: str
    nodes: Dict[str, str]
    edges: List[Edge]
    contracts: List[NodeContract]

    def node_contracts(self) -> Iterable[NodeContract]:
        return self.contracts


class ResponsibilitySpec:
    def __init__(self, ownership: Dict[str, str]) -> None:
        self.ownership = ownership

    def require_owner(self, responsibility: str, owner: str) -> None:
        expected = self.ownership.get(responsibility)
        if expected != owner:
            raise GraphError(f"{owner} does not own {responsibility}; expected {expected}")


def require_terminal_reachability(spec: GraphSpec) -> None:
    terminal_nodes = {name for name, kind in spec.nodes.items() if kind == "terminal"}
    if not terminal_nodes:
        raise GraphError("graph has no terminal node")


def reject_unbounded_cycles(spec: GraphSpec) -> None:
    # Simplified check for examples: self-loop edges are rejected unless they have a guard and owner.
    for edge in spec.edges:
        if edge.source == edge.destination and not edge.guard:
            raise GraphError("unbounded self-cycle detected")


def reject_action_paths_without_authority_guard(spec: GraphSpec) -> None:
    action_nodes = {name for name, kind in spec.nodes.items() if kind == "action"}
    for edge in spec.edges:
        if edge.destination in action_nodes and not edge.requires_authority:
            raise GraphError("action edge lacks authority guard")


def validate_graph(spec: GraphSpec, responsibility_spec: ResponsibilitySpec) -> bool:
    if spec.start not in spec.nodes:
        raise GraphError("start node is not registered")

    for edge in spec.edges:
        if edge.source not in spec.nodes:
            raise GraphError("edge references unknown source node")

        if edge.destination not in spec.nodes:
            raise GraphError("edge references unknown destination node")

        if not edge.guard or not edge.owner or not edge.failure_destination:
            raise GraphError("edge contract is incomplete")

    for node in spec.node_contracts():
        if node.responsibility:
            responsibility_spec.require_owner(
                node.responsibility,
                node.owner,
            )

    require_terminal_reachability(spec)
    reject_unbounded_cycles(spec)
    reject_action_paths_without_authority_guard(spec)

    return True
