# edge.py
from typing import Dict, Any

class Edge:
    def __init__(
        self,
        source: str,
        target: str,
        label: str,   # ← domain-specific, LLM-generated
        attributes: Dict[str, Any] | None = None
    ):
        self.source = source      # node id
        self.target = target      # node id
        self.label = label        # e.g. "catalyzes", "inhibits", "flows into"
        self.attributes = attributes or {}

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "attributes": self.attributes
        }

    def __repr__(self):
        return f"Edge({self.source} -[{self.label}]-> {self.target})"
