from langchain_core.language_models import BaseChatModel

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from utils.logger import evaluator_logger


class FinalEvaluatorAgent(EvaluatorAgent):
    def __init__(
        self,
        model: BaseChatModel,
        criteria: EvaluationCriteria,
        persona_name: str,
        character_name: str,
    ):
        super().__init__(model, criteria, persona_name, character_name)

    def __call__(self, state: ChatState) -> ChatState:
        evaluation = super().__call__(state["messages"])
        criteria_scores = evaluation["score"]
        criteria_score_description = evaluation["description"]

        result = {
            "criteria_scores": criteria_scores,
            "score": super().calculate_score(criteria_scores),
            "description": criteria_score_description,
        }

        evaluator_logger.info(f"final_score: {result}")
