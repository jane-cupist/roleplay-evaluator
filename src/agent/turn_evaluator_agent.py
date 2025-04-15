from langchain_core.language_models import BaseChatModel

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria


class TurnEvaluatorAgent(EvaluatorAgent):
    def __init__(self, model: BaseChatModel, criteria: EvaluationCriteria):
        super().__init__(model, criteria)

    def __call__(self, state: ChatState) -> ChatState:
        messages = state["messages"]

        evaluation = super().__call__(state, messages[-2:])

        criteria_scores = evaluation["score"]
        criteria_score_description = evaluation["description"]

        turn_score = {
            "turn": len(messages) // 2,
            "criteria_scores": criteria_scores,
            "score": super().calculate_score(criteria_scores),
            "description": criteria_score_description,
        }

        print("======== Turn Evaluator Agent ========")
        print(f"criteria_scores: {criteria_scores}")
        print(f"score: {super().calculate_score(criteria_scores)}")
        print(f"criteria_score_description: {criteria_score_description}")
        print(f"turn_score: {turn_score}")
        print("=====================================")
