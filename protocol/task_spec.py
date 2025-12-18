class TaskSpecification:
    def __init__(self, name, system_instruction, output_schema):
        self.name = name
        self.system_instruction = system_instruction
        self.output_schema = output_schema
