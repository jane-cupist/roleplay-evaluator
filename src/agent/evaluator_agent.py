from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from interface.agent import Agent
from interface.chat_state import ChatState
from interface.evaluation_criteria import EvaluationCriteria
from interface.evaluation_result import EvaluationResult
from prompt.prompt_template import PromptTemplate
from utils.retry_utils import retry_with_exponential_backoff

evlautor_output_schema = {
    "title": "Evaluation Result",
    "description": "evaluation result",
    "type": "object",
    "properties": {
        "score": {"type": "object", "description": "evaluation result score"},
        "description": {
            "type": "string",
            "description": "evaluation result description",
        },
    },
    "required": ["score", "description"],
}


class EvaluatorOutput(BaseModel):
    score: dict = Field(description="evaluation result score")
    description: str = Field(description="evaluation result description")


class EvaluatorAgent(Agent):
    def __init__(self, model: BaseChatModel, criteria: EvaluationCriteria):
        super().__init__(model)
        self.criteria = criteria

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, messages: List[BaseMessage]) -> dict:

        result = self.model.with_structured_output(EvaluatorOutput).invoke(
            self.make_prompt(messages),
            {"timeout": 60000},
        )

        return {
            "score": result.score,
            "description": result.description,
        }

    def make_prompt(self, messages: List[BaseMessage]) -> ChatPromptTemplate:
        message_contents = [msg.content for msg in messages]
        return PromptTemplate().render_evaluator_prompt(message_contents, self.criteria)

    def calculate_score(self, evaluation_result: EvaluationResult) -> float:
        total_score = 0

        for criterion, score in evaluation_result.items():
            criterion_info = next(
                (item for item in self.criteria if item["criterion"] == criterion),
                {"weight": 1},
            )
            total_score += score * criterion_info["weight"]

        return total_score
