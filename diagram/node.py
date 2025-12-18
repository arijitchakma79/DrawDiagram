# node.py
from typing import Dict, Any

class Node:
    def __init__(
        self,
        id: str,
        node_type: str,
        label: str,
        attributes: Dict[str, Any] | None = None
    ):
        self.id = id
        self.node_type = node_type
        self.label = label
        self.attributes = attributes or {}

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.node_type,
            "label": self.label,
            "attributes": self.attributes
        }

    def __repr__(self):
        return f"Node(id={self.id}, type={self.node_type}, label={self.label})"
