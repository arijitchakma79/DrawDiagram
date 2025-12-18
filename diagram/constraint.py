class Constraint:
    def __init__(self, name: str, description: str, fn):
        self.name = name
        self.description = description
        self.fn = fn  # fn(diagram) -> bool | (bool, str)

    def validate(self, diagram):
        result = self.fn(diagram)

        if isinstance(result, tuple):
            return result  # (bool, reason)

        return result, None