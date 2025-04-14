import json
from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate

from agent.evaluator_agent import EvaluatorAgent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from interface.evaluation_result import EvaluationResult
from prompt.prompt_template import PromptTemplate


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

        state["evaluation_result"] = state.get(
            "evaluation_result",
            {
                "turn_scores": [],
                "total_score": {},
            },
        )

        state["evaluation_result"]["turn_scores"].append(turn_score)

        return state
