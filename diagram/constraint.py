class Constraint:
    def __init__(self, name: str, description: str, fn):
        self.name = name
        self.description = description
        self.fn = fn

    def validate(self, diagram):
        return self.fn(diagram)
