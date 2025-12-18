from executor import run_task
from protocol import SELECT_DIAGRAM_FAMILY, ENUMERATE_NODES, DEFINE_CONSTRAINTS, CONNECT_EDGES


# Test topic
topic = 'photosynthesis'


print("Testing Diagram Family Selection")

controller = GoTController()

family_params = {"topic": topic}
family_result = run_task(SELECT_DIAGRAM_FAMILY, family_params)

print(f"Topic: {topic}")
print(f"Selected Family: {family_result.diagram_family}")
print()

print("Testing Node Generation")


# Test 2: Enumerate nodes
node_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "abstraction_level": "conceptual"
}
controller = GoTController()


results = controller.run_task(
    task=ENUMERATE_NODES,
    parameters={
        "topic": "photosynthesis",
        "diagram_family": "MECHANISTIC_PROCESS",
        "abstraction_level": "cellular"
    }
)

best_nodes = results[0].output

print(f"Topic: {topic}")
print(f"Diagram Family: {family_result.diagram_family}")
print(f"Number of nodes generated: {len(nodes_result.nodes)}")
print("\nNodes:")
print(nodes_result)


# Test 3: Define constraints
constraint_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "nodes": [{"id": node.id, "node_type": node.node_type} for node in nodes_result.nodes]
}
constraints_result = run_task(DEFINE_CONSTRAINTS, constraint_params)

print(f"Topic: {topic}")
print(f"Diagram Family: {family_result.diagram_family}")
print(f"Number of constraints generated: {len(constraints_result.constraints)}")
print("\nConstraints:")
for constraint in constraints_result.constraints:
    print(f"  - {constraint.name}: {constraint.description}")

print("\n" + "=" * 60)
print("Testing Edge Connection")
print("=" * 60)

# Test 4: Connect edges
edge_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "nodes": [{"id": node.id, "label": node.label, "node_type": node.node_type} for node in nodes_result.nodes],
    "constraints": [{"name": c.name, "description": c.description} for c in constraints_result.constraints]
}
edges_result = run_task(CONNECT_EDGES, edge_params)

print(f"Topic: {topic}")
print(f"Diagram Family: {family_result.diagram_family}")
print(f"Number of edges generated: {len(edges_result.edges)}")
print("\nEdges:")
# Create a lookup dictionary for node labels
node_lookup = {node.id: node.label for node in nodes_result.nodes}
for edge in edges_result.edges:
    source_label = node_lookup.get(edge.source, edge.source)
    target_label = node_lookup.get(edge.target, edge.target)
    print(f"  - {source_label} ({edge.source}) --[{edge.edge_label}]--> {target_label} ({edge.target})")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
