from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from interface.agent import Agent
from interface.evaluation_criteria import EvaluationCriteria
from interface.evaluation_result import EvaluationResult
from prompt.evaluator_prompt_template import (
    EvaluatorPromptParam,
    EvaluatorPromptTemplate,
)
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
    def __init__(
        self,
        model: BaseChatModel,
        criteria: EvaluationCriteria,
        persona_name: str,
        character_name: str,
    ):
        super().__init__(model)
        self.criteria = criteria
        self.persona_name = persona_name
        self.character_name = character_name

    @retry_with_exponential_backoff(max_retries=5, initial_delay=1.0, max_delay=10.0)
    def __call__(self, messages: List[BaseMessage]) -> dict:
        result = self.model.with_structured_output(EvaluatorOutput).invoke(
            input=self.make_prompt(messages),
            config={"timeout": 60000},
        )

        return {
            "score": result.score,
            "description": result.description,
        }

    # TODO: 수정
    def get_character_name(self, message: BaseMessage) -> str:
        if message.type == "ai":
            return self.character_name
        else:
            return self.persona_name

    def make_prompt(self, messages: List[BaseMessage]) -> ChatPromptTemplate:
        message_contents = [
            f"{self.get_character_name(msg)}: {msg.content}" for msg in messages
        ]

        return EvaluatorPromptTemplate().render(
            EvaluatorPromptParam(
                messages=message_contents, criteria=self.criteria
            ).__dict__
        )

    def calculate_score(self, evaluation_result: EvaluationResult) -> float:
        total_score = 0

        for criterion, score in evaluation_result.items():
            criterion_info = next(
                (item for item in self.criteria if item["criterion"] == criterion),
                {"weight": 1},
            )
            total_score += score * criterion_info["weight"]

        return total_score
