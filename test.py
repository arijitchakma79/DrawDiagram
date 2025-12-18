import json
import os

from executor import run_task
from protocol import (
    SELECT_DIAGRAM_FAMILY,
    ENUMERATE_NODES,
    DEFINE_CONSTRAINTS,
    CONNECT_EDGES,
)
from controller import GoTController


# Ensure debugging directory exists for intermediate logs
os.makedirs("debugging", exist_ok=True)

# Test topic
topic = "solar system"

print("Testing Diagram Family Selection")

# First, select the best diagram family for the topic.
family_params = {"topic": topic}
family_result = run_task(SELECT_DIAGRAM_FAMILY, family_params)

print(f"Topic: {topic}")
print(f"Selected Family: {family_result.diagram_family}")
print()

print("Testing Node Generation")

# Test 2: Enumerate nodes using the GoT controller
node_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "abstraction_level": "system",
}
controller = GoTController()

node_candidates = controller.run_task(
    task=ENUMERATE_NODES,
    parameters=node_params,
    log_path=os.path.join("debugging", "nodes_branches.json"),
)

# Take the best-scoring node set (first after sorting)
nodes_result = node_candidates[0].output

print(f"Topic: {topic}")
print(f"Diagram Family: {family_result.diagram_family}")
print(f"Number of nodes generated: {len(nodes_result.nodes)}")
print("\nNodes:")
print(nodes_result)

print("\nTesting Constraint Generation")

# Test 3: Define constraints using the GoT controller
constraint_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "nodes": [{"id": n.id, "node_type": n.node_type} for n in nodes_result.nodes],
}
constraint_candidates = controller.run_task(
    task=DEFINE_CONSTRAINTS,
    parameters=constraint_params,
    log_path=os.path.join("debugging", "constraints_branches.json"),
)
constraints_result = constraint_candidates[0].output

print(f"Number of constraints generated: {len(constraints_result.constraints)}")
print("\nConstraints:")
for c in constraints_result.constraints:
    print(f"  - {c.name}: {c.description}")

print("\nTesting Edge Generation")

# Test 4: Connect edges using the GoT controller
edge_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "nodes": [
        {"id": n.id, "label": n.label, "node_type": n.node_type}
        for n in nodes_result.nodes
    ],
    "constraints": [
        {"name": c.name, "description": c.description}
        for c in constraints_result.constraints
    ],
}
edge_candidates = controller.run_task(
    task=CONNECT_EDGES,
    parameters=edge_params,
    log_path=os.path.join("debugging", "edges_branches.json"),
)
edges_result = edge_candidates[0].output

print(f"Number of edges generated: {len(edges_result.edges)}")
print("\nEdges:")
node_lookup = {n.id: n.label for n in nodes_result.nodes}
for e in edges_result.edges:
    src_label = node_lookup.get(e.source, e.source)
    tgt_label = node_lookup.get(e.target, e.target)
    print(f"  - {src_label} ({e.source}) --[{e.edge_label}]--> {tgt_label} ({e.target})")

# Save final combined output
final_payload = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "nodes": [n.model_dump() for n in nodes_result.nodes],
    "constraints": [c.model_dump() for c in constraints_result.constraints],
    "edges": [e.model_dump() for e in edges_result.edges],
}

with open("final_output", "w", encoding="utf-8") as f:
    json.dump(final_payload, f, ensure_ascii=False, indent=2)
