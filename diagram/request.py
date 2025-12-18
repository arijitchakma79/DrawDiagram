class DiagramRequest:
    def __init__(
        self,
        topic: str,
        abstraction_level: str,
        max_nodes: int = 8,
        max_edges: int = 12,
        num_candidates: int = 1,
    ):
        self.topic = topic
        self.abstraction_level = abstraction_level
        self.max_nodes = max_nodes
        self.max_edges = max_edges
        self.num_candidates = num_candidates