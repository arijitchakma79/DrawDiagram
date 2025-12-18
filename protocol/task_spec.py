class TaskSpecification:
    def __init__(
        self,
        name,
        system_instruction,
        output_schema,
        branching_factor: int = 1,          
        critic_instruction: str | None = None,  
        merge_strategy: str | None = None        
    ):
        self.name = name
        self.system_instruction = system_instruction
        self.output_schema = output_schema
        self.branching_factor = branching_factor
        self.critic_instruction = critic_instruction
        self.merge_strategy = merge_strategy
