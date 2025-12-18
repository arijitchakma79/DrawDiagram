from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from protocol.task_spec import TaskSpecification

# ---------- FAMILY SELECTION ----------

class FamilyResponse(BaseModel):
    """Response schema for diagram family selection."""
    diagram_family: str = Field(..., description="Selected diagram family")

SELECT_DIAGRAM_FAMILY = TaskSpecification(
    name="select_diagram_family",
    system_instruction="""
    Choose exactly ONE diagram family that best fits the given scientific topic.

    DIAGRAM FAMILIES:
    STRUCTURAL_ANATOMICAL
    MECHANISTIC_PROCESS
    CAUSAL_REGULATORY
    CYCLIC_PROCESS
    STATE_TRANSITION
    HIERARCHICAL_EVOLUTIONARY
    INTERACTION_NETWORK
    FIELD_GRADIENT
    ENERGY_CONSTRAINT
    TEMPORAL_EVOLUTION

    RULES:
    - Choose exactly one family
    - Do not explain your choice
    - Output JSON only
    """.strip(),
    output_schema=FamilyResponse,
)

# ---------- NODE ENUMERATION ----------

class SemanticAttributes(BaseModel):
    """Attributes for a diagram node."""
    description: str
    role: str

class NodeOut(BaseModel):
    """Output schema for a single diagram node."""
    id: str = Field(..., min_length=1, description="Unique identifier for the node")
    label: str = Field(..., min_length=1, description="Human-readable label")
    node_type: Literal["entity", "process", "state", "variable", "region"] = Field(
        ..., description="Type of the node"
    )
    attributes: Optional[SemanticAttributes] = Field(
        default=None, description="Optional semantic attributes"
    )

class NodesResponse(BaseModel):
    """Response schema for node enumeration."""
    nodes: List[NodeOut] = Field(..., description="List of diagram nodes")

ENUMERATE_NODES = TaskSpecification(
    name="enumerate_nodes",
    system_instruction="""
    Enumerate the required diagram-level nodes for the scientific diagram.

    RULES:
    - Nodes must correspond to elements typically drawn as boxes or circles
    - Do not include fine-grained subcomponents
    - Do not define edges
    - Do not explain your choices
    - Each node must have a unique id
    - Use only allowed node types
    - Keep the set minimal and within provided limits
    - Output JSON only
    """.strip(),
    output_schema=NodesResponse,
)

# ---------- CONSTRAINTS ----------

class ConstraintOut(BaseModel):
    """Output schema for a single constraint."""
    name: str = Field(..., min_length=1, description="Constraint name")
    description: str = Field(..., min_length=1, description="Constraint description")

class ConstraintsResponse(BaseModel):
    """Response schema for constraint definition."""
    constraints: List[ConstraintOut] = Field(..., description="List of diagram constraints")

DEFINE_CONSTRAINTS = TaskSpecification(
    name="define_constraints",
    system_instruction="""
Define scientific constraints that restrict valid diagrams.

RULES:
- Constraints must apply globally
- Do not define nodes or edges
- Do not explain constraints
- Keep the set minimal
- Output JSON only
""".strip(),
    output_schema=ConstraintsResponse,
)


# ---------- EDGES ----------

class EdgeAttributes(BaseModel):
    """Attributes for a diagram edge."""
    pass

class EdgeOut(BaseModel):
    """Output schema for a single diagram edge."""
    source: str = Field(..., min_length=1, description="Source node ID")
    target: str = Field(..., min_length=1, description="Target node ID")
    edge_label: str = Field(..., min_length=1, description="Relationship")
    attributes: Optional[EdgeAttributes] = Field(
        default=None, description="Optional edge attributes"
    )

class EdgesResponse(BaseModel):
    """Response schema for edge connection."""
    edges: List[EdgeOut] = Field(..., description="List of diagram edges")

CONNECT_EDGES = TaskSpecification(
    name="connect_edges",
    system_instruction="""
    Connect the given nodes with directed edges to form a scientifically valid diagram.

    RULES:
    - Use descriptive edge labels that indicate the relationship type
    - Do not invent new nodes
    - Do not explain your choices
    - No duplicate edges (same source, target, edge_label)
    - Avoid unnecessary edges
    - Respect the provided constraints
    - Output JSON only matching the schema
    """.strip(),
    output_schema=EdgesResponse,
)
