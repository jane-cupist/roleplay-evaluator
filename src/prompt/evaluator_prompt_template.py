from dataclasses import dataclass

from interface.evaluation_criteria import EvaluationCriteria
from prompt.prompt_template import PromptParam, PromptTemplate


@dataclass
class EvaluatorPromptParam(PromptParam):
    messages: list
    criteria: EvaluationCriteria


class EvaluatorPromptTemplate(PromptTemplate):
    def __init__(self, template_name: str = "evaluator.j2"):
        super().__init__(template_name)

    def render(self, params: EvaluatorPromptParam) -> str:
        return self.template.render(params)
