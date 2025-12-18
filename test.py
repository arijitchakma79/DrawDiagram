from executor import run_task
from protocol import SELECT_DIAGRAM_FAMILY, ENUMERATE_NODES, DEFINE_CONSTRAINTS


# Test topic
topic = 'Life Cycle of butterfly'

print("=" * 60)
print("Testing Diagram Family Selection")
print("=" * 60)

# Test 1: Select diagram family
family_params = {"topic": topic}
family_result = run_task(SELECT_DIAGRAM_FAMILY, family_params)

print(f"Topic: {topic}")
print(f"Selected Family: {family_result.diagram_family}")
print()

print("=" * 60)
print("Testing Node Generation")
print("=" * 60)

# Test 2: Enumerate nodes
node_params = {
    "topic": topic,
    "diagram_family": family_result.diagram_family,
    "abstraction_level": "intermediate"
}
nodes_result = run_task(ENUMERATE_NODES, node_params)

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
print("All tests completed successfully!")
print("=" * 60)