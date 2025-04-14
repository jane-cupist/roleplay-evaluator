from typing import Annotated, List, TypedDict

from pydantic import BaseModel, Field


class TurnScore(TypedDict):
    turn: int
    criteria_scores: dict[str, int]
    score: float
    description: str


class TotalScore(TypedDict):
    criteria_scores: dict[str, int]
    score: float
    description: str


class EvaluationResult(TypedDict):
    turn_scores: List[TurnScore]
    total_score: TotalScore
