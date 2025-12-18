from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from protocol.task_spec import TaskSpecification



class FamilyResponse(BaseModel):
    """Response schema for diagram family selection."""
    diagram_family: str = Field(..., description="Selected diagram family")

SELECT_DIAGRAM_FAMILY = TaskSpecification(
    name="select_diagram_family",
    system_instruction="""
    Choose exactly ONE diagram family that best fits the given scientific topic.

    DIAGRAM FAMILIES:
    Flow
    Cycle
    Tree
    Network
    Timeline

    RULES:
    - Choose exactly one family
    - Do not explain your choice
    - Output JSON only
    """.strip(),
    output_schema=FamilyResponse,
    branching_factor=1,
    critic_instruction="""
    Score whether the selected diagram family fits the topic.
    Return a score from 1 to 5.
    Output JSON only: {"score": number}
    """
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
    - Do not define edges
    - Each node must have a unique id
    - Use only allowed node types
    - Nodes must be appropriate for the specified abstraction level
    - Output JSON only
    """.strip(),
    output_schema=NodesResponse,
    branching_factor=3,
    critic_instruction="""
    Score this node set for:
    - scientific completeness
    - minimality (no unnecessary nodes)
    - abstraction consistency

    Return a score from 1 to 5.
    Output JSON only: {"score": number}
    """
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
    branching_factor=2,
    critic_instruction="""
    Score whether these constraints are:
    - scientifically meaningful
    - not redundant
    - applicable globally

    Return a score from 1 to 5.
    Output JSON only.
    """
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
    - Avoid unnecessary edges
    - Respect the provided constraints
    - Output JSON only matching the schema
    """.strip(),
    output_schema=EdgesResponse,
    branching_factor=3,
    critic_instruction="""
    Evaluate the edges for:
    - scientific accuracy
    - meaningful edge labels
    - no redundancy
    - correct directionality

    Penalize vague labels like "related to".

    Return a score from 1 to 5.
    Output JSON only.
    """
)
