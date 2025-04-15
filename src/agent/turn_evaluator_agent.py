from langchain_core.language_models import BaseChatModel

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from utils.logger import evaluator_logger


class TurnEvaluatorAgent(EvaluatorAgent):
    def __init__(self, model: BaseChatModel, criteria: EvaluationCriteria):
        super().__init__(model, criteria)

    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]

        evaluation = super().__call__(messages[-2:])

        criteria_scores = evaluation["score"]
        criteria_score_description = evaluation["description"]

        result = {
            "turn": len(messages) // 2,
            "criteria_scores": criteria_scores,
            "score": super().calculate_score(criteria_scores),
            "description": criteria_score_description,
        }

        evaluator_logger.info(f"turn_score: {result}")
