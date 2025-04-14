from typing import Protocol


class EvaluationCriteria(Protocol):
    criterion: str
    description: str
    weight: float
