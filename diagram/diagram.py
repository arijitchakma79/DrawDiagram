# diagram.py
from typing import Dict, List, Any

class Diagram:
    def __init__(self, metadata: Dict[str, Any] | None = None):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.constraints: List[Any] = []
        self.metadata = metadata or {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def validate(self):
        failures = []

        for constraint in self.constraints:
            valid, reason = constraint.validate(self)
            if not valid:
                failures.append({
                    "constraint": constraint.name,
                    "reason": reason or constraint.description
                })

        return len(failures) == 0, failures

    def to_dict(self) -> dict:
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "metadata": self.metadata
        }

    def __repr__(self):
        return f"Diagram(nodes={len(self.nodes)}, edges={len(self.edges)})"
