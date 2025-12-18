class Edge:
    def __init__(self, source, target, edge_label: str, attributes=None):
        self.source = source
        self.target = target
        self.edge_label = 
        self.attributes = attributes or {}

    def __repr__(self):
        return f"Edge({self.source.id} -> {self.target.id}, {self.edge_type})"
