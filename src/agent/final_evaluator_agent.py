from langchain_core.language_models import BaseChatModel

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from utils.logger import evaluator_logger


class FinalEvaluatorAgent(EvaluatorAgent):
    def __init__(self, model: BaseChatModel, criteria: EvaluationCriteria):
        super().__init__(model, criteria)

    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]

        evaluation = super().__call__(messages)

        result = {
            "criteria_scores": evaluation["score"],
            "score": super().calculate_score(evaluation["score"]),
            "description": evaluation["description"],
        }

        evaluator_logger.info(f"final_score: {result}")
