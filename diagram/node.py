class Node:
    def __init__(self, id: str, node_type: str, attributes=None):
        self.id = id
        self.node_type = node_type
        self.attributes = attributes or {}

    def __repr__(self):
        return f"Node({self.id}, {self.node_type})"