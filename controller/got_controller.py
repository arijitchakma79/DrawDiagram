from dataclasses import dataclass
from typing import Any, List, Optional
import json

from pydantic import BaseModel

from executor.llm import run_task
from protocol.task_spec import TaskSpecification


# ---------- GoT CANDIDATE ----------

@dataclass
class GoTCandidate:
    output: Any
    score: float = 0.0
    critique: str | None = None


class CritiqueSchema(BaseModel):
    """Schema for critic responses: expects at least a numeric score."""
    score: float
    reason: str | None = None


# ---------- GoT CONTROLLER ----------

class GoTController:
    def __init__(self, model: str = "gpt-4o", temperature: float = 1.0):
        self.model = model
        self.temperature = temperature

    def run_task(
        self,
        task: TaskSpecification,
        parameters: dict,
        log_path: Optional[str] = None,
    ) -> List[GoTCandidate]:
        """
        Execute a TaskSpecification using Graph-of-Thoughts:
        - branching: sample multiple candidate outputs
        - optional critic scoring: score each candidate
        - pruning: sort candidates by score (best first)
        """

        candidates: List[GoTCandidate] = []

        # ---- 1. BRANCHING ----
        for _ in range(task.branching_factor):
            output = run_task(
                task=task,
                parameters=parameters,
                model=self.model,
                temperature=self.temperature,
            )
            candidates.append(GoTCandidate(output=output))

        # ---- 2. CRITIC SCORING (OPTIONAL) ----
        if task.critic_instruction:
            critic_spec = TaskSpecification(
                name=f"{task.name}_critic",
                system_instruction=task.critic_instruction,
                output_schema=CritiqueSchema,
            )

            for c in candidates:
                critique: CritiqueSchema = run_task(
                    task=critic_spec,
                    parameters=c.output.model_dump(),
                    model=self.model,
                    temperature=0.0,
                )

                c.score = critique.score
                c.critique = critique.reason

            # ---- 3. PRUNE / SORT ----
            candidates.sort(key=lambda c: c.score, reverse=True)

        # ---- 4. OPTIONAL JSON LOGGING ----
        if log_path:
            serializable_candidates = []
            for idx, c in enumerate(candidates):
                if hasattr(c.output, "model_dump"):
                    output_payload = c.output.model_dump()
                else:
                    # Fallback: best‑effort string representation
                    output_payload = str(c.output)

                serializable_candidates.append(
                    {
                        "index": idx,
                        "score": c.score,
                        "critique": c.critique,
                        "output": output_payload,
                    }
                )

            log_payload = {
                "task_name": task.name,
                "parameters": parameters,
                "candidates": serializable_candidates,
            }

            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(log_payload, f, ensure_ascii=False, indent=2)

        return candidates
