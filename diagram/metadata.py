# metadata.py
from typing import Literal, Dict, Any

AbstractionLevel = Literal["molecular", "cellular", "system", "conceptual"]

class DiagramMetadata:
    def __init__(
        self,
        diagram_family: str,          
        abstraction_level: AbstractionLevel
    ):
        self.diagram_family = diagram_family
        self.abstraction_level = abstraction_level

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagram_family": self.diagram_family,
            "abstraction_level": self.abstraction_level
        }

    def __repr__(self):
        return f"Metadata({self.diagram_family}, {self.abstraction_level})"
