from pydantic import BaseModel
from typing import List, Literal

from protocol.task_spec import TaskSpecification

# ---------- FAMILY SELECTION ----------

class FamilyResponse(BaseModel):
    diagram_family: str

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

class NodeOut(BaseModel):
    id: str
    label: str
    node_type: Literal["entity", "process", "state", "variable", "region"]

class NodesResponse(BaseModel):
    nodes: List[NodeOut]

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
    name: str
    description: str

class ConstraintsResponse(BaseModel):
    constraints: List[ConstraintOut]

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
