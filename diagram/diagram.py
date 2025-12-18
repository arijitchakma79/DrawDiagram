class Diagram:
    def __init__(self, metadata=None):
        self.nodes = {}
        self.edges = []
        self.constraints = []
        self.metadata = metadata

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def validate(self):
        return all(c.validate(self) for c in self.constraints)
