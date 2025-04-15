from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from interface.evaluation_criteria import EvaluationCriteria
from interface.evaluation_result import EvaluationResult


class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    decision: str
    evaluation_criterias: List[EvaluationCriteria]
    evaluation_result: EvaluationResult
    model: str
    turn_limit: int
