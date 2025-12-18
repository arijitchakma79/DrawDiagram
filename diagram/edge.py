class Edge:
    def __init__(self, source, target, edge_type: str, attributes=None):
        self.source = source
        self.target = target
        self.edge_type = edge_type
        self.attributes = attributes or {}

    def __repr__(self):
        return f"Edge({self.source.id} -> {self.target.id}, {self.edge_type})"
